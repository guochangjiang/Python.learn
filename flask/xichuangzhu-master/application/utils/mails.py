# coding: utf-8
import hashlib
from flask import render_template, url_for, current_app
from flask_mail import Message, Mail

mail = Mail()


def signup_mail(user):
    """Send signup email"""
    config = current_app.config
    token = hashlib.sha1(user.name).hexdigest()
    url = config.get('SITE_DOMAIN') + url_for('.activate', user_id=user.id, token=token)
    msg = Message("欢迎来到西窗烛", recipients=[user.email])
    msg.html = render_template('email/signup.html', url=url)
    mail.send(msg)