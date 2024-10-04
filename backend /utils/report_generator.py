# report_generator.py

import os
from fpdf import FPDF
from datetime import datetime
from model.model import segment_lung_tumor  # Assume the model is imported from model.py
from PIL import Image
import numpy as np

# Directory to save the reports
REPORTS_FOLDER = 'reports'

# Ensure the reports folder exists
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

class PDFReport(FPDF):
    """
    Class to create a PDF report using the FPDF library.
    """
    def header(self):
        # Title and timestamp for the report
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Lung CT Scan Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Footer with page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_report_content(self, report_data):
        # Add text content to the report
        self.set_font('Arial', '', 12)
        for key, value in report_data.items():
            self.cell(0, 10, f'{key}: {value}', 0, 1)
        self.ln(10)

    def add_scan_images(self, image_path):
        # Add images of the scan to the report (e.g., segmentation results)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'CT Scan Image:', 0, 1, 'L')
        self.image(image_path, x=10, y=None, w=100)
        self.ln(10)


def generate_report(ct_scan_path):
    """
    Function to generate a report after processing the CT scan.
    
    Args:
        ct_scan_path (str): The path to the uploaded CT scan.
        
    Returns:
        str: The path to the generated PDF report.
    """

    # Step 1: Process the CT scan with the model (segmentation and tumor detection)
    try:
        # Assuming the model's output is a segmented image
        segmentation_result, tumor_details = segment_lung_tumor(ct_scan_path)  # Model processing here

        # Step 2: Save the segmented result image (as PNG)
        segmented_image_path = os.path.splitext(ct_scan_path)[0] + "_segmented.png"
        Image.fromarray((segmentation_result * 255).astype(np.uint8)).save(segmented_image_path)

        # Step 3: Create the PDF report
        report_data = {
            "Patient ID": "12345",
            "Doctor Name": "Dr. Smith",
            "Tumor Presence": tumor_details["tumor_detected"],
            "Tumor Size": f'{tumor_details["tumor_size"]} mm',
            "Lung Condition": tumor_details.get("lung_condition", "Normal"),
            "Date of Scan": datetime.now().strftime("%Y-%m-%d"),
            "Model Confidence": f'{tumor_details["confidence"]} %'
        }

        # Step 4: Create and format the PDF
        report_pdf = PDFReport()
        report_pdf.add_page()
        report_pdf.add_report_content(report_data)
        report_pdf.add_scan_images(segmented_image_path)

        # Step 5: Save the PDF report
        report_filename = f'{REPORTS_FOLDER}/report_{os.path.basename(ct_scan_path).split(".")[0]}.pdf'
        report_pdf.output(report_filename)

        return report_filename  # Return the path to the generated report

    except Exception as e:
        print(f"Error generating report: {e}")
        raise


if __name__ == "__main__":
    # Example: Generating a report for a sample CT scan
    sample_ct_scan = "uploads/sample_ct_scan.dcm"
    report_path = generate_report(sample_ct_scan)
    print(f"Report generated: {report_path}")
