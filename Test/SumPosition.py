#!/usr/bin/python3
# 汇总仓位
#coding=utf-8
import os
import time
import paramiko
import sys


####### 变量定义 #######


wcgx=r'/CTA/MSTS/共喜/Release/最新持仓信息/每日持仓-{0}.csv'
ddmy=r'/CTA/MSTS/明月/Release/最新持仓信息/每日持仓-{0}.csv'
fh=r'/CTA/MSTS/复华/Release/最新持仓信息/每日持仓-{0}.csv'
zy=r'/CTA/MSTS/自营/Release/最新持仓信息/每日持仓-{0}.csv'
ry=r'/CTA/MSTS/瑞月/Release/最新持仓信息/每日持仓-{0}.csv'
jy=r'/CTA/MSTS/晶月/Release/最新持仓信息/每日持仓-{0}.csv'
qy=r'/CTA/MSTS/秋月/Release/最新持仓信息/每日持仓-{0}.csv'

##########  main  ########

date=time.strftime("%Y%m%d",time.localtime(time.time()))
#date='20160906'




username="1"
password="1"

#国际期货
client = paramiko.Transport(("180.169.101.101",8081))
client.connect(username=username,password=password)
sftp = paramiko.SFTPClient.from_transport(client)

remotepath=(zy.format(date)).encode(encoding='gb2312', errors='strict');
localpath=r"D:\Temp\持仓自营-CTA-{0}.csv".format(date)
sftp.get(remotepath, localpath)


client.close()



        

