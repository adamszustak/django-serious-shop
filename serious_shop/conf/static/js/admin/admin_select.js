$(function () {
    const sizes = $('#sizes-group');
    const quantity = $('#id_quantity');
    const time = 1000;
    console.log( $('#id_section').val())
    $('#id_section').change(function() {
        if ($(this).val().contains('Accessories')) {
            sizes.hide(time);
            quantity.show(time)
        }
        else {
            sizes.show(time);
            quantity.hide(time);
            $('#sizes-group input[type=number]').each(function(i) {
                if (!$(this).val()) {
                    $(this).val(0)
                }
            })
        }
    })
})