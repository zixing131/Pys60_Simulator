# -*- coding: utf-8 -*-
import time
import xml
import xml.sax
from xml.dom.minidom import parse
import xml.dom.minidom

import appuifw
import graphics
import e32
import os
import neteasemusicapi as api
import qrcode

class ScreenType:
    main=1
    login=2

def cn(x):
    return x.decode('utf8')

img=None
FONT = 'normal'
def get_text_size(text, font=None):
    global img
    if img is None:
        img = graphics.Image.new((0,0))
    wh=img.measure_text(text, (FONT,font))[0]
    #print(wh)
    return [wh[2],0-wh[1]]


#UI元素
class UIElement(object):
    def __init__(self):
        self.Screensize = appuifw.app.layout(appuifw.EScreen)[0]
        self.Width, self.Height = self.Screensize
        self.Left = 0
        self.Top = 0
        self.Props = [] #属性
        #以下是基础属性
        self.Props.append('Background') #背景色
        self.Props.append('Foreground') #前景色

        self.Props.append('Width') #宽度
        self.Props.append('Height') #高度
        self.Props.append('Left') #左边
        self.Props.append('Top') #顶边
        self.Props.append('Enabled')  # 是否启用
        self.Props.append('Visibility')  # 是否可见
        self.img=None

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        if(key == 'Width' or key == 'Height'):
            self.reNewImage()

    def reNewImage(self):
        try:
            self.img = graphics.Image.new((self.Width, self.Height))
        except:
            pass

    def onDraw(self,g):
        if(hasattr(self,'Visibility')):
            vis = getattr(self,"Visibility")
            if(vis!='Visible'):
                return

        if(self.img==None):
            self.reNewImage()
        for prop in self.Props:
            if(hasattr(self,prop)):
                propdata = getattr(self,prop)
                if(propdata):
                    if(prop=='Background'):
                        self.img.clear(propdata)

        for children in self.Childrens:
            children.onDraw(self.img)
        if(hasattr(self,'Background')):
            g.blit(self.img,target=(self.Left,self.Top))

    def loadNodeAttrs(self,nownode,childnode):
        # print(childnode.attributes.items())
        for attrdata in childnode.attributes.items():
            attrname = attrdata[0]
            attrprop = attrdata[1]
            if (attrname in self.Props):
                try:
                    # 强制转换int
                    attrprop = int(attrprop)
                except:
                    pass
                setattr(nownode, attrname, attrprop)
            else:
                try:
                    # 强制转换int
                    attrprop = cn(attrprop)
                except:
                    pass
                setattr(nownode, attrname, attrprop)

        self.Childrens.append(nownode)

    def loadChildrens(self,childrendata):
        self.Childrens = []
        if(not childrendata):
            return
        for childnode in childrendata:
            if (childnode.nodeName == u'#text'):
                continue
            try:
                nownode = eval(childnode.nodeName + '()')
                nownode.loadChildrens(childnode.childNodes)
                nownode.parent = self
                self.loadNodeAttrs(nownode,childnode)
            except Exception,e:
                print(e)
                print('not supported element type:' + childnode.nodeName)

#基本面板
class Panel(UIElement):
    def __init__(self):
        UIElement.__init__(self)

    def onDraw(self, g):
        UIElement.onDraw(self,g)

#Grid面板
class Grid(Panel):
    def __init__(self):
        Panel.__init__(self)

    def onDraw(self,g):
        Panel.onDraw(self,g)

#Image图像
class Image(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self.Source = ''

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        if(key==u'Source'):
            if(self.Source!='' and os.path.exists(self.Source)):
                self.image = graphics.Image.open(self.Source)
                self.Width ,self.Height = self.image.size

    def onDraw(self,g):
        UIElement.onDraw(self,g)
        if(self.Source!=''):
            g.blit(self.image,target=(self.Width,self.Height))

#TextBlock
class TextBlock(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self.Width = 0
        self.Height = 0
        self.FontSize = 16
        self.Props.append('Text')
        self.Props.append('FontSize')

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        #print (key,value)
        if(key==u'Text'):
            self.Width,self.Height = get_text_size(value,self.FontSize)
            self.Height = self.Height+10

    def onDraw(self, g):
        UIElement.onDraw(self, g)
        if(hasattr(self,"Text")):
            text = self.Text
            try:
                text=cn(text)
            except:
                pass
            foreground=0x0
            if(hasattr(self,"Foreground")):
                foreground = self.Foreground
            g.text((self.Left,self.Top+self.Height),text,foreground,font=('dense',self.FontSize))


#窗口，理论上只允许一个窗口出现
class Window(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self.parent = None
        self.Screensize = appuifw.app.layout(appuifw.EScreen)[0]
        self.Width, self.Height = self.Screensize
        self.baseimg = graphics.Image.new(self.Screensize)
        self.Canvas = appuifw.Canvas(None, self.handle_redraw)
        appuifw.app.body = self.Canvas
        self.lastImg = None
        self.running = 1

    def loadLayout(self,layoutpath):
        self.Childrens = []
        self.layoutpath=layoutpath
        xaml= open(self.layoutpath,'r').read()
        self.xamldata = xml.dom.minidom.parseString(xaml)
        collection = self.xamldata.documentElement
        if(collection.nodeName!=u'Window'):
            print(u'Can not load xaml without Window Element')
            return
        self.loadNodeAttrs(self,collection)
        self.loadChildrens(collection.childNodes)

    def onDraw(self, g):
        UIElement.onDraw(self, g)

    def setFullScreen(self,isfull='full'):
        appuifw.app.screen = isfull

    def exit(self):
        self.running = 0

    def handle_redraw(self):
        g = self.baseimg
        self.onDraw(g)
        for children in self.Childrens:
            children.onDraw(g)
        self.Canvas.blit(self.baseimg)

    def show(self):
        self.lastImg = None
        while self.running:
            try:
                self.handle_redraw()
                e32.ao_yield()
            except Exception , e:
                print(e)
                pass

#主程序
class MyApp(Window):
    def __init__(self):
        Window.__init__(self)
        self.setFullScreen('full')
        self.loadLayout('myapp.xaml')


if __name__ == "__main__":
    app = MyApp()
    app.show()
