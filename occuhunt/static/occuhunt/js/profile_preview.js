
// download document
function download_document(document_id){
    $.ajax({
        url: '/api/v2/visits/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            "Authorization": 'OAuth 6f9dd960cb005f85b5ba81c158829fe11c3541d9'
        },
        data: JSON.stringify({
            'document':document_id,
            'visit_type':2 
        }),
        statusCode: {
            201: function(data, status, xhr){
                console.log(1);
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
}

// visit link
function visit_link(document_id, link_id){
    $.ajax({
        url: '/api/v2/visits/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            "Authorization": 'OAuth 6f9dd960cb005f85b5ba81c158829fe11c3541d9'
        },
        data: JSON.stringify({
            'document':document_id,
            'visit_type':3,
            'link':link_id
        }),
        statusCode: {
            201: function(data, status, xhr){
                console.log(1);
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
}

// visited homepage
function visit_document(document_id){
    $.ajax({
        url: '/api/v2/visits/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            "Authorization": 'OAuth 6f9dd960cb005f85b5ba81c158829fe11c3541d9'
        },
        data: JSON.stringify({
            'document':document_id,
            'visit_type':1
        }),
        statusCode: {
            201: function(data, status, xhr){
                console.log(1);
            },
            404: function(){
                console.log(3);
            },
            500: function(){
                console.log(4);
            }
        }
    });
}


// view analytics for link
function get_visits(document_id) {
    $.ajax({
        url: '/api/v2/visits/',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            "Authorization": 'OAuth 6f9dd960cb005f85b5ba81c158829fe11c3541d9'
        },
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


// onload

function initialize() {
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

    // get document_id
    var document_id = $("input[name=document_id]").val();
    visit_document(document_id);
    get_visits(document_id);
}

function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
      'callback=initialize';
    document.body.appendChild(script);
}

window.onload = loadScript;
