"""
Production runner for PaperSummarizer
"""

import os
from app import app
from config import config

if __name__ == '__main__':
    # Get environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Load configuration
    app.config.from_object(config.get(env, config['default']))
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("=" * 60)
    print("🚀 PaperSummarizer - Academic Paper Analysis Tool")
    print("=" * 60)
    print(f"Environment: {env}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
