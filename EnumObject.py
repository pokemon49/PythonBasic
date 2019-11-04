#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'枚举类用例'
__author__ = '林金行'
from enum import Enum,unique
#自定义枚举
@unique  #确保不重复
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

class EnumObject(object):
    #自排例枚举值
    Date = Enum('Month',('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
    def run(self):
        for name,member in self.Date.__members__.items():
            print(name,'=>',member,',',member.value)
        for name,member in Weekday.__members__.items():
            print(name, '=>', member, ',', member.value)
        #其它访问方法：
        print("Date.Jan:"+str(self.Date.Jan))
        print("Date[Feb]:" + str(self.Date['Feb']))
        print("Weekday[Wed].value:" + str(Weekday['Wed'].value))
        pass

eo = EnumObject()
eo.run()


