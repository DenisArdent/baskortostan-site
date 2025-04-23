from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    """Модель пользователя системы с поддержкой авторизации"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Хеширование пароля"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def has_admin_rights(self):
        """Проверяет, является ли пользователь администратором любого уровня"""
        admin = Admin.query.filter_by(user_id=self.id, is_active=True).first()
        return admin is not None
    
    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        admin = Admin.query.filter_by(user_id=self.id, is_active=True).first()
        return admin is not None and admin.role == 'admin'
    
    def is_editor(self):
        """Проверяет, является ли пользователь редактором"""
        admin = Admin.query.filter_by(user_id=self.id, is_active=True).first()
        return admin is not None and admin.role == 'editor'
    
    def get_admin_role(self):
        """Возвращает роль администратора, если пользователь является администратором"""
        admin = Admin.query.filter_by(user_id=self.id, is_active=True).first()
        return admin.role if admin else None
    
    def __repr__(self):
        return f'<User {self.username}>'

class Admin(db.Model):
    """Модель администратора сайта"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    role = db.Column(db.String(50))  # 'admin' or 'editor'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # These fields are explicitly NOT included in the model:
    # added_at, added_by, description - they should be removed from the database
    
    user = db.relationship('User', backref=db.backref('admin_role', uselist=False))
    
    def __repr__(self):
        return f'<Admin {self.user.username}: {self.role}>'
