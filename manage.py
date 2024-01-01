# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:39:10 2023

@author: user
"""

from flask.cli import FlaskGroup
from app import create_app
from app.configuration import configuration_dict
from app.main.forms import SearchForm
from app.main.models import blog_db

app=create_app(configuration_dict)
cli=FlaskGroup(app)

if __name__=='__main__':
    cli()
    
@app.context_processor
def inject_posts():
    base_post=blog_db.query.order_by(blog_db.date)
    search_form=SearchForm()
    return {'base_post':base_post, 'search_form':search_form}