from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db
from app.models import User, Admin
from app.forms import LoginForm, RegistrationForm, ProfileForm, ContactForm, AuthenticatedContactForm

# Навигационные элементы
nav_items = [
    {'title': 'Главная', 'page': 'home', 'endpoint': 'index'},
    {'title': 'Культура', 'page': 'culture', 'endpoint': 'culture'},
    {'title': 'Природа', 'page': 'nature', 'endpoint': 'nature'},
    {'title': 'Достопримечательности', 'page': 'places', 'endpoint': 'places'},
    {'title': 'Связаться с нами', 'page': 'contact', 'endpoint': 'contact'}
]


@app.route('/')
def index():
    return render_template('index.html',
                           title='Главная',
                           current_page='Главная',
                           active_page='home',
                           nav_items=nav_items)


@app.route('/culture')
def culture():
    cultural_figures = [
        {'name': 'Муртаза Рахимов', 'role': 'Башкирский политик, первый Президент Республики Башкортостан (1993-2010)'},
        {'name': 'Мидхат Шакиров', 'role': 'Советский государственный деятель, первый секретарь Башкирского обкома КПСС (1969–1987)'},
        {'name': 'Михаил Нагой', 'role': 'Первый уфимский воевода, боярин'},
        {'name': 'Салават Юлаев', 'role': 'Сподвижник Емельяна Пугачёва, башкирский поэт-импровизатор'},
        {'name': 'Сергей Аксаков', 'role': 'Русский писатель, чиновник и общественный деятель'},
        {'name': 'Мажит Гафури', 'role': 'Башкирский и татарский писатель-просветитель'},
        {'name': 'Шайхзада Бабич', 'role': 'Башкирский поэт, классик национальной литературы'},
        {'name': 'Мустай Карим', 'role': 'Башкирский советский поэт, писатель, драматург'},
        {'name': 'Андрей Шаронов', 'role': 'Государственный деятель, заместитель мэра Москвы по экономической политике'},
        {'name': 'Эльвира Набиуллина', 'role': 'Российский экономист, председатель Центрального банка России'},
        {'name': 'Мифтахетдин Акмулла', 'role': 'Башкирский поэт-просветитель, поэт-философ'},
        {'name': 'Загир Исмагилов', 'role': 'Советский башкирский композитор, педагог, народный артист СССР'},
        {'name': 'Борис Шапошников', 'role': 'Маршал Советского Союза, военный теоретик'},
        {'name': 'Александр Матросов', 'role': 'Герой Советского Союза, красноармеец'},
        {'name': 'Миннигали Губайдуллин', 'role': 'Участник Великой Отечественной войны, Герой Советского Союза'},
        {'name': 'Муса Гареев', 'role': 'Советский военный лётчик, дважды Герой Советского Союза'},
        {'name': 'Шагит Худайбердин', 'role': 'Революционер, партийный и государственный деятель, писатель'},
        {'name': 'Рудольф Нуреев', 'role': 'Советский и британский артист балета, балетмейстер'},
        {'name': 'Сергей Довлатов', 'role': 'Российский писатель и журналист'},
        {'name': 'Инна Чурикова', 'role': 'Российская актриса театра и кино, народная артистка СССР'},
        {'name': 'Людмила Улицкая', 'role': 'Российская писательница, общественный деятель'},
        {'name': 'Рафаил Касимов', 'role': 'Композитор, заслуженный деятель искусств Республики Башкортостан'},
        {'name': 'Иван Якутов', 'role': 'Деятель российского социал-демократического движения'},
        {'name': 'Аскар Абдразаков', 'role': 'Российский оперный певец (бас), народный артист Башкортостана'}
    ]

    return render_template('culture.html',
                           title='Культура',
                           current_page='Культура',
                           active_page='culture',
                           nav_items=nav_items,
                           figures=cultural_figures)


@app.route('/nature')
def nature():
    nature_places = [
        {'name': 'Гора Ямантау', 'description': 'Высочайшая точка Южного Урала'},
        {'name': 'Река Белая', 'description': 'Главная водная артерия Башкортостана'}
    ]

    return render_template('nature.html',
                           title='Природа',
                           current_page='Природа',
                           active_page='nature',
                           nav_items=nav_items,
                           places=nature_places)


@app.route('/places')
def places():
    attractions = [
        {'name': 'Капова пещера', 'type': 'Археологический памятник'},
        {'name': 'Мечеть Ляля-Тюльпан', 'type': 'Архитектурная достопримечательность'}
    ]

    return render_template('places.html',
                           title='Достопримечательности',
                           current_page='Достопримечательности',
                           active_page='places',
                           nav_items=nav_items,
                           attractions=attractions)


# Добавим модель для сообщений обратной связи
from datetime import datetime  # Добавим импорт здесь, чтобы быть уверенным

class Feedback(db.Model):
    """Модель для хранения сообщений обратной связи"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    topic = db.Column(db.String(50))
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Связь с пользователем, если был авторизован
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)  # Поле для отметки о прочтении
    
    user = db.relationship('User', backref=db.backref('feedback', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Feedback {self.topic}: {self.email}>'    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Инициализируем соответствующую форму в зависимости от авторизации
    if current_user.is_authenticated:
        form = AuthenticatedContactForm()
    else:
        form = ContactForm()
    
    # Обрабатываем отправку формы
    if form.validate_on_submit():
        try:
            # Создаем новое сообщение обратной связи
            feedback = Feedback()
            feedback.topic = form.topic.data
            feedback.message = form.message.data
            
            # Если пользователь авторизован, используем его данные
            if current_user.is_authenticated:
                feedback.name = current_user.username
                feedback.email = current_user.email
                feedback.user_id = current_user.id
            else:
                # Иначе берем из формы
                feedback.name = form.name.data
                feedback.email = form.email.data
            
            # Сохраняем в базу данных
            db.session.add(feedback)
            db.session.commit()
            
            # Отображаем сообщение об успехе
            flash('Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.', 'success')
            
            # Создаем новую пустую форму вместо перенаправления
            if current_user.is_authenticated:
                form = AuthenticatedContactForm()
            else:
                form = ContactForm()
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Ошибка при сохранении формы обратной связи: {str(e)}')
            flash('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте еще раз.', 'error')

    # Добавляем контактную информацию
    contact_info = {
        'address': '450077, Республика Башкортостан, г. Уфа, ул. Тукаева, 46',
        'phone': '+7 (347) 123-45-67',
        'email': 'info@bashkortostan.ru',
        'working_hours': 'Пн-Пт: 9:00-18:00, Обед: 13:00-14:00'
    }
    
    return render_template('contact.html',
                          title='Контакты',
                          current_page='Связаться с нами',
                          active_page='contact',
                          nav_items=nav_items,
                          form=form,
                          contact_info=contact_info,
                          is_authenticated=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        # Если это AJAX-запрос
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Вы уже вошли в систему'})
        return redirect(url_for('index'))
    
    # Инициализация формы
    form = LoginForm()
    
    # Если форма валидна и отправлена методом POST
    if request.method == 'POST':
        # Для AJAX-запроса из модального окна
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            email = request.form.get('email')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me') == 'on'
            
            if not email or not password:
                return jsonify({'success': False, 'message': 'Введите email и пароль'})
            
            user = User.query.filter_by(email=email).first()
            
            if user is None or not user.check_password(password):
                return jsonify({'success': False, 'message': 'Неверный email или пароль'})
            
            login_user(user, remember=remember_me)
            return jsonify({'success': True, 'message': 'Вы успешно вошли в систему'})
        
        # Для обычного запроса (не AJAX)
        elif form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user is None or not user.check_password(form.password.data):
                flash('Неверный email или пароль', 'error')
                return redirect(url_for('login'))
            
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    
    # Для GET-запроса
    return render_template('login.html',
                          title='Вход',
                          current_page='Вход в систему',
                          active_page='login',
                          form=form,
                          nav_items=nav_items)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Инициализация формы
    form = RegistrationForm()
    
    # Проверяем, является ли запрос AJAX
    is_ajax_request = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Если форма валидна и отправлена методом POST
    if form.validate_on_submit():
        # Проверяем, есть ли уже пользователи в системе (является ли это первым пользователем)
        is_first_user = User.query.count() == 0
        
        # Создаем нового пользователя
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Сохраняем пользователя в базе данных
        db.session.add(user)
        db.session.commit()
        
        # Если это первый пользователь, делаем его администратором
        if is_first_user:
            app.logger.info(f'Назначаем первого пользователя {user.username} администратором')
            admin = Admin(user_id=user.id, role='admin', is_active=True)
            db.session.add(admin)
            db.session.commit()
            app.logger.info('Первый пользователь успешно назначен администратором')
        
        # Автоматическая авторизация пользователя после регистрации
        login_user(user, remember=True)
        
        flash('Добро пожаловать! Вы успешно зарегистрировались.', 'success')
        return redirect(url_for('index'))
    
    # Если форма не прошла валидацию и это AJAX-запрос, возвращаем JSON с ошибками
    if request.method == 'POST' and not form.validate() and is_ajax_request:
        return jsonify({'success': False, 'errors': form.errors})
    
    # Обычный GET-запрос или не AJAX POST-запрос, возвращаем шаблон
    return render_template('register.html',
                          title='Регистрация',
                          current_page='Регистрация',
                          active_page='register',
                          form=form,
                          nav_items=nav_items)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(original_username=current_user.username)
    
    if form.validate_on_submit():
        # Проверяем, были ли изменения в профиле
        username_changed = form.username.data and form.username.data != current_user.username
        password_changed = False
        
        # Применяем изменения к пользователю
        if username_changed:
            # Проверяем, что имя не занято
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Это имя пользователя уже занято.', 'danger')
                return redirect(url_for('profile'))
            current_user.username = form.username.data
        
        # Почту не меняем, только используем для валидации
        
        # Если изменен пароль
        if form.new_password.data:
            # Проверка текущего пароля
            if not current_user.check_password(form.current_password.data):
                flash('Неверный текущий пароль.', 'danger')
                return redirect(url_for('profile'))
            
            # Проверяем, что новый пароль совпадает с подтверждением
            if form.new_password.data != form.confirm_password.data:
                flash('Пароли не совпадают.', 'danger')
                return redirect(url_for('profile'))
            
            # Устанавливаем новый пароль
            current_user.set_password(form.new_password.data)
            password_changed = True
        
        # Сохраняем изменения
        db.session.commit()
        
        # Показываем соответствующее сообщение в зависимости от того, что было изменено
        if username_changed and password_changed:
            flash('Имя пользователя и пароль успешно обновлены!', 'success')
        elif password_changed:
            flash('Пароль успешно изменен!', 'success')
        elif username_changed:
            flash('Имя пользователя успешно обновлено!', 'success')
        
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        # Предзаполняем форму текущими данными пользователя
        form.username.data = current_user.username
    
    return render_template('profile.html',
                          title='Профиль',
                          current_page='Профиль',
                          form=form,
                          is_admin=current_user.is_admin() if current_user.is_authenticated else False,
                          nav_items=nav_items)


@app.route('/admin')
@login_required
def admin_panel():
    """Admin panel main page"""
    if not current_user.has_admin_rights():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('index'))
        
    return render_template('admin/index.html',
                          title='Администрирование',
                          current_page='Администрирование',
                          nav_items=nav_items)


@app.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    """Admin panel user management"""
    if not current_user.has_admin_rights():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Получаем список пользователей с пагинацией, отсортированный по ID
    users = User.query.order_by(User.id.asc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    admin_users = {}
    for user in users.items:
        admin = None
        if hasattr(user, 'admin_role') and user.admin_role and user.admin_role.is_active:
            admin = user.admin_role
        admin_users[user.id] = admin
    
    return render_template('admin/users.html',
                          title='Управление пользователями',
                          current_page='Управление пользователями',
                          users=users.items,
                          pagination=users,
                          admin_users=admin_users,
                          nav_items=nav_items)
@app.route('/admin/appeals', methods=['GET'])
@login_required
def admin_appeals():
    """Admin panel for viewing feedback messages"""
    if not current_user.has_admin_rights():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('index'))
    
    # Получаем параметры из запроса
    page = request.args.get('page', 1, type=int)
    per_page = 10
    topic = request.args.get('topic', 'all')
    search = request.args.get('search', '')
    
    # Базовый запрос
    query = Feedback.query
    
    # Применяем фильтр по теме, если указан
    if topic != 'all':
        query = query.filter(Feedback.topic == topic)
    
    # Применяем поиск по тексту, если указан
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Feedback.name.ilike(search_term),
                Feedback.email.ilike(search_term),
                Feedback.message.ilike(search_term)
            )
        )
    
    # Получаем список обращений с пагинацией, отсортированный по дате (старые сверху)
    appeals = query.order_by(Feedback.created_at.asc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    # Помечаем все просматриваемые обращения как прочитанные
    for appeal in appeals.items:
        if not appeal.is_read:
            appeal.is_read = True
    
    # Сохраняем изменения в базе данных
    db.session.commit()
    
    # Создаем словарь с темами обращений для отображения
    topic_labels = {
        'question': 'Вопрос о регионе',
        'feedback': 'Отзыв о посещении',
        'cooperation': 'Предложение о сотрудничестве',
        'error': 'Сообщение об ошибке на сайте',
        'other': 'Другое'
    }
    
    return render_template('admin/appeals.html',
                          title='Обращения пользователей',
                          current_page='Обращения',
                          appeals=appeals.items,
                          pagination=appeals,
                          topic_labels=topic_labels,
                          nav_items=nav_items)


@app.route('/admin/reset_password', methods=['POST'])
@login_required
def reset_password():
    """Сброс пароля пользователя администратором"""
    # Проверяем, является ли текущий пользователь администратором
    if not current_user.has_admin_rights():
        return jsonify({'success': False, 'message': 'У вас нет прав администратора.'})    
    
    # Получаем параметры из запроса
    user_id = request.form.get('user_id', type=int)
    password = request.form.get('password')
    
    if not user_id:
        flash('Неверный ID пользователя!', 'danger')
        return redirect(url_for('admin_users'))
    
    # Проверяем пароль
    if not password or len(password) < 6:
        flash('Пароль должен содержать минимум 6 символов!', 'danger')
        return redirect(url_for('admin_users'))
    
    # Находим пользователя
    user = User.query.get(user_id)
    if not user:
        flash('Пользователь не найден!', 'danger')
        return redirect(url_for('admin_users'))
    
    # Устанавливаем новый пароль
    user.set_password(password)
    db.session.commit()
    
    # Уведомляем об успехе
    flash(f'Пароль пользователя {user.username} успешно изменен!', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/user/update_field', methods=['POST'])
@login_required
def update_user_field():
    """Обновление поля пользователя (AJAX)"""
    # Проверяем, является ли текущий пользователь администратором
    if not current_user.has_admin_rights():
        return jsonify({'success': False, 'message': 'У вас нет прав администратора.'})
    
    # Получаем параметры из запроса
    user_id = request.form.get('user_id', type=int)
    field = request.form.get('field')
    value = request.form.get('value')
    
    if not user_id or not field or not value:
        return jsonify({'success': False, 'message': 'Недостаточно данных для запроса.'})
    
    # Находим пользователя
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден.'})
    
    # Обрабатываем запрос в зависимости от типа поля
    if field == 'username':
        existing_user = User.query.filter(User.username == value, User.id != user_id).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Это имя пользователя уже занято.'})
        user.username = value
    elif field == 'email':
        existing_user = User.query.filter(User.email == value, User.id != user_id).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Этот email уже используется.'})
        user.email = value
    else:
        return jsonify({'success': False, 'message': 'Неизвестное поле.'})
    
    # Сохраняем изменения
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Данные обновлены успешно!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка при обновлении данных: {str(e)}'})


@app.route('/admin/set_role', methods=['POST'])
@login_required
def set_admin_role():
    """Установка роли администратора для пользователя"""
    # Проверяем, является ли текущий пользователь администратором
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Только администратор может управлять ролями.'})
    
    # Получаем параметры запроса
    user_id = request.form.get('user_id', type=int)
    role = request.form.get('role')  # 'admin', 'editor' или 'none'
    
    if not user_id or not role:
        return jsonify({'success': False, 'message': 'Недостаточно данных для запроса.'})
    
    # Запрещаем снимать роль с самого себя
    if user_id == current_user.id and role == 'none':
        return jsonify({'success': False, 'message': 'Вы не можете снять роль администратора с самого себя.'})
    
    # Находим пользователя
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден.'})
    
    # Получаем текущую запись администратора для этого пользователя
    from app.models import Admin
    admin = Admin.query.filter_by(user_id=user.id).first()
    
    try:
        if role == 'none':
            # Удаляем роль администратора
            if admin:
                admin.is_active = False
                db.session.commit()
            return jsonify({'success': True, 'message': f'Роль администратора удалена у пользователя {user.username}!'})
        else:
            # Создаем или обновляем запись администратора
            if not admin:
                admin = Admin(user_id=user.id, role=role, is_active=True)
                db.session.add(admin)
            else:
                admin.role = role
                admin.is_active = True
            
            db.session.commit()
            return jsonify({'success': True, 'message': f'Роль {role} успешно назначена пользователю {user.username}!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка при изменении роли: {str(e)}'})