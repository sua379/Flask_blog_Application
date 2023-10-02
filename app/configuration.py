# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 21:14:32 2023

@author: user
"""

import os



class config():
    SECRET_KEY=os.getenv('SECRET_KEY') or 'A VERY VERY UNSECRET KEY'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_MAIL_SUBJECT_PREFIX = 'Pharm Africa'
    FLASKY_MAIL_SENDER='Pharm Africa Support <suatech3@gmail.com'
    ADMIN_EMAIL='suatech3@gmail.com'
    UPLOAD_FOLDER='C:/Users/user/spyder files/Pharmacy project/app/static/img'
    CKEDITOR_FILE_UPLOADER='main.image_upload'
    include_schemas=True
    
    def init_app(app):
        pass
    
class development(config):
    SQLALCHEMY_DATABASE_URI='mysql://root:{0}@localhost/pharmafrica'.format(os.getenv('Password'))
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True 
    MAIL_PASSWORD=os.getenv('Mail_Password')
    MAIL_USERNAME='suatech3@gmail.com'
    
class production(config):
    SQLALCHEMY_DATABASE_URI='mysql://root:{0}@localhost/prod_pharm_africa'.format(os.getenv('Password'))
    
class testing(config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='mysql://root:{0}@localhost/prod_pharm_africa'.format(os.getenv('Password'))
    

configuration_dict={'development':development,
                    'production':production,
                    'testing':testing,
                    'default':development}



    
    
    
    
    
    
'''
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:{0}@localhost/pharmafrica'.format(os.getenv('Password'))
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SECRET_KEY']='A VERY VERY UNSECRET KEY'
app.config['FLASKY_MAIL_SENDER']='Pharm AFrica Support <suatech3@gmail.com>'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True 
app.config['MAIL_USERNAME']='suatech3@gmail.com'
app.config['MAIL_PASSWORD']='jrusdydiyefybphn
'''