$(document).ready(function() {
    $('#main').on('click', '.editable-content', function() {
	make_editable(this); 
    }); 

    $('#main').on('keypress', '.editable-content', function(e) {
	if(!$(this).attr('contenteditable')) 
	    return; 

	if(e.charCode === 13) {
	    e.preventDefault(); 

	    $(this).attr("contenteditable", "false"); 
	    edit_field_ajax(this);
	}
    }); 

    $('#main').on('focusout', '.editable-content', function(e) {
	$(this).attr("contenteditable", "false"); 
	edit_field_ajax(this);
    }); 

}); 

function make_editable(elem) {
    $(elem).attr("contenteditable", "true").focus(); 
    $(elem).addClass('active'); 
}

/* Code that communicates with the server */
function edit_field_ajax(elem) {
    $.post(THIS_URL, {
	edit: $(elem).data('edit'), 
	datid: $(elem).data('id'), 
	dvalue: $(elem).text(), 
	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(), 
    }, function(data) {

    }); 
}