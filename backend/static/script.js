document.addEventListener('DOMContentLoaded', () => {
    // API Configurations
    // Update API_URL to use relative path for dynamic production routes
    const API_URL = '/summarize';

    // UI Elements
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const subBtn = document.getElementById('summarize-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultContainer = document.getElementById('result-container');
    const summaryOutput = document.getElementById('summary-output');
    const copyBtn = document.getElementById('copy-btn');
    
    // Inputs
    const rawTextNode = document.getElementById('raw-text');
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const fileNameDisplay = document.getElementById('file-name');

    let currentMode = 'text'; // 'text' | 'file'
    let selectedFile = null;

    // Tabs Logic
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            currentMode = tab.dataset.tab;
            document.getElementById(`${currentMode}-tab`).classList.add('active');
        });
    });

    // File Drop Zone Logic
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (file.type !== "text/plain" && file.type !== "application/pdf") {
            // Very rudimentary check. We rely on the backend for proper validation.
            if (!file.name.endsWith('.txt') && !file.name.endsWith('.pdf')) {
                alert("Please select a .txt or .pdf file.");
                return;
            }
        }
        selectedFile = file;
        fileNameDisplay.textContent = `Selected: ${file.name}`;
    }

    // Submit Action
    subBtn.addEventListener('click', async () => {
        // Validate
        if (currentMode === 'text') {
            if (!rawTextNode.value.trim()) {
                alert("Please enter some text to summarize.");
                return;
            }
        } else {
            if (!selectedFile) {
                alert("Please upload a file.");
                return;
            }
        }

        // Hide old results & show loader
        resultContainer.classList.add('hidden');
        loadingOverlay.classList.remove('hidden');

        try {
            const formData = new FormData();
            if (currentMode === 'text') {
                formData.append('text', rawTextNode.value.trim());
            } else {
                formData.append('file', selectedFile);
            }

            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData // multipart/form-data will be set automatically by fetch
            });

            const data = await response.json();

            if (response.ok) {
                if (data.summary) {
                    summaryOutput.textContent = data.summary;
                    resultContainer.classList.remove('hidden');
                    // smoothly scroll to result
                    setTimeout(() => {
                        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    alert("An unknown error occurred on the server.");
                }
            } else {
                alert(`Error: ${data.error || 'Server error occurred'}`);
            }

        } catch (error) {
            console.error(error);
            alert("Failed to reach the server. Is it running? Error: " + error.message);
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    });

    // Copy to Clipboard
    copyBtn.addEventListener('click', async () => {
        if (!summaryOutput.textContent) return;
        
        try {
            await navigator.clipboard.writeText(summaryOutput.textContent);
            // Visual feedback
            const originalHTML = copyBtn.innerHTML;
            copyBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
            setTimeout(() => {
                copyBtn.innerHTML = originalHTML;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy', err);
        }
    });
});
