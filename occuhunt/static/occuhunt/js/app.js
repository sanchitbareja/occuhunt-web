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
        $("#favorite_company_btn").html('<span class="glyphicon glyphicon-minus"></span>&nbsp;Unfav');
        $("#favorite_company_btn").attr('onclick', 'unfavoriteCompany();');
        $("button[value=company_"+company_id+"]").addClass("favorited-company");
      },
      500: function(data, textStatus, jsXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jsXHR);
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
        $("button[value=company_"+company_id+"]").removeClass("favorited-company");
      }, 
      500: function(data, textStatus, jsXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jsXHR);
      },
      400: function(data, textStatus, jsXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jsXHR);
      }
    }
  });
}

function favoriteCompanyWithId(company_id,element, callback){
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
        $(element).html('<span class="glyphicon glyphicon-minus">Remove</span>');
        $(element).attr('onclick', 'unfavoriteCompanyWithId('+company_id+',this,'+callback+');');
        callback();
      }
    }
  });
}

function unfavoriteCompanyWithId(company_id,element, callback){
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
        $(element).html('<span class="glyphicon glyphicon-plus">Add</span>');
        $(element).attr('onclick', 'favoriteCompanyWithId('+company_id+',this,'+callback+');');
        callback();
      }
    }
  });
}

function getCompanies(){
  user_id = $("#user_id").val();
  console.log("get companies");
  $.ajax({
    url: '/api/v1/companies/',
    data: {},
    success: function(data, textStatus, jqXHR) {
        // console.log(data);
        // console.log(textStatus);
        // console.log(jqXHR);
        if(user_id){
          for (var i = data['response']['companies'].length - 1; i >= 0; i--) {
            // need to check if need to display favorite or unfavorite icon
            if(data['response']['companies'][i]['favorites'].indexOf(parseInt(user_id)) >= 0){
              console.log($("a[value=company_"+data['response']['companies'][i]['id']+"]"));
              $("a[value=company_"+data['response']['companies'][i]['id']+"]").addClass("favorited-company");
            }
          };
        }
      },
    dataType: 'json',
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
        $("#company_banner_img").attr("src",data['banner_image']);
        $("#company_logo").attr("src",data["logo"]);
        $("#company_size").text(data['number_employees']);
        $("#company_founded").text(data['founded']);
        $("#company_website").html("<a href='"+data['website']+"' target='_blank'>"+data['name']+"</a>");
        $("#company_careers_website").html("<a class='btn btn-primary' href='"+data['careers_website']+"' target='_blank'>Visit Careers Site</a>");
        $("#company_id").val(id);
        // need to check if need to display favorite or unfavorite icon
        if(data['favorites'].indexOf(parseInt(user_id)) >= 0){
          $("#favorite_company_btn").html('<span class="glyphicon glyphicon-minus"></span>&nbsp;Unfav');
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

function updateHunts(){
  user_id = $("#user_id").val();
  console.log(user_id);
  $.ajax({
    url: '/api/v1/hunting/',
    type: 'GET',
    contentType: 'application/json',
    processData: false,
    success: function(data, textStatus, jqXHR) {
        $("#hunting_number").text(data['meta']['total_count']);
        if(user_id){
          for (var i = data['response']['favorites'].length - 1; i >= 0; i--) {
            if(data['response']['favorites'][i]['user']['id'] == parseInt(user_id)){
              $("#hunting_button").attr("disabled","disabled");
              $("#hunting_button").text("Hunted!");
            }
          };
        }
      },
    dataType: 'json',
  });
}

function registerHunt(){
  user_id = $("#user_id").val();
  console.log(user_id);
  $.ajax({ 
    url:'/api/v1/hunting/', 
    type:'POST',
    dataType: 'json',
    data: JSON.stringify({
      'fair': '1', 
      'user': user_id,
    }), 
    contentType: 'application/json',
    statusCode : {
      201: function(data, textStatus, jsXHR){
        console.log("Successfully hunted at fair!");
        updateHunts();
      }
    }
  });
}

function toggleTable(cssID){
  console.log(cssID);
  if(cssID == '.favorited-company'){
    console.log($(cssID).css('background-image'));
    if($(cssID).css('background-image') == "none"){
      $(cssID).css('background-image', "url('/static/images/target.png')");
    } else {
      $(cssID).css('background-image','none');
    }
  } else {
    if($(cssID).css('background-color') == "rgb(255, 255, 255)") {
      if(cssID == '.btn-categorydisabled'){
        recolorTables(cssID,'#999');
      }
      if(cssID == '.btn-engineering'){
        recolorTables(cssID,'#baf198');
      }
      if(cssID == '.btn-finance'){
        recolorTables(cssID,'#ffb8e7');
      }
      if(cssID == '.btn-government'){
        recolorTables(cssID,'#347aef');
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
}

function decolorTables(cssID){
  $(cssID).css('background-color','white');
}

function recolorTables(cssID, color){
  $(cssID).css('background-color',color);
}

function get_favorites(){
  user_id = $("#user_id").val();
  console.log(user_id);
  $.ajax({ 
    url:'/api/v1/favorites/', 
    type:'GET',
    dataType: 'json',
    data: JSON.stringify({
      'user_id': user_id
    }), 
    contentType: 'application/json',
    processData: false,
    success: function(data, textStatus, jqXHR) {
        $("#hunting_number").text(data['meta']['total_count']);
        if(user_id){
          for (var i = data['response']['favorites'].length - 1; i >= 0; i--) {
            if(data['response']['favorites'][i]['user']['id'] == parseInt(user_id)){
              
            }
          };
        }
      },
  });
}
