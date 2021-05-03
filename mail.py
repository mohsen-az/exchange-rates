import smtplib
from email.message import EmailMessage

from mail_config import sender, receiver, smtp


def send_smtp_mail(subject, body):
    message = EmailMessage()

    message['from'] = sender['email']
    message['to'] = receiver['email']
    message['subject'] = subject

    html_message = body

    message.set_content(html_message, 'html')

    try:
        with smtplib.SMTP(smtp['server'], smtp['port']) as server:
            server.ehlo()
            server.starttls()
            server.login(sender['email'], sender['password'])

            server.send_message(message)
        print('Successfully send the mail')
    except Exception:
        print('Failed to send mail')
