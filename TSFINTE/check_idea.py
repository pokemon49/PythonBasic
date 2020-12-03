#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '验证功能想法临时脚本'
# 'Version 1.0'
# '1.0 20200725 初始版本创建'
__author__ = '林金行'

import requests
import execjs
import re
from binascii import hexlify
from lxml import etree
import time
import os


if 0 == 1:  # X18R页面访问调试

    verify = r'G:\TS\x18r-com-chain.pem'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
             #, 'cookie': 'crisp-client%2Fsession%2Fd0775f8b-391e-432c-b808-f8fcb794ea24=session_6c5bc221-f4ac-46c8-9a0e-cbefc8676658; PHPSESSID=v05n96q2m40gdpdv6d7m4rip63; _gat_gtag_UA_121321830_1=1; _ga=GA1.2.106278597.1591633007; _gid=GA1.2.1604183792.1598660466'
              }
    v_url = r'https://x18r.com/index.php/portal/index/detail/identification/ffaf5431c242103fb7cb877086667fbe.html'
    response = requests.get(v_url, stream=False, headers=header, verify=verify)
    body_txt = response.text
    # print(body_txt)
    # 番號 時長
    # vcd = re.search(r'<dd><a class="no-hover">\S+', body_txt, re.I).group().replace('<dd><a class="no-hover">',
    #                                                                                '').replace('</a></dd>', '')
    # print(vcd)

    html_txt = etree.HTML(body_txt)
    #li_list = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[2]/span/text()')
    #print(li_list[0].strip(' '))

    li_list = html_txt.xpath('/html/body/div/p[1]/text()')
    print(li_list[0].strip(' '))

    '''
    d_url = r'https://x18r.com/portal/index/ekzloi_1.html?identification=ed7a152b340b14065765f7b52c8ff932&lang=zh'

    # verify = (r'G:\TS\x18r-com.pem', r'G:\TS\x18r-com-chain.pem')
    # verify = (r'G:\TS\sr.crt', r'G:\TS\aa.key')

    basePath = r'G:\TS\TEST'

    requests.packages.urllib3.disable_warnings()  # 禁用安全警告

    response = requests.get(d_url, stream=False, headers=header, verify=verify)
    js = response.text
    js = js[5:len(js) - 2]
    js = js.replace("c35", "c<a?'':e(parseInt(c/a)))+((c=c%a)>35")
    # print(js)
    result = execjs.eval(js)
    url = re.search(r'https://\S+expires=\d+', result, re.I).group()
    print(url)
    d_url = url

    response = requests.get(d_url, stream=False, headers=header)

    print(response.status_code)
    if response.status_code == 200:
        m3u8_txt = response.text
        key_url = m3u8_txt[m3u8_txt.find('URI="') + 5:m3u8_txt.find('.key') + 4]
        iv_val = m3u8_txt[m3u8_txt.find('IV=') + 5:m3u8_txt.find('IV=') + 37]
        key_name = key_url[key_url.find('keys/') + 5:key_url.find('.key')]
        print(key_url)
        print(iv_val)
        key = requests.get(key_url, stream=False, headers=header, verify=verify)
        if key.status_code == 200:
            key_path = basePath + '\\%s.key' % key_name
            with open(key_path, 'wb') as key_w:
                key_w.write(key.content)
            print('Key文件写入成功')
    '''
    # print(response.text)
elif 1 == 3:   # X18R Key解析调试
    file_path = r'G:\TS\ABP-996\8b923ba413e8f25adfa590bcdb95634f.key'
    file_open = open(file_path, 'rb')
    byte = file_open.read()
    file_open.close()
    HexVal = byte.hex()
    print(HexVal)

    '''
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
    '''
elif 1 == 4:  # fc aa1804内容获取
    # PHPSESSID获取

    SESSION_URL = r'https://aa1804.com/wtydfAA.htm'
    s = requests.session()
    res = s.get(SESSION_URL, stream=True)
    c = requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
    c.set('cookie-name', 'cookie-value')
    s.cookies.update(c)
    session = s.cookies.get_dict().get('PHPSESSID')
    # 基础参数
    verify = r'G:\TS\fc-aa1804-com-chain.pem'
    verify_xp1 = r'G:\TS\sni-cloudflaressl-com-chain.pem'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
              'Cookie': # 'cfduid=ddaef2da16999b15327db03e9737be6241597555699;' +
                        # 'UM_distinctid=173f5bdb1462ad-04065c8bb41d4c-6d0c04-384000-173f5bdb147761;' +
                        # 'javascript_cookie_Eighteenth=I_am_over_18_years_old;' +
                        # 'CNZZDATA1273435591=1990203647-1597552447-https%253A%252F%252Faa1804.com%252F%7C1598090379;' +
                        # 'CNZZDATA1273380027=1912863071-1597553488-https%253A%252F%252Faa1804.com%252F%7C1598089713;' +
                        'PHPSESSID=%s;' % session +
                        # 'PHPSESSID=rpj1s1i1arhcbe6ueehva58a21;' +
                        'TSCvalue=gb'
              }
    # v_url = r'https://fc.aa1804.com/fcfluidplayer.php?id=721_b_jhbqdsbagk'
    # 列表获取
    '''
    v_url = r'https://aa1804.com/Taboo_object.html'
    response = requests.get(v_url, stream=False, headers=header, verify=verify_xp1, timeout=30)
    body_txt = response.text
    # with open('E:\Source\Files\Main.html', 'w', encoding='utf-8') as html:
    #    html.write(body_txt.replace("\n", ''))
    # with open('E:\Source\Files\Main.html', 'r', encoding='utf-8') as html:
    #    body_txt = html.read()
    # print(body_txt)
    html_txt = etree.HTML(body_txt.replace("<span class='di_img'>", "<!--<span class='di_img'>").replace('<span id="friendLink"></span>', '<span id="friendLink"></span>-->'))
    # print(etree.tostring(html_txt))
    lk_list = html_txt.xpath('//span [@id="main"]/a/@href')
    print(len(lk_list))
    for lk in lk_list:
        print(lk)
    lk_list = html_txt.xpath('//*[@id="main"]/a/img/@alt')
    print(len(lk_list))
    for lk in lk_list:
        print(lk)
        # print(etree.tostring(lk))
    '''
    # 链接获取

    v_url = r'https://aa1804.com/av_Broadcast/23537.html'
    response = requests.get(v_url, stream=False, headers=header, verify=verify_xp1, timeout=30)
    body_txt = response.text
    # print(body_txt)
    lk_re =re.compile(r'https://\S+id=\d+_\S+"')
    result = lk_re.findall(body_txt)
    print(result)

    # 获取内容测试
    '''
    v_url = r'https://htemp2.ccmma18.com/file/10717/10717_213.jpg'
    response = requests.get(v_url, stream=True, headers=header)
    req_b = response.content
    file = r'E:\A.JPEG'
    with open(file, 'wb') as ft:
        ft.write(req_b)
        # print(etree.tostring(lk))
    '''
    # M3U8
    '''
    v_url = r'https://aa1804.com/xpmv/57146.html'
    response = requests.get(v_url, stream=False, headers=header, verify=verify_xp1, timeout=300)
    body_txt = response.text
    # print(body_txt)
    m3u8_url = re.search(r"<source src=\S+.m3u8", body_txt, re.I).group().replace('<source src=', '').replace("'", '')
    print(m3u8_url)
    m3u8_nm = m3u8_url.split('/')[3].replace('.m3u8', '')
    print(m3u8_nm)
    response = requests.get(m3u8_url, stream=False, headers=header)
    m3u8_txt = response.text
    print(m3u8_txt)
    '''
    # Pict
    '''
    v_url = r'https://aa1804.com/18H_8039.html'
    response = requests.get(v_url, stream=False, headers=header, verify=verify_xp1, timeout=300)
    body_txt = response.text
    # print(requests.session())
    # print(body_txt)
    html_txt = etree.HTML(body_txt)
    li_list = html_txt.xpath('/html/body/div/center/h1/text()')
    for li in li_list:
        print(re.search(r"\d+", li, re.I).group())
    # pag_list = html_txt.xpath('//*[@id="show_cg_html"]/center/img/@src')
    pag_list = html_txt.xpath('//script[@language="javascript"]/text()')
    jpg_re = re.compile(r'https://\S+.jpg', re.I)
    for pag in pag_list:
        result = jpg_re.findall(pag)
        print(result)
    '''
    #
elif 1 == 5 :  # X18R xPath验证
    verify = r'G:\TS\x18r-com-chain.pem'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
              'TE': 'Trailers'
              }
    # https://x18r.com/index.php/portal/index/search/sjr/1.html?sjr=1&page=2
    # v_url = r'https://x18r.com/index.php/portal/index/search/sjr/1.html'
    v_url = r'https://x18r.com/index.php'
    param = {'srj': 1, 'page': 1}
    response = requests.get(v_url, stream=False, headers=header, verify=verify, params=param)
    html = etree.HTML(response.text)
    # print(response.text)
    result = html.xpath('//*[@id="works"][@style="margin-bottom: 15px;"]/li/a/@href')
    for r in result:
        print(r)
        print(r[46:].replace('.html', ''))
    pass
elif 1 == 6:  # 列表查询
    verify = r'G:\TS\x18r-com-chain.pem'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
             # ,'cookie': 'crisp-client%2Fsession%2Fd0775f8b-391e-432c-b808-f8fcb794ea24=session_6c5bc221-f4ac-46c8-9a0e-cbefc8676658; PHPSESSID=5ffe6s51d3dji162e56ng5rb81; _gat_gtag_UA_121321830_1=1; _ga=GA1.2.106278597.1591633007; _gid=GA1.2.1604183792.1598660466'
              }
    x_url = r'https://x18r.com/index.php/portal/index/search/sjr/2.html'

    # ## JSON https://x18r.com/portal/index/ekzloi_1.html?identification=5edde9e61cb3ffdeb13c14f277199825&lang=zh  <cookie>
    # ## M3U8 https://svip-cdn.chuumm.cn/output/300f7e5408328c3b198a85e8a0a5a154/index.m3u8?md5=0y2TzsWMTxqrW6_AjI-9Mg&expires=1598679355
    # ## SVIP https://svip-cdn.chuumm.cn/output/300f7e5408328c3b198a85e8a0a5a154/index0.ts

    response = requests.get(x_url, stream=False, headers=header, verify=verify)
    # print(response.text)
    html_txt = etree.HTML(response.text)  # HTML格式化
    li_list = html_txt.xpath('//*[@id="works"]/li/a/@href')
    # ##获取文件名称
    for li in li_list:
        print(li)
elif 1 == 7:  # 读写字典
    fp = r'G:\TS\X18R\Code.txt'
    f_dict = {}
    with open(fp, 'r') as rf :
        d_txt = rf.read()
    for d in d_txt.splitlines():
        d = d.split(',')
        f_dict.update({d[0]: d[1]})
    d_txt = ''
    for k in f_dict.keys():
        if len(d_txt) == 0:
            d_txt = k + ',' +f_dict.get(k)
        else:
            d_txt = '\n' + k + ',' +f_dict.get(k)
    with open(fp, 'w') as wf :
        wf.write(d_txt)
elif 0 == 8:
    from selenium import webdriver
    browser = webdriver.Chrome(executable_path=r'E:\Source\bin\chromedriver')  # 调用chrome浏览器
    browser.get('https://x18r.com/index.php')
    log_link = browser.find_element_by_xpath("/html/body/header/div/div[3]/a[1]")
    log_link.click()
    time.sleep(5)
    # browser.get('https://x18r.com/index.php/user/login/index.html')  # 2.通过浏览器向服务器发送URL请求
    # browser.refresh()  # 3.刷新浏览器
    browser.set_window_size(800, 600)  # 4.设置浏览器的大小
    # 通过ID获取输入框
    un_input = browser.find_element_by_id("input_username")
    un_input.send_keys("pokemon49@sohu.com")

    # 通过ID获取输入框
    pw_input = browser.find_element_by_id("input_password")
    pw_input.send_keys("l1234567890")
    time.sleep(20)

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
            cookie_txt = cookie_txt + '; _' + cookie.get('name') + '=' + cookie.get('value')
    print(cookie_txt)
    pass
elif 0 == 1:
    # 地址截取
    link = 'https://svip-cdn.chuumm.cn/output/2ebb24d282aed2a0fe62a76f1f8d6dd3/index.m3u8?md5=cm3KZnPjPdU-rFkQ5XmSXg&expires=1598699022'
    print(link[:link.find('index.m3u8')])
    print(link.split('/')[2])

    # cookie处理
    cookie_list = [{'domain': '.x18r.com', 'expiry': 1598788339, 'httpOnly': False, 'name': '_gat_gtag_UA_121321830_1', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.x18r.com', 'expiry': 1598874720, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.381167666.1598788280'}, {'domain': '.x18r.com', 'expiry': 1661860320, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.2144143893.1598788280'}, {'domain': 'x18r.com', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False, 'value': 'ul85pivmqnnjc77nkh8d18sgqh'}]
    cookie_list.reverse()
    cookie_txt = ''
    for cookie in cookie_list:
        if len(cookie_txt) == 0:
            cookie_txt = cookie_txt + cookie.get('name') + '=' + cookie.get('value')
        else:
            cookie_txt = cookie_txt + '; _' + cookie.get('name') + '=' + cookie.get('value')

    print(cookie_txt)
    # 计时
    st_tm = time.time()
    time.sleep(5)
    use_tm = time.time() - st_tm
    seconds = use_tm
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("%d:%02d:%02d" % (h, m, s))
    # 转换日期
    timeArray = time.localtime(1462482700)  # 秒数
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)

elif 1 == 0:
    # #检查功能
    c_path = r'G:\TS\X18R'
    f_list = os.listdir(c_path)
    duo_lb = []
    shao_lb = []
    for f in f_list:
        f_path = c_path + '\\' + f
        if os.path.isdir(f_path):
            num = os.listdir(f_path)
            if len(num) > 5:
                duo_lb.append(f)
            if len(num) < 4:
                shao_lb.append(f)
    print('缺失文件列表（%d）：' % len(shao_lb))
    print(shao_lb)
    print('超多文件列表（%d）：' % len(duo_lb))
    print(duo_lb)
    print('%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
elif 1 == 0:
    # 根据网页内容获取数据
    # url = r'https://svip-cdn.chuumm.cn/output/c8255d368465d48299fb395efac08fc6/000.ts'
    # response = requests.get(url, stream=True)
    # print(response.status_code)
    from pubFunction import pubfunction
    pf = pubfunction()
    base_path = r'G:\TS\X18R\Temp'
    dir_list = os.listdir(base_path)
    for dir in dir_list:
        v_path = base_path + '\\' + dir
        html_list = [html for html in os.listdir(v_path) if html.count('.html') > 0]
        if len(html_list) > 0:
            html = [html for html in os.listdir(v_path) if html.count('.html') > 0][0]
            file = v_path + '\\' + html
            print(file)
            html_path = file
            vid = html.replace('.html', '')
            with open(html_path, 'r', encoding='utf-8') as html:
                 body_txt = html.read()
            html_txt = etree.HTML(body_txt)
            pre_list = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[1]/@href')
            pre_name = html_txt.xpath('//*[@id="contents-inline"]/div[4]/div/div/a[1]/span/text()')
            if len(pre_list) == 1:
                pre_cd = pre_list[0].strip().replace('/index.php/portal/index/search/yanyuan_id/', '') \
                    .replace('.html', '')
                pre_nm =pre_name[0].strip()
                if pre_cd in pf.pv_dict:
                    vid_list = pf.pv_dict.get(pre_cd).split('|')
                    if vid not in vid_list:
                        vid_list.append(vid)
                    vid_str = '|'.join(vid_list)
                    pf.pv_dict.update({pre_cd: vid_str})
                else:
                    pf.pv_dict.update({pre_cd: vid})
                if pre_cd not in pf.per_dict:
                    pf.per_dict.update({pre_cd: pre_nm})

        pf.sv_set_dict('pvid')
        pf.sv_set_dict('pnm')
    pass
else:
    '''
    tar_path = r'G:\TS\X18R\Temp\DASD-720\Bak'
    src_path = r'G:\TS\X18R\Temp\DASD-720'
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
    '''
    '''
    bpath = 'TEST'
    from TSFINTE.pubFunction import pubfunction
    pf = pubfunction()
    perf_code = '242'
    if perf_code in list(pf.per_dict.keys()):
        id_list = pf.pv_dict.get(perf_code).split('|')
        cd_list = [pf.f_dict.get(id) for id in id_list if id in list(pf.f_dict.keys())]
        print(cd_list)
        loss_id = set(id_list) - set(pf.f_dict.keys())
        print(loss_id)
        sp_list = [bpath + '\\' + cd for cd in cd_list]
        down_dict = dict(zip(cd_list, sp_list))
    '''
    from TSFINTE.pubFunction import pubfunction
    pf = pubfunction()
    down_list = pf.tk_set_dict('down_list')
    for key in down_list.keys():
        if key not in pf.pv_dict: raise Exception(key)
        vid_list = pf.pv_dict.get(key).split('|')
        vcd_list = [pf.f_dict.get(vid) for vid in vid_list if vid in pf.f_dict]
        err_num = 0
        fin_num = 0
        hv_num = len(vcd_list)
        for vcd in vcd_list:
            v_path = pf.SourcePath + '\\' + vcd
            if os.path.exists(v_path):
                fin_st = 0
                for fnm in os.listdir(v_path):
                    if fnm.count('finish') > 0:
                        fin_num = fin_num + 1
                    if fnm.count('.key') > 0 or fnm.count('index.m3u8') > 0 or fnm.count('add_list') > 0:
                        fin_st = fin_st + 1
                if fin_st < 3:
                    err_num = err_num + 1
            else:
                print('%s文件夹不存在' % vcd)
        if fin_num == 0:
            flg = 'P'
        elif fin_num == hv_num:
            flg = 'F'
        else:
            flg = 'H<--'
        new_st = {key: '%d|%d|%d|%s' % (err_num, fin_num, hv_num, flg)}
        down_list.update(new_st)
    keys = [int(key) for key in down_list.keys()]
    keys.sort()
    new_down_list = {}
    for key in keys:
       new_down_list.update({str(key): down_list[str(key)]})
    pf.sv_set_dict('down_list', new_down_list)

