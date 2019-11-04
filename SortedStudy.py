#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from operator import itemgetter
class SortedStudy(object):
    def run(self):
        l = [-1,23,-12,44,1,21,6,-89]
        #一般排序
        l1 = sorted(l)
        #带函数排序
        l2 = sorted(l,key=abs)
        sl = ["java","C++","Python","Html5","Javascript","CSS"]
        sl1 = sorted(sl)
        sl2 = sorted(sl,key=str.lower)
        #反向排序
        l3 = sorted(l1,reverse=True)
        ll = [("Anii",11),("July",64),("Babi",94),("Sunni",19),("Jifuni",24)]
        #指定子元素排序
        ll1 = sorted(ll,key=itemgetter(0))
        ll2 = sorted(ll,key=itemgetter(1))
        #显示
        print(l1)
        print(l2)
        print(l3)
        print(sl1)
        print(sl2)
        print(ll1)
        print(ll2)
    pass

ss = SortedStudy()
ss.run()