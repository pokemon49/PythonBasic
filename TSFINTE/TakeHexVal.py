#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '获取文件HEX值'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

import os
import argparse

class TakeHexVal():
    # 参数获取
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.description = '请输入需解析文件路径!'
        parser.add_argument('-f', '--filePath', help='输入文件地址', dest='File_Path', type=str, default="0")
        args = parser.parse_args()
        self.file_path = args.File_Path


    # 文件判断处理
    def isfile(self, fp):
        print(fp)
        if not os.path.exists(fp):
            raise Exception('文件不存在，请输入有效的文件地址！')
        if os.path.getsize(fp) > 16:
            raise Exception('输入文件过大，请不要超过16B')
        return True
        pass

    # 获取Hex值
    def gethexval(self, file_path):
        HexVal = ''
        n = 0
        while 1:
            s = file_path.read(1)
            if not s:
                break
            byte = ord(s)
            HexVal = HexVal + '%02x' % byte
            if n % 16 == 0:
                HexVal == HexVal + chr(16)
        return HexVal.upper()
    # 程序入口主调用方法
    def run(self):
        if self.isfile(self.file_path):
            f = open(self.file_path, 'rb')
            hexval = self.gethexval(f)
            print(hexval)
            f.close()
    pass

th = TakeHexVal()
th.run()