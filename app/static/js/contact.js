document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const responseDiv = document.getElementById('ajaxResponse');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Индикатор загрузки
            responseDiv.innerHTML = '<p class="loading">Отправка...</p>';

            try {
                const formData = {
                    name: form.name.value,
                    email: form.email.value,
                    topic: form.topic.value,
                    message: form.message.value
                };

                const response = await fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                responseDiv.innerHTML = `
                    <div class="success">
                        <h3>Спасибо, ${data.name}!</h3>
                        <p>Ваше сообщение на тему "${data.topic}" получено.</p>
                    </div>
                `;

                form.reset();

            } catch (error) {
                console.error('Ошибка:', error);
                responseDiv.innerHTML = `
                    <div class="error">
                        <h3>Ошибка</h3>
                        <p>${error.message || 'Не удалось отправить форму'}</p>
                    </div>
                `;
            }
        });
    }
});