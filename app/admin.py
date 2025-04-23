"""
Утилиты для работы с администраторами сайта.
Этот модуль предоставляет функции для управления администраторами и проверки прав доступа.
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from app.models import Admin, AdminRole, User
from app import db

def is_admin_required(view_func):
    """
    Декоратор для проверки, является ли текущий пользователь администратором.
    Используется для защиты маршрутов, доступных только администраторам.
    """
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа к этой странице необходимо авторизоваться.', 'warning')
            return redirect(url_for('login'))
        
        if not current_user.is_admin():
            flash('Доступ запрещен. У вас нет прав администратора.', 'danger')
            return redirect(url_for('index'))
            
        return view_func(*args, **kwargs)
    return decorated_view

def admin_required(view_func):
    """
    Декоратор для проверки, является ли текущий пользователь администратором.
    Используется для защиты маршрутов, доступных только администраторам.
    """
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа к этой странице необходимо авторизоваться.', 'warning')
            return redirect(url_for('login'))
        
        if not current_user.is_admin():
            flash('Доступ запрещен. У вас нет прав администратора.', 'danger')
            return redirect(url_for('index'))
            
        return view_func(*args, **kwargs)
    return decorated_view

# Алиас для обратной совместимости - роль 'admin' теперь заменяет super_admin
super_admin_required = admin_required

def editor_required(view_func):
    """
    Декоратор для проверки, имеет ли текущий пользователь права редактора или выше.
    """
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа к этой странице необходимо авторизоваться.', 'warning')
            return redirect(url_for('login'))
        
        if not current_user.can_manage_content():
            flash('Доступ запрещен. У вас нет прав редактора.', 'danger')
            return redirect(url_for('index'))
            
        return view_func(*args, **kwargs)
    return decorated_view
    
# Алиас для обратной совместимости
content_admin_required = editor_required

def admin_users_required(view_func):
    """
    Декоратор для проверки, имеет ли текущий пользователь права на управление пользователями.
    """
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа к этой странице необходимо авторизоваться.', 'warning')
            return redirect(url_for('login'))
        
        if not current_user.is_admin():
            flash('Доступ запрещен. У вас нет прав на управление пользователями.', 'danger')
            return redirect(url_for('index'))
            
        return view_func(*args, **kwargs)
    return decorated_view

# Алиас для обратной совместимости - теперь только администраторы могут управлять пользователями
user_admin_required = admin_users_required

def add_admin(user_id, role=AdminRole.EDITOR.value, added_by=None, description=None):
    """
    Добавляет пользователя в список администраторов.
    
    Args:
        user_id: ID пользователя, которого нужно сделать администратором
        role: Роль администратора (по умолчанию - контент-администратор)
        added_by: ID администратора, добавившего этого админа
        description: Описание полномочий администратора
    
    Returns:
        Admin: Объект нового администратора или None в случае ошибки
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return None
            
        # Проверяем, не является ли пользователь уже администратором
        existing_admin = Admin.query.filter_by(user_id=user_id).first()
        if existing_admin:
            # Если админ существует, но не активен, активируем его
            if not existing_admin.is_active:
                existing_admin.is_active = True
                existing_admin.role = role
                existing_admin.added_by = added_by
                existing_admin.description = description
                db.session.commit()
                return existing_admin
            return existing_admin
            
        # Создаем нового администратора
        admin = Admin(
            user_id=user_id,
            role=role,
            added_by=added_by,
            description=description
        )
        db.session.add(admin)
        db.session.commit()
        return admin
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении администратора: {str(e)}")
        return None

def remove_admin(user_id):
    """
    Удаляет пользователя из списка администраторов (делает его неактивным).
    
    Args:
        user_id: ID пользователя, которого нужно лишить прав администратора
        
    Returns:
        bool: True если операция успешна, иначе False
    """
    try:
        admin = Admin.query.filter_by(user_id=user_id).first()
        if not admin:
            return False
            
        # Не удаляем запись, а просто деактивируем
        admin.is_active = False
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при удалении администратора: {str(e)}")
        return False

def change_admin_role(user_id, new_role):
    """
    Изменяет роль администратора.
    
    Args:
        user_id: ID пользователя-администратора
        new_role: Новая роль
        
    Returns:
        Admin: Обновленный объект администратора или None в случае ошибки
    """
    try:
        admin = Admin.query.filter_by(user_id=user_id).first()
        if not admin:
            return None
            
        admin.role = new_role
        db.session.commit()
        return admin
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при изменении роли администратора: {str(e)}")
        return None

def get_all_admins():
    """
    Получает список всех активных администраторов.
    
    Returns:
        list: Список объектов Admin
    """
    return Admin.query.filter_by(is_active=True).all()

def initialize_admin():
    """
    Создает первого администратора, если в системе еще нет администраторов.
    Эта функция должна вызываться при первом запуске приложения.
    
    Returns:
        Admin: Объект администратора или None, если в системе уже есть администраторы
    """
    # Проверяем, есть ли уже администраторы
    if Admin.query.first():
        return None
        
    # Берем первого пользователя в системе (или создаем его, если нужно)
    user = User.query.first()
    if not user:
        # Здесь может быть логика создания первого пользователя
        return None
        
    return add_admin(user.id, role=AdminRole.ADMIN.value, description="Первоначальный администратор системы")

# Алиас для обратной совместимости
initialize_super_admin = initialize_admin
