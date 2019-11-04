#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'Rest API学习用例'
__author__ = '林金行'

class RestAPI(object):
    def __init__(self,path=''):
        self._path = path
    def __getattr__(self, path):
        return RestAPI("%s/%s" % (self._path,path))
    def __str__(self):
        return self._path
    __repr__ = __str__

    def run(self):
        pass

ra = RestAPI().status.user.timeline.list
ra2 = RestAPI().users('Jeke').repos
ra.run()
print(ra2)
