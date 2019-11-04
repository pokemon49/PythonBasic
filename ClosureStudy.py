#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#团包
class ClosureStudy(object):
    def cnt(self):
        def g(j):
            return lambda : j * j
        fs=[]
        for i in (range(1,7)):
            fs.append(g(i))
        return fs
    def fun_outer(self):
        var = "var at Outer"
        unuse_var = "this var is not use in Inner"
        print("Outer var : %s "  % var)
        print("Outer var local : %s " % str(locals()))
        print("Outer var id: %s " % str(id(var)))
        def fun_inner():
            print("Inner var : %s " % var)
            print("Inner var local : %s " % str(locals()))
            print("Inner var id: %s " % str(id(var)))
        return fun_inner
    def run(self):
        f1,f2,f3,f4,f5=self.cnt()
        #匿名函数
        la = lambda x : x + x
        print(f1())
        print(f2())
        print(f3())
        print(f4())
        print(f5())
        print(la(5))
        print(self.cnt.__name__)
        #闭包
        self.fun_outer()()

        pass



cs = ClosureStudy()
cs.run()