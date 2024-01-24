# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:17:14 2023

@author: user
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField, StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, Regexp
from flask_ckeditor import CKEditorField




class contactform(FlaskForm):
    name=StringField('Your Name', validators=[DataRequired()])
    email=EmailField('Your Email', validators=[DataRequired(),Length(0, 64)])
    subject=StringField('Subject', validators=[DataRequired()])
    message=TextAreaField('Message', validators=[DataRequired()])
    submit=SubmitField('Send Message')
    
class CommentForm(FlaskForm):
    comment=TextAreaField('Comment', validators=[DataRequired()])
    submit=SubmitField('Post Comment')
    
class SearchForm(FlaskForm):
    search=StringField('Search',  validators=[DataRequired()])
    submit=SubmitField('Submit')
    
class ImageForm(FlaskForm):
    featured_image=FileField('Featured Image')
    submit=SubmitField('Uplaod Image')
    
class Upload_Post(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    post=CKEditorField('Body')
    category=SelectField('Category', choices=[('Business', 'Business'), 
                                              ('Culture', 'Culture'), 
                                              ('Sport','Sport'), 
                                              ('Food', 'Food'), 
                                              ('Politics','Politics'),
                                              ('Celebrity','Celebrity'),
                                              ('Startup','Startup'),
                                              ('Travel','Travel')
                                              ], default='Uncategorized')
    featured_image=FileField('Featured Image', validators=[ 
                                                           FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 
                                                                                       'Only image files are allowed!')])
    submit=SubmitField('Upload')
    
class Edit_post_form(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    post=CKEditorField('Body')
    category=SelectField('Category', choices=[('Business', 'Business'), 
                                              ('Culture', 'Culture'), 
                                              ('Sport','Sport'), 
                                              ('Food', 'Food'), 
                                              ('Politics','Politics'),
                                              ('Celebrity','Celebrity'),
                                              ('Startup','Startup'),
                                              ('Travel','Travel')
                                              ], default='Uncategorized')
    submit=SubmitField('Update')
    