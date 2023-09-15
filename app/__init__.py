# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 21:46:41 2023

@author: user
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from .configuration import configuration_dict
from flask import Flask, render_template
from flask_login import LoginManager
from flask_ckeditor import CKEditor 



ckeditor=CKEditor()
migrate=Migrate()
mail=Mail()
moment=Moment()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'


def create_app(configuration_dict):
    app=Flask(__name__)
    app.config.from_object(configuration_dict['development'])
    configuration_dict['development'].init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    return app
    