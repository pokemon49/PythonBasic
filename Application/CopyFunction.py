#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'拷贝文件方法'
__author__ = '林金行'

import os,threading,sys,time
from MyException import *

class CopyFunction(threading.Thread):
    control = 0
    def __init__(self,source,target):
        threading.Thread.__init__(self)
        self.source = source
        self.target = target
    #运行状态显示
    def show_status(self,target=None,source=None,state=0,sech=0):
        if state == 0 :
            print(target+" --文件移动完成！")
        if state == 1 :
            print("\n")
            print(source+" --文件未移动！")
        if state == 3 :
            print("\n")
            print("正在将\""+source+"\"移动至\""+target+"\"")
        if state == 4 :
            sys.stdout.write('\r')
            sys.stdout.write("#" * sech + str(sech) + "%")
            sys.stdout.flush()
        pass
    #文件拷贝
    def copy_file(self,source,target,type=0,process_bar=False):
        s = open(source,"rb")
        t = open(target,"wb")
        c = True
        size = int(os.path.getsize(source)/100)
        i = 1
        self.show_status(target,source,3)
        while c:
            rs = s.read(size)
            if not rs:
                break
            else:
                t.write(rs)
                if process_bar:
                    self.show_status(state=4,sech=i)
            if self.control == "S":
                os.system("pause")
                self.control = 0
                c = True
                pass
            if self.control == 'E':
                c = False
                t.close()
                time.sleep(0.5)
                os.remove(target)
            i = i + 1
        if c == True:
            self.show_status(target,0)
        else:
            self.show_status(target,source,1)
        if type == 1:
            t.close()
            s.close()
            os.remove(source)
        pass
    #目录拷贝
    def copy_dir(self,source,target):
        exists = os.path.exists(target)
        if not exists:
            os.makedirs(target,exist_ok=True)
        pass
    #获取目录树状结构
    def take_tree(self,dir,treelist=None,subdir=True):
        list = os.listdir(dir)
        if not treelist:
            treelist =[]
        for l in list:
            f = dir+"\\"+l
            if os.path.isfile(f):
                treelist.append(f)
            elif subdir:
                treelist.append(f)
                self.take_tree(f,treelist)
        return treelist
        pass
    #拷贝主调用程序
    def copy_main(self,source,target):
        std = os.path.isdir(source)
        stf = os.path.isfile(source)
        ttd = os.path.isdir(target)
        ttf = os.path.isfile(target)
        #异常情况处理
        if ttf:
            cover = input("目标是文件确定要覆盖么？(1:覆盖,0:不覆盖)")
            if cover == 1:
                os.remove(target)
                target = os.path.split(target)[0]
        if ((std and stf)) or ((ttd and ttf)):
            raise MyException("输入\输出文件异常！")
        if std:
            stree = self.take_tree(source)
        if stf and ttd:
            self.show_status(target,source,3)
            file = os.path.split(source)
            file = file[1]
            target_file = target+file
            self.copy_file(source,target_file)
            pass
        pass
    def run(self):
        self.copy_main(self.source,self.target)
        #self.copy_file(self.source,self.target)
        pass
    pass

#cf = CopyFunction("G:\\【無量壽經】讀誦(木魚)悟行法師領眾讀誦 _标清.flv","F:\\")

#cf.run()
