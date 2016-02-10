import sendgrid

sg = sendgrid.SendGridClient('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')


def send_email():
    message = sendgrid.Mail()
    message.add_to('ltaziri@gmail.com')
    message.add_to_name('Leilani Taziri')

    message.set_subject('Test')
    message.set_html("<h1>this is an html test</h1>")
    message.set_text('this is a plain text test')
    message.set_from('Ltaziri <ltaziri@gmail.com>')
    status, msg = sg.send(message)

    print status, msg


send_email()