# -*- coding: utf-8 -*- 
import sys
import os
path = os.getcwd()
index = path.rfind('\\')
path=path[:index]
sys.path.append(path+"\\python\\pysoft\\lolbox\\app\\")
import lol
