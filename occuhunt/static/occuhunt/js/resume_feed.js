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

function s3_upload(){
    console.log("hello");
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
            $("#upload_button_div").hide();
            console.log(public_url);

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
