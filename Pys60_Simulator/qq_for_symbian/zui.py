# -*- coding: utf-8 -*-
import appuifw as ui
import graphics as ph
import akntextutils, txtfield
import e32
import glib

ui.app.screen = "full"
FONT = ('dense', 18)
SCRX, SCRY = ui.app.layout(ui.EScreen)[0]
WM_PAINT = 0
WM_KEYDOWN = 3
WM_KEYREPEAT = 1
WM_KEYUP = 2
WM_FOCUSCHANGE = 3
WM_MOUSEMOVE = 4
WM_REDRAW = 6
WM_WALKCHILDS = 7
WM_GETSTATE = 8
ARROW_LEFT = 14
ARROW_RIGHT = 15
ARROW_UP = 16
ARROW_DOWN = 17

cn = lambda x,: unicode(x, 'utf-8', 'ignore')


def Calc(text, font):
    temp = ph.Image.new((1, 1))
    tup = temp.measure_text(text, font)[0]
    return ((tup[2] - tup[0]), (tup[3] - tup[1]))


class Window(object):
    __module__ = __name__
    __module__ = __name__

    def __init__(self, parent=None, x=0, y=0, cx=SCRX, cy=SCRY, isFocus=False, color=0x205E86):
        self.parent = parent
        self.left = x
        self.top = y
        self.width = cx
        self.height = cy
        self.color = color
        self.Focusable = True
        self.isFocus = isFocus
        if self.__class__ == Window:
            self._Window__canvas = None
            self._Window__keydown = 0
            self._Window__keyboard = True
            self._Window__index = -1
            self.center = []
            self.bg = ph.Image.new((SCRX, SCRY))
            self.bg.clear(0)
            self.image = ph.Image.new((self.width, self.height))
            self._Window__oldscreen = ui.app.screen
            self._Window__oldbody = ui.app.body
            self.rect = [[0, 0, self.width, self.height], [0, 0, self.width, self.height]]
        else:
            self.image = self.parent.image
            if self.parent.__class__ != Window:
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

    def setFocusable(self, b):
        self.Focusable = b

    def focus(self, x, y):
        if x >= self.left and y >= self.top and x < self.left + self.width and y < self.top + self.height:
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
        if x > (m - cx) and x < m + cm and y > (n - cy) and y < n + cn:
            return True
        m = self.rect[0][0]
        n = self.rect[0][1]
        cm = self.rect[0][2]
        cn = self.rect[0][3]
        if x > (m - cx) and x < m + cm and y > (n - cy) and y < n + cn:
            return True
        return False

    def WalkChilds(wnd1, wnd2):
        for child in wnd2.childs:
            if not (child._show) or child.Focusable == False:
                continue
            # if child.__class__ == GroupButton:
            #    Window.WalkChilds(wnd1, child)
            elif child.__class__ == Panel:
                Window.WalkChilds(wnd1, child)
            # elif child.__class__ == StaticText:
            #    pass
            else:
                wnd1.center.append((child.left + (child.width / 2), child.top + (child.height / 2)))

    WalkChilds = staticmethod(WalkChilds)

    def run(self):
        if self.__class__ != Window:
            return None
        Window.WalkChilds(self, self)
        self._Window__canvas = ui.Canvas(redraw_callback=self.redraw, event_callback=self.event)
        ui.app.screen = 'full'
        ui.app.body = self._Window__canvas

    def exit(self):
        if self.__class__ != Window:
            return None
        del self._Window__canvas
        ui.app.screen = self._Window__oldscreen
        ui.app.body = self._Window__oldbody

    def state(self):
        if self.__class__ == Window:
            if self._Window__canvas:
                return True
            else:
                return False
            pass
        else:
            return self.parent.WndProc(WM_GETSTATE, 1, 0)

    def redraw(self, v):
        self.WndProc(WM_PAINT, 0, 0)

    def event(self, key):
        type = key['type']
        code = key['scancode']
        # print(key)
        if type == 3:
            self.WndProc(WM_KEYDOWN, code, 0)
        elif type == 1:
            self.WndProc(WM_KEYREPEAT, code, 0)
        else:
            self.WndProc(WM_KEYUP, code, 0)

    def _Window__move(self, wparam):

        if self.cx < 0:
            self.cx = 0
        elif self.cx > (self.width - 1):
            self.cx = (self.width - 1)
        elif self.cy < 0:
            self.cy = 0
        elif self.cy > (self.height - 1):
            self.cy = (self.height - 1)
        for child in self.childs:
            if child._show:
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
        while self._Window__keydown:
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
        while self._Window__keydown:
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
        while self._Window__keydown:
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
        while self._Window__keydown:
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
        if message == WM_PAINT:
            if self._change:
                self.image.clear(self.color)
                self._change = False
            for child in self.childs:
                if child._show and child.isFocus:
                    child.WndProc(WM_PAINT, 0, 0)
                else:
                    child.WndProc(WM_PAINT, 0, 0)
            self.bg.blit(self.image, target=(self.left, self.top))
            self._Window__canvas.blit(self.bg)
        elif message == WM_KEYDOWN:
            self._Window__keydown = 1
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYDOWN, wparam, 0)
            pass
        elif message == WM_KEYREPEAT:

            for child in self.childs:
                if (type(child) is Textbox and child._Textbox__editing == True):
                    return

            if self._lockcursor == True:
                self._Window__move(wparam)
                return None
            if wparam == ARROW_LEFT:
                if self._Window__keyboard and self.center:
                    self._Window__index -= 1
                    if self._Window__index < 0:
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
                else:
                    self._Window__left()
                pass
            elif wparam == ARROW_RIGHT:
                if self._Window__keyboard and self.center:
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1):
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
                else:
                    self._Window__right()
                pass
            elif wparam == ARROW_UP:
                if self._Window__keyboard and self.center:
                    self._Window__index -= 1
                    if self._Window__index < 0:
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
                else:
                    self._Window__up()
                pass
            elif wparam == ARROW_DOWN:
                if self._Window__keyboard and self.center:
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1):
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
                else:
                    self._Window__down()
                pass
            pass
        elif message == WM_KEYUP:
            self._Window__keydown = 0
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYUP, wparam, 0)
            for child in self.childs:
                if (type(child) is Textbox and child._Textbox__editing == True):
                    return
            pass
            if wparam == ARROW_LEFT:
                if self._Window__keyboard and self.center:
                    self._Window__index -= 1
                    if self._Window__index < 0:
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
                else:
                    self._Window__left()
                pass
            elif wparam == ARROW_RIGHT:
                if self._Window__keyboard and self.center:
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1):
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
                else:
                    self._Window__right()
                pass
            elif wparam == ARROW_UP:
                if self._Window__keyboard and self.center:
                    self._Window__index -= 1
                    if self._Window__index < 0:
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
                else:
                    self._Window__up()
                pass
            elif wparam == ARROW_DOWN:
                if self._Window__keyboard and self.center:
                    self._Window__index += 1
                    if self._Window__index > (len(self.center) - 1):
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
                else:
                    self._Window__down()
                pass
            pass
        elif message == WM_REDRAW:
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.image.FillRect(self.rect[0][0], self.rect[0][1], self.rect[0][2], self.rect[0][3], wparam)
            self.WndProc(WM_PAINT, 0, 0)
        elif message == WM_WALKCHILDS:
            self._Window__index = 0
            self.center = []
            Window.WalkChilds(self, self)
        elif message == WM_GETSTATE:
            if self._Window__canvas:
                return True
            else:
                return False
            pass

    def __del__(self):
        pass


class Panel(Window, ):
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
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        for child in self.childs:
            child.show()

    def hide(self):
        self._show = False
        for child in self.childs:
            child._show = False
            if child._lockcursor:
                child._lockcursor = False
        if self.state():
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
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self._change = False

            for child in self.childs:

                if child._show and self.cross(child):
                    child.WndProc(WM_PAINT, 0, 0)
            if wparam:
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass
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
                    child.WndProc(WM_MOUSEMOVE, wparam, (self.cx, self.cy))
            pass
        elif message == WM_KEYDOWN:
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYDOWN, wparam, 0)
            pass
        elif message == WM_KEYUP:
            for child in self.childs:
                if child._show:
                    child.WndProc(WM_KEYUP, wparam, 0)
            pass
        elif message == WM_REDRAW:
            self.rect[0][0] = lparam[0]
            self.rect[0][1] = lparam[1]
            self.rect[0][2] = lparam[2]
            self.rect[0][3] = lparam[3]
            self.parent.WndProc(WM_REDRAW, wparam, lparam)
        elif message == WM_WALKCHILDS:
            self.parent.WndProc(message, wparam, lparam)
        elif message == WM_GETSTATE:
            return self.parent.WndProc(message, wparam, lparam)

    def __del__(self):
        pass


class Textbox(Window, ):
    __module__ = __name__
    __module__ = __name__

    def __init__(self, parent, text, x, y, width, height, callback=None, isFocus=False, color=0xD6EFFE,
                 selectedColor=0xffffff, limit=0, size=16):
        Window.__init__(self, parent, x, y, width, height, False, color)
        self._Textbox__text = text
        self._Textbox__callback = callback
        self._Textbox__size = size
        self._Textbox__selectedColor = selectedColor
        self._Textbox__width = width
        self._Textbox__height = height
        self._Textbox__bcolor = self.parent.color
        self._Textbox__enter = False
        self._Textbox__editing = False
        self._Textbox__m = Calc(text, (FONT, self._Textbox__size))
        self._Textbox__y = (self.height / 2) + (self._Textbox__m[1] / 2)
        self._Textbox__w = self._Textbox__m[0]
        self.parent.childs.append(self)
        self.field = txtfield.New(
            (self.left, self.top, self.left + self.width, self.top + self.height),
            cornertype=txtfield.ECorner1, txtlimit=limit)
        self.field.textstyle(u'', 140, 0x0, style=u'normal')
        self.field.bgcolor(self._Textbox__selectedColor)
        self.field.add(self._Textbox__text)
        self.field.select(0, len(self._Textbox__text))
        self.field.focus(0)
        self.field.visible(0)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def SetText(self, txt):
        self._Textbox__text = txt
        self._Textbox__m = Calc(self._Textbox__text, (FONT, self._Textbox__size))
        self._Textbox__y = (self.height / 2) + (self._Textbox__m[1] / 2)
        self._Textbox__w = self._Textbox__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetColor(self, color):
        self.color = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetFont(self, size):
        self._Textbox__size = size
        self._Textbox__m = Calc(self._Textbox__text, (FONT, self._Textbox__size))
        self._Textbox__y = (self.height / 2) + (self._Textbox__m[1] / 2)
        self._Textbox__w = self._Textbox__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._Textbox__y = (self.height / 2) + (self._Textbox__m[1] / 2)
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()

    def getText(self):
        return self._Textbox__text

    def setText(self, t):
        self._Textbox__text = t

    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT:
            self._Textbox__text = self.field.get()
            if self._change:
                self.image.FillRect(self.left, self.top, self.width, self.height, self._Textbox__bcolor)
                self.image.drawString((FONT, self._Textbox__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Textbox__text, (glib.LEFT | glib.VCENTER))
                self._change = False
            if self._Textbox__enter:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), 16568953, 2)
                self.image.drawString((FONT, self._Textbox__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Textbox__text, (glib.LEFT | glib.VCENTER))
                if (self._Textbox__editing):
                    self.field.focus(1)
                    self.field.visible(1)
                else:
                    self.field.focus(0)
                    self.field.visible(0)
            else:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2),
                                    self._Textbox__bcolor, 2)
                self.image.drawString((FONT, self._Textbox__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Textbox__text, (glib.LEFT | glib.VCENTER))
                self.field.focus(0)
                self.field.visible(0)

            pass
        elif message == WM_MOUSEMOVE:
            if (self._Textbox__editing == True):
                return
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy):
                self._Textbox__enter = True
            else:
                self._Textbox__enter = False
            pass
        elif message == WM_KEYUP:
            if self._Textbox__enter and wparam == 167:
                if (self._Textbox__editing):
                    self._Textbox__editing = False
                else:
                    self._Textbox__editing = True
                self.parent.WndProc(WM_PAINT, 1, 0)
                if (self._Textbox__callback): self._Textbox__callback()
            pass

    def __del__(self):
        pass


class Label(Window, ):
    __module__ = __name__
    __module__ = __name__

    def __init__(self, parent, text, x, y, isFocus=False, color=0xA5D5F3, size=16):
        pos1 = Calc(text, FONT)
        cx, cy = pos1
        Window.__init__(self, parent, x, y, cx, cy, False, color)
        self._Label__text = text
        self._Label__size = size
        self._Label__bcolor = self.parent.color
        self._Label__enter = False
        self._Label__m = Calc(text, (FONT, self._Label__size))
        self._Label__y = (self.height / 2) + (self._Label__m[1] / 2)
        self._Label__w = self._Label__m[0]
        self.Focusable = False
        self.parent.childs.append(self)

    def show(self):
        self._change = True
        self._show = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def SetText(self, txt):
        self._Label__text = txt
        self._Label__m = Calc(self._Label__text, (FONT, self._Label__size))
        self._Label__y = (self.height / 2) + (self._Label__m[1] / 2)
        self._Label__w = self._Label__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetColor(self, color):
        self.color = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetFont(self, size):
        self._Label__size = size
        self._Label__m = Calc(self._Label__text, (FONT, self._Label__size))
        self._Label__y = (self.height / 2) + (self._Label__m[1] / 2)
        self._Label__w = self._Label__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def Move(self, x, y, cx, cy):
        self.hide()
        self.left = self.parent.left + x
        self.top = self.parent.top + y
        self.width = cx
        self.height = cy
        self._Label__y = (self.height / 2) + (self._Label__m[1] / 2)
        self._change = True
        self._show = True
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        self.show()

    def WndProc(self, message, wparam, lparam):
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left, self.top, self.width, self.height, self._Label__bcolor)
                self.image.drawString((FONT, self._Label__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Label__text, (glib.LEFT | glib.VCENTER))
                self._change = False
            if self._Label__enter:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), 16568953, 2)
                self.image.drawString((FONT, self._Label__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Label__text, (glib.LEFT | glib.VCENTER))
            else:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2),
                                    self._Label__bcolor, 2)
                self.image.drawString((FONT, self._Label__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._Label__text, (glib.LEFT | glib.VCENTER))
            pass
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy):
                self._Label__enter = True
            else:
                self._Label__enter = False
            pass
        elif message == WM_KEYUP:
            if self._Label__enter and wparam == 167:
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass

    def __del__(self):
        pass


class SysLink(Window, ):
    __module__ = __name__
    __module__ = __name__

    def __init__(self, parent, text, x, y, callback, isFocus=False, color=1921983, size=16):
        pos1 = Calc(text, FONT)
        cx, cy = pos1
        Window.__init__(self, parent, x, y, cx, cy, False, color)
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
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def hide(self):
        self._show = False
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def SetText(self, txt):
        self._SysLink__text = txt
        self._SysLink__m = Calc(self._SysLink__text, (FONT, self._SysLink__size))
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._SysLink__w = self._SysLink__m[0]
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetColor(self, color):
        self.color = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetFont(self, size):
        self._SysLink__size = size
        self._SysLink__m = Calc(self._SysLink__text, (FONT, self._SysLink__size))
        self._SysLink__y = (self.height / 2) + (self._SysLink__m[1] / 2)
        self._SysLink__w = self._SysLink__m[0]
        self._change = True
        if self.state():
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
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left, self.top, self.width, self.height, self._SysLink__bcolor)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._SysLink__text, (glib.LEFT | glib.VCENTER))
                self._change = False
            if self._SysLink__enter:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2), 16568953, 2)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._SysLink__text, (glib.LEFT | glib.VCENTER))
            else:
                self.image.drawRect((self.left + 1), (self.top + 1), (self.width - 2), (self.height - 2),
                                    self._SysLink__bcolor, 2)
                self.image.drawString((FONT, self._SysLink__size), self.color, (self.left + 2),
                                      self.top + (self.height / 2), self._SysLink__text, (glib.LEFT | glib.VCENTER))
                self.image.line(((self.left + 2), self.top + self._SysLink__y, ((self.left + 2) + self._SysLink__w + 1),
                                 self.top + self._SysLink__y), self.color)
            pass
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy):
                self._SysLink__enter = True
            else:
                self._SysLink__enter = False
            pass
        elif message == WM_KEYUP:
            if self._SysLink__enter and wparam == 167:
                self.parent.WndProc(WM_PAINT, 1, 0)
                self._SysLink__callback()
            pass

    def __del__(self):
        pass


class CheckButton(Window, ):
    __module__ = __name__
    __module__ = __name__

    def __init__(self, parent, text, x, y, cx, cy, color=0, size=16):
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
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def hide(self):
        self._show = False
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))
        self.parent.WndProc(WM_WALKCHILDS, 1, 0)

    def SetText(self, txt):
        self.text = txt
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetColor(self, color):
        self.fcolor = color
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def SetFont(self, size):
        self.size = size
        self._change = True
        if self.state():
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
        if message == WM_PAINT:
            if self._change:
                self.image.FillRect(self.left, self.top, self.width, self.height, self.color)
                self.image.drawRect(self.left + self.x1, self.top + self.y1, (self.size - 2), (self.size - 2), 1593732)
                self.image.FillRect((self.left + self.x1 + 1), (self.top + self.y1 + 1), (self.size - 4),
                                    (self.size - 4), 15724527)
                if self.check:
                    self.image.FillRect((self.left + self.x1 + 2), (self.top + self.y1 + 2), (self.size - 6),
                                        (self.size - 6), 2739497)
                self.image.drawString((FONT, self.size), self.fcolor, self.left + self.x2, self.top + self.y2,
                                      self.text)
                self._change = False
            if self.enter:
                self.image.drawRect(self.left, (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), 16568953, 2)
            else:
                self.image.drawRect(self.left, (self.top + self.y1 - 2), (self.size + 1), (self.size + 1), self.color,
                                    2)
            pass
        elif message == WM_MOUSEMOVE:
            self.cx = lparam[0]
            self.cy = lparam[1]
            if self.focus(self.cx, self.cy):
                self.enter = True
            else:
                self.enter = False
            pass
        elif message == WM_KEYUP:
            if self.enter and wparam == 167:
                self.check = not (self.check)
                self._change = True
                self.parent.WndProc(WM_PAINT, 1, 0)
            pass

    def GetState(self):
        return self.check

    def SetState(self, bool):
        self.check = bool
        self._change = True
        if self.state():
            self.parent.WndProc(WM_REDRAW, self.parent.color, (self.left, self.top, self.width, self.height))

    def __del__(self):
        pass


class Demo(object, ):
    __module__ = __name__

    def __init__(self):
        self.wnd = Window()
        self.link1 = SysLink(self.wnd, cn('链接1'), 20, 100, self.HelloWorld)
        self.link2 = SysLink(self.wnd, cn('链接2'), 20, 200, self.HelloWorld)
        self.label = Label(self.wnd, cn('Label'), 20, 220, self.HelloWorld)
        self.checkbutton = CheckButton(self.wnd, cn('检查'), 20, 60, (16 + 4) + (16 * 2), 20)
        # self.link.SetColor(1921983)
        self.ismoved = False
        self.oldhandler = ui.app.exit_key_handler
        self.lock = e32.Ao_lock()

    def HelloWorld(self):
        ui.note(cn('Hello World!'))

    def OnClicked(self):
        ui.note(cn('Hello World!'))

    def Start(self):
        self.wnd.run()
        ui.app.exit_key_handler = self.End
        self.lock.wait()

    def End(self):
        self.wnd.exit()
        ui.app.exit_key_handler = self.oldhandler
        self.lock.signal()

    def __del__(self):
        pass


if __name__ == '__main__':
    app = Demo()
    app.Start()
