#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'单元测试实例'
__author__ = '林金行'

#测试用自定义字典类型
class mydict(dict):
    def __init__(self,**kw):
        super().__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'MyDict' Object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    pass

import unittest
class UnitTestStudy(unittest.TestCase):
    #每个测试前运行代码
    def setUp(self):
        print("Test Start")
    # 每个测试后运行代码
    def tearDown(self):
        print("Test Down")
    #以test开头的方法就是测试方法
    def test_init(self):
        d = mydict(a = 1, b= 'test')
        self.assertEqual(d.a,1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d,mydict))
    def test_key(self):
        d = mydict()
        d['key'] = 'value'
        self.assertEqual(d.key,'value')
    def test_attr(self):
        d = mydict()
        d.key = 'value'
        self.assertEqual(d['key'],'value')
        self.assertTrue('key' in d)
    def test_key(self):
        d = dict()
        #期待抛出指定类型的Error
        with self.assertRaises(KeyError):
            value = d['empty']
    def test_attreroor(self):
        d = dict()
        with self.assertRaises(AttributeError):
            value = d.empty
    if __name__ == '__main__':
        unittest.main()
    pass


#使用文档测试方法
class mydict2(dict):
    '''
    Study The Doctest Function
    >>> d1= mydict2()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = mydict2(a = 1, b='2', c = 'c')
    >>> d2.c
    'c'
    >>> d2['empty']
    Traceback (most recent call last):
    ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
    ...
    AttributeError: 'mydict2' Object has no attribute 'empty'
    '''
    def __init__(self,**kw):
        super().__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'mydict2' Object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    pass

def fan(n):
    '''
    doctest study demo
    >>> fan(0)
    Traceback (most recent call last):
    ...
    ValueError
    >>> fan(-1)
    Traceback (most recent call last):
    ...
    ValueError
    >>> fan(1)
    1
    >>> fan(2)
    2
    >>> fan(3)
    6
    '''
    if n < 1 :
        raise ValueError()
    if n == 1:
        return 1
    return n*fan(n -1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()