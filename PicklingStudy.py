#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'序列化学习用例'
__author__ = '林金行'

import pickle,json
class car(object):
    def __init__(self,brand,type,cc):
        self.brand = brand
        self.type = type
        self.cc = cc

class PicklingStudy(object):
    d = dict(name='bob', age=12, sex='mail')
    def pick(self):
        d = self.d
        print("--对像序列化")
        p = pickle.dumps(d)
        print(p)
        print("--对像序列化存储")
        with open("F:\\Study\\Python\\Pickling.txt","wb") as wf:
            pickle.dump(d,wf)
        print("Success")
        print("--对像序列化读取")
        with open("F:\\Study\\Python\\Pickling.txt", "rb") as rf:
            rp = pickle.load(rf)
        print(rp)
    def jsons(self):
        d = self.d
        print("--对像JSON化")
        j = json.dumps(d)
        print(j)
        print("--对像JSON化存储")
        with open("F:\\Study\\Python\\Json.txt","w") as wf:
            json.dump(d,wf)
        print("Success")
        print("--对像JSON化读取")
        with open("F:\\Study\\Python\\Json.txt", "r") as rf:
            rp = json.load(rf)
        print(rp)
        print("--JSON对像转换为Python对像")
        json_str = '{"name":"bob", "age":"12", "sex":"mail"}'
        rp = json.loads(json_str)
        print(rp["age"])
        print("--类实例转换为Json对像")
        c = car("Benz","S400","V8 4.0")
        cj = json.dumps(c,default=lambda x:x.__dict__)
        print(cj)
        print("--Json对像转换为类实例")
        c = json.loads(cj,object_hook=self.dict2car)
        print(c)
    def dict2car(self,d):
        return car(d["brand"],d["type"],d["cc"])
    def run(self):
        self.pick()
        self.jsons()
        pass


ps = PicklingStudy()
ps.run()