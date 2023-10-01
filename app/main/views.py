# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:10:14 2023

@author: user
"""


from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_required
from datetime import datetime
from app.Email_script import send_mail
from . import main
from .forms import contactform, CommentForm, Upload_Post
from .models import contact_db, blog_db, comments_db
from app import db, ckeditor
import uuid
import os
import re 
from flask_ckeditor import upload_success, upload_fail 


@main.route('/')
def home():
    slide_posts=blog_db.query.filter(blog_db.id <5)
    category=['Business','Culture','Sport', 'Food', 'Politics', 'Celebrity','Startup', 'Travel']
    post_grid=[]
    blog=blog_db.query.order_by(blog_db.post_title)
    for x in category:
        blog_post=blog_db.query.filter_by(category=x).first()
        post_grid.append(blog_post)
    culture=blog_db.query.filter_by(category='Culture')
    business=blog_db.query.filter_by(category='Business')
    sport=blog_db.query.filter_by(category='Sport')
    
    return render_template('index.html', 
                           slide_posts=slide_posts,
                           post_grid=post_grid,
                           trending=blog,
                           culture=culture,
                           business=business,
                           sport=sport)
                           

@main.route('/single-post/<int:id>', methods=['GET', 'POST'])
def singlepost(id):
    post=blog_db.query.get_or_404(id)
    post_comments=post.comments
    comment=CommentForm()
    comment_count=len(post_comments)
    if comment.validate_on_submit():
        add_comment=comments_db(author_id=post.author.id,
                                blog_id=post.id,
                                comment=comment.comment.data
                                )
        db.session.add(add_comment)
        db.session.commit()
    popular=blog_db.query.order_by(blog_db.post_intro)
    trending=blog_db.query.order_by(blog_db.post_title)
    latest=blog_db.query.order_by(blog_db.date)
    
    return render_template('single-post.html',
                           post=post, 
                           form=comment,
                           comments=post_comments,
                           comment_count=comment_count,
                           popular=popular, 
                           trending=trending,
                           latest=latest)


@main.route('/categories/<cat>/', methods=['GET'])
def category(cat): 
    popular=blog_db.query.order_by(blog_db.post_intro)
    trending=blog_db.query.order_by(blog_db.post_title)
    latest=blog_db.query.order_by(blog_db.date)
    page=request.args.get('page', 1, int)
    paginate=blog_db.query.filter_by(category=cat).paginate(page=page, per_page=5, error_out=False)
    posts=paginate.items
    return render_template('category.html', 
                           popular=popular, 
                           trending=trending,
                           latest=latest,
                           posts=posts,
                           pagination=paginate)

@main.route('/search-results', methods=['GET', 'POST'])
def search_results():
    return render_template('search-result.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form=contactform()
    if form.validate_on_submit():
        inquiry=contact_db(name=form.name.data, 
                        email=form.email.data,
                        subject=form.subject.data,
                        Message=form.message.data)
        db.session.add(inquiry)
        db.session.commit()
        flash('Your message has been recieved sucessfully', category='info')
        send_mail(form.email.data, 'Inquiry Confirmation', 'email/contact_mail')
        return redirect(url_for('main.contact', success=True))
    '''else:
        flash('Something went wrong, Please check your form and try again', category='info')
        return render_template('contact.html', form=form)'''
    return render_template('contact.html', form=form)

@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/files/<path:filename>')
def uploaded_file(filename):
    path=current_app.config['UPLOAD_FOLDER']
    return send_from_directory(path, filename)

@main.route('/image_upload', methods=['POST'])
def image_upload():
    file=request.files.get('upload')
    extension=file.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'png', 'gif', 'jpeg']:
        return upload_fail(message='Upload Error, only image files allowed')
    random_sg=str(uuid.uuid1())+'_'+ file.filename
    random_string=random_sg.replace('\\','/')
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], random_string))
    url=url_for('main.uploaded_file', filename=random_string)
    return upload_success(url, filename=random_string)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def uplaod():
    form=Upload_Post()
    if form.validate_on_submit():
        intr=form.post.data.split('</p>')[0]
        pattern='<[^>]+>'
        intro=re.sub(pattern, '', intr)
        image_nam=form.featured_image.data 
        image_name=image_nam.filename
        random_sg=str(uuid.uuid1())+'_'+ image_name
        random_string=random_sg.replace('\\','/')
        
        
        upload=blog_db(author_id=current_user.id,
                       post_title=form.title.data,
                       post_body=form.post.data,
                       post_intro=intro,
                       category=form.category.data,
                       featured_image='/img/'+random_string
                       )
        file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], random_string)
        form.featured_image.data.save(file_path.replace('\\','/'))
        db.session.add(upload)
        db.session.commit()
        #return render_template('test.html', intro=intro)
        return(redirect(url_for('main.home')))
    return render_template('add_post.html', form=form)
        
        
        


@main.route('/check', methods=['GET', 'POST'])
def check():
    form=Upload_Post()
    flash('i am just testing out the new feature')
    return render_template('test.html')