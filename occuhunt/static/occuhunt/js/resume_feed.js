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
    $("#file_upload").before('<br /></br /><div id="spinnerWait"><div class="spinner"><div class="bar1"></div><div class="bar2"></div><div class="bar3"></div><div class="bar4"></div><div class="bar5"></div><div class="bar6"></div><div class="bar7"></div><div class="bar8"></div><div class="bar9"></div><div class="bar10"></div><div class="bar11"></div><div class="bar12"></div></div><p></p></div>');

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

                // show canvas
                $("#"+canvasId).css("display","block");

                // show upload_button
                $("#"+uploadBtnId).css("display", "block");

                // hide file select button
                $("#"+fileSelectBtnId).css("display", "none");

                // make canvas drawable
                init_canvas_drawing();
            }
        });
    }
}

function init_canvas_drawing() {
    ctx = document.getElementById(canvasId).getContext("2d");

    $('#'+canvasId).mousedown(function (e) {
        mousePressed = true;
        canvas_draw(e.pageX - $(this).offset().left + 10, e.pageY - $(this).offset().top + 10, false);
    });

    $('#'+canvasId).mousemove(function (e) {
        if (mousePressed) {
            canvas_draw(e.pageX - $(this).offset().left + 10, e.pageY - $(this).offset().top + 10, true);
        }
    });

    $('#'+canvasId).mouseup(function (e) {
        mousePressed = false;
    });
    $('#'+canvasId).mouseleave(function (e) {
        mousePressed = false;
    });
}

function canvas_draw(x, y, isDown) {
    ctx = document.getElementById(canvasId).getContext("2d");
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 20;
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}
  
function canvas_clear_area() {
    ctx = document.getElementById(canvasId).getContext("2d");
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
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

// 
// 
// Commenting and adding resumes
// 
// 


function add_new_comment(e) {
    if(e.which == 13) {
        console.log(e);
        console.log($(e.currentTarget).parent());
        // make ajax request to post comment on the resume
        var resume_id = $(e.data).find("#resume_id").val();
        var comment_x = $(e.currentTarget).parent().find("#comment_x").val();
        var comment_y = $(e.currentTarget).parent().find("#comment_y").val();
        var comment_text = $(e.currentTarget).val();
        var user_id = $("#user_id").val();
        $.ajax({
            url: '/api/v1/comments/',
            type: 'POST',
            data: JSON.stringify({
              'user': user_id,
              'resume': resume_id,
              'comment': comment_text,
              'x': comment_x,
              'y': comment_y
            }), 
            dataType: 'json',
            contentType: 'application/json',
            statusCode : {
                201: function(data, textStatus, jsXHR){
                    console.log(data);
                    console.log(textStatus);
                    console.log(jsXHR);
                    console.log(data["user"]);
                    console.log(data["user"]["resume_points"]);

                    $(e.currentTarget).parent().replaceWith('<div class="comment-box" style="position:absolute; top:'+comment_y+'px; "><p>'+comment_text+'</p></div>');
                },
                500: function(data, textStatus, jsXHR){
                    console.log(data);
                    console.log(textStatus);
                    console.log(jsXHR);
                }
            }
        });
    }
}

function get_resumes(){
    $.ajax({
        url: '/api/v1/resumes/',
        data: {},
        dataType: 'json',
        success: function(data, textStatus, jqXHR){
            for (var i = data['response']['resumes'].length - 1; i >= 0; i--) {
                add_new_resume_html(data['response']['resumes'][i]['id'],data['response']['resumes'][i]['url'],data['response']['resumes'][i]['comments']);
            };
        },
    });
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
        }), 
        dataType: 'json',
        contentType: 'application/json',
        statusCode : {
            201: function(data, textStatus, jsXHR){
                console.log(data);
                if(should_add_new_resume){
                    // remove canvas_div
                    $("#canvas_div").remove();
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
    var comment_boxes = '';
    var comment_circles = '';
    if (comments) {

        for (var i = comments.length - 1; i >= 0; i--) {
            console.log(comments[i]['y']);
            // id = comment-{comment-id}
            var comment_box = '<div class="comment-box" id="comment-'+comments[i]['id']+'" style="position:absolute; top:'+comments[i]['y']+'px; "><p>'+comments[i]['comment']+'</p></div>';
            comment_boxes = comment_boxes + comment_box;
            comment_circles = comment_circles + "<a onclick='toggle_comment(event, "+comments[i]['id']+");' id='comment-circle-"+comments[i]['id']+"' class='circle' style='position: absolute;z-index: 10; top:"+comments[i]['y']+"px; left:"+comments[i]['x']+"px;'></a>";
        };
    };
    $("#resume-feed").prepend(
    '<div class="row">'+
      '<div class="col-lg-1 col-sm-1"></div>'+
      '<div class="col-lg-8 col-sm-8">'+
        '<div class="row resume-container">'+
          '<img class="resume-image" src="'+url+'" />'+
          '<input type="hidden" id="resume_id" value="'+resume_id+'" >'+
          comment_circles + 
        '</div>'+
        '<hr />'+
      '</div>'+
      '<div class="col-lg-3 col-sm-3">'+
        '<div class="row comments-container">'+
                comment_boxes+
            '</div>'+
        '</div>'+
      '</div>'+
    '</div>');
    bind_events();
}

function bind_events(){
    $(".resume-container").on("click", function(e) {
        // calculate where to add circle
        var offset_t = $(this).offset().top - $(window).scrollTop();
        var offset_l = $(this).offset().left - $(window).scrollLeft();
        var left = e.clientX - offset_l - 10;
        var top = e.clientY - offset_t - 10;
        var box_position = top - 12;

        // create comment box
        var comments_div = $(this).parent().parent().find(".comments-container");
        var comment_input = $.parseHTML('<input type="text" class="form-control comment-input" placeholder="Add a comment..">');
        var comment_x = $.parseHTML('<input type="hidden" id="comment_x" value="'+left+'">');
        var comment_y = $.parseHTML('<input type="hidden" id="comment_y" value="'+top+'">');
        var comment_box = $.parseHTML('<div class="comment-box" style="position:absolute; top:'+box_position+'px;"></div>');
        
        // add circle
        var circle = $.parseHTML("<a class='circle' style='position: absolute;z-index: 10; top:"+top+"px; left:"+left+"px;'></a>");
        $(this).append(circle);
  
        $(comment_input).keypress(this, add_new_comment);
        $(comment_input).keyup(function(e) {
            if (e.keyCode == 27) { 
                $(comment_input).focusout();
            }
        });
        
        $(comment_box).append(comment_input);
        $(comment_box).append(comment_x);
        $(comment_box).append(comment_y);
        $(comments_div).append(comment_box);
        
        $(comment_input).focus();
        $(comment_input).focusout(function() {
            if ($(this).val() == '') {
                $(comment_box).remove();
                $(circle).remove();
            }
            else {
                $(this).blur();
            }
        });

   });

}

function toggle_all_comments(){
    $("#toggle-comments").on("click", function(e){
        $(".comments-container").toggle();
        $(".circle").toggle();
        $("#toggle-comments").toggleClass("toggleCommentsButton");

        // the next 2 lines will toggle the Hide Comments button.
        $("#toggle-comments").text("Hide Comments");
        $(".toggleCommentsButton").text("Show Comments");
    })
}

function toggle_comment(event, comment_id){
    console.log("toggle_comment fired");
    console.log(event);
    event.cancelBubble = true;
    $("#comment-"+comment_id).toggle();
    $("#comment-circle-"+comment_id).toggleClass("toggleCircle");
}

// 
// Update statistics
// 

function get_bounty(){
    console.log("getting boutny");  
    
    $.ajax({
        url: '/api/v1/users/'+$("#user_id").val()+'/',
        data: {},
        dataType: 'json',
        success: function(data, textStatus, jqXHR){
            console.log(data);

            $("#resume-menu-bounty").contents()[0].nodeValue = 'Bounty: ' + data["resume_points"];
        },
    });
};  


$(document).ready(function() {
    get_resumes();
    toggle_all_comments();
    get_bounty();
});
