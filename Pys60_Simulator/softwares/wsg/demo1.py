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

def main():
    a = Window()
    StaticEdit(a,cn(open(r"c:\python\wisdom.txt").read()),0,0,SCRX,SCRY,0xFFFFFF,20,0)
    a.run()
    
main()
import e32
e32.ao_yield()
