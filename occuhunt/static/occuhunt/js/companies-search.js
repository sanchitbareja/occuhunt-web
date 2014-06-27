function randomizeString(){
    var myStrings = new Array();
    myStrings[0] = "Search \x22San Francisco\x22";
    myStrings[1] = "Search \x22San Mateo\x22";
    myStrings[2] = "Search \x22Apple\x22";
    myStrings[3] = "Search \x22Google\x22";
    myStrings[4] = "Search \x22Facebook\x22";
    myStrings[5] = "Search \x22social network\x22";
    myStrings[6] = "Search \x22education\x22";
    var randomnumber=Math.floor(Math.random()*7)
    $("#inputCompanySearch").attr("placeholder", myStrings[randomnumber]);
}

function considerCompanyWithId(companyId){
  favorite_url = '/api/v2/application_status/';
  console.log(favorite_url);
  $.ajax({ 
    url: favorite_url, 
    type:'POST',
    dataType: 'json',
    headers: {
        "Authorization": 'OAuth 6f9dd960cb005f85b5ba81c158829fe11c3541d9'
    },
    data: JSON.stringify({
        'company_id': companyId,
    }),
    contentType: 'application/json',
    statusCode : {
      201: function(data, textStatus, jsXHR){
        updateUIWithConfirmation(true);
      },
      400: function(data, textStatus, jsXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jsXHR);
        updateUIWithConfirmation(false);
      }
    }
  });
}

function updateUIWithConfirmation(success){
  if(success){
    $("#messages").append('<div class="alert alert-success alert-dismissible" role="alert">'+
      '<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'+
      '<strong>Added it to list!</strong> Do check your dashboard to manage your companies'+
    '</div>');
  } else {
    $("#messages").append('<div class="alert alert-warning alert-dismissible" role="alert">'+
      '<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'+
      '<strong>Oops!</strong> Please try again. Something went wrong in the process :('+
    '</div>');
  }
}

function get_companies(count){
  user_id = $("#user_id").val();
  // loading state ui
  $("#loading_state").html('<div id="loadingProgressG"><div id="loadingProgressG_1" class="loadingProgressG"></div></div>');

  // make ajax call
  $.ajax({
    url: '/api/v1/companies/',
    data: { limit: count },
    success: function(data, textStatus, jqXHR) {
        // console.log(data);
        // console.log(textStatus);
        // console.log(jqXHR);
        $("#loading_state").empty();
        document.getElementById('inputCompanySearch').onkeypress = function(e) {
          var event = e || window.event;
          var charCode = event.which || event.keyCode;

          if ( charCode == '13' ) {
            // Enter pressed
            searchCompanies();
          }
        }
        for(i in data['response']['companies']){
          if(data['response']['companies'][i]['favorites'].indexOf(parseInt(user_id)) > -1){
            $("#companies_list").append('<div class="col-lg-3 no-margin" id="company_info">'+
                                          '<div class="thumbnail" id="company_thumbnail">'+
                                            '<a id="company_thumbnail_logo" href="/company/'+data['response']['companies'][i]['id']+'/"><img id="company_thumbnail_logo" src="'+data['response']['companies'][i]['logo']+'"></a>'+
                                          '</div>'+
                                          '<div id="company_thumbnail_favorite">'+
                                            '<a class="btn-link" onclick="unfavoriteCompanyWithId('+data['response']['companies'][i]['id']+',this,update_favorites);"><span class="glyphicon glyphicon-plus"></span></a>'+
                                          '</div>'+
                                        '</div>');
          } else {
            $("#companies_list").append('<div class="col-lg-3 no-margin" id="company_info">'+
                                          '<div class="thumbnail" id="company_thumbnail">'+
                                            '<a id="company_thumbnail_logo" href="/company/'+data['response']['companies'][i]['id']+'/"><img id="company_thumbnail_logo" src="'+data['response']['companies'][i]['logo']+'"></a>'+
                                          '</div>'+
                                          '<div id="company_thumbnail_favorite">'+
                                            '<a class="btn-link" onclick="favoriteCompanyWithId('+data['response']['companies'][i]['id']+',this,update_favorites); "><span class="glyphicon glyphicon-plus"></span></a>'+
                                          '</div>'+
                                        '</div>');
          }
        }
      },
    dataType: 'json',
  });
}

function searchCompanies(){
  user_id = $("#user_id").val();
  // get search term
  search_query = $("#inputCompanySearch").val();
  // load UI state
  $("#loading_state").html('<div id="loadingProgressG"><div id="loadingProgressG_1" class="loadingProgressG"></div></div>');
  // make query
  $.ajax({
    url: '/api/v1/companies/search/',
    data: {
      'q': search_query
    }, 
    success: function(data, textStatus, jqXHR) {
        // console.log(data);
        // console.log(textStatus);
        // console.log(jqXHR);
        console.log("searching done");
        $("#companies_found").text(data['response']['companies'].length+" companies found");
        $("#companies_list").empty();
        $("#loading_state").empty();
        for(i in data['response']['companies']){
          if(data['response']['companies'][i]['favorites'].indexOf(parseInt(user_id)) > -1){
            $("#companies_list").append('<div class="col-lg-3 no-margin" id="company_info">'+
                                          '<div class="thumbnail" id="company_thumbnail">'+
                                            '<a id="company_thumbnail_logo" href="/company/'+data['response']['companies'][i]['id']+'/"><img id="company_thumbnail_logo" src="'+data['response']['companies'][i]['logo']+'"></a>'+
                                          '</div>'+
                                          '<div id="company_thumbnail_favorite">'+
                                            '<a class="btn-link" onclick="unfavoriteCompanyWithId('+data['response']['companies'][i]['id']+',this, update_favorites);"><span class="glyphicon glyphicon-minus"></span>Remove</a>'+
                                          '</div>'+
                                        '</div>');
          } else {
            $("#companies_list").append('<div class="col-lg-3 no-margin" id="company_info">'+
                                          '<div class="thumbnail" id="company_thumbnail">'+
                                            '<a id="company_thumbnail_logo" href="/company/'+data['response']['companies'][i]['id']+'/"><img id="company_thumbnail_logo" src="'+data['response']['companies'][i]['logo']+'"></a>'+
                                          '</div>'+
                                          '<div id="company_thumbnail_favorite">'+
                                            '<a class="btn-link" onclick="favoriteCompanyWithId('+data['response']['companies'][i]['id']+',this, update_favorites);"><span class="glyphicon glyphicon-plus"></span>Add to favorites</a>'+
                                          '</div>'+
                                        '</div>');
          }
        }
      },
    dataType: 'json',
  });
}