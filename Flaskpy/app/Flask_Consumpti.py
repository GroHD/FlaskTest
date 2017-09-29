#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
消费
'''
r'''
    获取消费类型列表
    @pageIndex 是页码
'''
from .models import  ConsumptionType,ConsumptionRecord
from . import  db
from flask import  render_template,g
import time
#获取列表
def GetComsumPtiList(pageIndex):
    consuAll =   db.session.query(ConsumptionType).order_by(ConsumptionType.id.asc()).all()
    maxId = len(consuAll)
    if maxId >0:
        objMaxId = consuAll[maxId-1]
        maxId = objMaxId.id+1
    else:
        maxId = maxId+1
    return render_template('Consumpti/ConsumptionTy.html',title='消费类型',menu = g.menu,userInfo = g.user,Consumption = consuAll,maxId = maxId)
#添加数据
def InsertComsumPti(comsumPtiName,comsumPtiEnable,id):
    try:
        if len(comsumPtiName)<=0:
            return "-2"
        checkBool = CheckedComsunPti(comsumPtiName,id)
        if checkBool:
            return "-1"
        if int(id)>0:
            consu = db.session.query(ConsumptionType).filter(ConsumptionType.id == id).first()
            if consu is not None:
                consu.typeName = comsumPtiName
                consu.typeDisable = comsumPtiEnable
                db.session.commit()
        else:
            consu = ConsumptionType(typeName=comsumPtiName,typeDisable = int(comsumPtiEnable))
            db.session.add(consu)
            db.session.commit()
        return str(GetMaxId())
    except  Exception as ex:
        return ex
#修改状态
def UpdateComsumPtiState(comsumPtiState,id):
    try:
        consum = db.session.query(ConsumptionType).filter(ConsumptionType.id == int(id)).first()
        if consum is not None:
            if comsumPtiState == 'True':
                consum.typeDisable = 0
            else:
                consum.typeDisable = 1
            db.session.commit()
            return "0"
        else:
            return "-1"
    except Exception as ex:
        return ex
#删除数据
def DeleteComsumPtion(id):
    try:
         db.session.query(ConsumptionType).filter(ConsumptionType.id == id).delete()
         db.session.commit()
         return str(GetMaxId())
    except Exception as ex:
        return ex;
r'''
    判断消费类型是否使用
'''
def CheckedComsunPti(typeName,id):
    if int(id)>0:
        checkedConsu = db.session.query(ConsumptionType).filter(ConsumptionType.typeName == typeName,ConsumptionType.id != id).all()
        if len(checkedConsu)>0:
            return True
        else:
            return False
    else:
        checkedConsu = db.session.query(ConsumptionType).filter(ConsumptionType.typeName == typeName).all()
        if len(checkedConsu) > 0:
            return True
        else:
            return False

#拿到消费类型的数据
def GetComsumTypeList():
    conTyp = db.session.query(ConsumptionType).filter(ConsumptionType.typeDisable == 1).order_by(ConsumptionType.id.asc()).all()
    return conTyp
def AddConsunPtion(xfType,xfMoney,xfTime,jeYongTu):
    try:
        consun = ConsumptionRecord(consumptionTypeId=xfType,consumptionMoney=xfMoney,consumptionUserId = g.user.id,consumptionType=jeYongTu,consumptionDisable = 1,consumptionInsertUserId = g.user.id)
        db.session.add(consun)
        db.session.commit()
    except Exception as ex:
        raise  ex
def GetMaxId():
    consuAll = db.session.query(ConsumptionType).order_by(ConsumptionType.id.desc()).first()
    if consuAll is not None:
        return consuAll.id+1
    else:
        return 1

