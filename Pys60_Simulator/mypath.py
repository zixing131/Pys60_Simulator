#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 10:42
# @Author  : zixing
# @QQun    : 140369358
# @File    : mypath.py
# @Software: PyCharm
import os
def getmypath(path="\\python\\pysoft\\ithome\\"):
    if (os.name != 'nt'):
        mypath = 'e:'+path
        return mypath
    p=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    return p+path
if __name__ == '__main__':
    getmypath()
