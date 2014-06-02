/* -*- Mode: Java; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set shiftwidth=2 tabstop=2 autoindent cindent expandtab: */

//
// See README for overview
//

'use strict';

//
// Fetch the PDF document from the URL using promises
//
var BASE64_MARKER = ';base64,';
var mousePressed = false;
var lastX, lastY;
var ctx;
var canvasId = 'the-canvas';
var uploadBtnId = 'upload_button';
var fileSelectBtnId = 'file_select_div';
var fileUploadId = 'file_upload';
var canvasHeight = 0;
var canvasWidth = 778;
var feature_resume = false;
var bounty_points = 0;
var page_limit = 10;
var current_offset = 0;

function convert_data_URI_to_binary(dataURI) {
    var base64Index = dataURI.indexOf(BASE64_MARKER) + BASE64_MARKER.length;
    var base64 = dataURI.substring(base64Index);
    var raw = window.atob(base64);
    var rawLength = raw.length;
    var array = new Uint8Array(new ArrayBuffer(rawLength));
 
    for(var i = 0; i < rawLength; i++) {
        array[i] = raw.charCodeAt(i);
    }
    return array;
}

function render_pdf(){
    var file_element = document.getElementById(fileUploadId);
    var reader = new FileReader();
    var files = file_element.files;
    console.log(files);
    s3_upload_original();
    reader.onload = function (event) {
        //converts pdf to canvas element and makes canvas element editable
        parse_pdf(convert_data_URI_to_binary(event.target.result));
    };

    var myURL = reader.readAsDataURL(files[0]);

};

function parse_pdf(data){
    // function variables
    canvasHeight = 0;
    var pages = new Array();
    var pageStarts = new Array();
    var canvas = document.getElementById(canvasId);
    var context = canvas.getContext('2d');
    var pdfPages;
    var currPage = 1;
    var numPages = 1;

    // init variables
    pageStarts[0] = 0;

    // Show loading state
    $("#"+fileUploadId).before('<div id="spinnerWait"><div class="spinner"><div class="bar1"></div><div class="bar2"></div><div class="bar3"></div><div class="bar4"></div><div class="bar5"></div><div class="bar6"></div><div class="bar7"></div><div class="bar8"></div><div class="bar9"></div><div class="bar10"></div><div class="bar11"></div><div class="bar12"></div></div><p></p></div>');

    PDFJS.getDocument(data).then(function(pdf) {
        pdfPages = pdf;
        numPages = pdf.numPages;
        // Using promise to fetch the page
        pdfPages.getPage(currPage).then(handle_page);
    });

    function handle_page(page){
        var scale = canvasWidth/page.getViewport(1.0).width;
        var viewport = page.getViewport(scale);

        // Prepare canvas using PDF page dimensions
        canvas.width = canvasWidth;
        canvas.height = viewport.height/viewport.width * canvasWidth;

        // Render PDF page into canvas context
        page.render({
            canvasContext: context,
            viewport: viewport
        }).then(function() {
            // update variables to keep track of pages rendered
            pages[currPage - 1] = context.getImageData(0, 0, canvas.width, canvas.height);
            pageStarts[currPage - 1] = canvasHeight;
            canvasHeight += canvas.height;

            //Move to next page
            currPage = currPage + 1;
            if(pdfPages !== null && currPage <= numPages) {
                pdfPages.getPage(currPage).then(handle_page);
            }

            if(currPage > numPages) {
                // finalize canvas height and width
                canvas.width = canvasWidth;
                canvas.height = canvasHeight;

                // update canvas with ALL pdf pages
                for (var i = 0; i < numPages; i++) {
                    console.log(i);
                    console.log(pageStarts[i]);
                    console.log(pages[i]);
                    context.putImageData(pages[i], 0, pageStarts[i]);
                }
            }
            s3_upload(false);
        });
    }
}

// 
// 
// Uploading images
// 
// 

// converts image data from canvas into a Blob object so that it can be used with s3Upload
function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}

function s3_upload(featured){
    featured = featured || "none"
    console.log("s3 upload");
    $('.progress-button').progressInitialize();
    var file_path = $("#"+fileUploadId).val();
    var file_name = string_to_slug(get_file_name_from_path(file_path));
    var s3upload = new S3Upload({
        file_data: dataURItoBlob(document.getElementById(canvasId).toDataURL('image/jpeg')),
        s3_sign_put_url: '/plan/resume-feed/new-resume/sign_s3_upload/',
        s3_object_name: file_name,

        onProgress: function(percent, message) {
            console.log(percent);
            $(".progress-button").progressSet(percent);
        },
        onFinishS3Put: function(public_url) {
            $("#resume_url").val(public_url);
            $(".progress-button").progressFinish();
            $("#"+uploadBtnId).text("YOU'RE ALL SET!");
            $("#"+uploadBtnId).attr("disabled","disabled");
            console.log(public_url);
            new_resume(public_url, true, false, true);
        },
        onError: function(status) {
            $('#status').html('Upload error: ' + status);
            console.log(status);
            alert("There was an error :( Please try again!");
            window.location.reload();
        }
    });
}

function s3_upload_original(){
    var file_path = $("#"+fileUploadId).val();
    var file_name = string_to_slug(get_file_name_from_path(file_path));
    var s3upload = new S3Upload({
        file_dom_selector: fileUploadId,
        s3_sign_put_url: '/plan/resume-feed/new-resume/sign_s3_upload/',
        s3_object_name: file_name,

        onProgress: function(percent, message) {
            console.log(percent);
        },
        onFinishS3Put: function(public_url) {
            console.log(public_url);
            // create an entry in resume of the original pdf
            new_resume(public_url, true, true, false);
        },
        onError: function(status) {
            console.log(status);
            // alert("There was an error :( Please try again!");
            // window.location.reload();
        }
    });
}

//convert any string to slug
function string_to_slug(str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
  
    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

  return str;
}

//return the filname from a path
// e.g. /path/to/file/file.ext will return file.ext
function get_file_name_from_path(fullPath) {
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
        if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
            filename = filename.substring(1);
        }
        return filename;
    }
    return "";
}



function new_resume(url,anonymous,original,should_add_new_resume){
    var user_id = $("#user_id").val();
    // do error checking if everything exists
    $.ajax({
        url: '/api/v1/resumes/',
        type: 'POST',
        data: JSON.stringify({
          'user': user_id,
          'url': url,
          'anonymous': anonymous,
          'original': original,
          'featured': feature_resume,
          'showcase': true
        }), 
        dataType: 'json',
        contentType: 'application/json',
        statusCode : {
            201: function(data, textStatus, jsXHR){
                console.log(data);
                if(should_add_new_resume){
                    // remove canvas_div
                    // $("#"+canvasId).remove();
                    // $("#canvas_div").append('<canvas id="the-canvas" style="display:none;" />');

                    console.log("uplaoded resume");
                    add_new_resume_html(data['id'],data['url']);
                }
            },
            500: function(data, textStatus, jsXHR){
                console.log(data);
                console.log(textStatus);
                console.log(jsXHR);
            }
        }
    });
}
function add_new_resume_html(resume_id,url,comments){
    // add image element
    var resume_direct_url = window.location.origin+"/plan/resume-feed/"+url.slice(36);
    $("#resume-showcase").empty();
    $("#resume-showcase").append('<img class="resume-image" src="'+url+'" />'+
          '<input type="hidden" id="resume_id" value="'+resume_id+'" >');

    $("#spinnerWait").remove();
}


//
//
// -- Recommendation 
//
//

function person_who_recommended_me_ui(linkedin_uid){
	IN.API.Profile(String(linkedin_uid)).result(function(result) {
		$("#recommendation_from_name0_"+String(linkedin_uid)).text(result.values[0].firstName+" "+result.values[0].lastName); 
	   	if(result.values[0].pictureUrl){
			$("#recommendation_from_image_"+String(linkedin_uid)).attr("src",result.values[0].pictureUrl);
		} else {
			$("#recommendation_from_image_"+String(linkedin_uid)).attr("src","https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png");
		}
	});
}

function recommend_friends_ui(){
	IN.API.Connections("me").result(function(result) {
		for (var j = 5; j >= 0; j--) {
			var i = Math.floor((Math.random()*result.values.length))
			if(result.values[i].pictureUrl){
				$("#recommend_connections").append('<div class="list-group-item">'+
		    		'<img src="'+result.values[i].pictureUrl+'" style="height:40px;">'+
		    		'<span> '+result.values[i].firstName+'</span>'+
		    		'<a href="/showcase/new/'+result.values[i].id+'/" class="btn-sm btn btn-success pull-right">Rec</a>'+
				'</div>');
		    } else {
		    	$("#recommend_connections").append('<div class="list-group-item">'+
		    		'<img src="https://www.clearsounds.com/sites/default/files/images/color-linkedin-128.png" style="height:40px;">'+
		    		'<span> '+result.values[i].firstName+' '+result.values[i].lastName+'</span>'+
		    		'<a href="/showcase/new/'+result.values[i].id+'/" class="btn-sm btn btn-success pull-right">Rec</a>'+
				'</div>');
		    }
		};
	});	
}
