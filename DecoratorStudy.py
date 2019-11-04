#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

def log(text):
    if isinstance(text,str):
        def decorator(func):
            @functools.wraps(func)
            def wrap(*args,**kw):
                print("%s,%s():" % (text, func.__name__))
                func(*args,**kw)
                print('End')
                return wrap
            return wrap
        return decorator
    else:
        #@functools.wraps(text)
        def wrapper(*agrs, **kw):
            print('call %s()' % text.__name__)
            text(*agrs, **kw)
            return wrapper
        return wrapper


class DecoratorStudy(object):
    @log
    def now2(self):
        print('2018-02-03')

    @log("Execute")
    def now(self):
        print('2018-02-04')
        #显示本地名称信息
        #print(str(locals()))
        #显示全局名称信息
        #print(str(globals()))
    #静态装饰:可直接访问不需要实例化
    @staticmethod
    def static_method(msg):
        print(msg)

    def normal_method(msg):
        print(msg)
    #类装饰:所接收的第一个参数不是 self 类实例的指针，而是当前类的具体类型
    @classmethod
    def class_method(cls):
        print (repr(cls))
    #属性:通过类实例直接访问的信息???
    @property
    def var(self):
        return self._var
    @var.setter
    def var(self,var):
        self._var = var

    def run(self):
        self.now2()
        self.now()
        n1 = log('execute')(self.now)
        print(n1.__name__)
        pass


ds = DecoratorStudy()
ds.run()
print(str(locals()))
