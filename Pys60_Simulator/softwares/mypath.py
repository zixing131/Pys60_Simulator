#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 10:42
# @Author  : zixing
# @QQun    : 140369358
# @File    : mypath.py
# @Software: PyCharm
import os
def getmypath(path="\\python\\pysoft\\ithome\\"):
    #print(os.name)
    if (os.name != 'nt' and os.name!='posix'):
        mypath = 'e:'+path
        return mypath

    path = path.replace("\\","/")
    p=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    p = p.replace("\\", "/")
    p=p[:p.rfind("/")+1]
    if(path.startswith("/")):
        path=path[1:]
    realpath = os.path.join(p,path)
    return realpath
if __name__ == '__main__':
    getmypath()
