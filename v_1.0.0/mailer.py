import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from credentials import config

def send_email(email_from, email_to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config.EMAIL_MAIN, config.MAILERPASS)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    server.quit()