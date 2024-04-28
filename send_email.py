import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_mail(email, fullname, username):
    # SMTP configuration
    smtp_host = 'smtp.hostinger.com'
    smtp_port = 587
    smtp_username = os.getenv('SMTP_USERNAME')  # Retrieve SMTP username from environment variable
    smtp_password = os.getenv('SMTP_PASSWORD')  # Retrieve SMTP password from environment variable


    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = "We have a website for you!"
    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" lang="en">
    <head>
      <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    </head>
    <body>
      Here is your mail
    </body>
    </html>
    """.format(fullname, fullname)
    msg.attach(MIMEText(html, 'html'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Use TLS encryption
        # Login to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(smtp_username, email, msg.as_string())
        # Close the connection
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Example usage
if __name__ == "__main__":
    email = 'kushwaha@codestam.com'  # Recipient's email address
    fullname = 'Recipient Full Name'  # Recipient's full name
    username = 'Recipient Username'  # Recipient's username
    send_mail(email, fullname, username)
