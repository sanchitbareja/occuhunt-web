function addInputField(e){
  // Here you'll do whatever you want to happen when they click
  var textareaHtml = $('');
  var doneButton = $('<div id="note-options">'+
    '<textarea id="note-options" class="form-control" rows="3"></textarea>'+
    '<div id="note-buttons">'+
    '<button type="submit" class="btn btn-done btn-sm pull-right" onclick="addNote($(this).parent().parent());">DONE</button></div></div>');
  var note = $(e).find('.list-group-item-text').text();
  if($(e).find("textarea").length == 0){
    if(note){
      $(e).find('.list-group-item-text').text('');
    }
    $(e).append(doneButton);
    $(e).find('textarea').val(note);
    $(e).find('textarea').focus();
  }
}

function addNote(e){
  var note = $(e).find('textarea').val();
  if(note){
    $(e).parent().find('.list-group-item-text').text(note);
    favorite_id = $(e).parent().parent().parent().find('#favorite_id').val();
    note = $(e).parent().parent().parent().find('.list-group-item-text').text();
    category = $(e).parent().parent().parent().parent().find('.list-group-header-title').text();
    status = $(e).parent().parent().parent().parent().find('#application_status').val();
    // make AJAX request to update
    updateApplicationStatus(favorite_id, status, note);
  }
  console.log(e);
  $(e).remove();
}

function updateApplicationStatus(favorite_id, status, note){
  console.log(favorite_id);
  console.log(status);
  console.log(note);
  favorite_url = '/api/v2/applications/'+favorite_id+'/';
  console.log(favorite_url);
  $.ajax({ 
    url: favorite_url, 
    type:'PUT',
    dataType: 'json',
    data: JSON.stringify({
        'student_note': note,
        'status': status
    }),
    contentType: 'application/json',
    statusCode : {
      201: function(data, textStatus, jsXHR){
        console.log("Successfully changed favorite company!");
      },
      400: function(data, textStatus, jsXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jsXHR);
      }
    }
  });
}

function refreshStats(){
    // update the number of companies left in the list
    var listGroups = $(".list-group");
    for (var i = listGroups.length - 1; i >= 0; i--) {
        $(listGroups[i]).find('.list-group-header-stats').text($(listGroups[i]).find('.list-group-item').length);
    };
}

function initialize_favoriting() {
    console.log("initialize_favoriting");
    var oldContainer;
    $("div.list-group").sortable({
        containerSelector:"div.list-group-item.user-enable-dragging", 
        itemSelector:"div.list-group-item.user-enable-dragging",
        group:"list-group", 
        pullPlaceholder:true, 
        placeholder:'<div class="list-group-item"/>',
        afterMove: function (placeholder, container) {
            console.log("switching!");
            if(oldContainer != container){
                if(oldContainer) {
                    oldContainer.el.removeClass("activate");
                }
                container.el.addClass("activate");
        
                oldContainer = container;
            }
        },
        onDrop: function ($item, container, _super) {
            $item.removeClass("dragged").removeAttr("style");
            $("body").removeClass("dragging");
            oldContainer.el.removeClass("activate");

            favorite_id = $($item).find('#favorite_id').val();
            note = $($item).find('.list-group-item-text').text();
            category = $($item).parent().find('.list-group-header-title').text();
            status = $($item).parent().find('#application_status').val();

            updateApplicationStatus(favorite_id, status, note);
            refreshStats();
            console.log(favorite_id);
            console.log(note);
            console.log(status);
        },
    });
}

// Get application statuses
function get_application_statuses() {
    console.log("get application statuses");
    $.ajax({
        url: '/api/v2/applications/',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        data: {},
        statusCode: {
            200: function(data, status, xhr){
                console.log(1);
                // add link to the list
                console.log(data);
                add_application_statuses(data['response']['applications']);
                refreshStats();
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

function add_application_statuses(application_statuses){
    // status reference
    // 1: 'Applied'
    // 2: 'Interacted With'
    // 3: 'Rejected',
    // 4: 'To Interview',
    // 5: 'Offered',
    // 6: 'Considering',
    $('.list-group-item').remove();
    var category = "#favorite-category-applied-considering";
    var user_control_dragging = "user-disable-dragging";
    for(i in application_statuses){
        if (application_statuses[i]['status'] == 1) {
            category = "#favorite-category-applied-considering";
        };
        if (application_statuses[i]['status'] == 2) {
            category = "#favorite-category-applied-considering";
        };
        if (application_statuses[i]['status'] == 3) {
            category = "#favorite-category-rejected";
        };
        if (application_statuses[i]['status'] == 4) {
            category = "#favorite-category-interviewing";
        };
        if (application_statuses[i]['status'] == 5) {
            category = "#favorite-category-offered";
        };
        if (application_statuses[i]['status'] == 6) {
            category = "#favorite-category-applied-considering";
        };
        if (application_statuses[i]['added_by_user'] == false && application_statuses[i]['status'] == 1) {
            user_control_dragging = "user-disable-dragging";
        } else {
            user_control_dragging = "user-enable-dragging";
        }
        $(category).append('<div class="list-group-item '+user_control_dragging+'">'+
            '<input id="favorite_id" type="hidden" value="'+application_statuses[i]['id']+'"/>'+
            '<div class="row">'+
                '<div class="col-lg-12">'+
                    '<div class="row">'+
                        '<div class="col-lg-2">'+
                            '<a target="_blank" href="/company/'+application_statuses[i]['company']['id']+'/"><img class="logo-thumbnail" src="'+application_statuses[i]['company']['logo']+'"></a>'+
                        '</div>'+
                        '<div class="col-lg-8">'+
                            '<h4 class="list-group-item-heading">'+application_statuses[i]['company']['name']+'</h4>'+
                        '</div>'+
                        '<div class="col-lg-2">'+
                            '<a class="pull-right" id="write-note" onclick="addInputField($(this).parent().parent().parent());"><span class="glyphicon glyphicon-pencil"></span></a>'+
                        '</div>'+
                    '</div>'+
                    '<div class="row">'+
                        '<div class="col-lg-10 col-lg-offset-2">'+
                            '<p class="list-group-item-text">'+application_statuses[i]['student_note']+'</p>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>');
    }
}

// this is used by dashboard page
function initialize(){
    // update_favorites();
    initialize_favoriting();
    get_application_statuses();
}
