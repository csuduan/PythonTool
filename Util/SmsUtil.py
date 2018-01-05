#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib
import urllib.parse
import numpy as np
import pandas as pd
import base64
import time

#----------------------------------
# 短信发送工具 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/54
#----------------------------------

appkey = "d6be4ede12d9b41b4e9aa2466d3cf3e1"
tpl_id = '37084'

def main():

    print('''
###########################
    上海宽投短信通知工具
###########################
注意：由于运行商限制
“同1个号码同1个签名的内容1分钟内只能接收1条，1小时内只能接收3条，一天最多接收10条”
若存在某个客户需要通知多个账户密钥情况，注意控制每个账户的发送间隔
        
    ''')

    dfProduct=pd.read_excel("SmsUtil.xlsx",sheetname='Product')
    dfUser=pd.read_excel("SmsUtil.xlsx",sheetname='User')
    dfProduct=dfProduct[dfProduct.IsSend=='Y' ]

    print(dfProduct)
    productNo=input('请输入产品序号,-1表示所有:')
    if productNo=='-1':
        df1=dfProduct
    else:
        df1=dfProduct[dfProduct.index== int(productNo)]

    print('已选择以下产品:')
    print(df1)
    sure=input("确认请输入y，其他退出:")
    if sure!='y':
        return
    df=pd.merge(df1,dfUser,how='left',on='Product')

    print('待发送清单：')
    print(df)

    #df.apply(lambda x: sendSms(x.Name, x.Phone,x.Key), axis=1)
    for i in df.index:
        name, phone,key = df.loc[i, ['Name', 'Phone','Key']].values
        sendSms(name,phone,key)


    #2.发送短信
    #sendSms(appkey,"GET")


#发送某个产品


#屏蔽词检查测
def checkSms(m="GET"):
    url = "http://v.juhe.cn/sms/black"
    params = {
        "word" : "", #需要检测的短信内容，需要UTF8 URLENCODE
        "key" : appkey, #应用APPKEY(应用详细页查询)

    }
    params = urllib.parse.urlencode(params)
    if m =="GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print (res["result"])
        else:
            print ("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print ("checkSms error")

#发送短信
def sendSms(name,phone,key):
    print(f'''准备向{name} {phone}发送短信通知''')
    #return
    url = "http://v.juhe.cn/sms/send"
    params = {
        "key" : appkey, #应用APPKEY(应用详细页查询)
        "tpl_id" : tpl_id, #短信模板ID，请参考个人中心短信模板设置

        "mobile" : phone, #接收短信的手机号码
        "tpl_value" : f'''#Name#={name}&#Key#={key}''',

    }
    params = urllib.parse.urlencode(params)
    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            #print ("发送成功"+res["result"]["sid"])
            print("发送成功")
        else:
            print ("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print ("sendSms api error")



if __name__ == '__main__':
    main()