

$(document).ready(function(){
	console.log($("input[name=recommendation_for]").val());
	console.log($("input[name=recommendation_by]").val());
	update_details($("input[name=recommendation_for]").val());
});

function update_details(linkedin_uid){
	IN.API.Profile(String(linkedin_uid)).result(function(result) {
	   	console.log(result.values[0]);
	   	$("#recommendation_for_name").text(result.values[0].firstName+" "+result.values[0].lastName);
	   	if(result.values[0].pictureUrl){
			$("#recommendation_for_image").attr("src",result.values[0].pictureUrl);
		} else {
			$("#recommendation_for_image").attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		}
	});
}

function send_recommendation(){
	var request_id = ($("input[name=request_id]").val())? $("input[name=request_id]").val(): null;
	$.ajax({
	    url:'/api/v1/recommendations/', 
	    type:'POST',
	    dataType: 'json',
	    data: JSON.stringify({
	      'from': $("input[name=recommendation_by]").val(), 
	      'to': $("input[name=recommendation_for]").val(),
	      'relationship': $("input[name=recommendation_relationship]").val(),
	      'project': $("input[name=recommendation_project]").val(),
	      'answer1': $("input[name=recommendation_answer1]").val(),
	      'answer2': $("input[name=recommendation_answer2]").val(),
	      'answer3': $("textarea[name=recommendation_answer3]").val(),
	      'replied': request_id
	    }),
	    contentType: 'application/json',
	    statusCode : {
	      201: function(data, textStatus, jsXHR){
	        console.log("successfully sent recommendation!");
	        // sent recommendations UI
			$("#recommendation_form").replaceWith('<div class="category_box" id="request_sent">'+
				'<img src="/static/images/checkmark.png" style="height:100px;"/>'+
				'<h1>Recommendation Sent</h1>'+
				'<i>Good work! Recommendations are the first step to a great start! <a href="/showcase/requests/new/" class="btn btn-link">Send more recs</a></i>'+
			'</div>');
	      },
	      500: function(data, textStatus, jsXHR){
	        console.log(data);
	        console.log(textStatus);
	        console.log(jsXHR);
	      }
	    }
	});
}