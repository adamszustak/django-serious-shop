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

// promo-code
// $(document).on('submit', '#code_form',function(e){
//     e.preventDefault();
//     $.ajax({
//         type: 'POST',
//         url: $(this).data('url'),
//         data:{
//             code: $('#id_code').val(),
//             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//         },
//         success:function(json){
//             $('#id_code').val('');
//             $('#code').empty().show(500).prepend('<img src="' + json.image + '"><div class="info"><p class="item-name">Coupon - ' + json.code + '</p><p class="quantity">Coupon for ' + json.discount + '% off</p><p class="price">- ' + json.get_discount + ' $</p></div>');
//             $('#message-coupon').hide()
//             $('p.total').empty().html('Total price:<span> $'+ json.get_total + ' - <span style="color:red;">$' + json.get_discount +'</span> = $' + json.get_final_price)
//         },
//         error: function() {
//             $('#message-coupon').show()
//         }
//     })
// })
$(document).on('submit', '#code_form',function(e){
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data:{
            code: $('#id_code').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(json){
            let trans = gettext('off')
            let trans1 = gettext('Coupon for ')
            $('#id_code').val('');
            $('#code').empty().show(500).prepend(`<img src="${json.image}"><div class="info"><p class="item-name">${gettext('Coupon')} - ${json.code}</p><p class="quantity">${gettext(trans1)} ${json.discount}% ${gettext(trans)}</p><p class="price">- ${json.get_discount} $</p></div>`);
            $('#message-coupon').hide()
            $('p.total').empty().html(gettext('Total price') +':<span> $'+ json.get_total + ' - <span style="color:red;">$' + json.get_discount +'</span> = $' + json.get_final_price)
        },
        error: function() {
            $('#message-coupon').show()
        }
    })
})
