#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'Moviepy学习用例'
# 'Version 1.0'
# '1.0 20200101 初始版本创建'
__author__ = '林金行'

from moviepy.editor import VideoFileClip

file_path = r'E:\Study\Python\ABS\index0.ts'
try:
   clip = VideoFileClip(file_path)
   print(clip.duration)
except IndexError as err:
    print("视频文件错误")

except Exception as err:
    print(err)