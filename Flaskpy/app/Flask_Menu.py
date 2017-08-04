#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
添加菜单
'''
from flask import render_template,g
def SystemMenu():
    return render_template('/SystemMenu/menuIndex.html',title='菜单管理',userInfo=g.user,newMenuId=1)