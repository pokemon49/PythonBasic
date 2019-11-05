#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'解码Torrent文件的基础方法'
__author__ = '林金行'

#程序调用入口
def bdcode(data):
    #序列化数据
    data = list(data)
    return _read_chunk(data)

def _read_chunk(data):
    chunk = None
    if len(data) == 0:
        return chunk
    leading_chr = str(data[0])

    if leading_chr.isdigit():
        chunk = _read_string(data)
    elif leading_chr == 'd':
        chunk = _read_dict(data)
    elif leading_chr == 'i':
        chunk = _read_integer(data)
    elif leading_chr == 'l':
        chunk = _read_list(data)

    return chunk

def _read_dict(data):
    if len(data) == 0  or data.pop(0) != 'd':
        return None
    chunk  ={}
    while len(data) > 0 and data[0] != 'e':
        key = _read_chunk(data)
        value = _read_chunk(data)
        if key and value and type(key) == type(''):
            chunk[key] = value
        else:
            return None
    pass

def _read_list(data):
    if len(data) == 0  or data.pop(0) != 'l':
        return None
    chunk = []
    while len(data) > 0 and data[0] != 'e':
        value = _read_chunk(data)
        if value:
            chunk.append(value)
        else:
            return None
    return chunk

def _read_string(data):
    str_len=''
    if len(data) == 0  or str(data[0]).isdigit():
        str_len += str(data.pop(0))
    if len(data) == 0  or data.pop(0) != ':':
        return None
    str_len = int(str_len)
    if str_len > len(data):
        return None
    value = data[0:str_len]
    return ''.join(value)

def _read_integer(data):
    integer = ''
    if len(data)< len('i2e') or data.pop(0) != 'i':
        return None

    sign = data.pop(0)
    if sign != '-' and not sign.isdigit():
        return None
    integer += sign

    while len(data) > 0 and data[0].isdigit():
        integer += data.pop(0)

    if len(data) == 0 or data.pop(0) != 'e':
        return  None
    return int(integer)
