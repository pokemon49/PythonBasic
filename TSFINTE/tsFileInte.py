#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'TS文件整合'
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
from Crypto.Cipher import AES

from IndexBar import IndexBar


class tsFileInte(object):

    # 初始始化参数
    def __init__(self):
        # 默认参数配置
        self.baseUrl = 'x18r.com'
        self.baseInputPath = r'G:\TS'
        self.baseOutputPath = r'E:\My Document\Downloads\Merger'
        self.PrivateOutputPath = r'G:\TS\X18R\Source'
        self.verifyFilePath = r'G:\TS\x18r-com-chain.pem'
        self.de_parm = {}
        self.file_list = []   # 存储文件列表
        self.file_list_len = 0
        self.file_downed = []  # 己完成存储文件列表
        self.lock = threading.Lock()
        # #定义公用请求头文件
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
        # 下载请求实例
        self.req = requests.Session()
        # #设置重试次数
        self.req.mount('http://', HTTPAdapter(max_retries=3))
        self.req.mount('https://', HTTPAdapter(max_retries=3))
        # 参数模块
        parser = argparse.ArgumentParser()
        parser.description = '请输入需解析文件路径!'  # 参数介绍
        parser.add_argument('-f', '--fileMenuPath', help='输入目录地址', dest='File_Path', type=str, default="0")  # 文件存放目录
        parser.add_argument('-o', '--putfilePath', help='输出文件地址', dest='Output_Path', type=str, default="0")  # 文件输出目录
        parser.add_argument('-d', '--downflag', help='下载文件标识：0 己下载文件；1 多线程下载文件 ；3 优化后的多线程下载；2 单线程下载文件', dest='Down_Flag', type=int,
                            default=1, choices=[0, 1, 2, 3])  # 配置下载模式，默认多线程下载模式
        parser.add_argument('-k', '--vkey', help='下载文件Key值输入', dest='File_key', type=str,
                            default="0")  # 配置下载模式，默认多线程下载模式
        # #参数处理
        args = parser.parse_args()
        self.file_path = args.File_Path
        self.output_path = args.Output_Path
        self.down_flag = args.Down_Flag
        self.file_key = args.File_key
        fp = self.file_path
        if self.file_key == '0' and self.chk_file(fp):
            self.ts_list = sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 9]) \
                           + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 10]) \
                           + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 11]) \
                           + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 12])
            self.key_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.key') == 1][0]
            self.m3u8_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.m3u8') == 1][0]
            if self.down_flag in (1, 3):
                self.down_path = [fp + '\\' + ts for ts in os.listdir(fp) if ts.count('add_list') == 1][0]

        # 进度条实例
        self.idx = IndexBar()
        # self.ln = 0
        # self.lock = threading.Lock()

    # 解析番号
    def tk_vcd(self):
        # 拼接访问网站地址
        v_url = r'https://%s/index.php/portal/index/detail/identification/%s.html' % (self.baseUrl, self.file_key)
        body_txt = self.file_down(v_url, rtype=1, verify=True, header=self.header)  # 访问网站
        # 获取番号
        vcd = re.search(r'<dd><a class="no-hover">\S+', body_txt, re.I).group().replace('<dd><a class="no-hover">',
                                                                                        '').replace('</a></dd>', '')
        print('获取番号成功！')
        # 获取番号异常处理
        if len(vcd) > 15:
            raise Exception('番号获取异常，请检查！%s' % vcd)
        # 创建文件夹
        # #组合存储目录
        vdir = self.baseInputPath+'\\'+vcd
        if not os.path.exists(vdir):
            os.mkdir(vdir)
            print('创建文件夹成功！')
        self.vdir = vdir
        self.vcd = vcd

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

    # 解密Javascript
    def de_js(self, jstxt):
        """
        :param jstxt: 加密的JS文件
        :return :解密后的JS文件
        """
        result = {}
        js = jstxt
        js = js[5:len(js) - 2]
        js = js.replace("c35?", "c<a?'':e(parseInt(c/a)))+((c=c%a)>35?")  # 补全加密文本段
        js_txt = execjs.eval(js.rstrip())  # 解密脚本
        m3u8_url = re.search(r'https://\S+expires=\d+', js_txt, re.I).group()  # 获取m3u8文件链接地址
        pict_url = re.search(r'https://image.\S+png|jpge', js_txt, re.I).group()  # 获取封面图片链接地址
        result.update({'m3u8_url': m3u8_url})
        result.update({'pict_url': pict_url})
        print('解密JavaScript文件成功！')
        return result

    # 获取下载配置文件
    def tk_set_file(self):
        set_url = 'https://%s/portal/index/ekzloi_1.html?identification=%s&lang=zh' % (
            self.baseUrl, self.file_key)  # 拼出链接地址
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}  # 定义请求头文件
        en_js = self.file_down(url=set_url, header=header, rtype=1, stream=False, verify=True)  # 访问地址获取内容
        url_dict = self.de_js(en_js)  # 解密Javascript脚本
        m3u8_url = url_dict.get('m3u8_url', -1)  # 获取M3U8文件链接地址
        # 未获取到文件链接地址处理
        if m3u8_url == -1:
            raise Exception('未解析出M3u8文件地址！')
        else:
            # 获取M3U8内容
            m3u8_txt = self.file_down(url=m3u8_url, header=header, rtype=1, stream=False)  # 访问地址获取内容
            # 获取Key文件地址
            key_url = m3u8_txt[m3u8_txt.find('URI="') + 5:m3u8_txt.find('.key') + 4]
            # 获取IV值
            iv_val = unhexlify(m3u8_txt[m3u8_txt.find('IV=') + 5:m3u8_txt.find('IV=') + 37].strip('\n'))
            key_name = key_url[key_url.find('keys/') + 5:key_url.find('.key')]
            # 存储M3U8配置文件
            m3u8_path = self.vdir+'\\index.m3u8'
            with open(m3u8_path, 'w') as m3u8_w:
                m3u8_w.write(m3u8_txt)
            # 存储完成提示
            print('M3U8文件己存储完成！')
        # 获取解密用Key内容
        key_code = self.file_down(url=key_url, header=header, rtype=0, stream=False, verify=True)  # 访问地址获取内容
        key_val = key_code
        # 存储Key文件
        key_path = self.vdir + '\\'+key_name+'.key'
        with open(key_path, 'wb') as key_w:
            key_w.write(key_code)
        # 存储完成提示
        print('Key文件己存储完成！')
        # 存储访问文件地址
        ts_url = m3u8_url[:m3u8_url.find('index.m3u8')]
        url_path = self.vdir+'\\add_list.txt'
        with open(url_path, 'w') as url_w:
            url_w.write(ts_url)
            url_w.write(chr(10)+m3u8_url)
            url_w.write(chr(10)+set_url)
        # 存储完成提示
        print('配置文件己存储完成！')
        # 传递Key和IV值
        self.de_parm.update({'key': key_val})
        self.de_parm.update({'IV': iv_val})
        self.de_parm.update({'tsPath': ts_url})
        self.de_parm.update({'m3Path': m3u8_path})
        self.de_parm.update({'urlPath': url_path})

    # 文件检查
    def chk_file(self, file_path):
        """
        :param file_path: 文件存储文件夹

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
            elif ft.count('.ts') == 1:
                e_ts = True
        if not e_key:
            raise Exception("缺少Key文件,请检查！")
        elif not e_m3u8:
            raise Exception("缺少m3u8文件,请检查！")
        elif not e_add and self.down_flag == 1:
            raise Exception("缺少add_list文件,请检查！")
        elif not e_ts and self.down_flag == 0:
            raise Exception("缺少ts文件,请检查")
        return True

    # 获取必要的文件地址
    def tk_fList(self, fp):
        """
        :param fp: 文件存储目录

        """
        fp = fp
        self.ts_list = sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 9]) \
                       + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 10]) \
                       + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 11]) \
                       + sorted([fp + '\\' + ts for ts in os.listdir(fp) if ts.count('.ts') == 1 and len(ts) == 12])
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
        # dl = dl.replace(dl.split('/')[2], 'svi3-cdn.aoborl.com') 备用地址，速度慢
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
            # if ln >= 10: # 测试用
            #    break
            dl = dl_list[ln]
            response = requests.get(dl, stream=True, headers=header)
            file_size = response.headers["Content-Length"]
            file_real_size = len(response.content)
            # print(file_size + '||' + str(len(response.content)))
            if response.status_code == 200 and int(file_size) == file_real_size:
                # data = data + response.content
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
        # 多线程任务调起
        """
        t1 = threading.Thread(target=self.thread_down, name='DownThread-1', args=(fthred_list[0], ))
        t2 = threading.Thread(target=self.thread_down, name='DownThread-2', args=(fthred_list[1], ))
        t3 = threading.Thread(target=self.thread_down, name='DownThread-3', args=(fthred_list[2], ))
        t4 = threading.Thread(target=self.thread_down, name='DownThread-4', args=(fthred_list[3], ))
        t5 = threading.Thread(target=self.thread_down, name='DownThread-5', args=(fthred_list[4], ))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        """
        # 多线程任务调起（线程池）
        td_pool = threadpool.ThreadPool(dthred_num)
        if self.down_flag == 1:
            re_pool = threadpool.makeRequests(self.thread_down, fthred_list)
        elif self.down_flag == 3:
            re_pool = threadpool.makeRequests(self.optimize_thread_down, fthred_list)
        [td_pool.putRequest(req) for req in re_pool]
        td_pool.wait()
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
        # dl_list = ['https://p2-cdn.zhangbk.cn/output/616fa4b45e8ad5b233d84e37d0da67c1/index0.ts',
        #            'https://p2-cdn.zhangbk.cn/output/616fa4b45e8ad5b233d84e37d0da67c1/index1.ts']
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
                    # self.lock.acquire()
                    # try:
                    #     self.ln = self.ln + 1
                    # finally:
                    #     self.lock.release()
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
    def optimize_thread_down(self, param):
        """
        :param param: 无作用参数

        """
        header = {  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                    # 'Host': 'p2-cdn.chuumm.cn',
                    # 'Origin': 'https://x18r.com',
                    # 'Connection': 'keep-alive'
                 }
        ln = 0
        max_e = 0
        err = False
        while 1:
            if len(self.file_list) == 0:
                break
            # 获取文件Key值
            if not err:
                d_key = self.tk_file_key()
                err = False
            # 获取文件下载路径
            dl = self.dl_dict[d_key]
            # print('下载：%s' % dl)
            try:
                response = self.req.get(dl, stream=True, headers=header)
                # 获取文件应有大小
                file_size = response.headers["Content-Length"]
                # 获取文件实际大小
                file_real_size = len(response.content)
                if response.status_code == 200 and int(file_size) == file_real_size:
                    self.dd_dict.update({d_key: response.content})
                    time.sleep(1)
                    ln = len(self.file_downed)
                    print(self.idx(ln, self.file_list_len, '文件下载进度'), end='')
                    max_e = 0
                else:
                    if max_e == 6:
                        raise Exception(dl + '文件下载错误！异常代码：%d' % response.status_code)
                    max_e = max_e + 1
                    err = True
                    pass
            except BaseException:
                print("\n%s 文件下载出错，正重试。" % d_key)
                err = True
                time.sleep(10)

            # 测试用
            # ln = ln + 1
        pass

    # #多线程处理获取Key值
    def tk_file_key(self):
        self.lock.acquire()
        try:
            key = self.file_list[0]
            self.file_list.pop(0)
            self.file_downed.append(key)
        finally:
            self.lock.release()
        return key

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
            # ts_inte = ts_inte + ts_read.read()
            sum_byte.append(ts_read.read())
            print(self.idx(ln, max_l, '文件整合进度'), end='')
            ln = ln + 1
            ts_read.close()
        ts_inte = ts_inte.join(sum_byte)
        return ts_inte
        pass

    # 主调用方法
    def run(self):
        """
        # 测试用参数区间
        self.tk_fList('G:\TS\SSNI-826')
        self.output_path = r'E:\SSNI-826.ts'
        # key = unhexlify('7FD0DF14400E450FDCB82C13A0F77767')
        # iv = unhexlify('d7116a13601de7b92b1ea26d657ad5e2')
        # print('key:%s' % str(key))
        # print('iv:%s' % str(iv))
        """
        st_tm = time.time()  # 获取程序开始时间
        if self.file_key == '0':
            # 获取Key值
            key = self.tk_Keyval(self.key_path)
            # 获取iv值
            iv = self.tk_ViVal(self.m3u8_path)
            is_notfin = self.is_finish(self.file_path)
        else:
            self.tk_vcd()
            self.tk_set_file()
            key = self.de_parm.get('key')
            iv = self.de_parm.get('iv')
            is_notfin = self.de_parm.get('tsPath')
            self.m3u8_path = self.de_parm.get('m3Path')
            self.down_path = self.de_parm.get('urlPath')
            self.output_path = self.baseOutputPath+'\\'+self.vcd+'.ts'

        if self.down_flag != 0 and is_notfin:
            # 获取下载文件集
            fl = self.tk_df_list(self.m3u8_path)
            self.file_list = fl
            self.file_list_len = len(fl)
            # 组合下载路径集
            dl = self.tk_down_list(self.down_path, fl)

        if is_notfin:
            # 文件下载
            if self.down_flag == 0:  # 己有文件整合
                # ts_list = ['G:\TS\HND-863\index0.ts']
                print('文件合并任务')
                ts_list = self.ts_list
                data = self.integration(ts_list)
            elif self.down_flag in (1, 3):  # 多线程下载文件整合
                print('开始多线程下载任务')
                data = self.split_merge(fl, 5)
            elif self.down_flag == 2:  # 单线程下载文件整合
                print('开始单线程下载任务')
                data = self.down_file(dl)
            print('文件下载完成！')

            # 设置解密模式
            md = AES.MODE_CBC

            # 解密调用
            de_data = self.decrypt(data, key, md, iv)
            with open(self.output_path, 'wb') as wf:
                wf.write(de_data)
            print(self.output_path + '转换完成')
            # 完成标识
            if self.file_path == '0':
                find_path = self.vdir + '\\' + 'finish'
            else:
                find_path = self.file_path + '\\' + 'finish'
            with open(find_path, 'w') as wf:
                wf.write('Finish')
            private_path = self.PrivateOutputPath + '\\' + self.vcd
            if not os.path.exists(private_path):
                os.mkdir(private_path)
            else:
                private_find_path = private_path + '\\' + 'finish'
                with open(private_find_path, 'w') as wf:
                    wf.write('Finish')
            print('登记结束完成!')
        else:
            print('文件己下载完成！')

        # 获取耗时
        use_sc = time.time() - st_tm
        # 转换时间格式
        m, s = divmod(use_sc, 60)
        h, m = divmod(m, 60)
        # 显示耗时
        print("总耗时：%d:%02d:%02d" % (h, m, s))


tfi = tsFileInte()
tfi.run()
