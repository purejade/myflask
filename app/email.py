# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from threading import Thread
from flask import render_template,current_app
from flask.ext.mail import Message
from . import mail
__author__ = 'purejade'

def send_sync_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    # mail.send(msg)
    thr = Thread(target=send_sync_email,args=[app,msg])
    thr.start()
    return thr