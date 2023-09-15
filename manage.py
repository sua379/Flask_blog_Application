# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:39:10 2023

@author: user
"""

from flask.cli import FlaskGroup
from app import create_app
from app.configuration import configuration_dict

app=create_app(configuration_dict)
cli=FlaskGroup(app)

if __name__=='__main__':
    cli()
    
