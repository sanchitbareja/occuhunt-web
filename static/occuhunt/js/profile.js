/* -*- Mode: Java; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set shiftwidth=2 tabstop=2 autoindent cindent expandtab: */

//
// See README for overview
//

// 1. render pdf
// 2. parse pdf
// 3. s3_upload (uploads image)
// 4. s3_upload_original (uploads pdf)
// 5. create new document entry
// 6. add new document to UI

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
var fileUploadClass = 'file_upload';
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

function render_pdf(document_type){
    var file_element = $("."+fileUploadClass)[document_type-1];
    console.log(file_element);
    var reader = new FileReader();
    var files = file_element.files;
    console.log(files);
    show_loading_state();
    reader.onload = function (event) {
        //converts pdf to canvas element and makes canvas element editable
        parse_pdf(convert_data_URI_to_binary(event.target.result), document_type);
    };

    var myURL = reader.readAsDataURL(files[0]);

};

function parse_pdf(data, document_type){
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
                s3_upload(document_type);
            }
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

function s3_upload(document_type){
    console.log("s3 upload");
    var file_path = $($("."+fileUploadClass)[document_type-1]).val();
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
            s3_upload_original(public_url, document_type);
            // new_resume(public_url, true, false, true);
        },
        onError: function(status) {
            $('#status').html('Upload error: ' + status);
            console.log(status);
            alert("There was an error :( Please try again!");
            window.location.reload();
        }
    });
}

function s3_upload_original(image_url, document_type){
    var file_path = $($("."+fileUploadClass)[document_type-1]).val();
    var file_name = string_to_slug(get_file_name_from_path(file_path));
    var s3upload = new S3Upload({
        file_dom_class: fileUploadClass,
        file_number: document_type-1,
        s3_sign_put_url: '/plan/resume-feed/new-resume/sign_s3_upload/',
        s3_object_name: file_name,

        onProgress: function(percent, message) {
            console.log(percent);
        },
        onFinishS3Put: function(public_url) {
            console.log(public_url);
            // create an entry in resume of the original pdf
            // new_resume(public_url, true, true, false);
            add_document(document_type, image_url, public_url);
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

// Add a new resume/cv/portfolio doc
function add_document(document_type, image_url, pdf_url) {
    $.ajax({
        url: '/api/v2/documents/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            'document_type':document_type,
            'image_url':image_url,
            'pdf_url':pdf_url,    
        }),
        statusCode: {
            201: function(data, status, xhr){
                add_new_document(data['id'], data['document_type'], data['user']['username'], data['image_url'], data['unique_hash']);
                hide_loading_state();
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
};

// delete resume/cv/portfolio
function delete_document(user_id ,document_id, html_handle) {
    $.ajax({
        url: '/api/v2/documents/'+document_id+'/',
        type: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            'delete':true
        }),
        statusCode: {
            204: function(){
                $(html_handle).parent().parent().parent().remove();
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
};

// view analytics for link
function get_visits(document_id) {
    $.ajax({
        url: '/api/v2/visits/',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        data: {
            'document':document_id
        },
        statusCode: {
            200: function(data, status, xhr){
                console.log(1);
                // update the map and notification
                console.log(data);
                update_map_and_notifications(data['response']['visits'], data['meta']['total_count']);
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
};


function update_map_and_notifications(data_points, total_views){
    var mapOptions = {
        center: new google.maps.LatLng(37.87, -122.27),
        zoom: 14,
        disableDefaultUI: true,
        panControl: false,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        overviewMapControl: false
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    var latlngbounds = new google.maps.LatLngBounds();

    var visit_notifs = $("#visit_notifications");
    visit_notifs.empty();
    visit_notifs.prepend('<div class="list-group-item">'+
        '<h4><b>'+total_views+'</b> views <span>the past month</span></h4>'+
    '</div>');
    // check for data_points that have null values and empty strings. display them differently
    // 1 city could be null, empty
    // 2 region_code could be null, empty
    // 3 lat,lng could be null, empty
    // any one of the above could fail and in that case, can't show location at all.
    for (var i = 0; i <= data_points.length + 1; i++) {
        var time_obj = moment.utc(data_points[i]['timestamp']);
        var time_string = time_obj.fromNow().toString();
        if(data_points[i]['city']){
            // add marker to map and a notification
            if(data_points[i]['visit_type'] == 1){
                var myLatlng = new google.maps.LatLng(data_points[i]['lat'], data_points[i]['lng']);
                var marker = new google.maps.Marker({
                    position: myLatlng,
                    map: map,
                    title:"Visit"
                });
                latlngbounds.extend(myLatlng);
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Viewed: <b>'+time_string+'</b> from '+data_points[i]['city']+', '+data_points[i]['region_code']+'</p>'+
                '</div>');
            }
            if(data_points[i]['visit_type'] == 2){
                var myLatlng = new google.maps.LatLng(data_points[i]['lat'], data_points[i]['lng']);
                var marker = new google.maps.Marker({
                    position: myLatlng,
                    map: map,
                    title:"Download"
                });
                latlngbounds.extend(myLatlng);
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Download document: <b>'+time_string+'</b> from '+data_points[i]['city']+', '+data_points[i]['region_code']+'</p>'+
                '</div>');
            }
            if(data_points[i]['visit_type'] == 3){
                var myLatlng = new google.maps.LatLng(data_points[i]['lat'], data_points[i]['lng']);
                var marker = new google.maps.Marker({
                    position: myLatlng,
                    map: map,
                    title:"Click"
                });
                latlngbounds.extend(myLatlng);
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Clicked link: <b>'+time_string+'<b> from '+data_points[i]['city']+', '+data_points[i]['region_code']+'</p>'+
                '</div>');
            }
        } else {
            if(data_points[i]['visit_type'] == 1){
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Viewed: <b>'+time_string+'</b></p>'+
                '</div>');
            }
            if(data_points[i]['visit_type'] == 2){
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Downloaded document: <b>'+time_string+'</b></p>'+
                '</div>');
            }
            if(data_points[i]['visit_type'] == 3){
                visit_notifs.append('<div class="list-group-item">'+
                    '<p>Clicked link: <b>'+time_string+'</b></p>'+
                '</div>');
            }
        }
    };

    map.fitBounds(latlngbounds);
}




// Add a new link
function save_new_link(dom_element) {
    // check if label and link are valid
    var link_label = $(dom_element).parent().find("#link_label").val();
    var link_url = $(dom_element).parent().find("#link_url").val();
    console.log(link_label);
    console.log(link_url);
    $.ajax({
        url: '/api/v2/links/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            'label':link_label,
            'url':link_url 
        }),
        statusCode: {
            201: function(data, status, xhr){
                console.log(1);
                // add link to the list
                console.log(data);
                add_link_pill(data['id'], data['link_name'], data['url']);
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
};

// delete link
function delete_link(link_id, dom_element) {

    $.ajax({
        url: '/api/v2/links/'+link_id+'/',
        type: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
        }),
        statusCode: {
            204: function(){
                console.log(1);
                $(dom_element).parent().remove();
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
};

// Update UI
function add_new_document(document_id, document_type, username, image_url, hash){
    var documents_ul = $(".documents#resumes");
    if(document_type == 1){
        documents_ul = $(".documents#resumes");
    }
    if(document_type == 2){
        documents_ul = $(".documents#cvs");
    }
    if(document_type == 3){
        documents_ul = $(".documents#portfolio");
    }
    documents_ul.append('<li class="document">'+
        '<a href="/document/'+username+'/'+hash+'/" target="_blank"><img style="width:100%; height:100%;" src="'+image_url+'"></a>'+
        '<ul class="actions">'+
            '<li><a class="viewAnalytics" data-toggle="tooltip" data-placement="top" onclick="get_visits('+document_id+');"><span class="glyphicon glyphicon-eye-open"></span></a></li>'+
            '<li><a class="copyToClipboard" data-clipboard-text="http://www.occuhunt.com/document/'+username+'/'+hash+'/" data-toggle="tooltip" data-placement="top"><span class="glyphicon glyphicon-link"></span></a></li>'+
            '<li><a class="deleteResume" data-toggle="tooltip" data-placement="top" onclick="delete_document('+document_id+', this);"><span class="glyphicon glyphicon-trash"></span></a></li>'+
        '</ul>'+
    '</li>');
}

function add_link(){
    var add_new_link_div = $("#add_new_link");
    console.log('hello');
    add_new_link_div.append('<div style="display:inline-block; padding: 10px 0px;">'+
        '<input class="input-text" id="link_label" style="vertical-align:top; display:inline-block; width:25%;" type="text" placeholder="Label">'+
        '<input class="input-text" id="link_url" style="vertical-align:top; display:inline-block; width:50%;" type="text" placeholder="http://hello.com">'+
        '<button class="btn btn-sm btn-inverted-default" style="vertical-align:bottom; display:inline-block;" onclick="new_link(this);">Save</button>'+
    '</div>');
}

function add_link_pill(link_id, label, url){
    var link_pills = $("#link_pills");
    link_pills.append('<div class="label label-link">'+
        '<a style="color:#fdfdfd;" href="'+url+'" target="_blank"><span>'+label+'</span></a>&nbsp;'+
        '<span class="glyphicon glyphicon-remove" id="delete_link" onclick="delete_link('+link_id+',this);"></span>'+
    '</div>');
}


function show_loading_state(){
    $('.loading-state').show();
}

function hide_loading_state(){
    $('.loading-state').hide();
    initialize_clipboard();
}

function initialize_clipboard(){
    // copying to clipboard
    var client = new ZeroClipboard($('.copyToClipboard'), {
        moviePath : '/static/zeroclipboard/ZeroClipboard.swf'
    });

    client.on( 'mouseover', function ( event ) {
        $(this).attr('title', 'Click to copy and share').tooltip('fixTitle').tooltip("show");
    });

    client.on( 'mouseout', function ( event ) {
        $(this).tooltip("hide");
    });

    client.on( 'mousedown', function(event) {
        var newTitle = 'Copied!';
        $(this).attr('title', newTitle).tooltip('fixTitle').tooltip("show");
    });

    // view analytics for resume
    $(".viewAnalytics").attr("title","Who's viewed your doc?").tooltip('fixTitle').tooltip();

    // delete resume/cv/portfolio
    $(".deleteResume").attr("title",'Delete Resume').tooltip('fixTitle').tooltip();
}

// onload and ready

function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(37.87, -122.27),
        zoom: 14
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
      'callback=initialize';
    document.body.appendChild(script);
}

$(document).ready(function() {
    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    initialize_clipboard();
});

window.onload = loadScript;

