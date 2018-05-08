#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/4/20 9:22
# @desc  :


import os
import time
import re
import shutil


##############  自定义变量  ##############
svnrepo = r"D:\svn\svn-aliyun"
mstspath = r"D:\MSTS"

date = time.strftime("%Y%m%d", time.localtime(time.time()))
now = time.strftime("%Y%m%d %H:%M:%S", time.localtime(time.time()))

cachePath=svnrepo + "/缓存/"
#########   Main     ############
print("开始同步svn" + now)

# 更新svn
os.system("svn up  " + svnrepo)
print("更新svn完毕")

try:

    for account in os.listdir(mstspath):
        if account.count("结束") > 0 or account.count("over") > 0:
            continue
        print("开始处理:" + account)


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