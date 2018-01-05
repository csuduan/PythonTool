#!/usr/bin/python3
#coding=utf-8

import os
import time
import re
#import paramiko
import shutil


##############  自定义变量  ##############
accountList=['大地明月','微冲共喜','海通繁星','华泰赤月','国泰晶月','红岭秋月','中信皓月','复华一号']


mstspath=r"D:\CTA\MSTS"
date=time.strftime("%Y%m%d",time.localtime(time.time()))
date1=time.strftime("%Y.%m.%d",time.localtime(time.time()))
svnrepo=r"D:\svn\svn-aliyun"

positionPath=svnrepo+"/持仓/CTA策略/"+date
positionDetailPath=svnrepo+"/仓位明细/"
profitRecordPath=svnrepo+"/收益记录/"
#########   Main     ############
#更新svn
os.system("svn up  "+svnrepo)

if os.path.exists(positionPath) == False:
	os.makedirs(positionPath)

for account in accountList:
	#每日持仓
	source=mstspath+"/"+account+r"/Release/最新持仓信息/每日持仓-"+date+".csv"
	target=positionPath+"/持仓"+account+"-CTA-"+date+".csv"
	print(target)
	shutil.copyfile(source,target)

	#仓位明细
	source=mstspath+"/"+account+r"/Release/最新持仓信息/最新仓位信息-"+date+".csv"
	target=positionDetailPath+account+"-CTA-仓位明细-"+date+".csv"
	print(target)
	shutil.copyfile(source,target)

	#收益记录
	source=mstspath+"/"+account+r"/Release/Logs/PerformanceLog"
	target=profitRecordPath+account
	print(target)
	if os.path.exists(target):
		shutil.rmtree(target)
	shutil.copytree(source,target)


#提交svn
os.system(r'svn add  '+svnrepo+' --no-ignore --force')
os.system(r'svn commit -m "" '+svnrepo)

time.sleep(5)


