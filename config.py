import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key-here'
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app/static')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'app/templates')