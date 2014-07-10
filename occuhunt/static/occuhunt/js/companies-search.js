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
  favorite_url = '/api/v2/applications/';
  console.log(favorite_url);
  $.ajax({ 
    url: favorite_url, 
    type:'POST',
    dataType: 'json',
    data: JSON.stringify({
        'company_id': companyId,
        'added_by_user':true
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
