import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utilities import logger


def send_mail(subject="sample", body=None, attachments=None, fromaddr="ansible@limetray.com",
              toaddr="rtandon@limetray.com"):
    try:
        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = subject

        # string to store the body of the mail
        body_file = body

        # attach the body with the msg instance

        msg.attach(MIMEText(body_file, 'html'))

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, "Ansible@lime")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()
    except Exception as e:
        logger.exception(e, exc_info=True)
