#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 部署Tool

import os
import subprocess
import shutil

source='D:/Workspace_vs/DqSolution/Tools/bin/Debug'
target='D:/Program/Tool/Debug'


resp=os.popen("taskkill /im MyTool.exe /f 2>&1")
print(resp.read())

if os.path.exists(target):
    shutil.rmtree(target,ignore_errors=True)

shutil.rmtree(source+'/logs',ignore_errors=True)
shutil.copytree(source,target)

resp=os.popen('cd '+target+' && MyTool.exe 2>&1')
print(resp.read())



