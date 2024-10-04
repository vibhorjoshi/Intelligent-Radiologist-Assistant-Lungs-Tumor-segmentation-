// dashboard.js

document.getElementById('bulk-upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Get the selected files from the form input
    let filesInput = document.getElementById('files');
    let files = filesInput.files;

    if (files.length === 0) {
        alert("Please select files to upload.");
        return;
    }

    // Create a FormData object to hold the files
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    try {
        // Make the POST request to upload files and generate reports
        let response = await fetch('/bulk_upload', {
            method: 'POST',
            body: formData
        });

        // Parse the JSON response
        let result = await response.json();

        // Check if the upload was successful
        if (response.ok && result.success) {
            displayReports(result.reports); // Display the reports on the UI
        } else {
            alert("Error: " + (result.error || "Unknown error occurred."));
        }

    } catch (error) {
        console.error("Error uploading files:", error);
        alert("An error occurred while uploading files.");
    }
});

// Function to display the generated reports
function displayReports(reportPaths) {
    let reportSection = document.getElementById('report-section');
    reportSection.innerHTML = ''; // Clear previous reports

    // Create report links
    reportPaths.forEach(function(reportPath) {
        let reportLink = document.createElement('a');
        reportLink.href = reportPath;
        reportLink.target = '_blank';
        reportLink.innerText = `View Report: ${reportPath}`;
        reportSection.appendChild(reportLink);
        reportSection.appendChild(document.createElement('br'));
    });
}