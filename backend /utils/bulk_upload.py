# bulk_upload.py
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import zipfile
import shutil
from model import generate_report  # This assumes you have a generate_report function in model.py

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}

# Create a blueprint for bulk upload
bulk_upload_bp = Blueprint('bulk_upload', __name__)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bulk_upload_bp.route('/bulk_upload', methods=['POST'])
def bulk_upload():
    # Check if the request contains files
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')

    # Create a directory to store uploaded files temporarily
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_paths = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_paths.append(file_path)

    # Assume the model processes the files here and generates reports
    try:
        # This function should process files and return a report (dummy function below)
        report_paths = []
        for file_path in file_paths:
            report_path = generate_report(file_path)
            report_paths.append(report_path)
        
        # Cleanup the uploaded files after processing
        for file_path in file_paths:
            os.remove(file_path)

        return jsonify({
            'success': True,
            'message': 'Reports generated successfully',
            'reports': report_paths  # Paths to the generated reports
        }), 200

    except Exception as e:
        # Handle exceptions and cleanup if necessary
        for file_path in file_paths:
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500
