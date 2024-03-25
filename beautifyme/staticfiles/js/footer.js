const footer = document.getElementById('footer');

function toggleFooterVisibility() {
    if (window.scrollY > 0) {
        footer.classList.add('hidden');
    } else {
        footer.classList.remove('hidden');
    }
}


window.addEventListener('scroll', toggleFooterVisibility);
