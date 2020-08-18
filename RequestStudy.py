import json

import requests

# HTTP请求类型
# get类型 获取指定URL地址的资源
r = requests.get('https://github.com/timeline.json')
# post类型 获取指定URL地址的资源后附加的新数据
r = requests.post("http://m.ctrip.com/post")
# put类型 请求向指定的URL地址存储一个资源，覆盖原URL位置的资源
r = requests.put("http://m.ctrip.com/put")
# delete类型 删除指定URL地址存储的资源
r = requests.delete("http://m.ctrip.com/delete")
# head类型 获取URL位置资源的响应消息报告，即获得该资源的头部信息
r = requests.head("http://m.ctrip.com/head")
# options类型
r = requests.options("http://m.ctrip.com/get")
# patch类型 请求局部更新URL位置的资源，改变该处资源的部份内容。
r = requests.patch("http://m.ctrip.com/get")


# 控制访问参数，用于各类HTTP请求类型。
# #params：字典或字节序列，作为参数增加到url中、
# #data：字典、字节序列或文件对象，作为Request的对象
# #json：JSON格式的数据，作为Request的内容
# #headers：字典类型，用于定制HTTP请求头
# #cookies：字典或CookieJar，Request中的cookie
# #auth：元组，支持HTTP认证功能
# #files：字典类型，传输文件
# #timeout：设定超时时间，秒为单位
# #proxies：字典类型，设置访问代理服务器，可以增加登录认证
# #allow_redirects：True/False，默认为Ture，重定向开关
# #stream：True/False，默认为True，获取内容立即下载开关
# #verigy：True/False，默认为True，认证SSL证书开关,也可以直接带入PEM证书链文件路径，以实现认证。
# #cert：本地SSL证书路径


class req():
       header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
       #header = {'User-Agent': 'User-Agent:Mozilla/5.0'}
       #proxie = {"https": "https://120.27.131.204:3128"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://221.229.252.98:8080"}
       #proxie = {"http": "http://120.27.131.204:3128"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #proxie = {"https": "https://14.111.8.46:8118"}
       #url = "http://www.baidu.com/"
       #url = "http://www.baidu.com/img/bd_logo1.png"
       url = "http://pics.dmm.co.jp/mono/actjpgs/akasaka_zyunko.jpg"
       #response = requests.get(url, stream=True, headers=header, proxies=proxie)
       response = requests.get(url, stream=True, headers=header)
       res_date = response.headers["Content-Length"]
       print(type(res_date))
       print(res_date)
       print(response.status_code)
       print(response.headers)
       print(response.url)
       res_url = response.url
       if (res_url.find("now_printing") == -1):
              print("cc")
       #print(response.text)

url = "http://sdom.csisc.cn/showVersion_baseAttribute.action"

querystring = {"behavior": "EX0001", "codeArray": "PUBLC|VRTIS|EX0001", "maxVersion": "V1.1"}

payload = ""
headers = {
    #'cache-control': "no-cache",
    #'Postman-Token': "f7f6016a-91ff-4b67-8854-a3c3cab984cb",
    'cookie': "acw_tc=65e300a715513164778408046e76b0ae907;JSESSIONID=60E3F52A437A6F226626FAE9C8B3C87B"
    }

"""

"""
response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)

# HTTP请求类型
# get类型
r = requests.get('https://github.com/timeline.json')
# post类型
r = requests.post("http://m.ctrip.com/post")
# put类型
r = requests.put("http://m.ctrip.com/put")
# delete类型
r = requests.delete("http://m.ctrip.com/delete")
# head类型
r = requests.head("http://m.ctrip.com/head")
# options类型
r = requests.options("http://m.ctrip.com/get")

# 获取响应内容
print(r.content)  # 以字节的方式去显示，中文显示为字符
print(r.text)  # 以文本的方式去显示

# URL传递参数
payload = {'keyword': '香港', 'salecityid': '2'}
r = requests.get("http://m.ctrip.com/webapp/tourvisa/visa_list", params=payload)
print(r.url)  # 示例为http://m.ctrip.com/webapp/tourvisa/visa_list?salecityid=2&keyword=香港

# 获取/修改网页编码
r = requests.get('https://github.com/timeline.json')
print (r.encoding)


# json处理
r = requests.get('https://github.com/timeline.json')
print(r.json())  # 需要先import json

# 定制请求头
url = 'http://m.ctrip.com'
headers = {
       'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
r = requests.post(url, headers=headers)
print(r.request.headers)

# 复杂post请求
url = 'http://m.ctrip.com'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))  # 如果传递的payload是string而不是dict，需要先调用dumps方法格式化一下

# post多部分编码文件
url = 'http://m.ctrip.com'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)

# 响应状态码
r = requests.get('http://m.ctrip.com')
print(r.status_code)

# 响应头
r = requests.get('http://m.ctrip.com')
print(r.headers)
print(r.headers['Content-Type'])
print(r.headers.get('content-type'))  # 访问响应头部分内容的两种方式

# Cookies
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
r.cookies['example_cookie_name']  # 读取cookies

url = 'http://m.ctrip.com/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)  # 发送cookies

# 设置超时时间
r = requests.get('http://m.ctrip.com', timeout=0.001)

# 设置访问代理
proxies = {
"http": "http://10.10.1.10:3128",
"https": "http://10.10.1.100:4444",
}
r = requests.get('http://m.ctrip.com', proxies=proxies)

# 如果代理需要用户名和密码，则需要这样：
proxies = {
"http": "http://user:pass@10.10.1.10:3128/",
}
# 返回结果
# #返回结果状态代码
r.status_code
# #响应内容的字符串形式
r.text
# #从响应头中获得的内容编码格式
r.encoding
# #从响应内容中分析出的内容编码格式
r.apparent_encoding
# #响应内容的二进制形式
r.content

# 异常
# #网络链接错误，如DNS查询失败，拒绝链接等
requests.ConnectionError
# #Http错误异常
requests.HTTPError
# #URL缺失异常
requests.URLRequired
# #超过最大重定向次数，产生重大定向异常
requests.TooManyRedirects
# #链接远程服务器超时异常
requests.ConnectTimeout
# #请求URL超时，产生超时异常
requests.Timeout
# #如果不是200，产生异常HttpError
r.raise_for_status()

