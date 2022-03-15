#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 10:05
# @Author  : zixing
# @QQun    : 140369358
# @File    : pys60Socket.py
# @Software: PyCharm
import socket

functions = ['access_point','access_points','set_default_access_point']

def access_point(a=''):
    return 1

def access_points():
    dic = [
        {'iapid': 1 , 'name': 'cmnet'},
        {'iapid': 2 ,'name': 'cmwap'}
    ]
    return dic
def set_default_access_point(point):
    pass

for i in functions:
    setattr(socket, i, eval(i))
