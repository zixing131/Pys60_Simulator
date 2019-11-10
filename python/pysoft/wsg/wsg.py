# -*- coding: utf-8 -*-
# terminal: s60
# name: wsg.py
# author: jijijilelele

__doc__ = "Windows Similar GUI"
__author = "jijijilelele"
__version__ = "1.0.2"

import appuifw
import graphics
import e32
import sys
import glib

FONT = appuifw.Text().font[0]
SCRX,SCRY = appuifw.app.layout(appuifw.EScreen)[0]
WM_PAINT = 0
WM_KEYDOWN = 3
WM_KEYREPEAT = 1
WM_KEYUP = 2
WM_MOUSEMOVE = 4
WM_LOCKCURSOR = 5
WM_REDRAW = 6
WM_WALKCHILDS = 7
WM_GETSTATE = 8
ARROW_LEFT = 14
ARROW_RIGHT = 15
ARROW_UP = 16
ARROW_DOWN = 17

cn = lambda x:unicode(x,"utf-8","ignore")

def Calc(text,font):
    temp = graphics.Image.new((1,1))
    tup = temp.measure_text(text,font)[0]
    return tup[2]-tup[0],tup[3]-tup[1]

class Window(object,):
    
    __module__ = __name__
    
    def __init__(self,parent=None,x=0,y=0,cx=SCRX,cy=SCRY,color=0xECE9D8):
        self.parent = parent
        self.left = x
        self.top = y
        self.width = cx
        self.height = cy
        self.color = color
        if self.__class__ == Window:
            self.__canvas = None
            self.__curimg = graphics.Image.open(r"c:\python\cursor.png")
            self.__curmsk = graphics.Image.new(self.__curimg.size,"L")
            self.__curmsk.load(r"c:\python\cursor_mask.png")
            self.__keydown = 0
            self.__keyboard = False
            self.__index = -1
            self.center = []
            self.bg = graphics.Image.new((SCRX,SCRY))
            self.bg.clear(0)
            self.image = graphics.Image.new((self.width,self.height))
            self.__oldscreen = appuifw.app.screen
            self.__oldbody = appuifw.app.body
            self.rect = [[0,0,self.width,self.height],[0,0,self.width,self.height]]
        else:
            self.image = self.parent.image
            if self.parent.__class__ != Window:
                self.left = self.parent.left+self.left
                self.top = self.parent.top+self.top
            self.rect = [[self.left,self.top,self.width,self.height],[self.left,self.top,self.width,self.height]]
        self.cw,self.ch = (12,19)
        self.cx = 0
        self.cy = 0
        self._change = True
        self._show = True
        self._lockcursor = False
        self.childs = []
        
    def focus(self,x,y):
        if x>=self.left and y>= self.top and x<self.left+self.width and y<self.top+self.height:
            return True
        return False
    
    def cross(self,child):
        x = child.left
        y = child.top
        cx = child.width
        cy = child.height
        m = self.rect[1][0]
        n = self.rect[1][1]
        cm = self.rect[1][2]
        cn = self.rect[1][3]
        if x>m-cx and x<m+cm and y>n-cy and y<n+cn:
            return True
        m = self.rect[0][0]
        n = self.rect[0][1]
        cm = self.rect[0][2]
        cn = self.rect[0][3]
        if x>m-cx and x<m+cm and y>n-cy and y<n+cn:
            return True
        return False
    
    def keyboard(self,bool):
        if self.__class__ != Window:
            return
        self.__keyboard = bool
        if self.state():
            self.cx,self.cy = self.center[self.__index]
            self.__move(0)
        
    def WalkChilds(wnd1,wnd2):
        for child in wnd2.childs:
            if not child._show:
                continue
            if child.__class__ == GroupButton:
                Window.WalkChilds(wnd1,child)
            elif child.__class__ == Panel:
                Window.WalkChilds(wnd1,child)
            elif child.__class__ == StaticText:
                pass
            else:
                wnd1.center.append((child.left+child.width/2,child.top+child.height/2))

    WalkChilds = staticmethod(WalkChilds)

    def run(self):
        if self.__class__ != Window:
            return
        Window.WalkChilds(self,self)
        self.__canvas = appuifw.Canvas(redraw_callback=self.redraw,event_callback=self.event)
        appuifw.app.screen = "full"
        appuifw.app.body = self.__canvas
        
    def exit(self):
        if self.__class__ != Window:
            return
        del self.__canvas
        appuifw.app.screen = self.__oldscreen
        appuifw.app.body = self.__oldbody
    
    def state(self):
        if self.__class__ == Window:
            if self.__canvas:
                return True
            else:
                return False
        else:
            return self.parent.WndProc(WM_GETSTATE,1,0)

    def redraw(self,v):
        self.WndProc(WM_PAINT,0,0)
    
    def event(self,key):
        type = key["type"]
        code = key["scancode"]
        if type == 3:
            self.WndProc(WM_KEYDOWN,code,0)
        elif type == 1:
            self.WndProc(WM_KEYREPEAT,code,0)
        else:
            self.WndProc(WM_KEYUP,code,0)
    
    def __move(self,wparam):
        if self.cx<0:self.cx=0
        elif self.cx>self.width-1:self.cx=self.width-1
        elif self.cy<0:self.cy=0
        elif self.cy>self.height-1:self.cy=self.height-1
        for child in self.childs:
            if child._show:
                child.WndProc(WM_MOUSEMOVE,wparam,(self.cx,self.cy))
        self.WndProc(WM_PAINT,0,0)
    
    def __left(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cx-=8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self.__move(ARROW_LEFT)
        e32.ao_yield()
        while self.__keydown:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx-=8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self.__move(ARROW_LEFT)
            e32.ao_yield()

    def __right(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cx+=8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self.__move(ARROW_RIGHT)
        e32.ao_yield()
        while self.__keydown:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx+=8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self.__move(ARROW_RIGHT)
            e32.ao_yield()

    def __up(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cy-=8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self.__move(ARROW_UP)
        e32.ao_yield()
        while self.__keydown:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cy-=8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self.__move(ARROW_UP)
            e32.ao_yield()

    def __down(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cy+=8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self.__move(ARROW_DOWN)
        e32.ao_yield()
        while self.__keydown:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cy+=8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self.__move(ARROW_DOWN)
            e32.ao_yield()
    
    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.clear(self.color)
                self._change = False
            for child in self.childs:
                if child._show and self.cross(child):
                    child.WndProc(WM_PAINT,0,0)
            self.bg.blit(self.image,target=(self.left,self.top))
            if not self.__keyboard and not self._lockcursor:
                self.bg.blit(self.__curimg,target=(self.left+self.cx,self.top+self.cy),mask=self.__curmsk)
            self.__canvas.blit(self.bg)
        elif message == WM_KEYDOWN:
            self.__keydown = 1
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYDOWN,wparam,0)
        elif message == WM_KEYREPEAT:
            if self._lockcursor == True:
                self.__move(wparam)
                return
            if wparam == ARROW_LEFT:
                if self.__keyboard and self.center:
                    self.__index-=1
                    if self.__index<0:
                        self.__index = len(self.center)-1
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx,self.cy = self.center[self.__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self.__move(wparam)
                else:
                    self.__left()
            elif wparam == ARROW_RIGHT:
                if self.__keyboard and self.center:
                    self.__index+=1
                    if self.__index>len(self.center)-1:
                        self.__index = 0
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx,self.cy = self.center[self.__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self.__move(wparam)
                else:
                    self.__right()
            elif wparam == ARROW_UP:
                if self.__keyboard and self.center:
                    self.__index-=1
                    if self.__index<0:
                        self.__index = len(self.center)-1
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx,self.cy = self.center[self.__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self.__move(wparam)
                else:
                    self.__up()
            elif wparam == ARROW_DOWN:
                if self.__keyboard and self.center:
                    self.__index+=1
                    if self.__index>len(self.center)-1:
                        self.__index = 0
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx,self.cy = self.center[self.__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self.__move(wparam)
                else:
                    self.__down()
        elif message == WM_KEYUP:
            self.__keydown = 0
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYUP,wparam,0)
        elif message == WM_LOCKCURSOR:
            self._lockcursor = lparam
        elif message == WM_REDRAW:
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.image.FillRect(self.rect[0][0],self.rect[0][1],self.rect[0][2],self.rect[0][3],wparam)
            self.WndProc(WM_PAINT,0,0)
        elif message == WM_WALKCHILDS:
            self.__index = 0
            self.center = []
            Window.WalkChilds(self,self)
        elif message == WM_GETSTATE:
            if self.__canvas:
                return True
            else:
                return False
    
    def __del__(self):
        pass

class PushButton(Window,):
    
    __module__ = __name__
    
    def __init__(self,parent,text,x,y,cx,cy,callback,color=0,size=16):
        Window.__init__(self,parent,x,y,cx,cy)
        self.color = self.parent.color
        self.__bcolor = 0xF4F4F0
        self.__fcolor = color
        self.__text = text
        self.__callback = callback
        self.__size = size
        self.__enter = False
        self.__down = False
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def SetText(self,txt):
        self.__text = txt
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetColor(self,color):
        self.__fcolor = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.__size = size
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()
        
    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.color)
                self.image.drawRoundRect(self.left,self.top,self.width,self.height,5,5,0x003C74)
                self.image.FillRoundRect(self.left+1,self.top+1,self.width-2,self.height-2,4,4,self.__bcolor)
                self.image.drawString((FONT,self.__size),self.__fcolor,self.left+self.width/2,self.top+self.height/2,self.__text,glib.HCENTER|glib.VCENTER)
                self._change = False
            if self.__enter and not self.__down:
                self.image.drawRoundRect(self.left+1,self.top+1,self.width-3,self.height-3,4,4,0xFCD279,2)
            else:
                self.image.drawRoundRect(self.left+1,self.top+1,self.width-3,self.height-3,4,4,self.__bcolor,2)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.__enter = True
            else:
                self.__enter = False
        elif message == WM_KEYDOWN:
            if self.__enter and wparam==167:
                self.__down = True
                self.__bcolor = 0xE3E2DA
                self._change = True
                self.parent.WndProc(WM_PAINT,1,0)
        elif message == WM_KEYUP:
            if self.__enter and wparam==167:
                self.__down = False
                self.__bcolor = 0xF4F4F0
                self._change = True
                self.parent.WndProc(WM_PAINT,1,0)
                self.__callback()
    
    def __del__(self):
        pass

class CheckButton(Window,):
    
    __module__ = __name__
    
    def __init__(self,parent,text,x,y,cx,cy,color=0,size=16):
        Window.__init__(self,parent,x,y,cx,cy)
        self.color = self.parent.color
        self.fcolor = color
        self.text = text
        self.size = size
        self.enter = False
        self.check = False
        self.x1 = 2
        self.y1 = (self.height-self.size)/2+2
        self.x2 = self.size+4
        self.y2 = self.y1-1
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def hide(self):
        self._show = False
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def SetText(self,txt):
        self.text = txt
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetColor(self,color):
        self.fcolor = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.size = size
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self.y1 = (self.height-self.size)/2+2
        self.y2 = self.y1-1
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.color)
                self.image.drawRect(self.left+self.x1,self.top+self.y1,self.size-2,self.size-2,0x185184)
                self.image.FillRect(self.left+self.x1+1,self.top+self.y1+1,self.size-4,self.size-4,0xEFEFEF)
                if self.check:
                    self.image.FillRect(self.left+self.x1+2,self.top+self.y1+2,self.size-6,self.size-6,0x29CD29)
                self.image.drawString((FONT,self.size),self.fcolor,self.left+self.x2,self.top+self.y2,self.text)
                self._change = False
            if self.enter:
                self.image.drawRect(self.left,self.top+self.y1-2,self.size+1,self.size+1,0xFCD279,2)
            else:
                self.image.drawRect(self.left,self.top+self.y1-2,self.size+1,self.size+1,self.color,2)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.enter = True
            else:
                self.enter = False
        elif message == WM_KEYUP:
            if self.enter and wparam==167:
                self.check = not self.check
                self._change = True
                self.parent.WndProc(WM_PAINT,1,0)
    
    def GetState(self):
        return self.check
    
    def SetState(self,bool):
        self.check = bool
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
    
    def __del__(self):
        pass

class RadioButton(CheckButton,):
    
    __module__ = __name__
    
    def __init__(self,parent,text,x,y,cx,cy,color=0,size=16):
        CheckButton.__init__(self,parent,text,x,y,cx,cy,color,size)

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.color)
                self.image.ellipse((self.left+self.x1,self.top+self.y1,self.left+self.x1+self.size-2,self.top+self.y1+self.size-2),0x185184)
                self.image.ellipse((self.left+self.x1+1,self.top+self.y1+1,self.left+self.x1+self.size-3,self.top+self.y1+self.size-3),0xEFEFEF,0xEFEFEF)
                if self.check:
                    self.image.ellipse((self.left+self.x1+2,self.top+self.y1+2,self.left+self.x1+self.size-4,self.top+self.y1+self.size-4),0x29CD29,0x29CD29)
                self.image.drawString((FONT,self.size),self.fcolor,self.left+self.x2,self.top+self.y2,self.text)
                self._change = False
            if self.enter:
                self.image.drawRect(self.left+self.x1-2,self.top+self.y1-2,self.size+1,self.size+1,0xFCD279,2)
            else:
                self.image.drawRect(self.left+self.x1-2,self.top+self.y1-2,self.size+1,self.size+1,self.color,2)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.enter = True
            else:
                self.enter = False
        elif message == WM_KEYUP:
            if self.enter and wparam==167:
                self.check = not self.check
                self._change = True
                self.parent.WndProc(WM_PAINT,1,0)

    def __del__(self):
        pass

class GroupButton(Window,):
    
    __module__ = __name__
    
    def __init__(self,parent,text,x,y,cx,cy,size=16):
        Window.__init__(self,parent,x,y,cx,cy)
        self.color = self.parent.color
        self.__fcolor = 0x0046D5
        self.__text = text
        self.__size = size
        self.__x1,self.__y1,self.__x2,self.__y2 = (0,0,0,0)
        self.__calc()
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        for child in self.childs:
            child.show()

    def hide(self):
        self._show = False
        for child in self.childs:
            child._show = False
            if child._lockcursor:
                child._lockcursor = False
                child.parent.WndProc(WM_LOCKCURSOR,1,False)
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def SetText(self,txt):
        self.__text = txt
        self.__calc()
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.__size = size
        self.__calc()
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetColor(self,color):
        self.__fcolor = color
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        pleft = self.left
        ptop = self.top
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()
        for child in self.childs:
            child.Move(child.left-pleft,child.top-ptop,child.width,child.height)
        
    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.color)
                self.image.drawRoundRect(self.left,self.top+8,self.width,self.height-8,8,8,0xD0D0BF)
                self.image.rectangle((self.left+self.__x1,self.top+self.__y1,self.left+self.__x2,self.top+self.__y2),self.color,self.color)
                self.image.drawString((FONT,self.__size),self.__fcolor,self.left+self.__x1,self.top+self.__y1,self.__text)
                self._change = False
            for child in self.childs:
                if child._show and self.cross(child):
                    child.WndProc(WM_PAINT,0,0)
            if wparam:
                self.parent.WndProc(WM_PAINT,1,0)
        elif message == WM_MOUSEMOVE:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx = lparam[0]
            self.cy = lparam[1]
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            for child in self.childs:
                child.WndProc(WM_MOUSEMOVE,wparam,(self.cx,self.cy))
        elif message == WM_KEYDOWN:
            for child in self.childs:
                child.WndProc(WM_KEYDOWN,wparam,0)
        elif message == WM_KEYUP:
            for child in self.childs:
                child.WndProc(WM_KEYUP,wparam,0)
        elif message == WM_LOCKCURSOR:
            self.parent.WndProc(WM_LOCKCURSOR,wparam,lparam)
        elif message == WM_REDRAW:
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.parent.WndProc(WM_REDRAW,wparam,lparam)
        elif message == WM_WALKCHILDS:
            self.parent.WndProc(message,wparam,lparam)
        elif message == WM_GETSTATE:
            return self.parent.WndProc(message,wparam,lparam)
    
    def __calc(self):
        w,h = Calc(self.__text,(FONT,self.__size))
        self.__x1 = 8
        self.__y1 = 0
        self.__x2 = self.__x1+w
        self.__y2 = self.__y1+h
    
    def __del__(self):
        pass

class Panel(Window,):
    
    __module__ = __name__
    
    def __init__(self,parent,x,y,cx,cy,color):
        Window.__init__(self,parent,x,y,cx,cy,color)
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        for child in self.childs:
            child.show()

    def hide(self):
        self._show = False
        for child in self.childs:
            child._show = False
            if child._lockcursor:
                child._lockcursor = False
                child.parent.WndProc(WM_LOCKCURSOR,1,False)
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def Move(self,x,y,cx,cy):
        pleft = self.left
        ptop = self.top
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()
        for child in self.childs:
            child.Move(child.left-pleft,child.top-ptop,child.width,child.height)

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.color)
                self._change = False
            for child in self.childs:
                if child._show and self.cross(child):
                    child.WndProc(WM_PAINT,0,0)
            if wparam:
                self.parent.WndProc(WM_PAINT,1,0)
        elif message == WM_MOUSEMOVE:
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx = lparam[0]
            self.cy = lparam[1]
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_MOUSEMOVE,wparam,(self.cx,self.cy))
        elif message == WM_KEYDOWN:
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYDOWN,wparam,0)
        elif message == WM_KEYUP:
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYUP,wparam,0)
        elif message == WM_LOCKCURSOR:
            self.parent.WndProc(WM_LOCKCURSOR,wparam,lparam)
        elif message == WM_REDRAW:
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.parent.WndProc(WM_REDRAW,wparam,lparam)
        elif message == WM_WALKCHILDS:
            self.parent.WndProc(message,wparam,lparam)
        elif message == WM_GETSTATE:
            return self.parent.WndProc(message,wparam,lparam)

    def __del__(self):
        pass

class SysLink(Window,):

    __module__ = __name__

    def __init__(self,parent,text,x,y,cx,cy,callback,color=0x1D53BF,size=16):
        Window.__init__(self,parent,x,y,cx,cy,color)
        self.__text = text
        self.__callback = callback
        self.__size = size
        self.__bcolor = self.parent.color
        self.__enter = False
        self.__m = Calc(text,(FONT,self.__size))
        self.__y = self.height/2+self.__m[1]/2
        self.__w = self.__m[0]
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def SetText(self,txt):
        self.__text = txt
        self.__m = Calc(self.__text,(FONT,self.__size))
        self.__y = self.height/2+self.__m[1]/2
        self.__w = self.__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetColor(self,color):
        self.color = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.__size = size
        self.__m = Calc(self.__text,(FONT,self.__size))
        self.__y = self.height/2+self.__m[1]/2
        self.__w = self.__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self.__y = self.height/2+self.__m[1]/2
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.__bcolor)
                self.image.drawString((FONT,self.__size),self.color,self.left+2,self.top+self.height/2,self.__text,glib.LEFT|glib.VCENTER)
                self._change = False
            if self.__enter:
                self.image.drawRect(self.left+1,self.top+1,self.width-2,self.height-2,0xFCD279,2)
            else:
                self.image.drawRect(self.left+1,self.top+1,self.width-2,self.height-2,self.__bcolor,2)
                self.image.line((self.left+2,self.top+self.__y,self.left+2+self.__w+1,self.top+self.__y),self.color)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.__enter = True
            else:
                self.__enter = False
        elif message == WM_KEYUP:
            if self.__enter and wparam==167:
                self.parent.WndProc(WM_PAINT,1,0)
                self.__callback()

    def __del__(self):
        pass

class StaticText(Window,):

    __module__ = __name__

    def __init__(self,parent,text,x,y,cx,cy,color=0,size=16):
        Window.__init__(self,parent,x,y,cx,cy,color)
        self.__text = text
        self.__size = size
        self.__bcolor = self.parent.color
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetText(self,txt):
        self.__text = txt
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetColor(self,color):
        self.color = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.__size = size
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.__bcolor)
                self.image.drawString((FONT,self.__size),self.color,self.left,self.top+self.height/2,self.__text,glib.LEFT|glib.VCENTER)
                self._change = False

    def __del__(self):
        pass

class StaticEdit(Window,):

    __module__ = __name__

    def __init__(self,parent,text,x,y,cx,cy,fcolor=0,size=16,bcolor=0xFFFFFF):
        Window.__init__(self,parent,x,y,cx,cy,fcolor)
        self.__text = text
        self.__size = size
        self.__bcolor = bcolor
        self.__wid,self.__hei = Calc(cn("测"),(FONT,self.__size))
        self.__pad = Calc(cn("自自"),(FONT,self.__size))[0]-Calc(cn("自"),(FONT,self.__size))[0]*2
        self.__cmapw = {u" ":self.__wid/2+1,u"\r":self.__wid+self.__pad,u"\n":self.__wid+self.__pad}
        self.__enter = False
        self.__len = len(self.__text)
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__lineh = self.__hei+2
        self.__linen = (self.height-6)/self.__lineh
        assert(self.__linen>0)
        self.__num = []
        self.__index = -1
        self.__maxh = 5+(self.__linen-1)*self.__lineh
        self.__w = self.width-6
        assert(self.__w>0)
        self.__h = self.__maxh-5
        self.__temp = graphics.Image.new((self.__w,self.__h))
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__num = []
        self.__index = -1
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def SetText(self,txt):
        self.__text = txt
        self._change = True
        self.__len = len(self.__text)
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__num = []
        self.__index = -1
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFont(self,size):
        self.__size = size
        self.__wid,self.__hei = Calc(cn("测"),(FONT,self.__size))
        self.__pad = Calc(cn("自自"),(FONT,self.__size))[0]-Calc(cn("自"),(FONT,self.__size))[0]*2
        self.__cmapw = {u" ":self.__wid/2+1,u"\r":self.__wid+self.__pad,u"\n":self.__wid+self.__pad}
        self._change = True
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__lineh = self.__hei+2
        self.__linen = (self.height-6)/self.__lineh
        assert(self.__linen>0)
        self.__num = []
        self.__index = -1
        self.__maxh = 5+(self.__linen-1)*self.__lineh
        self.__w = self.width-6
        assert(self.__w>0)
        self.__h = self.__maxh-5
        self.__temp = graphics.Image.new((self.__w,self.__h))
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetFontColor(self,color):
        self.color = color
        self._change = True
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__num = []
        self.__index = -1
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def SetBkColor(self,color):
        self.__bcolor = color
        self._change = True
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__num = []
        self.__index = -1
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        self._change = True
        self.__beg = 0
        self.__end = 0
        self.__scroll = False
        self.__linen = (self.height-6)/self.__lineh
        assert(self.__linen>0)
        self.__num = []
        self.__index = -1
        self.__maxh = 5+(self.__linen-1)*self.__lineh
        self.__w = self.width-6
        assert(self.__w>0)
        self.__h = self.__maxh-5
        self.__temp = graphics.Image.new((self.__w,self.__h))
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left,self.top,self.width,self.height,self.__bcolor)
                self.drawText()
                self._change = False
            if self.__enter:
                self.image.drawRect(self.left,self.top,self.width,self.height,0xFCD279)
            else:
                self.image.drawRect(self.left,self.top,self.width,self.height,0x7B9EBD)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.__enter = True
            else:
                self.__enter = False
            if wparam==ARROW_UP:
                if self._lockcursor and self.__scroll:
                    self.drawPrev()
                    self.parent.WndProc(WM_PAINT,1,0)
            elif wparam==ARROW_DOWN:
                if self._lockcursor and self.__scroll:
                    self.drawNext()
                    self.parent.WndProc(WM_PAINT,1,0)
        elif message == WM_KEYUP:
            if self.__enter:
                if wparam==167:
                    self._lockcursor = not self._lockcursor
                    self.parent.WndProc(WM_LOCKCURSOR,1,self._lockcursor)
                    self.parent.WndProc(WM_PAINT,1,0)

    def drawText(self):
        x,y,w = 5,5,0
        sls = u""
        oldend = 0
        for char in self.__text:
            w = self.__wid+self.__pad
            if ord(char)<0x4E00:
                if self.__cmapw.has_key(char):
                    w = self.__cmapw[char]
                else:
                    w = Calc(char,(FONT,self.__size))[0]+1
                    self.__cmapw[char] = w
            if char == u"\n":
                self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+y+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                sls = u""
                y+=self.__lineh
                x = 5
                self.__end += 1
                self.__num.append(self.__end-oldend)
                oldend = self.__end
                self.__index+=1
                if y > self.__maxh:
                    self.__scroll = True
                    return
            elif char == u"\r":
                self.__end+=1
                x+=w
            elif x+w>self.width-6-w:
                a = Calc(sls+char,(FONT,self.__size))[0]
                if 5+a<self.width-6-w:
                    sls+=char
                    x = 5+a
                    self.__end+=1
                    continue
                elif 5+a>self.width-6:
                    self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+y+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                    sls = char
                    y+=self.__lineh
                    x = 5+w
                    self.__num.append(self.__end-oldend)
                    oldend = self.__end
                    self.__index+=1
                    self.__end+=1
                    if y > self.__maxh:
                        self.__scroll = True
                        return
                else:
                    sls+=char
                    self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+y+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                    sls = u""
                    y+=self.__lineh
                    x = 5
                    self.__end+=1
                    self.__num.append(self.__end-oldend)
                    oldend = self.__end
                    self.__index+=1
                    if y > self.__maxh:
                        self.__scroll = True
                        return
            else:
                sls+=char
                x+=w
                self.__end+=1
        self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+y+self.__size,sls,glib.LEFT|glib.BOTTOM)
        self.__num.append(self.__end-oldend)
        self.__index+=1
    
    def drawPrev(self):
        if self.__beg == 0:
            return
        self.__temp.blit(self.image,source=((self.left+5,self.top+5),self.__w,self.__h))
        self.image.blit(self.__temp,target=(self.left+5,self.top+5+self.__lineh))
        self.image.FillRect(self.left+5,self.top+4,self.__w,self.__lineh+1,self.__bcolor)
        old = self.__beg
        self.__beg-=self.__num[self.__index+1-self.__linen-1]
        self.__end-=self.__num[self.__index]
        self.__index-=1
        s = self.__text[self.__beg:old]
        s = s.replace(u"\r",u"").replace(u"\n",u"")
        self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+5+self.__hei,s,glib.LEFT|glib.BOTTOM)
        
    def drawNext(self):
        if self.__end == self.__len:
            return
        self.__temp.blit(self.image,source=((self.left+5,self.top+5+self.__lineh),self.__w,self.__h))
        self.image.blit(self.__temp,target=(self.left+5,self.top+5))
        self.image.FillRect(self.left+5,self.top+self.__maxh,self.__w,self.__lineh,self.__bcolor)
        old = self.__end
        self.__beg+=self.__num[self.__index+1-self.__linen]
        if self.__index<len(self.__num)-1:
            self.__end+=self.__num[self.__index+1]
            self.__index+=1
            s = self.__text[old:self.__end]
            s=s.replace(u"\r",u"").replace(u"\n",u"")
            self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+self.__maxh+self.__hei,s,glib.LEFT|glib.BOTTOM)
            return
        sls = u""
        x = 5
        while self.__end<self.__len:
            char = self.__text[self.__end]
            w = self.__wid+self.__pad
            if ord(char)<0x4E00:
                if self.__cmapw.has_key(char):
                    w = self.__cmapw[char]
                else:
                    w = Calc(char,(FONT,self.__size))[0]+1
                    self.__cmapw[char] = w
            if char==u"\n":
                self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+self.__maxh+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                self.__end+=1
                break
            elif char==u"\r":
                self.__end+=1
                x+=w
            elif x+w>self.width-6-w:
                a = Calc(sls+char,(FONT,self.__size))[0]
                if 5+a<self.width-6-w:
                    sls+=char
                    x = 5+a
                    self.__end+=1
                    continue
                elif 5+a>self.width-6:
                    self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+self.__maxh+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                else:
                    sls+=char
                    self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+self.__maxh+self.__hei,sls,glib.LEFT|glib.BOTTOM)
                    self.__end+=1
                break
            else:
                sls+=char
                x+=w
                self.__end+=1
        if self.__end == self.__len:
            self.image.drawString((FONT,self.__size),self.color,self.left+5,self.top+self.__maxh+self.__hei,sls,glib.LEFT|glib.BOTTOM)
        self.__num.append(self.__end-old)
        self.__index+=1

    def __del__(self):
        pass

class Trackbar(Window,):

    __module__ = __name__

    FOLLOW = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    def __init__(self,parent,x,y,cx,cy,gap=1,minvalue=0,maxvalue=100,beg=0,bool=False,format=u"%d",style=FOLLOW,color=0,size=16):
        Window.__init__(self,parent,x,y,cx,cy,color)
        self.__bcolor = self.parent.color
        self.__cur = beg
        self.__bool = bool
        self.__format = format
        self.__style = style
        self.__size = size
        if maxvalue==minvalue:
            maxvalue+=100
        self.__minvalue = minvalue
        self.__maxvalue = maxvalue
        if beg<min(minvalue,maxvalue):
            self.__cur = minvalue
        elif beg>max(minvalue,maxvalue):
            self.__cur = maxvalue
        if self.width<10:
            self.width = 108
        if self.height<20:
            self.height = 20
        self.__dx = float(maxvalue-minvalue)/(self.width-9)
        self.__gap = gap
        if abs(self.__gap)>abs(maxvalue-minvalue):
            self.__gap = maxvalue-minvalue
        if maxvalue>minvalue and gap<=0:
            self.__gap = self.__dx
        elif maxvalue<minvalue and gap>=0:
            self.__gap = self.__dx
        self.__float = self.__gap/self.__dx
        self.__int = int(self.__float)
        if self.__int == 0:self.__int = 1
        self.__n = int((self.__cur-minvalue)/self.__gap)
        self.__num = (self.width-9)/self.__int
        self.__max = (self.__maxvalue-self.__minvalue)/self.__gap
        self.__enter = False
        self.__bg = graphics.Image.new((self.width,self.height))
        self.__txt = graphics.Image.new((self.width,self.height-20))
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))
        self.parent.WndProc(WM_WALKCHILDS,1,0)

    def Move(self,x,y,cx,cy):
        self.hide()
        self.left = self.parent.left+x
        self.top = self.parent.top+y
        self.width = cx
        self.height = cy
        if self.width<10:
            self.width = 108
        if self.height<20:
            self.height = 20
        self.__dx = float(self.__maxvalue-self.__minvalue)/(self.width-9)
        self.__float = self.__gap/self.__dx
        self.__int = int(self.__float)
        if self.__int == 0:self.__int = 1
        self.__num = (self.width-9)/self.__int
        self._change = True
        self.__bg = graphics.Image.new((self.width,self.height))
        self.__txt = graphics.Image.new((self.width,self.height-20))
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS,1,0)
        self.show()

    def WndProc(self,message,wparam,lparam):
        if message == WM_PAINT:
            if self._change:
                self.__bg.clear(self.__bcolor)
                self.__bg.drawRoundRect(1,6,self.width-2,4,2,2,0x9C9E9C)
                self.__bg.line((3,9,self.width-3,9),0xFFFFFF)
                for i in range(self.__num+1):
                    x = 4+i*self.__int
                    self.__bg.line((x,17,x,20),0xA5A294)
                self._change = False
            self.image.blit(self.__bg,target=(self.left,self.top))
            x = 4+int(round(self.__n*self.__float))/self.__int*self.__int
            self.image.line((self.left+x-2,self.top+2,self.left+x+3,self.top+2),0xB5C7CE)
            self.image.line((self.left+x-3,self.top+3,self.left+x-3,self.top+12),0xB5C7CE)
            self.image.line((self.left+x-2,self.top+3,self.left+x+3,self.top+3),0xFFC35A)
            self.image.line((self.left+x+3,self.top+3,self.left+x+3,self.top+12),0x738A94)
            self.image.FillRect(self.left+x-2,self.top+4,5,7,0xF7F7F7)
            self.image.line((self.left+x-3,self.top+11,self.left+x+1,self.top+15),0xB5C7CE)
            self.image.line((self.left+x-2,self.top+11,self.left+x+1,self.top+14),0xFFC35A)
            self.image.line((self.left+x+2,self.top+11,self.left+x-1,self.top+14),0xC68E29)
            self.image.line((self.left+x+3,self.top+11,self.left+x-1,self.top+15),0x738A94)
            if self.__bool:
                if self.__style == Trackbar.FOLLOW:
                    self.__txt.clear(self.__bcolor)
                    self.__txt.drawString((FONT,self.__size),self.color,x,2,self.__format%(self.__minvalue+self.__n*self.__gap),glib.HCENTER|glib.TOP)
                    self.image.blit(self.__txt,target=(self.left,self.top+20))
                elif self.__style == Trackbar.LEFT:
                    self.__txt.clear(self.__bcolor)
                    self.__txt.drawString((FONT,self.__size),self.color,0,2,self.__format%(self.__minvalue+self.__n*self.__gap),glib.LEFT|glib.TOP)
                    self.image.blit(self.__txt,target=(self.left,self.top+20))
                elif self.__style == Trackbar.center:
                    self.__txt.clear(self.__bcolor)
                    self.__txt.drawString((FONT,self.__size),self.color,self.width/2,2,self.__format%(self.__minvalue+self.__n*self.__gap),glib.HCENTER|glib.TOP)
                    self.image.blit(self.__txt,target=(self.left,self.top+20))
                elif self.__style == Trackbar.RIGHT:
                    self.__txt.clear(self.__bcolor)
                    self.__txt.drawString((FONT,self.__size),self.color,self.width-1,2,self.__format%(self.__minvalue+self.__n*self.__gap),glib.RIGHT|glib.TOP)
                    self.image.blit(self.__txt,target=(self.left,self.top+20))
            if self.__enter:
                self.image.drawRect(self.left,self.top,self.width,self.height,0xFCD279)
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx,self.cy):
                self.__enter = True
            else:
                self.__enter = False
            if wparam == ARROW_LEFT:
                if self._lockcursor:
                    self.__n -= 1
                    if self.__n<0:
                        self.__n = 0
                    self.WndProc(WM_PAINT,0,0)
            elif wparam == ARROW_RIGHT:
                if self._lockcursor:
                    self.__n += 1
                    if self.__n>self.__max:
                        self.__n = self.__max
                    self.WndProc(WM_PAINT,0,0)
        elif message == WM_KEYUP:
            if self.__enter:
                if wparam == 167:
                    self._lockcursor = not self._lockcursor
                    self.parent.WndProc(WM_LOCKCURSOR,1,self._lockcursor)
                    self.WndProc(WM_PAINT,0,0)

    def SetValue(self,value):
        if value<min(self.__minvalue,self.__maxvalue):
            value = self.__minvalue
        elif value>max(self.__minvalue,self.__maxvalue):
            value = self.__maxvalue
        self.__n = int((value-self.__minvalue)/self.__gap)
        if self.state():
            self.parent.WndProc(WM_REDRAW,self.parent.color,(self.left,self.top,self.width,self.height))

    def GetValue(self):
        return self.__minvalue+self.__n*self.__gap

    def __del__(self):
        pass

class Demo(object,):

    def __init__(self):
        self.wnd = Window()
        self.button1 = PushButton(self.wnd,cn("Move"),20,20,100,20,self.OnClicked,0,12)
        self.button2 = CheckButton(self.wnd,cn("检查"),20,60,16+4+16*2,20)
        self.button2.SetState(True)
        self.button3 = RadioButton(self.wnd,cn("互斥"),20,100,16+4+16*2,20)
        self.button4 = GroupButton(self.wnd,cn("组框"),20,140,100,40,12)
        self.button5 = PushButton(self.button4,cn("嵌套"),10,16,60,20,self.HelloWorld,0,12)
        self.link = SysLink(self.wnd,cn("链接"),20,200,2+16*2+2,2+16+2,self.HelloWorld)
        self.text = StaticText(self.wnd,cn("文字"),20,230,100,16)
        self.edit = StaticEdit(self.wnd,cn("静态编辑控件"),20,250,100,24,0xFFFFFF,12,0)
        self.trackbar = Trackbar(self.wnd,20,280,100,20+2+12,5,0,100,40,True,u"%.2f",Trackbar.FOLLOW,0x808080,12)
        self.ismoved = False
        self.oldhandler = appuifw.app.exit_key_handler
        self.lock = e32.Ao_lock()

    def HelloWorld(self):
        appuifw.note(cn("Hello World!"))

    def OnClicked(self): 
        if not self.ismoved:
            self.button1.Move(10,10,SCRX-20,30)
            self.button2.Move(10,50,SCRX-20,30)
            self.button3.Move(10,90,SCRX-20,30)
            self.button4.Move(10,130,SCRX-20,50)
            self.button5.Move(10,16,SCRX-40,20)
            self.link.Move(10,190,SCRX-20,30)
            self.text.Move(10,220,SCRX-20,16)
            self.edit.Move(10,240,SCRX-20,30)
            self.trackbar.Move(10,280,SCRX-20,40)
            self.ismoved = True
        else:
            appuifw.note(cn("已移动过！"))

    def Start(self):
        self.wnd.keyboard(1)
        self.wnd.run()
        appuifw.app.exit_key_handler = self.End
        self.lock.wait()

    def End(self):
        self.wnd.exit()
        appuifw.app.exit_key_handler = self.oldhandler
        self.lock.signal()

    def __del__(self):
        pass

if __name__ == "__main__":
    app = Demo()
    app.Start()
