#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'修改实例属性及方法的用例'
__author__ = '林金行'

from types import MethodType

def set_attr(self,y):
    self.y = y

class TestObject(object):
    #限制动态添加的属性，仅对当前类有用，对子类无用。
    __slot__=("x","z")
    y = ""
    def __init__(self):
        self.__len__="9"
    def fun(self):
        print("TestObject")
        pass

class ChangeInstanceInfo(object):
    def run(self):
        to = TestObject()
        #动态绑定变量
        print("#动态绑定变量")
        print("是否存在x变量："+str(hasattr(to,"x")))
        to.x = "123"
        print("添加x变量：" + str(hasattr(to, "x")))
        print("动态变量x的值："+str(to.x))
        print("删除x变量")
        del to.x
        print("是否存在x变量：" + str(hasattr(to, "x")))
        #动态绑定方法
        print("是否存在set方法：" + str(hasattr(to, "set")))
        print("添加set方法")
        to.set = MethodType(set_attr,to)
        print("是否存在set方法：" + str(hasattr(to, "set")))
        to.set("abc")
        print("动态方法使用后y的值：" + to.y)
        pass
    pass


cii = ChangeInstanceInfo()
cii.run()