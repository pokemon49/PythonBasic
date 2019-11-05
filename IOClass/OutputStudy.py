#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'输出方法示例'
__author__ = '林金行'

class OutputStudy(object):
    def Normal(self):
        print("This is Basic CLO（Command Line Output）")
        #多重输出
        print("This's Mulit Element Output:","A","B","C","D")
    def run(self):
        self.Normal()
        pass
    pass

OS = OutputStudy()
OS.run()