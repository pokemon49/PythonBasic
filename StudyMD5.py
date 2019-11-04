#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'MD5加密学习'
__author__ = '林金行'
import hashlib

string = "password"
md = hashlib.md5()
md.update(string.encode())
print(md.hexdigest())