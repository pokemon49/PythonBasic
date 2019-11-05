#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'IO操作学习实例'
__author__ = '林金行'

#文件读写操作
class FileIOStudy(object):
    def run(self):
        of = open("F:\\Study\\Python\\USER-AGENT.txt",'rb') #r:读取 b:字节
        print(of.read())
        print(of.readline())  #读取一行
        of.close()
        #免close写法。
        with open("F:\\Study\\Python\\USER-AGENT.txt",'r',encoding='gbk',errors='ignore') as ofr: #encoding指定打开编码,errors错误处理方式'ignore':忽略
            print(ofr.read(1024)) #按字节大小读取
            print(ofr.readlines())  # 按行读取，返回一个List
        with open('F:\\Study\\Python\\WriteFile.txt','w') as wf:
            print(wf.write("Hello Python"))
    pass

fis = FileIOStudy()
fis.run()


#内存读写操作
from io import StringIO,BytesIO
class MemoryIOStudy():
    def strio(self):
        f = StringIO()
        print("--内存字符流处理")
        f.write("ABC"+chr(10))
        f.write("Hello Python"+chr(10))
        f.write('Hi,Study Python!')
        print(f.getvalue())#获取所有值
    def bio(self):
        b = BytesIO()
        print("--内存字节流处理")
        b.write(b'ABC\n' )
        b.write(b'Hello Python\n')
        b.write(b'Hi,Study Python!\n')
        print(b.getvalue())  # 获取所有值
    def run(self):
        print("--内存读写操作")
        self.strio()
        self.bio()
    pass


mios = MemoryIOStudy()
mios.run()