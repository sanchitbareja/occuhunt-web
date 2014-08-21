mixpanel.track_links("#mp-viewjobs", "Clicked on view jobs from modal in fair page", {'referrer': document.referrer });
$(document).ready(function(){
  getCompanies();
  $('*[data-poload]').on("click", function() {
    var e = $(this);
    mixpanel.track('Viewed company popup from Fair Page');
    $.ajax({
        url: '/api/v2/companies/'+e.data('poload')+'/',
        data: {},
        dataType: 'json',
        success: function(data, textStatus, jqXHR){
          console.log(data);
          e.unbind("click").popover({
            html:true,
            trigger: 'click',
            container: $(this).attr('id'),
            title:"<a class='btn-link pull-left' onclick='closeModal("+data['id']+")'><b>X</b></a><h3 class='text-center'>"+data["name"]+"</h3><a class='btn-link' id='modal-plus' onclick='favoriteCompanyWithId("+data['id']+",this, null);' style='right:17px; top:10px;position:absolute; float:right; '><span class='glyphicon glyphicon-plus'></span></a>",
            content:"<div class='popover-company-info'><img id='background_banner' src='"+data["banner_image"]+"'/><img id='foreground_banner' src='"+data['logo']+"'><p>"+data["company_description"].slice(0,140)+"...</p><a class='btn btn-done' id='mp-viewjobs' href='/company/"+data['id']+" /'>VIEW JOBS</a></div>"
          }).popover("show");
        },
    });
  });
});

function closeModal(id){
  $('[data-poload='+id+']').click();
}

$(window).bind('scroll resize', function() {
    $('#filter_bar').css('top', $(this).scrollTop());
});