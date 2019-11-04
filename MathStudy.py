#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
class MathStudy(object):
    a = 101
    b = 2
    c = 3
    d = 4
    e = 5
    f = True
    g = False
    def basicMath(self):
        #数学运算
        print("101 + 2=" + str(self.a + self.b))
        print("101 - 2=" + str(self.a - self.b))
        print("101 * 2=" + str(self.a * self.b))
        print("101 / 2=" + str(self.a / self.b))
        print("101 // 2=" + str(self.a // self.b)+'（地板除）')
        print("101 % 2=" + str(self.a % self.b))
        #逻辑运算
        print("True and False：" + str(self.f and self.g))
        print("True or False：" + str(self.f or self.g))
        print("Not False：" + str(not self.g))


ms = MathStudy()
ms.basicMath()