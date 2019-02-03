from creds import PASSWORD, FROM, TO
import smtplib
import ssl


def send_mail(msg=None, to=TO[0]):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = FROM
    receiver_email = to
    password = PASSWORD
    if msg is not None:
        message = msg
    else:
        message = """\
        Subject: Hello There!

        This message is sent from Python."""

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
