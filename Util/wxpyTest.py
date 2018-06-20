#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/6/6 9:27
# @desc  :

# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆


def qrHandler(uuid, status, qrcode):
    pass

bot = Bot(qr_path='qr.jpg')

my_friend = bot.friends().search('瘦瘦')[0]


pass