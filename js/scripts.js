const icon = document.querySelector('.icon');
const search = document.querySelector('.search');

icon.onclick = function() {
    search.classList.toggle('active');
    if (icon.style.background == 'rgb(237, 28, 36)') {
        icon.style.background = 'none';
        icon.style.border = 'none'
    } else {
        icon.style.background = '#ed1c24';
        icon.style.border = '1px solid #ed1c24'
    }
};