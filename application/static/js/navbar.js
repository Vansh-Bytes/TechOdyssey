// Check if the window has been scrolled 

function checkScroll() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        document.querySelector('.navbar').classList.add('navbar-scrolled');
    }
    else {
        document.querySelector('.navbar').classList.remove('navbar-scrolled');
    }
}

// Check if the window has been resized
function checkResize() {
    if (window.innerWidth > 768) {
        document.querySelector('.navbar').classList.remove('navbar-mobile');
    }
    else {
        document.querySelector('.navbar').classList.add('navbar-mobile');
    }

}

document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('scroll', checkScroll);
    window.addEventListener('resize', checkResize);
});

function toggleMobileNav() {
    document.querySelector('.mobile-nav-links').classList.toggle('mobile-nav-links-active');
}