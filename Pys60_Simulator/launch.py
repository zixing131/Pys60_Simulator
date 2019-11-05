# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import msys
msys.send_bg()
import graphics as gr
scrshot = gr.screenshot()
import appuifw as ap
cvs = ap.Canvas()
def redraw(rect):
    cvs.blit(scrshot)


ap.app.body = cvs = ap.Canvas(redraw_callback = redraw)
ap.app.screen = 'full'
import os
mypath=u"..\\python\\pygame\\2048_maps\\"
splash = gr.Image.open(mypath+'splash_2.1.png')
import sysinfo
x, y = sysinfo.display_pixels()
if x > y : 
    scrshot.blit(splash, target = (72, 78))
else : 
    scrshot.blit(splash, target = (32, 117))
msys.send_fg()
import main