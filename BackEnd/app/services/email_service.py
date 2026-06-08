import code

from flask_mail import Message
from extensions import mail

def send_email(email, codigo):

    msg = Message(
        'Código de Ativação - KR Tech Store',
        sender='krtechstorebr@gmail.com',
        recipients=[email]
        )
    
    msg.body = f'Seu código de ativação é: {codigo}'

    mail.send(msg)


# teste
    '''def send_email(to, code):
        """Mostra o código no terminal para desenvolvimento"""
        print("\n" + "🔐" * 20)
        print(f"📧 SIMULANDO ENVIO DE EMAIL")
        print(f"   Para: {to}")
        print(f"   Código de recuperação: {code}")
        print(f"   Use este código para resetar a senha")
        print("🔐" * 20 + "\n")
        return True'''