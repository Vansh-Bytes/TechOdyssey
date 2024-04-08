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
    if (document.querySelector('.mobile-nav-links').classList.contains('mobile-nav-links-active')) {
        document.querySelector('.mobile-nav-links').classList.remove('mobile-nav-links-active');
    }
    else {
        document.querySelector('.mobile-nav-links').classList.add('mobile-nav-links-active');
        document.addEventListener('click', function (e) {
            if (e.target.classList.contains('mobile-nav-links') || e.target.classList.contains('mobile-nav-link') || e.target.classList.contains('hamburger') || e.target.classList.contains('hamburger-icon')) {
                return;
            }
            else {
                console.log(e.target);
                document.querySelector('.mobile-nav-links').classList.remove('mobile-nav-links-active');
            }
        });
    }
}