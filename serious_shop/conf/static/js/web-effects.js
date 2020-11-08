// menu dropdown
$(document).ready(function() {
    $( '.dropdown' ).hover(
        function(){
            $(this).children('.dropdown-content').slideDown(200);
        },
        function(){
            $(this).children('.dropdown-content').slideUp(200);
        }
    );
});

// messages $ detail-item tabs
$(document).ready(function() {
    const btns = document.querySelectorAll('.tablinks');
    const btnsText = document.querySelectorAll('.description, .shipment');
    const toggleFunction = () => {
        btns.forEach(btn => btn.classList.toggle('active'));
        btnsText.forEach(text => text.classList.toggle('active'));
    }
    btns.forEach(btn => btn.addEventListener('click', toggleFunction));

    const closeX = document.querySelector('ul.messages span.close');
    const baner = document.querySelector('ul.messages');
    closeX.addEventListener('click', function() {
        baner.style.transition = "all .8s"
        baner.style.opacity = 0
    });
});
