#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'通讯管理系统处理集合'
__author__ = '林金行'

from tkinter import *
import tkinter.messagebox
from  Exercise.BookManagerSystem.systemDB import *

class systemProcess(object):
    def __init__(self):
        self.sd = systemDB()
    #查询方法
    def take_data(self,tree,such_name=None,such_phone=None):
        if isinstance(such_name,Entry):
            s_name = such_name.get()
            s_phone = such_phone.get()
        else:
            s_name = ""
            s_phone = ""
        if len(s_name)+len(s_phone) == 0:
            data_list = self.sd.take_data()
        else:
            s_name = s_name.strip()
            s_phone = s_phone.strip()
            data_list = self.sd.take_data(name=s_name,tel=s_phone)
        if len(data_list) > 0:
            self.flush_tree(tree,data_list)
        else:
            self.clearn_tree(tree)
    #新增方法
    def create_data(self,tree,sun_window,E_name,E_company,E_tel,E_email):
        name = E_name.get()
        company = E_company.get()
        tel = E_tel.get()
        email = E_email.get()
        sd = systemDB()
        result = self.sd.insert_data(name = name,company=company,telephone=tel,email=email)
        if result:
            self.message_box("联系人创建成功","info")
            self.exit_windows(sun_window)
            self.take_data(tree=tree)
    #修改数据
    def change_data(self,tree,sub_window,E_code,E_name,E_company,E_tel,E_email):
        code = E_code.get()
        name = E_name.get()
        company = E_company.get()
        tel = E_tel.get()
        email = E_email.get()
        sd = systemDB()
        result = self.sd.change_date(code,name=name, company=company, telephone=tel, email=email)
        if result:
            self.message_box("联系人变更成功", "info")
            self.exit_windows(sub_window)
            self.take_data(tree=tree)
    #删除功能
    def delete_data(self,tree):
        select_values = tree.selection()
        select_len = len(select_values)
        if select_len != 1:
            self.message_box("请选择一条记录", "warn")
        else:
            select_value = tree.item(select_values, "values")
            msg = "确定要删除<%s>的联系方式么?" % (select_value[1])
            print(msg)
            if self.message_box(msg,"ask"):
                sd = systemDB()
                result = self.sd.delete_data(select_value[0])
                if result:
                    self.message_box("联系人删除成功", "info")
                    self.take_data(tree)
        pass
    #消息提示窗口
    def message_box(self,msg,type):
        if type == "info":
            tkinter.messagebox.showinfo('提示', msg)
        elif type == "warn":
            tkinter.messagebox.showwarning('警告', msg)
        elif type == "error":
            tkinter.messagebox.showerror('错误', msg)
        elif type == "ask":
            resule = tkinter.messagebox.askokcancel('提示', msg)
            return resule
    # 更新列表方法
    def flush_tree(self, tree,dataList):
        #清空列表
        self.clearn_tree(tree)
        #更新数据
        if not isinstance(dataList[0],tuple):
            tree.insert('', 'end', values=dataList)
        else:
            for data in dataList:
                tree.insert('','end',values=data)
    #清空列表方法
    def clearn_tree(self,tree):
        # 获取列表项
        data = tree.get_children()
        # 清空列表
        for item in data:
            tree.delete(item)
    #关闭子窗体方法
    def exit_windows(self,winodw):
        winodw.destroy()