# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 21:34:12 2023

@author: user
"""
from flask_mail import Message
from flask import render_template, current_app
from app import  mail



def send_mail(to, subject, template, **kwargs):
    msg=Message('Pharm Africa '+subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body=render_template(template+'.html', **kwargs)
    msg.html=render_template(template+'.txt', **kwargs)
    mail.send(msg)