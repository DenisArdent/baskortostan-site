// navigation.js - обработка навигационного меню
export function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const pageTitle = document.getElementById('page-title');
    
    // Соответствие страниц и их названий
    const pageTitles = {
        "home": "Главная",
        "culture": "Культура",
        "nature": "Природа",
        "places": "Достопримечательности",
        "contact": "Связь с нами"
    };

    // Обновление интерфейса
    function updateUI(page) {
        // Обновляем заголовок
        if (pageTitle) {
            pageTitle.textContent = ` / ${pageTitles[page]}`;
        }
        
        // Обновляем активную ссылку
        navLinks.forEach(link => {
            const isActive = link.getAttribute('data-page') === page;
            link.classList.toggle('active', isActive);
            
            // Добавляем стиль при наведении
            link.addEventListener('mouseenter', () => {
                if (!isActive) {
                    link.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
                }
            });
            
            link.addEventListener('mouseleave', () => {
                if (!isActive) {
                    link.style.backgroundColor = '';
                }
            });
        });
    }

    return {
        updateUI
    };
}