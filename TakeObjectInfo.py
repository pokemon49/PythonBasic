#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'获取对像信息'
__author__ ='林金行'

def set_attr(self,y):
    self.y = y

class TestObject(object):
    y = ""
    def __init__(self,name):
        self.__len__="9"
        self.name = name
    #实例本身的方法
    def __call__(self):
        print("Instance Name is %s" % self.name)
    def fun(self):
        print("TestObject")
        pass

class fib(object):
    def __init__(self):
        self.a,self.b =0,1
    #类返回一个序列
    def __iter__(self):
        return self
    #定义下一个值的规则
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100000:
            raise StopIteration()
        return self.a
#不可以与__iter__,__next__同时使用。
class fib2(object):
    #定义获取值
    def __getitem__(self, item):
        if isinstance(item,int):
            a,b = 0,1
            for x in range(item):
                a, b = b, a+b
            return a
        if isinstance(item,slice):
            start = item.start
            end = item.stop
            if start is None:
                start = 0
            a , b = 0 , 1
            l = []
            for x in range(end):
               if x >= start:
                   l.append(a)
               a, b = b , a+b
            return l
    #__setitem__,设置序列值
    #__delitem__,删除序列值

class TakeObjectInfo(object):
    #配置实例变量
    def __init__(self,name):
        self.name = name
    #配置实例名称(用户看)
    def __str__(self):
        return 'TakeObjectInfo Object: %s' % self.name
    # 实例名称(开发者看) __repr__
    ##统一用户及开发者查看类基本信息
    __repr__ = __str__
    def fn(self):
        pass
    def run(self):
        #判断类型
        print("--判断类型")
        print(type(3))
        print(type('abc'))
        ##比较类型
        print("--比较类型")
        print("'abc'是否字符串："+str((type('abc')==str)))
        print("'abc'是否数字：" + str((type('abc') == int)))
        print("'abc'是否方法：" + str((type('abc') == type(self.fn()))))
        #isinstance
        print("--实例判断")
        print("'abc'是否数字：" + str((isinstance('abc',int))))
        # 获取对像的属性和方法
        print("--获取对像的属性和方法")
        fl = dir(int)
        print("Int类型的对像和方法")
        for f in fl :
            print("".center(4," ")+f)
        #hasattr\setattr\getattr
        print("--判断、添加、修改、获取对像属性")
        s = TestObject("ABB")
        print("'TestObject'是否存在属性x:" + str(hasattr(s,"x")))
        print("'TestObject'是否存在属性__len__:" + str(hasattr(s, "__len__")))
        #添加、修改属性
        setattr(s, "x",11)
        print("再看'TestObject'是否存在属性x:" + str(hasattr(s, "x")))
        print("获取'TestObject'是否存在属性x:" + str(getattr(s, "x")))
        print("获取'TestObject'不存在的属性:" + str(getattr(s, "y",404)))
        #对像调用
        f = getattr(s,"fun")
        f()
        #序列类的实现
        print("--序列类的实现")
        for n in fib():
            print(n)
        f = fib2()
        print(f[10])
        print(f[10:20])
        pass



toi = TakeObjectInfo("Test")
toi.run()
to  = TestObject("ABC")
#callable判断对像是否可以被调用
print("__call__对像是否可以被调用："+str(callable(to)))