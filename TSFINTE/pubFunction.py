#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '公共方法'
# 'Version 1.0'
# '1.0 20200912 初始版本创建'
__author__ = '林金行'

class pubfunction(object):
    # 初始始化参数
    def __init__(self):
        # 默认参数配置
        self.baseUrl = 'x18r.com'
        self.baseInputPath = r'G:\TS\X18R'
        self.SourcePath = self.baseInputPath + r'\Source'
        self.SettingPath = self.baseInputPath + r'\Setting'
        # #存储变量配置
        self.set_menu = self.tk_set_dict('Set_menu')
        self.cookie = self.tk_set_list('Cookie')
        self.f_dict = self.tk_set_dict('Code')
        self.err_list = self.tk_set_list('Err')
        self.err_key = []
        self.exp_list = self.tk_set_list('Exp')
        self.per_dict = self.tk_set_dict('pnm')
        self.pv_dict = self.tk_set_dict('pvid')
        self.pfin_list = self.tk_set_list('pfin')
        self.pexp_list = self.tk_set_list('pexp')
        self.set_dict = {'Code': self.f_dict,
                         'Cookie': self.cookie,
                         'Err': self.err_list,
                         'Exp': self.exp_list,
                         'pnm': self.per_dict,
                         'pvid': self.pv_dict,
                         'pfin': self.pfin_list,
                         'pexp': self.pexp_list
                         }
        print('初始化完成')

    # 读取字典型配置文件
    def tk_set_dict(self, file_cd, Src_path=''):
        """
        :return : 返回己分析文件列表
        """
        if len(Src_path) == 0:
            fp = self.SettingPath + '\\%s.txt' % file_cd
        else:
            fp = Src_path + '\\%s.txt' % file_cd
        f_dict = {}
        with open(fp, 'r', encoding='utf-8') as rf:
            d_txt = rf.read()
        for d in d_txt.splitlines():
            d = d.split(',')
            f_dict.update({d[0]: d[1]})
        if file_cd == 'Set_menu':
            print('初始化配置成功！')
        else:
            print('读取%s成功！' % self.set_menu.get(file_cd))
        return f_dict

    # 保存字典型配置文件
    def sv_set_dict(self, file_cd, sv_dict={}):
        # 保存文件路径
        fp = self.SettingPath + '\\%s.txt' % file_cd
        if len(sv_dict) == 0:
            wrt_src = self.set_dict.get(file_cd)  # 获取己分析字典
        else:
            wrt_src = sv_dict
        if not isinstance(wrt_src, dict):
            raise Exception('存储类型异常！需要字典类型数据')
        w_txt = ''  # 初始化保存文本
        for k in wrt_src.keys():  # 整合保存文本
            if len(w_txt) == 0:
                w_txt = k + ',' + wrt_src.get(k)
            else:
                w_txt = w_txt + '\n' + k + ',' + wrt_src.get(k)
        with open(fp, 'w', encoding='utf-8') as wf:  # 保存文件
            wf.write(w_txt)
        print('保存%s完成！' % self.set_menu.get(file_cd))

    # 读取序列型配置文件
    def tk_set_list(self, file_cd):
        """
        :return : 读取文件列表
        """
        fp = self.SettingPath + '\\%s.txt' % file_cd  # 保存文件路径
        with open(fp, 'r', encoding='utf-8') as rf:  # 保存文件
            set_txt = rf.read()
        set_list = set_txt.splitlines()
        return set_list

    # 保存序列型配置文件
    def sv_set_list(self, file_cd):
        fp = self.SettingPath + '\\%s.txt' % file_cd  # 保存文件路径
        wrt_list = self.set_dict.get(file_cd)
        if not isinstance(wrt_list, list):
            raise Exception('存储类型异常！需要序列类型数据')
        wrt_txt = '\n'.join(wrt_list)  # 初始化保存文本
        with open(fp, 'w', encoding='utf-8') as wf:  # 保存文件
            wf.write(wrt_txt)
        print('%s记录完成！' % self.set_menu.get(file_cd))