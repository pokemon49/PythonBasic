#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'命令行输入操全实例'
__author__ = '林金行'
class InputStudy(object):
    def run(self):
        #记录录入信息
        age = input("请输入您的年龄：")
        age = int(age)
        #打印记录内容
        if age >= 18:
            n = "adult"
        elif age >= 6:
            n = "teenager"
        else:
            n = "kid"
        print (n+':'+str(age))

IS = InputStudy()
IS.run()
