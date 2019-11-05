#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'通讯管理系统界面布局'
__author__ = '林金行'
from tkinter import *
from tkinter import ttk
from Exercise.BookManagerSystem.systemProcess import *

class basicGUI(object):
    def __init__(self,root):
        #初始化处理方法
        self.sp = systemProcess()
        # 使用Frame增加一层容器
        fm1 = Frame(root)
        fm2 = Frame(root)
        # 增加上层组件
        ##增加Label标题
        name = Label(fm2, text='姓名：')
        ##增加文本框
        such_name = Entry(fm2, width=25)
        ##增加Label标题
        phone = Label(fm2, text='电话：')
        ##增加文本框
        such_phone = Entry(fm2, width=25)
        ##增加按钮
        such = Button(fm2, text='查询')
        create = Button(fm2, text='新增')
        change = Button(fm2, text='修改')
        delete = Button(fm2, text='删除')
        ##生成布局
        name.pack(side=LEFT)
        such_name.pack(side=LEFT, anchor=W, fill=X, expand=YES, ipadx=10)
        phone.pack(side=LEFT)
        such_phone.pack(side=LEFT, anchor=W, fill=X, expand=YES, padx=3)
        such.pack(side=LEFT, anchor=W, fill=X, expand=YES, padx=3)
        create.pack(side=LEFT, anchor=W, fill=X, expand=YES, padx=3)
        change.pack(side=LEFT, anchor=W, fill=X, expand=YES, padx=3)
        delete.pack(side=LEFT, anchor=W, fill=X, expand=YES, padx=3)
        fm2.pack(side=TOP, fill=BOTH, pady=10)
        # 增加结果查询窗口
        ##结果窗口
        tree = ttk.Treeview(fm1, columns=['1', '2', '3', '4', '5'], show='headings', height=600)
        vbar = ttk.Scrollbar(fm1, orient=VERTICAL, command=tree.yview)
        # 定义树形结构与滚动条
        tree.configure(yscrollcommand=vbar.set)
        # 结果内容定义
        tree.column('1', width=55, anchor='center')
        tree.column('2', width=100, anchor='center')
        tree.column('3', width=155, anchor='center')
        tree.column('4', width=155, anchor='center')
        tree.column('5', width=155, anchor='center')
        tree.heading('1', text='编号')
        tree.heading('2', text='姓名')
        tree.heading('3', text='工作单位')
        tree.heading('4', text='联系电话')
        tree.heading('5', text='E-Mail')
        tree.pack(side=TOP)
        tree.bind('<Double-1>',self.d_change_data)
        vbar.pack()
        fm1.pack(side=BOTTOM, fill=BOTH, pady=10)
        #配置功能区
        ##查询功能配置
        such['command'] = lambda : self.sp.take_data(tree,such_name,such_phone)
        create['command'] = lambda: self.sub_windows("c")
        change['command'] = self.change
        delete['command'] = lambda :self.sp.delete_data(tree=tree)
        # 功能组件初始化
        self.tree = tree
        #功能组件初始化
        self.such = such
        self.create = create
        self.change = change
        self.delete = delete
        # 生成窗口
        ##设置窗口大小
        root.geometry('640x480')
        ##设置窗口不可变
        root.resizable(0, 0)
        ##设置窗口标题
        root.title("通讯录管理系统")
        ##设置窗口大小
        root.mainloop()

    # 创建子窗体
    def sub_windows(self,fun="s",**kw):
        # 创建窗体
        change_top = Toplevel()
        change_top.resizable(0, 0)
        #使用Frame增加一层容器
        sfm1 = Frame(change_top)
        sfm2 = Frame(change_top)
        ##生成标题
        code = Label(sfm1, text='编号：')
        name = Label(sfm1, text='姓名：')
        company = Label(sfm1, text='工作单位：')
        tel = Label(sfm1, text='电话：')
        email = Label(sfm1, text='E-Mail：')
        ##变量值定义
        v_code = StringVar()
        v_name = StringVar()
        v_company = StringVar()
        v_email = StringVar()
        v_tel = StringVar()
        ##生成文本框
        E_code = Entry(sfm1, width=25,state=DISABLED,textvariable =v_code)
        E_name = Entry(sfm1, width=25,textvariable =v_name)
        E_company = Entry(sfm1, width=25,textvariable =v_company)
        E_email = Entry(sfm1, width=25,textvariable =v_email)
        E_tel = Entry(sfm1, width=25,textvariable =v_tel)
        if fun =="c":
            change_top.geometry('270x150')
            change_top.title("新增联系人")
            botton_name = "创建"
            botton_command = lambda : self.sp.create_data(self.tree,change_top,E_name = E_name,E_company = E_company,E_email = E_email ,E_tel = E_tel)
            row_num = 0
        else:
            change_top.geometry('270x180')
            change_top.title("修改联系人")
            botton_name = "修改"
            botton_command = lambda : self.sp.change_data(self.tree,change_top,E_code=E_code,E_name = E_name,E_company = E_company,E_email = E_email ,E_tel = E_tel)
            row_num = 1
            v_code.set(kw['code'])
            v_name.set(kw['name'])
            v_company.set(kw['company'])
            v_tel.set(kw['tel'])
            v_email.set(kw['email'])
            code.grid(row=row_num - 1, column=0, padx=1, pady=1)
            E_code.grid(row=row_num - 1, column=1, padx=1, pady=1)
        ##生成布局
        name.grid(row=row_num, column=0, padx=1, pady=1)
        E_name.grid(row=row_num, column=1, padx=1, pady=1)
        company.grid(row=row_num+1, column=0, padx=1, pady=1)
        E_company.grid(row=row_num+1, column=1, padx=1, pady=1)
        tel.grid(row=row_num+2, column=0, padx=1, pady=1)
        E_tel.grid(row=row_num+2, column=1, padx=1, pady=1)
        email.grid(row=row_num+3, column=0, padx=1, pady=1)
        E_email.grid(row=row_num+3, column=1, padx=1, pady=1)
        sfm1.pack(side=TOP, fill=BOTH, pady=10)
        #按钮区
        s_change = Button(sfm2, text=botton_name,command = botton_command)
        s_exit = Button(sfm2, text="退出",command=lambda :self.exit_windows(change_top))
        #布局
        s_change.pack(side=LEFT,padx=60)
        s_exit.pack(side=LEFT,padx=2)
        sfm2.pack(side=BOTTOM, fill=BOTH, pady=2)
        #功能映射
        self.E_code = E_code
        self.E_name = E_name
        self.E_company = E_company
        self.E_email = E_email
        self.E_tel = E_tel
        self.change_top=change_top

    #关闭子窗体方法
    def exit_windows(self,winodw):
        winodw.destroy()

    #修改窗口调用
    def change(self):
        select_values = self.tree.selection()
        select_len = len(select_values)
        if select_len != 1:
            self.sp.message_box("请选择一条记录","warn")
        else:
            select_value = self.tree.item(select_values,"values")
            self.sub_windows(code = select_value[0],name = select_value[1],company = select_value[2],tel = select_value[3],email = select_value[4])
        pass
    #双击修改窗口调用
    def d_change_data(self,event):
        print(event)
        select_values = self.tree.selection()
        select_len = len(select_values)
        if select_len != 1:
            self.sp.message_box("请选择一条记录","warn")
        else:
            select_value = self.tree.item(select_values,"values")
            self.sub_windows(code = select_value[0],name = select_value[1],company = select_value[2],tel = select_value[3],email = select_value[4])
        pass




