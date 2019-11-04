#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'元类学习用例'
__author__ = '林金行'

from ImageStudy import *

def dn(self):
    print("This is Type Create Object!")

Is = ImageStudy()
Is.run()
print(type(ImageStudy))
print(type(Is))
#使用type创建Class
print("--type创建Class")
             #Class名称,继承的类[属于tuple类],绑定方法
Hello = type('Hello',(object,),dict(hello=dn))
h = Hello()
h.hello()
print(type(Hello))
print(type(h))

#使用metaclass创建类
print('--使用metaclass创建类')
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):#参数说明：当前准备创建的类的对象，类的名字，类继承的父类集合，类的方法集合
        attrs['add'] = lambda self,value:self.append(value)
        return type.__new__(cls, name, bases, attrs)

class MyList(list,metaclass=ListMetaclass):
    pass

l = MyList()
l.add(1)
l.add(2)
l.add(3)
l.add(5)
print(l)
print(type(MyList))
print(type(l))

#ORM(Object Relational Mapping)框架
print('--ORM(Object Relational Mapping)框架')
##Field保存字段名和字段类型：
class Field(object):
    def __init__(self, name, column_type):
        self.name=name
        self.column_type=column_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
    pass
##定义具体的字段类型
class StringField(Field):
    def __init__(self,name):
        super(StringField, self).__init__(name, 'varchar(100)')
    pass
class IntegerField(Field):
    def __init__(self,name):
        super(IntegerField, self).__init__(name, 'bigint')
    pass
##定义ModelMetaclass
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found Model:%s'% name)
        mappings = dict()
        for k ,v in attrs.items():
            if isinstance(v,Field):
                print("Found Mapping:%s ==> %s" % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings #保存属性和列的映射关系
        attrs['__table__'] = name #假设表名和类名一致
        return type.__new__(cls, name , bases, attrs)
    pass

#定义基础类Model
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' Object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    def save(self):
        fields = []
        params = []
        agrs = []
        for k,v in self.__mappings__.items():
            fields.append(v.name)
            params.append("'"+str(getattr(self,k,None))+"'")
            agrs.append(getattr(self,k,None))
        sql = 'insert into %s(%s) values(%s)' % (self.__table__, ','.join(fields),','.join(params))
        print('SQL: %s' % sql)
        print('AGRS: %s' % str(agrs))
    pass

##User表
class User(Model):
    #定义类的属性到列的映射
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    pass
u = User(id = 12345,name='Jake',email='Jake@JJ.com',password="jpwd")
u.save()
