from email.message import EmailMessage
import smtplib
import ssl

def main(areaRead):

    area = areaRead

    email_sender = "firesender2023@gmail.com"
    email_pass = "vgot jmho vkdc ivln"
    email_receiver = "augustotoledo23@gmail.com"

    subject = 'Alerta de Incêndio'

    if area == 1:
        body = 'Incêndio ocorrendo no vídeo 1!'
        
    elif area == 2:
        body = 'Incêndio ocorrendo no vídeo 2!'

    em_write = EmailMessage()

    em_write['From'] = email_sender
    em_write['To'] = email_receiver
    em_write['Subject'] = subject
    em_write.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em_write.as_string())