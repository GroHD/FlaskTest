#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    userName = StringField('userName',validators=[DataRequired(message='用户名不可为空')])
    userPass = PasswordField('userPass',validators=[DataRequired(message='密码不可为空')])
    remember_me = BooleanField('remember_me',default=False)