#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'异常处理'
__author__ = '林金行'

class MyException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg