#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '数据类型操作实例'
__author__ = '林金行'
import os


class DataType(object):
    # 常规数据类型
    I = 123
    F = 1.34
    S1 = 'This is Single Quotation'
    S2 = "This is Double Quotation"
    S3 = "This is \"Escape Charter\""
    # #非转义字符串
    S4 = r"Can't Use Escape Charter:\\\t"
    print(I, "\n", F, "\n", S1, "\n", S2, "\n", S3, "\n", S4)
    # 多行
    # #多字符串链接
    S4 = "Multi String Link:" \
         "Line1" \
         "Line2"
    # #多行字符串
    S5 = '''Multi Column2:
    Line 1
    Line 2
    Line 3
    '''
    print(S4, S5)
    # #字符处理
    c1 = 'a'
    c2 = '文'
    c3 = 78
    c4 = 20755
    c5 = '\u4e2d\u6587'
    # ##转换
    print("转换为数字：", c1, ":", ord(c1), r"\\", c2, ":", ord(c2))
    print("转换为字符：", c3, ":", chr(c3), r"\\", c4, ":", chr(c4))
    print(r'十六进制转换字符：\u4e2d\u6587', '-', c5)
    # 可变系列
    # #List
    l = ['Java', 'Scala', 'Html', 'Javascript']
    # #列表生成
    # ##数字序列
    l = list(range(1, 100))
    print(l)
    # ##乘数序列
    l = [x*x for x in range(1, 100)]
    print(l)
    # ##乘数序列带条件
    l = [x*x for x in range(1, 100) if x % 2 == 0]
    print(l)
    # ##双层全排列序列
    l = [m+n for m in "Java" for n in "Python"]
    print(l)
    # ##目录序列
    l = [d for d in os.listdir('C:/')]
    print(l)
    # ##过滤序列
    l = ['a', 'b', 'c', 9, 'd', 'e']
    l = [x for x in l if not isinstance(x, (int, float))]
    print(l)
    # ##元素添加
    l.append('e')
    print(l)
    # #元素遍历
    # ##区间取数
    print(l[0:3])
    print(l[:3])
    print(l[1:3])
    # ###倒数
    #####
    print(l[-2])
    print(l[-1:-2])
    lr = list(range(100))
    # #切片
    # ##取前十个数，每2个取一个
    print(l[:10:2])
    # ##每五个取一个
    print(l[::5])
    # 删除元素
    # #删除最后一个
    lr.pop()
    # #删除指定下标元素
    lr.pop(3)
    # #修改指定下标元素
    lr[5] = "abc"
    print(lr)
    # 复合List
    lu = [0, 10, 20, 30, [31, 32, 33, 34, 35, 36, 37, 38, 39], 40]
    print(lu)
    l1 = [31, 32, 33, 34, 35, 36, 37, 38, 39]
    l2 = [0, 10, 20, 30, l1, 40]
    # 不可变系列
    # #dict
    print("-- Dict")
    d = {'Java': 90, 'Python': 85, 'C': 88, 'C++': 83}
    print(d['C'])
    print("获取字典key：")
    print(list(d))
    print("获取字典value：")
    print(list(d.values()))
    # 判断是否存在元素
    print('Scala' in d)
    print(d.get('Java'))
    print(d.get('Html5'))
    print(d.get('Php', -1))  # 不存在的返回值
    # 删除元素
    d.pop('C')
    # #set-没有Value的Dict
    print("-- Set")
    s1 = {56, 77, 35}
    s2 = {80, 77, 90}
    # ##添加元素
    s1.add(65)
    # ##删除元素
    s1.remove(35)
    print(s1 & s2)
    print(s1 | s2)
    # tuple(不可变的List)
    print('-- tuple')
    # 声明
    # #一般
    t = (1, 2)
    # #空
    t = ()
    # #单一元素
    t = (1,)
    # 可变的tuple
    t = (1, 2, 3, 4, [5, 6, 7], 8, 9)
    # 判断集合是否为子集
    print(s1.issubset(s2))
    # 获取两集合的交集
    s3 = s1.intersection(s2)
    print(s3)
