#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'JS功能模块学习'
# 'Version 1.0'
# '1.0 20200101 初始版本创建'
__author__ = '林金行'

import execjs
import requests

url = ""
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

# response = requests.request("GET", url, headers=header)
# requests.post()

js = r"eval(function(p,a,c,k,e,d){e=function(c){return(c35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('R s=r q({p:o.n(\'2\'),m:1,l:\'#k\',h:\'i-9\',g:0.3,f:e,d:1,c:\'b\',2:{6:\'7://a-t.j.u/w/Q/P.O?N=M&L=K\',J:\'7://I.H.G/F-E.D\',\'4\':\'C\'},B:{\'6\':\'\',4:\'A\',z:\'y\',x:\'5%\',v:\'#8\'}});',54,54,'|true|video||type||url|https|ffffff|tw|p2|auto|preload|hotkey|false|screenshot|volume|lang|zh|chuumm|FADFA3|theme|autoplay|getElementById|document|element|DPlayer|new|dp|cdn|cn|color|output|bottom|24px|fontSize|webvtt|subtitle|hls|png|973C|WANZ|com|japronx|image|thumbnails|1596014481|expires|yDHyUngK3G0pzrN17F4d0w|md5|m3u8|index|03beebad4fe4795362f7dfa82e8ca958|var'.split('|'),0,{}))"
js = js[5:len(js)-1]

js = js.replace("c35", "c<a?'':e(parseInt(c/a)))+((c=c%a)>35")
# 运行JS脚本
result = execjs.eval(js)

print(result)
