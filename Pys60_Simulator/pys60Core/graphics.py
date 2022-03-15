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

#from appuifw import app as _app
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
        p = os.path.split(os.path.realpath(__file__))[0]+'\\fonts\\S60SC.ttf'
        if (os.path.exists(p)):
            myfnt = ImageFont.truetype(p, int(font[1]))
        elif (os.path.exists("fonts\\S60SC.ttf")):
            myfnt = ImageFont.truetype("..\\fonts\\S60SC.ttf", int(font[1]))
        elif(os.path.exists("fonts/S60SC.ttf")):
            myfnt = ImageFont.truetype("fonts\\S60SC.ttf",int(font[1]))
        elif (os.path.exists("../pys60Core/fonts/S60SC.ttf")):
            myfnt = ImageFont.truetype("../pys60Core/fonts/S60SC.ttf", int(font[1]))

        elif(os.path.exists("Pys60_Simulator\\fonts\\S60SC.ttf")):
            myfnt = ImageFont.truetype("Pys60_Simulator\\fonts\\S60SC.ttf", int(font[1]))
    lastfont = font
    return myfnt

def getTextFontWidth(text,size=18):
    im = Image2.new('RGB', (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    w, h = draw.textsize(text, font=GetFont(font=('dense',size)))
    return [w,h]

def convertColor(bgcolor):
    if(type(bgcolor) is tuple):
        bgcolor = RGB_to_Hex(bgcolor)
    elif(type(bgcolor) is int):
        bgcolor = hex2rgb(bgcolor)
        bgcolor = sysgraphics.color_rgb(bgcolor[0], bgcolor[1], bgcolor[2])
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

    #"coords", "start", "end", "outline", "fill",
    #"width", "pattern"
    def rectangle(self, coords ,outline=0x0, fill=-1, width=1,pattern = 0x0):
        draw = ImageDraw.Draw(self.image)
        if(fill==-1):
            outline = convertColor(outline)
            draw.rectangle((coords[0], coords[1], coords[2], coords[3]),outline=outline, width=width)
            del draw
            return
        fill = convertColor(fill)
        if(outline!=0):
            outline = convertColor(outline)
            draw.rectangle((coords[0], coords[1], coords[2], coords[3]), fill=fill, outline=outline, width=width)
        else:
            draw.rectangle((coords[0], coords[1], coords[2], coords[3]), fill=fill, width=width)
        del draw
        
    def clear(self,color=0):
        color = convertColor(color)
        if(self.mode!=None):
           color = color+color[-2:]
        image2 = Image2.new("RGBA",self.size,color)
        self.image.paste(image2,(0,0,self.size[0],self.size[1]))
        if(self.canvas):
            self.canvas.blit(self)
    def blit(self,img,source=None,target=None,mask=None,scale =False):

        if(source==None):
            source = (0,0,img.size[0],img.size[1])
        if(target == None):
            target = (0, 0, img.size[0], img.size[1])
        if(len(source)==2):
            source = (source[0],source[1],img.size[0],img.size[1])
        if (len(target) == 2):
            target = (target[0], target[1], img.size[0], img.size[1])
        #pos=(target[0]-source[0],target[1]-source[1])
        pos = (int(target[0] - source[0]), int(target[1] - source[1]))
        if(mask!=None):
            try:
                #self.image.paste(img.image, (pos[0], pos[1], pos[0] + source[2], pos[1] + source[3]),mask=mask.image)
                self.image.paste(img.image.crop((0, 0, (int)(source[2]), (int)(source[3]))), ((int)(pos[0]), (int)(pos[1]), (int)(pos[0] + source[2]), (int)(pos[1] + source[3])),mask=mask.image)
            except Exception,ex:
                print(ex)
                self.image.paste(img.image.crop((0, 0, (int)(source[2]), (int)(source[3]))),
                                 ((int)(pos[0]), (int)(pos[1]), (int)(pos[0] + source[2]), (int)(pos[1] + source[3])))

                # self.image.paste(img.image.crop(
                #     ((int)(pos[0]), (int)(pos[1]), (int)(pos[0] + source[2]), (int)(pos[1] + source[3]))),
                #      ((int)(pos[0]), (int)(pos[1]), (int)(pos[0] + source[2]), (int)(pos[1] + source[3])))

                #self.image.paste(img.image, (pos[0], pos[1], pos[0] +source[2], pos[1] + source[3]))
        else:
            try:
                #self.image.paste(img.image, (pos[0], pos[1], pos[0] + source[2], pos[1] + source[3]))
                self.image.paste(img.image.crop((0, 0, (int)(source[2]), (int)(source[3]))),
                                 ((int)(pos[0]), (int)(pos[1]), (int)(pos[0] + source[2]), (int)(pos[1] + source[3])))

            except Exception,ex:
                print("graphics 150",ex)
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
        
    def text(self,pos,text,fill = 0x0,font=('dense',15)):
        if(font==None):
            font = ('dense', 15)
        elif(len(font)>=2 and font[1]==None):
            font = ('dense', 15)
        color = fill
        #print(pos,text,color,font)
        draw = ImageDraw.Draw(self.image)
        color = convertColor(color)
        if(type(font) is str or type(font) is unicode):
            font=(font,15)
        else:
            try:
                font = (font[0],int(font[1]))
            except Exception,e:
                print font
        #text=text.encode('u8')
        draw.text((int(pos[0]),int(pos[1]-font[1])),text,fill=color,font = GetFont(color,font))
        if(self.canvas):
            self.canvas.blit(self)
         
    def polygon(self,pos,color=0x0,width=1,fill=0x0,outline = 0x0):
        draw = ImageDraw.Draw(self.image)
        ismask = 0
        if( len(str(fill))>7):
            ismask = 1
        fill = convertColor(fill)
        if(ismask):
            fill = fill+'bb'
        #print(fill)
        pos2=[]
        for i in pos:
            if(type(i) is tuple or type(i) is list):
                pos2 += list(i)
            else:
                pos2.append(i)
        pos2 = list(pos2)
        draw.polygon( pos2 , fill=fill)
        del draw
    def point(self,pos,color,width=1,fill=0x0):
        # draw = ImageDraw.Draw(self.image)
        # fill = convertColor(fill)
        # pos = list(pos)
        # draw.point( pos , fill=fill)
        # del draw
        self.ellipse((pos[0],pos[1],pos[0]+width,pos[1]+width),color,color)
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
    def measure_text(self,title,font='dense',maxwidth = -1,maxadvance=-1):
        if (maxwidth == -1):
            fontsize = 18
            if(type(font) is tuple or type(font) is list):
                if(font[1]==None):
                    fontsize=18
                else:
                    fontsize= font[1]

            w,h = getTextFontWidth(title,int(fontsize))
            if(self.canvas):
                self.canvas.blit(self)
            return ((0,0-h,w,0),w,len(title))
        else:
            fontsize = 18
            if (type(font) is tuple or type(font) is list):
                fontsize = font[1]
            w, h = getTextFontWidth(title, int(fontsize))
            if (self.canvas):
                self.canvas.blit(self)
            if (w <= maxwidth):
                w = maxwidth
                return ((0, 0-h, w,0), w, len(title))
            else:
                w,h = 0,0
                nowchars = ''
                for i in title:
                    nowchars+=i
                    w, h = getTextFontWidth(nowchars, int(fontsize))
                    if(w>=maxwidth):
                        nowchars= nowchars[:-1]
                        w, h = getTextFontWidth(nowchars, int(fontsize))
                        break
                return ((0, 0-h, w, 0), w, len(nowchars))

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
