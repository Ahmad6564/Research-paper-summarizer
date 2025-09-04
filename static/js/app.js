// PaperSummarizer Frontend JavaScript

class PaperSummarizer {
    constructor() {
        this.initializeEventListeners();
        this.setupFormValidation();
    }

    initializeEventListeners() {
        // File form submission
        document.getElementById('fileForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFileSubmission();
        });

        // URL form submission
        document.getElementById('urlForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleUrlSubmission();
        });

        // Text form submission
        document.getElementById('textForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleTextSubmission();
        });

        // File input change handler
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.validateFile(e.target.files[0]);
        });
    }

    setupFormValidation() {
        // Real-time validation for URL input
        document.getElementById('urlInput').addEventListener('input', (e) => {
            const url = e.target.value;
            const isValid = this.isValidUrl(url);
            
            if (url && !isValid) {
                e.target.classList.add('is-invalid');
            } else {
                e.target.classList.remove('is-invalid');
            }
        });
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    validateFile(file) {
        if (!file) return false;

        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = ['application/pdf', 'text/plain'];
        
        if (file.size > maxSize) {
            this.showError('File size exceeds 16MB limit.');
            return false;
        }

        if (!allowedTypes.includes(file.type)) {
            this.showError('Please upload a PDF or TXT file.');
            return false;
        }

        return true;
    }

    async handleFileSubmission() {
        const form = document.getElementById('fileForm');
        const formData = new FormData(form);
        const file = document.getElementById('fileInput').files[0];

        if (!file || !this.validateFile(file)) {
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError(result.error || 'An error occurred while processing the file.');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async handleUrlSubmission() {
        const url = document.getElementById('urlInput').value.trim();

        if (!url || !this.isValidUrl(url)) {
            this.showError('Please enter a valid URL.');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/api/summarize_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    metadata: {}
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError(result.error || 'An error occurred while processing the URL.');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async handleTextSubmission() {
        const text = document.getElementById('textInput').value.trim();

        if (!text) {
            this.showError('Please enter some text to analyze.');
            return;
        }

        if (text.length < 100) {
            this.showError('Please provide more text for meaningful analysis (minimum 100 characters).');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/api/summarize_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    metadata: {}
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError(result.error || 'An error occurred while processing the text.');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    displayResults(result) {
        // Display Markdown content
        const markdownContent = document.getElementById('markdownContent');
        if (typeof marked !== 'undefined') {
            markdownContent.innerHTML = marked.parse(result.markdown);
        } else {
            // Fallback: display as preformatted text
            markdownContent.innerHTML = `<pre>${this.escapeHtml(result.markdown)}</pre>`;
        }

        // Display JSON content
        const jsonContent = document.getElementById('jsonContent');
        jsonContent.textContent = JSON.stringify(result.json, null, 2);

        // Show results section
        this.showResults();

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }

    showLoading() {
        document.getElementById('loadingIndicator').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loadingIndicator').style.display = 'none';
    }

    showError(message) {
        const errorAlert = document.getElementById('errorAlert');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorAlert.style.display = 'block';
        
        // Scroll to error
        errorAlert.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }

    hideError() {
        document.getElementById('errorAlert').style.display = 'none';
    }

    showResults() {
        document.getElementById('resultsSection').style.display = 'block';
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Copy to clipboard functionality
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent || element.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const button = event.target.closest('button');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-primary');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            // Show success feedback
            const button = event.target.closest('button');
            const originalText = button.innerHTML;
            
            button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        } catch (err) {
            console.error('Fallback copy failed: ', err);
        }
        
        document.body.removeChild(textArea);
    });
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PaperSummarizer();
    
    // Add some UI enhancements
    addUIEnhancements();
});

function addUIEnhancements() {
    // Add drag and drop functionality for file input
    const fileInput = document.getElementById('fileInput');
    const fileForm = document.getElementById('fileForm');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileForm.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileForm.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileForm.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        fileForm.classList.add('border-primary', 'bg-light');
    }
    
    function unhighlight(e) {
        fileForm.classList.remove('border-primary', 'bg-light');
    }
    
    fileForm.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            // Trigger change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
    
    // Add tooltips for better UX
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}
