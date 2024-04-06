function toggleFaq(element) {
    if (element.nextElementSibling.classList.contains('hidden')) {
        element.nextElementSibling.classList.remove('hidden');
        element.nextElementSibling.classList.add('visible');
    } else {
        element.nextElementSibling.classList.remove('visible');
        element.nextElementSibling.classList.add('hidden');
    }
    // Get svg inside element and rotate it
    element.querySelector('svg').style.transform = element.nextElementSibling.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
}