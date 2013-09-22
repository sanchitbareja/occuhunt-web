function favoriteCompany(){
  company_id = $("#company_id").val();
  user_id = $("#user_id").val();
  console.log(user_id);
  $.ajax({ 
    url:'/api/v1/favorites/', 
    type:'POST',
    dataType: 'json',
    data: JSON.stringify({
      'company': company_id, 
      'user': user_id,
      'unfavorite': false
    }), 
    contentType: 'application/json',
    statusCode : {
      201: function(data, textStatus, jsXHR){
        console.log("Successfully favorited company!");
        $("#favorite_company_btn").html('<span class="glyphicon glyphicon-minus"></span>&nbsp;Unfavorite');
        $("#favorite_company_btn").attr('onclick', 'unfavoriteCompany();');
      }
    }
  });
}

function unfavoriteCompany(){
  company_id = $("#company_id").val();
  user_id = $("#user_id").val();
  console.log(user_id);
  $.ajax({ 
    url:'/api/v1/favorites/', 
    type:'POST',
    dataType: 'json',
    data: JSON.stringify({
      'company': company_id, 
      'user': user_id,
      'unfavorite': true,
    }), 
    contentType: 'application/json',
    statusCode : {
      201: function(data, textStatus, jsXHR){
        console.log("Successfully favorited company!");
        $("#favorite_company_btn").html('<span class="glyphicon glyphicon-plus"></span>&nbsp;Favorite');
        $("#favorite_company_btn").attr('onclick', 'favoriteCompany();');
      }
    }
  });
}

function getCompany(id){
  user_id = $("#user_id").val();
  $.ajax({
    url: '/api/v1/companies/'+id+'/',
    data: {},
    success: function(data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        $("#company_name").text(data['name']);
        $("#company_description").text(data['company_description']);
        $("#company_looking_for").text(data['position_types']);
        $("#company_number_of_expected_hires").text(data['expected_hires']);
        $("#company_id").val(id);
        // need to check if need to display favorite or unfavorite icon
        if(data['favorites'].indexOf(parseInt(user_id)) >= 0){
          $("#favorite_company_btn").html('<span class="glyphicon glyphicon-minus"></span>&nbsp;Unfavorite');
          $("#favorite_company_btn").attr('onclick', 'unfavoriteCompany();');
        } else {
          $("#favorite_company_btn").html('<span class="glyphicon glyphicon-plus"></span>&nbsp;Favorite');
          $("#favorite_company_btn").attr('onclick', 'favoriteCompany();');
        }
      },
    dataType: 'json',
  });
}

function getHunting(id){
  $.ajax({
    url: '/api/v1/hunting/',
    type: 'GET',
    contentType: 'application/json',
    data: {
      "fair":"1",
      "user":"2",
    },
    processData: false,
    success: function(data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        $("#fair").text(data['fair']);
        $("#user").text(data['user']);
      },
    dataType: 'json',
  });
}

function toggleTable(cssID){
  if($(cssID).css('background-color') == "rgb(255, 255, 255)") {
    if(cssID == '.btn-categorydisabled'){
      recolorTables(cssID,'grey');
    }
    if(cssID == '.btn-engineering'){
      recolorTables(cssID,'#baf198');
    }
    if(cssID == '.btn-finance'){
      recolorTables(cssID,'#ffb8e7');
    }
    if(cssID == '.btn-government'){
      recolorTables(cssID,'');
    }
    if(cssID == '.btn-health'){
      recolorTables(cssID,'#fe9f9f');
    }
    if(cssID == '.btn-technology'){
      recolorTables(cssID,'#c4dff9');
    }
    if(cssID == '.btn-other'){
      recolorTables(cssID,'#ffcfaf');
    }
  } else {
    decolorTables(cssID)
  }
}

function decolorTables(cssID){
  $(cssID).css('background-color','white');
}

function recolorTables(cssID, color){
  $(cssID).css('background-color',color);
}
