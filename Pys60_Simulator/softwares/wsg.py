# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


__doc__ = 'Windows Similar GUI'
__author = 'jijijilelele'
__version__ = '1.0.2'

import graphics, appuifw, e32
import glib

path = u"../../python/pysoft/wsg\\"
#FONT = appuifw.Canvas().font[0]
FONT = 'dense'
SCRX, SCRY = appuifw.app.layout(appuifw.EScreen)[0]
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
cn = lambda x, : unicode(x, 'utf-8', 'ignore') 
def Calc(text, font):
    temp = graphics.Image.new((1, 1))
    tup = temp.measure_text(text, font)[0]
    return ((tup[2] - tup[0]), (tup[3] - tup[1]))




class Window(object, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent = None, x = 0, y = 0, cx = SCRX, cy = SCRY, color = 15526360):
        self.parent = parent
        self.left = x
        self.top = y
        self.width = cx
        self.height = cy
        self.color = color
        if self.__class__ == Window : 
            self._Window__canvas = None
            self._Window__curimg = graphics.Image.open(path + 'cursor.png')
            self._Window__curmsk = graphics.Image.new(self._Window__curimg.size, 'L')
            self._Window__curmsk.load(path + 'cursor_mask.png')
            self._Window__keydown = 0
            self._Window__keyboard = False
            self._Window__index = -1
            self.center = []
            self.bg = graphics.Image.new((SCRX, SCRY))
            self.bg.clear(0)
            self.image = graphics.Image.new((self.width, self.height))
            self._Window__oldscreen = appuifw.app.screen
            self._Window__oldbody = appuifw.app.body
            self.rect = [[0, 0, self.width, self.height], [0, 0, self.width, self.height]]
        else : 
            self.image = self.parent.image
            if self.parent.__class__ != Window : 
                self.left = self.parent.left + self.left
                self.top = self.parent.top + self.top
            self.rect = [[self.left, self.top, self.width, self.height], [self.left, self.top, self.width, self.height]]
        self.cw, self.ch = (12, 19)
        self.cx = 0
        self.cy = 0
        self._change = True
        self._show = True
        self._lockcursor = False
        self.childs = []




    def focus(self, x, y):
        if x >= self.left and y >= self.top and x < self.left + self.width and y < self.top + self.height : 
            return True
        return False




    def cross(self, child):
        x = child.left
        y = child.top
        cx = child.width
        cy = child.height
        m = self.rect[1][0]
        n = self.rect[1][1]
        cm = self.rect[1][2]
        cn = self.rect[1][3]
        if x > (m - cx) and x < m + cm and y > (n - cy) and y < n + cn : 
            return True
        m = self.rect[0][0]
        n = self.rect[0][1]
        cm = self.rect[0][2]
        cn = self.rect[0][3]
        if x > (m - cx) and x < m + cm and y > (n - cy) and y < n + cn : 
            return True
        return False




    def keyboard(self, bool):
        if self.__class__ != Window : 
            return None
        self._Window__keyboard = bool
        if self.state() : 
            self.cx, self.cy = self.center[self._Window__index]
            self._Window__move(0)




    def WalkChilds(wnd1, wnd2):
        for child in wnd2.childs:
            if  not (child._show) : 
                continue
            if child.__class__ == GroupButton : 
                Window.WalkChilds(wnd1, child)
            elif child.__class__ == Panel : 
                Window.WalkChilds(wnd1, child)
            elif child.__class__ == StaticText : 
                pass
            else : 
                wnd1.center.append((child.left + (child.width / 2), child.top + (child.height / 2)))




    WalkChilds = staticmethod(WalkChilds)
    def run(self):
        if self.__class__ != Window : 
            return None
        Window.WalkChilds(self, self)
        self._Window__canvas = appuifw.Canvas(redraw_callback = self.redraw, event_callback = self.event)
        appuifw.app.screen = 'full'
        appuifw.app.body = self._Window__canvas




    def exit(self):
        if self.__class__ != Window : 
            return None
        del self._Window__canvas
        appuifw.app.screen = self._Window__oldscreen
        appuifw.app.body = self._Window__oldbody




    def state(self):
        if self.__class__ == Window : 
            if self._Window__canvas : 
                return True
            else : 
                return False
            pass
        else : 
            return self.parent.WndProc(WM_GETSTATE, 1, 0)




    def redraw(self, v=0):
        self.WndProc(WM_PAINT, 0, 0)




    def event(self, key):
        type = key['type']
        code = key['scancode']
        #print(key)
        if type == 3 : 
            self.WndProc(WM_KEYDOWN, code, 0)
        elif type == 1 : 
            self.WndProc(WM_KEYREPEAT, code, 0)
        else : 
            self.WndProc(WM_KEYUP, code, 0)




    def _Window__move(self, wparam):
        if self.cx < 0 : 
            self.cx = 0
        elif self.cx > (self.width - 1) : 
            self.cx = (self.width - 1)
        elif self.cy < 0 : 
            self.cy = 0
        elif self.cy > (self.height - 1) : 
            self.cy = (self.height - 1)
        for child in self.childs:
            if child._show : 
                child.WndProc(WM_MOUSEMOVE, wparam, (self.cx, self.cy))
        self.WndProc(WM_PAINT, 0, 0)




    def _Window__left(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cx -= 8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self._Window__move(ARROW_LEFT)
        e32.ao_yield()
        while self._Window__keydown : 
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx -= 8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self._Window__move(ARROW_LEFT)
            e32.ao_yield()




    def _Window__right(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cx += 8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self._Window__move(ARROW_RIGHT)
        e32.ao_yield()
        while self._Window__keydown : 
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cx += 8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self._Window__move(ARROW_RIGHT)
            e32.ao_yield()




    def _Window__up(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cy -= 8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self._Window__move(ARROW_UP)
        e32.ao_yield()
        while self._Window__keydown : 
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cy -= 8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self._Window__move(ARROW_UP)
            e32.ao_yield()




    def _Window__down(self):
        self.rect[0][0] = self.cx
        self.rect[0][1] = self.cy
        self.rect[0][2] = self.cw
        self.rect[0][3] = self.ch
        self.cy += 8
        self.rect[1][0] = self.cx
        self.rect[1][1] = self.cy
        self.rect[1][2] = self.cw
        self.rect[1][3] = self.ch
        self._Window__move(ARROW_DOWN)
        e32.ao_yield()
        while self._Window__keydown : 
            self.rect[0][0] = self.cx
            self.rect[0][1] = self.cy
            self.rect[0][2] = self.cw
            self.rect[0][3] = self.ch
            self.cy += 8
            self.rect[1][0] = self.cx
            self.rect[1][1] = self.cy
            self.rect[1][2] = self.cw
            self.rect[1][3] = self.ch
            self._Window__move(ARROW_DOWN)
            e32.ao_yield()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT :
            if self._change : 
                self.image.clear(self.color)
                self._change = False
            for child in self.childs:
                if child._show and self.cross(child) : 
                    child.WndProc(WM_PAINT, 0, 0)
            self.bg.blit(self.image, target = (self.left, self.top))
            if  not ( not (self._Window__keyboard) and self._lockcursor) :
                self.bg.blit(self._Window__curimg, target = (0-(self.left + self.cx),0- (self.top + self.cy)), mask = self._Window__curmsk)
            self._Window__canvas.blit(self.bg)
        elif message == WM_KEYDOWN : 
            self._Window__keydown = 1
            for child in self.childs:
                if child._show : 
                    child.WndProc(WM_KEYDOWN, wparam, 0)
            pass
        elif message == WM_KEYREPEAT : 
            if self._lockcursor == True : 
                self._Window__move(wparam)
                return None
            if wparam == ARROW_LEFT : 
                if self._Window__keyboard and self.center : 
                    self._Window__index -= 1
                    if self._Window__index < 0 : 
                        self._Window__index = (len(self.center) - 1)
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx, self.cy = self.center[self._Window__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self._Window__move(wparam)
                else : 
                    self._Window__left()
                pass
            elif wparam == ARROW_RIGHT : 
                if self._Window__keyboard and self.center : 
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1) : 
                        self._Window__index = 0
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx, self.cy = self.center[self._Window__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self._Window__move(wparam)
                else : 
                    self._Window__right()
                pass
            elif wparam == ARROW_UP : 
                if self._Window__keyboard and self.center : 
                    self._Window__index -= 1
                    if self._Window__index < 0 : 
                        self._Window__index = (len(self.center) - 1)
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx, self.cy = self.center[self._Window__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self._Window__move(wparam)
                else : 
                    self._Window__up()
                pass
            elif wparam == ARROW_DOWN : 
                if self._Window__keyboard and self.center : 
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1) : 
                        self._Window__index = 0
                    self.rect[0][0] = self.cx
                    self.rect[0][1] = self.cy
                    self.rect[0][2] = self.cw
                    self.rect[0][3] = self.ch
                    self.cx, self.cy = self.center[self._Window__index]
                    self.rect[1][0] = self.cx
                    self.rect[1][1] = self.cy
                    self.rect[1][2] = self.cw
                    self.rect[1][3] = self.ch
                    self._Window__move(wparam)
                else : 
                    self._Window__down()
                pass
            pass
        elif message == WM_KEYUP : 
            self._Window__keydown = 0
            for child in self.childs:
                if child._show : 
                    child.WndProc(WM_KEYUP, wparam, 0)
            pass
        elif message == WM_LOCKCURSOR : 
            self._lockcursor = lparam
        elif message == WM_REDRAW : 
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.image.FillRect(self.rect[0][0], self.rect[0][1], self.rect[0][2], self.rect[0][3], wparam)
            self.WndProc(WM_PAINT, 0, 0)
        elif message == WM_WALKCHILDS : 
            self._Window__index = 0
            self.center = []
            Window.WalkChilds(self, self)
        elif message == WM_GETSTATE : 
            if self._Window__canvas : 
                return True
            else : 
                return False
            pass




    def __del__(self):
        pass






class PushButton(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, callback, color = 0, size = 16):
        Window.__init__(self, parent, x, y, cx, cy)
        self.color = self.parent.color
        self._PushButton__bcolor = 16053488
        self._PushButton__fcolor = color
        self._PushButton__text = text
        self._PushButton__callback = callback
        self._PushButton__size = size
        self._PushButton__enter = False
        self._PushButton__down = False
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def hide(self):
        self._show = False
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def SetText(self, txt):
        self._PushButton__text = txt
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetColor(self, color):
        self._PushButton__fcolor = color
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self._PushButton__size = size
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self.image.drawRoundRect(self.left, self.top, self.width, self.height, 5, 5, 15476)
                self.image.FillRoundRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), 4, 4, self._PushButton__bcolor)
                self.image.drawString((FONT, self._PushButton__size), self._PushButton__fcolor, self.left + (self.width / 2), self.top + (self.height / 2), self._PushButton__text, (
                            glib.HCENTER | glib.VCENTER))
                self._change = False
            if  not (self._PushButton__enter and self._PushButton__down) : 
                self.image.drawRoundRect((self.left + 1), (self.top + 1), (self.width - 3), (self.height - 3), 4, 4, 16568953, 2)
            else : 
                self.image.drawRoundRect((self.left + 1), (self.top + 1), (self.width - 3), (self.height - 3), 4, 4, self._PushButton__bcolor, 2)
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self._PushButton__enter = True
            else : 
                self._PushButton__enter = False
            pass
        elif message == WM_KEYDOWN : 
            if self._PushButton__enter and wparam == 167 : 
                self._PushButton__down = True
                self._PushButton__bcolor = 14934746
                self._change = True
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass
        elif message == WM_KEYUP : 
            if self._PushButton__enter and wparam == 167 : 
                self._PushButton__down = False
                self._PushButton__bcolor = 16053488
                self._change = True
                self.parent.WndProc(WM_PAINT, 1, 0)
                self._PushButton__callback()
            pass




    def __del__(self):
        pass






class CheckButton(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, color = 0, size = 16):
        Window.__init__(self, parent, x, y, cx, cy)
        self.color = self.parent.color
        self.fcolor = color
        self.text = text
        self.size = size
        self.enter = False
        self.check = False
        self.x1 = 2
        self.y1 = (((self.height - self.size) / 2) + 2)
        self.x2 = (self.size + 4)
        self.y2 = (self.y1 - 1)
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def hide(self):
        self._show = False
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def SetText(self, txt):
        self.text = txt
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetColor(self, color):
        self.fcolor = color
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self.size = size
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self.y1 = (((self.height - self.size) / 2) + 2)
        self.y2 = (self.y1 - 1)
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self.image.drawRect(self.left + self.x1, self.top + self.y1, (self.size - 2), (self.size - 2), 1593732)
                self.image.FillRect((self.left + self.x1 + 1), (self.top + self.y1 + 1), (self.size - 4), (self.size - 4), 15724527)
                if self.check : 
                    self.image.FillRect((self.left + self.x1 + 2), (self.top + self.y1 + 2), (self.size - 6), (self.size - 6), 2739497)
                self.image.drawString((FONT, self.size), self.fcolor, self.left + self.x2, self.top + self.y2, self.text)
                self._change = False
            if self.enter : 
                self.image.drawRect(self.left, (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), 16568953, 2)
            else : 
                self.image.drawRect(self.left, (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), self.color, 2)
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self.enter = True
            else : 
                self.enter = False
            pass
        elif message == WM_KEYUP : 
            if self.enter and wparam == 167 : 
                self.check =  not (self.check)
                self._change = True
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass




    def GetState(self):
        return self.check




    def SetState(self, bool):
        self.check = bool
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def __del__(self):
        pass






class RadioButton(CheckButton, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, color = 0, size = 16):
        CheckButton.__init__(self, parent, text, x, y, cx, cy, color, size)




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self.image.ellipse((self.left + self.x1, self.top + self.y1, (self.left + self.x1 + self.size - 2), (self.top + self.y1 + self.size - 2)), 1593732)
                self.image.ellipse(((self.left + self.x1 + 1), (self.top + self.y1 + 1), (self.left + self.x1 + self.size - 3), (self.top + self.y1 + self.size - 3)), 15724527, 15724527)
                if self.check : 
                    self.image.ellipse(((self.left + self.x1 + 2), (self.top + self.y1 + 2), (self.left + self.x1 + self.size - 4), (self.top + self.y1 + self.size - 4)), 2739497, 2739497)
                self.image.drawString((FONT, self.size), self.fcolor, self.left + self.x2, self.top + self.y2, self.text)
                self._change = False
            if self.enter : 
                self.image.drawRect((self.left + self.x1 - 2), (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), 16568953, 2)
            else : 
                self.image.drawRect((self.left + self.x1 - 2), (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), self.color, 2)
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self.enter = True
            else : 
                self.enter = False
            pass
        elif message == WM_KEYUP : 
            if self.enter and wparam == 167 : 
                self.check =  not (self.check)
                self._change = True
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass




    def __del__(self):
        pass






class GroupButton(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, size = 16):
        Window.__init__(self, parent, x, y, cx, cy)
        self.color = self.parent.color
        self._GroupButton__fcolor = 18133
        self._GroupButton__text = text
        self._GroupButton__size = size
        self._GroupButton__x1, self._GroupButton__y1, self._GroupButton__x2, self._GroupButton__y2 = (0, 0, 0, 0)
        self._GroupButton__calc()
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        for child in self.childs:
            child.show()




    def hide(self):
        self._show = False
        for child in self.childs:
            child._show = False
            if child._lockcursor : 
                child._lockcursor = False
                child.parent.WndProc(WM_LOCKCURSOR, 1, False)
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def SetText(self, txt):
        self._GroupButton__text = txt
        self._GroupButton__calc()
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self._GroupButton__size = size
        self._GroupButton__calc()
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetColor(self, color):
        self._GroupButton__fcolor = color
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        pleft = self.left
        ptop = self.top
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()
        for child in self.childs:
            child.Move((child.left - pleft), (child.top - ptop), child.width, child.height)




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self.image.drawRoundRect(self.left, (self.top + 8), self.width, (self.height - 8), 8, 8, 13684927)
                self.image.rectangle((self.left + self._GroupButton__x1, self.top + self._GroupButton__y1, self.left + self._GroupButton__x2, self.top + self._GroupButton__y2), self.color, self.color)
                self.image.drawString((FONT, self._GroupButton__size), self._GroupButton__fcolor, self.left + self._GroupButton__x1, self.top + self._GroupButton__y1, self._GroupButton__text)
                self._change = False
            for child in self.childs:
                if child._show and self.cross(child) : 
                    child.WndProc(WM_PAINT, 0, 0)
            if wparam : 
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass
        elif message == WM_MOUSEMOVE : 
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
                child.WndProc(WM_MOUSEMOVE, wparam, (self.cx, self.cy))
            pass
        elif message == WM_KEYDOWN : 
            for child in self.childs:
                child.WndProc(WM_KEYDOWN, wparam, 0)
            pass
        elif message == WM_KEYUP : 
            for child in self.childs:
                child.WndProc(WM_KEYUP, wparam, 0)
            pass
        elif message == WM_LOCKCURSOR : 
            self.parent.WndProc(WM_LOCKCURSOR, wparam, lparam)
        elif message == WM_REDRAW : 
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.parent.WndProc(WM_REDRAW, wparam, lparam)
        elif message == WM_WALKCHILDS : 
            self.parent.WndProc(message, wparam, lparam)
        elif message == WM_GETSTATE : 
            return self.parent.WndProc(message, wparam, lparam)




    def _GroupButton__calc(self):
        w, h = Calc(self._GroupButton__text, (FONT, self._GroupButton__size))
        self._GroupButton__x1 = 8
        self._GroupButton__y1 = 0
        self._GroupButton__x2 = self._GroupButton__x1 + w
        self._GroupButton__y2 = self._GroupButton__y1 + h




    def __del__(self):
        pass






class Panel(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, x, y, cx, cy, color):
        Window.__init__(self, parent, x, y, cx, cy, color)
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        self.rect[0][0] = self.left
        self.rect[0][1] = self.top
        self.rect[0][2] = self.width
        self.rect[0][3] = self.height
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        for child in self.childs:
            child.show()




    def hide(self):
        self._show = False
        for child in self.childs:
            child._show = False
            if child._lockcursor : 
                child._lockcursor = False
                child.parent.WndProc(WM_LOCKCURSOR, 1, False)
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def Move(self, x, y, cx, cy):
        pleft = self.left
        ptop = self.top
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()
        for child in self.childs:
            child.Move((child.left - pleft), (child.top - ptop), child.width, child.height)




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self._change = False
            
            for child in self.childs:
                
                if child._show and self.cross(child) : 
                    child.WndProc(WM_PAINT, 0, 0)
            if wparam : 
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass
        elif message == WM_MOUSEMOVE : 
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
                if child._show : 
                    child.WndProc(WM_MOUSEMOVE, wparam, (self.cx, self.cy))
            pass
        elif message == WM_KEYDOWN : 
            for child in self.childs:
                if child._show : 
                    child.WndProc(WM_KEYDOWN, wparam, 0)
            pass
        elif message == WM_KEYUP : 
            for child in self.childs:
                if child._show : 
                    child.WndProc(WM_KEYUP, wparam, 0)
            pass
        elif message == WM_LOCKCURSOR : 
            self.parent.WndProc(WM_LOCKCURSOR, wparam, lparam)
        elif message == WM_REDRAW : 
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.parent.WndProc(WM_REDRAW, wparam, lparam)
        elif message == WM_WALKCHILDS : 
            self.parent.WndProc(message, wparam, lparam)
        elif message == WM_GETSTATE : 
            return self.parent.WndProc(message, wparam, lparam)




    def __del__(self):
        pass






class SysLink(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, callback, color = 1921983, size = 16):
        Window.__init__(self, parent, x, y, cx, cy, color)
        self._SysLink__text = text
        self._SysLink__callback = callback
        self._SysLink__size = size
        self._SysLink__bcolor = self.parent.color
        self._SysLink__enter = False
        self._SysLink__m = Calc(text, (FONT, self._SysLink__size))
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._SysLink__w = self._SysLink__m[0]
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def hide(self):
        self._show = False
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def SetText(self, txt):
        self._SysLink__text = txt
        self._SysLink__m = Calc(self._SysLink__text, (FONT, self._SysLink__size))
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._SysLink__w = self._SysLink__m[0]
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetColor(self, color):
        self.color = color
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self._SysLink__size = size
        self._SysLink__m = Calc(self._SysLink__text, (FONT, self._SysLink__size))
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._SysLink__w = self._SysLink__m[0]
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT :
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self._SysLink__bcolor)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2), self.top + (self.height / 2), self._SysLink__text, (
                            glib.LEFT | glib.VCENTER))
                self._change = False
            if self._SysLink__enter : 
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), 16568953, 2)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2), self.top + (self.height / 2), self._SysLink__text, (
                            glib.LEFT | glib.VCENTER))
            else : 
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), self._SysLink__bcolor, 2)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2), self.top + (self.height / 2), self._SysLink__text, (
                            glib.LEFT | glib.VCENTER))
                self.image.line(((self.left + 2), self.top + self._SysLink__y, ((self.left + 2) + self._SysLink__w + 1), self.top + self._SysLink__y), self.color)
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self._SysLink__enter = True
            else : 
                self._SysLink__enter = False
            pass
        elif message == WM_KEYUP : 
            if self._SysLink__enter and wparam == 167 : 
                self.parent.WndProc(WM_PAINT, 1, 0)
                self._SysLink__callback()
            pass




    def __del__(self):
        pass






class StaticText(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, color = 0, size = 16):
        Window.__init__(self, parent, x, y, cx, cy, color)
        self._StaticText__text = text
        self._StaticText__size = size
        self._StaticText__bcolor = self.parent.color
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def hide(self):
        self._show = False
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetText(self, txt):
        self._StaticText__text = txt
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetColor(self, color):
        self.color = color
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self._StaticText__size = size
        self._change = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self._StaticText__bcolor)
                self.image.drawString((FONT, self._StaticText__size), self.color, self.left, self.top + (self.height / 2), self._StaticText__text, (
                            glib.LEFT | glib.VCENTER))
                self._change = False
            pass




    def __del__(self):
        pass






class StaticEdit(Window, ) :


    __module__ = __name__
    __module__ = __name__
    def __init__(self, parent, text, x, y, cx, cy, fcolor = 0, size = 16, bcolor = 16777215):
        Window.__init__(self, parent, x, y, cx, cy, fcolor)
        self._StaticEdit__text = text
        self._StaticEdit__size = size
        self._StaticEdit__bcolor = bcolor
        self._StaticEdit__wid, self._StaticEdit__hei = Calc(cn('测'), (FONT, self._StaticEdit__size))
        self._StaticEdit__pad = (Calc(cn('自自'), (FONT, self._StaticEdit__size))[0] - (Calc(cn('自'), (FONT, self._StaticEdit__size))[0] * 2))
        self._StaticEdit__cmapw = {u' ' : ((self._StaticEdit__wid / 2) + 1), u'\r' : self._StaticEdit__wid + self._StaticEdit__pad, u'\n' : self._StaticEdit__wid + self._StaticEdit__pad}
        self._StaticEdit__enter = False
        self._StaticEdit__len = len(self._StaticEdit__text)
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__lineh = (self._StaticEdit__hei + 2)
        self._StaticEdit__linen = ((self.height - 6) / self._StaticEdit__lineh)
        assert self._StaticEdit__linen > 0
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        self._StaticEdit__maxh = (5 + ((self._StaticEdit__linen - 1) * self._StaticEdit__lineh))
        self._StaticEdit__w = (self.width - 6)
        assert self._StaticEdit__w > 0
        self._StaticEdit__h = (self._StaticEdit__maxh - 5)
        self._StaticEdit__temp = graphics.Image.new((self._StaticEdit__w, self._StaticEdit__h))
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def hide(self):
        self._show = False
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def SetText(self, txt):
        self._StaticEdit__text = txt
        self._change = True
        self._StaticEdit__len = len(self._StaticEdit__text)
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFont(self, size):
        self._StaticEdit__size = size
        self._StaticEdit__wid, self._StaticEdit__hei = Calc(cn('测'), (FONT, self._StaticEdit__size))
        self._StaticEdit__pad = (Calc(cn('自自'), (FONT, self._StaticEdit__size))[0] - (Calc(cn('自'), (FONT, self._StaticEdit__size))[0] * 2))
        self._StaticEdit__cmapw = {u' ' : ((self._StaticEdit__wid / 2) + 1), u'\r' : self._StaticEdit__wid + self._StaticEdit__pad, u'\n' : self._StaticEdit__wid + self._StaticEdit__pad}
        self._change = True
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__lineh = (self._StaticEdit__hei + 2)
        self._StaticEdit__linen = ((self.height - 6) / self._StaticEdit__lineh)
        assert self._StaticEdit__linen > 0
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        self._StaticEdit__maxh = (5 + ((self._StaticEdit__linen - 1) * self._StaticEdit__lineh))
        self._StaticEdit__w = (self.width - 6)
        assert self._StaticEdit__w > 0
        self._StaticEdit__h = (self._StaticEdit__maxh - 5)
        self._StaticEdit__temp = graphics.Image.new((self._StaticEdit__w, self._StaticEdit__h))
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetFontColor(self, color):
        self.color = color
        self._change = True
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def SetBkColor(self, color):
        self._StaticEdit__bcolor = color
        self._change = True
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._change = True
        self._StaticEdit__beg = 0
        self._StaticEdit__end = 0
        self._StaticEdit__scroll = False
        self._StaticEdit__linen = ((self.height - 6) / self._StaticEdit__lineh)
        assert self._StaticEdit__linen > 0
        self._StaticEdit__num = []
        self._StaticEdit__index = -1
        self._StaticEdit__maxh = (5 + ((self._StaticEdit__linen - 1) * self._StaticEdit__lineh))
        self._StaticEdit__w = (self.width - 6)
        assert self._StaticEdit__w > 0
        self._StaticEdit__h = (self._StaticEdit__maxh - 5)
        self._StaticEdit__temp = graphics.Image.new((self._StaticEdit__w, self._StaticEdit__h))
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self.image.FillRect(self.left, self.top, self.width, self.height, self._StaticEdit__bcolor)
                self.drawText()
                self._change = False
            if self._StaticEdit__enter : 
                self.image.drawRect(self.left, self.top, self.width, self.height, 16568953)
                self.drawText()
            else : 
                self.image.drawRect(self.left, self.top, self.width, self.height, 8101565)
                self.drawText()
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self._StaticEdit__enter = True
            else : 
                self._StaticEdit__enter = False
            if wparam == ARROW_UP : 
                if self._lockcursor and self._StaticEdit__scroll : 
                    self.drawPrev()
                    self.parent.WndProc(WM_PAINT, 1, 0)
                pass
            elif wparam == ARROW_DOWN : 
                if self._lockcursor and self._StaticEdit__scroll : 
                    self.drawNext()
                    self.parent.WndProc(WM_PAINT, 1, 0)
                pass
            pass
        elif message == WM_KEYUP : 
            if self._StaticEdit__enter : 
                if wparam == 167 : 
                    self._lockcursor =  not (self._lockcursor)
                    self.parent.WndProc(WM_LOCKCURSOR, 1, self._lockcursor)
                    self.parent.WndProc(WM_PAINT, 1, 0)
                pass
            pass




    def drawText(self):
        x, y, w = (5, 5, 0)
        sls = u''
        oldend = 0
        for char in self._StaticEdit__text:
            w = self._StaticEdit__wid + self._StaticEdit__pad
            if ord(char) < 19968 : 
                if self._StaticEdit__cmapw.has_key(char) : 
                    w = self._StaticEdit__cmapw[char]
                else : 
                    w = (Calc(char, (FONT, self._StaticEdit__size))[0] + 1)
                    self._StaticEdit__cmapw[char] = w
                pass
            if char == u'\n' : 
                self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + y + self._StaticEdit__hei, sls, (
                            glib.LEFT | glib.BOTTOM))
                sls = u''
                y += self._StaticEdit__lineh
                x = 5
                self._StaticEdit__end += 1
                self._StaticEdit__num.append((self._StaticEdit__end - oldend))
                oldend = self._StaticEdit__end
                self._StaticEdit__index += 1
                if y > self._StaticEdit__maxh : 
                    self._StaticEdit__scroll = True
                    return None
                pass
            elif char == u'\r' : 
                self._StaticEdit__end += 1
                x += w
            elif x + w > ((self.width - 6) - w) : 
                a = Calc(sls + char, (FONT, self._StaticEdit__size))[0]
                if (5 + a) < ((self.width - 6) - w) : 
                    sls += char
                    x = (5 + a)
                    self._StaticEdit__end += 1
                    continue
                elif (5 + a) > (self.width - 6) : 
                    self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + y + self._StaticEdit__hei, sls, (
                                glib.LEFT | glib.BOTTOM))
                    sls = char
                    y += self._StaticEdit__lineh
                    x = (5 + w)
                    self._StaticEdit__num.append((self._StaticEdit__end - oldend))
                    oldend = self._StaticEdit__end
                    self._StaticEdit__index += 1
                    self._StaticEdit__end += 1
                    if y > self._StaticEdit__maxh : 
                        self._StaticEdit__scroll = True
                        return None
                    pass
                else : 
                    sls += char
                    self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + y + self._StaticEdit__hei, sls, (
                                glib.LEFT | glib.BOTTOM))
                    sls = u''
                    y += self._StaticEdit__lineh
                    x = 5
                    self._StaticEdit__end += 1
                    self._StaticEdit__num.append((self._StaticEdit__end - oldend))
                    oldend = self._StaticEdit__end
                    self._StaticEdit__index += 1
                    if y > self._StaticEdit__maxh : 
                        self._StaticEdit__scroll = True
                        return None
                    pass
                pass
            else : 
                sls += char
                x += w
                self._StaticEdit__end += 1
        self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + y + self._StaticEdit__size, sls, (
                    glib.LEFT | glib.BOTTOM))
        self._StaticEdit__num.append((self._StaticEdit__end - oldend))
        self._StaticEdit__index += 1




    def drawPrev(self):
        if self._StaticEdit__beg == 0 : 
            return None
        self._StaticEdit__temp.blit(self.image, source = (((self.left + 5), (self.top + 5)), self._StaticEdit__w, self._StaticEdit__h))
        self.image.blit(self._StaticEdit__temp, target = ((self.left + 5), (self.top + 5) + self._StaticEdit__lineh))
        self.image.FillRect((self.left + 5), (self.top + 4), self._StaticEdit__w, (self._StaticEdit__lineh + 1), self._StaticEdit__bcolor)
        old = self._StaticEdit__beg
        self._StaticEdit__beg -= self._StaticEdit__num[(((self._StaticEdit__index + 1) - self._StaticEdit__linen) - 1)]
        self._StaticEdit__end -= self._StaticEdit__num[self._StaticEdit__index]
        self._StaticEdit__index -= 1
        s = self._StaticEdit__text[self._StaticEdit__beg : old]
        s = s.replace(u'\r', u'').replace(u'\n', u'')
        self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), (self.top + 5) + self._StaticEdit__hei, s, (
                    glib.LEFT | glib.BOTTOM))




    def drawNext(self):
        if self._StaticEdit__end == self._StaticEdit__len : 
            return None
        self._StaticEdit__temp.blit(self.image, source = (((self.left + 5), (self.top + 5) + self._StaticEdit__lineh), self._StaticEdit__w, self._StaticEdit__h))
        self.image.blit(self._StaticEdit__temp, target = ((self.left + 5), (self.top + 5)))
        self.image.FillRect((self.left + 5), self.top + self._StaticEdit__maxh, self._StaticEdit__w, self._StaticEdit__lineh, self._StaticEdit__bcolor)
        old = self._StaticEdit__end
        self._StaticEdit__beg += self._StaticEdit__num[((self._StaticEdit__index + 1) - self._StaticEdit__linen)]
        if self._StaticEdit__index < (len(self._StaticEdit__num) - 1) : 
            self._StaticEdit__end += self._StaticEdit__num[(self._StaticEdit__index + 1)]
            self._StaticEdit__index += 1
            s = self._StaticEdit__text[old : self._StaticEdit__end]
            s = s.replace(u'\r', u'').replace(u'\n', u'')
            self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + self._StaticEdit__maxh + self._StaticEdit__hei, s, (
                        glib.LEFT | glib.BOTTOM))
            return None
        sls = u''
        x = 5
        while self._StaticEdit__end < self._StaticEdit__len : 
            char = self._StaticEdit__text[self._StaticEdit__end]
            w = self._StaticEdit__wid + self._StaticEdit__pad
            if ord(char) < 19968 : 
                if self._StaticEdit__cmapw.has_key(char) : 
                    w = self._StaticEdit__cmapw[char]
                else : 
                    w = (Calc(char, (FONT, self._StaticEdit__size))[0] + 1)
                    self._StaticEdit__cmapw[char] = w
                pass
            if char == u'\n' : 
                self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + self._StaticEdit__maxh + self._StaticEdit__hei, sls, (
                            glib.LEFT | glib.BOTTOM))
                self._StaticEdit__end += 1
                break
            elif char == u'\r' : 
                self._StaticEdit__end += 1
                x += w
            elif x + w > ((self.width - 6) - w) : 
                a = Calc(sls + char, (FONT, self._StaticEdit__size))[0]
                if (5 + a) < ((self.width - 6) - w) : 
                    sls += char
                    x = (5 + a)
                    self._StaticEdit__end += 1
                    continue
                elif (5 + a) > (self.width - 6) : 
                    self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + self._StaticEdit__maxh + self._StaticEdit__hei, sls, (
                                glib.LEFT | glib.BOTTOM))
                else : 
                    sls += char
                    self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + self._StaticEdit__maxh + self._StaticEdit__hei, sls, (
                                glib.LEFT | glib.BOTTOM))
                    self._StaticEdit__end += 1
                break
            else : 
                sls += char
                x += w
                self._StaticEdit__end += 1
        if self._StaticEdit__end == self._StaticEdit__len : 
            self.image.drawString((FONT, self._StaticEdit__size), self.color, (self.left + 5), self.top + self._StaticEdit__maxh + self._StaticEdit__hei, sls, (
                        glib.LEFT | glib.BOTTOM))
        self._StaticEdit__num.append((self._StaticEdit__end - old))
        self._StaticEdit__index += 1




    def __del__(self):
        pass






class Trackbar(Window, ) :


    __module__ = __name__
    __module__ = __name__
    FOLLOW = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    def __init__(self, parent, x, y, cx, cy, gap = 1, minvalue = 0, maxvalue = 100, beg = 0, bool = False, format = u'%d', style = FOLLOW, color = 0, size = 16):
        Window.__init__(self, parent, x, y, cx, cy, color)
        self._Trackbar__bcolor = self.parent.color
        self._Trackbar__cur = beg
        self._Trackbar__bool = bool
        self._Trackbar__format = format
        self._Trackbar__style = style
        self._Trackbar__size = size
        if maxvalue == minvalue : 
            maxvalue += 100
        self._Trackbar__minvalue = minvalue
        self._Trackbar__maxvalue = maxvalue
        if beg < min(minvalue, maxvalue) : 
            self._Trackbar__cur = minvalue
        elif beg > max(minvalue, maxvalue) : 
            self._Trackbar__cur = maxvalue
        if self.width < 10 : 
            self.width = 108
        if self.height < 20 : 
            self.height = 20
        self._Trackbar__dx = (float((maxvalue - minvalue)) / (self.width - 9))
        self._Trackbar__gap = gap
        if abs(self._Trackbar__gap) > abs((maxvalue - minvalue)) : 
            self._Trackbar__gap = (maxvalue - minvalue)
        if maxvalue > minvalue and gap <= 0 : 
            self._Trackbar__gap = self._Trackbar__dx
        elif maxvalue < minvalue and gap >= 0 : 
            self._Trackbar__gap = self._Trackbar__dx
        self._Trackbar__float = (self._Trackbar__gap / self._Trackbar__dx)
        self._Trackbar__int = int(self._Trackbar__float)
        if self._Trackbar__int == 0 : 
            self._Trackbar__int = 1
        self._Trackbar__n = int(((self._Trackbar__cur - minvalue) / self._Trackbar__gap))
        self._Trackbar__num = ((self.width - 9) / self._Trackbar__int)
        self._Trackbar__max = ((self._Trackbar__maxvalue - self._Trackbar__minvalue) / self._Trackbar__gap)
        self._Trackbar__enter = False
        self._Trackbar__bg = graphics.Image.new((self.width, self.height))
        self._Trackbar__txt = graphics.Image.new((self.width, (self.height - 20)))
        self.parent.childs.append(self)




    def show(self):
        self._change = True
        self._show = True
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def hide(self):
        self._show = False
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)




    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        if self.width < 10 : 
            self.width = 108
        if self.height < 20 : 
            self.height = 20
        self._Trackbar__dx = (float((self._Trackbar__maxvalue - self._Trackbar__minvalue)) / (self.width - 9))
        self._Trackbar__float = (self._Trackbar__gap / self._Trackbar__dx)
        self._Trackbar__int = int(self._Trackbar__float)
        if self._Trackbar__int == 0 : 
            self._Trackbar__int = 1
        self._Trackbar__num = ((self.width - 9) / self._Trackbar__int)
        self._change = True
        self._Trackbar__bg = graphics.Image.new((self.width, self.height))
        self._Trackbar__txt = graphics.Image.new((self.width, (self.height - 20)))
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()




    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT : 
            if self._change : 
                self._Trackbar__bg.clear(self._Trackbar__bcolor)
                self._Trackbar__bg.drawRoundRect(1, 6, (self.width - 2), 4, 2, 2, 10264220)
                self._Trackbar__bg.line((3, 9, (self.width - 3), 9), 16777215)
                for i in range((self._Trackbar__num + 1)):
                    x = (4 + (i * self._Trackbar__int))
                    self._Trackbar__bg.line((x, 17, x, 20), 10855060)
                self._change = False
            self.image.blit(self._Trackbar__bg, target = (self.left, self.top))
            x = (4 + ((int(round((self._Trackbar__n * self._Trackbar__float))) / self._Trackbar__int) * self._Trackbar__int))
            self.image.line(((self.left + x - 2), (self.top + 2), (self.left + x + 3), (self.top + 2)), 11913166)
            self.image.line(((self.left + x - 3), (self.top + 3), (self.left + x - 3), (self.top + 12)), 11913166)
            self.image.line(((self.left + x - 2), (self.top + 3), (self.left + x + 3), (self.top + 3)), 16761690)
            self.image.line(((self.left + x + 3), (self.top + 3), (self.left + x + 3), (self.top + 12)), 7572116)
            self.image.FillRect((self.left + x - 2), (self.top + 4), 5, 7, 16250871)
            self.image.line(((self.left + x - 3), (self.top + 11), (self.left + x + 1), (self.top + 15)), 11913166)
            self.image.line(((self.left + x - 2), (self.top + 11), (self.left + x + 1), (self.top + 14)), 16761690)
            self.image.line(((self.left + x + 2), (self.top + 11), (self.left + x - 1), (self.top + 14)), 13012521)
            self.image.line(((self.left + x + 3), (self.top + 11), (self.left + x - 1), (self.top + 15)), 7572116)
            if self._Trackbar__bool : 
                if self._Trackbar__style == Trackbar.FOLLOW : 
                    self._Trackbar__txt.clear(self._Trackbar__bcolor) 
                    self._Trackbar__txt.drawString((FONT, self._Trackbar__size), self.color, x, 2, (self._Trackbar__format % self._Trackbar__minvalue + str(self._Trackbar__n * self._Trackbar__gap)), (
                                glib.HCENTER | glib.TOP))
                    self.image.blit(self._Trackbar__txt, target = (self.left, (self.top + 20)))
                elif self._Trackbar__style == Trackbar.LEFT : 
                    self._Trackbar__txt.clear(self._Trackbar__bcolor)
                    self._Trackbar__txt.drawString((FONT, self._Trackbar__size), self.color, 0, 2, (self._Trackbar__format % self._Trackbar__minvalue + (self._Trackbar__n * self._Trackbar__gap)), (
                                glib.LEFT | glib.TOP))
                    self.image.blit(self._Trackbar__txt, target = (self.left, (self.top + 20)))
                elif self._Trackbar__style == Trackbar.center : 
                    self._Trackbar__txt.clear(self._Trackbar__bcolor)
                    self._Trackbar__txt.drawString((FONT, self._Trackbar__size), self.color, (self.width / 2), 2, (self._Trackbar__format % self._Trackbar__minvalue + (self._Trackbar__n * self._Trackbar__gap)), (
                                glib.HCENTER | glib.TOP))
                    self.image.blit(self._Trackbar__txt, target = (self.left, (self.top + 20)))
                elif self._Trackbar__style == Trackbar.RIGHT : 
                    self._Trackbar__txt.clear(self._Trackbar__bcolor)
                    self._Trackbar__txt.drawString((FONT, self._Trackbar__size), self.color, (self.width - 1), 2, (self._Trackbar__format % self._Trackbar__minvalue + (self._Trackbar__n * self._Trackbar__gap)), (
                                glib.RIGHT | glib.TOP))
                    self.image.blit(self._Trackbar__txt, target = (self.left, (self.top + 20)))
                pass
            if self._Trackbar__enter : 
                self.image.drawRect(self.left, self.top, self.width, self.height, 16568953)
            pass
        elif message == WM_MOUSEMOVE : 
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy) : 
                self._Trackbar__enter = True
            else : 
                self._Trackbar__enter = False
            if wparam == ARROW_LEFT : 
                if self._lockcursor : 
                    self._Trackbar__n -= 1
                    if self._Trackbar__n < 0 : 
                        self._Trackbar__n = 0
                    self.WndProc(WM_PAINT, 0, 0)
                pass
            elif wparam == ARROW_RIGHT : 
                if self._lockcursor : 
                    self._Trackbar__n += 1
                    if self._Trackbar__n > self._Trackbar__max : 
                        self._Trackbar__n = self._Trackbar__max
                    self.WndProc(WM_PAINT, 0, 0)
                pass
            pass
        elif message == WM_KEYUP : 
            if self._Trackbar__enter : 
                if wparam == 167 : 
                    self._lockcursor =  not (self._lockcursor)
                    self.parent.WndProc(WM_LOCKCURSOR, 1, self._lockcursor)
                    self.WndProc(WM_PAINT, 0, 0)
                pass
            pass




    def SetValue(self, value):
        if value < min(self._Trackbar__minvalue, self._Trackbar__maxvalue) : 
            value = self._Trackbar__minvalue
        elif value > max(self._Trackbar__minvalue, self._Trackbar__maxvalue) : 
            value = self._Trackbar__maxvalue
        self._Trackbar__n = int(((value - self._Trackbar__minvalue) / self._Trackbar__gap))
        if self.state() : 
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))




    def GetValue(self):
        return self._Trackbar__minvalue + (self._Trackbar__n * self._Trackbar__gap)




    def __del__(self):
        pass






class Demo(object, ) :


    __module__ = __name__
    def __init__(self):
        self.wnd = Window()
        self.button1 = PushButton(self.wnd, cn('Move'), 20, 20, 100, 20, self.OnClicked, 0, 12)
        self.button2 = CheckButton(self.wnd, cn('检查'), 20, 60, (16 + 4) + (16 * 2), 20)
        self.button2.SetState(True)
        self.button3 = RadioButton(self.wnd, cn('互斥'), 20, 100, (16 + 4) + (16 * 2), 20)
        self.button4 = GroupButton(self.wnd, cn('组框'), 20, 140, 100, 40, 12)
        self.button5 = PushButton(self.button4, cn('嵌套'), 10, 16, 60, 20, self.HelloWorld, 0, 12)
        self.link = SysLink(self.wnd, cn('链接'), 20, 200, (2 + (16 * 2) + 2), (2 + 16 + 2), self.HelloWorld)
        self.text = StaticText(self.wnd, cn('文字'), 20, 230, 100, 16)
        self.edit = StaticEdit(self.wnd, cn('静态编辑控件'), 20, 250, 100, 24, 16777215, 12, 0)
        self.trackbar = Trackbar(self.wnd, 20, 280, 100, (20 + 2 + 12), 5, 0, 100, 40, True, u'%.2f', Trackbar.FOLLOW, 8421504, 12)
        self.ismoved = False
        self.oldhandler = appuifw.app.exit_key_handler
        self.lock = e32.Ao_lock()




    def HelloWorld(self):
        appuifw.note(cn('Hello World!'))




    def OnClicked(self):
        if  not (self.ismoved) : 
            self.button1.Move(10, 10, (SCRX - 20), 30)
            self.button2.Move(10, 50, (SCRX - 20), 30)
            self.button3.Move(10, 90, (SCRX - 20), 30)
            self.button4.Move(10, 130, (SCRX - 20), 50)
            self.button5.Move(10, 16, (SCRX - 40), 20)
            self.link.Move(10, 190, (SCRX - 20), 30)
            self.text.Move(10, 220, (SCRX - 20), 16)
            self.edit.Move(10, 240, (SCRX - 20), 30)
            self.trackbar.Move(10, 280, (SCRX - 20), 40)
            self.ismoved = True
        else : 
            appuifw.note(cn('已移动过！'))




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




if __name__ == '__main__' : 
    app = Demo()
    app.Start()
