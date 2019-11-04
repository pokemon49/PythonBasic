#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'时间控制测试脚本'
__author__ = '林金行'

import random,datetime,time

class TimeControl():
    now = 0
    next = datetime.datetime.now() + datetime.timedelta(minutes=2)
    def MatchTime(self):
        rs = random.randint(1, 4)
        time.sleep(rs)
        self.now =datetime.datetime.now()
        if self.now >= self.next:
            print("sleeping...")
            print(self.now - self.next)
            rm = random.randint(5, 10)
            sleeptime = rm * 60
            time.sleep(sleeptime)
            self.now = datetime.datetime.now()
            self.next = self.now + datetime.timedelta(minutes=1)
            print("Start...")
        pass

    def run(self):
        while True:
            print("A:"+str(self.now))
            self.MatchTime()
        pass



tc = TimeControl()
tc.run()