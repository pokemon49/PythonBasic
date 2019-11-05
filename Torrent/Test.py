#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''
__author__ = '林金行'

import magneturi

import base64

import sys

torrentname = 'E:\Study\Python\Files\Test.torrent'

mangetlink = magneturi.from_torrent_file(torrentname)

ch = ''
n = 20
b32Hash = n * ch + mangetlink[20:mangetlink.find("&")]
print(b32Hash)

#print (b32Hash)

b16Hash = base64.b16encode(base64.b32decode(b32Hash))

b16Hash = b16Hash.lower()

b16Hash = str(b16Hash,"utf-8")

print ("40位info hash值："+'\n'+b16Hash)

print ("磁力链："+'\n'+"magnet:?xt=urn:btih:"+b16Hash)
