#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 'XML 文件操作学习记录'
__author__ = '林金行'

from xml.dom.minidom import parse,Element,NodeList,Text
import os.path
import xml.dom.minidom



class XmlFileStudy():

    def __init__(self, filePath):
        if isinstance(filePath,str):
            assert AttributeError("输入地址错误")
        if not os.path.exists(filePath):
            assert AttributeError("输入文件不存在")
        readfile = parse(filePath)
        self.initfile = readfile.documentElement

    def getsetcoll(self,setName):
        return self.initfile.getElementsByTagName(setName)

    def getElement(self,coll,eleName):
        elements = coll.getElementsByTagName(eleName)
        for element in elements:
            elementChilds = element.childNodes
            for elementChild in elementChilds:
                elementValue =elementChild.nodeValue
        return elementValue


    def getvalue(self,attrName):
        attrList = attrName.split(".")
        initcolls = self.initfile
        initList = []
        attrlen = len(attrList)
        if attrlen == 1:
            attr = attrList[0]
            if isinstance(initcolls, Element) and attr.find("@") == 0:
                attr = attr.replace("@", "")
                if initcolls.hasAttribute(attr) :
                    initList.append(initcolls.getAttribute(attr))
        else:
            initList = self.getvalues(attrList,initcolls,attrlen)
        return initList

    def getvalues(self,attrName,initcolls,attrlen):
        initvalue = []
        if len(attrName) > 1:
            initcolls = initcolls.getElementsByTagName(attrName[0])
            if isinstance(initcolls,NodeList):
                for initcoll in initcolls:
                    if len(attrName) == attrlen:
                        initvalue.append(self.getvalues(attrName[1:], initcoll,attrlen))
                    else:
                        initvalue = self.getvalues(attrName[1:], initcoll,attrlen)
        elif attrName[0].find("@") == 0:
            attr = attrName[0].replace("@","")
            initvalue = initcolls.getAttribute(attr)
        else:
            initvalue = self.getElement(initcolls,attrName[0])
        return initvalue
    pass

xfs = XmlFileStudy(r"E:\Study\XML\Study.xml")
colls = xfs.getsetcoll("movie")
print(xfs.getvalue("movie.@title"))
print(xfs.getvalue("@shelf"))
print(xfs.getvalue("movie.test.type"))
# print(type(colls))
# for coll in colls:
#     val = xfs.getElement(coll, "type")
#    #print(val)
print("".center(20, "-"))

DOMTree = parse(r"E:\Study\XML\Study.xml")
Coll = DOMTree.documentElement
if Coll.hasAttribute("shelf"):
    print ("Root element:%s" % Coll.getAttribute("shelf"))
Movies = Coll.getElementsByTagName("movie")

for Movie in Movies:
    print("Movie".center(11,"*"))
    if Movie.hasAttribute("title"):
        print("Title: %s" % Movie.getAttribute("title"))
    types = Movie.getElementsByTagName("type")[0]
    print("Type: %s" % types.childNodes[0].data)
    #配置属性值
    Movie.setAttribute("add","ABC")

# fp = open(r"E:\Study\XML\Studyt.xml", "w", encoding = "utf-8")
# Coll.writexml(fp,indent='',addindent='\t',newl='\n')
# fp.close()

print("".center(20, r"%"))
# Etree使用方法
import xml.etree.cElementTree as et
tree = et.parse(r'E:\Study\XML\Studyt.xml')
root = tree.getroot()
# 从文本中读取
# root = ET.fromstring(country_data_as_string)
#根标识属性
print(root.tag)
#根属性信息
print(root.attrib)
#子属性信息查询
for child in root:
    print(child.tag, child.attrib)
#通过索引查询值
print(root[0][0][1].text)

#查找属性值
for neighbor in root.iter("type"):
    print(neighbor.text)
for test in root.findall("movie"):
    year = test.find("test").text
    mune = test.get("title")
    print(year, mune)
#修改属性信息
for year in root.iter("year"):
    new_year = int(year.text)+1
    year.text = str(new_year)
    #添加/修改属性值
    year.set("update", "yes")
#删除元素信息
for moive in root.iter("movie"):
    rank = int(moive.find("rank").text)
    if rank >= 100:
        root.remove(moive)
#建构元系信息
a  = et.Element('a')
b  = et.SubElement(a, 'b')
c  = et.SubElement(a, 'c')
d  = et.SubElement(c, 'd')
et.dump(a)
#更新XML文件
tree.write(r'E:\Study\XML\Studyt.xml')
#
#快速构建XML
print("".center(20, r"%"))
parser = et.XMLPullParser(['start', 'end'])
parser.feed('<mytag>sometext')
list(parser.read_events())
parser.feed(' more text</mytag>')
for event, elem in parser.read_events():
    print(event)
    print(elem.tag, 'text=', elem.text)