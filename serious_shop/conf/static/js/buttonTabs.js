const btns = document.querySelectorAll('.tablinks');
const btnsText = document.querySelectorAll('.description, .shipment');
const toggleFunction = () => {
    btns.forEach(btn => btn.classList.toggle('active'));
    btnsText.forEach(text => text.classList.toggle('active'));
}
btns.forEach(btn => btn.addEventListener('click', toggleFunction));
