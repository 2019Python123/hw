# from application import email
# from flask_mail import Message
# from flask import session
# from threading import Thread
# from random import randint
#
#
# def send_async_email(app_, msg):
#     with app_.app_context():
#
#
#
# def send_email(sender,app):
#     from application import app_factory
#     msg = Message('绑定邮箱认证',sender=app_factory.config['MAIL_USERNAME'],recipients=[sender,])
#     yzm = randint(1000,9999)
#     session['yzm'] = str(yzm)
#     msg.body = '您的验证码是: <h3>'+str(yzm)+'</h3>'
#     thread = Thread(target=send_async_email, args=[app, msg,])
#     thread.start()
#
