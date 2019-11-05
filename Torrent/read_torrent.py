#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'读取torrent文件'
__author__ = '林金行'

import os
from bencode import bdecode,bencode
import hashlib,base64
class BTFormatError(BaseException):
    pass

class TorrentFile(object):
    _metaininfo = {}
    _file_name = ''

    def read_file(self,filename):
        if os.path.exists(filename):
            if (os.path.isfile(filename) and os.path.splitext(filename)[1].lower() == ".torrent"):
                torrent_file = open(filename,'rb')
                data = torrent_file.read()
                torrent_file.close()
                self.take_magnet(data)
            else:
                print("不是torrent文件或文件后缀名不正确！")
        else:
            print("文件不存在，请查检文件地址！")

    def take_magnet(self,data,type = 0):
        #格式化种子文件
        magenta_source = bdecode(data)
        #反格式化种子文件的"Info"部份进行BTIH(BitTorrent Info Hash)运算
        magent_info = bencode(magenta_source['info'])
        #对Info信息进行SHA1的编码
        digest = hashlib.sha1(magent_info).digest()
        #对INFO信息进行base32转码,获得32位原始BTIH<可用于utorrent等软件>
        b32hash = base64.b32encode(digest)
        b32hash = str(b32hash,"utf-8")
        magent_url_32 = "magnet:?xt=urn:btih:" + b32hash
        print(magent_url_32)
        #对INFO信息进行base32转码,获得40位BTIH<可用于网盘离线下载>
        b16Hash = base64.b16encode(digest)
        b16Hash = b16Hash.lower()
        b16Hash = str(b16Hash, "utf-8")
        magent_url_40 = "magnet:?xt=urn:btih:"+b16Hash
        print(magent_url_40)
        print(magenta_source["info"].keys())
        print(magenta_source["info"]["name"].decode("UTF8"))
        if "length" in magenta_source["info"]:
            print(magenta_source["info"]["length"]/1024/1024,"MB")
        if "files" in magenta_source["info"]:
            for file in magenta_source["info"]["files"]:
                print(print(file["path"][0].decode("utf-8")),file["length"]/1024/1024,"MB")
        '''
        if metainfo and type(metainfo) == type({}):
            self._metaininfo = metainfo
            self._file_name = filename
        else:
            raise BTFormatError()
        '''
        if type == 1:
            return magent_url_32
        else:
            return magent_url_40
    pass

tf = TorrentFile()
tf.read_file("E:\Study\Python\Files\Test.torrent")