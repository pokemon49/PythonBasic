#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '练习集合'
__author__ = '林金行'

import math


class Exercise(object):

    def number_system(self):
        n = 123456789
        #转换为十六进制
        n16 = hex(n)
        print("使用hex将%d转换为%s" % (n,n16))

    def quadratic(self,a,b,c):
        def power(b,n=2):
            r = 1
            while n >0:
                n = n - 1
                r = r * b
            return r
        if a==0 :
            raise 'a Must Don''t equar to Zero  '
        d = power(b)-4*a*c
        if d < 0:
            raise 'derta Must grater than Zero'
        if a != 0 and d >=0 :
            x1 = (-b + math.sqrt(d)) / 2 * a
            x2 = (-b - math.sqrt(d)) / 2 * a
            return x1,x2
        pass

    def Tower_of_hanoi(self,n,a,b,c):
        if n == 1:
            print('Move:',a,'-->',c)
        else:
            self.Tower_of_hanoi(n-1,a,c,b) #将n-1个盘子从a移动到b,以c做为辅助
            self.Tower_of_hanoi(1,a,b,c)   #将a上的最后一个盘子移动到c
            self.Tower_of_hanoi(n-1,b,a,c) #将n-1个盘子从b移动到c，以a作为辅助

    def triangles(self):
        ret = [1]
        while True:
            yield ret
            for i in range(1, len(ret)):
                ret[i] = pre[i] + pre[i-1]
            ret.append(1)
            pre = ret[:]

    def run(self):
        self.number_system()
        r1,r2 = self.quadratic(3,9,3)
        print ("一元二次方程结果：x1:%f ,x2:%f" % (r1,r2))
        print ("汉诺塔结果：")
        print(self.Tower_of_hanoi(3,'A','B','C'))
        # 杨辉三角形
        print("杨辉三角形")
        n = 0
        for t in self.triangles():
            print(t)
            n = n+1
            if n ==10 :
                break
        pass


dtf = Exercise()
dtf.run()