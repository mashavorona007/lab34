/* Click handler for closing message boxes */
$(document).ready(function() {
    $('.message .close-button').click(function () {
        $(this).closest('.message').slideUp(1000); 
    }); 
}); 