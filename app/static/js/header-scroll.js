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
        navLogo.style.transition = 'opacity 0.3s ease, visibility 0.3s ease';
        
        // Добавляем логотип в начало навигационного меню
        navContainer.insertBefore(navLogo, navContainer.firstChild);
    }
    
    // Добавляем плавный переход для верхнего логотипа
    if (topLogo) {
        topLogo.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
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
        const animationDistance = 100; // Увеличиваем расстояние для более плавной анимации
        
        // Определяем прогресс анимации (от 0 до 1) с более плавной кривой ускорения
        let progress = 0;
        if (scrollPosition >= threshold) {
            // Используем кубическую функцию для более плавного перехода
            const linearProgress = Math.min(1, (scrollPosition - threshold) / animationDistance);
            progress = easeInOutCubic(linearProgress);
        }
        
        // Проверяем, изменился ли прогресс существенно (с точностью до 2 знаков)
        // Это помогает избежать ненужных обновлений DOM
        const roundedProgress = Math.round(progress * 100) / 100;
        if (Math.abs(roundedProgress - lastProgress) < 0.01 && lastProgress !== -1) {
            return;
        }
        
        lastProgress = roundedProgress;
        
        // Применяем плавную анимацию скрытия верхней панели
        if (progress > 0) {
            const opacity = 1 - progress;
            const translateY = -progress * initialTopHeaderHeight;
            
            // Синхронизированное изменение стилей для плавного перехода
            header.classList.add('transitioning');
            
            // Для верхней панели - прозрачность и сдвиг
            topHeader.style.opacity = opacity;
            topHeader.style.transform = `translateY(${-progress * 10}px)`;
            
            // Для навигационного меню - перемещение вверх относительно прогресса
            mainNav.style.transform = `translateY(${translateY}px)`;
            
            // Плавно управляем видимостью навигационного логотипа
            // Добавляем небольшую задержку для навигационного логотипа, чтобы избежать наложения
            if (progress > 0.05) {
                navLogo.style.visibility = 'visible';
                
                // Делаем навигационный логотип видимым только когда верхний логотип начинает скрываться
                // Используем кубическую функцию для более плавного появления
                navLogo.style.opacity = easeInOutCubic(Math.max(0, (progress - 0.1) / 0.9));
                
                // Делаем логотип кликабельным, когда он достаточно видимый
                if (progress > 0.3) {
                    navLogo.style.pointerEvents = 'auto';
                    // Добавляем класс visible для гарантии кликабельности
                    navLogo.classList.add('visible');
                } else {
                    navLogo.style.pointerEvents = 'none';
                    navLogo.classList.remove('visible');
                }
            } else {
                navLogo.style.opacity = '0';
                navLogo.style.pointerEvents = 'none';
                navLogo.classList.remove('visible');
                
                // Используем setTimeout для задержки скрытия, чтобы завершить анимацию прозрачности
                setTimeout(() => {
                    if (lastProgress <= 0.05) {
                        navLogo.style.visibility = 'hidden';
                    }
                }, 300);
            }
            
            // Полное скрытие верхней панели при почти завершенной анимации
            if (progress >= 0.95 && !isHeaderCollapsed) {
                document.body.classList.add('header-hidden');
                mainNav.classList.add('nav-fixed');
                // Гарантируем, что логотип кликабельный в фиксированном режиме
                navLogo.classList.add('visible');
                navLogo.style.pointerEvents = 'auto';
                isHeaderCollapsed = true;
            } else if (progress < 0.95 && isHeaderCollapsed) {
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
            
            // Сначала скрываем с анимацией, затем убираем видимость
            navLogo.style.opacity = '0';
            navLogo.style.pointerEvents = 'none';
            navLogo.classList.remove('visible');
            setTimeout(() => {
                if (lastProgress <= 0) {
                    navLogo.style.visibility = 'hidden';
                }
            }, 300);
            
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
