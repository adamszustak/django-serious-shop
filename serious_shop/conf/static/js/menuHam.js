const iconBar = document.querySelector('i.fa-bars');
const sectionChoice = document.querySelector('section.choice div.wrapper');
iconBar.addEventListener('click', (e) => {
    e.preventDefault()
    sectionChoice.classList.toggle('show');
})
