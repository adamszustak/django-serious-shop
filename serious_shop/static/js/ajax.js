$(document).ready(function(){
    const cartQuantity = $('#total_cart_quantity b')
    const cartPrice = $('#total_cart_price b')
    $('.remove_one').click(function(event) {
        event.preventDefault();
        const id = $(this).parent().data('objectid');
        let size = $(this).parent().data('size');
        let quantity = $(this).next()
        let totalItem = $(this).parent().next();
        let icon = $(this).next().next().children()
        const url = $(this).data('url')
        $.ajax({
            url: url,
            type: 'POST',
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(cart) {
                if (quantity.text() > 1) {
                key = cart['cart'][id + '-' + size];actualQuantity = key['quantity'];
                quantity.text(actualQuantity);
                totalItem.text('$' + cart.item_final_price)
                cartQuantity.text(cart.len_cart)
                cartPrice.text(cart.final_price)
                if (quantity.text() < 10) {
                    $(icon).show()
                }}
                else {
                    location.reload();
                }
            }
        })
    })
    $('.add_to_cart').click(function(event) {
        event.preventDefault();
        const id = $(this).parent().data('objectid');
        let size = $(this).parent().data('size');
        let quantity = $(this).prev();
        let totalItem = $(this).parent().next();
        let icon = $(this).children()
        const url = $(this).data('url')
        $.ajax({
            url: url,
            type: 'POST',
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(cart) {
                key = cart['cart'][id + '-' + size];actualQuantity = key['quantity'];
                quantity.text(actualQuantity)
                totalItem.text('$' + cart.item_final_price)
                cartQuantity.text(cart.len_cart)
                cartPrice.text(cart.final_price)
                if (quantity.text() === '10') {
                    $(icon).hide()
                }
            }
        })
    })
});