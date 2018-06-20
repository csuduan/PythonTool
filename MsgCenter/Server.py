#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/6/6 15:16
# @desc  :

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by duanqing 2018/2/6

from flask import Flask, jsonify, request
import json


import logging

logger = logging.getLogger(__name__)

# 导入模块
from QYWX import *
# 初始化机器人，扫码登陆
#bot = Bot(cache_path=True)

#初始化企业微信接口
aggentid = '1000004'
corpid = 'ww8e9eafab581b182c'
corpsecret = 'kFdYRS9olP_P28_9yGLH5i2r6xsinz78GZLJUTezXHA'
wx = QYWX(corpid, corpsecret, aggentid)
config = None

f = open("config.json",encoding='utf-8')
config=json.load(f)
f.close()

print("启动...")


print("加载:",config)

# Flask初始化
app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    return  "helloworld"

@app.route('/send', methods=['POST'])
def sendMsg():

    ret='SUCCESS'
    try:

        msg = request.json['msg']
        topicName = request.json['topic']

        topic=list(filter(lambda x: x['topic']==topicName,config['subscribe']))[0]
        users=topic.get('users')
        if users!=None:
            wx.sendMessage(msg, users=users)

        chat=topic.get('chat')
        if chat!= None:
            wx.sendChat(msg, chat_id=chat)

    except Exception as ex:
        logging.error(ex)
        ret="ERROR"


    return  ret



if __name__ == "__main__":
    # 生产模式关闭debug
    app.run(host='0.0.0.0', debug=True,use_reloader=False)


