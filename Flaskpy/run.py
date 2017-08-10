#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:HD
'''
from app import  app
app.run(debug=True,host='192.168.10.254' )

r'''
    导出项目所需要的包
    pip freeze >requirements.txt
    导入项目所需要的包
    pip install  -r requirements.txt
    
'''