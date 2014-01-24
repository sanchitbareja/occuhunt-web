//
//
// This file assumes that the LinkedIn JS API has already been loaded before hand.
//
//

var linkedin_connections_list_id = "linkedin_connections";
var connection = null;
var request_recommendation_div = "request_recommendation";
var request_preview_div = "request_preview";
var linkedin_connection_info = "linkedin_connection_info";
var linkedin_connection_image = "linkedin_connection_image";
var linkedin_connection_info_preview = "linkedin_connection_info_preview";
var linkedin_connection_image_preview = "linkedin_connection_image_preview";
var linkedin_connection_input_project = "linkedin_connection_input_project";
var linkedin_connection_input_relationship = "linkedin_connection_input_relationship";
var linkedin_connection_textarea_message = "linkedin_connection_textarea_message";
var linkedin_subject_preview = "linkedin_subject_preview";
var linkedin_subject_name_preview = "linkedin_subject_name_preview";
var linkedin_subject_project_preview = "linkedin_subject_project_preview";
var linkedin_message_preview = "linkedin_message_preview";
var linkedin_connection_
var linkedin_connections_list = [];

//get a list of connections and update the UI
$(document).ready(function(){
	IN.API.Connections("me").result(function(result) {
		console.log("my connections");
		linkedin_connections_list = result.values;
		console.log(linkedin_connections_list);
		update_list();
	});
});

// UI Updates
// bindings to change picture as soon as a connection is clicked
function update_list(){
	$("#"+linkedin_connections_list_id).empty();
	for (var i = linkedin_connections_list.length - 1; i >= 0; i--) {
		$("#"+linkedin_connections_list_id).append('<a class="list-group-item" onclick="selected_connection('+i+')">'+linkedin_connections_list[i].firstName+' '+linkedin_connections_list[i].lastName+'</a>');
	};
}

function selected_connection(list_index){
	connection = linkedin_connections_list[list_index];
	// update image
	if(connection.pictureUrl){
		$("#"+linkedin_connection_image).attr("src",connection.pictureUrl);
		$("#"+linkedin_connection_image_preview).attr("src",connection.pictureUrl);
		console.log(connection)
	} else {
		$("#"+linkedin_connection_image).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		$("#"+linkedin_connection_image_preview).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");	
	}

	// update headline
	if(connection.headline){
		$("#"+linkedin_connection_info).text(connection.firstName+" "+connection.firstName+", "+connection.headline);
		$("#"+linkedin_connection_info_preview).text(connection.firstName+" "+connection.firstName+", "+connection.headline);
	} else {
		$("#"+linkedin_connection_info).text(connection.firstName+" "+connection.firstName);
		$("#"+linkedin_connection_info_preview).text(connection.firstName+" "+connection.firstName);
	}

	// update subject line with name
	$("#"+linkedin_subject_name_preview).text(connection.firstName+" "+connection.lastName);
}


// live changes to preview
$("#"+linkedin_connection_input_project).keyup(function(eventObject){
	$("#"+linkedin_subject_project_preview).text($(this).val());
});

$("#"+linkedin_connection_textarea_message).keyup(function(eventObject){
	$("#"+linkedin_message_preview).text($(this).val());
});


// Network calls
// send linkedin message 
function send_request(){
	if(connection){

		// construct linkedin API body data
		var BODY = {
	       	"recipients": {
	          	"values": [{
	            	"person": {
	               	"_path": "/people/~", // need to replace with actual person's id.
	            	}
	          	}]
	        },
	      	"subject": "Hi "+connection.firstName+", I wanted your input on my work for "+$("#"+linkedin_connection_input_project).val()+".",
		    "body": $("#"+linkedin_connection_textarea_message).val()+" View the request on http://occuhunt.com/recommend/requests/",
		}

		// send linkedin API request
	    IN.API.Raw("/people/~/mailbox")
	          .method("POST")
	          .body(JSON.stringify(BODY)) 
	          .result(console.log("successfully posted message"))
	          .error(function error(e) { alert ("No dice") });

        // update our own server 
		$.ajax({ 
		    url:'/api/v1/recommendation_requests/', 
		    type:'POST',
		    dataType: 'json',
		    data: JSON.stringify({
		      'from': 'ykkFoi6c68', 
		      'to': connection.id,
		      'relationship': $("#"+linkedin_connection_input_relationship).val(),
		      'project': $("#"+linkedin_connection_input_project).val(),
		      'message': $("#"+linkedin_connection_textarea_message).val(),
		    }),
		    contentType: 'application/json',
		    statusCode : {
		      201: function(data, textStatus, jsXHR){
		        console.log(data);
		        console.log(textStatus);
		        console.log(jsXHR);
		      },
		      500: function(data, textStatus, jsXHR){
		        console.log(data);
		        console.log(textStatus);
		        console.log(jsXHR);
		      }
		    }
		});

		// sent recommendations UI
		$("#"+request_preview_div).remove();
		$("#"+request_recommendation_div).replaceWith('<div class="category_box" id="request_sent">'+
			'<img src="/static/images/checkmark.png" style="height:100px;"/>'+
			'<h1>Request Sent</h1>'+
			'<i>Good work! Recommendations are the first step to a great start! <a href="/recommend/requests/new/" class="btn btn-link">Send more recs</a></i>'+
		'</div>');
	} else {
		// show error message that they need to select someone to send to
	}
}