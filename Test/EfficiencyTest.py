#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '性能测试实例'
__author__ = '林金行'

import timeit
import dis


class EfficiencyTest(object):

    # 生成要测试的对像
    def test_object_1(self):
        return set([1, 2, 3])

    def test_object_2(self):
        return set((1, 2, 3))

    def test_object_3(self):
        return {1, 2, 3}

    # 分析生成原理
    dis.dis(test_object_1)
    dis.dis(test_object_2)
    dis.dis(test_object_3)
    pass


et = EfficiencyTest()
# 性能测试
print("测试结果1："+str(min(timeit.repeat(et.test_object_1))))
print("测试结果2："+str(min(timeit.repeat(et.test_object_2))))
print("测试结果3："+str(min(timeit.repeat(et.test_object_3))))
