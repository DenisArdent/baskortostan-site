import logging
from app import app
from app.database import init_db

if __name__ == '__main__':
    # Настройка логирования для отладки
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    # Инициализация базы данных при первом запуске
    init_db()
    
    app.run(host='0.0.0.0', port=8888, debug=True)