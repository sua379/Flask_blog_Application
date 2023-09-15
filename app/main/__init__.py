# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:08:01 2023

@author: user
"""

from flask import Blueprint

main=Blueprint('main', __name__)

from app.main import views, errors


