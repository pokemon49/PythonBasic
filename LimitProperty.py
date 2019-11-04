#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'限制变量值的用例'
__author__ = '林金行'


class LimitProperty(object):
    @property
    def hight(self):
        return self._hight

    @hight.setter
    def hight(self, value):
        if not isinstance(value, int):
            raise ValueError("hight Must be an Integer!")
        if value < 0:
            raise ValueError("hight Must Greater Then 0!")
        self._hight = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            raise ValueError("width Must be a Integer!")
        if value < 0:
            raise ValueError("width Must Greater Then 0!")
        self._width = value
    @property
    def resolution(self):
        return self._hight * self._width

    def run (self):
        pass

lp = LimitProperty()
lp.hight = 1024
lp.width = 768
print(lp.resolution)
assert  lp.resolution == 786432," 1024*768 = %d" % lp.resolution