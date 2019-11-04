import pymysql
class SavetoMysqlPipeline(object):
    #def process_item(self, item, spider):
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="Study", passwd="study", db="Scrapy", charset="utf8")
        cur = conn.cursor()
        sql = "select * from JD_prod_basic_info where prod_code=232344"
        #sql = "insert into JD_prod_basic_info values(4163951,\"联想(Lenovo)拯救者R720 15.6英寸游戏笔记本电脑(i7-7700HQ 8G 1T+128G SSD GTX1050Ti 4G IPS 黑)\",7399.00,\"F:\\Study\\Python\\Scrapy\\img\\dmoz\\['4163951'].jpg\",\"//item.jd.com/4163951.html\")"
        num = cur.execute(sql)
        print(num)
        #conn.commit()
        rows = cur.fetchall()
        for dr in rows:
            print(dr)
       # return item