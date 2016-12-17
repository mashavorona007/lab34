/* Initialize event handlers and fade in wishlist list */
$(document).ready(function() {
    
    $('#add-button').click(add_list_ajax); 
    $('#add-wishlist-form').submit(function(event) {
	add_list_ajax(); 
	event.preventDefault(); 
    }); 
    
    $('#wishlists-main').on('click', '.wishlist-wrapper .delete-button', function() {
        delete_list_ajax($(this).closest('.wishlist-wrapper'), $(this).closest('.wishlist-wrapper').find('.list-id').val()); 
    }); 
    
    $('.wishlist-wrapper').fadeIn(500); 
    
}); 

/* Communication with the server */
function add_list_ajax() {
    $.post(ADD_URL, {
        name: $('#add-name').val(),
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {
        $('#add-name').val(''); 
        $('.sad.message').slideUp(1000); 
        add_list_item(data); 
    }); 
}

function delete_list_ajax(elem, wishlist_id) {
    $.post(DELETE_URL, {
        wid: wishlist_id, 
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {
        elem.fadeOut(1000, function() {
	    $(this).remove();
	}); 
    }); 
}

/* Update the web page visually */
function add_list_item(html_string) {
    $('#wishlists-main').prepend(html_string);
    $('.wishlist-wrapper').slideDown(1000); 
}
