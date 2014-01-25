

$(document).ready(function(){
	$("input[name=recommendation_to]").each(function(index){
		console.log($(this).val());
		recommendations_given_ui($(this).val());
	});
	$("input[name=person_who_recommended_me]").each(function(index){
		console.log($(this).val());
		person_who_recommended_me_ui($(this).val());
	});
	recommend_friends_ui();
});

function recommendations_given_ui(linkedin_uid){
	IN.API.Profile(String(linkedin_uid)).result(function(result) {
		console.log("Recform New Route");
	   	console.log(result.values[0]);
	   	$("#recommendation_given_name0_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName);
	   	$("#recommendation_given_name1_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName);
	   	$("#recommendation_given_name2_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName);
	   	$("#recommendation_given_name3_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName);
	   	if(result.values[0].pictureUrl){
			$("#recommendation_given_image_"+String(linkedin_uid)).attr("src",result.values[0].pictureUrl);
		} else {
			$("#recommendation_given_image_"+String(linkedin_uid)).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		}
	});
}

function person_who_recommended_me_ui(linkedin_uid){
	IN.API.Profile(String(linkedin_uid)).result(function(result) {
		console.log("Recform New Route");
	   	console.log(result.values[0]);
	   	if(result.values[0].pictureUrl){
			$("#person_who_recommended_me_"+String(linkedin_uid)).attr("src",result.values[0].pictureUrl);
		} else {
			$("#person_who_recommended_me_"+String(linkedin_uid)).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		}
	   	$("#person_who_recommended_me_"+String(linkedin_uid)).tooltip({'placement':'left','title':result.values[0].firstName+" "+result.values[0].lastName});
	});
}

function recommend_friends_ui(){
	IN.API.Connections("me").result(function(result) {
		for (var j = 5; j >= 0; j--) {
			i = Math.floor((Math.random()*result.values.length))
			if(result.values[i].pictureUrl){
				$("#recommend_connections").append('<div class="list-group-item">'+
		    		'<img src="'+result.values[i].pictureUrl+'" style="height:40px;">'+
		    		'<span> '+result.values[i].firstName+'</span>'+
		    		'<a href="/recommend/new/'+result.values[i].id+'/" class="btn-sm btn btn-success pull-right">Rec</a>'+
				'</div>');
		    } else {
		    	$("#recommend_connections").append('<div class="list-group-item">'+
		    		'<img src="https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png" style="height:40px;">'+
		    		'<span> '+result.values[i].firstName+' '+result.values[i].lastName+'</span>'+
		    		'<a href="/recommend/new/'+result.values[i].id+'/" class="btn-sm btn btn-success pull-right">Rec</a>'+
				'</div>');
		    }
		};
	});
	
}