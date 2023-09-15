# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 23:28:09 2023

@author: user
"""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from .models import Users_db
from wtforms import ValidationError


class register_form(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    email=EmailField('Email', validators=[DataRequired(), Email()])
    username=StringField('Username', validators=[DataRequired(),Regexp('^[A-Za-z1-9._]*$',0,'username must '
                                                                'contain only letters, numbers,dots and underscore'), Length(3,20)])
    password=PasswordField('Password', validators=[DataRequired(), EqualTo('password2', 'Passwords must match'),Regexp('^[A-Za-z][A-Za-z1-9._]+$',0,'password must contain '
                                                                                                                       'only letters, numbers,dots and underscore'), Length(3,20)])
    password2=PasswordField('Confirm Password', validators=[DataRequired()])
    
    sex=RadioField('Sex', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    Submit=SubmitField('Submit')
    
    def validate_email(self, field):
        if Users_db.query.filter_by(email=field.data).first() !=None:
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if Users_db.query.filter_by(username=field.data).first() !=None:
            raise ValidationError('Username already in use by another member')
    
class login_form(FlaskForm):
    email=EmailField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Submit')
    
class Password_update_Form(FlaskForm):
    password=PasswordField('Old Password', validators=[DataRequired()])
    new_password=PasswordField('New Password', validators=[DataRequired(), 
                                                           EqualTo('confirm_password', 'passwords must match'),
                                                           Regexp('^[A-Za-z1-9._]*$',0,
                                                                  'Password must contain only letters, numbers, dots and underscore'), 
                                                           Length(3, 20)])
    confirm_password=PasswordField(' Confirm Password', validators=[DataRequired()])
    submit=SubmitField('Update Password')
    
class Email_update_Form(FlaskForm):
    email=EmailField('New Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Change Email')
    
    def validate_email(self, field):
        if Users_db.query.filter_by(email=field.data).first() !=None:
            raise ValidationError('Email already registered.')
    
    
class Password_reset_form(FlaskForm):
    new_password=PasswordField('New Password', validators=[DataRequired(), 
                                                           EqualTo('confirm_password', 'passwords must match'),
                                                           Regexp('^[A-Za-z1-9._]*$',0,
                                                                  'Password must contain only letters, numbers, dots and underscore'), 
                                                           Length(3, 20)])
    confirm_password=PasswordField(' Confirm Password', validators=[DataRequired()])
    submit=SubmitField('Change Email')
    
class Password_token_form(FlaskForm):
    email=EmailField('New Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Password Reset Token')
    

    
