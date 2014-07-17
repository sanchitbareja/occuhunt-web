
// download document
function download_document(document_id){
    $.ajax({
        url: '/api/v2/visits/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
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
