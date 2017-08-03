#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
import os
PERMANENT_SESSION_LIFETIME = 1800 #设置session的过期时间
SQLALCHEMY_COMMIT_ON_THARDOWN = True #自动提交数据
SCRF_ENABLED = True # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
SECRET_KEY="my_block_blog_guess" #ECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单。当你编写自己的应用程序的时候，请务必设置很难被猜测到密钥。
#配置数据库
basedir = os.path.abspath('.')
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'db\\app.db')

