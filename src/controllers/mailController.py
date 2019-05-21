from flask import render_template
from flask_mail import Message
from ..app import mail
import socket
import random
import string


def login_success(template, email, keys=None):
    message = "Nous vous remercions pour votre confiance," \
              "nous vous souhaitons un agreable moment en notre compagnie a bientot !"
    message_key = "votre clé de validation est de " + str(keys)
    msg = Message('Remerciement', sender='elhorm_j@etna-alternance.net', recipients=[email])
    if keys: msg.html = render_template(template, message=message, message_key=message_key)
    else: msg.html = render_template(template, message=message)
    try: mail.send(msg); return 1
    except socket.gaierror: return 0


def reset_password(template, keys, email):
    msg = Message('Changement de Mot de Passe', sender='elhorm_j@etna-alternance.net', recipients=[email])
    msg.html = render_template(template, keys=keys)
    try:
        mail.send(msg)
        return 1
    except socket.gaierror:
        return 0


def password_updated(template, email):
    message = "Votre mot de passe a été changer avec succes. Nous vous souhaitons un agreable moment" \
              " en notre compagnie a bientot !"
    msg = Message('Changement de Mot de Passe', sender='elhorm_j@etna-alternance.net', recipients=[email])
    msg.html = render_template(template, message=message)
    try:
        mail.send(msg)
        return 1
    except socket.gaierror:
        return 0

def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))