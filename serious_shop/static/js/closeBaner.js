const closeX = document.querySelector('ul.messages span.close');
const baner = document.querySelector('ul.messages');

closeX.addEventListener('click', function() {
    baner.style.transition = "all .8s"
    baner.style.opacity = 0
})