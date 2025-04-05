// API URL Configuration
const API_URL = 'http://127.0.0.1:3000';

document.addEventListener('DOMContentLoaded', function()  {
    // PDF Upload Functionality
    const pdfUploadInput = document.getElementById('pdf-upload');
    const pdfPlaceholder = document.getElementById('pdf-placeholder');
    const pdfAnalysisStatus = document.getElementById('pdf-analysis-status');
    const pdfAnalysisResults = document.getElementById('pdf-analysis-results');
    
    if (pdfUploadInput) {
        // Handle file selection
        pdfUploadInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file && file.type === 'application/pdf') {
                uploadAndAnalyzePDF(file);
            } else {
                alert('Please select a valid PDF file.');
            }
        });
    }
    
    // Handle drag and drop
    const pdfViewer = document.getElementById('pdf-viewer');
    
    if (pdfViewer) {
        pdfViewer.addEventListener('dragover', function(e) {
            e.preventDefault();
            pdfViewer.classList.add('drag-over');
        });
        
        pdfViewer.addEventListener('dragleave', function() {
            pdfViewer.classList.remove('drag-over');
        });
        
        pdfViewer.addEventListener('drop', function(e) {
            e.preventDefault();
            pdfViewer.classList.remove('drag-over');
            
            const file = e.dataTransfer.files[0];
            if (file && file.type === 'application/pdf') {
                uploadAndAnalyzePDF(file);
            } else {
                alert('Please drop a valid PDF file.');
            }
        });
    }
    
    // Function to upload and analyze PDF
    function uploadAndAnalyzePDF(file) {
        // Show loading status
        if (pdfPlaceholder) pdfPlaceholder.style.display = 'none';
        if (pdfAnalysisStatus) pdfAnalysisStatus.style.display = 'block';
        if (pdfAnalysisResults) pdfAnalysisResults.style.display = 'none';
        
        // Create form data for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Send file to backend for analysis
        fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Hide loading status
            if (pdfAnalysisStatus) pdfAnalysisStatus.style.display = 'none';
            if (pdfAnalysisResults) pdfAnalysisResults.style.display = 'block';
            
            // Display results
            if (document.getElementById('symbols-count'))
                document.getElementById('symbols-count').textContent = data.symbols.count;
            if (document.getElementById('pipe-length'))
                document.getElementById('pipe-length').textContent = data.symbols.total_pipe_length.toFixed(1);
            if (document.getElementById('confidence-score'))
                document.getElementById('confidence-score').textContent = data.symbols.confidence_score;
            if (document.getElementById('analysis-time'))
                document.getElementById('analysis-time').textContent = data.analysis_time;
            
            // Display materials
            const materialsList = document.getElementById('materials-list');
            if (materialsList) {
                materialsList.innerHTML = '';
                
                data.symbols.materials.forEach(material => {
                    const materialItem = document.createElement('div');
                    materialItem.className = 'material-item';
                    materialItem.innerHTML = `
                        <span class="material-name">${material.type}</span>
                        <span class="material-quantity">${material.quantity}</span>
                    `;
                    materialsList.appendChild(materialItem);
                });
            }
            
            // Update the PDF Analysis Status section in the main UI if it exists
            updateMainUIWithResults(data);
        })
        .catch(error => {
            // Hide loading status
            if (pdfAnalysisStatus) pdfAnalysisStatus.style.display = 'none';
            if (pdfAnalysisResults) pdfAnalysisResults.style.display = 'block';
            
            // Display error
            if (pdfAnalysisResults) {
                pdfAnalysisResults.innerHTML = `
                    <h3>Analysis Error</h3>
                    <p>There was an error analyzing your PDF: ${error.message}</p>
                    <p>Please try again with a different file or contact support.</p>
                `;
            }
            console.error('Error analyzing PDF:', error);
        });
    }
    
    // Function to update the main UI with analysis results
    function updateMainUIWithResults(data) {
        // This function can be expanded to update other parts of the UI
        console.log('Analysis results:', data);
    }
    
    // Also handle the "Try Demo" button if it exists
    const demoBtn = document.getElementById('demo-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', function() {
            // Scroll to the PDF viewer section
            const pdfViewerSection = document.querySelector('section:has(#pdf-viewer)');
            if (pdfViewerSection) {
                pdfViewerSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
});

        
        // Update Recent Activity
        const activityTimeline = document.querySelector('.activity-timeline');
        if (activityTimeline) {
            const now = new Date();
            const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const newActivity = document.createElement('div');
            newActivity.className = 'activity-item';
            newActivity.innerHTML = `
                <div class="activity-time">${timeString}</div>
                <div class="activity-content">PDF uploaded: ${data.file_info.filename}</div>
            `;
            
            // Insert at the beginning
            activityTimeline.insertBefore(newActivity, activityTimeline.firstChild);
            
            // Add analysis completed activity
            const analysisActivity = document.createElement('div');
            analysisActivity.className = 'activity-item';
            analysisActivity.innerHTML = `
                <div class="activity-time">${timeString}</div>
                <div class="activity-content">PDF analysis completed (${data.analysis_time})</div>
            `;
            
            // Insert at the beginning
            activityTimeline.insertBefore(analysisActivity, activityTimeline.firstChild);
        }
    }
});
