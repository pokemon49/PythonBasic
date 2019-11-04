#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'内建模块学习'
__author__ = '林金行'

#时间模块
from datetime import datetime,timedelta,timezone
#工具模块
from collections import namedtuple,deque,defaultdict,OrderedDict,Counter
class InnerModelStudy(object):
    def timeexec(self,time,tz):
        tz = tz.replace(":","")
        time = datetime.strptime(time+tz,'%Y-%m-%d %H:%M:%S%Z%z')
        #tmz = timezone()
        time = time.timestamp()
        print(time)
    def timemodel(self):
        now = datetime.now()
        st = datetime(2018,8,30,18,00,00,1123)
        ts = st.timestamp()
        sts = datetime.fromtimestamp(ts)
        uts = datetime.utcfromtimestamp(ts)
        sst = datetime.strftime(st,'%Y-%m-%d %H:%M:%S')
        tst = datetime.strptime(sst,'%Y-%m-%d %H:%M:%S')
        tm = now + timedelta(hours=10,days=1)
        tz = tm.replace(tzinfo=timezone(timedelta(hours=8)))
        utct = datetime.utcnow().replace(tzinfo=timezone.utc)
        bjtm = utct.astimezone(timezone(timedelta(hours=8)))
        djtm = bjtm.astimezone(timezone(timedelta(hours=9)))
        print(now)
        print(st)
        print("st的timestamp:"+str(ts))
        print("ts转换回时间:" + str(sts))
        print("ts转换回UTC时间:" + str(uts))
        print("时间转换字符串:"+sst)
        print("字符串转换时间:" + str(tst))
        print("时间运算:" + str(tm))
        print("设置时区:" + str(tz))
        print("UTC时间：" + str(utct))
        print("UTC获取北京时区时间：" + str(bjtm))
        print("北京获取东京时区时间：" + str(djtm))
        self.timeexec('2015-6-1 08:10:30', 'UTC+07:00')
        self.timeexec('2015-5-31 16:10:30', 'UTC-09:00')
    def coll(self):
        #自定义tuple
        P = namedtuple('Point',['x','y'])
        a = P(1,2)
        print("自定义tuple:"+str(a.x)+"、"+str(a.y))
        #头尾操作的List
        ql = deque(['d','e','f'])
        ql.append('x')
        ql.appendleft('c')
        print(ql)
        #有默认值的dict
        dd = defaultdict(lambda :"N/A")
        dd['key1'] = 'abc'
        print("dict default value:"+dd["default"])
        #排序dict
        d = dict([('X', 7), ('E', 11), ('A', 23), ('C', 13)])
        od = OrderedDict([('X',7), ('E', 11), ('A', 23), ('C', 13)])
        print(d)
        print(od)
        #Counter计数器
        c = Counter()
        c["cdef"]= c["cdfwd"] + 1
        print(c["fx"])

    def run(self):
        print("--时间模块")
        self.timemodel()
        print("--工具模块")
        self.coll()
        pass

ims = InnerModelStudy()
ims.run()


