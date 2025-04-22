// Обработка клика на иконку профиля
document.addEventListener('DOMContentLoaded', function() {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const profileIcon = document.querySelector('.profile-icon');
    
    if (profileIcon && profileDropdown) {
        // Обработка клика на иконку профиля
        profileIcon.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Переключаем класс show для отображения/скрытия меню
            profileDropdown.classList.toggle('show');
        });
        
        // Закрытие меню при клике вне его
        document.addEventListener('click', function(e) {
            if (!profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('show');
            }
        });
    }
});
