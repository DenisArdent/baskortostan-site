from app import app, db
from app.models import User, Admin
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Функция транслитерации для преобразования кириллицы в латиницу
def transliterate(text):
    # Словарь соответствий кириллица -> латиница
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    }
    
    result = ''
    for char in text:
        result += translit_dict.get(char, char)
    return result

# Список имен пользователей
first_names = ["Александр", "Алексей", "Анна", "Екатерина", "Дмитрий", "Ольга", "Михаил", 
              "Иван", "Мария", "Сергей", "Наталья", "Владимир", "Татьяна", "Андрей", 
              "Елена", "Павел", "Светлана", "Никита", "Виктория", "Юрий"]

last_names = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов",
             "Михайлов", "Новиков", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев",
             "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"]

# Функция для создания случайной почты (с использованием только латиницы)
def generate_email(username):
    # Транслитерация кириллических символов в латиницу
    latin_username = transliterate(username)
    domains = ["mail.ru", "gmail.com", "yandex.ru", "outlook.com", "hotmail.com"]
    return f"{latin_username.lower()}@{random.choice(domains)}"

# Функция для создания случайной даты
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

# Создаем пользователей с контекстом приложения
with app.app_context():
    # Проверяем, существуют ли уже пользователи
    existing_users = User.query.count()
    if existing_users > 2:
        print(f"В базе данных уже есть {existing_users} пользователей. Прерываем создание тестовых пользователей.")
    else:
        # Создаем пользователей
        print("Создаем тестовых пользователей...")
        
        # Генерируем случайные комбинации имен и фамилий без повторений
        user_combinations = []
        for i in range(20):
            if i < len(first_names) and i < len(last_names):
                first_name = first_names[i]
                last_name = last_names[i]
            else:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
            
            # Создаем username с кириллическими символами (для отображения)
            username = f"{first_name}_{last_name}"
            # Убеждаемся, что имена пользователей не повторяются
            if username in [uc[0] for uc in user_combinations]:
                username = f"{first_name}_{last_name}{random.randint(1, 999)}"
            
            email = generate_email(username)
            user_combinations.append((username, email))
        
        # Список ролей
        admin_roles = ['admin', 'editor']
        
        # Создаем пользователей
        for i, (username, email) in enumerate(user_combinations):
            # Создаем пользователя
            user = User(
                username=username,
                email=email,
                created_at=random_date(datetime(2024, 1, 1), datetime(2025, 4, 22))
            )
            user.set_password('password')  # Общий пароль для всех тестовых пользователей
            db.session.add(user)
            db.session.commit()  # Сохраняем, чтобы получить ID
            
            # Делаем некоторых пользователей администраторами
            if random.random() < 0.3:
                role = random.choice(admin_roles)
                admin = Admin(
                    user_id=user.id,
                    role=role,
                    is_active=True
                )
                db.session.add(admin)
            
            # Показываем в консоли имя пользователя и латинский email
            print(f"Создан пользователь {i+1}/20: {username} ({email})")
        
        # Сохраняем все изменения
        db.session.commit()
        print("Успешно создано 20 тестовых пользователей!")
