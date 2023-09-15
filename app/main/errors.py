# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:10:49 2023

@author: user
"""

from . import main
from flask import render_template

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500