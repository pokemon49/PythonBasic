#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'过滤器试验用例'
__author__ = '林金行'

class FilterTest(object):
    def Original_List(self):
        n = 1
        while True:
            n = n + 3
            yield n
    def Filter_Condition(self,n):
        return lambda x:x%n == 0
    def Core_List(self):
        ol = self.Original_List()
        while True:
            q = next(ol)
            yield  q
            ol =filter(self.Filter_Condition(q),ol)

    def run(self):
        for n in self.Core_List():
            print(n)
            if n > 100:
                break
    pass

ft = FilterTest()
ft.run()