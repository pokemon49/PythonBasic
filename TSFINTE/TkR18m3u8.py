#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '获取r18的M3u8文件'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

import argparse
import requests
import execjs
from Crypto.Cipher import AES
from binascii import unhexlify
import os
import re
from lxml import etree
import time
import random


class TkR18m3u8(object):

    # 初始始化参数
    def __init__(self):
        # 默认参数配置
        self.baseUrl = 'x18r.com'
        self.baseInputPath = r'G:\TS\X18R'
        self.SourcePath = self.baseInputPath + r'\Source'
        self.SettingPath = self.baseInputPath + r'\Setting'
        self.baseOutputPath = r'E:\My Document\Downloads\Merger'
        self.verifyFilePath = r'G:\TS\x18r-com-chain.pem'
        self.de_parm = {}
        # #定义公用请求头文件
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'}
        # #功能性对像配置
        self.ra = random
        # #存储变量配置
        self.set_menu = self.tk_set_dict('Set_menu')
        self.cookie = self.tk_cookie()
        self.f_dict = self.tk_analysis()
        self.err_list = self.tk_err_key()
        self.err_key = []
        self.exp_list = self.tk_exp_key()
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
                         'pexp': self.pexp_list}
        print('读取配置完成')

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
        js = js.replace("c35?", "c<a?'':e(parseInt(c/a)))+((c=c%a)>35?", 1)  # 补全加密文本段
        js_txt = execjs.eval(js.rstrip())  # 解密脚本
        # print(js_txt) 测试验证用
        m3u8_url = re.search(r'https://\S+expires=\d+', js_txt, re.I).group()  # 获取m3u8文件链接地址
        pict_url = re.search(r'https://image.\S+png|jpge', js_txt, re.I).group()  # 获取封面图片链接地址
        result.update({'m3u8_url': m3u8_url})
        result.update({'pict_url': pict_url})
        print('解密JavaScript文件成功！')
        return result

    # 解析番号
    def tk_vcd(self, file_key):
        """
         :param file_key: 文件编号
         :return :获取的番号
        """
        fk = file_key
        # 定义请求头文件
        header = self.header
        # 更新Cookie
        header.update(self.cookie)
        # 拼接访问网站地址
        v_url = r'https://%s/index.php/portal/index/detail/identification/%s.html' % (self.baseUrl, fk)
        body_txt = self.file_down(v_url, rtype=1, verify=True, header=header)  # 访问网站
        # 获取番号
        html_txt = etree.HTML(body_txt)
        li_list = html_txt.xpath('/html/body/div/p[1]/text()')
        if len(li_list) > 0:
            if li_list[0].strip(' ') == '此片為會員獨享 - 將自動跳轉到購買頁面':
                raise Exception('Cookie丢失')
        li_list = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[2]/span/text()')
        if len(li_list) == 1:
            vcd = li_list[0].strip()
        else:
            # 补充番号
            vcd = re.search(r'<dd><a class="no-hover">\S+', body_txt, re.I).group().replace('<dd><a class="no-hover">',
                                                                                            '').replace('</a></dd>', '')
        print('获取番号成功！')

        pre_list = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[1]/@href')
        pre_name = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[1]/span/text()')
        if len(pre_list) == 1:
            pre_cd = pre_list[0].strip().replace('/index.php/portal/index/search/yanyuan_id/', '') \
                                        .replace('.html', '')
            pre_nm = pre_name[0].strip()
            self.upd_pvid(pre_cd, file_key, pre_nm)
        # 获取番号异常处理
        if len(vcd) > 15:
            raise Exception('番号获取异常，请检查！%s' % vcd)
        # 创建文件夹
        # #组合存储目录
        vdir = self.SourcePath+'\\'+vcd
        if not os.path.exists(vdir):
            os.mkdir(vdir)
            print('创建文件夹成功！')
        kf_path = vdir + '\\' + file_key
        with open(kf_path, 'w') as kw:
            kw.write(file_key)
        html_path = vdir+'\\%s.html' % fk
        with open(html_path, 'w', encoding='utf-8') as html_w:
            html_w.write(body_txt)
        return vcd

    # 更新人员作品关系
    def upd_pvid(self, pid, vid, pre_nm):
        if pid in self.pv_dict:
           vid_list = self.pv_dict.get(pid).split('|')
           if vid not in vid_list:
               vid_list.append(vid)
           vid_str = '|'.join(vid_list)
           self.pv_dict.update({pid: vid_str})
        else:
           self.pv_dict.update({pid: vid})
        if pid not in self.per_dict:
            self.per_dict.update({pid: pre_nm})
        pass
    # 获取下载配置文件
    def tk_set_file(self, file_key, vcd):
        """
        :param file_key: 文件编号
        """
        fk = file_key
        set_url = 'https://%s/portal/index/ekzloi_1.html?identification=%s&lang=zh' % (
            self.baseUrl, fk)  # 拼出链接地址
        header = self.header  # 定义请求头文件
        # 基础存储目录
        vdir = self.SourcePath + '\\' + vcd
        # 更新Cookie
        header.update(self.cookie)
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
            # iv_val = unhexlify(m3u8_txt[m3u8_txt.find('IV=') + 5:m3u8_txt.find('IV=') + 37].strip('\n'))
            key_name = key_url[key_url.find('keys/') + 5:key_url.find('.key')]
            # 存储M3U8配置文件
            m3u8_path = vdir+'\\index.m3u8'
            with open(m3u8_path, 'w') as m3u8_w:
                m3u8_w.write(m3u8_txt)
            # 存储完成提示
            print('M3U8文件己存储完成！')
            # 获取解密用Key内容
            key_code = self.file_down(url=key_url, header=header, rtype=0, stream=False, verify=True)  # 访问地址获取内容
            # 存储Key文件
            key_path = vdir + '\\'+key_name+'.key'
            with open(key_path, 'wb') as key_w:
                key_w.write(key_code)
            # 存储完成提示
            print('Key文件己存储完成！')
            # 存储访问文件地址
            ts_url = m3u8_url[:m3u8_url.find('index.m3u8')]
            url_path = vdir+'\\add_list.txt'
            with open(url_path, 'w') as url_w:
                url_w.write(ts_url)
                url_w.write(chr(10)+m3u8_url)
                url_w.write(chr(10)+set_url)
            # 存储完成提示
            self.f_dict.update({file_key: vcd})
            print('配置文件己存储完成！-->:%s' % time.strftime('%Y-%m-%d %H:%M:%S'))


    # 获取本页所有文件编号
    def tk_file_key(self, url):
        """
        :param url: 存储文件编号页面
        """
        fk_url = url
        # 定义请求头文件
        header = self.header
        # 更新Cookie
        header.update(self.cookie)
        # 拼接访问网站地址
        body_txt = self.file_down(fk_url, rtype=1, verify=True, header=header)  # 访问网站
        html_txt = etree.HTML(body_txt)  # HTML格式化
        li_list = html_txt.xpath('//*[@id="works"]/li/a/@href')
        result = [li.replace('/index.php/portal/index/detail/identification/', '').replace('.html', '') for li in li_list]
        print('页面分析完成')
        return result

    # 读取字典型配置文件
    def tk_set_dict(self, file_cd):
        """
        :return : 返回己分析文件列表
        """
        fp = self.SettingPath + '\\%s.txt' % file_cd
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
    def sv_set_dict(self, file_cd):
        # 保存文件路径
        fp = self.SettingPath + '\\%s.txt' % file_cd
        wrt_src = self.set_dict.get(file_cd)  # 获取己分析字典
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

    # 读取己分析文件
    def tk_analysis(self):
        """
        :return : 返回己分析文件列表
        """
        fp = self.SettingPath + '\\Code.txt'
        f_dict = {}
        with open(fp, 'r') as rf :
            d_txt = rf.read()
        for d in d_txt.splitlines():
            d = d.split(',')
            f_dict.update({d[0]: d[1]})
        return f_dict

    # 保存己分析文件
    def sv_anlysis(self):
        fp = self.SettingPath + '\\Code.txt'  # 保存文件路径
        f_dict = self.f_dict  # 获取己分析字典
        d_txt = ''  # 初始化保存文本
        for k in f_dict.keys():  # 整合保存文本
            if len(d_txt) == 0:
                d_txt = k + ',' + f_dict.get(k)
            else:
                d_txt = d_txt + '\n' + k + ',' + f_dict.get(k)
        with open(fp, 'w') as wf:  # 保存文件
            wf.write(d_txt)
        print('历史记录完成！')

    # 保存错误文件Key值
    def sv_err_key(self):
        fp = self.SettingPath + '\\Err.txt'  # 保存文件路径
        err_txt = '\n'.join(self.err_key)  # 初始化保存文本
        with open(fp, 'w') as wf:  # 保存文件
            wf.write(err_txt)
        print('错误Key值记录完成！')

    # 读取错误文件Key值
    def tk_err_key(self):
        """
        :return : 读取文件列表
        """
        fp = self.SettingPath + '\\Err.txt'  # 保存文件路径
        with open(fp, 'r') as rf:  # 保存文件
            err_txt = rf.read()
        err_list = err_txt.splitlines()
        return err_list

    # 读取异常Key值
    def tk_exp_key(self):
        """
        :return : 读取文件列表
        """
        fp = self.SettingPath + '\\Exp.txt'  # 保存文件路径
        with open(fp, 'r') as rf:  # 保存文件
            err_txt = rf.read()
        exp_list = err_txt.splitlines()
        return exp_list

    # 获取新的Cookie值
    def tk_session(self):
        """
        :return : 更新最新登陆Cookies
        """
        from selenium import webdriver
        browser = webdriver.Chrome(executable_path=r'E:\Source\bin\chromedriver')  # 调用chrome浏览器
        # 配置header
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/85.0.4183.83 Safari/537.36'}
        # 进入主页面
        browser.get('https://x18r.com/index.php')
        # 进入登陆页面
        log_link = browser.find_element_by_xpath("/html/body/header/div/div[3]/a[1]")
        log_link.click()
        time.sleep(3)
        browser.set_window_size(800, 600)  # 4.设置浏览器的大小
        # 通过ID获取输入框
        un_input = browser.find_element_by_id("input_username")
        un_input.send_keys("pokemon49@sohu.com")

        # 通过ID获取输入框
        pw_input = browser.find_element_by_id("input_password")
        pw_input.send_keys("l1234567890")
        time.sleep(5)

        # 登陆操作
        submit = browser.find_element_by_xpath('//*[@id="index-page"]/body/div[2]/div/div/form/div[3]/button')
        submit.click()
        time.sleep(5)
        # 获取cookie
        cookie_list = browser.get_cookies()
        cookie_list.reverse()
        cookie_txt = ''
        for cookie in cookie_list:
            if len(cookie_txt) == 0:
                cookie_txt = cookie_txt + cookie.get('name') + '=' + cookie.get('value')
            else:
                cookie_txt = cookie_txt + ';' + cookie.get('name') + '=' + cookie.get('value')
        cookie = {'cookie': cookie_txt}
        # 更新访问头文件
        self.header.update(header)
        self.cookie.update(cookie)
        # 记录访问头文件
        cookie_path = self.SettingPath + '\\Cookie.txt'
        with open(cookie_path, 'w') as cf:
            cf.write(cookie_txt)
        browser.close()
        pass

    # 获取记录Cookie值
    def tk_cookie(self):
        cookie_path = self.SettingPath + '\\Cookie.txt'
        if os.path.exists(cookie_path):
            with open(cookie_path, 'r') as cf:
                cookie_txt = cf.readline()
            cookie = {'cookie': cookie_txt}
            return cookie
        else:
            self.tk_session()

    # 获取人员列表
    def tk_person(self, pnum):
        # 拼接访问网站地址
        base_url = r'https://%s/index.php/portal/index/genre/id/13.html?id=13&page=%d' % (self.baseUrl, pnum)
        header = self.header  # 定义请求头文件
        # 更新Cookie
        header.update(self.cookie)
        body_txt = self.file_down(url=base_url, header=header, rtype=1, stream=False, verify=True)  # 访问地址获取内容
        # print(body_txt)
        # 列表
        html_txt = etree.HTML(body_txt)
        link_list = html_txt.xpath('//*[@id="contents"]/div/ul[@class="clearfix"]/li/a/@href')
        if len(link_list) > 0:
            print('人员地址获取完成')
            link_list = [cd.replace('/index.php/portal/index/search/yanyuan_id/', '')
                           .replace('.html', '') for cd in link_list]
        name_list = html_txt.xpath('//*[@id="contents"]/div/ul[@class="clearfix"]/li/a/text()')
        if len(name_list) > 0:
            name_list = [nm.strip() for nm in name_list]
            print('人员名称获取完成')
        per_dict = dict(zip(link_list, name_list))
        print('第%d页完成!-->%s' % (pnum, time.strftime('%Y-%m-%d %H:%M:%S')))
        self.per_dict.update(per_dict)

    # 获取人员番号关系
    def tk_per_vid(self, pid):
        # 访问地址
        print('%s番号信息获取开始！' % self.per_dict.get(pid))
        pre_url = r'https://x18r.com/index.php/portal/index/search/yanyuan_id/%s.html' % pid
        header = self.header  # 定义请求头文件
        # 更新Cookie
        header.update(self.cookie)
        body_txt = self.file_down(url=pre_url, header=header, rtype=1, stream=False, verify=True)  # 访问地址获取内容
        # 列表
        html_txt = etree.HTML(body_txt)
        link_list = html_txt.xpath('//*[@id="works"]/li/a/@href')
        end_link = html_txt.xpath('//*[@id="contents"]/div/ul/div/a[@title="尾頁"]/@href')
        if len(end_link) > 0:
            end_page = end_link[0].replace('/index.php/portal/index/search/yanyuan_id/%s.html?yanyuan_id=%s&page=' %
                                           (pid, pid), '')
            for pag in range(2, int(end_page)+1):
                sub_pre_url = r'https://x18r.com/index.php/portal/index/search/%s.html?yanyuan_id=%s&page=%s.html' % \
                              (pid, pid, pag)
                sub_body_txt = self.file_down(url=sub_pre_url, header=header, rtype=1, stream=False, verify=True)  # 访问地址获取内容
                sub_html_txt = etree.HTML(sub_body_txt)
                sub_link_list = sub_html_txt.xpath('//*[@id="works"]/li/a/@href')
                link_list = link_list+sub_link_list
                print('%s子番号信息获取中,第%s页!' % (self.per_dict.get(pid), pag))
                tm = self.ra.randint(1, 3)
                time.sleep(tm)
        if len(link_list) > 0:
            link_list = [vid.replace('/index.php/portal/index/detail/identification/', '')
                            .replace('.html', '') for vid in link_list]
            pv_dict = {pid: '|'.join(link_list)}
            self.pv_dict.update(pv_dict)
            self.pfin_list.append(pid)
            print('%s番号信息获取完成' % self.per_dict.get(pid))
            # 保存页面
            sv_path = self.baseInputPath + r'\Phtml\%s.html' % pid
            with open(sv_path, 'w', encoding='utf-8') as phtml:
                phtml.write(body_txt)
        else:
            print('未获取到%s号人员番号信息' % pid)
            self.pexp_list.append(pid)

    def run_pre_inf(self):
        if 1 == 1:
            for i in range(1, 11):
                self.tk_person(i)
                tm = self.ra.randint(1, 5)
                time.sleep(tm)
        else:
            per_list = list(self.per_dict.keys())
            p = 0
            while 1 == 1:
                if p == len(per_list):break
                pid = per_list[p]
                if pid not in self.pfin_list and pid not in self.pexp_list:
                    try:
                        self.tk_per_vid(str(pid))
                        p = p + 1
                    except BaseException:
                        print('%s号%s分析出错等待重试！' % (pid, self.per_dict.get(pid)))
                        tm = self.ra.randint(5, 10)
                        time.sleep(tm)
                    finally:
                        self.sv_set_dict('pvid')
                        self.sv_set_list('pfin')
                        self.sv_set_list('pexp')
                        tm = self.ra.randint(3, 5)
                        time.sleep(tm)
                else:
                    p = p + 1



    # 主运行程序
    def run(self):
        # #测试验证
        # self.tk_session()
        st_tm = time.time()  # 获取程序开始时间
        if 1 == 1:
            # ##未正确获取番号处理
            if len(self.err_list) > 0:
                print('异常番号处理开始！')
                for err_key in self.err_list:
                    if self.f_dict.get(err_key, -1) == -1 and err_key not in self.exp_list:
                        tm = self.ra.randint(5, 10)
                        time.sleep(tm)
                        try:
                            vcd = self.tk_vcd(err_key)
                            self.tk_set_file(err_key, vcd)
                        except Exception as err:
                            self.err_key.append(err_key)
                            self.sv_anlysis()
                            self.sv_set_dict('pvid')
                            self.sv_set_dict('pnm')
                            print(err)
                            pass
                print('异常番号处理结束！')
            # ##获取番号
            base_url = 'https://x18r.com/index.php/portal/index/search/sjr/1.html?sjr=1&page='
            finish_pag = 0
            tk_page = list(range(1, 10))
            # tk_page = [1, 2]
            for n in tk_page:  # #最大742 需要最大值+1 己完成区间[1~380]
                if n > finish_pag or n in (1, 2):
                    print(str(n)+'页开始！！')
                    url = base_url + str(n)
                    fk_list = self.tk_file_key(url)
                    for file_key in fk_list:
                        if file_key == 'javascript:no_down();':
                            print('Cookie失效！')
                            break
                        if self.f_dict.get(file_key, -1) == -1:
                            tm = self.ra.randint(5, 10)
                            time.sleep(tm)
                            try:
                                vcd = self.tk_vcd(file_key)
                                self.tk_set_file(file_key, vcd)
                            except Exception as err:
                                self.err_key.append(file_key)
                                self.sv_anlysis()
                                self.sv_set_dict('pvid')
                                self.sv_set_dict('pnm')
                                print(err)
                                pass
                    self.sv_anlysis()
                    self.sv_set_dict('pvid')
                    self.sv_set_dict('pnm')
                    print('-----' + str(n) + '页结束！！')
                    time.sleep(5)
            # #存储记录区
            if len(self.err_key) > 0:
                self.sv_err_key()
            self.sv_anlysis()
        elif 2 == 2:
            # self.tk_per_vid('177')
            self.run_pre_inf()
            # #存储记录区
            # self.sv_set_dict('pnm')
            # self.sv_set_dict('pvid')
            # self.sv_set_list('pfin')

        # 获取耗时
        use_sc = time.time() - st_tm
        # 转换时间格式
        m, s = divmod(use_sc, 60)
        h, m = divmod(m, 60)
        # 显示耗时
        print("总耗时：%d:%02d:%02d" % (h, m, s))
        pass


trm = TkR18m3u8()
trm.run()
