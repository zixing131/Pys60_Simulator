# -*- coding: utf-8 -*-
import appuifw,e32
from graphics import*
def cn(x):return x.decode("u8")
canvas=appuifw.Canvas()
appuifw.app.body=canvas
run=1
img=Image.new((240,320))
img.clear(0)
print dir(img)
x=0
y=0
list=["菜单一","菜单二","菜单三"]
#Lang
def app():
    img.rectangle((0,80,80,140), 0x222299,fill=0x009110,width=2)
    img.rectangle((0,y+80,
    80,y+100),0x666666,
    fill=0x002233)
    for i in range(len(list)):
        img.text((10,100+20*i),cn(list[i]),0x990000)
        img.rectangle((y+50,30,
        y+90,60),0x002255)
def press():
    global y
    if y==0:
        appuifw.note(cn(list[0]))
    if y==20:
        appuifw.note(cn(list[1]))
    if y==40:
        appuifw.note(cn(list[2]))

def Move(a,b):
    global x,y
    x+=a
    y+=b
    if y>40:y=0
    if y<0:y=40

def Menu():
    while 1:
        img.clear(0)
        app()
        canvas.blit(img)
        e32.ao_yield()

canvas.bind(63497,lambda:Move(20,-20))
canvas.bind(63498,lambda:Move(-20,20))
canvas.bind(63557,lambda:press())

Menu()

#lock.wait()