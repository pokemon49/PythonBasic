#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'R18ts文件下载'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

import argparse
import math
import os
import time
from binascii import unhexlify

import execjs
import re
import requests
from requests.adapters import HTTPAdapter
import threadpool
import threading
import random
from Crypto.Cipher import AES

from IndexBar import IndexBar
from pubFunction import pubfunction


class tsFileInte(object):

    # 初始始化参数
    def __init__(self):
        # 默认参数配置
        self.baseUrl = 'x18r.com'
        self.baseInputPath = r'G:\TS\X18R\Source'
        self.baseOutputPath = r'G:\Media\X18R'
        self.verifyFilePath = r'G:\TS\x18r-com-chain.pem'
        self.de_parm = {}
        self.file_list = []  # 存储文件列表
        self.file_list_len = 0
        self.file_downed = set()  # 开始存储文件列表
        self.file_fin_down = set()  # 己完成存储文件列表
        self.lock = threading.Lock()
        self.key_path = r''
        self.m3u8_path = r''
        self.down_path = r''
        self.down_code = ''
        # #定义公用请求头文件
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
        # 进度条实例
        self.idx = IndexBar()
        # 下载请求实例
        self.req = requests.Session()
        # #设置重试次数
        self.req.mount('http://', HTTPAdapter(max_retries=3))
        self.req.mount('https://', HTTPAdapter(max_retries=3))

        # 公共方法
        self.pf = pubfunction()
        # 参数模块
        parser = argparse.ArgumentParser()
        parser.description = '请输入需解析文件路径!'  # 参数介绍
        parser.add_argument('-c', '--fileCode', help='输入文件番号或番号集开头', dest='File_Code', type=str, default="0")  # 文件番号
        parser.add_argument('-o', '--putfilePath', help='输出文件地址', dest='Output_Path', type=str, default="0")  # 文件输出目录
        parser.add_argument('-p', '--perfCode', help='输入人员编号', dest='Perf_Code', type=str, default="0")  # 文件番号
        parser.add_argument('-t', '--thread', help='线程数量', dest='thread_num', type=int, default=5)  # 线程数量
        parser.add_argument('-d', '--downflag', help='下载文件标识：0 己下载文件；1 多线程下载文件 ；3 优化后的多线程下载；2 单线程下载文件',
                            dest='Down_Flag', type=int,
                            default=1, choices=[0, 1, 2, 3])  # 配置下载模式，默认多线程下载模式
        # #参数处理
        args = parser.parse_args()
        self.file_path = self.baseInputPath
        self.file_code = args.File_Code.upper()
        self.output_path = (args.Output_Path != "0" and args.Output_Path or self.baseOutputPath)
        # print(self.output_path)
        self.perf_code = args.Perf_Code
        self.down_flag = args.Down_Flag
        self.thread_num = args.thread_num

    # 文件检查
    def chk_file(self, file_path):
        """
        :param file_path: 文件存储文件夹
        :return ：返回文件完整性检结果

        """
        if not os.path.exists(self.verifyFilePath):
            raise Exception("缺少访问所需证书文件,请检查！")

        fp = file_path
        if not os.path.isdir(fp):
            raise Exception("输入的非文件夹，请输入文件夹路径")
        fl = os.listdir(fp)
        e_key = False
        e_m3u8 = False
        e_add = False
        e_ts = False
        for ft in fl:
            if ft.count('.key') == 1:
                e_key = True
            elif ft.count('.m3u8') == 1:
                e_m3u8 = True
            elif ft.count('add_list') == 1:
                e_add = True
        if not e_key:
            raise Exception("缺少Key文件,请检查！")
        elif not e_m3u8:
            raise Exception("缺少m3u8文件,请检查！")
        elif not e_add and self.down_flag == 1:
            raise Exception("缺少add_list文件,请检查！")
        return True

    # 下载方法
    def file_down(self, url, header={}, rtype=0, stream=True, verify=False):
        """
        :param url: 下载文件路径
        :param header: 请求头信息
        :param stream: 获取内容立即下载开关。默认为True
        :param rtype: 返回类型： 0:返回字节，1：返回文本
        :param verify: 是否需要安全证书链接
        """
        d_url = url
        header = header
        stream = stream
        rtype = rtype
        verify = verify
        if verify:
            response = requests.get(d_url, stream=stream, headers=header, verify=self.verifyFilePath, timeout=7)
        else:
            response = requests.get(d_url, stream=stream, headers=header, timeout=7)

        if response.status_code != 200:
            raise Exception('文件下载错误！地址：%s' % d_url)
        if rtype == 0:
            r_val = response.content
        elif rtype == 1:
            r_val = response.text
        return r_val

    # 获取必要的文件地址
    def tk_fList(self, fp):
        """
        :param fp: 文件存储目录

        """
        self.key_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.key') == 1][0]
        self.m3u8_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.m3u8') == 1][0]
        self.down_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('add_list') == 1][0]
        pass

    # 获取IV值
    @classmethod
    def tk_ViVal(cls, m3p):
        """
        :param m3p: m3u8文件路径
        :return: 返回获取的IV字节码

        """
        m3p = m3p
        m3u8_file = open(m3p, 'r')
        while 1:
            m3u8_line = m3u8_file.readline()
            if not m3u8_line:
                break
            if m3u8_line.count('EXT-X-KEY:') > 0:
                vi_val = m3u8_line[m3u8_line.find('IV=') + 5:]
        m3u8_file.close()
        print('获取IV码成功')
        return unhexlify(vi_val.strip('\n'))

    # 获取Key值
    @classmethod
    def tk_Keyval(cls, file_path):
        """
        :param file_path: Key文件地址
        :return: 返回获取的Key字节码

        """
        file_open = open(file_path, 'rb')
        HexVal = ''
        n = 0
        while 1:
            s = file_open.read(1)
            if not s:
                break
            byte = ord(s)
            HexVal = HexVal + '%02x' % byte
            if n % 16 == 0:
                HexVal == HexVal + chr(16)
        file_open.close()
        print('获取Key码成功')
        return unhexlify(HexVal.upper())  # unhexlify用于将表示16进制的字符串转换为二进制数据

    # 解密部份
    def decrypt(self, data, key, md, iv):
        """
        :param data: 需要解密的字节存储
        :param key:  解密用的Key值
        :param md:   解密模式
        :param iv:   解密用的iv值

        """
        print('\n解密进行中.')
        key = key
        mode = md
        iv = iv
        # 实例化加密套件
        cipher = AES.new(key, mode, iv)
        # 初始化输出内容
        de_data = b''
        de_data = de_data + cipher.decrypt(data)
        print('解密完成.')
        return de_data

    # 下载文件部份
    # #获取下载文件集
    def tk_df_list(self, m3p):
        """
        :param m3p: m3u8文件路径

        """
        m3p = m3p
        m3u8_file = open(m3p, 'r')
        # 文件目录存储
        file_list = []
        while 1:
            m3u8_line = m3u8_file.readline()
            if not m3u8_line:
                break
            if m3u8_line.count('.ts') > 0:
                file_list.append(m3u8_line.replace('\n', ''))
        m3u8_file.close()
        return file_list

    # #获取下载路径集
    def tk_down_list(self, down_path, file_list):
        """
        :param down_link: 下载路径记录文件地址
        :param file_list: 下载文件列表

        """
        fl = file_list
        dp = down_path
        dlf = open(dp, 'r')
        dl = dlf.readline().replace("index0.ts", "").replace('\n', '')
        # dl = dl.replace(dl.split('/')[2], 'svip-ap.japronx.com') # 备用地址，速度慢
        # dl = dl.replace(dl.split('/')[2], 'svip-ea.japronx.com') # 备用地址，速度慢
        dw_list = [dl + ts for ts in fl]
        # 多线程下载路径集
        self.dl_dict = dict(zip(file_list, dw_list))
        # 多线程下载数据集
        self.dd_dict = dict.fromkeys(file_list)
        return dw_list

    # #下载文件
    def down_file(self, dl_list):
        """
        :param dl_list: 下载路径列表

        """
        header = {  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            # 'Host': 'p2-cdn.chuumm.cn',
            # 'Origin': 'https://x18r.com',
            # 'Connection': 'keep-alive'
        }
        # dl_list = ['https://p2-cdn.zhangbk.cn/output/616fa4b45e8ad5b233d84e37d0da67c1/index0.ts', 'https://p2-cdn.zhangbk.cn/output/616fa4b45e8ad5b233d84e37d0da67c1/index1.ts']
        # 进度条参数
        ln = 0
        max_l = len(dl_list)
        max_e = 0
        total_size = 0
        data = b''
        sum_byte = []
        while 1:
            if ln >= max_l:
                break
            dl = dl_list[ln]
            response = requests.get(dl, stream=True, headers=header)
            file_size = response.headers["Content-Length"]
            file_real_size = len(response.content)
            if response.status_code == 200 and int(file_size) == file_real_size:
                sum_byte.append(response.content)
                time.sleep(0.5)
                print(self.idx(ln, max_l, '文件下载进度'), end='')
                ln = ln + 1
                max_e = 0
                total_size = total_size + file_real_size
            else:
                if max_e == 4:
                    raise Exception(dl + '文件下载错误！异常代码：%d' % response.status_code)
                    time.sleep(5)
                max_e = max_e + 1
                pass
        data = data.join(sum_byte)
        return data

    # #多线程下载
    # ##拆分整合文件
    def split_merge(self, file_list, dthred_num):
        # 最终整合变量
        data = b''
        # 任务总数量
        self.ln_max = len(file_list)
        # 折分下载路径
        file_list = file_list
        f_len = len(file_list)
        n = 0
        fthred_list = []
        # 分配线程任务数量
        task_num = math.ceil(f_len / dthred_num)
        for i in range(0, f_len, task_num):
            i_limit = i + task_num
            if i_limit > f_len:
                i_limit = f_len
            fthred_list.append(file_list[i:i_limit])
        # 多线程任务调起（线程池）
        td_pool = threadpool.ThreadPool(dthred_num)
        if self.down_flag == 1:
            re_pool = threadpool.makeRequests(self.thread_down, fthred_list)
        elif self.down_flag == 3:
            re_pool = threadpool.makeRequests(self.optimize_thread_down, fthred_list)
        [td_pool.putRequest(req) for req in re_pool]
        td_pool.wait()
        if len(self.file_downed) == len(self.file_list):
            data = data.join(self.dd_dict.values())
        return data

    # ##线程下载处理
    def thread_down(self, dthred_list):
        """
        :param dthread_list: 下载路径列表

        """
        header = {  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            # 'Host': 'p2-cdn.chuumm.cn',
            # 'Origin': 'https://x18r.com',
            # 'Connection': 'keep-alive'
        }
        # 进度条参数
        ln = 0
        max_l = len(dthred_list)
        max_e = 0
        while 1:
            if ln >= max_l:
                break
            # 获取文件Key值
            d_key = dthred_list[ln]
            # 获取文件下载路径
            dl = self.dl_dict[d_key]
            # print('下载：%s' % dl)
            try:
                response = requests.get(dl, stream=True, headers=header)
                # 获取文件应有大小
                file_size = response.headers["Content-Length"]
                # 获取文件实际大小
                file_real_size = len(response.content)
                if response.status_code == 200 and int(file_size) == file_real_size:
                    self.dd_dict.update({d_key: response.content})
                    time.sleep(1)
                    print(self.idx(ln, max_l, '文件下载进度'), end='')
                    ln = ln + 1
                    max_e = 0
                else:
                    if max_e == 6:
                        raise Exception(dl + '文件下载错误！异常代码：%d' % response.status_code)
                    max_e = max_e + 1
                    pass
            except BaseException:
                print("\n%s 文件下载出错，正重试。" % d_key)
                time.sleep(10)

            # 测试用
            # ln = ln + 1
        pass

    # ##线程下载处理
    def optimize_thread_down(self, dthred_list):
        """
        :param param: 无作用参数

        """
        header = {
            # 'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            # 'Host': 'svip-cdn.chuumm.cn',
            # 'Origin': r'https://x18r.com',
            # 'Referer': r'https://www.x18r.com/',
            # 'Sec-Fetch-Site': r'cross-site',
            # 'Sec-Fetch-Mode': r'cors',
            # 'Sec-Fetch-Dest': r'empty',
            # 'Connection': 'keep-alive'
        }
        ln = 0
        down_st = True
        err_num = 0
        while 1:
            if len(self.file_list) == len(self.file_downed) and down_st:
                break
            if down_st == 'Error':
                print('\n处理异常,文件不存在!')
                break
            # 获取文件Key值
            elif down_st:
                d_key = self.tk_file_key(dthred_list)
            # 获取文件下载路径
            dl = self.dl_dict[d_key]
            try:
                down_st = self.ts_down(d_key, dl, header)
                time.sleep(1)
                ln = len(self.file_downed)
                print(self.idx(ln, self.file_list_len, '文件下载进度'), end='')
            except BaseException as err:
                #if err_num == 3:
                #     break
                down_st = False
                print("\n%s 文件下载出现%s，正重试。" % (d_key, err))
                err_num = err_num + 1
                time.sleep(10)
        pass

    # #多线程处理获取Key值
    def tk_file_key(self, dthred_list=[]):
        down_list = list(set(dthred_list) - (self.file_downed))
        if len(down_list) == 0:
            if len(set(self.file_list) - (self.file_downed)) > 0:
                self.lock.acquire()
                try:
                    key_list = list(set(self.file_list) - (self.file_downed))
                    key = random.choice(key_list)  # key_list[0]
                    self.file_downed.update([key])
                finally:
                    self.lock.release()
            '''
            elif len(set(self.file_list) - self.file_fin_down) > 0:
                key_list = set(self.file_list) - self.file_fin_down
                key = key_list[0]
                pass
            '''
        else:
            key_list = set(dthred_list) - self.file_downed
            key = random.choice(list(key_list))  # key_list[0]
            self.lock.acquire()
            try:
                self.file_downed.update([key])
            finally:
                self.lock.release()
        return key

    # #TS文件下载
    def ts_down(self, d_key, dl, header):
        err = 0
        while err <= 6:
            response = self.req.get(dl, stream=True, headers=header, timeout=7)
            # 获取文件应有大小
            file_size = response.headers["Content-Length"]
            # 获取文件实际大小
            file_real_size = len(response.content)
            if response.status_code == 200 and int(file_size) == file_real_size:
                self.dd_dict.update({d_key: response.content})
                self.file_fin_down.update([d_key])
                err = 0
                return True
                break
            elif response.status_code == 404:
                self.exp_proc()
                return 'Error'
                break
            else:
                if err == 6:
                    raise Exception(dl + '文件下载错误！异常代码：%d' % response.status_code)
                    return False
                err = err + 1

    # #异常番处理
    def exp_proc(self):
        self.lock.acquire()
        try:
            for key in self.pf.f_dict.keys():
                if self.pf.f_dict[key] == self.down_code:
                    if key not in self.pf.err_list:
                        self.pf.err_list.append(key)
                        self.pf.sv_set_list('Err')
                        del self.pf.f_dict[key]
                        self.pf.sv_set_dict('Code')
                        print('成功登记错误及删除完成记录！')
                        src_path = self.baseInputPath + '\\' + self.down_code
                        tar_path = self.baseInputPath + '\\' + self.down_code + '\\Bak'
                        self.copy_file(src_path, tar_path)
                        break
        finally:
            self.lock.release()

    # #复制文件方法
    def copy_file(self, src_path, tar_path):
        if not os.path.exists(tar_path):
            os.makedirs(tar_path, exist_ok=True)
            print('成功创建备份文件夹')
        for file in os.listdir(src_path):
            src_file = src_path + '\\' + file
            tar_file = tar_path + '\\' + file
            if not os.path.isdir(src_file):
                with open(src_file, 'rb') as rf:
                    file_byte = rf.read()
                with open(tar_file, 'wb') as wf:
                    wf.write(file_byte)
                os.remove(src_file)
        print('成功进行异常文件备份！')
        pass

    # 判断是否己下载完成
    def is_finish(self, src_path):
        """
        :param src_path: 存储配置文件的目录
        :return 是否未完成的结果

        """
        f_list = os.listdir(src_path)
        for f in f_list:
            if f.count('finish') > 0:
                result = False
                break
            result = True
        return result

    # 整合部份
    def integration(self, ts_list):
        """
        :param ts_list: ts文件列表

        """
        ts_list = ts_list
        ts_inte = b''
        ln = 1
        max_l = len(ts_list)
        sum_byte = []
        for ts in ts_list:
            ts_read = open(ts, 'rb')
            sum_byte.append(ts_read.read())
            print(self.idx(ln, max_l, '文件整合进度'), end='')
            ln = ln + 1
            ts_read.close()
        ts_inte = ts_inte.join(sum_byte)
        return ts_inte
        pass

    # 获取待下载列表
    def tk_src_list(self):
        """
        :return 返回文件集

        """
        bpath = self.baseInputPath
        down_dict = {}
        if self.file_code == "0":
            if self.perf_code == "0":
                cd_list = os.listdir(bpath)
                d_list = [bpath + '\\' + fk for fk in cd_list]
                down_dict = dict(zip(cd_list, d_list))
            elif self.perf_code in list(self.pf.per_dict.keys()):
                id_list = self.pf.pv_dict.get(self.perf_code).split('|')
                cd_list = [self.pf.f_dict.get(id) for id in id_list if id in list(self.pf.f_dict.keys())]
                loss_id = set(id_list) - set(self.pf.f_dict.keys())
                # 未获取到番号的异常处理
                if len(loss_id) > 0:
                    self.pf.err_list = self.pf.err_list + list(loss_id)
                    self.pf.sv_set_list('Err')
                sp_list = [bpath + '\\' + cd for cd in cd_list]
                down_dict = dict(zip(cd_list, sp_list))
            elif self.perf_code not in list(self.pf.per_dict.keys()):
                raise Exception('人员编号错误！请核对后再输入。')
        elif self.file_code.find('-') > 0:
            if self.file_code.find(',') > 0:
                cd_list = self.file_code.split(',')
                sp_list = [bpath + '\\' + cd for cd in cd_list]
                down_dict = dict(zip(cd_list, sp_list))
            else:
                f_path = bpath + '\\' + self.file_code
                down_dict.update({self.file_code: f_path})
        else:
            cd_list = os.listdir(bpath)
            cd_list = [cd for cd in cd_list if cd.startswith(self.file_code)]
            fp_list = [bpath + '\\' + fk for fk in cd_list if fk.startswith(self.file_code)]
            down_dict = dict(zip(cd_list, fp_list))
        return down_dict

    # 本地下载程序入口
    def local_down(self, src_path):
        # #获取完成标识
        is_notfin = self.is_finish(src_path)
        if is_notfin:
            # #更新需要的文件地址
            self.tk_fList(src_path)
            # #获取Key值
            key = self.tk_Keyval(self.key_path)
            # #获取iv值
            iv = self.tk_ViVal(self.m3u8_path)
            # #获取下载文件列表
            fl = self.tk_df_list(self.m3u8_path)
            self.file_list = fl
            # #获取文件集
            self.file_list_len = len(fl)
            # 组合下载路径集
            dl = self.tk_down_list(self.down_path, fl)

            # 下载部份
            if self.down_flag == 0:  # 己有文件整合
                print('文件合并任务')
                ts_list = self.ts_list
                data = self.integration(ts_list)
            elif self.down_flag in (1, 3):  # 多线程下载文件整合
                print('开始多线程下载任务')
                data = self.split_merge(fl, self.thread_num)
            elif self.down_flag == 2:  # 单线程下载文件整合
                print('开始单线程下载任务')
                data = self.down_file(dl)

            # 解密部份
            if len(data) > 0:
                print('文件下载完成！')
                # #设置解密模式
                md = AES.MODE_CBC
                # #解密调用
                de_data = self.decrypt(data, key, md, iv)
                sv_path = self.output_path + '\\' + self.down_code + '.ts'
                # #写入文件
                with open(sv_path, 'wb') as wf:
                    wf.write(de_data)
                print(sv_path + '转换完成')
                # 完成标识
                find_path = src_path + '\\finish'
                with open(find_path, 'w') as wf:
                    wf.write('Finish')
                print('文件转换完成!')
        else:
            print('文件己下载完成！')

    # 主调用方法
    def run(self):
        st_tm = time.time()  # 获取程序开始时间
        # 获取源文件集
        src_dict = self.tk_src_list()
        tsk_tot = len(src_dict)
        print('共获取%d个任务' % tsk_tot)
        tsk_now = 1
        # 开始下载
        for code in src_dict.keys():
            sub_st_tm = time.time()  # 获取程序开始时间
            print('[%d/%d]%s号任务开始' % (tsk_now, tsk_tot, code))
            self.down_code = code
            self.local_down(src_dict[code])
            self.file_downed.clear()
            self.file_fin_down.clear()
            tsk_now = tsk_now + 1
            sub_end_tm = time.time() - sub_st_tm
            # 转换时间格式
            m, s = divmod(sub_end_tm, 60)
            h, m = divmod(m, 60)
            # 显示耗时
            print("耗时：%d:%02d:%02d" % (h, m, s))

        # 获取耗时
        use_sc = time.time() - st_tm
        # 转换时间格式
        m, s = divmod(use_sc, 60)
        h, m = divmod(m, 60)
        # 显示耗时
        print("总耗时：%d:%02d:%02d" % (h, m, s))


tfi = tsFileInte()
tfi.run()
