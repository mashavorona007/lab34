/* Initialize event handlers and fade in all existing entries */
$(document).ready(function() {
    
    $('#add-button').click(add_product_ajax); 
    $('#add-item-form').submit(function(event) {
        add_product_ajax(); 
        event.preventDefault(); 
    }); 

    $('#link-field').change(get_thumbnails); 
    $('#left-arrow').click(thumbnail_left); 
    $('#right-arrow').click(thumbnail_right); 

    $('#wishlist-items-main').on(
	'click', '.wishlist-item-wrapper .delete-button', function() {
            delete_product_ajax(
		$(this).closest('.wishlist-item-wrapper'), 
		$(this).closest('.wishlist-item-wrapper').find('.product-id').val()); 
    }); 

    $('.wishlist-item-wrapper').fadeIn(500); 
    update_thumbnails(); 
}); 


/* Update the thumbnail images */
var thumbnail_imgs = [NO_IMG]; 
var current_index = 0; 

function display_loading() {
    display_thumbnail(LOADING_IMG); 
    $('#item-thumbnail > div').addClass('loading'); 
}

function display_thumbnail(img_url) {
    $('.loading').removeClass('loading'); 
    $('#item-thumbnail > div').css(
	'background-image', "url('" + img_url + "')"); 
    $('#thumbnail-field').val(img_url); 
}

function update_thumbnails() {
    // Updates the HTML with new thumbnails list
    if(thumbnail_imgs.length > 1) {
	current_index = 1; 
    }
    display_thumbnail(thumbnail_imgs[current_index]); 
}

function thumbnail_left() {
    // Move to the previous thumbnail in the thumbnails list
    current_index = --current_index % thumbnail_imgs.length; 
    display_thumbnail(thumbnail_imgs[current_index]); 
}

function thumbnail_right() {
    // Move to the next thumbnail in the thumbnails list
    current_index = ++current_index % thumbnail_imgs.length; 
    display_thumbnail(thumbnail_imgs[current_index]); 
}


/* Communication with server */
function add_product_ajax() {
    $.post(ADD_URL, {
        item_name: $('#name-field').val(),
        item_link: $('#link-field').val(), 
        item_price: $('#price-field').val(), 
        item_description: $('#notes-field').val(), 
        item_thumbnail: $('#thumbnail-field').val(), 
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {
        $('#add-item-form input').val(''); 
        $('#add-item-form textarea').val(''); 
        $('.sad.message').slideUp(1000); 
        add_product_display(data); 
	thumbnail_imgs = [NO_IMG];
	update_thumbnails(); 
    }); 
}

function delete_product_ajax(elem, product_id) {
    $.post(DELETE_URL, {
	pid: product_id, 
	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {
	elem.fadeOut(1000, function() {
	    $(this).remove(); 
	}); 
    }); 
}

function get_thumbnails() {
    display_loading(); 

    $.post(THUMBNAILS_URL, {
	url: $('#link-field').val(), 
	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {
	if(data.length) {
	    thumbnail_imgs = [NO_IMG].concat(data); 
	} 
	update_thumbnails(); 
    }); 

}


/* Update the web page visually */
function add_product_display(html_string) {
    $('#wishlist-items-main').prepend(html_string);
    $('.wishlist-item-wrapper').slideDown(1000); 
}