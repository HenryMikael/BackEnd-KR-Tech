from flask_mail import Message
from app.extensions import mail
def send_email(email, codigo):

    msg = Message(
        'Código de Ativação - KR Tech Store',
        sender='krtechstorebr@gmail.com',
        recipients=[email]
        )
    
    msg.body = f'Seu código de ativação é: {codigo}'

    mail.send(msg)