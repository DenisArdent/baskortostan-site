/**
 * Анимация логотипа при прокрутке
 * Логотип плавно перемещается из верхней панели в левую часть навигационного меню
 */

document.addEventListener('DOMContentLoaded', function() {
    // Находим элементы
    const topHeader = document.querySelector('.top-header');
    const mainNav = document.querySelector('.main-nav');
    const navContainer = document.querySelector('.main-nav .container');
    const header = document.querySelector('header');
    const topLogo = document.querySelector('.top-header .logo');
    
    // Измеряем исходную высоту верхней панели (нужно для анимации)
    const initialTopHeaderHeight = topHeader.offsetHeight;
    
    // Создаем элемент для логотипа в навигационном меню
    let navLogo = navContainer.querySelector('.nav-logo');
    
    // Если элемент не существует, создаем его
    if (!navLogo) {
        navLogo = document.createElement('div');
        navLogo.className = 'nav-logo';
        navLogo.innerHTML = '<a href="/" class="logo-link">Башкортостан</a>';
        
        // Явно устанавливаем начальные стили для навигационного логотипа
        navLogo.style.opacity = '0';
        navLogo.style.visibility = 'hidden';
        navLogo.style.transition = 'none';
        
        // Добавляем логотип в начало навигационного меню
        navContainer.insertBefore(navLogo, navContainer.firstChild);
    }
    
    // Убираем анимацию для верхнего логотипа - будет резкий переход
    if (topLogo) {
        topLogo.style.transition = 'none';
    }
    
    // Переменная для отслеживания состояния заголовка (скрыт/показан)
    let isHeaderCollapsed = false;
    // Переменная для предотвращения частых обновлений DOM
    let lastProgress = -1;
    // Переменная для хранения ID запроса анимации
    let animationFrameId = null;
    
    // Обработчик прокрутки страницы с использованием requestAnimationFrame для оптимизации
    window.addEventListener('scroll', function() {
        // Отменяем предыдущий запрос анимации, если он был
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
        
        // Планируем новую анимацию на следующий frame
        animationFrameId = requestAnimationFrame(updateHeaderAnimation);
    });
    
    function updateHeaderAnimation() {
        const scrollPosition = window.scrollY;
        const threshold = 50; // Порог начала анимации
        
        // Вместо плавного прогресса используем резкое переключение
        const showHeader = scrollPosition < threshold;
        
        // Упрощенная логика: либо показываем хедер полностью, либо скрываем его
        const progress = showHeader ? 0 : 1;
        
        // Проверяем, изменилось ли состояние заголовка
        if (progress === lastProgress && lastProgress !== -1) {
            return;
        }
        
        lastProgress = progress;
        
        // Применяем плавную анимацию скрытия верхней панели
        if (progress > 0) {
            // Полностью резкое изменение стилей без плавного перехода
            header.classList.add('transitioning');
            
            // Резко скрываем или показываем верхнюю панель
            topHeader.style.opacity = progress === 1 ? '0' : '1';
            topHeader.style.transform = progress === 1 ? 'translateY(-100%)' : 'translateY(0)';
            
            // Навигационное меню сразу перемещается вверх на полную высоту хедера
            mainNav.style.transform = progress === 1 ? `translateY(${-initialTopHeaderHeight}px)` : 'translateY(0)';
            
            // Бинарное управление видимостью навигационного логотипа
            // Сразу показываем/скрываем без промежуточных состояний
            if (progress === 1) {
                // Показываем логотип в меню
                navLogo.style.visibility = 'visible';
                navLogo.style.opacity = '1';
                navLogo.style.pointerEvents = 'auto';
                navLogo.classList.add('visible');
            } else {
                // Скрываем логотип
                navLogo.style.opacity = '0';
                navLogo.style.visibility = 'hidden';
                navLogo.style.pointerEvents = 'none';
                navLogo.classList.remove('visible');
            }
            
            // резкое переключение классов для фиксированного режима
            if (progress === 1 && !isHeaderCollapsed) {
                document.body.classList.add('header-hidden');
                mainNav.classList.add('nav-fixed');
                // Гарантируем, что логотип кликабельный в фиксированном режиме
                navLogo.classList.add('visible');
                navLogo.style.pointerEvents = 'auto';
                isHeaderCollapsed = true;
            } else if (progress === 0 && isHeaderCollapsed) {
                document.body.classList.remove('header-hidden');
                mainNav.classList.remove('nav-fixed');
                isHeaderCollapsed = false;
            }
        } else {
            // Сбрасываем все стили при возврате вверх
            header.classList.remove('transitioning');
            topHeader.style.opacity = '1';
            topHeader.style.transform = 'translateY(0)';
            mainNav.style.transform = 'translateY(0)';
            
            // Сразу скрываем без анимации
            navLogo.style.opacity = '0';
            navLogo.style.pointerEvents = 'none';
            navLogo.classList.remove('visible');
            navLogo.style.visibility = 'hidden';
            
            document.body.classList.remove('header-hidden');
            mainNav.classList.remove('nav-fixed');
            isHeaderCollapsed = false;
        }
    }
    
    // Функция плавного перехода с кубической кривой
    function easeInOutCubic(x) {
        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    }
    
    // Вызываем обработчик сразу, чтобы применить эффект при загрузке страницы на прокрученной позиции
    window.dispatchEvent(new Event('scroll'));
});
