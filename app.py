from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
from paper_summarizer import PaperSummarizer
import tempfile
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the summarizer
summarizer = PaperSummarizer()

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload interface."""
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize_file():
    """API endpoint to summarize uploaded file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload PDF or TXT files.'}), 400
        
        # Get metadata from form
        metadata = {
            'title': request.form.get('title', ''),
            'authors': request.form.get('authors', ''),
            'venue_year': request.form.get('venue_year', ''),
            'doi_or_arxiv': request.form.get('doi_or_arxiv', '')
        }
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Determine file type and summarize
            if filename.lower().endswith('.pdf'):
                result = summarizer.summarize_paper(filepath, 'pdf', metadata)
            else:  # txt file
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                result = summarizer.summarize_paper(text, 'text', metadata)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'markdown': result['markdown'],
                'json': result['json'],
                'metadata': result['metadata']
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({
            'error': f'Error processing file: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/summarize_url', methods=['POST'])
def summarize_url():
    """API endpoint to summarize paper from URL."""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        metadata = data.get('metadata', {})
        
        result = summarizer.summarize_paper(url, 'url', metadata)
        
        return jsonify({
            'success': True,
            'markdown': result['markdown'],
            'json': result['json'],
            'metadata': result['metadata']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing URL: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/summarize_text', methods=['POST'])
def summarize_text():
    """API endpoint to summarize raw text."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        metadata = data.get('metadata', {})
        
        result = summarizer.summarize_paper(text, 'text', metadata)
        
        return jsonify({
            'success': True,
            'markdown': result['markdown'],
            'json': result['json'],
            'metadata': result['metadata']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing text: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'PaperSummarizer'})

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting PaperSummarizer Web Application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
