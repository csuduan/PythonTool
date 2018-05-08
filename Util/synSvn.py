#!/usr/bin/python3
# coding=utf-8

import os
import time
import re
# import paramiko
import shutil

##############  自定义变量  ##############
svnrepo = r"D:\svn\svn-aliyun"
mstspath = r"D:\MSTS"

date = time.strftime("%Y%m%d", time.localtime(time.time()))
now = time.strftime("%Y%m%d %H:%M:%S", time.localtime(time.time()))
positionPath = svnrepo + "/持仓/CTA策略/" + date
positionDetailPath = svnrepo + "/仓位明细/"
profitRecordPath = svnrepo + "/收益记录/"
positionMarketValuePath = svnrepo + "/市值/"

cachePath=svnrepo + "/缓存/"
#########   Main     ############
print("开始同步svn" + now)

# 更新svn
os.system("svn up  " + svnrepo)
print("更新svn完毕")

try:
    # 拷贝 仓位/收益等
    if os.path.exists(positionPath) == False:
        os.makedirs(positionPath)

    for account in os.listdir(mstspath):
        if account.count("结束") > 0 or account.count("over") > 0:
            continue
        print("开始处理:" + account)

        # 每日持仓
        source = mstspath + "/" + account + r"/Release/最新持仓信息/每日持仓-" + date + ".csv"
        target = positionPath + "/持仓" + account + "-CTA-" + date + ".csv"
        print(target)
        shutil.copyfile(source, target)

        # 仓位明细
        source = mstspath + "/" + account + r"/Release/最新持仓信息/最新仓位信息-" + date + ".csv"
        target = positionDetailPath + account + "-CTA-仓位明细-" + date + ".csv"
        print(target)
        shutil.copyfile(source, target)

        # 收益记录
        source = mstspath + "/" + account + r"/Release/Logs/PerformanceLog"
        target = profitRecordPath + account
        print(target)
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(source, target)

        # 市值信息
        source = mstspath + "/" + account + r"/Release/Logs/PositionLog"
        target = positionMarketValuePath + account
        print(target)
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(source, target)

        # 缓存
        source = mstspath + "/" + account + r"/Release/cache.db"
        target = cachePath + account
        if os.path.exists(target) == False:
            os.makedirs(target)
        shutil.copyfile(source, target + "/cache.db")
except Exception as e:
    print(e)

# 提交svn
os.system(r'svn add  ' + svnrepo + ' --no-ignore --force')
os.system(r'svn commit -m "" ' + svnrepo)
print("同步svn完毕")

# time.sleep(5)
