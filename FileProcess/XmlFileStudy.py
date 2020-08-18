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

print("".center(20, r"-"))


#  xml.etree.ElementTree使用方法
import xml.etree.cElementTree as et
tree = et.parse(r'E:\Study\XML\Study.xml')

root = tree.getroot()
# 从文本中读取
# root = ET.fromstring(country_data_as_string)
#根标识属性
print('#根标识属性')
print(root.tag)
#根属性信息
print('#根属性信息')
print(root.attrib)
#子属性信息查询
print('#子属性信息查询')
for child in root:
    print(child.tag, child.attrib)
#通过索引查询值
print('#通过索引查询值')
print(root[0][0][1].text)

#查找属性值
print('#查找属性值')
##在所有元素及子元素中查找。
for neighbor in root.iter("type"):
    print(neighbor.text)
##获取本元素及其子元素的信息
for test in root.findall("movie"):
    ##获取本元素信息
    year = test.find("rank").text
    ##获取属性值信息
    mune = test.get("add")
    item = test.items()
    print(year)
    print(mune)
    print(item)
##Xpath查找功能
### * 表示所有子元素
### . 表示当前元素
### //表示所有子元系包括其孙元素等
### ..表示父节点元素
### [@attrrib] 含有某个属性值
### [@attrrib = "abc"] 含有某个属性值，且属性值等于abc
### [tag] 含有指定子节点的元素
### [.='abc'] 指定元素的字符是abc的元素
### [tag = 'abc'] 含有指定节点，且节点值为abc的元素
### [1] 含有指定个数属性的元素
print('#Xpath查找功能')
### .查找当前节点/元素
for r in root.findall("."):
    print(r.tag)
    pass

### 查找某节点下的子节点
for r in root.findall("./movie/test/format"):
    print(r.text)
### 查找含有指定子节点，且有某个属性值限制的节点
for r in root.findall('.//year/..[@ mune= "ss"]'):
    print(r.tag)
### 查找含有指定子节点，且有某个属性值限制的节点
for r in root.findall('.//*[@ mune= "ss"]/year'):
    print(r.text)
### 查找含有指定个数属性的元素
for r in root.findall('.//test/year[1]/../..'):
    print(r.attrib['title'])
### 查找有指定节点，且限定节点内容的元素
for r in root.findall(".//test[format='VHS']"):
    print(r.tag)
### 查找有指定节点，且限定节点内容的元素
for r in root.findall(".//test/format[.='PGS']/../.."):
    print(r.attrib['title'])
#修改属性信息
for year in root.iter("year"):
    new_year = int(year.text)-1
    year.text = str(new_year)
    #添加/修改属性值
    year.set("update", "yes")
#删除元素信息
for moive in root.iter("movie"):
    rank = int(moive.find("rank").text)
    if rank >= 100:
        root.remove(moive)
#解析名称空间XML
trees = et.parse(r'E:\Study\XML\NameSpace.xml')
roots = trees.getroot()
ns = {'rela_person': 'http://people.example.com',
      'role': 'http://characters.example.com'}
for actor in roots.findall('rela_person:actor', ns):
    name = actor.find("rela_person:name", ns)
    print(name.text)
    for char in actor.findall('role:character', ns):
        print(' -->', char.text)

#建构元系信息
a = et.Element('a')
b = et.SubElement(a, 'b')
c = et.SubElement(a, 'c')
d = et.SubElement(c, 'd')
et.dump(a)
for moive in root.iter("movie"):
    moive.append(a)
#更新XML文件
tree.write(r'E:\Study\XML\Studyt.xml')

#快速构建XML
print("".center(20, r"%"))
parser = et.XMLPullParser(['start', 'end'])
parser.feed('<mytag>sometext')
list(parser.read_events())
parser.feed(' more text</mytag>')
for event, elem in parser.read_events():
    print(event)
    print(elem.tag, 'text=', elem.text)

print("XMLParser构造测试")
from xml.etree.cElementTree import XMLParser
class maxDepth:
    maxDepth = 0
    depth = 0
    def start(self, tag):
        self.depth += 1
        if self.depth > self.maxDepth:
            self.maxDepth = self.depth
    def end(self, tag):
        self.depth -= 1
    def data(self, data):
        pass
    def close(self):
        return self.maxDepth
target= maxDepth
parser = XMLParser(target=target)
exampleXml = """
<a>
   <b>
   </b>
   <c>
     <d>
     </d>
   </c>
</a>"""
parser.feed(exampleXml)
parser.close()
