# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 23:25:44 2023

@author: user
"""

from flask import Blueprint

auth=Blueprint('auth', __name__)

from app.auth import views, forms, models