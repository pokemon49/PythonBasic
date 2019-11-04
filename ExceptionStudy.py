#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'异常学习实例'
__author__ = '林金行'
#调用日志记录
import logging
def foo(s):
     return 10 // int(s)

def bar(s):
    return foo(s) * 2

def main():
    #错误可以在适当的地方捕获处理。
    try:
        bar(0)
    #捕获错误的父类就不会再捕获其子类
    except Exception as e:
        #使用logging记录错误后，程序会继续执行
        logging.exception(e)

main()
print('End')