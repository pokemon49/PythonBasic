#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'通讯管理系统数据操作'
__author__ = '林金行'
import pymysql

class systemDB(object):
    def __init__(self):
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="scrapy", passwd="scrapy", db="exercise", charset="utf8")
        cur = conn.cursor()
        self.cur=cur
        self.conn = conn
    #获取数据
    def take_data(self,name = "",tel = ""):
        base_sql = "select * from bmsd"
        where_sql = " where name like ('%s') and telephone like ('%s') " %('%'+name+'%','%'+tel+'%')
        sql=base_sql+where_sql
        #print(sql)
        row_num = self.cur.execute(sql)
        #print (row_num)
        result = self.cur.fetchall()
        return result
    #变更数据
    def change_date(self,code,**kw):
        base_sql = "update bmsd set"
        set_sql = ""
        if set(['name','company','telephone','email']).issubset(kw.keys()):
            set_sql = set_sql + " name = '%s'," % (kw['name'])
            set_sql = set_sql + " company = '%s'," % (kw['company'])
            set_sql = set_sql + " telephone = '%s'," % (kw['telephone'])
            set_sql = set_sql + " email = '%s'," % (kw['email'])
        if len(set_sql) >0:
            set_sql = set_sql[:-1]+" "
            where_sql = "where code = %d" % (int(code))
            sql = base_sql + set_sql + where_sql
            #print(sql)
            row_num = self.cur.execute(sql)
            self.conn.commit()
            return True
        #self.db_close()
    #插入新增数据
    def insert_data(self,**kw):
        base_sql = "insert into bmsd (name,company,telephone,email) "
        val_sql = ""
        if  set(['name','company','telephone','email']).issubset(kw.keys()):
            val_sql = "values('%s','%s','%s','%s')" % (kw['name'],kw['company'],kw['telephone'],kw['email'])
        if len(val_sql) !=0:
            sql = base_sql+val_sql
            #print(sql)
            row_num = self.cur.execute(sql)
            self.conn.commit()
            return True
        #self.db_close()
    #删除数据
    def delete_data(self,code):
        base_sql = "delete from bmsd "
        where_sql = " where code = %d" % (int(code))
        sql = base_sql+where_sql
        #print(sql)
        self.cur.execute(sql)
        self.conn.commit()
        #self.db_close()
        return True

    #关闭数据库链接
    def db_close(self):
        self.cur.close()
        self.conn.close()
#----------------------------------测试---------------------------------------------
#sd = systemDB()
#sd.change_date(100001,company="中信证券",telephone="010-33563321",email="zhangsan@cs.ecitic.com")
#sd.change_date(100002,telephone="0734-35623353")
#sd.insert_data(name="陈裕源",company="长亮证券",telephone="021-31469762",email="chenyuyuan@sunline.cn")
#sd.delete_data(100001)
