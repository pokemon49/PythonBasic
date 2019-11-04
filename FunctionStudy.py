#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'方法定义试验'
__author__ = '林金行'

import math,functools


class FunctionStudy(object):
    name = "King"

    def show(self):
        print(self.name)
        if not 1==2 :
            print("abc")

    def null_fun(self):
        pass

    def check_par_type(self,x):
        #检查类型匹配
        if not isinstance(x,(int,float)):
            raise TypeError("bad Operand Type")

    def mulit_return(self,x,y,step,angle=0):
        rx = x + step * math.cos(angle)
        ry = y + step * math.cos(angle)
        return rx,ry

    def quadratic(self,a,b,c):
        if a == 0:
            raise ArithmeticError("a is 0")
        if b ** 2 - 4 * a * c < 0:
            raise ArithmeticError("Match Error")
        x1 = ((-b + math.sqrt(b ** 2 - 4 * a * c)) / 2 * a)
        x2 = ((-b - math.sqrt(b ** 2 - 4 * a * c)) / 2 * a)
        return x1,x2

    #参数默认值
    def default_value(self,x,y=5):
        s=1
        while y > 0:
            y=y-1
            s=s*x
        return s

    #默认参数BUG，默认参数需要使用不可变的对像。
    def defalut_value(self,l=None):
        if l is None:
            l = []
        l.append("end")
        return l
    #可变参数(作为一个List或是tuple传入函数，List和Tuple对像也可以在调用方法时前加面*整体作为可变参数进入函数)
    def change_par(self,*num_list):
        sum = 0
        for n in num_list:
            sum = sum+n
        return sum

    #关键参数（传入的参数作为Dict类型），Dict类型在调用函数时，可以通过前置**来直接作为关键参数传入
    def key_par(self,name,age,sex,**other):
        print("NAME:",name,"AGE",age,"SEX",sex,"OTHER:",other)

    #命名关键字参数（*之后即为关键参数） --限制关键字参数的名称，调用时必须使用参数名称。
    def name_key(self,name,age,*,sex,job):
        print("NAME:",name,"AGE",age,"SEX",sex,"Job:",job)

    #复合参数
    def mulit_par1(self,a,b,c=0,*,d,e,**kw):
        print('复合参数测试1：a=',a,'b=',b,'c=',c,'d=',d,'e=',e,'kw:',kw)

    def mulit_par2(self, a, b, *args, **kw):
        print('复合参数测试2：a=', a, 'b=', b, 'args=', args, 'kw:', kw)

    #递归函数
    def fact(self,x):
        if x == 1:
            return x
        #print(str(x) + "*" + str(x-1) + str(x*(x-1)))
        return x * self.fact(x-1)
    #尾递归函数:在函数返回的时候，调用自身本身，并且，return语句不能包含表达式,使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。

    def fact2(self,x):
        return self.fact2_iter(x,1)

    def fact2_iter(self,x,num):
        if x == 1:
            return num
        return self.fact2_iter(x - 1,x * num)
    #偏函数 为一些函数设置好一些固定参数值，方便调用
    int2 = functools.partial(int,base=2)
    max10 = functools.partial(max,10)

    def run(self):
        print("方法的声明:")
        self.show()
        print("参数类型匹配:")
        print(self.check_par_type(7))
        print("多返回结果:")
        print(self.mulit_return(70,80,math.pi/6))
        print("多返回结果练习（一元二次方程的解：")
        print("一元二次方程解："+str(self.quadratic(3,-5,-7)))
        print("默认参数学习：")
        print(self.default_value(x=99,))
        print("默认参数的陷阱：")
        print(self.defalut_value())
        print("可变参数：")
        nums = [7, 8, 56, 8, 9, 561, 8, 9, 5]  # list或tuple作为参数传入可变参数时，前加*即可。
        print(self.change_par(*nums))
        print("限定范围的可变参数：")
        print(self.name_key("Zhao","25",sex="Male",job="Designer"))
        print("Dict参数：")
        print(self.key_par("Zhou","25","Male",Country='China',Place="SiChuan"))
        print("复合参数组测试：")
        self.mulit_par2(1, 2)
        self.mulit_par2(1, 2, c=7)
        self.mulit_par2(1, 2, 3, 'a', 'b', 'c')
        self.mulit_par2(1, 2, 'a', 'b', 'd', x="8799")
        self.mulit_par2(1, 2, x="7895", y="95612")
        args = (1, 2, 3, 4)
        kw = {'cc': 1612, "Havle": 66}
        self.mulit_par2(1, 2, *args, **kw)
        self.mulit_par1(75, 33, 55, d=89, e=123, CHANGAN="86")
        print("递归函数学习：")
        print(str(self.fact(10)))
        print("尾递归函数学习（防止栈溢出）：")
        print(self.fact2(100))
        print("偏函数学习：")
        print(self.int2('10010010010000'))
        print(self.max10(1, 2, 3, 4, 5))


vf = FunctionStudy()
vf.run()

