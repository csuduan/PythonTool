import itchat
#-----------------
#基于itchat的微信自动收发消息程序
#API: http://itchat.readthedocs.io/zh/latest/
#-----------------


itchat.auto_login(True)
#itchat.run()

#itchat.send('Hello, filehelper', toUserName='filehelper')

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    return msg['Text']


user=itchat.search_friends(name='瘦瘦')
print(user)
#itchat.send('hahaha', toUserName=user[0].UserName)

group=itchat.search_chatrooms(name='甩肉见世面[机智]')
#itchat.send('hahaha', toUserName=group[0].UserName)
print(group)


#itchat.run()