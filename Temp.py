#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'临时想法集'
__author__ = '林金行'

import queue,time
class Temp(object):
    l = []
    def mybreak(self):
        return False
    def loop(self):
        for i in range(100):
            if i == 55:
                break
            print(i)
    def wloop(self):
        con = True
        i = 1
        while con:
            i = i + 1
            if i == 10:
                con = self.mybreak()
            print(i)
            time.sleep(1)
    def test(self):
        b = {"keys":0}
        for a in range(1,10):
            b["keys"] = a
            self.l.append(b)
        return self.l
    def run(self):
        #self.loop()
        self.wloop()
    pass


t = Temp()
t.run()
print(t.test())