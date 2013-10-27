function addInputField(e){
  // Here you'll do whatever you want to happen when they click
  var textareaHtml = $('');
  var doneButton = $('<div id="note-options">'+
    '<textarea id="note-options" class="form-control" rows="3" style="width:100%; margin-top:5px; padding-left: 6px;padding-top: 5px;padding-right: 6px;"></textarea>'+
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
    // make AJAX request to update
    updateFavorite(favorite_id, category, note);
  }
  console.log(e);
  $(e).remove();
}

function updateFavorite(favorite_id, category, note){
  console.log(favorite_id);
  console.log(category);
  console.log(note);
  favorite_url = '/api/v1/favorites/'+favorite_id+'/';
  console.log(favorite_url);
  $.ajax({ 
    url: favorite_url, 
    type:'PUT',
    dataType: 'json',
    data: JSON.stringify({
      'favorite': favorite_id,
      'note': note,
      'category': category
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