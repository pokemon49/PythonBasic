#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'Bisect排序管理应用样例'
# 'Version 1.0'
# '1.0 20200101 初始版本创建'
__author__ = '林金行'

import bisect
import sys

class BisectStudy(object):
    # 查找原素
    HAYSTACK = [0, 1, 3, 5, 6, 23, 55, 77, 80, 84, 86, 93, 98, 99]
    NEEDELS = [0, 5, 7, 8, 9, 33, 43, 51, 67, 77, 90, 91, 93, 95, 99, 100]
    ROW_FMT = '{0:3d} @ {1:3d}  {2}{0:<3d}'
    # #查找应用样例
    def such_demo(self, bisect_fn, base_list, such_list):
        for needel in reversed(such_list):
            position = bisect_fn(base_list, needel)
            offect = position * '  |'
            print(self.ROW_FMT.format(needel, position, offect))
    if __name__ == '__main__':
        if sys.argv[-1] == 'left':
            bisect_fn = bisect.bisect_left
        else:
            bisect_fn = bisect.bisect

    def such_item(self):
        print('DEMO：', self.bisect_fn.__name__)
        print('haystack ->', ' '.join('%2d' % n for n in self.HAYSTACK))
        self.such_demo(self.bisect_fn, self.HAYSTACK, self.NEEDELS)

    # #查找原元素的衍生用法
    def grade(self, score, breakpoints, grades):
        bp = [60, 70, 80, 90]
        gd = 'FDCBA'
        i = self.bisect_fn(breakpoints,score)
        return grades[i]

    # 查找并插入元素
    def insert_item(self):
        import random
        size = 12
        random.seed(1729)
        my_list = []
        for i in range(size):
            new_item = random.randrange(size*size)
            bisect.insort(my_list, new_item)
            print('%2d -> ' % new_item,my_list)

    # #主调用方法
    def run(self):
        self.such_item()
        bp = [60, 70, 80, 90]
        gd = 'FDCBA'
        lvl = [self.grade(s, bp, gd) for s in [21, 35, 66, 77, 32, 79, 87, 93, 68, 99]]
        print('查找的衍生用法：')
        print(lvl)
        print('插入元素')
        self.insert_item()
        pass

bs = BisectStudy()

bs.run()