
mixpanel.track_links("#nav", "Click nav link", {'referrer': document.referrer });

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
        $("#favorite_company_btn").html('<span class="glyphicon glyphicon-plus"></span>');
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
        if ($(element).attr('id') == 'modal-plus') {
          $(element).html('<span class="glyphicon glyphicon-minus"></span>');
        }
        else {
          $(element).html('<span class="icon-minus icon-2x"></span>');
        }
        console.log(element);
        $(element).attr('onclick', 'unfavoriteCompanyWithId('+company_id+',this,'+callback+');');
        if(typeof callback !== "undefined"){
          callback();
        }
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
        if ($(element).attr('id') == 'modal-plus') {
          $(element).html('<span class="glyphicon glyphicon-plus"></span>');
        }
        else {
          $(element).html('<span class="icon-plus icon-2x"></span>');
        }
        $(element).attr('onclick', 'favoriteCompanyWithId('+company_id+',this,'+callback+');');
        if(typeof callback !== "undefined"){
          callback();
        }
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
          $("#favorite_company_btn").html('<span class="glyphicon glyphicon-minus"></span>');
          $("#favorite_company_btn").attr('onclick', 'unfavoriteCompany();');
        } else {
          $("#favorite_company_btn").html('<span class="glyphicon glyphicon-plus"></span>');
          $("#favorite_company_btn").attr('onclick', 'favoriteCompany();');
        }
      },
    dataType: 'json',
  });
}

function toggleTable(cssID){
  console.log(cssID);
  if(cssID == '.favorited-company'){
    console.log($(cssID).css('background-image'));
    if($(cssID).css('background-image') == "none"){
      $(cssID).css('background-image', "url('/static/images/other/fold.png')");
      recolorTables('.btn-categorydisabled','#dcdcdc');
    } else {
      $(cssID).css('background-image','none');
      decolorTables('.btn-categorydisabled');
    }
  } else {
    if($(cssID).css('border-color') == "rgb(255, 255, 255)") {
      if(cssID == '.btn-categorydisabled'){
        recolorTables(cssID,'#dcdcdc');
      }
      if(cssID == '.btn-engineering'){
        recolorTables(cssID,'#96b6d6');
      }
      if(cssID == '.btn-finance'){
        recolorTables(cssID,'#edf36d');
      }
      if(cssID == '.btn-government'){
        recolorTables(cssID,'#f98fda');
      }
      if(cssID == '.btn-health'){
        recolorTables(cssID,'#ffafc2');
      }
      if(cssID == '.btn-technology'){
        recolorTables(cssID,'#ffa753');
      }
      if(cssID == '.btn-other'){
        recolorTables(cssID,'#88b9be');
      }
    } else {
      decolorTables(cssID);
    }
  }
}

function decolorTables(cssID){
  $(cssID).css('border-color','white');
}

function recolorTables(cssID, color){
  $(cssID).css('border-color',color);
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
