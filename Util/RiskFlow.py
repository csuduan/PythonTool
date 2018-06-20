#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @desc  : 风险控制模块
import  logging




def RiskControl(product,value):
    retNetValueCheck=NetValueCheck()
    if retNetValueCheck==False:
        logging.warn("未通过市值检测，禁止交易！")
        return False

    retProductRangeCheck=ProductRangeCheck(product)
    if retProductRangeCheck==False:
        logging.warn("该品种超出投资范围，禁止交易！")
        return False

    retProductValueCheck=ProductValueCheck(product,value)
    if retProductValueCheck==False:
        logging.warn("该品种市值超限，禁止交易！")
        return False
    return True



def NetValueCheck():
    '''
    净值检测
    '''
    warnLine1 = 0.93
    warnLine2 = 0.88
    closeLine = 0.80

    netValue=GetNetValue()
    if netValue > warnLine1 :
        return  True
    elif netValue >warnLine2:
        DoWarn1()    #执行告警1
        return False
    elif netValue >closeLine:
        DoWarn2()     #执行告警2
        return False
    else:
        DoClose()    #执行止损
        return  False


def ProductRangeCheck(product):
    '''
        品种范围检测
    '''

    productList=GetProductListFromDb() #从数据库获取投资品种列表
    if product in product:
        return True
    else:
        return  False


def ProductValueCheck(product):
    '''
        品种价值检测
    '''
    ratioList=CalProductRatio(product)    #计算品种各风控指标
    productLine=GetProductCtrlLine(product)  #获取品种风控线

    ret=True

    for i in len(ratioList):
        if ratioList[i]>productLine[i]:
            logging.warn("单品种控制超限")
            ret=False

    return ret






def GetProductListFromDb():
    pass
def GetNetValue():
    pass
def DoWarn1():
    pass
def DoWarn2():
    pass

def DoClose():
    pass

def CalProductRatio():
    pass

def GetProductCtrlLine():
    pass



