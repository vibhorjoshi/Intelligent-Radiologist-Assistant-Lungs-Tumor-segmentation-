from flask import Flask, request, jsonify
import os
from model.model import load_model,ResNet15
from utils.report_generator import  PDFReport , footer,add_report_content,add_scan_images,generate_report
from utils.bulk_upload import allowed_file,bulk_upload
from torchvision import transforms

app = Flask(__name__)

# Load the trained model
model = load_model()
model.eval()  # Set the model to evaluation mode

# Define preprocessing transformations (resize to match the input size expected by the model)
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Prediction function for single file
def predict(file, model):
    """
    Process the uploaded file and predict the classification and segmentation result.

    Args:
        file (werkzeug.datastructures.FileStorage): Uploaded file.
        model (torch.nn.Module): Loaded model.

    Returns:
        dict: Dictionary containing classification and segmentation results.
    """
    # Convert uploaded file to an image
    image = Image.open(file).convert('RGB')
    
    # Preprocess the image
    image_tensor = preprocess(image).unsqueeze(0)  # Add batch dimension
    
    # Perform model inference
    with torch.no_grad():
        classification_output, segmentation_output = model(image_tensor)
    
    # Post-process the model outputs
    classification = torch.argmax(classification_output, dim=1).item()
    segmentation = segmentation_output.squeeze().cpu().numpy()

    # Create a dictionary with classification and segmentation result
    result = {
        'classification': 'Tumor' if classification == 1 else 'No Tumor',
        'segmentation': segmentation.tolist()  # Convert segmentation mask to list (can return image as well)
    }

    return result

# Bulk upload handling function
def handle_bulk_upload(files, model):
    """
    Handle bulk upload of multiple files for processing.

    Args:
        files (list of werkzeug.datastructures.FileStorage): List of uploaded files.
        model (torch.nn.Module): Loaded model.

    Returns:
        list of dict: List of dictionaries containing classification and segmentation results for each file.
    """
    results = []
    
    for file in files:
        # Call the predict function for each file
        result = predict(file, model)
        results.append(result)
    
    return results

# Report generation (for demonstration purposes, it just formats the result)
def generate_report(result):
    """
    Generate a sample report from the prediction results.

    Args:
        result (dict): Prediction result containing classification and segmentation.

    Returns:
        dict: A sample report.
    """
    report = {
        'Report': f"Classification: {result['classification']}",
        'Segmentation': result['segmentation']  # Can add more details or save as an image file
    }
    
    return report

@app.route('/predict', methods=['POST'])
def predict_scan():
    """
    Endpoint to predict classification and segmentation for a single file.
    """
    file = request.files['file']
    
    # Preprocess and predict
    result = predict(file, model)
    
    # Generate report
    report = generate_report(result)
    
    return jsonify(report)

@app.route('/bulk-upload', methods=['POST'])
def bulk_upload():
    """
    Endpoint to handle bulk uploads and generate reports for each file.
    """
    files = request.files.getlist('files')  # Retrieve the list of files uploaded
    
    # Process each file and return reports
    reports = handle_bulk_upload(files, model)
    
    return jsonify(reports)

if __name__ == '__main__':
    app.run(debug=True)