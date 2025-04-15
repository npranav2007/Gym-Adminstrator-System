import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_sms(user_email, message):

    sender_email = "ajaydorale270600@gmail.com"
    sender_password = "elpg owzo dpmy rcco"
    receiver_email = user_email

    msg = MIMEMultipart()
    msg['From'] = 'Gym management system'
    msg['To'] = receiver_email
    msg['Subject'] = "Mail for your gym account"

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")