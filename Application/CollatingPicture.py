#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from CopyFunction import *
import threading
'图片整理方法'
__author__ = '林金行'

class CollatingPicture(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.CF = CopyFunction("1","2")
    def ControlCenter(self,path):
        p = path
        tree = self.CF.take_tree(p,subdir=False)
        for f in tree:
            fi = os.path.split(f)
            tp = fi[0]
            tf = fi[1]
            nd = tp+"\\\\"+tf[0]
            self.CF.copy_dir(source="Null",target=nd)
            nf = nd+"\\\\"+tf
            self.CF.copy_file(f,nf,type=1)
        pass
    def run(self):
        self.ControlCenter("G:\\Media\\vadio\\uncensored")
        pass
    pass

cp = CollatingPicture()
cp.run()