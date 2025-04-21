from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

app = Flask(__name__)

# Загрузка конфигурации
app.config.from_object(Config)

# Явная установка секретного ключа для форм и сессий
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['WTF_CSRF_ENABLED'] = True

# Инициализация CSRF-защиты
csrf = CSRFProtect(app)

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # указываем страницу авторизации
login_manager.login_message = 'Пожалуйста, авторизуйтесь для доступа к этой странице'
login_manager.login_message_category = 'info'

from app import routes, models