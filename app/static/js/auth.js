// Глобальная функция для показа формы входа
function showLoginForm() {
    console.log('showLoginForm called');
    var loginModal = document.getElementById('login-modal');
    var registerModal = document.getElementById('register-modal');
    
    if (registerModal) {
        registerModal.style.display = 'none';
    }
    
    if (loginModal) {
        loginModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    return false;
}

// Глобальная функция для показа формы регистрации
function showRegisterForm() {
    console.log('showRegisterForm called');
    var loginModal = document.getElementById('login-modal');
    var registerModal = document.getElementById('register-modal');
    
    if (loginModal) {
        loginModal.style.display = 'none';
    }
    
    if (registerModal) {
        registerModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    return false;
}

// Обработка закрытия flash-сообщений и модальных окон для авторизации

// Функция, которая добавляет все необходимые обработчики событий
function initAuthHandlers() {
    console.log('Initializing auth handlers...');
    
    // Находим все элементы закрытия flash-сообщений
    const closeButtons = document.querySelectorAll('.close-flash');
    
    // Обработка закрытия flash-сообщений
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Получаем родительский элемент (flash-сообщение) и скрываем его
            const flashMessage = this.parentElement;
            flashMessage.style.opacity = '0';
            setTimeout(() => {
                flashMessage.style.display = 'none';
            }, 300);
        });
    });
    
    // Получаем ссылки на модальные окна и элементы форм
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const loginError = document.getElementById('login-error');
    
    // Находим все кнопки входа и регистрации
    const loginButtons = document.querySelectorAll('.login-button');
    const registerButtons = document.querySelectorAll('.register-button');
    const closeModals = document.querySelectorAll('.close-modal');
    
    // Функция открытия модального окна входа
    function openLoginModal(e) {
        if (e) e.preventDefault();
        if (registerModal) registerModal.style.display = 'none';
        if (loginModal) {
            loginModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }
    
    // Функция открытия модального окна регистрации
    function openRegisterModal(e) {
        if (e) e.preventDefault();
        if (loginModal) loginModal.style.display = 'none';
        if (registerModal) {
            registerModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }
    
    // Открытие модального окна входа
    loginButtons.forEach(button => {
        button.addEventListener('click', openLoginModal);
    });
    
    // Открытие модального окна регистрации
    registerButtons.forEach(button => {
        button.addEventListener('click', openRegisterModal);
    });
    
    // Закрытие модальных окон по клику на крестик
    closeModals.forEach(closeBtn => {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const modal = this.closest('.dark-auth-overlay');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    });
    
    // Закрытие модальных окон по клику вне формы
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('dark-auth-overlay')) {
            e.target.style.display = 'none';
            document.body.style.overflow = '';
        }
    });
    
    // Обработка активации/деактивации кнопок форм
    if (loginForm) {
        const loginInputs = loginForm.querySelectorAll('input[required]');
        const loginButton = loginForm.querySelector('button[type="submit"]');
        
        // Функция проверки всех полей формы входа
        function validateLoginForm() {
            let isValid = true;
            loginInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                }
            });
            loginButton.disabled = !isValid;
        }
        
        // Проверяем при загрузке
        validateLoginForm();
        
        // Проверяем при вводе в любое поле
        loginInputs.forEach(input => {
            input.addEventListener('input', validateLoginForm);
        });
        
        // Обработка отправки формы входа через AJAX
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload(); // Перезагружаем страницу при успешном входе
                } else {
                    // Показываем ошибку
                    if (loginError) {
                        loginError.textContent = data.message || 'Ошибка входа. Проверьте данные и попробуйте снова.';
                        loginError.style.display = 'block';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (loginError) {
                    loginError.textContent = 'Произошла ошибка при входе. Пожалуйста, попробуйте позже.';
                    loginError.style.display = 'block';
                }
            });
        });
    }
    
    // Обработка активации/деактивации кнопки формы регистрации
    if (registerForm) {
        const registerInputs = registerForm.querySelectorAll('input[required]');
        const registerButton = registerForm.querySelector('button[type="submit"]');
        
        // Функция проверки всех полей формы регистрации
        function validateRegisterForm() {
            let isValid = true;
            registerInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                }
            });
            
            // Дополнительная проверка паролей
            const password = registerForm.querySelector('input[name="password"]');
            const password2 = registerForm.querySelector('input[name="password2"]');
            if (password && password2 && password.value !== password2.value) {
                isValid = false;
            }
            
            registerButton.disabled = !isValid;
        }
        
        // Проверяем при загрузке
        validateRegisterForm();
        
        // Проверяем при вводе в любое поле
        registerInputs.forEach(input => {
            input.addEventListener('input', validateRegisterForm);
        });
    }
}

// Инициализация формы входа
function initLoginModal() {
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    
    if (!loginModal) return false;
    
    if (registerModal) registerModal.style.display = 'none';
    loginModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    return true;
}

// Инициализация формы регистрации
function initRegisterModal() {
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    
    if (!registerModal) return false;
    
    if (loginModal) loginModal.style.display = 'none';
    registerModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    return true;
}

// Функция для обработки глобальных кликов (работает даже если DOM изменился)
function setupGlobalClickHandlers() {
    // Обработчик для кликов по всему документу
    document.addEventListener('click', function(e) {
        let target = e.target;
        console.log('Click detected on:', target);
        
        // Проверяем, является ли элемент кнопкой входа или содержит ее
        if (target.classList.contains('login-button') || 
            target.closest('.login-button')) {
            console.log('Login button clicked');
            e.preventDefault();
            initLoginModal();
            return;
        }
        
        // Проверяем, является ли элемент кнопкой регистрации или содержит ее
        if (target.classList.contains('register-button') || 
            target.closest('.register-button')) {
            console.log('Register button clicked');
            e.preventDefault();
            initRegisterModal();
            return;
        }
    }, true);
    
    // Добавляем дополнительные прямые обработчики для кнопок
    const loginButtons = document.querySelectorAll('.login-button');
    const registerButtons = document.querySelectorAll('.register-button');
    
    console.log('Found login buttons:', loginButtons.length);
    console.log('Found register buttons:', registerButtons.length);
    
    // Добавляем обработчики для каждой кнопки входа
    loginButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Login button clicked via direct handler');
            e.preventDefault();
            initLoginModal();
        });
    });
    
    // Добавляем обработчики для каждой кнопки регистрации
    registerButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Register button clicked via direct handler');
            e.preventDefault();
            initRegisterModal();
        });
    });
}

// Дополнительный обработчик для открытия модальных окон по URL-параметрам
function checkUrlParams() {
    if(window.location.search.includes('action=login')) {
        console.log('Login action detected in URL');
        initLoginModal();
    } else if(window.location.search.includes('action=register')) {
        console.log('Register action detected in URL');
        initRegisterModal();
    }
}

// Инициализируем все обработчики при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing handlers...');
    initAuthHandlers();
    
    // Обработка отправки формы регистрации через AJAX
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Предотвращаем стандартную отправку формы
            
            const formData = new FormData(registerForm);
            const registerError = document.getElementById('register-error');
            
            // Делаем кнопку неактивной во время отправки
            const submitButton = registerForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Отправка...';
            }
            
            // Скрываем предыдущие ошибки
            if (registerError) {
                registerError.style.display = 'none';
                registerError.textContent = '';
            }
            
            // Отправляем данные формы через AJAX
            fetch('/register', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                // Восстанавливаем кнопку
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Зарегистрироваться';
                }
                
                if (response.redirected) {
                    // Если сервер перенаправляет нас, значит регистрация успешна
                    
                    // Показываем успешное сообщение перед переходом
                    const registerModal = document.getElementById('register-modal');
                    if (registerModal) {
                        registerModal.style.opacity = '0';
                        setTimeout(() => {
                            // Закрываем модальное окно и переходим на главную страницу
                            window.location.href = response.url;
                        }, 500);
                    } else {
                        window.location.href = response.url;
                    }
                    
                    return null;
                } else {
                    // Если нет перенаправления, проверяем ответ
                    return response.json();
                }
            })
            .then(data => {
                if (data) {
                    // Обработка ошибок
                    if (data.errors) {
                        if (registerError) {
                            // Форматируем ошибки в виде списка, если их несколько
                            const errorMessages = Object.values(data.errors);
                            
                            if (errorMessages.length === 1) {
                                // Если всего одна ошибка, просто показываем её
                                registerError.textContent = errorMessages[0];
                            } else {
                                // Если несколько ошибок, форматируем с заголовком
                                registerError.innerHTML = 'Пожалуйста, исправьте следующие ошибки:<br>';
                                
                                const errorList = document.createElement('ul');
                                errorList.style.textAlign = 'left';
                                errorList.style.paddingLeft = '20px';
                                errorList.style.margin = '8px 0';
                                
                                errorMessages.forEach(error => {
                                    const listItem = document.createElement('li');
                                    listItem.textContent = error;
                                    errorList.appendChild(listItem);
                                });
                                
                                registerError.appendChild(errorList);
                            }
                            
                            registerError.style.display = 'block';
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Registration error:', error);
                if (registerError) {
                    registerError.textContent = 'Произошла ошибка при регистрации. Попробуйте еще раз.';
                    registerError.style.display = 'block';
                }
                
                // Восстанавливаем кнопку
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Зарегистрироваться';
                }
            });
        });
    }
    setupGlobalClickHandlers();
    checkUrlParams();
    
    // Специальный обработчик для главной страницы с хешем
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        console.log('On homepage, adding special handler for login button');
        document.querySelectorAll('.login-button').forEach(element => {
            element.onclick = function(e) {
                console.log('Login button clicked on homepage');
                e.preventDefault();
                e.stopPropagation();
                initLoginModal();
                return false;
            };
        });
    }
});

// Дополнительный обработчик для полной загрузки страницы
window.addEventListener('load', function() {
    console.log('Window fully loaded');
    
    // Переинициализация для страниц с хеш-символом
    if (window.location.hash) {
        console.log('Hash detected in URL, reinitializing handlers...');
        // Повторная инициализация обработчиков
        setTimeout(function() {
            setupGlobalClickHandlers();
            
            // Обработчик для узкого случая с главной страницей
            var loginButton = document.querySelector('.auth-link.login-button');
            if (loginButton) {
                console.log('Found login button after hash change:', loginButton);
                loginButton.onclick = function(e) {
                    console.log('Direct click on homepage login button');
                    e.preventDefault();
                    e.stopPropagation();
                    return initLoginModal();
                };
            }
        }, 300);
    }
});

// Обработчик изменения хеша в URL
window.addEventListener('hashchange', function() {
    console.log('Hash changed, reinitializing handlers...');
    setTimeout(setupGlobalClickHandlers, 300);
});
