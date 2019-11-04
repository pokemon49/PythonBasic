#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '过滤器学习实例'
__author__ = "林金行"


class FilterStudy(object):

    def _odd_iter(self):
        n = 1
        while True:
            n = n + 2
            yield n

    def _not_divisible(self, n):
        return lambda x : x % n > 0

    def primer(self):
        yield 2                # 生成第一个数：2
        it = self._odd_iter()  # 初始化序列
        while True:
            n = next(it)
            yield n
            it = filter(self._not_divisible(n), it)

    def is_palindrome(self, n):
        i, m = n, 0
        while i:
            m = m * 10 + i % 10
            i = i // 10
        return n == m
        pass

    def take_palindrome(self, n):
        i, m = n, 0
        while i:
            m = m * 10 + i % 10
            i = i // 10
        if m == n:
            return m
        else:
            return self.take_palindrome(m + n)

    def run(self):
        for n in self.primer():
            if n < 1000 :
                print(n)
            else:
                break
        l = list(filter(self.is_palindrome,[11,12,13,44,55,777,123,121,141]))
        print(l)


fs = FilterStudy()  # Filter属于惰性计算
fs.run()
print(fs.take_palindrome(199))
# print(fs.is_palindrome(132))
