// script.js - основной файл
import { initNavigation } from './navigation.js';
import { initContactForm } from './contact.js';
import { initAccordion } from './accordion.js';

document.addEventListener("DOMContentLoaded", function() {
    const content = document.getElementById("content");
    const { updateUI } = initNavigation();

    // Загрузка страницы
    function loadPage(page) {
        const pageToLoad = page === "" ? "home" : page;
        
        fetch(`pages/${pageToLoad}.html`)
            .then(response => {
                if (!response.ok) throw new Error("Страница не найдена");
                return response.text();
            })
            .then(html => {
                content.innerHTML = html;
                history.pushState({ page: pageToLoad }, "", `/${pageToLoad === "home" ? "" : pageToLoad}`);
                updateUI(pageToLoad);

                // Инициализация компонентов
                if (pageToLoad === 'contact') initContactForm();
                if (pageToLoad === 'home') initAccordion();
            })
            .catch(() => {
                content.innerHTML = "<h1>Ошибка загрузки страницы</h1>";
                if (pageToLoad !== "home") loadPage("home");
            });
    }

    // Обработка кликов
    document.addEventListener("click", function(e) {
        if (e.target.matches("[data-page]")) {
            e.preventDefault();
            loadPage(e.target.getAttribute("data-page"));
        }
    });

    // Обработка истории
    window.addEventListener("popstate", function(e) {
        const page = e.state?.page || window.location.pathname.slice(1) || "home";
        loadPage(page);
    });

    // Первоначальная загрузка
    loadPage(window.location.pathname.slice(1) || "home");
});