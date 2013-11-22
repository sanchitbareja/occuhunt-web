// 
// 
// Commenting and adding resumes
// 
// 


function add_new_comment(e) {
    if(e.which == 13) {
        console.log(e);
        console.log($(e.currentTarget).parent());
        // make ajax request to post comment on the resume
        var resume_id = $(e.data).find("#resume_id").val();
        var comment_x = $(e.currentTarget).parent().find("#comment_x").val();
        var comment_y = $(e.currentTarget).parent().find("#comment_y").val();
        var comment_text = $(e.currentTarget).val();
        var user_id = $("#user_id").val();
        $.ajax({
            url: '/api/v1/comments/',
            type: 'POST',
            data: JSON.stringify({
              'user': user_id,
              'resume': resume_id,
              'comment': comment_text,
              'x': comment_x,
              'y': comment_y
            }), 
            dataType: 'json',
            contentType: 'application/json',
            statusCode : {
                201: function(data, textStatus, jsXHR){
                    console.log(data);
                    console.log(textStatus);
                    console.log(jsXHR);
                    console.log(data["user"]);
                    console.log(data["user"]["resume_points"]);
                    get_bounty();
                    $(e.currentTarget).parent().replaceWith('<div class="comment-box" style="position:absolute; top:'+comment_y+'px; "><p>'+comment_text+'</p></div>');
                },
                500: function(data, textStatus, jsXHR){
                    console.log(data);
                    console.log(textStatus);
                    console.log(jsXHR);
                }
            }
        });
    }
}

function add_new_resume_html(resume_id,url,comments){
    // add image element
    var comment_boxes = '';
    var comment_circles = '';
    if (comments) {

        for (var i = comments.length - 1; i >= 0; i--) {
            // id = comment-{comment-id}
            var comment_box = '<div class="comment-box" id="comment-'+comments[i]['id']+'" style="position:absolute; top:'+comments[i]['y']+'px; "><p>'+comments[i]['comment']+'</p></div>';
            comment_boxes = comment_boxes + comment_box;
            comment_circles = comment_circles + "<a onclick='toggle_comment(event, "+comments[i]['id']+");' id='comment-circle-"+comments[i]['id']+"' class='circle' style='position: absolute;z-index: 10; top:"+comments[i]['y']+"px; left:"+comments[i]['x']+"px;'></a>";
        };
    };
    $("#resume-feed").prepend(
    '<div class="row">'+
      '<div class="col-lg-1 col-sm-1"></div>'+
      '<div class="col-lg-8 col-sm-8">'+
        '<div class="row resume-container">'+
          '<img class="resume-image" src="'+url+'" />'+
          '<input type="hidden" id="resume_id" value="'+resume_id+'" >'+
          comment_circles + 
        '</div>'+
        '<hr />'+
      '</div>'+
      '<div class="col-lg-3 col-sm-3">'+
        '<div class="row comments-container">'+
                comment_boxes+
            '</div>'+
        '</div>'+
      '</div>'+
    '</div>');
    bind_events();
}

function bind_events(){
    $(".resume-container").on("click", function(e) {
        // calculate where to add circle
        var offset_t = $(this).offset().top - $(window).scrollTop();
        var offset_l = $(this).offset().left - $(window).scrollLeft();
        var left = e.clientX - offset_l - 10;
        var top = e.clientY - offset_t - 10;
        var box_position = top - 12;

        // create comment box
        var comments_div = $(this).parent().parent().find(".comments-container");
        var comment_input = $.parseHTML('<input type="text" class="form-control comment-input" placeholder="Add a comment..">');
        var comment_x = $.parseHTML('<input type="hidden" id="comment_x" value="'+left+'">');
        var comment_y = $.parseHTML('<input type="hidden" id="comment_y" value="'+top+'">');
        var comment_box = $.parseHTML('<div class="comment-box" style="position:absolute; top:'+box_position+'px;"></div>');
        
        // add circle
        var circle = $.parseHTML("<a class='circle' style='position: absolute;z-index: 10; top:"+top+"px; left:"+left+"px;'></a>");
        $(this).append(circle);
  
        $(comment_input).keypress(this, add_new_comment);
        $(comment_input).keyup(function(e) {
            if (e.keyCode == 27) { 
                $(comment_input).focusout();
            }
        });
        
        $(comment_box).append(comment_input);
        $(comment_box).append(comment_x);
        $(comment_box).append(comment_y);
        $(comments_div).append(comment_box);
        
        $(comment_input).focus();
        $(comment_input).focusout(function() {
            if ($(this).val() == '') {
                $(comment_box).remove();
                $(circle).remove();
            }
            else {
                $(this).blur();
            }
        });

   });

}

function toggle_all_comments(){
    $("#toggle-comments").on("click", function(e){
        $(".comments-container").toggle();
        $(".circle").toggle();
        $("#toggle-comments").toggleClass("toggleCommentsButton");

        // the next 2 lines will toggle the Hide Comments button.
        $("#toggle-comments").text("Hide Comments");
        $(".toggleCommentsButton").text("Show Comments");
    })
}

function toggle_comment(event, comment_id){
    console.log("toggle_comment fired");
    console.log(event);
    event.cancelBubble = true;
    $("#comment-"+comment_id).toggle();
    $("#comment-circle-"+comment_id).toggleClass("toggleCircle");
}

// 
// Update statistics
// 

function get_bounty(){
    console.log("getting boutny");  
    
    $.ajax({
        url: '/api/v1/users/'+$("#user_id").val()+'/',
        data: {},
        dataType: 'json',
        success: function(data, textStatus, jqXHR){
            console.log(data);

            $("#resume-menu-bounty").contents()[0].nodeValue = 'Bounty: ' + data["resume_points"];
            bounty_points = data['resume_points'];
        },
    });
};  
