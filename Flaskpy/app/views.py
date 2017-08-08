#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from . import app,db,Flask_Email,Flask_Menu,Flask_SystemUser
from flask import  render_template,redirect,url_for,session,flash,g,request
from .forms import LoginForm
from .models import LoginUser,LoginUserIp
import math

#首页
@app.route('/')
@app.route('/index')
def index():
    user={'nickname':'hd'}
    posts = [
        {'author':{'nickname':'hd'},
         'body':'beautiful day in portland!'
         },
        {
            'author':{'nickname':'job'},
            'body':'The Avengers movie was so cool!'
        }


    ]
    return render_template('index.html',user=user,posts=posts)
#用户登陆
@app.route('/userLogin',methods=['GET','POST'])
def userLogin():
    #如果已登陆则直接跳转到用户界面
    if session.keys().__contains__('userIndex'):
        return render_template('userIndex.html',title='登录成功',userInfo = g.user)
    form = LoginForm()
    return Flask_SystemUser.SystemUserLogin(form)
#用户信息
@app.route('/userInfo')
def UserInfo():
    if g.user:
        return render_template('userIndex.html', title='用户中心', userInfo=g.user)
    else:
        return redirect(url_for('index'))
#登陆记录
@app.route('/LoginRecord/<pageIndex>')
def LoginRecord(pageIndex):
    if g.user:
        if not pageIndex:
            pageIndex = 1
        pageCount = 10
        pageIndex = int(str(pageIndex))
        pageStart = (pageIndex-1)*pageCount
        recoreds = db.session.query(LoginUserIp).filter(LoginUserIp.userId == g.user.id).order_by(LoginUserIp.id.desc())
        itemCount = recoreds.count()
        recoreds = recoreds.offset(pageStart).limit(pageCount).all()
        PageSum = int(math.ceil((itemCount/(pageCount*1.0))))
        pageSumCount = range(1,(PageSum+1))
        return render_template('LoginRecord.html',title='用户中心',userInfo=g.user,loginUserIp = recoreds,pageCount = pageSumCount,pageInde = pageIndex,PageSum = PageSum)
    else:
        return redirect(url_for('index'))
#修改昵称
@app.route('/updateNickName',methods=['POST'])
def UpdateNickName():
    if None is g.user:
        return "2",200
    nickName = request.values.get('newNickName',default=None)
    return  Flask_SystemUser.SystemUpdateNickName(nickName)
#发送Email
@app.route("/sendEmail",methods=['POST'])
def Send_Cheked_Email():
    oid = request.values.get('typ')
    email = request.values.get('email',default=None)
    if str(oid) == '1':
        if email == None:
            return "0"
    else:
        email = g.user.userEmail
    rand = Flask_Email.Send_CheckedEmail(oid,email)
    #typ:oid,email:newEmail

    if rand !="0":
        session['rand_'+str(session.get('userIndex'))] = rand
        return "1"
    else:
        return rand
#验证邮箱验证码
@app.route('/checkedEmail/<code>/<email>')
def CheCked_Email(code,email):
    if g.user:
        #拿到验证码
        if not session.keys().__contains__('rand_'+str(session.get('userIndex'))):
            return "2"

        strCode = session.get('rand_'+str(session.get('userIndex')))
        if strCode == code:
            #修改邮箱验证状态
            user = db.session.query(LoginUser).filter(LoginUser.id == session.get('userIndex')).first()
            user.validationEmail = 1
            user.userEmail = email
            db.session.commit()
            #移除ession
            del session['rand_' + str(session.get('userIndex'))]
            return "1"
        else:
            return "0"
    else:
        return "Login Time Out"
#退出登陆
@app.route('/loginOut')
def loginOut():
    if session['userIndex']:
        session.pop('userIndex',None)
    return redirect(url_for('index'))
#修改密码
@app.route('/updatePass',methods=['POST'])
def UpdatePassword():
    if g.user:
        oldPass = request.values.get('oldPass')
        newPass = request.values.get('newPass')
        return Flask_SystemUser.SystemUpdatePassword(oldPass,newPass)
    else:
        return "Login Time Out"
#菜单Menu
@app.route('/SystemMenu')
def SystemMenu():
    if g.user:
        return  Flask_Menu.SystemMenu()
    else:
        return redirect(url_for('index'))
#添加菜单
@app.route('/SystemMenuAdd',methods=['POST'])
def SystemMenuAdd():
    try:
        if g.user:
            menuType = request.values.get('menuType')
            menuName = request.values.get('menuName')
            menuUrl = request.values.get('menuUrl')
            menuEnable = request.values.get('menuEnable')
            return  Flask_Menu.SystemMenuAdd(menuName,menuUrl,menuEnable,menuType)
        else:
            return "Login Time Out"
    except Exception as ex:
        return "0"
#404错误
@app.errorhandler(404)
def error_NotPage(e):
    return render_template('error/404.html',title='未找到页面',errorMess='页面正在施工请稍后再试!')
#500错误
@app.errorhandler(500)
def error_ServerError(e):
    return "Error!Server!Error!",500

#405是什么?忘记了
@app.errorhandler(405)
def error_PageError(e):
    return "Say Hello",200
#每次发来请求的时候先获取用户信息
@app.before_request
def before_request():
    g.user =getCurrent_user()


#拿到用户数据
def getCurrent_user():
    if session.keys().__contains__('userIndex'):
        #为了防止session 不操作过期,重新复制然后更新session 过期时间
        session['userIndex'] = session.get('userIndex')
        user = db.session.query(LoginUser).filter(LoginUser.id == session.get('userIndex')).first()

        #user.userName = str(user.userName,encoding='utf8')
        return user
    else:
        return None