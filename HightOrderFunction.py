#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
class HightOrderFunction(object):
    #简单的高阶函数
    def add(self,x,y,f):
        return f(x)+f(y)
    def run(self):
        #系统函数命名
        f = abs
        print(f(-10))
        #系统函数重定义,若要其它模块也同样修改则使用__builtin__.abs = 10
        #abs = 10
        #高阶函数应用
        print(self.add(6,7,abs))
        #匿名函数
        ride = lambda x, y, z : z(x) * z(y)
        print(ride(7,5,math.sqrt))


HOF = HightOrderFunction()
HOF.run()
