"""
Утилиты для работы с базой данных и её инициализацией.
"""
import os
import subprocess
import logging
from app import app, db
from config import Config

def init_db():
    """
    Инициализирует базу данных при первом запуске приложения.
    Проверяет существование файла базы данных и применяет миграции, если файл не существует.
    """
    with app.app_context():
        app.logger.info('Проверка состояния базы данных...')
        
        # Получаем путь к базе данных
        db_path = Config.SQLALCHEMY_DATABASE_URI
        if db_path.startswith('sqlite:///'):
            db_file_path = db_path.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_file_path) if os.path.dirname(db_file_path) else '.'
            
            app.logger.info(f'Путь к файлу базы данных: {db_file_path}')
            app.logger.info(f'Директория базы данных: {db_dir}')
            
            # Создаем директорию, если она не существует
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                app.logger.info(f'Создана директория для базы данных: {db_dir}')
            
            # Проверяем существует ли база данных
            if not os.path.exists(db_file_path):
                app.logger.info('База данных не найдена. Запуск миграций для создания базы данных...')
                # Здесь мы используем Flask-Migrate вместо прямого вызова db.create_all()
                try:
                    # Запуск flask db upgrade для применения всех миграций
                    # Выходим из контекста приложения перед запуском subprocess, чтобы избежать конфликтов
                    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                    app.logger.info(f'Запуск миграций из директории: {root_dir}')
                    subprocess.run([
                        'flask', 'db', 'upgrade'
                    ], cwd=root_dir)
                    app.logger.info('Миграции успешно применены, база данных создана')
                except Exception as e:
                    app.logger.error(f'Ошибка при запуске миграций: {str(e)}')
                    app.logger.info('Попытка создания базы данных вручную...')
                    app.logger.info('Пожалуйста, запустите команду "flask db upgrade" вручную для инициализации базы данных')
            else:
                app.logger.info('База данных уже существует')
            
            # Проверяем, есть ли пользователи с правами администратора в системе
            ensure_first_user_is_admin()


def ensure_first_user_is_admin():
    """
    Функция проверяет, есть ли администраторы в системе, и если нет, назначает первого пользователя администратором.
    """
    try:
        from app.models import User, Admin
        
        with app.app_context():
            # Проверяем, есть ли администраторы в системе
            admin_exists = Admin.query.filter_by(is_active=True).first() is not None
            
            if not admin_exists:
                app.logger.info('Администраторы не найдены. Проверка пользователей...')
                
                # Проверяем, есть ли пользователи в системе
                first_user = User.query.first()
                
                if first_user:
                    app.logger.info(f'Назначаем первого пользователя {first_user.username} администратором')
                    
                    # Проверяем, есть ли у него уже запись администратора
                    admin = Admin.query.filter_by(user_id=first_user.id).first()
                    
                    if not admin:
                        # Создаем новую запись администратора
                        admin = Admin(user_id=first_user.id, role='admin', is_active=True)
                        db.session.add(admin)
                    else:
                        # Активируем существующую запись и убеждаемся, что роль администратора
                        admin.is_active = True
                        admin.role = 'admin'
                    
                    db.session.commit()
                    app.logger.info('Первый пользователь успешно назначен администратором')
                else:
                    app.logger.info('Пользователей в системе нет. Администратор будет назначен позже.')
            else:
                app.logger.info('Администраторы уже существуют в системе.')
    except Exception as e:
        app.logger.error(f'Ошибка при проверке/назначении администратора: {str(e)}')
