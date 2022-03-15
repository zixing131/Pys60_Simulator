#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 16:18
# @Author  : zixing
# @QQun    : 140369358
# @File    : test.py
# @Software: PyCharm
import graphics
from Pys60_Simulator.pys60Core.fonts import fonts

def getFontSize(str,size):
    if(fonts.has_key(str)==False):
        return [-1,-1]
    basesize = 15
    sizeof15 = fonts[str]
    x = int( round( ((float)(size)/(float)(basesize)) * sizeof15[0],0))
    y= int(round(((float)(size)/(float)(basesize)) * sizeof15[1],0))
    sizeofsize = (x,y)
    return sizeofsize
def getStrSize(str,size):
    count = 0
    max = 0
    for i in str: 
        msize = getFontSize(i,size)
        count+=msize[0]
        if(max<msize[1]):
            max = msize[1]
    return [count,max]
dic = {}
'''
for i in range(0x4e00,0x9fa5): 
    ttt=hex(i) .replace('0x','')  
    tt = ('\u'+ttt).decode('unicode_escape')
    #print(tt)
    t=graphics.getTextFontWidth(tt,15)
    dic[tt]=t  
open('fonts.py','wb').write('fonts = '+(str(dic)))
'''
for i in range(1,100):
    a = getStrSize('你好啊啊'.decode('u8'),i)
    b= graphics.getTextFontWidth('你好啊啊'.decode('u8'), i)
    print(a,b, a==b)
 
print('ok')
