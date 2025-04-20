from flask import render_template, request, jsonify
from app import app

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
        {'name': 'Мустай Карим', 'role': 'Писатель, поэт'},
        {'name': 'Рудольф Нуриев', 'role': 'Балетмейстер, артист'}
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