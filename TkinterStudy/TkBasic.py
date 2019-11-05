#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'Tkinter基础方法实现'
__author__ = '林金行'

from tkinter import *
from tkinter import ttk
#创建一个窗口对像
root = Tk()
#使用Frame增加一层容器
fm1 = Frame(root)
#Label是一种用来显示文字或者图片的组件
#Label(fm1,text = 'Lable1',bg='red').pack(side=LEFT)
#Label(fm1,text = 'Lable1',bg='yellow').pack(side=RIGHT)
#Label(fm1,text = 'Lable1',bg='blue').pack(side=BOTTOM)
#fm1.pack(side=TOP,fill=BOTH,expand=YES)
# Button是一种按钮组件，与Label类似，只是多出了响应点击的功能
Button(fm1, text='Top').pack(side=TOP, anchor=W, fill=X, expand=YES)
Button(fm1, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
Button(fm1, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
fm1.pack(side=LEFT, fill=BOTH, expand=YES)

fm2 = Frame(root)
Button(fm2, text='Left').pack(side=LEFT)
Button(fm2, text='This is the Center button').pack(side=LEFT)
Button(fm2, text='Right').pack(side=LEFT)
li = ['王记','12','男']
tree = ttk.Treeview(root,columns=['1','2','3'],show='headings')
tree.column('1',width=100,anchor='center')
tree.column('2',width=100,anchor='center')
tree.column('3',width=100,anchor='center')
tree.heading('1',text='姓名')
tree.heading('2',text='学号')
tree.heading('3',text='性别')
tree.insert('','end',values=li)
tree.pack(side=LEFT)
fm2.pack(side=LEFT, padx=10)

#root.geometry('640x480')
root.resizable(0,0)
root.title("Tkinter")
root.mainloop()
