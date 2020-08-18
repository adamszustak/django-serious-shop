const slideList = [{
    img: '../static/img/main slider/slide1.jpg',
    text: 'section/male',
    dot: 'one'
},
{
    img: '../static/img/main slider/slide2.jpg',
    text: 'section/accessories',
    dot: 'two'
},{
    img: '../static/img/main slider/slide3.jpg',
    text: 'section/female',
    dot: 'three'
}];

const time = 2000;
let active = 0;
const image = document.querySelector('section.slider img');
const link = document.querySelector('section.slider a.link');
const dots = [...document.querySelectorAll('section.slider .dots span')];


const changeDot = () => {
    const activeDot = dots.findIndex(dot => dot.classList.contains('active'));
    dots[activeDot].classList.remove('active');
    dots[active].classList.add('active');
}

const changeSlide = () => {
    active++;
    if (active === slideList.length) active = 0;
    image.src = slideList[active].img;
    link.href = slideList[active].text;
    changeDot();
};

let indexInterval = setInterval(changeSlide, time);


const clickChangeSlide = function() {
    clearInterval(indexInterval)
    active = slideList.findIndex(p => p.dot == this.id)
    image.src = slideList[active].img;
    link.href = slideList[active].text;
    changeDot();
    indexInterval = setInterval(changeSlide, time);
}

dots.forEach(dot => {
    dot.addEventListener('click', clickChangeSlide)
})