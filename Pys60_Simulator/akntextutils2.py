#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 13:25
# @Author  : zixing
# @QQun    : 140369358
# @File    : akntextutils2.py
# @Software: PyCharm
import akntextutils
def to_array(content,dense,width):
    return akntextutils.wrap_text_to_array(content,dense,width)
