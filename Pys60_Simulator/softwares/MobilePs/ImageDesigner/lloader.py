# -*- coding: utf-8 -*-
import appuifw
import graphics
from os import path as path
import os
from sysinfo import display_pixels as display_pixels
__version__ = 1.4
if path.exists('C:\\System\\Apps\\ImageDesigner\\palette.dat') : 
    drive = 'c:\\'
else : 
    drive = 'e:\\'
path = os.getcwd()
mypath2=path+"\\ImageDesigner\\"

logo = graphics.Image.open(mypath2+'\\skin\\id_logo.png')
appuifw.app.screen = 'full'
appuifw.app.body = canv = appuifw.Canvas(redraw_callback = None, event_callback = None)
canv.blit(logo, target = (((display_pixels()[0] - logo.size[0]) / 2), ((display_pixels()[1] - logo.size[1]) / 2)))
canv.blit(logo, target = (((display_pixels()[0] - logo.size[0]) / 2), ((display_pixels()[1] - logo.size[1]) / 2)))
import sys
sys.path.insert(-1,mypath2)