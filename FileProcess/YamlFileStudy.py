#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'Yaml文件使用基础类'
__author__ = '林金行'
import yaml, os , datetime
'''
#url = r'E:\EVETools\EVEDB\sde\bsd\trnTranslations.yaml'
url = r'E:\EVETools\EVEDB\sde-20190911-2-TRANQUILITY\sde\fsd\marketGroups.yaml'
lang = "zh"
stream = open(url, mode='r', encoding='utf8')
strs = stream.readlines()
str1 = ''
marketgroup = {"marketGroupID": "", "descriptionID": "", "hasTypes": "", "iconID": "", "nameID": "", "parentGroupID": ""}
#dict = {"a": {"b": "c"}}
for str in strs :
    str1 = str1 + str
dates = yaml.load(str1,yaml.Loader)
key_list = dates.keys()
for key in key_list:
    marketgroup = {"marketGroupID": "", "descriptionID":"", "hasTypes":"", "iconID": "", "nameID": "", "parentGroupID": ""}
    marketgroup["marketGroupID"] = key
    if 'descriptionID' in dates.get(key) :
        marketgroup["descriptionID"] = dates.get(key).get('descriptionID').get(lang)
    marketgroup["hasTypes"] = dates.get(key).get('hasTypes')
    marketgroup['iconID'] = dates.get(key).get('iconID')
    marketgroup['nameID'] = dates.get(key).get('nameID').get(lang)
    marketgroup['parentGroupID'] = dates.get(key).get('parentGroupID')
    #print(marketgroup)
'''
#for date in dates:
#    print(date)
#    for d in date:
#        print(len(d))
#    'date = yaml.load(str)
#    'print(date)
url = r'E:\EVETools\EVEDB\sde-20190911-2-TRANQUILITY\sde\bsd\dgmTypeAttributes.yaml'
data_list = []
time1 = datetime.datetime.now()
with open(url, "r", encoding="utf8") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    for d in data:
        pass
        #print(d)
        #data_list.append(d.values())
        #print(data_list)
time2 = datetime.datetime.now()
t = (time2 - time1).seconds
print(t)
str1 = ""
time1 = datetime.datetime.now()
stream = open(url, mode='r', encoding='utf8')
strs = stream.readlines()
for str in strs :
    str1 = str1 + str
datas = yaml.load(str1,yaml.Loader)
for d in datas:
    pass
time2 = datetime.datetime.now()
t = (time2 - time1).seconds
print(t)
pass

