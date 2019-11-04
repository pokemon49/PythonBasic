#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''
__author__ = '林金行'

from multiprocessing import Process,Pool,Queue
import os,time,random,subprocess

#子进程
class MulitProcessStudy(object):
    def LinuxProcess(self):
        print('Process (%s) start .....' % os.getpid())
        pid = os.fork()
        if pid == 0 :
            print('I am child process (%s) and my parent is %s' % (os.getpid(),os.getppid()))
        else:
            print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
    def WindowsChildProcess(self,name):
        if name == 'test':
            print('Run child process %s (%s)...' % (name,os.getpid()))
        else:
            print('Ran task %s (%s)' % (name,os.getpid()))
            start = time.time()
            time.sleep(random.random()*10)
            end = time.time()
            print("Task %s runs %0.2f seconds" % (name,(end - start)))
    def WindowsProcess(self):
        if __name__ == '__main__':
            print("Parent process %s." % os.getpid())
            p = Process(target= self.WindowsChildProcess ,args=("test",))
            print("Child process will start.")
            p.start()
            p.join()
            print('Child process end.')
    def WindowsPollProcess(self):
        if __name__ == '__main__':
            print('Parent process %s.' % os.getpid())
            p = Pool(1)
            for i in range (6):
                p.apply_async(self.WindowsChildProcess, args=(i,))
            print('Waiting for all subprocess done...')
            #调用前必需调用Close,结束线程添加
            p.close()
            p.join()
            print('All subprocess done.')
    def run(self):
        #Linux环境才可运行
        #self.LinuxProcess()
        #Windows环境运行
        #self.WindowsProcess()
        #self.WindowsPollProcess()
        # 子进程处理
        self.SubProcess()
        self.InteractionSubProcess()
        self.ConnectionProcess()
        pass
    #子程序
    def SubProcess(self):
        print('$nslookup www.baidu.com')
        r = subprocess.call(['nslookup','www.baidu.com'])
        print('Exit code:',r)
    #
    def InteractionSubProcess(self):
        print('$nslookup')
        p = subprocess.Popen(['nslookup'],stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        out,err = p.communicate(b'set q = mx\npython.org\nexit\n')
        print(out)
        print('Exit code:',p.returncode)
    #进程间通信
    def ConnectionProcessWrite(self,q):
        print('Process to Write: %s' % os.getpid())
        for value in ['AA','AB','AC']:
            print('Put %s to queue' % value)
            q.put(value)
            time.sleep(random.random()*3)
    def ConnectionProcessRead(self,q):
        print('Process to Read: %s' % os.getpid())
        while True:
            value = q.get(True)
            print('Get %s from queue.' % value)
    def ConnectionProcess(self):
        if __name__ == '__main__':
            q = Queue()
            pw = Process(target=self.ConnectionProcessWrite,args=(q,))
            pr = Process(target=self.ConnectionProcessRead, args=(q,))
            pw.start()
            pr.start()
            pw.join()
            #强行结束
            pr.terminate()


mps = MulitProcessStudy()
mps.run()