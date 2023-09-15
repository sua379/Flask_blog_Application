# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:20:11 2023

@author: user
"""

from app import db
from datetime import datetime
from app.auth.models import Users_db


class contact_db(db.Model):
    __tablename__='user_message'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(128))
    email=db.Column(db.String(61))
    subject=db.Column(db.String(60))
    Message=db.Column(db.Text())
    
    def __repr__(self):
        return 'contact %r' %self.name 
    
class blog_db(db.Model):
    __tablename__='blog_posts'
    id=db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments=db.relationship('comments_db', backref='blog_post')
    post_title=db.Column(db.String(150), nullable=False)
    post_body=db.Column(db.Text(), nullable=False)
    post_intro=db.Column(db.Text())
    date=db.Column(db.DateTime, default=datetime.now)
    category=db.Column(db.String(50))
    featured_image=db.Column(db.String(200))
    
    
    @staticmethod
    def add_featured_image():
        import os
        import uuid
        import shutil
        count=blog_db.query.count()
        r'''

        directory = r'C:\Users\user\spyder files\pictures'

        files=[]

        for filename in os.listdir(directory):
            file_dir=os.path.join(directory, filename)
            if os.path.isfile(file_dir):
                files.append(file_dir)
     '''

        for i in range(1, count+1):
            post_object=blog_db.query.filter_by(id=i).first()
            new_path=post_object.featured_image
            post_object.featured_image=new_path.replace('\\', '/')
            

        db.session.commit()
        
    @staticmethod
    def adding_intro():
        count=blog_db.query.count()
        for i in range(1, count+1):
            post_object=blog_db.query.filter(blog_db.id==i).first()
            post=post_object.post_body
            post_intr=post.split('\n')[0]
            post_object.post_intro=post_intr
        db.session.commit()
        
    @staticmethod 
    def generate_fake(count=100):
        import forgery_py
        from random import seed
        from sqlalchemy.exc import IntegrityError
        import random
        
        seed() 
        category_id=['Business','Culture','Sport', 'Food', 'Politics', 'Celebrity','Startup', 'Travel']
        user_count=Users_db.query.count()
        for i in range(count): 
            
            u=Users_db.query.offset(random.randint(0, user_count - 1)).first()
            p=blog_db(post_title=forgery_py.lorem_ipsum.title(5), 
                       post_body=forgery_py.lorem_ipsum.paragraphs(quantity=4),
                       date=forgery_py.date.date(True),
                       category=random.choice(category_id),
                       author_id=u.id
                       )
            db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    
    def __repr__(self):
        return 'Post_id is %r' %self.author_id
    
class comments_db(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id=db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    date=db.Column(db.DateTime, default=datetime.now)
    comment=db.Column(db.Text())
    comment_replies=db.relationship('replies_db', backref='main_comment')
    
    @staticmethod 
    def generate_fake(count=100):
        import forgery_py
        from random import seed
        from sqlalchemy.exc import IntegrityError
        import random
        
        seed() 
    
        user_count=Users_db.query.count()
        blog_count=blog_db.query.count()
        for i in range(count): 
            u=Users_db.query.offset(random.randint(0, user_count-1)).first()
            b=blog_db.query.offset(random.randint(0, blog_count-1)).first()
            
            c=comments_db( 
                       comment=forgery_py.lorem_ipsum.words(5),
                       date=forgery_py.date.date(True),
                       author_id=u.id,
                       blog_id=b.id)
            db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    
class replies_db(db.Model):
    __tablename__='replies'
    id=db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id=db.Column(db.Integer, db.ForeignKey('comments.id'))
    date=db.Column(db.DateTime, default=datetime.now)
    reply=db.Column(db.Text())
    
    @staticmethod 
    def generate_fake(count=100):
        import forgery_py
        from random import seed
        from sqlalchemy.exc import IntegrityError
        import random
        
        seed() 
    
        user_count=Users_db.query.count()
        comment_count=comments_db.query.count()
        for i in range(count): 
            u=Users_db.query.offset(random.randint(0, user_count-1)).first()
            c=comments_db.query.offset(random.randint(0, comment_count-1)).first()
            
            r=replies_db( 
                       reply=forgery_py.lorem_ipsum.words(3),
                       date=forgery_py.date.date(True),
                       author_id=u.id,
                       comment_id=c.id)
            db.session.add(r)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    