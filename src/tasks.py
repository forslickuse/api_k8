import smtplib

from email.message import EmailMessage

# TODO: remove Albert and Han strings
async def send_email(email, first_name, last_name):
    with open('./email_template.txt') as fp:
        # Create a text/plain message
        msg = EmailMessage()
        msg.set_content(fp.read())

    msg['Subject'] = f'{first_name} {last_name}'
    msg['From'] = 'no-reply@reach.vote'
    msg['To'] = email

    s = smtplib.SMTP('localhost', 1025)
    s.send_message(msg)
    s.quit()
