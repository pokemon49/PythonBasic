#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '二进制和 ASCII 码互转方法的学习'
# 'binascii模块包含很多在二进制和二进制表示的各种ASCII码之间转换的方法。 通常情况不会直接使用这些函数，而是使用像uu，base64或
#  binhex这样的封装模块。为了执行效率高，binascii 模块含有许多用 C 写的低级函数，这些底层函数被一些高级模块所使用。'
# 'Version 1.0'
# '1.0 20200817 初始版本创建'
__author__ = '林金行'
import binascii as bs

# UU编码转换
# #将单行 uu 编码数据转换成二进制数据并返回。
# #@uu 编码每行的数据通常包含45 个（二进制）字节，最后一行除外。每行数据后面可能跟有空格。
bs.a2b_uu('17CD')

# #将二进制数据转换为 ASCII 编码字符,返回值是转换后的行数据，包括换行符。data的长度最多为45。
# #@在3.7版增加backtick，如果 backtick为ture，则零由 '`' 而不是空格表示。
data = b''
bs.b2a_uu(data, backtick=False)

# base64编码转换
# #将 base64 数据块转换成二进制并以二进制数据形式返回。一次可以传递多行数据。
bs.a2b_base64('ABCD')
# #将二进制数据转换为一行用base64编码的ASCII字符串。返回值是转换后的行数据
# #@在3.6版增加newline，如果newline为true，则返回值包括换行符。
bs.b2a_base64(data, newline=True)

# 打印数据转换
# #将一个引号可打印的数据块转换成二进制数据并返回。一次可以转换多行。
# #@如果可选参数 header 存在且为true，则数据中的下划线将被解码成空格。
bs.a2b_qp(data, header=False)
# #将二进制数据转换为一行或多行带引号可打印编码的ASCII字符串。返回值是转换后的行数据。
# #@如果可选参数 quotetabs 存在且为True，则对所有制表符和空格进行编码。
# #@如果可选参数 istext 存在且为True，则不对新行进行编码，但将对尾随空格进行编码。
# #@如果可选参数 header 存在且为True，则空格将被编码为下划线 。
# #@如果可选参数 header 存在且为False，则也会对换行符进行编码;不进行换行转换编码可能会破坏二进制数据流。
bs.b2a_qp(data, quotetabs=False, istext=True, header=False)

# binhex4编码数据转换
# #将 binhex4 格式的 ASCII 数据不进行 RLE 解压缩直接转换为二进制数据。
# #@该字符串应包含完整数量的二进制字节，或者（在binhex4 数据最后部分）剩余位为零。
bs.a2b_hqx('ABCD')
# #根据 binhex4 标准对数据执行 RLE 解压缩。
# #@该算法在一个字节的数据后使用 0x90 作为重复指示符，然后计数。
# #@计数 0 指定字节值 0x90 。该例程返回解压缩的数据，输入数据以孤立的重复指示符结束的情况下，将引发 Incomplete 异常。
# #3.2版后，仅接受 bytestring 或 bytearray 对象作为输入。
bs.rledecode_hqx(data)
# #在 data 上执行 binhex4 游程编码压缩并返回结果。
bs.rlecode_hqx(data)
# #执行 hexbin4 类型二进制到 ASCII 码的转换并返回结果字符串。输入数据应经过 RLE 编码，且数据长度可被3整除（除了最后一个片段）。
bs.b2a_hqx(data)
# #以 value 作为初始 CRC 计算 data 的16位 CRC 值。该 CRC 被用于 binhex4 格式。
value = b''
bs.crc_hqx(data, value)
# #计算 CRC-32 ，从 value 的初始 CRC 开始计算 data 的32位校验和。默认初始 CRC 为零。
# #@该算法与 ZIP 文件校验和一致。由于该算法被设计用作校验和算法，因此不适合用作通用散列算法。
# ##bs.crc32(data[, value])
print(bs.crc32(b"hello world"))
# Or, in two pieces:
crc = bs.crc32(b"hello")
crc = bs.crc32(b" world", crc)
print('crc32 = {:#010x}'.format(crc))

# 十六进制数据转换
# #返回二进制数据 data 的十六进制表示形式,
# #@data 的每个字节都被转换为相应的2位十六进制表示形式。因此返回的字节对象的长度是 data 的两倍。
# #@使用：bytes.hex() 方法也可以方便地实现相似的功能（但仅返回文本字符串）。
# #@如果指定了 sep，它必须为单字符 str 或 bytes 对象。它将被插入每个 bytes_per_sep 输入字节之后。
# #@分隔符位置默认从输出的右端开始计数，如果你希望从左端开始计数，请提供一个负的 bytes_per_sep 值。
# ##bs.b2a_hex(data[, sep[, bytes_per_sep=1]])
# ##bs.hexlify(data[, sep[, bytes_per_sep=1]])
bs.b2a_hex(b'\xb9\x01\xef')
bs.hexlify(b'\xb9\x01\xef', '-')
bs.b2a_hex(b'\xb9\x01\xef', '-', 2)
bs.b2a_hex(b'\xb9\x01\xef', '-', -2)
# #返回由十六进制字符串 hexstr 表示的二进制数据。
# # hexstr 必须包含偶数个十六进制数字（可以是大写或小写），否则会引发 Error 异常。
# #使用：bytes.fromhex() 类方法也实现相似的功能（仅接受文本字符串参数，不限制其中的空白字符）。
hexstr = b'\x1\s23\23'
bs.a2b_hex(hexstr)
bs.unhexlify(hexstr)

# 异常
# #通常是因为编程错误引发的异常。
bs.Error
# #数据不完整引发的异常。通常不是编程错误导致的，可以通过读取更多的数据并再次尝试来处理该异常。
bs.Incomplete