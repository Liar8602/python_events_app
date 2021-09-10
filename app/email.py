from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "getdata@gmail.com"
app.config['MAIL_PASSWORD'] = 'kfajlfaj9'
app.config['MAIL_DEFAULT_SENDER'] = "getdata@gmail.com"


def sender(email, password):
    msg = Message('Upgrade password', sender="joker8602@mail.ru", recipients=[email])
    msg.body = f'Hello. If you are reading this, then the password recovery system is working properly. Your password {password}'
    mail.send(msg)
    return "Message sent!"
