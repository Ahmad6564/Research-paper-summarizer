"""
Configuration settings for PaperSummarizer
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
    
    # Processing settings
    MAX_TEXT_LENGTH = 1000000  # 1MB of text
    MIN_TEXT_LENGTH = 100      # Minimum text for analysis
    
    # Output settings
    MAX_CONTRIBUTIONS = 10
    MAX_EQUATIONS = 20
    MAX_RESULTS = 15
    MAX_CITATIONS = 30
    MAX_GLOSSARY_TERMS = 15
    
    # API settings
    REQUEST_TIMEOUT = 300  # 5 minutes
    RETRY_ATTEMPTS = 3
    
    # Model settings
    SPACY_MODEL = "en_core_web_sm"
    
    # Validation rules
    STRICT_FAITHFULNESS = True
    PRESERVE_CITATIONS = True
    PRESERVE_EQUATIONS = True
    REQUIRE_EVIDENCE = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    @property
    def SECRET_KEY(self):
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable must be set in production")
        return secret_key

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
