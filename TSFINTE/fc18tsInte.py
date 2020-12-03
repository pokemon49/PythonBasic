#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'FC18网站下载功能'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

import os
import time
import requests
import threadpool
import re
import math
import argparse
from IndexBar import IndexBar
from lxml import etree


class fc18tsInte(object):
    # 初始始化参数
    def __init__(self):
        # 默认参数配置
        self.baseUrl = 'fc.aa1804.com'
        self.baseUrl_xp = 'aa1804.com'
        self.baseInputPath = r'G:\TS\FC18'
        self.baseOutputPath = r'E:\My Document\Downloads\Merger\FC18'
        self.verifyFilePath = r'G:\TS\fc-aa1804-com-chain.pem'
        self.verifyFilePath_xp = r'G:\TS\sni-cloudflaressl-com-chain.pem'
        self.de_parm = {}
        # #定义公用请求头文件
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
        # 参数模块
        parser = argparse.ArgumentParser()
        parser.description = '请输入需解析文件路径!'  # 参数介绍
        parser.add_argument('-k', '--vkey', help='下载文件Key值输入', dest='File_key', type=str,
                            default="0")  # 配置下载模式，默认多线程下载模式
        parser.add_argument('-c', '--Channel', help='下载文件渠道: fc/xp', dest='Source_channel', type=str,
                            default="fc", choices=["fc", "xp"])  # 配置下载模式，默认多线程下载模式
        parser.add_argument('-t', '--type', help='文件类型: v/p', dest='File_type', type=str,
                            default="v", choices=["v", "p"])  # 配置下载模式，默认多线程下载模式
        parser.add_argument('-o', '--OutputPath', help='下载文件存储路径', dest='Output_Path', type=str,
                            default="0")  # 配置下载模式，默认多线程下载模式
        parser.add_argument('-l', '--ListFlag', help='列表更新标识', dest='List_Flag', type=str,
                            default="n", choices=["y", "n"])  # 配置下载模式，默认多线程下载模式
        # #参数处理
        args = parser.parse_args()
        self.file_key = args.File_key
        self.sc = args.Source_channel
        self.ft = args.File_type
        if args.Output_Path != "0":
            self.baseOutputPath = args.Output_Path
        self.lf = args.List_Flag
        # 进度条实例
        self.idx = IndexBar()
        # self.ln = 0
        # self.lock = threading.Lock()
        # PHPSession处理
        self.phpsession = self.tk_session()


    # 解析番号
    def tk_vcd(self):
        '''
        # 拼接访问网站地址
        v_url = r'https://%s/index.php/portal/index/detail/identification/%s.html' % (self.baseUrl, self.file_key)
        body_txt = self.file_down(v_url, rtype=1, verify=True, header=self.header)  # 访问网站
        # 获取番号
        vcd = re.search(r'<dd><a class="no-hover">\S+', body_txt, re.I).group().replace('<dd><a class="no-hover">',
                                                                                        '').replace('</a></dd>', '')
        # 获取番号异常处理
        if len(vcd) > 15:
            raise Exception('番号获取异常，请检查！%s' % vcd)
        # 创建文件夹
        # #组合存储目录
        vdir = self.baseInputPath+'\\'+vcd
        if not os.path.exists(vdir):
            os.mkdir(vdir)
        self.vdir = vdir
        self.vcd = vcd
        print('获取番号成功！')
        '''
        pass

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
            if self.sc == 'fc':
                response = requests.get(d_url, stream=stream, headers=header, verify=self.verifyFilePath)
            elif self.sc == 'xp':
                response = requests.get(d_url, stream=stream, headers=header, verify=self.verifyFilePath_xp)
        else:
            response = requests.get(d_url, stream=stream, headers=header)

        if response.status_code != 200:
            raise Exception('文件下载错误！地址：%s' % d_url)
        if rtype == 0:
            r_val = response.content
        elif rtype == 1:
            r_val = response.text
        return r_val

    # 获取PHPSESSION
    def tk_session(self):
        # PHPSESSID获取
        SESSION_URL = r'https://aa1804.com/wtydfAA.htm'
        s = requests.session()
        res = s.get(SESSION_URL, stream=True)
        c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        c.set('cookie-name', 'cookie-value')
        s.cookies.update(c)
        session = s.cookies.get_dict().get('PHPSESSID')
        return session

    # 获取下载配置文件
    def tk_set_file(self):
        if self.sc == 'fc':
            play_url = 'https://%s/fcfluidplayer.php?id=%s' % (self.baseUrl, self.file_key)  # 拼出链接地址
            # 定义请求头文件
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
            body_txt = self.file_down(url=play_url, header=header, rtype=1, stream=False, verify=True)  # 存储m3u8地址的网页
            # 提取m3u8地址
            m3u8_url = re.search(r"<source src=\S+.m3u8", body_txt, re.I).group().replace('<source src=', '') \
                                                                                 .replace("'", '')
            m3u8_nm = m3u8_url.split('/')[5].replace('.m3u8', '')
        elif self.sc == 'xp':
            play_url = 'https://%s/xpmv/%.html' % (self.baseUrl_xp, self.file_key)  # 拼出链接地址
            # 定义请求头文件
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
                      'Cookie': '__cfduid=dc636dab1b027af948b76c1e9d09f0ee61597587275; PHPSESSID=%s' % self.phpsession +
                                '42hp712; TSCvalue=gb; javascript_cookie_Eighteenth=I_am_over_18_years_old'}
            body_txt = self.file_down(url=play_url, header=header, rtype=1, stream=False, verify=True)  # 存储m3u8地址的网页
            # 提取m3u8地址
            m3u8_url = re.search(r"<source src=\S+", body_txt, re.I).group().replace('<source src=', '')\
                                                                            .replace("'", '')
            m3u8_nm = m3u8_url.split('/')[3].replace('.m3u8', '')
        # 临时处理
        self.vdir = self.baseInputPath + '\\' + m3u8_nm
        self.vcd = m3u8_nm
        if not os.path.exists(self.vdir):
            os.mkdir(self.vdir)
        # 未获取到文件链接地址处理
        if len(m3u8_url) == 0:
            raise Exception('未解析出M3u8文件地址！')
        else:
            m3u8_txt = self.file_down(url=m3u8_url, header=header, rtype=1, stream=False)  # 访问地址获取内容
            # 存储M3U8配置文件
            m3u8_path = self.vdir + '\\index.m3u8'
            with open(m3u8_path, 'w') as m3u8_w:
                m3u8_w.write(m3u8_txt)
            # 存储完成提示
            print('M3U8文件己存储完成！')
            # 存储访问文件地址
            ts_url = m3u8_url[:35]
            url_path = self.vdir + '\\add_list.txt'
            with open(url_path, 'w') as url_w:
                url_w.write(ts_url)
                url_w.write(chr(10) + m3u8_url)
            # 存储完成提示
            print('配置文件己存储完成！')
            # 传递Key和IV值
            self.de_parm.update({'tsPath': ts_url})
            self.de_parm.update({'m3Path': m3u8_path})
            self.de_parm.update({'urlPath': url_path})

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
        re_pool = threadpool.makeRequests(self.thread_down, fthred_list)
        [td_pool.putRequest(req) for req in re_pool]
        td_pool.wait()
        if self.ft == 'v':
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

    # 下载文件部份
    # #获取下载文件集
    def tk_df_list(self, m3p):
        """
        :param m3p: m3u8文件路径
        :return: 返回下载文件集

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
                file_list.append(m3u8_line.strip())
        m3u8_file.close()
        return file_list

    # #获取下载路径集
    def tk_down_list(self, down_path, file_list):
        """
        :param down_link: 下载路径记录文件地址
        :param file_list: 下载文件列表
        :return: 返回下载路径集

        """
        fl = file_list
        dp = down_path
        dlf = open(dp, 'r')
        dl = dlf.readline().replace("index0.ts", "").replace('\n', '')
        dw_list = [dl + ts for ts in fl]
        # 多线程下载路径集
        self.dl_dict = dict(zip(file_list, dw_list))
        # 多线程下载数据集
        self.dd_dict = dict.fromkeys(file_list)
        return dw_list

    # #XP渠道下载路径集
    def tk_xp_list(self, m3p):
        """
        :param m3p: m3u8文件路径
        :return: 返回下载路径集
        """
        m3p = m3p
        m3u8_file = open(m3p, 'r')
        # 文件目录存储
        dw_list = []
        while 1:
            m3u8_line = m3u8_file.readline()
            if not m3u8_line:
                break
            if m3u8_line.count('.ts') > 0:
                dw_list.append(m3u8_line.strip())
        m3u8_file.close()
        file_list = [f[f.rfind('/')+1:] for f in dw_list]
        # 多线程下载路径集
        self.dl_dict = dict(zip(file_list, dw_list))
        # 多线程下载数据集
        self.dd_dict = dict.fromkeys(file_list)
        return dw_list

    # #图片下载集
    def tk_pict_list(self, fkey):
        """
            :param fkey: 文件Key值
            :return: 返回下载路径集
        """
        file_key = fkey
        pict_url = 'https://' + self.baseUrl_xp + '/' + file_key + '.html'  # 组合链接地址
        # ##组合访问PHPSESSION信息
        cookie = {'Cookie':'__cfduid=dc636dab1b027af948b76c1e9d09f0ee61597587275; PHPSESSID=%s' % self.phpsession +
                           '; TSCvalue=gb; javascript_cookie_Eighteenth=I_am_over_18_years_old'}
        header = self.header
        header.update(cookie)  # 组合访问请求头文件
        pict_txt = self.file_down(url=pict_url, header=header, rtype=1, stream=False, verify=True)
        html_txt = etree.HTML(pict_txt)  # HTML格式化
        li_list = html_txt.xpath('/html/body/div/center/h1/text()')
        # ##获取文件名称
        for li in li_list:
            self.pict_nm = li
        # ##存储图片地址信息的脚本地址
        pag_list = html_txt.xpath('//script[@language="javascript"]/text()')
        # ##配置正则表达式
        jpg_re = re.compile(r'https://\S+.jpg', re.I)
        for pag in pag_list:
            result = jpg_re.findall(pag)
        pict_nm_list = [pict_nm.split('/')[-1] for pict_nm in result]
        # 多线程下载路径集
        self.dl_dict = dict(zip(pict_nm_list, result))
        # 多线程下载数据集
        self.dd_dict = dict.fromkeys(pict_nm_list)
        return pict_nm_list

    # #存储图片集
    def save_pict(self, pict_list):
        save_path = self.baseOutputPath + '\\' + self.pict_nm  # 组合存储目录地址
        if not os.path.exists(save_path):                      # 创建文件夹
            os.mkdir(save_path)
            print("存储文件夹创建成功！")
        # ##获取文件列表
        file_list = pict_list
        for file in file_list:
            # ##组合文件存储地址
            save_file = save_path + '\\' + file
            # ##获取文件内容
            save_byte = self.dd_dict.get(file)
            # ##存储文件
            with open(save_file, 'wb') as sf:
                sf.write(save_byte)
        print('存储成功!')

    # #获取视频链接地址
    def tk_voide_list(self, url):
        url = url
        # ##组合访问PHPSESSION信息
        cookie = {'Cookie':'__cfduid=dc636dab1b027af948b76c1e9d09f0ee61597587275; PHPSESSID=%s' % self.phpsession +
                           '; TSCvalue=gb; javascript_cookie_Eighteenth=I_am_over_18_years_old'}
        header = self.header
        header.update(cookie)  # 组合访问请求头文件
        response = requests.get(url, stream=False, headers=header, verify=self.verifyFilePath_xp, timeout=30)
        body_txt = response.text
        # ##整理HTML文件及Html文件格式化
        html_txt = etree.HTML(body_txt.replace("<span class='di_img'>", "<!--<span class='di_img'>").replace(
            '<span id="friendLink"></span>', '<span id="friendLink"></span>-->'))
        # ##获取链接地址
        lk_list = html_txt.xpath('//span [@id="main"]/a/@href')
        # ##获取链接地址
        nm_list = html_txt.xpath('//*[@id="main"]/a/img/@alt')
        vm_d = dict(zip(lk_list, nm_list))
        vlk_d = dict.fromkeys(lk_list)
        n = 0
        while n < len(lk_list):
            try:
                lk = lk_list[n]
                time.sleep(1)
                lk_url = 'https:' + lk
                response = requests.get(lk_url, stream=False, headers=header, verify=self.verifyFilePath_xp, timeout=30)
                body_txt = response.text
                lk_re = re.compile(r'https://\S+id=\d+_\S+"')
                result = lk_re.findall(body_txt)
                vlk_d.update({lk: result})
                n = n + 1
                print("获取成功！")
            except Exception:
                print("%d获取失败！等待十秒后重试" % n)
                time.sleep(10)
        for lk in lk_list:
            print(vm_d.get(lk))
            print(vlk_d.get(lk))

    # #主调用方法
    def run(self):
        if self.file_key == '0' and self.lf == 'n':
            pass
        elif len(self.file_key) == 16 and self.ft == 'v' and self.lf == 'n':
            self.tk_vcd()
            # ##下载配置文件
            self.tk_set_file()
            # ##获取M3U8文件地址
            self.m3u8_path = self.de_parm.get('m3Path')
            # ##获取路径文件地址
            self.down_path = self.de_parm.get('urlPath')
            # ##存储路径
            self.output_path = self.baseOutputPath + '\\' + self.vcd + '.ts'
            # 获取下载文件集
            fl = self.tk_df_list(self.m3u8_path)
            # 组合下载路径集
            dl = self.tk_down_list(self.down_path, fl)
            # 文件下载
            print('开始多线程下载任务')
            data = self.split_merge(fl, 5)
            print('\n文件下载完成！')
            # 写入
            with open(self.output_path, 'wb') as wf:
                wf.write(data)
                print(self.output_path + '写入完成')
        elif len(self.file_key) == 8 and self.ft == 'p' and self.lf == 'n':
            pict_list = self.tk_pict_list(self.file_key)
            print('开始多线程下载任务')
            self.split_merge(pict_list, 5)
            self.save_pict(pict_list)
            pass
        elif self.lf == 'y':
            url = r'https://aa1804.com/serch_18av/%E4%B8%AD%E6%96%87%E5%AD%97%E5%B9%95%E5%85%A8%E9%83%A8%E5%88%97%E8%A1%A8_1.htm'
            self.tk_voide_list(url)
            pass


fc = fc18tsInte()
fc.run()
