document.addEventListener('DOMContentLoaded', function() {

    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
            navToggle.classList.toggle('active');
        });
    }

    const mainNav = document.querySelector('.main-nav');
    
    if (mainNav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                mainNav.classList.add('nav-scrolled');
            } else {
                mainNav.classList.remove('nav-scrolled');
            }
        });
    }

    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('show')) {
                navMenu.classList.remove('show');
                navToggle.classList.remove('active');
            }
        });
    });
});