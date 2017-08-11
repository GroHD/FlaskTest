#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
用户表
'''
from . import db
from flask import g,session,request,redirect,url_for,flash,render_template
from .models import LoginUser,LoginUserIp
import  hashlib,time
def SystemUserLogin(form):
    if form.validate_on_submit():
       hasbPass = hashlib.sha256()
       hasbPass.update(form.userPass.data.encode('utf8'))
       shaPass = hasbPass.hexdigest()
       userAdmin =  db.session.query(LoginUser).filter(LoginUser.loginName==form.userName.data,LoginUser.loginPass == shaPass).first()
       if  userAdmin != None:
            session['userIndex'] = userAdmin.id

            host = request.access_route[0]
            userAdmin.loginCount = userAdmin.loginCount+1#登陆次数加1
            #设置登陆次数
            loginU =  LoginUserIp(LoginIp=host,userId=userAdmin.id,LoginTime = time.strftime('%Y-%m-%d %X', time.localtime()))
            db.session.add(loginU)
            db.session.commit()

            g.user = userAdmin
            return redirect(url_for('UserInfo'))
       else:
           flash('密码或用户名错误')
    return render_template('userLogin.html', title='HD Blog Login', form=form)
def SystemUpdateNickName(nickName):
    if nickName:
        userInfo = db.session.query(LoginUser).filter(LoginUser.id == session.get('userIndex')).first()
        userInfo.userName = nickName
        db.session.commit()
        return "1",200
    else:
       return "0",200
def SystemUpdatePassword(oldPass,newPass,confNewPass):
    if oldPass is None:
        # 旧密码为空
        return "0"
    if newPass is None:
        # 新密码为空
        return "-1"
    if newPass != confNewPass:
        #两次密码不一致
        return "-2"
    hasbPass = hashlib.sha256()
    hasbPass.update(oldPass.encode('utf8'))
    shaPass = hasbPass.hexdigest()
    if g.user.loginPass ==shaPass :
        user = db.session.query(LoginUser).filter(LoginUser.id == session.get('userIndex')).first()
        hasbPass = hashlib.sha256()
        hasbPass.update(newPass.encode('utf8'))
        shaPass = hasbPass.hexdigest()
        user.loginPass = shaPass
        db.session.commit()
        # 修改成功
        return "1"
    else:
        # 旧密码不匹配
        return "2"