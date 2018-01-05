import smtplib
from email.mime.text import MIMEText
from email.header import Header

#sender = 'csuduan@126.com'
receiver = ['duanq@quantinv.com']
subject = 'test'
smtpserver = 'smtp.126.com'
username = 'quantinv@126.com'
password = 'quantfly2016'

msg = MIMEText('hahahha ','text','utf-8')#中文需参数‘utf-8’，单字节字符不需要
msg['Subject'] = Header(subject, 'utf-8')
msg['To']=";".join(receiver)
msg['From']=username

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(username, receiver, msg.as_string())
smtp.quit()  