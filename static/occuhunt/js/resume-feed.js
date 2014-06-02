$(document).ready(function(){
	$('#imageholder img').on('mousemove', null, [$('#horizontal'), $('#vertical')], function(e){
    e.data[1].css('left', e.offsetX);
    e.data[0].css('top', e.offsetY);
	});

	$('#imageholder').on('mouseenter', null, [$('#horizontal'), $('#vertical')], function(e){
	    e.data[0].show();
	    e.data[1].show();
	}).on('mouseleave', null, [$('#horizontal'), $('#vertical')], function(e){
	        e.data[0].hide();
	        e.data[1].hide();
	    }
	);
	$('#imageholder').click(function () {
		console.log('I clicked!');
		$("#imageholder").popover();
	});
});

jQuery(function ($) {
    var content = $('#content').annotator();
    // content.annotator('addPlugin', 'Store');
    // content.annotator('addPlugin', 'Auth');
    // content.annotator('addPlugin', 'Permissions');
});