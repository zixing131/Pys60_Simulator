# -*- coding: utf-8 -*-
import sysgraphics
try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk
from PIL import Image as Image2
from PIL import ImageDraw
from PIL import ImageFont
import os
import string 
import tkFont
from appuifw import app as _app
Draw=lambda x: x

FONT_BOLD=1
FONT_ITALIC=2
FONT_SUBSCRIPT=4
FONT_SUPERSCRIPT=8
FONT_ANTIALIAS=16
FONT_NO_ANTIALIAS=32

#win=sysgraphics.GraphWin("Pys60 Simulator",240,320)
def RGB_to_Hex(tmp):
    rgb = tmp #将RGB格式划分开来
    strs = '#'
    for i in rgb:
        num = int(i)#将str转int
        #将R、G、B分别转化为16进制拼接转换并大写
        strs += str(hex(num))[-2:].replace('x','0').upper()
        
    return strs 
	
def hex2rgb(hexcolor):
  rgb = [(hexcolor >> 16) & 0xff,
      (hexcolor >> 8) & 0xff,
      hexcolor & 0xff
     ]
  return rgb
def rgb2hex(rgbcolor):
  r, g, b = rgbcolor
  return (r << 16) + (g << 8) + b
  
myfnt=None
lastfont=None
def GetFont(fill=None,font=None):
    global myfnt,lastfont
    if(font==lastfont):
        pass
    else:
        if(os.path.exists("fonts\\S60SC.ttf")):
            myfnt = ImageFont.truetype("fonts\\S60SC.ttf", font[1])
        elif(os.path.exists("Pys60_Simulator\\fonts\\S60SC.ttf")):
            myfnt = ImageFont.truetype("Pys60_Simulator\\fonts\\S60SC.ttf", font[1])
    lastfont = font
    return myfnt

def getTextFontWidth(text,size=18):
    im = Image2.new('RGB', (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    w, h = draw.textsize(text, font=GetFont(font=('dense',size)))
    return w,h

def convertColor(bgcolor):
    if(type(bgcolor) is tuple):
        bgcolor = RGB_to_Hex(bgcolor)
    elif(type(bgcolor) is int):
        bgcolor = hex2rgb(bgcolor)
        bgcolor = sysgraphics.color_rgb(bgcolor[0],bgcolor[1],bgcolor[2]) 
    return bgcolor
            
class Image:
    def __init__(self,size,mode=None,canvas = None):
        if(mode!='L'):
            self.image = Image2.new("RGBA",size,(255,255,255))
        else:
            self.image = Image2.new("RGBA", size, (255, 255, 255))

        self.size = size
        self._image = self.size
        self.mode=mode
        self.canvas = canvas
        #win=sysgraphics.GraphWin(width=size[0],height=size[1])
        #_app.redraw()
    def transpose(self,a=1):
        return self
    def open(path):
        img = Image2.open(path)
        img2 = Image(img.size)
        img2.image = img
        return img2 	
    def load(self,path):
        img = Image2.open(path)
        if(self.mode!=None):
            img = img.convert(self.mode)
        self.image = img
        self.size = img.size
    def new(size,mode=None):
        return Image(size,mode)
    
    def rectangle(self,pos,color = 0x0,fill=0x0,width=1,outline=0x0):
        draw = ImageDraw.Draw(self.image)
        fill = convertColor(fill)
        if(outline!=0):
            outline = convertColor(outline)
            draw.rectangle((pos[0],pos[1],pos[2],pos[3]), fill=fill,outline=outline,width=width)
        else:
            draw.rectangle((pos[0],pos[1],pos[2],pos[3]), fill=fill,width=width)
        del draw
        
    def clear(self,color=0):
        color = convertColor(color)
        if(self.mode!=None):
           color = color+color[-2:]
        image2 = Image2.new("RGBA",self.size,color)
        self.image.paste(image2,(0,0,self.size[0],self.size[1]))
        if(self.canvas):
            self.canvas.blit(self)
    def blit(self,img,target=(0,0),mask=None,source=(0,0)):
        pos=target 
        pos=(0-pos[0],0-pos[1])
        if(mask!=None):
            try:
                self.image.paste(img.image,(int(pos[0]),int(pos[1]),int(pos[0]+img.size[0]),int(pos[1]+img.size[1])),mask = mask.image)
            except Exception,ex:
                print(ex)
                self.image.paste(img.image, (pos[0], pos[1], pos[0] + img.size[0], pos[1] + img.size[1]))
        else:
           self.image.paste(img.image,(int(pos[0]),int(pos[1]),int(pos[0]+img.size[0]),int(pos[1]+img.size[1])))
        if(self.canvas):
            self.canvas.blit(self)
    def line(self,pos,bgcolor=0,width=0,outline=0):
        draw = ImageDraw.Draw(self.image)
        bgcolor = convertColor(bgcolor)
        draw.line((pos[0],pos[1],pos[2],pos[3]), fill=bgcolor,width=width)
        #myline = sysgraphics.Line(sysgraphics.Point(pos[0],pos[1]),sysgraphics.Point(pos[2],pos[3]))
        #myline.setFill(bgcolor)
        #myline.setWidth(width)
        #myline.draw(win)
        del draw
    def save(self,path):
        self.image = self.image.convert('RGB')
        self.image.save(path)
        
    def text(self,pos,text,fill = 0x0,font=('sence',15)):
        color = fill
        #print(pos,text,color,font)
        draw = ImageDraw.Draw(self.image)
        color = convertColor(color)
        if(type(font) is str):
            font=(font,15)
        draw.text((pos[0],pos[1]-font[1]),text,fill=color,font = GetFont(color,font))
        if(self.canvas):
            self.canvas.blit(self)
         
    def polygon(self,pos,color=0x0,width=1,fill=0x0):
        draw = ImageDraw.Draw(self.image)
        ismask = 0
        if( len(str(fill))>7):
            ismask = 1
        fill = convertColor(fill)
        if(ismask):
            fill = fill+'bb'
        #print(fill)
        pos = list(pos)
        draw.polygon( pos , fill=fill)
        del draw
    def point(self,pos,color,width=1,fill=0x0):
        draw = ImageDraw.Draw(self.image)
        fill = convertColor(fill)
        pos = list(pos)
        draw.point( pos , fill=fill,width=width)
        del draw
    def arc(self,pos,pi1,pi2,color,width=1):
        draw = ImageDraw.Draw(self.image)
        color = convertColor(color)
        pos = list(pos)
        draw.arc( pos ,pi1,pi2, fill=color)
        del draw
    def pieslice(self,pos,pi1,pi2,color,width=1):
        draw = ImageDraw.Draw(self.image)
        color = convertColor(color)
        pos = list(pos)
        draw.pieslice( pos ,pi1,pi2, fill=color)
        del draw
    def ellipse(self,pos,color=0x0,fill=0x0):
        draw = ImageDraw.Draw(self.image)
        color = convertColor(color)
        fill = convertColor(fill)
        draw.ellipse( pos ,color,fill)
        del draw
    def getpixel(self,(x,y)):
        color = self.image.getpixel((x,y))
        if(type(color)!=tuple):
            color = hex2rgb(color)
            print color
        return [color]
    def resize(self,size):
        self.image = self.image.resize(size)
        self.size = size
        return self
    def measure_text(self,title,font='dense'):
        fontsize = 18
        if(type(font) is tuple):
            fontsize= font[1]
        w,h = getTextFontWidth(title,fontsize)
        if(self.canvas):
            self.canvas.blit(self)
        return [[0,0,w,h],w]
   
    new=staticmethod(new)
    open=staticmethod(open)
def Draw(canvas):
    img = Image(canvas.size,canvas = canvas) 
    canvas.blit(img)
    return img
def screenshot():
    img = Image((240,320))
    return img
if(__name__=='__main__'):
   print(convertColor((3,280,280)))
