from smtplib import SMTP
from email.message import EmailMessage
from config import settings

def recuperarContrasenia(email,link):
    msg = EmailMessage()


    msg.set_content('RESTABLECIMIENTO DE CONTRASEÑA:  {}'.format(link))
    msg['Subject'] = 'confirmacion de cambio de usuario'
    msg['From'] = "yeinerangulo2020@itp.edu.co"
    msg['To'] = email

    username =settings.MAIL_USERNAME
    password =settings.MAIL_PASSWORD

    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)

    server.quit()