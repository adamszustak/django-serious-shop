;(function(){
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
})();
