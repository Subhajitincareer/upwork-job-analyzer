"""
Configuration Management
Centralized configuration with validation
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Email Settings
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
    
    # Scraping Settings
    SEARCH_QUERY = os.getenv('SEARCH_QUERY', 'AI and ML engineer')
    PAGES_TO_SCRAPE = int(os.getenv('PAGES_TO_SCRAPE', 3))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', 30))
    
    # Scheduling
    SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '08:00')
    TIMEZONE = os.getenv('TIMEZONE', 'Asia/Kolkata')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    REPORTS_DIR = DATA_DIR / 'reports'
    LOGS_DIR = BASE_DIR / 'logs'
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        errors = []
        
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == 'your_gemini_api_key_here':
            errors.append("GEMINI_API_KEY not set")
        
        if not cls.GMAIL_USER or '@' not in cls.GMAIL_USER:
            errors.append("GMAIL_USER invalid or not set")
        
        if not cls.GMAIL_APP_PASSWORD or len(cls.GMAIL_APP_PASSWORD) < 10:
            errors.append("GMAIL_APP_PASSWORD not set")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        for dir_path in [cls.RAW_DATA_DIR, cls.PROCESSED_DATA_DIR, 
                         cls.REPORTS_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# Validate and create directories on import
try:
    Config.validate()
    Config.create_directories()
except Exception as e:
    print(f"⚠️  Configuration warning: {e}")
