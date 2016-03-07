
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
    htmlStr += "<div class='section_divider comments'>";
    htmlStr += "<div class='row'><div class='col-xs-2 col-lg-1'>";
    htmlStr += "<img src='/" + results.comment_user_photo + "' width='50px'></div>";
    htmlStr += "<div class='col-xs-10 col-lg-11'>";
    htmlStr += "<p><h4>"+ results.comment_user_name + "</h4><br>";
    htmlStr += "<i>" + results.comment_timestamp + "</i></p></div></div>";
    htmlStr += "<div class='well'><div class='comment_text'>" + results.comment_text + "</div>";
    if(results.comment_image) {
      htmlStr += "<br><div class='row'><div class='col-xs-12 col-sm-6 col-md-6 col-sm-offset-3 col-md-offset-3'>";
      htmlStr += "<img class='comment_image' src='/" + results.comment_image + "></div></div>";
    }
    if (results.youtube_id){
      htmlStr +="<br><div class='embed-responsive embed-responsive-16by9'>";
      htmlStr += "<iframe width='300' height='300' src='http://www.youtube.com/embed/"; 
      htmlStr += results.youtube_id + "?autoplay=0'></iframe><br></div>";
    }
    htmlStr += "</div></div>"

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
    
