#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import reduce
class MapReduceStudy(object):
    p = x = 0
    def sqare(self,x):
        return x*x
    def sqare2(self,x,y):
        return x*y
    def strtransnum(self,x):
        def chanmapint(n):
            return {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,".":10}[n]
        def trnasformation(x,y):
            self.x = self.x + 1
            if self.p == 0 :
                if y == 10:
                    self.p = self.x
                    return x
                else:
                    return x * 10 + y
            else:
                return x + y*(0.1**(self.x-self.p))
        #return reduce(lambda x,y:x*10+y,map(chanmapint,x))
        return reduce(trnasformation, map(chanmapint, x))
    def normalize(self,name):
        if isinstance(name,(str)):
            return name.capitalize()
    def run(self):
        #Map
        l = list(range(1,10))
        m = map(self.sqare,l)
        l1 = ['adam', 'LISA', 'barT']
        l2 = list(map(self.normalize,l1))
        print(list(m))
        print(l2)
        #Reduce
        r = reduce(self.sqare2,l)
        print(r)
        print(self.strtransnum("112312.23431"))
        pass



mrs = MapReduceStudy()
mrs.run()