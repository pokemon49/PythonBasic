#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'快速排序算法实例'
__author__ = '林金行'

class SpeedOrder(object):
    main_list = []
    def Order(self,data=[],):
        if isinstance(data,list) and data != []:
            self.main_list=data

    pass

so = SpeedOrder
l = [4,1]
l1 = so.Order(so,l)
print(l1)