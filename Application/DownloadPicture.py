import requests,datetime
import os,threading
import pymysql
import time
import random
import setting

class DownPict(threading.Thread):

    #配置初始化
    def __init__(self,type):
        threading.Thread.__init__(self)
        # 配置下载类型1:act\2:vadio
        self.type = type
        # 参数初始化操作
        self.conn = ""
        self.cur = ""
        self.now = 0
        # 初始化第一次下载时间周期
        self.next = datetime.datetime.now() + datetime.timedelta(minutes=15)
        # 初始化下载图片数量
        self.picnum = 0
        # 初始化控制符号
        self.control = ""
        # 初始化目录
        self.__lv1_folder = ""
        self.__lv2_folder = ""
        self.__lv3_folder = ""
        # 图片大小
        self.__size_limit = 0

    #链接数据库
    def Link_Database(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="Study",passwd="study",db="Scrapy",charset="utf8")
        self.cur = self.conn.cursor()
    #获取封面图片地址
    def take_vadio(self):
        self.Link_Database()
        sql = " SELECT DISTINCT " \
              "  V.CENSORED_FLAG " \
              " ,V.VADIO_CODE " \
              " ,V.VADIO_PAGE_IMG_URL " \
              " ,V.VADIO_URL " \
              "  FROM VADIO_INFO V " \
              " WHERE VADIO_PAGE_IMG_URL NOT LIKE '%nopic.jpg%'" \
              "   AND VADIO_PAGE_IMG_URL NOT LIKE '%pics.dmm.co.jp%' " \
              "   AND V.CENSORED_FLAG = 'censored'" \
              "   AND NOT EXISTS(" \
              "       SELECT 1" \
              "         FROM PIC_SIZE P" \
              "        WHERE P.VADIO_CODE = V.VADIO_CODE" \
              "          AND P.SIZE = P.PSIZE" \
              "     )"\
              " ORDER BY VADIO_CODE "
              #"   and v.VADIO_PAGE_IMG_URL NOT LIKE '%javcdn.pw%'" \
        cur = self.cur
        num = cur.execute(sql)
        if num > 0:
            rows = cur.fetchall()
            return rows
        cur.close()

    # 获取截图地址
    def take_screen(self):
        self.Link_Database()
        sql = ""

    # 获取截图地址
    def take_actress(self):
        self.Link_Database()
        sql= "SELECT p.censored_flag "\
                   " ,p.preformer_code "\
                   " ,p.preformer_photo_url " \
                   " ,pl.preformer_url"\
              " FROM preformer_info p " \
              "     ,preformer_list pl " \
             " WHERE p.preformer_photo_url NOT LIKE '%nowprinting.gif%' " \
             " AND p.preformer_photo_url NOT LIKE '%printing.jpg%' " \
             " AND P.preformer_photo_url NOT LIKE '%[%]%' " \
             " AND P.preformer_photo_url LIKE '%prn_a%' " \
             " AND p.preformer_code = pl.preformer_code " \
             " AND p.CENSORED_FLAG  = pl.censored_flag " \
             " ORDER BY p.preformer_code "
        cur = self.cur
        num = cur.execute(sql)
        if num > 0 :
            rows = cur.fetchall()
            return rows
        cur.close()
        self.conn.close()
    #获取图片信息
    def get_size(self,filename):
        self.Link_Database()
        sql = "select size from PIC_SIZE WHERE VADIO_CODE = \"%s\"" % (filename)
        cur = self.cur
        num = cur.execute(sql)
        if num == 0:
            return 0
        else:
            size_list = cur.fetchone()
            for size in size_list:
                return size
        cur.close()
        self.conn.close()

    #保存图片信息
    def save_pic_size(self,filename,size):
        self.Link_Database()
        sql = "DELETE FROM PIC_SIZE WHERE VADIO_CODE = \"%s\""% (filename)
        cur = self.cur
        cur.execute(sql)
        self.conn.commit();
        sql = " Insert into pic_size (vadio_code,size) " \
              " value(\"%s\",%s) " % (filename,size)
        cur.execute(sql)
        self.conn.commit();
        cur.close()
        self.conn.close()

    #保存图片
    def compose_url(self,l1file,l2file,l3file,filename,url):
       dir_path = "G:\\Media\\%s\\%s"%(l1file,l2file)
       file_type = url.split(".")[-1]
       if l3file != "None":
           dir_path = dir_path+"\\"+l3file
       if not os.path.exists(dir_path) :
           os.makedirs(dir_path)
       save_path = ("%s\\%s.%s") %(dir_path,filename,file_type)
       return save_path
       #print(save_path)

    def save_body(self,save_path,url,refurl,filename):
       #print(url)
       #print(time.ctime(time.time()))
       user_agent = random.choice(setting.USER_AGENTS)
       proxie = random.choice(setting.PROXIES)
       header = {'Referer': refurl,
                 #'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Android 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)/Mobile'
                 #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
                 'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.6 Safari/534.57.2'
                 }
       response = requests.get(url, stream=True, headers=header,timeout=60)
       res_url = response.url
       img_size=response.headers["Content-Length"]
       if (res_url.find("now_printing")==-1):
           self.save_pic_size(filename, img_size)
           with open(save_path, 'wb') as handle:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

    #时间控制模块
    def MatchTime(self):
        #随机生成下载间隔
        rs = random.randint(1, 4)
        time.sleep(rs)
        self.now = datetime.datetime.now()
        if self.now >= self.next:
            print("Sleeping...Download Picture:%d P!" % self.picnum)
            #随机生成休息时间区间
            rm = random.randint(2, 6)
            #随机生成下载时间区间
            rd = random.randint(15, 20)
            #计算休息秒数
            sleeptime = rm * 60
            time.sleep(sleeptime)
            self.now = datetime.datetime.now()
            #配置下一次休息的时间
            self.next = self.now + datetime.timedelta(minutes=rd)
            #初始化图片数目
            self.picnum = 0
            print("Starting...")

    #图片信息更新模块
    def reflash(self, savePath, voidCode):
        self.Link_Database()
        psize = os.path.getsize(savePath)
        sql = "update PIC_SIZE set psize = %d WHERE VADIO_CODE = \"%s\"" % (psize, voidCode)
        cur = self.cur
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()
        pass
    #核心处理模块
    def core_process(self,proc_list,l1file,l3file):
        for m in proc_list:
            #获取二级目录名称
            l2file = m[0]
            #获取文件名称
            filename = m[1]
            #获取图片下载地址
            url = m[2]
            #获取Referer地址
            refurl = m[3]
            #组合保存路径
            save_path = self.compose_url(l1file, l2file, l3file, filename, url)
            #获取图片大小
            size_limit = self.get_size(filename)
            # print(save_path)
            #图片不存在时的处理
            if not (os.path.exists(save_path)):
                try:
                    # 下载图片
                    self.save_body(save_path, url, refurl, filename)
                    # 更新图片完整信息
                    self.reflash(save_path, filename)
                    self.picnum = self.picnum + 1
                    self.MatchTime()
                except BaseException:
                    print(url)
                    continue
            #图片不完整时的处理
            elif os.path.getsize(save_path) < size_limit:
                try:
                    #删除旧有图片
                    os.remove(save_path)
                    #下载图片
                    self.save_body(save_path, url, refurl, filename)
                    #更新图片完整信息
                    self.reflash(save_path, filename)
                    self.picnum = self.picnum + 1
                    self.MatchTime()
                except BaseException:
                    print(url)
                    continue
            #图片存在且完整时的处理
            else:
                pass
            # 下载控制
            if self.control == "E":
                break
    #初始化入口模块
    def entry(self,type):
        if type == 1:
            list = self.take_actress()
            self.__lv1_folder = "actress"
            self.__lv3_folder = "None"
        elif type == 2:
            list = self.take_vadio()
            self.__lv1_folder = "vadio"
            self.__lv3_folder = "None"
            #self.__size_limit = 100*1024
        return list
        pass
    #主调用程序
    def run(self):
        #初始化参数
        ##传输列表
        list = self.entry(self.type)
        ##图片大小
        self.__size_limit = 0
        if list:
            self.core_process(list,self.__lv1_folder,self.__lv3_folder)

#dp = DownPict(2)
#dp.run()