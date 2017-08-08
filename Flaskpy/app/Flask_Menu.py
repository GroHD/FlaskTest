#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
添加菜单
'''
from flask import render_template,g
from . import db,models
def SystemMenu():
    menuAll = db.session.query(models.SystemMenu).order_by(models.SystemMenu.id.desc()).all();
    maxId = len(menuAll)
    maxId = maxId+1
    return render_template('/SystemMenu/menuIndex.html',title='菜单管理',userInfo=g.user,newMenuId=maxId,sysMenuAll = menuAll)

def SystemMenuAdd(menuName,menuUrl,menuChecked,menuType):
    try:
        if len(menuName.strip(' '))<=0:
            return "1"
        elif len(menuUrl.strip(' '))<=0:
            return "2"
        if int(menuType) <=0:
            menuSys = models.SystemMenu(menuName=menuName,menuUrl=menuUrl,menuDisable = int(menuChecked))
            db.session.add(menuSys)
            db.session.commit()
        else:
            menuSys = db.session.query(models.SystemMenu).filter(models.SystemMenu.id == menuType).first()
            menuSys.menuName = menuName
            menuSys.menuUrl = menuUrl
            menuSys.menuDisable = int(menuChecked)
            db.session.commit()

        return "0"
    except Exception as ex:
        raise ex
