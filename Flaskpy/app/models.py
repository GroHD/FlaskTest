#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from . import  db
class LoginUser(db.Model):
    __tablename__='loginuser'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    loginName = db.Column(db.String(255),unique=True)
    loginPass = db.Column(db.String(256))
    userName = db.Column(db.String(36))
    userEmail = db.Column(db.String(128),unique=True)
    userHeadImg = db.Column(db.String(255),default='default.gif')
    loginCount = db.Column(db.Integer,default=0)
    validationEmail = db.Column(db.Integer,default=0)#是否验证邮箱,默认都是为验证


class LoginUserIp(db.Model):
    __tablename__='loginuserip'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    LoginIp = db.Column(db.String(18),default='0.0.0.0')
    LoginTime = db.Column(db.String(36))
    userId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))

class SystemMenu(db.Model):
        __tablename__="systemMenu"
        id = db.Column(db.Integer,primary_key=True,autoincrement=True)
        '''
        菜单名称
        '''
        menuName = db.Column(db.String(32),unique=True)
        '''
        菜单URL
        '''
        menuUrl = db.Column(db.String(128),default='#')
        '''
        上级ID
        '''
        parendId = db.Column(db.Integer,default=0)
        '''
        是否启用,默认启用
        '''
        menuDisable = db.Column(db.Boolean,default=1)




