#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'多线程学习实例'
__author__ = '林金行'
import os, time, random, threading, multiprocessing, threadpool, random


class MulitThreadStudy(object):
    balance = 0
    lock = threading.Lock()
    tl = threading.local()
    exp_dict = {'Java': 1, 'C': 1, 'Scala': 1}
    new_bal = 0
    max_bal = 10000
    gobal_dict = {'JAVA': 0, 'C': 0, 'C#': 0, 'SCALA': 0, 'SQL': 0, 'C++': 0}
    key_list = list(range(1, 2000))
    key_runed = []

    def LoopThread(self, key='A'):
        print('Thread %s is running' % threading.current_thread().name)
        n = 0
        while n < 9:
            n = n + 1
            print("Thread %s >>> %s" % (threading.current_thread().name, n))
            time.sleep(random.random()*1)
            if key == 'Java':
                self.exp_dict.update({key: self.exp_dict[key] + n})
            elif key == 'C':
                self.exp_dict.update({key: self.exp_dict[key] * n})
            elif key == 'Scala':
                self.exp_dict.update({key: self.exp_dict[key] / n})
        print("Thread %s ended." % threading.current_thread().name)

    def ThreadActive(self):
        print('Thread %s is running...' % threading.current_thread().name)
        t1 = threading.Thread(target=self.LoopThread, name='LoopThread1', args=('Java',))
        t2 = threading.Thread(target=self.LoopThread, name='LoopThread2', args=('C',))
        t3 = threading.Thread(target=self.LoopThread, name='LoopThread3', args=('Scala',))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        print(self.exp_dict)
        print("Thread %s end." % threading.current_thread().name)

    def LockBalance(self, n):
        self.balance = self.balance + n
        self.balance = self.balance - n

    # 锁处理方法
    def LockThread(self, n):
        for i in range(1000):
            #获得锁
            self.lock.acquire()
            try:
                self.LockBalance(n)
            finally:
                #释放锁
                self.lock.release()

    def LockThreadActive(self):
        t1 = threading.Thread(target=self.LockThread, args=(5,))
        t2 = threading.Thread(target=self.LockThread, args=(8,))
        t3 = threading.Thread(target=self.LockThread, args=(4,))
        t4 = threading.Thread(target=self.LockThread, args=(6,))
        t5 = threading.Thread(target=self.LockThread, args=(22,))
        t6 = threading.Thread(target=self.LockThread, args=(62,))
        t7 = threading.Thread(target=self.LockThread, args=(65,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        print(self.balance)

    def BadThread(self):
        x = 0
        while True:
            x = x ^ 1

    def BadThreadActive(self):
        for i in range(multiprocessing.cpu_count()):
            t = threading.Thread(target= self.BadThread)
            t.start()

    # ThreadLocal线程变量控制
    def LocalStudent(self):
        std = self.tl.student
        print("Hello %s (in %s)" % (std, threading.current_thread().name))

    def LocalThread(self, name):
        self.tl.student = name
        self.LocalStudent()

    def LocalThreadActive(self):
        t1 = threading.Thread(target=self.LocalThread, args=("Lily",), name ="Student1")
        t2 = threading.Thread(target=self.LocalThread, args=("Anni",), name ="Student2")
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    # 线程池操作
    def localThreadPool(self):
        num_list = [n for n in range(0, 9)]
        script_list = [['JAVA', 'C', 'C#'], ['SCALA', 'SQL', 'C++']]
        pool = threadpool.ThreadPool(2)
        # requests = threadpool.makeRequests(self.threadpool_proc, script_list)
        requests = threadpool.makeRequests(self.threadpool_dict, script_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        # print(self.gobal_dict)
        print(self.key_runed)

    def threadpool_proc(self, n):
        for sc in n:
            print(sc)
            # self.gobal_dict.update({sc: self.new_bal})
        # 获得锁
        self.lock.acquire()
        try:
            # print("%d + %d = " % (self.new_bal, n))
            self.new_bal = self.new_bal + 1
            # print(self.new_bal)
            # print(self.new_bal / self.max_bal)
        finally:
            # 释放锁
            self.lock.release()

    def tk_key(self):
        self.lock.acquire()
        try:
           key = self.key_list[0]
           self.key_list.pop(0)
        finally:
            self.lock.release()
        return key
    
    # 验证多线程返回序列
    def threadpool_dict(self, para):
        while 1 == 1:
            if len(self.key_list) == 0:
                break
            key = self.tk_key()
            self.key_runed.append(key)
            # re = random.randint(5, 10)
            # time.sleep(re)
    def run(self):
        # self.ThreadActive()
        # self.LockThreadActive()
        # self.BadThread()
        # self.LocalThreadActive()
        self.localThreadPool()
        pass

mts = MulitThreadStudy()
mts.run()