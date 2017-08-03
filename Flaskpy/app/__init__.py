#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from flask import  Flask
from timeit import  timeit
from flask_sqlalchemy import  SQLAlchemy

import  os
app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
from . import views,models