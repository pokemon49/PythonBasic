#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#凡是可作用于for循环的对象都是Iterable类型；
#凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
from collections import Iterable,Iterator
class IterationStudy(object):
    def fib(self,max): #generator方法《生成器》
        n,a,b = 0,0,1
        while n < max:
            yield b  #<每次执行到此就返回，下次调用时再从这里执行>
            a,b = b,a+b
            n=n+1
        return "done"
    def run(self):
        d = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6}
        for key in d:
            print(key)
        #对Dict中的Value进行迭代
        for value in d.values():
            print(value)
        print("***********************")
        #同时对Key,Value进行迭代。
        for k,v in d.items():
            print(k)
            print(v)
        print("***********************")
        for st in "Python":
            print(st)
        #判断是否可以进行迭代
        print("***********************")
        print("字符串是否可以迭代：" + str(isinstance("abc",Iterable)))
        print("List是否可以迭代：" + str(isinstance(['a','b','d','e'], Iterable)))
        print("整数是否可以迭代：" + str(isinstance(21365121, Iterable)))
        print("tuple是否可以迭代：" + str(isinstance(('a','b'), Iterable)))
        print("***********************")
        #List带下标的进行迭代
        for i,v in enumerate(['a','b','d','e']):
            print(i, v)
        #双变量迭代
        for i, v in [(1,2),(3,4),(5,6),(7,8)]:
            print(i, v)
        #generator生成器，区别在于Generator是使用"()"进行声明，而其它则使用"[]"
        g = (x+x for x in range(100))
        ##访问
        m = 0
        for n in g:
           m=m+n
        print(m)
        #yield形式生成器
        g = self.fib(8)
        for n in g:
            print(n)
        #异常处理
        g = self.fib(10)
        while True:
            try:
                x = next(g)
                print("x:"+str(x))
            except StopIteration as e:  #捕获Generator结束错误
                print("Generator return value:",e.value)
                break
        #Iterable转换为Iterator:用于dict,list,str转换
        #使用iter()方法将Iterable转变为Iterator，使它们可以使用next()
        print("字符串是否进行转换Iterator：" + str(isinstance(iter("abc"), Iterator)))
        print("List是否进行转换Iterator：" + str(isinstance(iter(['a', 'b', 'd', 'e']), Iterator)))
IS = IterationStudy()
IS.run()