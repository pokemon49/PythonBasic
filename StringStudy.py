#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class StringStudy(object):
    list1= ['666i_1.jpg', '666i_2.jpg', '666i_3.jpg', '666i_4.jpg', '666i_5.jpg', '666i_6.jpg', '666i_7.jpg', '666i_8.jpg', '666i_9.jpg', '666i_10.jpg']
    #print(type(list1))
    #for list in list1:
    #    print(list)
    #序列添加
    ##末尾添加
    list1.append('777i_10.jpg')
    ##指定位置添加
    list1.insert(2,'877i_10.jpg')
    #序列删除
    ##未尾删除
    list1.pop()
    ##指定位置删除
    list1.pop(2)
    #原始字符串
    print(r'c:\windows\name')
    #换行字符串,'\'抵消换行
    print('''\
    Usage Printer New Line
    ：
    Use New Line\
    ''')
    #固定字符重复和连接,不适用于变量与字符串混合
    print("abc"*5+"def")
    s1 = "py"
    s2 = "thon"
    print(s1+s2)
    #自连接字符串
    print("abdc"
          "def")
    #字符串切片
    s3=s1+s2
    print(s3[3:6])
    print(s3[:2])
    print(s3[3:])
    print(s3[-2:])
    #大写首写母
    print("abcdf".capitalize())
    #全部小写化
    print("ABDCEF".casefold())
    #全部小写化
    print("ABDCEF".lower())
    #以字符串靠左,填充指定的字符串到指定的位数
    print("ABCDEF".center(10,"*"))
    #以字符串为中心,以空格或指定字符填充
    print("ABDCEF".center(10,"*"))
    #查找指定字符串出现的次数
    print("wer6ee546z8".count("e",4,8))
    #将字符串转换为bytes
    print("编码".encode("GB2312"))
    #将bytes编码转换为字符串
    print(b'\xb1\xe0\xc2\xeb'.decode("GB2312"))
    #查找是否为指定的字符串结尾
    print("Balance".endswith("ance",3,8))
    #把字符串中的 tab 符号('\t')转为空格，tab 符号('\t')默认的空格数是8
    print(" Lin ".expandtabs(0))
    #查找字符串是否存在字符串中的位置
    print("jdoafdkwejoc".find("fd",2,10))
    print("jdoafdkwejoc".index("fd", 2, 10))  #查找位置，没找到会报错
    #链接指定的序列
    str2="<>"
    print(str2.join(list1))
    #截掉字符串左边的空格或指定字符
    print("    jdoafdkwejoc".lstrip())
    print("jdoafdkwejoc".lstrip("jd"))
    ## 把末尾的'\n'删掉
    print(b'dfalkdjoifdafljlj/n'.strip())


    str1 = "https://www.fdfsdf.info/fs4-043126";
    print(str1.rfind("."))
    #替换
    str2 = str1[str1.rfind("."):]
    #切分
    str3 = str1.split("/")[-1]
    print(str1)
    print(str2)
    print(str3)
    print(str1.find("cc"))
    #获取字符的整数表示
    print("中的数字表示："+str(ord("中")))
    #格式化输出
    ## %d:整数
    print("整数格式化：%d,%02d,%3d" % (70,7,51))
    ## %f:浮点数
    print("浮点数格式化：%f,%.3f" % (3.14,3.14159265))
    ## %s:字符串
    print("字符串格式化：%s" % ("测试字符"))
    ## %x:十六进制数
    print("十六进制格式化：%x" % (0x7f36c7))

    #tuple不可变序列
    t = ("Python", 1, 33)
    print(t[0]) 
    #声明单元素tuple
    t = (3,)
    print(t[0])

    def format_function(self):
        # 格式化字符串
        ##默认顺序
        print("{},{}{}".format("Hello", "Python", "!"))
        ##指定顺序
        print("{0},{2} {1}".format("Hello", "Python", "New"))
        ##指定名称
        print("第一名：{First} 第二名：{Second} 第三名：{Thired}".format(First="abc", Second="def", Thired="eeef"))
        ##字典类型参数
        d1 = {"First": "Zhou", "Second": "Zhao"}
        print("第一位：{First} 第二位：{Second}".format(**d1))
        ##序列类型参数
        l1 = ["Lin", "JinHang"]
        print("Surame:{0[0]} Name:{0[1]}".format(l1))  # "0"必须
        ##Mapping类型参数

        "My Name is {name}".format_map({'name': "abc"})
        #格式化数字
        #^, <, > 分别是居中、左对齐、右对齐，后面带宽度， : 号后面带填充的字符，只能是一个字符，不指定则默认是用空格填充。
        #+ 表示在正数前显示 +，负数前显示 -；  （空格）表示在正数前加空格
        #
        ## 保留小数点后两位
        print("{:.2f}".format(3.1415926538))
        ## 带符号保留小数点后两位
        print("{:+.2f}".format(3.1415926538))
        ## 带符号保留小数点后两位
        print("{:+.2f}".format(3.1415926538))
        ## 不带小数
        print("{:.0f}".format(3.1415926538))
        ## 数字补零 (填充左边, 宽度为2)
        print("{:0>2d}".format(7))
        ## 数字补x (填充右边, 宽度为4)
        print("{:x<4d}".format(7))
        ## 数字补x (填充右边, 宽度为4)
        print("{:x<4d}".format(7))
        ## 以逗号分隔的数字格式
        print("{:,}".format(3.1415926538))
        ## 百分比格式
        print("{:.2%}".format(3.1415926538))
        ## 指数记法
        print("{:.2e}".format(3.1415926538))
        ## 右对齐 (默认, 宽度为10)
        print("{:10d}".format(7))
        ## 左对齐 (宽度为10)
        print("{:<10d}".format(7))
        ## 中间对齐 (宽度为10)
        print("{:^10d}".format(7))
        ## 进制 b、d、o、x 分别是二进制、十进制、八进制、十六进制。
        print('{:b}'.format(11))  #2
        print('{:d}'.format(11))  #10
        print('{:o}'.format(11))  #8
        print('{:x}'.format(11))  #16
        print('{:#x}'.format(11)) #
        print('{:#X}'.format(11)) #

    def Distingush(self):
        #判断是否由字母或数字组成
        print("adb123".isalnum())
        # 判断是否只由字母组成
        print("adb123".isalpha())
        # 判断是否只由数字组成
        print("adb123".isdigit())
        #判断是否只由小写字母组成
        print("adb123".islower())
        # 判断是否只由数字组成，针对Unicode对像，只需要在对像前添加u即可成为Unicode对像
        print("adb123".isnumeric())
        # 检查字符串是否只包含十进制字符。这种方法只存在于unicode对象。
        print("adb123".isdecimal())
        # 判断是否由空格组成
        print("adb123".isspace())
        # 判断检查字符串中所有单词首写母是否为大写，其它字母为小写
        print("adb123".istitle())
        # 判断是否都由大写字母组成
        print("adb123".isupper())
        # 判断字符串是否可打印或是为空
        print("adb123".isprintable())

    def text_slice(self):
        print("纯文本切片解析：")
        invoice = """
        0.....6................................40........52...55........
        1909  Pimoroni PiBrella                $17.50    3    $52.50
        1489  6mm Tactile Switch x20           $4.95     2    $9.90
        1510  Panavise Jr. - PV-201            $28.00    1    $28.00
        1601  PiTFT Mini Kit 320x240           $34.95    1    $34.95
        """
        SKU = slice(0, 6)
        DESCRIPTION = slice(6, 40)
        UNIT_PRICE = slice(40, 52)
        QUARTITY = slice(52, 55)
        ITEM_TOTAL = slice(55, None)
        line_items = invoice.split('\n')[2:]
        for item in line_items:
            print(item[UNIT_PRICE], item[DESCRIPTION])
    def run(self):
        self.text_slice()
        self.Distingush()
        self.format_function()

ss =  StringStudy()
ss.run()
