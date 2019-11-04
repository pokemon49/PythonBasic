#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'程序调试学习样例'
__author__ = '林金行'
#命令行调试
##python3 -m pdb err.py
import logging,pdb
#调整日志参数
logging.basicConfig(level=logging.INFO)
def fun(s):
    n = int(s)
    print('>>>n = %d' % n)
    #设置断点
    pdb.set_trace()
    #logging
    logging.info('n = %d' % n)
    #断言
    assert n != 0,'n is Zero'

    return 10 / n

def run():

    fun(0)

run()
