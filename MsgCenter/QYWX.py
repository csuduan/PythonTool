#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: XiaoZ
# @created on: 2018/6/14 0:42
# @desc  :

import urllib.request
import json
import threading


class MsgType(object):
    msg_to_chat = 'appchat/send'
    msg_to_user = 'message/send'
    create_chat = 'appchat/create'


class QYWX(object):
    def __init__(self, corpid, corpsecret, aggentid, url='https://qyapi.weixin.qq.com'):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.url = url

        self.aggentid = aggentid

        self.__get_token()



    # 获取企业微信token
    def __get_token(self):
        token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (self.url, self.corpid, self.corpsecret)
        self.token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']
        print('get token:'+self.token)

        timer = threading.Timer(7200, self.__get_token)
        timer.start()


    def __chat(self, msg, chat_id):
        values = {
            "chatid": chat_id,
            "msgtype": 'text',
            "text": {'content': msg},
            "safe": 0
        }
        msg = (bytes(json.dumps(values), 'utf-8'))

        return msg


    def __message(self, msg, users):
        values = {
            "touser": users,
            "msgtype": 'text',
            "agentid": self.aggentid,
            "text": {'content': msg},
            "safe": 0
        }
        msg = (bytes(json.dumps(values), 'utf-8'))

        return msg

    # post请求
    def __post(self, data, msg_type=MsgType.msg_to_chat):
        send_url = '%s/cgi-bin/%s?access_token=%s' % (self.url, msg_type, self.token)
        respone = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()
        x = json.loads(respone.decode())['errcode']
        if x == 0:
            print('Succesfully')
        else:
            print('Failed')

        return x == 0

    # 创建群聊
    # chat_id必须唯一
    def create_chat(self, name, chat_id, users=["qy0132dd6bfc2ac4c89b0a89ba89", "XiaoXiZhuShou"]):
        values = {
            "name": "py接口测试",
            "owner": "qy0132dd6bfc2ac4c89b0a89ba89",
            "userlist": users,
            "chatid": chat_id
        }
        msg = (bytes(json.dumps(values), 'utf-8'))

        return msg

    def sendChat(self, msg, chat_id):

        return self.__post(self.__chat(msg, chat_id),MsgType.msg_to_chat)

    def sendMessage(self, msg, users):

        return self.__post(self.__message(msg, users),MsgType.msg_to_user)



if __name__ == '__main__':
    msg = 'test,Python调用企业微信测试'
    aggentid = '1000004'
    corpid = 'ww8e9eafab581b182c'
    corpsecret = 'kFdYRS9olP_P28_9yGLH5i2r6xsinz78GZLJUTezXHA'

    wx = QYWX(corpid, corpsecret,aggentid)
    wx.sendChat(msg, chat_id='pyg001')
    wx.sendMessage(msg,users='qy0132dd6bfc2ac4c89b0a89ba89|XiaoXiZhuShou|duanqing')
