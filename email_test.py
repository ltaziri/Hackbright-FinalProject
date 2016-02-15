import sendgrid
import os
import sys


def send_email(invite_email, invite_name, user_name, group_name, invite_text, invite_id):

    api_key = os.environ['SEND_GRID_API']
    sg = sendgrid.SendGridClient(api_key)
    
    
    message = sendgrid.Mail()
    message.add_to(invite_email)
    message.set_subject("Come play with %s" % (user_name))
    message.set_text("Hello %s,\n\n %s has invited you to join the %s group.\n\nJoin the group!" %(invite_name, user_name, group_name))
    message.set_html("""<h2>Hello %s</h2> 
                        <p>%s has sent you the following invite for the %s group.\n</p> 
                        <p>%s</p>
                        
                        <a href=\"/%d\">Join the group!</a> """% (invite_name, 
                                                                  user_name, 
                                                                  group_name, 
                                                                  invite_text, 
                                                                  invite_id ))

    message.set_from("admin@virtcraft.com")
    

    status, msg = sg.send(message)

    print status, msg
    





