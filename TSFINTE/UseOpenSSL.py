#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'OPENSSL加密、解密过程'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

from Crypto.Cipher import AES
from binascii import hexlify, unhexlify


class UseOpenSSL(object):
    # 从前边文件中读取出加密的内容
    file_in = open(r'E:\Object\Python\ABS\index0.ts', "rb")
    key = unhexlify('2DF08BF441EB01D13A72F47AE296ED66')
    iv = unhexlify('e58eb5e0619148be89cfdfffa9906c6e')

    encrypted_data = []
    for x in (16, AES.block_size, -1):
        encrypted_data = encrypted_data + [file_in.read(x)]

    # 实例化加密套件
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #初始化输出内容
    data = b''
    for ed in encrypted_data:
        data = data + cipher.decrypt(ed)

    with open(r'E:\Object\Python\ABS\result.ts', 'wb') as wf:
        wf.write(data)
    file_in.close()