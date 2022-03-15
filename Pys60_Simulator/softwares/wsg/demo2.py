# -*- coding: utf-8 -*-
import sys
import os
path = os.getcwd()
index = path.rfind('\\')
path=path[:index]
sys.path.append(path)
index = path.rfind('\\')
path=path[:index]
sys.path.insert(-1,path+"\\python\\pysoft\\wsg\\")
from wsg import *

ab = lambda:appuifw.note(cn("Hello World!"))

def main():
    a = Window()
    GroupButton(a,cn("计算器"),20,12,SCRX-40,60)
    b = GroupButton(a,u"",20,80,SCRX-40,SCRY-100)
    w = (SCRX-40-80)/3
    PushButton(b,u"1",20,20,w,30,ab)
    PushButton(b,u"2",20+w+20,20,w,30,ab)
    PushButton(b,u"3",40+2*w+20,20,w,30,ab)
    PushButton(b,u"4",20,60,w,30,ab)
    PushButton(b,u"5",20+w+20,60,w,30,ab)
    PushButton(b,u"6",40+2*w+20,60,w,30,ab)
    PushButton(b,u"7",20,100,w,30,ab)
    PushButton(b,u"8",20+w+20,100,w,30,ab)
    PushButton(b,u"9",40+2*w+20,100,w,30,ab)
    PushButton(b,u"*",20,140,w,30,ab)
    PushButton(b,u"0",20+w+20,140,w,30,ab)
    PushButton(b,u"#",40+2*w+20,140,w,30,ab)
    a.run()
    
main()
import e32
e32.ao_yield()
