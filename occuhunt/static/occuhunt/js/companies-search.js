function randomizeString(){
    var myStrings = new Array();
    myStrings[0] = "Try \x22San Francisco\x22";
    myStrings[1] = "Try \x22San Mateo\x22";
    myStrings[2] = "Try \x22Apple\x22";
    myStrings[3] = "Try \x22Google\x22";
    myStrings[4] = "Try \x22Facebook\x22";
    myStrings[5] = "Try \x22social network\x22";
    myStrings[6] = "Try \x22education\x22";
    var randomnumber=Math.floor(Math.random()*7)
    $("#inputCompanySearch").attr("placeholder", myStrings[randomnumber]);
  }
  function get_companies(count){
    user_id = $("#user_id").val();
    $("#loading_state").html('<div id="loadingProgressG"><div id="loadingProgressG_1" class="loadingProgressG"></div></div>');
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
    search_query = $("#inputCompanySearch").val();
    $("#loading_state").html('<div id="loadingProgressG"><div id="loadingProgressG_1" class="loadingProgressG"></div></div>');
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