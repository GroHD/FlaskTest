#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
//发送邮件
'''
import smtplib,random
from email.mime.text import MIMEText
From = 'laoshou125hd@163.com'
subject='验证码'
userName = 'laoshou125hd@163.com'
userpassword='woaiwode1314.'
#发送验证邮箱的邮件
def Send_CheckedEmail(oid,email):
    To = email
    randChar =['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',
               '1','2','3','4','5','6','7','8','9','0','Q',
               'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    rand =""
    for ined in range(5):
        rd = random.Random().randint(0,(len(randChar)-1))
        rand = rand+randChar[rd]

    msg = MIMEText("<h1>MisMg 提示您:</br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;您的验证码为：["+rand+"] 有效期为30分钟</h1>",'html', 'utf-8')  # 发送html
    msg['Subject'] = subject
    msg['From'] = From
    msg['To'] = To
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        smtp.login(userName, userpassword)
        smtp.sendmail(From, To, msg.as_string())
        smtp.quit()
        return rand
    except Exception as e:
       return "0"