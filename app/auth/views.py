# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 23:52:35 2023

@author: user
"""
from .forms import register_form, login_form, Password_update_Form, Email_update_Form, Password_reset_form, Password_token_form
from flask import render_template, redirect, url_for, flash, request, current_app
from . import auth
from .models import Users_db
from app import db
from app.Email_script import send_mail
from flask_login import login_user, current_user, login_required, logout_user
import jwt
from datetime import datetime


@auth.route('/register', methods=['GET','POST' ])
def register():
    form=register_form()
    if form.validate_on_submit():
        user=Users_db(name=form.name.data, 
                      email=form.email.data, 
                      username=form.username.data, 
                      sex=form.sex.data, 
                      password=form.password.data )
        flash('A verification email has been sent to you, please verify your account')
        token=user.email_token()
        db.session.add(user)
        db.session.commit()
        send_mail(form.email.data, 'Confirm Your Account', 'email/confirm_account', token=token)
        return redirect(url_for('auth.login', form=form))
    return render_template('auth/register.html', form=form)

@auth.route('/generate_token', methods=['GET'])
@login_required
def generate_token():
    token=current_user.email_token()
    send_mail(current_user.email, 'Confirm Your Account', 'email/confirm_account', token=token)
    flash('Please check your mail for the confirmation email', category='infor')
    return redirect(url_for('login'))


@auth.route('/confirm_user/<token>')
@login_required
def confirm_user(token):
    if current_user.confirmed:
        flash('Your account has been confirmed')
        return redirect(url_for('main.home'))
    if current_user.confirm_email_token(token):
        flash('Account confirmed. Thanks!')
        return redirect('main.home')
    else:
        flash('The confirmation Link is invalid or has expired. Try again.', category='info')
        return render_template('auth/new_token.html')
'''
@auth.before_app_request 
def before_request():
    if (current_user.is_authenticated 
        and not current_user.confirmed 
        and request.endpoint[:5]!='auth.':
        return redirect(url_for('auth.unconfirmed'))
    
@auth.route('/unconfirmed', methods=['GET'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return render_template('index.html')
    return render_template('auth/new_token.html')
'''

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form=login_form()
    if form.validate_on_submit():
        user=Users_db.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect Login Information! Try again', category='warning')
        return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    user=Users_db.query.filter_by(email=current_user.email).first()
    logout_user()
    flash('You have been logged Out')
    return redirect(url_for('main.home'))

@auth.route('/update_password', methods=['GET', 'POST'])
@login_required 
def update_password():
    form=Password_update_Form()
    if form.validate_on_submit():
        user=current_user.password(password=form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your Password has been updated sucessfully! Login with your new password.', category='info')
        return redirect(url_for('auth.login'))
    return render_template('auth/update_password.html', form=form)

@auth.route('/password_reset_token', methods=['GET', 'POST'])
def password_token():
    form=Password_token_form()
    if form.validate_on_submit() and Users_db.query.filter_by(email=form.email.data).first() !=None:
        token=jwt.encode({'Email':form.email.data,
                               'exp':int(datetime.now().timestamp()+3600)},
                              current_app.config['SECRET_KEY'], algorithm='HS256')
        send_mail(form.email.data, 'Change your Password', 'email/change_password', token=token)
        flash('A password reset token has been sent to your email')
        return redirect(url_for('auth.login'))
    else:
        flash('Email does not exist in our database. Please enter a valid email or register an account')
        return render_template('auth/request_password_token.html', form=form)
    return render_template('auth/request_password_token.html', form=form)
         
@auth.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    form=Password_reset_form()
    data=jwt.decode(token,
                    current_app.config['SECRET_KEY'], 
                    algorithms='HS256')
    email=data['Email']
    user=Users_db.query.filter_by(email=email).first()
    if form.validate_on_submit() and user!=None:
        user.password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated! Please log in with your new password')
        return redirect(url_for('auth.login')) 
    return render_template('auth/change_password.html', form=form) 

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form=Email_update_Form()
    if form.validate_on_submit():
        token=User_db.change_email_token(form.email.data)
        send_mail(form.new_email.data, 'Change your Email', 'email/change_email', token=token)
        flash('Check your new email for verification token')
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for('main.login'))
    return render_template('auth/change_email.html', form=form)
        
@auth.route('/email_change_token/<token>', methods=['GET', 'POST'])
@login_required
def change_email_token(token):
    if current_user.confirm_change_email_token(token) !=False:
        db.session.commit()
        flash('Your email has been updated. Login with your new  email')
        return redirect(url_for('auth.login'))
    else:
        flash('Your web token has expired, Try again.')
        return redirect(url_for('auth.change_email'))