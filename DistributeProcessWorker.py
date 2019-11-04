#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'分布式进程编程--客户端'
__author__ = '林金行'


import sys,time,queue
from multiprocessing.managers import BaseManager

class Worker(BaseManager):
    pass

class DistributeProcessWorker(object):
    def __init__(self):
        Worker.register('get_task_queue')
        Worker.register('get_result_queue')
        self.server_addr = '127.0.0.1'
        print('Connect to server %s...' % self.server_addr)
    def connect(self):
        self.m = Worker(address=(self.server_addr,5000),authkey=b'abc')
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
    def work(self):
        for i in range(10):
            try:
                n = self.task.get(timeout = 1)
                print('Run task %d * %d' % (n,n))
                r = '%d * %d = %d' % (n,n,n*n)
                time.sleep(1)
                self.result.put(r)
            except Exception:
                print('task queue is empty!')
        print('Woker exit.')
    def run(self):
        pass
dpw = DistributeProcessWorker()
dpw.run()