#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'多线程学习实例'
__author__ = '林金行'

import os,time,random,threading,multiprocessing
class MulitThreadStudy(object):
    balance = 0
    lock = threading.Lock()
    tl = threading.local()
    def LoopThread(self):
        print('Thread %s is running' % threading.current_thread().name)
        n = 0
        while n < 5:
            n = n + 1
            print("Thread %s >>> %s" % (threading.current_thread().name,n))
            time.sleep(random.random()*1)
        print("Thread %s ended." % threading.current_thread().name)
    def ThreadActive(self):
        print('Thread %s is running...' % threading.current_thread().name)
        t = threading.Thread(target=self.LoopThread ,name='LoopThread')
        t.start()
        t.join()
        print("Thread %s end." % threading.current_thread().name)
    def LockBalance(self,n):
        self.balance = self.balance + n
        self.balance = self.balance - n
    def LockThread(self,n):
        for i in range(1000000):
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
            x =x ^ 1
    def BadThreadActive(self):
        for i in range(multiprocessing.cpu_count()):
            t = threading.Thread(target= self.BadThread)
            t.start()
    #ThreadLocal线程变量控制
    def LocalStudent(self):
        std = self.tl.student
        print("Hello %s (in %s)" %  (std,threading.current_thread().name))
    def LocalThread(self,name):
        self.tl.student = name
        self.LocalStudent()
    def LocalThreadActive(self):
        t1 = threading.Thread(target=self.LocalThread, args=("Lily",), name ="Student1")
        t2 = threading.Thread(target=self.LocalThread, args=("Anni",), name ="Student2")
        t1.start()
        t2.start()
        t2.join()
        t2.join()
    def run(self):
        self.ThreadActive()
        self.LockThreadActive()
        self.BadThread()
        self.LocalThreadActive()
        pass

mts = MulitThreadStudy()
mts.run()