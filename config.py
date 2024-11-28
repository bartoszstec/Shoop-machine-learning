from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/shoop2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey787'