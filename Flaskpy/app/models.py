#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from . import  db
r'''
    登陆用户
'''
class LoginUser(db.Model):
    __tablename__='loginuser'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    loginName = db.Column(db.String(255),unique=True)
    loginPass = db.Column(db.String(256))
    userName = db.Column(db.String(36))
    userEmail = db.Column(db.String(128),unique=True)
    userHeadImg = db.Column(db.String(255),default='default.gif')
    loginCount = db.Column(db.Integer,default=0)
    validationEmail = db.Column(db.Integer,default=0)#是否验证邮箱,默认都是为未验证


r'''
    用户登录的IP记录
'''
class LoginUserIp(db.Model):
    __tablename__='loginuserip'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    LoginIp = db.Column(db.String(18),default='0.0.0.0')
    LoginTime = db.Column(db.String(36))
    userId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))


r'''
    菜单
'''
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


r'''
    用户文章
'''
class UserArticle(db.Model):
    __tablename__="UserArticle"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r'''
        文章标题
    '''
    articleTitle = db.Column(db.String(512))
    r'''
        文章内容
    '''
    articleContent = db.Column(db.Text())
    r'''
        添加时间
    '''
    insertTime = db.Column(db.DateTime)
    insertUserId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))
    updateTime=db.Column(db.DateTime)
    updateUserId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))
    menuDisable = db.Column(db.Boolean,default=1)


r'''
操作记录
    添加,修改,删除,都有记录操作
'''
class OperationRecord(db.Model):
    __tablename__="OperationRecord"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r'''
    操作类型
    '''
    recordType=db.Column(db.String(32))
    r'''
        操作时间
    '''
    recordTime= db.Column(db.DateTime)
    r'''
        操作用户ID
    '''
    userId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))
    r'''
        记录ID
    '''
    columnId = db.Column(db.Integer)


r'''
用户软件
'''
class UserSoftware(db.Model):
    __tablename__="UserSoftware"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r'''
        软件名称/说明
    '''
    softwareName = db.Column(db.String(512))
    r'''
        软件地址
    '''
    softwareAddress = db.Column(db.String(512))
    r'''
        软件介绍:
            简单的介绍即可
    '''
    softeareIntroduce = db.Column(db.String(1024))
    r'''
        添加时间
    '''
    insertTime = db.Column(db.DateTime)
    r'''
        添加用户
    '''
    insertUserId = db.Column(db.Integer, db.ForeignKey('loginuser.id'))
    r'''
        修改时间
    '''
    updateTime = db.Column(db.DateTime)
    r'''
        修改的用户ID
    '''
    updateUserId = db.Column(db.Integer, db.ForeignKey('loginuser.id'))
    r'''
        是否启用
    '''
    menuDisable = db.Column(db.Boolean, default=1)


r'''
    消费类型
'''
class ConsumptionType(db.Model):
    __tablename__="ConsumptionType"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r'''
            消费类型
    '''
    typeName=db.Column(db.String(512),unique=True)
    r'''
        该消费类型是否可用,如果不可用,则该类型下的所有消费记录都无法查询
    '''
    typeDisable = db.Column(db.Boolean,default=0)

r'''
    消费记录
'''
class ConsumptionRecord(db.Model):
    __tablename__="ConsumptionRecord"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    r'''
        消费类型
    '''
    consumptionTypeId = db.Column(db.Integer,db.ForeignKey('ConsumptionType.id'))
    r'''
        消费金额
    '''
    consumptionMoney = db.Column(db.Float())
    r'''
        消费用户
    '''
    consumptionUserId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))
    r'''
        是收入还是支出
            1是收入
            0是支出
            
    '''
    consumptionType = db.Column(db.Boolean,default=1)
    r'''
        是否作废,作废之后不计入统计
    '''
    consumptionDisable = db.Column(db.Boolean,default=0)

    r'''
        添加时间
    '''
    consumptionInsertTime = db.Column(db.DateTime)
    r'''
        添加用户
    '''
    consumptionInsertUserId = db.Column(db.Integer,db.ForeignKey('loginuser.id'))

    r'''
        消费时间
    '''
    consumptionTime =db.Column(db.DateTime)




