from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    email = StringField('Email', validators=[DataRequired(), Email(message='Пожалуйста, введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    """Форма регистрации нового пользователя"""
    username = StringField('Имя пользователя', validators=[
        DataRequired(), 
        Length(min=4, max=25, message='Имя пользователя должно быть от 4 до 25 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Пожалуйста, введите корректный email')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message='Пароль должен содержать минимум 6 символов')
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(), 
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        """Проверка уникальности имени пользователя"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя уже занято. Попробуйте выбрать другое.')

    def validate_email(self, email):
        """Проверка уникальности email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже используется. Возможно, вы уже регистрировались?')


class ProfileForm(FlaskForm):
    """Форма редактирования профиля пользователя"""
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25, message='Имя пользователя должно быть от 4 до 25 символов')
    ])
    
    current_password = PasswordField('Текущий пароль', validators=[
        Optional()
    ])
    
    new_password = PasswordField('Новый пароль', validators=[
        Optional(),
        Length(min=6, message='Пароль должен содержать минимум 6 символов')
    ])
    
    confirm_password = PasswordField('Повторите новый пароль', validators=[
        Optional(),
        EqualTo('new_password', message='Пароли должны совпадать')
    ])
    
    submit = SubmitField('Сохранить изменения')
    
    def __init__(self, original_username, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        """Проверка уникальности имени пользователя, исключая текущее имя"""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Это имя уже занято. Попробуйте выбрать другое.')


class ContactForm(FlaskForm):
    """Форма обратной связи для незарегистрированных пользователей"""
    name = StringField('Ваше имя', validators=[DataRequired(message='Пожалуйста, введите ваше имя')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Пожалуйста, введите корректный email')])
    topic = SelectField('Тема обращения', validators=[DataRequired()], 
                      choices=[
                          ('', 'Выберите тему'),
                          ('question', 'Вопрос о регионе'),
                          ('feedback', 'Отзыв о посещении'),
                          ('cooperation', 'Предложение о сотрудничестве'),
                          ('error', 'Сообщить об ошибке на сайте'),
                          ('other', 'Другое')
                      ])
    message = TextAreaField('Сообщение', validators=[DataRequired(message='Пожалуйста, введите текст сообщения'),
                                                   Length(min=10, message='Сообщение должно содержать минимум 10 символов')])
    submit = SubmitField('Отправить сообщение')


class AuthenticatedContactForm(FlaskForm):
    """Форма обратной связи для зарегистрированных пользователей (без полей имени и email)"""
    topic = SelectField('Тема обращения', validators=[DataRequired()], 
                      choices=[
                          ('', 'Выберите тему'),
                          ('question', 'Вопрос о регионе'),
                          ('feedback', 'Отзыв о посещении'),
                          ('cooperation', 'Предложение о сотрудничестве'),
                          ('error', 'Сообщить об ошибке на сайте'),
                          ('other', 'Другое')
                      ])
    message = TextAreaField('Сообщение', validators=[DataRequired(message='Пожалуйста, введите текст сообщения'),
                                                   Length(min=10, message='Сообщение должно содержать минимум 10 символов')])
    submit = SubmitField('Отправить сообщение')
