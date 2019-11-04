import requests

class req():
       header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
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

querystring = {"behavior":"EX0001","codeArray":"PUBLC|VRTIS|EX0001","maxVersion":"V1.1"}

payload = ""
headers = {
    #'cache-control': "no-cache",
    #'Postman-Token': "f7f6016a-91ff-4b67-8854-a3c3cab984cb",
    'cookie': "acw_tc=65e300a715513164778408046e76b0ae907;JSESSIONID=60E3F52A437A6F226626FAE9C8B3C87B"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)