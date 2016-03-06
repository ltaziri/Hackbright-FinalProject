
"use strict";

$(document).ready(function(){

// changing value of comment image button to the file selected so there is an indication to the user
  $('#comment_image').on('change', function() {
        var commentFile = $('#comment_image').val();
        if (commentFile.length > 1) {
          var commentFileName = commentFile.split('\\').pop();
          $(this).prev('label.upload_label').html('selected file:' + commentFileName);
        } else {
          $(this).prev('label.upload_label').html('<span class="glyphicon glyphicon-camera" aria-hidden="true"></span> Include a picture</label>');
        } 
  })
 
// for linkify to work in ajax call
var linkOptions = {
      defaultProtocol: 'http',
      events: null,
      format: function (value, type) {
        return value;
      },
      formatHref: function (href, type) {
        return href;
      },
      linkAttributes: null,
      linkClass: null,
      nl2br: false,
      tagName: 'a',
      target: function (href, type) {
        return type === 'url' ? '_blank' : null;
      }
    };
}) 
// Comment AJAX call //
$("#comment_form").submit(function(event){
  
  event.preventDefault();

    var formData = new FormData($('form#comment_form')[0]);
    
    $.ajax({
      url: '/comment_add.json',
      type: 'POST',
      data: formData,
      async: false,
      cache: false,
      contentType: false,
      processData: false,
      success: showComment,
      });
    
  });
 
// success function after ajax results returned from server 
    function showComment(results) {
    var htmlStr = "";
    htmlStr += "<div class='section_divider'>"
    htmlStr += "<img src='/" + results.comment_user_photo + "' width='50'>";
    htmlStr += "<b>"+ results.comment_user_name + "</b><br>"
    htmlStr += "<i>" + results.comment_timestamp + "</i><br>"
    htmlStr += results.comment_text 
    if(results.comment_image) {
      htmlStr += "<img src='/" + results.comment_image + "' width='300'><br>";
    }
    if (results.youtube_id){
      htmlStr +='<br><div class="embed-responsive embed-responsive-16by9"><iframe width="300" height="300" src="http://www.youtube.com/embed/' + results.youtube_id + '?autoplay=0"></iframe><br></div>';
    }
    htmlStr += "</div>"

    $("#new_comment").prepend(htmlStr);
    $("#new_comment").linkify(linkOptions);
    $("#comment_text").val('');
    $("#comment_image").val('');
    $('label.upload_label').html('<span class="glyphicon glyphicon-camera" aria-hidden="true"></span> Include a picture</label>');
}

// show group users info on click
  function showUserInfo(evt) {
      $(this).prev('div.pop-up').css('z-index', 2);
      $(this).prev('div.pop-up').siblings('div').css('z-index', 1);
      $(this).prev('div.pop-up').show();
  }

  function hideUserInfo(evt) {
        $('div.pop-up').hide();
  }

  $('.show_user').click(showUserInfo);
  $('.pop-up').click(hideUserInfo);
    
