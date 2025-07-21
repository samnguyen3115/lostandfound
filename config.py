import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to PostgreSQL with environment variables
        DB_USER = os.environ.get('DB_USER', 'postgres')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('DB_NAME', 'lostandfound_db')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Path Configuration
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app', 'static')
    TEMPLATE_FOLDER_MAIN = os.path.join(basedir, 'app', 'main', 'templates')
    TEMPLATE_FOLDER_ERRORS = os.path.join(basedir, 'app', 'errors', 'templates')
    TEMPLATE_FOLDER_AUTH = os.path.join(basedir, 'app', 'auth', 'templates')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@lostandfound.com')    