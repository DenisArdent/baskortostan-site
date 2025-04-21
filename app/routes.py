from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm

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


@app.route('/contact', methods=['GET', 'POST'])  # Оба метода!
def contact():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Получены данные:", data)  # Для отладки

            if not data:
                return jsonify({'error': 'No data received'}), 400

            return jsonify({
                'status': 'success',
                'name': data.get('name'),
                'email': data.get('email'),
                'topic': data.get('topic')
            }), 200

        except Exception as e:
            print("Ошибка:", str(e))  # Логирование
            return jsonify({'error': str(e)}), 500

    # GET-запрос (возвращаем HTML)
    return render_template('contact.html',
                           title='Контакты',
                           current_page='Связаться с нами',
                           active_page='contact',
                           nav_items=nav_items)


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
            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me') == 'on'
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Введите имя пользователя и пароль'})
            
            user = User.query.filter_by(username=username).first()
            
            if user is None or not user.check_password(password):
                return jsonify({'success': False, 'message': 'Неверное имя пользователя или пароль'})
            
            login_user(user, remember=remember_me)
            return jsonify({'success': True, 'message': 'Вы успешно вошли в систему'})
        
        # Для обычного запроса (не AJAX)
        elif form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user is None or not user.check_password(form.password.data):
                flash('Неверное имя пользователя или пароль', 'error')
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
        # Создаем нового пользователя
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Сохраняем пользователя в базе данных
        db.session.add(user)
        db.session.commit()
        
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