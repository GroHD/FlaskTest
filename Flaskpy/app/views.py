#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from . import app,db,Flask_Email,Flask_Menu,Flask_SystemUser,Flask_Consumpti
from flask import  render_template,redirect,url_for,session,flash,g,request
from .forms import LoginForm
from .models import LoginUser,LoginUserIp
from . import  models
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
    return render_template('index.html',user=user,posts=posts,menu =g.menu)
#用户登陆
@app.route('/userLogin',methods=['GET','POST'])
def userLogin():
    #如果已登陆则直接跳转到用户界面
    if session.keys().__contains__('userIndex'):
        return render_template('userIndex.html',title='登录成功',userInfo = g.user,menu =g.menu)
    form = LoginForm()
    return Flask_SystemUser.SystemUserLogin(form)
#用户信息
@app.route('/userInfo')
def UserInfo():
    if g.user:
        return render_template('userIndex.html', title='用户中心', userInfo=g.user,menu =g.menu)
    else:
        return redirect(url_for('index'))
#登陆记录
@app.route('/LoginRecord/<pageIndex>')
def LoginRecord(pageIndex):
    if g.user:
        if not pageIndex:
            pageIndex = 1
        pageCount = 6
        pageIndex = int(str(pageIndex))
        pageStart = (pageIndex-1)*pageCount
        recoreds = db.session.query(LoginUserIp).filter(LoginUserIp.userId == g.user.id).order_by(LoginUserIp.id.desc())
        itemCount = recoreds.count()
        recoreds = recoreds.offset(pageStart).limit(pageCount).all()
        PageSum = int(math.ceil((itemCount/(pageCount*1.0))))
        pageSumCount = range(1,(PageSum+1))
        return render_template('LoginRecord.html',title='用户中心',userInfo=g.user,loginUserIp = recoreds,pageCount = pageSumCount,pageInde = pageIndex,PageSum = PageSum,menu =g.menu)
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
        confNewPass = request.values.get('confNewPass')
        return Flask_SystemUser.SystemUpdatePassword(oldPass,newPass,confNewPass)
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
#修改菜单的状态
@app.route('/menuState',methods=['POST'])
def SystemMenuStateChange():
    if  g.user is not None :
        try:
            id = request.values.get('id')
            state = request.values.get('state')
            return Flask_Menu.SysteMenuStateChange(id,state)
        except Exception as ex:
            print("SystemMenuStateChange===>>"+ex)
            return "-2"
    else:
        return "Login Time Out...."
#删除菜单(永久删除)
@app.route('/menuDelete',methods=['POST'])
def SystemMenuDelete():
    if g.user is not None:
        try:
            id = request.values.get('id')
            return Flask_Menu.SystemMenuDeleted(id)
        except Exception as ex:
            print("SystemMenuDelete=====>"+ex)
            return "-1"
    else:
        return "Login Time Out...."

#消费类型
@app.route('/ConsumptionTy/<pageIndex>',methods=['GET'])
def ConsumptiTy(pageIndex):
    if g.user is not None:
        return Flask_Consumpti.GetComsumPtiList(pageIndex)
    else:
        return redirect(url_for('index'))
#添加消费类型
@app.route('/ConsumPtionInsert',methods=['POST','GET'])
def ConsumPtionInsert():
    if g.user is not None:
        #类型名称
        menuName = request.values.get('menuName')
        #是否启用
        menuEnable = request.values.get('menuEnable')
        #id 如果是0则表示是添加,否则就是修改
        typ = request.values.get('typ')
        return Flask_Consumpti.InsertComsumPti(menuName,menuEnable,typ)
    else:
        return 'Login Time Out'
#修改消费类型状态
@app.route('/updateState',methods=['POST'])
def ConsumPtionUpdateState():
    if g.user is not None:
        menuState = request.values.get('menuStateType')
        conId = request.values.get('id')
        return Flask_Consumpti.UpdateComsumPtiState(menuState,conId);
    else:
        return 'Login Time Out'
#删除消费类型
@app.route('/deleteConsun',methods=['POST'])
def ConsumPtionDelete():
    if g.user is not None:
        cid=  request.values.get('id')
        return Flask_Consumpti.DeleteComsumPtion(cid)
    else:
        return 'Login Time Out'

#添加消费
@app.route('/ConsumptionRe',methods=['GET'])
def ConsunPtionRe():
    if g.user is not None:
        conType = GetConTypeList()
        return  render_template('/Consumpti/ConsunPtionReOptions.html',title='消费记录',menu=g.menu,conType = conType)
    else:
        return redirect(url_for('index'))

@app.route('/GetMoney',methods=['GET'])
def GetDayMoney():
    if g.user is not None:
        try:
            return Flask_Consumpti.GetMoney()
        except Exception as ex:
            return ex
    else:
        return "login Out"
#获取消费类型
def GetConTypeList():
    return Flask_Consumpti.GetComsumTypeList()
#添加消费金额
@app.route('/ConsunPtionReSave',methods=['POST'])
def SaveConsunPtion():
    if g.user is not None:
        try:
            xfType = request.values.get('xfType') #消费类型
            xfMoney = request.values.get('xfMoney')#消费金额
            xfTime = request.values.get('xfTime')#消费时间
            jeYongTu = request.values.get('jeYongTu')#金额用途
            return Flask_Consumpti.AddConsunPtion(xfType,xfMoney,xfTime,jeYongTu)
        except Exception as ex:
            return ex;

    else:
        return " Login Out"
#404错误
@app.errorhandler(404)
def error_NotPage(e):
    return render_template('error/404.html',title='未找到页面',errorMess='页面正在施工请稍后再试!')
#500错误
@app.errorhandler(500)
def error_ServerError(e):
    return "Error!Server!Error!"

#405是什么?忘记了
@app.errorhandler(405)
def error_PageError(e):
    return "Say Hello",200
#每次发来请求的时候先获取用户信息
@app.before_request
def before_request():
    g.user =getCurrent_user()
    getMenu()
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
#拿到要显示的菜单,如果是0则是禁用的
def getMenu():
    menu = db.session.query(models.SystemMenu).filter(models.SystemMenu.menuDisable == 1).all()
    g.menu = menu


#http://echarts.baidu.com/demo.html#mix-zoom-on-value