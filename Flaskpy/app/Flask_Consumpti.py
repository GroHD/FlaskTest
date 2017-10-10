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
from sqlalchemy import  func
from flask import  render_template,g
from  datetime import datetime
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
#添加消费
def AddConsunPtion(xfType,xfMoney,xfTime,jeYongTu):
    try:
        if(len(xfMoney) <=0):
            return "1"
        xfdt =datetime.strptime(xfTime,'%Y-%m-%d')
        consun = ConsumptionRecord(consumptionTypeId=int(xfType),consumptionMoney=xfMoney,consumptionUserId = g.user.id,consumptionType=int(jeYongTu),consumptionDisable = 1,consumptionInsertUserId = g.user.id,consumptionInsertTime = datetime.utcnow(),consumptionTime=xfdt)
        db.session.add(consun)
        db.session.commit()
        return  "0"
    except Exception as ex:
        raise  ex
#拿到消费的列表
def GetMoney(sDate,eDate):
    try:
        consumAll = db.session.query(func.sum(ConsumptionRecord.consumptionMoney),ConsumptionRecord.consumptionType,ConsumptionRecord.consumptionTime).filter(ConsumptionRecord.consumptionTime>=sDate,ConsumptionRecord.consumptionTime<=eDate).group_by(ConsumptionRecord.consumptionType,ConsumptionRecord.consumptionTime).all()
        if consumAll is None or len(consumAll)<=0:
            return "[]"
        jsonStr ='['
        for consumItem in consumAll:
            if len(jsonStr)>2:
                jsonStr = jsonStr+','
            stp = str(consumItem[2]).split(' ')
            jsonStr = jsonStr+'{\"'+stp[0]+'\":'+str(consumItem[0])+',\"typ\":\"'+str(consumItem[1])+'\"}'
        jsonStr= jsonStr+']'
        return jsonStr
    except Exception as ex:
        return ex

#获取某一天的消费情况
def GetDateCase(date):
    try:
        caseDate = db.session.query(ConsumptionRecord.id,ConsumptionRecord.consumptionMoney,ConsumptionRecord.consumptionUserId,ConsumptionRecord.consumptionType).filter(ConsumptionRecord.consumptionTime>=str(date)+' 00:00:00',ConsumptionRecord.consumptionTime<=str(date)+' 23:59:59').all()
        if caseDate is None or len(caseDate)<=0:
            return "[]"
        jsonStr='['
        for item in caseDate:
            if  len(jsonStr)>2:
                jsonStr = jsonStr+','
            jsonStr = jsonStr+'{"ID":'+str(item[0])+',"Money":'+str(item[1])+',"UserId":'+str(item[2])+',"ConType":"'+str(item[3])+'"}'
        jsonStr = jsonStr+']'
        return jsonStr
    except Exception as ex:
        return ex

# 删除消费
def DeleteDatacash(id):
    try:
       db.session.query(ConsumptionRecord).filter(ConsumptionRecord.id == id).delete()
       db.session.commit()
       return "1"
    except Exception as ex:
        return ex

def GetMaxId():
    consuAll = db.session.query(ConsumptionType).order_by(ConsumptionType.id.desc()).first()
    if consuAll is not None:
        return consuAll.id+1
    else:
        return 1

