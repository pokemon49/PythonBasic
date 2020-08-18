#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'系统(OS)操作学习实例'
__author__ = '林金行'


import os,sys,time

class osstudy():
    # 文件操作
    def fileop(self):
        path = 'E:\\'
        file_path= path +'对比度测试.png'
        #file_path= 'F:\\H6.rar'
        # 获取文件名
        print('--获取文件名')
        file_size = os.path.basename(file_path)
        print(file_size)
        # 获取文件大小
        print('--获取文件大小')
        file_size = os.path.getsize(file_path)
        print(file_size)
        #折分文件及路径
        print('--折分文件及路径')
        print(os.path.split(file_path))
        #折分文件路径和扩展名
        print('--折分文件路径和扩展名')
        print(os.path.splitext(file_path))
        #获取当前决对路径
        print('--获取当前决对路径')
        tp = os.path.abspath('.')
        tp = os.getcwd()
        print(tp)
        print('--组合路径')
        tp = os.path.join(tp,'testdir')
        print(tp)
        print('--建立文件夹')
        print(os.mkdir(tp))
        print('--删除文件夹')
        print(os.rmdir(tp))
        #获取目录文件列表
        print('--获取目录文件列表')
        file_list = os.listdir(path)
        print(file_list.__len__())
        #for file in file_list:
        #    print(file)
        # 获取文件信息
        print('--获取文件信息')
        file_attr = os.stat(file_path)
        print(file_attr.st_size)
        print('--文件创建')
        tp = 'F:\\Study\\python\\text.txt'
        ttp = 'F:\\Study\\python\\test.py'
        f = open(tp,'w')
        f.write('a')
        f.close()
        print('--文件重命名')
        os.rename(tp,ttp)
        print('--文件删除')
        os.remove(ttp)
    #系统操作
    def osop(self):
        #获取系统信息（非Windows系统才有）
        #os.uname()
        #获取环境变量
        print('--获取环境变量')
        print(os.environ)
        print(os.environ.get('path'))
    #输出操作
    def out(self):
        i = 1
        while True:
            i = i + 1
            if i%2 == 0:
                c = "\\"
            else:
                c = "/"
            sys.stdout.write("\r")
            sys.stdout.write("#"* i +c)
            sys.stdout.flush() ##随时刷新到屏幕上
            time.sleep(0.5)
            if i == 10: break
    #运行
    def run(self):
        print('-文件操作')
        self.fileop()
        print('-系统操作')
        self.osop()
        print('--输出操作')
        self.out()


oss = osstudy()
oss.run()

import re

class OSexec():
    ftree = ([])
    def filelist(self,path):
        self.ftree = ([])
        if os.path.isfile(path):
            print(path+' is File')
        else:
            self.treelist(path)
        return self.ftree

    def treelist(self,path):
        for m in os.listdir(path):
            if os.path.isfile(path+'\\'+m):
                self.ftree.append(os.path.split(path+'\\'+m))
            else:
                self.treelist(path+'\\'+m)
        pass
    def run(self):
        t = self.filelist("G:\\新建文件夹")
        print(t)
        d = [x for x in self.filelist("G:\\games\\World_of_warships") if str(x[1]).find("global.mo") >= 0]
        for dd in d:
            print(dd)


o = OSexec()
o.run()

