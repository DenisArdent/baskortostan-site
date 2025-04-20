// script.js - основной файл
document.addEventListener("DOMContentLoaded", function() {
    // Инициализация всех компонентов
    if (document.querySelector('.accordion-item')) {
        initAccordion();
    }

    if (document.getElementById('contactForm')) {
        initContactForm();
    }

    initNavigation();
});

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const currentPath = window.location.pathname;

    // Определяем текущую страницу по URL
    let currentPage = 'home';
    if (currentPath.includes('/culture')) currentPage = 'culture';
    else if (currentPath.includes('/nature')) currentPage = 'nature';
    else if (currentPath.includes('/places')) currentPage = 'places';
    else if (currentPath.includes('/contact')) currentPage = 'contact';

    // Обновляем активную ссылку
    navLinks.forEach(link => {
        const page = link.getAttribute('data-page');
        link.classList.toggle('active', page === currentPage);
    });
}

function initAccordion() {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');

        header.addEventListener('click', () => {
            accordionItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });

            item.classList.toggle('active');
        });
    });
}

function initContactForm() {
    const form = document.getElementById('contactForm');
    const modal = document.getElementById('modal');
    const modalData = document.getElementById('modalData');
    const closeBtn = document.querySelector('.close-btn');
    const confirmBtn = document.getElementById('confirmBtn');

    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            name: form.name.value,
            email: form.email.value,
            topic: form.topic.options[form.topic.selectedIndex].text,
            message: form.message.value
        };

        modalData.innerHTML = `
            <p><strong>Имя:</strong> ${formData.name}</p>
            <p><strong>Email:</strong> ${formData.email}</p>
            <p><strong>Тема:</strong> ${formData.topic}</p>
            <p><strong>Сообщение:</strong> ${formData.message}</p>
        `;

        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    confirmBtn.addEventListener('click', () => {
        fetch('/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: form.name.value,
                email: form.email.value,
                topic: form.topic.value,
                message: form.message.value
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('Форма успешно отправлена!');
            form.reset();
            modal.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка отправки формы');
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}