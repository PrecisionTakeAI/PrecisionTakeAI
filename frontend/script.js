# Create script.js
const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', function()  {
  // Test backend connection
  fetch(`${API_URL}/health`)
    .then(response => response.json())
    .then(data => console.log('Backend connection successful:', data))
    .catch(error => console.error('Error connecting to backend:', error));
  
  // Add code to fetch and display symbols
  fetch(`${API_URL}/api/symbols`)
    .then(response => response.json())
    .then(data => {
      console.log('Symbols data:', data);
      // You could update the UI with this data
    })
    .catch(error => console.error('Error fetching symbols:', error));
  
  // Rest of your existing code...
  const demoBtn = document.getElementById('demo-btn');
  const demoArea = document.getElementById('demo-area');
  // ... other existing code ...
});



cat > ~/precisiontake/frontend/script.js << 'EOF'
document.addEventListener('DOMContentLoaded', function() {
  const demoBtn = document.getElementById('demo-btn');
  const demoArea = document.getElementById('demo-area');
  const analyzeBtn = document.getElementById('analyze-btn');
  const resultsArea = document.getElementById('results');
  const fileInput = document.getElementById('pdf-upload');
  
  demoBtn.addEventListener('click', function() {
    demoArea.style.display = 'block';
    demoBtn.textContent = 'Hide Demo';
    
    // Toggle demo area visibility
    if (demoArea.style.display === 'block') {
      demoArea.style.display = 'none';
      demoBtn.textContent = 'Try Demo';
    } else {
      demoArea.style.display = 'block';
      demoBtn.textContent = 'Hide Demo';
    }
  });
  
  analyzeBtn.addEventListener('click', function() {
    if (!fileInput.files.length) {
      alert('Please select a PDF file first');
      return;
    }
    
    // In a real implementation, this would send the file to the backend
    // For now, we'll just show a simulated result
    resultsArea.style.display = 'block';
    
    // Simulate API call delay
    setTimeout(function() {
      const resultsContainer = document.querySelector('.results-container');
      resultsContainer.innerHTML = `
        <h4>Analysis Complete</h4>
        <p><strong>Symbols Detected:</strong> 24 plumbing fixtures</p>
        <p><strong>Pipe Length:</strong> 142.5 feet</p>
        <p><strong>Estimated Materials:</strong></p>
        <ul>
          <li>PVC Pipe (1"): 86.3 feet</li>
          <li>PVC Pipe (2"): 56.2 feet</li>
          <li>Elbows (1"): 12 units</li>
          <li>Elbows (2"): 8 units</li>
          <li>T-Joints: 6 units</li>
        </ul>
        <p><strong>Confidence Score:</strong> 98.7%</p>
      `;
    }, 2000);
  });
});
EOF