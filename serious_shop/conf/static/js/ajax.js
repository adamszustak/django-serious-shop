$(document).ready(function(){
    $('#addItemForm').submit(function(event) {
        event.preventDefault();
        const serializedData = $(this).serialize();
        const slug = $(this).data('slug');
        console.log(slug)
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        let size = $(this).children("input[name='size']:checked").val()
        if (size === undefined) {
            size = null
        }

        $.ajax({
            url: '/add-to-cart/' + slug + '/' + size,
            data: {
                csrfmiddlewaretoken: csrfToken,
                slug: slug,
                size: size
            },
            type: 'post',
            success: function() {
                $('input[type="radio"]').prop('checked', false);
            }
        })
    })
});