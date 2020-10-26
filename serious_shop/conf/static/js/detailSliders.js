$('#lightSlider').lightSlider({
    gallery: true,
    item: 1,
    loop:true,
    slideMargin: 0,
    thumbItem: 9
});

$(document).ready(function() {
    $('#responsive').lightSlider({
        item:5,
        loop:false,
        slideMove:2,
        easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
        speed:600,
        responsive : [
            {
                breakpoint:1150,
                settings: {
                    item:4,
                    slideMove:1,
                    slideMargin:6,
                  }
            },
            {
                breakpoint:900,
                settings: {
                    item:3,
                    slideMove:1,
                    slideMargin:6,
                  }
            },
            {
                breakpoint:600,
                settings: {
                    item:2,
                    slideMove:1
                  }
            },
            {
                breakpoint:382,
                settings: {
                    item:1,
                    slideMove:1
                  }
            }
        ]
    });
});
