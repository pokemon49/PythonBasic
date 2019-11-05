
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'数据交互中心'
__author__ = '林金行'

import threading
from MyException import *

class InteractiveCenter(threading.Thread):
    def __init__(self,inst):
        threading.Thread.__init__(self)
        self.inst = inst
    def terminal(self):
        return self.terminal_basic()
    def terminal_basic(self):
        print("输入：\"S\" 表示暂停")
        print("输入：\"E\" 表示退出")
        print("输入：\"C\" 表示继续")
        input_info = input("请输入所需要操作的命令:")
        if input_info in ("S","E","C"):
            return input_info
        else:
            print("输入值错误！请重新输入")
        return self.terminal_basic()
    def command_process(self):
        take_info = self.terminal()
        if take_info and hasattr(self.inst,"control"):
            self.inst.control = take_info
        else:
            raise MyException("输入实例不存在\"control\"属性！")
    def run(self):
       self.command_process()
       pass
    pass


#ic = InteractiveCenter()
#ic.run()