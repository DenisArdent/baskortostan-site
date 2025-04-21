import logging
from app import app

if __name__ == '__main__':
    # Настройка логирования для отладки
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    app.run(host='0.0.0.0', port=8888, debug=True)