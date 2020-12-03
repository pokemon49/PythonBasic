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
    file_in = open(r'E:\My Document\Downloads\Merger\200725132919.ts', "rb")
    key = unhexlify('3E010C4C5823555982B35665543F5C7C')
    iv = unhexlify('e0cc57682fad374b45584065de37c86e')
    '''
    encrypted_data = []
    for x in (16, AES.block_size, -1):
        encrypted_data = encrypted_data + [file_in.read(x)]

    print(len(encrypted_data))

    # 实例化加密套件
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #初始化输出内容
    data = b''
    for ed in encrypted_data:
        data = data + cipher.decrypt(ed)
    '''
    encrypted_data = file_in.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(encrypted_data)
    with open(r'E:\JUL-268.ts', 'wb') as wf:
        wf.write(data)
    file_in.close()