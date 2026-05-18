"""
Development Configuration for Personal Blog Application

This configuration is designed for development purposes only.
"""
import os
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).parent

# Load environment variables
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')


class DevelopmentConfig:
    """Development configuration"""
    # Flask settings
    DEBUG = True
    TESTING = False
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-when-deploying'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR / "instance" / "dev_blog.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session security (relaxed for development)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Remember me cookie (relaxed for development)
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 604800  # 7 days


# Set the active configuration
config = DevelopmentConfig
