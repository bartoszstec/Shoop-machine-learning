from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os

BASE_DIR = Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/shoopdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key_change_me')
    SESSION_COOKIE_HTTPONLY = True  # Chroni przed atakami XSS
    SESSION_COOKIE_SECURE = False  # Wymaga HTTPS do ciasteczek sesji
    SESSION_COOKIE_SAMESITE = 'Strict'  # Ochrona przed CSRF

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'default_password')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    