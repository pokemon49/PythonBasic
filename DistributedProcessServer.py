#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'分布式进程编程--服务器端'
__author__ = '林金行'

import random,time,queue
from multiprocessing.managers import BaseManager

class Server(BaseManager):
    pass

take_queue = queue.Queue()
result_queue = queue.Queue()
Server.register('get_task_queue', callable=take_queue)
Server.register('get_result_queue', callable=result_queue)

class DistributedProcessServer(object):
    def set(self):
        self.manage = Server(address=('',5000),authkey=b'abc')
    def start(self):
        self.manage.start()
    def end(self):
        self.manage.shutdown()
    def execute(self):
        self.set()
        self.start()
        task = self.manage.get_task_queue()
        result = self.manage.get_result_queue()
        for i  in range(10):
            n = random.randint(0,10000)
            print('Put task %d...' % n)
            task.put(n)
        print('Try get results....')
        for i in range(10):
            r = result.get(timeout=10)
            print('Result: %s' % r)
        self.end()
        print('master exit')
    def run(self):
        self.execute()
        pass


dps = DistributedProcessServer()
dps.run()