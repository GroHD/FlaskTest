#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
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
    pas.update(b'admin') #要加密的内容
    varPass = pas.hexdigest()# 取到加密后的密文
    u = models.LoginUser(loginName='admin',loginPass=varPass,userEmail='1105061266@qq.com',loginCount=0,userName=str('超级管理员'))
    menuNotes = models.SystemMenu(menuName='笔记',menuUrl='Notes')
    menuSoft = models.SystemMenu(menuName='软件', menuUrl='Software')
    menuMate = models.SystemMenu(menuName='资料', menuUrl='Material')
    menuConsuRe = models.SystemMenu(menuName='消费记录', menuUrl='ConsumptionRe')
    db.session.add(u)
    db.session.add(menuNotes)
    db.session.add(menuSoft)
    db.session.add(menuMate)
    db.session.add(menuConsuRe)
    db.session.commit()
    db.session.remove()
