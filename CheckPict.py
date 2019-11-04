import requests
import os
import pymysql
import time
import random
import setting

class CheckPict:
    conn = ""
    cur = ""
    #链接数据库
    def Link_Database(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="Study",passwd="study",db="Scrapy",charset="utf8")
        self.cur = self.conn.cursor()

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
    def run(self):
        path = 'G:\\Media\\vadio\\censored\\'
        file_list = os.listdir(path)
        #file_list = ['AP-484.jpg']
        print (type(file_list))
        print (len(file_list))
        n = 1
        '''
        for file in file_list:
            file_path = path+file
            file_size = os.path.getsize(file_path)
            file_name = file.split('.')[-2]
            file_true_size = self.get_size(file_name)
            if file_size != file_true_size and file_true_size != 0:
                n = n+1
                print(os.statvfs(file_path))
                #print(file+':'+str(file_size)+'《》'+str(file_true_size))
        print(n)'''

cp = CheckPict()
cp.run()