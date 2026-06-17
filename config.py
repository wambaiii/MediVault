import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'medivault-super-secret-key-2024-strathmore'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Alice.2020@localhost/secure_med'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}

    # Session fixes
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 3600
    WTF_CSRF_ENABLED = False