# -*- coding: utf-8 -*-

zt=u"Sans MT 936_s60",15,1
import appuifw as ui,e32
import graphics as ph,base64,thread,os,random
from BingyiApp import *
cn=lambda x:x.decode("u8")
sleep=e32.ao_sleep
mypath=u"..\\python\\pysoft\\ithome\\"

class ithomeUi(object,):
    def __init__(self):
        pass
    def main(self):
        ui.app.Yield()

app=App(mypath+'splash.png',3)
app.TitleName=cn("IT之家")
#app.keyType=0
app.allClass([ithomeUi])
app.main()
