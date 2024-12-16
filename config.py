from pathlib import Path
import secrets

BASE_DIR = Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/shoop2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(64)
    SESSION_COOKIE_HTTPONLY = True  # Chroni przed atakami XSS
    SESSION_COOKIE_SECURE = False  # Wymaga HTTPS do ciasteczek sesji
    SESSION_COOKIE_SAMESITE = 'Strict'  # Ochrona przed CSRF