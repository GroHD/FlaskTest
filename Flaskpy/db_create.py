#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from config import SQLALCHEMY_MIGRATE_REPO
from app import  db,models
import hashlib
import os.path
#创建数据库
db.drop_all()
db.create_all()
#插入一条默认的数据
adminUser = db.session.query(models.LoginUser).filter(models.LoginUser.userName=='admin').all()
#如果创建数据库的时候数据没有存在则添加一条默认的数据
if not adminUser:
    #进行加密
    pas = hashlib.sha256()
    pas.update(b'houge9999991') #要加密的内容
    varPass = pas.hexdigest()# 取到加密后的密文
    u = models.LoginUser(loginName='admin',loginPass=varPass,userEmail='1105061266@qq.com',loginCount=0,userName=buffer('超级管理员'))
    db.session.add(u)
    db.session.commit()
    db.session.remove()
