

$(document).ready(function(){
	$("input[name=rec_request]").each(function(index){
		console.log($(this).val());
		request_ui($(this).val());
	});
	recommend_friends_ui();
});

function request_ui(linkedin_uid){
	IN.API.Profile(String(linkedin_uid)).result(function(result) {
		console.log("Recform New Route");
	   	console.log(result.values[0]);
	   	console.log()
	   	$("#request_name_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName);
	   	if(result.values[0].pictureUrl){
			$("#request_image_"+String(linkedin_uid)).attr("src",result.values[0].pictureUrl);
		} else {
			$("#request_image_"+String(linkedin_uid)).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		}
	});
}

function recommend_friends_ui(){
	IN.API.Connections("me").result(function(result) {
		for (var i = result.values.length - 1; i >= 0; i--) {
			if(result.values[i].pictureUrl){
				$("#recommend_connections").append('<a href="/showcase/new/'+result.values[i].id+'/">'+
		      		'<div class="friend_thumbnail"><img src="'+result.values[i].pictureUrl+'" style="height:100px;">'+
		      		'<span>'+result.values[i].firstName+' '+result.values[i].lastName+'</span></div>'+
		      	'</a>');
		    } else {
		    	$("#recommend_connections").append('<a href="/showcase/new/'+result.values[i].id+'/">'+
		      		'<div class="friend_thumbnail"><img src="https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png" style="height:100px;">'+
		      		'<span>'+result.values[i].firstName+' '+result.values[i].lastName+'</span></div>'+
		      	'</a>');
		    }
		};
	});
	
}