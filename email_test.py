import sendgrid
import os
import sys


def send_email(invite_email, invite_name, user_name, group_name, invite_text):
    message_html="""
    <!doctype html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>MakeAlong - Come play!</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto+Slab" rel="stylesheet" type="text/css">
    <style>

    * {
      font-family: "Roboto Slab", sans-serif;
      font-size: 100%%;
      margin: 0;
      padding: 0;
    }
    img {
      max-width: 600px;
      width: auto;
    }
    body {
      -webkit-font-smoothing: antialiased;
      height: 100%%;
      -webkit-text-size-adjust: none;
      width: 100%% !important;
    }

    .last {
      margin-bottom: 0;
    }
    .first {
      margin-top: 0;
    }
    .padding {
      padding: 10px 0;
    }
    .btn-primary {
      Margin-bottom: 10px;
      width: auto !important;
    }
    .btn-primary td {
      background-color: #348eda; 
      border-radius: 25px;
      font-size: 14px; 
      text-align: center;
      vertical-align: top; 
    }
    .btn-primary td a {
      background-color: black;
      border: solid 1px black;
      border-radius: 25px;
      border-width: 10px 20px;
      display: inline-block;
      color: white;
      cursor: pointer;
      font-weight: bold;
      line-height: 2;
      text-decoration: none;
    }

    table.body-wrap {
      padding: 20px;
      width: 100%%;
    }
    table.body-wrap .container {
      border: 1px solid #f0f0f0;
    }

    table.footer-wrap {
      clear: both !important;
      width: 100%%;  
    }
    .footer-wrap .container p {
      color: #666666;
      font-size: 12px;
      
    }
    table.footer-wrap a {
      color: #999999;
    }

    h1, 
    h2 {
      color: #111111;
      font-weight: 200;
      line-height: 1.2em;
      margin: 40px 0 10px;
    }
    h1 {
      font-size: 36px;
    }
    h2 {
      font-size: 28px;
    }
    h3 {
      font-size: 18px;
      color: #111111;
      font-weight: 200;
      line-height: 1.2em;
      margin: 10px 0 10px;
    }
    p, 
    ul, 
    ol {
      font-size: 14px;
      font-weight: normal;
      margin-bottom: 10px;
    }
    ul li, 
    ol li {
      margin-left: 5px;
      list-style-position: inside;
    }
    .container {
      clear: both !important;
      display: block !important;
      Margin: 0 auto !important;
      max-width: 600px !important;
    }
    .body-wrap .container {
      padding: 20px;
    }
    .content {
      display: block;
      margin: 0 auto;
      max-width: 600px;
    }
    .content table {
      width: 100%%;
    }
    </style>
    </head>

    <body>

    <table class="body-wrap">
      <tr>
        <td></td>
        <td class="container">

          <div class="content" style="border: 1px solid black">
          <table>
            <tr>
              <td>
                <img src="http://uvmbored.com/wp-content/uploads/2016/01/KnittingBasket.jpg" width="80%%">
                <h1>Hi %s!</h1>
                <p>%s has sent you the following invite for %s:</p>
                <p><i>%s</i><br>
                <a href="test.com"><h3>Join now!</h3></a>
                </p>
               <p> Happy making!<br>
               Your friends at <b>MakeAlong</b></p>
              </td>
            </tr>
          </table>
          </div>
          
        </td>
        <td></td>
      </tr>
    </table>

    <table class="footer-wrap">
      <tr>
        <td></td>
        <td class="container">
          
          <div class="content">
            <table>
              <tr>
                <td align="center">
                  <p>Don"t like these emails? <a href="#"><unsubscribe>Unsubscribe</unsubscribe></a>.
                  </p>
                </td>
              </tr>
            </table>
          </div>
          
        </td>
        <td></td>
      </tr>
    </table>

    </body>
    </html>""" % (invite_name, user_name, group_name, invite_text)

    api_key = os.environ['SEND_GRID_API']
    sg = sendgrid.SendGridClient(api_key)
    
    
    message = sendgrid.Mail()
    message.add_to(invite_email)
    message.set_subject("Come play with %s" % (user_name))
    message.set_text("Hello %s,\n\n %s has invited you to join the %s group.\n\nJoin the group!" %(invite_name, user_name, group_name))
    message.set_html(message_html)

    message.set_from("admin@makealong.com")
    

    status, msg = sg.send(message)

    print status, msg
    





