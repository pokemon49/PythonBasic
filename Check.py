#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import os,pymysql
class Check(object):
    conn = ""
    cur = ""
    # 链接数据库
    def Link_Database(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="Study", passwd="study", db="Scrapy",
                                    charset="utf8")
        self.cur = self.conn.cursor()
    def check(self):
        path = 'G:\\Media\\vadio\\censored\\'
        image_list = os.listdir(path)
        n = 0
        for image in image_list:
            image_path = path + image
            if os.path.isfile(image_path):
                im = Image.open(image_path)
                try:
                    pix = im.load()
                except:
                    im.close()
                    n = n + 1
                    # print(image)
                    # os.remove(image_path)
        print(n)
    def fcheck(self):
        path = 'G:\\Media\\vadio\\censored\\'
        image_list = os.listdir(path)
        n = 0
        for image in image_list:
            image_path = path + image
            image_name = os.path.basename(image_path)
            vadio_code = os.path.splitext(image_name)[0]
            size = os.path.getsize(image_path)
            self.flash(vadio_code,size)

    def flash(self,vadioCode,size):
        self.Link_Database()
        sql = " insert into pic_size (vadio_code,psize)"\
              " values (\'%s\',%d)"\
		      " on DUPLICATE key UPDATE psize = %d" % (vadioCode,size,size)
        cur = self.cur
        cur.execute(sql)
        self.conn.commit();
        pass
    def reflash(self,savePath,voidCode):
        self.Link_Database()
        psize = os.path.getsize(savePath)
        sql = "update PIC_SIZE set psize = %d WHERE VADIO_CODE = \"%s\"" % (psize,voidCode)
        cur = self.cur
        cur.execute(sql)
        self.conn.commit();
        pass
    def run(self):
        #self.check()
        #self.reflash("G:\\Media\\vadio\\censored\\HUNTA-398.jpg","HUNTA-398")
        self.fcheck()


ims =Check()
ims.run()