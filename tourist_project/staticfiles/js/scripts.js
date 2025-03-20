// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Apply saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Offcanvas toggle
function toggleOffcanvas(offcanvasId) {
    const offcanvas = document.getElementById(offcanvasId);
    offcanvas.classList.toggle('active');
}

// Close offcanvas on outside click
document.addEventListener('click', function(event) {
    const offcanvases = document.querySelectorAll('.offcanvas-right');
    offcanvases.forEach(offcanvas => {
        if (!offcanvas.contains(event.target) && !event.target.closest('.nav-link')) {
            offcanvas.classList.remove('active');
        }
    });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Form validation
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

// Show toast
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('toast');
    toastEl.querySelector('.toast-body').textContent = message;
    toastEl.className = `toast bg-${type} text-white`;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// Image load handler
document.querySelectorAll('.card-img-top').forEach(img => {
    img.onload = function() {
        this.style.opacity = '1';
        this.previousElementSibling.style.display = 'none';
    };
});