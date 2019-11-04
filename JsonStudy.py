#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'Json学习案例'
__authon__ = '林金行'
import json
class JsonStudy():
    jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
    text1 =json.dumps(jsonData)
    #text2 = json.load(text1)
    print(text1)
    pass