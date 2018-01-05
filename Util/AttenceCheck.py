# -*- coding:utf-8 -*-
import pyodbc
import pandas as pd
import time
import smtplib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#考勤坚持工具

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)



#receivers=['duanq@quantinv.com','zhengl@quantinv.com']

#cnxn = pyodbc.connect("DSN=testaccess")
DBfile='D:\\tmp\\att2000.mdb'
date=time.strftime('%Y%m%d',time.localtime(time.time()))

def notice(context,receivers):
    subject = '缺勤记录-测试（请忽略）'
    smtpserver = 'smtp.126.com'
    username = 'csuduan@126.com'
    password = 'quantfly2016'

    msg = MIMEText(context,'text','utf-8')#中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To']=";".join(receivers)
    msg['From']=username

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(username, receivers, msg.as_string())
    smtp.quit()
    pass




def main():
    #获取考勤记录集用户信息
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
    dfUser=pd.read_sql("select * from USERINFO",conn)
    df=pd.read_sql("SELECT * FROM CHECKINOUT",conn)
    conn.close()

    dfUser['Name']=dfUser['Name'].apply(lambda x:x.split('\x00')[0])
    dfValidUser=dfUser[(dfUser.street.isnull()==False)&(dfUser.street!='')]
    #receivers=dfUser[dfUser.street.isnull()==False]['street'].unique()


    df['Date']=df['CHECKTIME'].apply(lambda x : x.strftime('%Y%m%d'))
    df1=df[df.Date==date]

    df2=df1.merge(dfUser,on='USERID')[['Name','CHECKTIME']]
    #df2['exist']=~df2.duplicated('Name',keep='first')
    #df2=df2[df2.exist==True]

    list1=dfValidUser['Name'].unique()
    list2=df2['Name'].unique()

    diff=set(list1)-set(list2)



    print('出勤记录：')
    print(df2)
    print('缺勤名单：')
    print(diff)


    if  len(df2)==0 or len(diff)==0:
        return



    result='出勤记录:\n'+str(df2)+'\n\n缺勤名单：\n'+str(diff)+'\n\n请坚持打卡！'


    #获取缺勤者邮箱
    receivers=['duanq@quantinv.com','zhengl@quantinv.com']
    for name in diff:
        mail=dfValidUser[dfValidUser.Name==name].iloc[0]['street']
        receivers.append(mail)


    notice(result,receivers)
    print('END')

if __name__ == '__main__':
    main()







