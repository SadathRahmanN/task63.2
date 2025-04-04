// Dark Mode Functions
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Apply saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Offcanvas Functions
function toggleOffcanvas(offcanvasId) {
    const offcanvas = document.getElementById(offcanvasId);
    offcanvas.classList.toggle('active');
}

// Close offcanvas when clicking outside
document.addEventListener('click', function(event) {
    const offcanvases = document.querySelectorAll('.offcanvas-right');
    offcanvases.forEach(offcanvas => {
        if (!offcanvas.contains(event.target) && !event.target.closest('.nav-link')) {
            offcanvas.classList.remove('active');
        }
    });
});

// Destinations Link Handler
function handleDestinationsClick(event) {
    event.preventDefault();
    const isHomePage = window.location.pathname === "{% url 'home' %}";
    const targetSection = document.getElementById('featured-destinations');
    
    if (isHomePage && targetSection) {
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    } else {
        window.location.href = "{% url 'home' %}#featured-destinations";
        window.addEventListener('load', () => {
            const section = document.getElementById('featured-destinations');
            if (section) {
                section.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
}

// Smooth Scroll Handler
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Form Validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            showToast('Please fill all required fields!', 'danger');
        }
    });
});

// Toast Notification System
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('toast');
    toastEl.querySelector('.toast-body').textContent = message;
    toastEl.className = `toast bg-${type} text-white`;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// Image Load Handler
document.querySelectorAll('.card-img-top').forEach(img => {
    img.onload = function() {
        this.style.opacity = '1';
        this.previousElementSibling.style.display = 'none';
    };
});

// Initial Page Load Hash Handling
window.addEventListener('load', () => {
    // Handle featured destinations hash
    if (window.location.hash === '#featured-destinations') {
        const section = document.getElementById('featured-destinations');
        if (section) {
            section.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    // Handle other hashes
    const hash = window.location.hash;
    if (hash && hash !== '#featured-destinations') {
        const target = document.querySelector(hash);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }
});

// CSRF Token Handling for AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    headers: { 'X-CSRFToken': csrftoken }
});