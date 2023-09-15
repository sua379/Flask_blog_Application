# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 23:53:06 2023

@author: user
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import UserMixin
import jwt
#from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from flask import current_app
from datetime import datetime



class Users_db(db.Model, UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(128), nullable=False)
    email=db.Column(db.String(64), nullable=False)
    username=db.Column(db.String(64), nullable=False)
    password_hash=db.Column(db.String(500), nullable=False)
    sex=db.Column(db.String(20), nullable=False)
    blog_posts=db.relationship('blog_db', backref='author', lazy=True)
    comments=db.relationship('comments_db', backref='author', lazy=True)
    replies=db.relationship('replies_db', backref='author', lazy=True)
    confirmed=db.Column(db.Boolean, default=False)
    
          
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def email_token(self):
        token=jwt.encode({'id':self.id, 'exp':int(datetime.now().timestamp()+3600)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token 
    
   
    def confirm_email_token(self, token):
        try:
            data=jwt.decode(token, 
                            current_app.config['SECRET_KEY'],
                            algorithm='HS256')
        except:
            return False
        if data['id']!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True
    
    def change_email_token(self, new_email):
        token=jwt.encode({'id':self.id, 'new_email':new_email, 'exp':int(datetime.now().timestamp()+3600)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        self.confirmed=False
        return token 
    
    def confirm_change_email_token(self, token):
        try:
            data=jwt.decode(token, 
                            current_app.config['SECRET_KEY'],
                            algorithm='HS256')
        except:
            return False
        if data['id']!=self.id:
            return False
        self.confirmed=True
        self.email=data['new_email']
        db.session.add(self)
        return True
    @staticmethod 
    def generate_fake(count=100):
        import forgery_py
        from random import seed
        from sqlalchemy.exc import IntegrityError
        import random
        
        seed() 
        
        for i in range(count): 
            num=random.randint(0,1)
            if num==1:
                gender='Male'
            else:
                gender='Female'
            u=Users_db(name=forgery_py.name.full_name(), 
                       email=forgery_py.internet.email_address(),
                       username=forgery_py.internet.user_name(True),
                       sex=gender,
                       confirmed=True, 
                       password=forgery_py.lorem_ipsum.word()
                       )
            db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        
        
        
        

    def __repr__(self):
        return 'contact %r' %self.name 
    
@login_manager.user_loader
def load_user(id):
    return Users_db.query.get(id)
    
    