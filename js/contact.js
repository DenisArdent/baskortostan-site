export function initContactForm() {
    const form = document.getElementById('contactForm');
    const modal = document.getElementById('modal');
    const modalData = document.getElementById('modalData');
    const closeBtn = document.querySelector('.close-btn');
    const confirmBtn = document.getElementById('confirmBtn');

    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Собираем данные формы
        const formData = {
            name: form.name.value,
            email: form.email.value,
            topic: form.topic.options[form.topic.selectedIndex].text,
            message: form.message.value
        };

        // Заполняем модальное окно
        modalData.innerHTML = `
            <p><strong>Имя:</strong> ${formData.name}</p>
            <p><strong>Email:</strong> ${formData.email}</p>
            <p><strong>Тема:</strong> ${formData.topic}</p>
            <p><strong>Сообщение:</strong> ${formData.message}</p>
        `;

        // Показываем модальное окно
        modal.style.display = 'block';
    });

    // Закрытие модального окна
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Подтверждение отправки
    confirmBtn.addEventListener('click', () => {
        alert('Форма успешно отправлена!');
        form.reset();
        modal.style.display = 'none';
    });

    // Закрытие при клике вне окна
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}