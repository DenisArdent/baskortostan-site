/**
 * Скрипт для навигации между вкладками с помощью колёсика мыши
 * Позволяет переходить на следующую/предыдущую вкладку при прокрутке в конце/начале страницы
 */

// Карта страниц в нужном порядке
const pageOrder = [
    'home',     // Главная
    'culture',  // Культура
    'nature',   // Природа
    'places',   // Достопримечательности
    'contact'   // Связаться с нами
];

// Получаем текущую страницу
function getCurrentPageKey() {
    const activePage = document.querySelector('.nav-links a.active');
    if (activePage) {
        return activePage.getAttribute('data-page');
    }
    return 'home'; // По умолчанию - главная
}

// Получаем URL для следующей/предыдущей страницы
function getPageUrl(pageKey) {
    const pageLink = document.querySelector(`.nav-links a[data-page="${pageKey}"]`);
    if (pageLink) {
        return pageLink.getAttribute('href');
    }
    return '/';
}

// Определяем предыдущую страницу
function getPreviousPage() {
    const currentPage = getCurrentPageKey();
    const currentIndex = pageOrder.indexOf(currentPage);
    
    if (currentIndex > 0) {
        return pageOrder[currentIndex - 1];
    }
    return null; // Уже на первой странице
}

// Определяем следующую страницу
function getNextPage() {
    const currentPage = getCurrentPageKey();
    const currentIndex = pageOrder.indexOf(currentPage);
    
    if (currentIndex < pageOrder.length - 1) {
        return pageOrder[currentIndex + 1];
    }
    return null; // Уже на последней странице
}

// Основная функция обработки колёсика мыши
let isScrolling = false;
let lastScrollTime = 0;
const scrollCooldown = 1000; // Задержка между переходами (мс)

function handleScroll(event) {
    const now = Date.now();
    if (isScrolling || now - lastScrollTime < scrollCooldown) {
        return;
    }
    
    const isAtBottom = (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50;
    const isAtTop = window.scrollY <= 50;
    
    // Событие колёсика мыши имеет свойство deltaY
    // deltaY > 0 - прокрутка вниз, deltaY < 0 - прокрутка вверх
    const scrollDown = event.deltaY > 0;
    const scrollUp = event.deltaY < 0;
    
    let navigateTo = null;
    
    if (isAtBottom && scrollDown) {
        // В конце страницы и прокручиваем вниз - переходим на следующую
        navigateTo = getNextPage();
    } else if (isAtTop && scrollUp) {
        // В начале страницы и прокручиваем вверх - переходим на предыдущую
        navigateTo = getPreviousPage();
    }
    
    if (navigateTo) {
        isScrolling = true;
        lastScrollTime = now;
        
        // Плавная анимация перед переходом
        document.body.style.opacity = '0.5';
        document.body.style.transition = 'opacity 0.3s ease';
        
        setTimeout(() => {
            window.location.href = getPageUrl(navigateTo);
        }, 300);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, не находимся ли мы на странице профиля или администрирования
    // Если URL содержит '/profile' или '/admin', не активируем навигацию скроллом
    const isProfilePage = window.location.pathname.includes('/profile');
    const isAdminPage = window.location.pathname.includes('/admin');
    
    if (!isProfilePage && !isAdminPage) {
        // Добавляем обработчик события колёсика мыши
        window.addEventListener('wheel', handleScroll, { passive: false });
        
        // Добавляем обработчик для тач-устройств
        let touchStartY = 0;
        
        window.addEventListener('touchstart', function(e) {
            touchStartY = e.touches[0].clientY;
        }, { passive: true });
        
        window.addEventListener('touchend', function(e) {
            const touchEndY = e.changedTouches[0].clientY;
            const touchDiff = touchStartY - touchEndY;
            
            // Эмуляция события колёсика
            if (Math.abs(touchDiff) > 50) {
                handleScroll({ deltaY: touchDiff });
            }
        }, { passive: true });
    }
    
    // Проверяем, есть ли хеш в URL для прокрутки к определенной секции
    if (window.location.hash) {
        const element = document.querySelector(window.location.hash);
        if (element) {
            setTimeout(() => {
                element.scrollIntoView();
            }, 100);
        }
    }
});
