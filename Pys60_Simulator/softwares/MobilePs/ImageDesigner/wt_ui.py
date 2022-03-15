# -*- coding: utf-8 -*-
import graphics
import appuifw
import key_codes
import sys
from sysinfo import display_pixels as display_pixels
from time import clock as clock
import sys
__version__ = 1.4
def Nullevent():
    return {'type' : None, 'keycode' : None, 'scancode' : None, 'modifiers' : None}




class Keyboard(object, ) :


    __module__ = __name__
    def __init__(self, onevent = lambda  : None ):
        self._keyboard_state = {}
        self._downs = {}
        self._onevent = onevent




    def handle_event(self, event):
        if event['type'] == appuifw.EEventKeyDown : 
            code = event['scancode']
            if  not (self.is_down(code)) : 
                self._downs[code] = (self._downs.get(code, 0) + 1)
            self._keyboard_state[code] = 1
        elif event['type'] == appuifw.EEventKeyUp : 
            self._keyboard_state[event['scancode']] = 0
        self._onevent()




    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, 0)




    def pressed(self, scancode):
        if self._downs.get(scancode, 0) : 
            self._downs[scancode] -= 1
            return True
        return False






class Tmessagebox(object, ) :


    __module__ = __name__
    def __init__(self,cc, buff, colors, fnt = None, mess = '', style = 'center'):
        x, y, w, h =cc
        self.coord = (x, y, x + w, y + h)
        self.buff = buff
        self.clrs = colors
        self.sz = [0, 0]
        self.fnt = None
        self.textw = 0
        self.texth = 0
        self.textcoord = [0, 0]
        self.size((w, h))
        self.font(fnt)
        self.style = style
        self.message(mess)
        self.boxstyle = 0




    def message(self, mess):
        self.mess = mess
        s = self.buff.measure_text(self.mess, font = self.fnt)
        self.textw = (s[0][2] - s[0][0])
        if self.style == 'center' : 
            self.textcoord[0] = (self.coord[0] + (self.sz[0] / 2) - (self.textw / 2))
            self.textcoord[1] = self.coord[1] + (self.sz[1] / 2) + (self.texth / 2)
        elif self.style == 'up' : 
            self.textcoord[0] = (self.coord[0] + (self.sz[0] / 2) - (self.textw / 2))
            self.textcoord[1] = self.coord[1] + ((self.texth * 3) / 2)




    def font(self, fnt = None):
        if fnt is not None : 
            self.fnt = fnt
            s = self.buff.measure_text(u'Tq', font = self.fnt)
            self.texth = (s[0][3] - s[0][1])
        return self.fnt




    def size(self, sz = None):
        if sz is not None : 
            if sz[0] is not None : 
                self.sz[0] = sz[0]
            if sz[1] is not None : 
                self.sz[1] = sz[1]
            pass
        return self.sz




    def draw(self, mess = None):
        if mess is not None : 
            self.message(mess)
        if self.boxstyle is 0 : 
            self.buff.rectangle(((self.coord[0] + 4), (self.coord[1] + 4), (self.coord[2] + 4), (self.coord[3] + 4)), outline = 0, fill = 0, width = 1)
            self.buff.rectangle(self.coord, outline = self.clrs[0], fill = self.clrs[1], width = 1)
        elif self.boxstyle is 1 : 
            softrect(self.buff, ((self.coord[0] + 4), (self.coord[1] + 4), (self.coord[2] + 4), (self.coord[3] + 4)), outline = 0, fill = 0, width = 1, corner = 3)
            softrect(self.buff, self.coord, outline = self.clrs[0], fill = self.clrs[1], width = 1, corner = 3)
        self.buff.text(self.textcoord, self.mess, fill = self.clrs[2], font = self.fnt)






class Tmessageform(object, ) :


    __module__ = __name__
    def __init__(self, coord, canv, colors, mess, fnt = None):
        if type(coord) == type('') : 
            self.pos = coord
            self.coord = None
        else : 
            self.pos = None
            self.coord = coord
        self.canv = canv
        self.clrs = colors
        self.sz = [0, 0]
        self.space = [10, 10]
        self.blspace = 1
        self.fnt = None
        self.textsize = 0
        self.rectcoord = [0, 0, 0, 0]
        self.textcoord = [0, 0]
        self.font(fnt)
        self.lsize = [0, 0]
        self.scroll = False
        self.scrollspd = 1
        self.message(mess, fnt)
        self.hdn = False
        self.img = None
        self.msk = None
        self.keybrd = Keyboard()
        self.cllbck = None
        self.ciclecount = 0
        self.messtimeout = None
        self.boxstyle = 0
        self.borderwidth = 1
        self.corner = 3
        self.hiden(False)




    def addimage(self, coord, img, msk):
        self.img = img
        self.msk = msk
        self.img_coord = coord




    def message(self, mess, font = None):
        if font is not None : 
            self.fnt = font
        self.mess = mess
        self.textcoord = [[0, 0] for t in mess]
        self.textsize = self.gettextsize(mess, self.fnt)
        scrsize = display_pixels()
        if self.textsize[0] > (scrsize[0] - (self.space[0] * 2)) : 
            self.textsize[0] = (scrsize[0] - (self.space[0] * 2))
        if self.pos == 'center' : 
            self.coord = [0, 0]
            self.coord[0] = ((scrsize[0] - self.textsize[0] + (self.space[0] * 2)) / 2)
            self.coord[1] = ((scrsize[1] - self.textsize[1] + (self.space[1] * 2)) / 2)
        self.rectcoord = (self.coord[0], self.coord[1], self.coord[0] + self.textsize[0] + (self.space[0] * 2), self.coord[1] + self.textsize[1] + (self.space[1] * 2))
        if (self.rectcoord[3] - self.rectcoord[1]) > scrsize[1] : 
            self.scroll = True
        self.lsize = self.getlinesize(mess[0], self.fnt)
        if self.scroll : 
            for t in xrange(len(mess)):
                self.textcoord[t][0] = self.coord[0] + self.space[0]
                self.textcoord[t][1] = self.coord[1] + self.space[1] + (self.lsize[1] * (t + 1)) + self.rectcoord[3]
            pass
        else : 
            for t in xrange(len(mess)):
                self.textcoord[t][0] = self.coord[0] + self.space[0]
                self.textcoord[t][1] = self.coord[1] + self.space[1] + (self.lsize[1] * (t + 1))
            pass




    def getlinesize(self, text, font):
        s = self.canv.measure_text(text, font = font)
        return ((s[0][2] - s[0][0]), (s[0][3] - s[0][1]) + self.blspace)




    def gettextsize(self, messar, font):
        width = 0
        height = (len(messar) * self.getlinesize(messar[0], font)[1])
        for t in xrange(len(messar)):
            size = self.getlinesize(messar[t], font)
            width = max(width, size[0])
        return [width, height]




    def font(self, fnt = None):
        if fnt is not None : 
            self.fnt = fnt
        return self.fnt




    def draw(self, mess = None):
        if  not (self.hdn) : 
            if self.messtimeout is not None : 
                if (clock() - self.counter) > self.messtimeout : 
                    self.hiden(True)
                pass
            if self.boxstyle is 0 : 
                self.canv.rectangle(((self.rectcoord[0] + 4), (self.rectcoord[1] + 4), (self.rectcoord[2] + 4), (self.rectcoord[3] + 4)), outline = 0, fill = 0, width = self.borderwidth)
                self.canv.rectangle(self.rectcoord, outline = self.clrs[0], fill = self.clrs[1], width = 1)
            elif self.boxstyle is 1 : 
                softrect(self.canv, ((self.rectcoord[0] + 4), (self.rectcoord[1] + 4), (self.rectcoord[2] + 4), (self.rectcoord[3] + 4)), outline = 0, fill = 0, width = self.borderwidth, corner = self.corner)
                softrect(self.canv, self.rectcoord, outline = self.clrs[0], fill = self.clrs[1], width = self.borderwidth, corner = self.corner)
            if self.img is not None : 
                self.canv.blit(self.img, target = (self.coord[0] + self.img_coord[0], self.coord[1] + self.img_coord[1]), mask = self.msk)
            for t in xrange(len(self.mess)):
                if self.scroll : 
                    self.textcoord[t][1] -= self.scrollspd
                self.canv.text(self.textcoord[t], self.mess[t], fill = self.clrs[2], font = self.fnt)
            if self.scroll : 
                if self.textcoord[-1][1] < 0 : 
                    self.ciclecount += 1
                    for t in xrange(len(self.mess)):
                        self.textcoord[t][1] = self.coord[1] + self.space[1] + (self.lsize[1] * (t + 1)) + self.rectcoord[3]
                    pass
                pass
            pass




    def setcallback(self, cl):
        self.cllbck = cl




    def control(self, evt):
        self.keybrd.handle_event(evt)
        if self.keybrd.pressed(key_codes.EScancodeSelect) or self.keybrd.pressed(key_codes.EScancodeLeftSoftkey) or self.keybrd.pressed(key_codes.EScancodeRightSoftkey) : 
            self.hdn = True
            if callable(self.cllbck) : 
                self.cllbck()
            pass




    def hiden(self, state = None):
        if state is not None : 
            self.hdn = state
            if self.messtimeout is not None : 
                if state is False : 
                    self.counter = clock()
                pass
            pass
        else : 
            return self.hdn






class Ticonlist(object, ) :


    __module__ = __name__
    def _joinicons(self, mode, items):
        self.img = graphics.Image.new([items[0].size[0], (items[0].size[1] * len(items))], mode)
        for t in xrange(len(items)):
            self.img.blit(items[t], target = (0, (items[0].size[1] * t)))




    def icon(self, t, im = None):
        if im is not None : 
            self.img.blit(im, target = (0, (self.sbw * t)))




    def __init__(self, x, y, itcnt, items = [], mode = 'RGB16'):
        self.x = x
        self.y = y
        self.cicled = True
        self.sp_l = 1
        self.sp_r = 1
        self.sp_u = 1
        self.sp_d = 1
        self.hdn = False
        self.sbcur = 0
        self.sbx = x
        self.sby = y
        self.sbw = items[0].size[0]
        if len(items) == 1 : 
            self.itcnt = itcnt
            self.sbh = items[0].size[0]
        else : 
            self.itcnt = itcnt
            self.sbh = items[0].size[1]
        self.event = ['item']
        self.sbcol = 0
        self.sbwidth = 2
        self.moving = False
        self.blckd = False
        self.movespd = 0
        self.clback = None
        self.movex = 0
        self.movey = 0
        self.count = len(items)
        self._joinicons(mode, items)
        self.offset = [0, 0]
        self.rsize = [(self.sbw - (self.sbwidth / 2)), (self.sbh - (self.sbwidth / 2))]
        self.callback_onchangeit = None




    def draw(self, c):
        if self.hdn != True : 
            self._move(self.movex, self.movey, self.movespd)
            c.blit(self.img, target = (self.x, self.y))
            if self.sbcur != -1 : 
                c.rectangle((self.sbx + self.offset[0], self.sby + self.offset[1], self.sbx + self.rsize[0], self.sby + self.rsize[1]), outline = self.sbcol, width = self.sbwidth)
            pass




    def nextitem(self):
        self.sbcur += 1
        if self.sbcur > (self.itcnt - 1) : 
            if self.cicled is True : 
                self.sbcur = 0
            else : 
                self.sbcur = (self.itcnt - 1)
            pass
        if callable(self.callback_onchangeit) : 
            self.callback_onchangeit()




    def previtem(self):
        self.sbcur -= 1
        if self.sbcur < 0 : 
            if self.cicled is True : 
                self.sbcur = (self.itcnt - 1)
            else : 
                self.sbcur = 0
            pass
        if callable(self.callback_onchangeit) : 
            self.callback_onchangeit()




    def control(self, evt):
        if self.blckd : 
            return None
        if evt['keycode'] == key_codes.EKeyDownArrow : 
            self.nextitem()
        elif evt['keycode'] == key_codes.EKeyUpArrow : 
            self.previtem()
        self.sby = (self.sbcur * self.sbh) + self.y




    def coord(self, crd = None):
        if crd is not None : 
            if crd[0] is not None : 
                self.x = crd[0]
            if crd[1] is not None : 
                self.y = crd[1]
            pass
        else : 
            return (self.x, self.y)




    def moveto(self, x, y, spd, callback = None):
        self.movex = x
        self.movey = y
        self.movespd = spd
        self.moving = True
        self.clback = callback




    def _move(self, x, y, spd):
        if self.moving is True : 
            value = (self.x - self.sbx)
            dy = (self.y - self.sby)
            if self.x < x : 
                self.x += spd
                if self.x >= x : 
                    self.x = x
                pass
            if self.y < y : 
                self.y += spd
                if self.y >= y : 
                    self.y = y
                pass
            if self.x > x : 
                self.x -= spd
                if self.x <= x : 
                    self.x = x
                pass
            if self.y > y : 
                self.y -= spd
                if self.y <= y : 
                    self.y = y
                pass
            self.sbx = (self.x - value)
            self.sby = (self.y - dy)
            if self.x == x and self.y == y : 
                self.moving = False
                if callable(self.clback) : 
                    self.clback()
                pass
            pass




    def curitem(self, cur = None):
        if cur is not None : 
            self.sbcur = cur
        return self.sbcur




    def rectcolor(self, color = None):
        if color is not None : 
            self.sbcol = color
        return self.sbcol




    def rectwidth(self, width = None):
        if width is not None : 
            self.sbwidth = width
        return self.sbwidth




    def rectoffset(self, offset = None):
        if offset is not None : 
            self.offset = offset
        return self.offset




    def rectsize(self, size = None):
        if size is not None : 
            self.rsize = size
        return self.rsize




    def hiden(self, hd = None):
        if hd is not None : 
            self.hdn = hd
            if self.hdn is True : 
                self.blckd = True
            else : 
                self.blckd = False
            pass
        return self.hdn




    def blocked(self, bl = None):
        if bl is not None : 
            self.blckd = bl
        return self.blckd




    def getsize(self):
        return self.img.size






class Ticongrid(Ticonlist, ) :


    __module__ = __name__
    grids = []
    def _joinicons(self):
        self.img = graphics.Image.new([self.items[0].size[0], (self.items[0].size[1] * self.count)])
        for t in xrange(self.count):
            self.img.blit(self.items[t], target = (0, (self.items[0].size[1] * t)))




    def icon(self, coord, im = None):
        if im is not None : 
            self.lst[coord[0]].icon(coord[1], im)




    def __init__(self, x, y, items = [], mode = 'RGB16'):
        Ticongrid.grids.append(self)
        self.x = x
        self.y = y
        self.items = items
        self.count = len(items)
        self.curcolm = 0
        self.cicled = True
        self.hdn = False
        self.blckd = False
        self.lst = []
        for t in xrange(self.count):
            l = Ticonlist(x + (self.items[t][0].size[0] * t), y, len(items[0]), self.items[t], mode)
            self.lst.append(l)
            if t != 0 : 
                self.lst[t].sbcur = -1
                self.lst[t].blocked(True)
        del self.items
        self.course = None
        self.spd = 0
        self.scancode = None
        self.cllbcks = (None, None)
        self.callback_onchangeit = None
        self.excludelist = []




    def draw(self, c):
        if self.hdn != True : 
            for t in self.lst:
                t.draw(c)
            pass




    def nextitem(self):
        c = self.lst[self.curcolm].curitem()
        self.lst[self.curcolm].blocked(True)
        self.lst[self.curcolm].curitem(-1)
        self.curcolm += 1
        if self.curcolm > (self.count - 1) : 
            if self.cicled : 
                self.curcolm = 0
                self.lst[self.curcolm].curitem(c)
                self.lst[self.curcolm].nextitem()
            else : 
                self.curcolm = (self.count - 1)
                self.lst[self.curcolm].curitem(c)
            pass
        else : 
            self.lst[self.curcolm].curitem(c)
        self.lst[self.curcolm].blocked(False)
        if callable(self.callback_onchangeit) : 
            self.callback_onchangeit()




    def previtem(self):
        c = self.lst[self.curcolm].curitem()
        self.lst[self.curcolm].blocked(True)
        self.lst[self.curcolm].curitem(-1)
        self.curcolm -= 1
        if self.curcolm < 0 : 
            if self.cicled : 
                self.curcolm = (self.count - 1)
                self.lst[self.curcolm].curitem(c)
                self.lst[self.curcolm].previtem()
            else : 
                self.curcolm = 0
                self.lst[self.curcolm].curitem(c)
            pass
        else : 
            self.lst[self.curcolm].curitem(c)
        self.lst[self.curcolm].blocked(False)
        if callable(self.callback_onchangeit) : 
            self.callback_onchangeit()




    def control(self, evt):
        if self.blckd : 
            return None
        if evt['type'] == appuifw.EEventKeyDown : 
            if evt['scancode'] == key_codes.EScancodeSelect : 
                if self.curitem() in self.excludelist : 
                    return False
                self.hideandblock()
                if callable(self.cllbcks[2]) : 
                    self.cllbcks[2]()
                return True
            elif evt['scancode'] == key_codes.EScancodeRightSoftkey : 
                self.hideandblock()
                return False
            elif evt['scancode'] == key_codes.EScancodeBackspace : 
                self.hideandblock()
                return False
            pass
        if evt['keycode'] == key_codes.EKeyRightArrow : 
            self.nextitem()
        elif evt['keycode'] == key_codes.EKeyLeftArrow : 
            self.previtem()
        for t in self.lst:
            t.control(evt)




    def moveto(self, x, y, spd, callback = None):
        for t in xrange(0, len(self.lst)):
            self.lst[t].moveto(x + (t * self.lst[t].sbw), y, spd, callback)




    def coord(self, crd = None):
        if crd is not None : 
            if crd[0] is not None : 
                self.x = crd[0]
            if crd[1] is not None : 
                self.y = crd[1]
            for t in xrange(0, len(self.lst)):
                self.lst[t].coord(crd)
            pass
        else : 
            return (self.lst[0].x, self.lst[0].y)




    def curitem(self, cur = None):
        if cur is not None : 
            for t in xrange(self.count):
                self.lst[t].sbcur = -1
                self.lst[t].blocked(True)
            self.curcolm = cur[0]
            self.lst[self.curcolm].curitem(cur[1])
        return [self.curcolm, self.lst[self.curcolm].curitem()]




    def curindex(self):
        return (self.lst[0].count * self.curcolm) + self.lst[self.curcolm].curitem()




    def rectcolor(self, color = None):
        if color is not None : 
            for t in xrange(len(self.lst)):
                self.lst[t].rectcolor(color)
            pass
        return self.lst[0].rectcolor()




    def rectwidth(self, width = None):
        if width is not None : 
            for t in xrange(len(self.lst)):
                self.lst[t].rectwidth(width)
            pass
        return self.lst[0].rectwidth()




    def hiden(self, hd = None):
        if hd is not None : 
            self.hdn = hd
            if self.hdn is True : 
                self.blocked(True)
            else : 
                self.blocked(False)
            pass
        return self.hdn




    def blocked(self, bl = None):
        if bl is not None : 
            self.blckd = bl
            self.lst[self.curcolm].blocked(bl)
        return self.blckd




    def setcourse(self, x, y, x1, y1, spd, scancode):
        self.course = (x, y, x1, y1)
        self.spd = spd
        self.scancode = scancode




    def setslidespeed(self, spd):
        self.spd = spd




    def callback(self, onshow, onhide, press = None):
        self.cllbcks = (onshow, onhide, press)




    def setcallback_onchangeitem(self, hor, vert):
        self.callback_onchangeit = hor
        for l in self.lst:
            l.callback_onchangeit = vert




    def setexcludeitem(self, it):
        self.excludelist.append(it)




    def hideandblock(self):
        self.moveto(self.course[2], self.course[3], self.spd, lambda  :  self.hiden(True) )
        if callable(self.cllbcks[1]) : 
            self.cllbcks[1]()




    def unlockandshow(self):
        self.hiden(False)
        self.moveto(self.course[0], self.course[1], self.spd)
        if callable(self.cllbcks[0]) : 
            self.cllbcks[0]()




    def switch(self):
        if self.hiden() : 
            for t in Ticongrid.grids:
                if t is not self : 
                    t.hideandblock()
            self.unlockandshow()
        elif  not (self.hiden()) : 
            self.hideandblock()




    def showcontrol(evt):
        for grid in Ticongrid.grids:
            grid.control(evt)




    showcontrol = staticmethod(showcontrol)
    def isallhiden():
        for grid in Ticongrid.grids:
            if  not (grid.hiden()) : 
                return False
        return True




    isallhiden = staticmethod(isallhiden)
    def hideall():
        for grid in Ticongrid.grids:
            grid.hideandblock()




    hideall = staticmethod(hideall)
    def rectoffset(self, offset = None):
        if offset is not None : 
            for t in xrange(len(self.lst)):
                self.lst[t].rectoffset(offset)
            pass
        return self.lst[0].rectoffset()




    def rectsize(self, size = None):
        if size is not None : 
            for t in xrange(len(self.lst)):
                self.lst[t].rectsize(size)
            pass
        return self.lst[0].rectsize()




    def getsize(self):
        return ((len(self.lst) * self.lst[0].getsize()[0]), (len(self.lst) * self.lst[0].getsize()[1]))






def softrect(canv,cc, outline = 0, fill = 16777215, width = 1, corner = 1):
    x, y, x1, y1 =cc
    canv.polygon(((x + corner, y), (x, y + corner), (x, (y1 - corner)), (x + corner, y1), ((x1 - corner), y1), (x1, (y1 - corner)), (x1, y + corner), ((x1 - corner), y)), outline = outline, fill = fill, width = width)




def octrect(canv,cc, outline = 0, fill = 16777215, width = 1):
    x, y, x1, y1 =cc
    d = ((y1 - y) / 2)
    canv.polygon(((x + d, y), (x, y + d), (x + d, y1), ((x1 - d), y1), (x1, y + d), ((x1 - d), y)), outline = outline, fill = fill, width = width)




class Tbar(object, ) :


    __module__ = __name__
    def __init__(self, x, y, x1, y1,dd, scrv, canv, vert = True, kind = 0):
        minv, maxv =dd
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.dcor = 0
        self.curval = 0
        self.perc = 0
        self.minv = minv
        self.maxv = maxv
        self.scrv = scrv
        self.vert = vert
        self.canv = canv
        self.kind = kind
        self.linew = 1
        self.space = 1
        self.corner = 1
        self.vert = vert
        self._scrollwupdt(True)




    def size(self, size, updt = True):
        if size[0] is not None : 
            self.x = size[0]
        if size[1] is not None : 
            self.y = size[1]
        if size[2] is not None : 
            self.x1 = size[2]
        if size[3] is not None : 
            self.y1 = size[3]
        self._scrollwupdt(updt)




    def _scrollwupdt(self, updt = True):
        if self.vert is True : 
            self.barw = ((self.y1 - self.y) - (self.linew * 2))
            if updt is True : 
                self.scrollw = (((self.y1 - self.y) * self.scrv) / self.maxv)
                if self.scrollw < 1 : 
                    self.scrollw = 1
                pass
            pass
        else : 
            self.barw = ((self.x1 - self.x) - (self.linew * 2))
            if updt is True : 
                self.scrollw = (((self.x1 - self.x) * self.scrv) / self.maxv)
                if self.scrollw > (self.x1 - self.x) : 
                    self.scrollw = (self.x1 - self.x)
                pass
            pass
        self.clr = [0, 2113648, 16777215]




    def scrollwidth(self, val = None):
        if val is not None : 
            self.scrollw = val
        return self.scrollw




    def draw(self):
        if self.kind == 0 : 
            self.canv.rectangle((self.x, self.y, self.x1, self.y1), outline = self.clr[0], fill = self.clr[2], width = self.linew)
            if self.vert is True : 
                self.canv.rectangle((self.x + self.linew, self.y + self.linew + self.dcor, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = None, fill = self.clr[1])
            else : 
                self.canv.rectangle((self.x + self.linew + self.dcor, self.y + self.linew, self.x + self.linew + self.dcor + self.scrollw, (self.y1 - self.linew)), outline = None, fill = self.clr[1])
            pass
        elif self.kind == 1 : 
            self.canv.rectangle((self.x, self.y, self.x1, self.y1), outline = self.clr[0], fill = self.clr[2], width = self.linew)
            if self.vert is True : 
                self.canv.line(((self.x1 - self.linew), self.y + self.linew + self.dcor, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = self.clr[1])
            else : 
                self.canv.line((self.x + self.linew + self.dcor + self.scrollw, self.y + self.linew, self.x + self.linew + self.dcor + self.scrollw, (self.y1 - self.linew)), outline = self.clr[1])
            pass
        elif self.kind == 2 : 
            self.canv.rectangle((self.x, self.y, self.x1, self.y1), outline = self.clr[0], fill = self.clr[2], width = self.linew)
            if self.vert is True : 
                self.canv.rectangle((self.x + self.linew, self.y + self.linew, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = None, fill = self.clr[1])
            else : 
                self.canv.rectangle((self.x + self.linew + self.space, self.y + self.linew + self.space, (self.x + self.linew + self.space + self.dcor + 1), (((self.y1 - self.space) - self.linew) + 1)), outline = None, fill = self.clr[1])
            pass
        elif self.kind == 3 : 
            softrect(self.canv, (self.x, self.y, self.x1, self.y1), outline = self.clr[0], fill = self.clr[2], width = self.linew, corner = self.corner)
            if self.vert is True : 
                self.canv.rectangle((self.x + self.linew, self.y + self.linew, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = None, fill = self.clr[1])
            else : 
                softrect(self.canv, (self.x + (self.linew / 2) + self.space, self.y + (self.linew / 2) + self.space, (self.x + (self.linew / 2) + self.space + self.dcor + 1), (((self.y1 - self.space) - (self.linew / 2)) + 1)), outline = None, fill = self.clr[1], corner = self.corner)
            pass




    def percent(self, perc = None):
        if perc is not None : 
            self.perc = perc
            if perc < 0.0 : 
                self.perc = 0.0
            if perc > 100.0 : 
                self.perc = 100.0
            self.dcor = ((self.perc * (self.barw - self.scrollw)) / 100.0)
            if self.dcor > ((self.barw - self.scrollw) - (self.space * 2)) : 
                self.dcor = ((self.barw - self.scrollw) - (self.space * 2))
            pass
        else : 
            return self.perc




    def update(self, perc):
        self.percent(perc)
        self.draw()




    def value(self, val = None):
        if val is not None : 
            self.curval = float(val)
            if self.curval > self.maxv : 
                self.curval = self.maxv
            if self.curval < self.minv : 
                self.curval = self.minv
            self.percent(((self.curval * 100.0) / self.maxv))
        else : 
            return self.curval




    def maxvalue(self, maxv = None):
        if maxv is not None : 
            self.maxv = maxv
            if self.vert is True : 
                self.barw = (self.y1 - self.y)
                self.scrollw = (((self.y1 - self.y) * (self.y1 - self.y)) / self.maxv)
                if self.scrollw > (self.y1 - self.y) : 
                    self.scrollw = (self.y1 - self.y)
                pass
            else : 
                self.barw = (self.x1 - self.x)
                self.scrollw = (((self.x1 - self.x) * (self.x1 - self.x)) / self.maxv)
                if self.scrollw > (self.x1 - self.x) : 
                    self.scrollw = (self.x1 - self.x)
                pass
            pass
        else : 
            return self.maxv




    def screenvalue(self, val = None):
        if val is not None : 
            self.scrv = val
        return self.scrv




    def color(self, color = None):
        if color is not None : 
            self.clr = color
        else : 
            return self.clr




    def linewidth(self, width = None):
        if width is not None : 
            self.linew = width
        else : 
            return self.linew






class Ttextlist(object, ) :


    __module__ = __name__
    def __init__(self, coord, canv, itempares, font = None):
        self._define(coord, canv, itempares, font)




    def _define(self, coord, canv, itempares, font = None):
        self.canv = canv
        self.x = coord[0]
        self.y = coord[1]
        self.w = 0
        self.h = 0
        self.texth = 0
        self.lineh = 0
        self.itemblckd = [False for x in itempares]
        self.keylessit = [False for x in itempares]
        self.items = [x[0] for x in itempares]
        self.drawitems = [str((t + 1)) + ' ' + self.items[t] for t in xrange(len(self.items)) if t < 9 ]
        self.drawitems.extend([str(0) + ' ' + self.items[t] for t in xrange(len(self.items)) if t == 9 ])
        self.drawitems.extend([u'*' + ' ' + self.items[t] for t in xrange(len(self.items)) if t == 10 ])
        self.drawitems.extend([u'#' + ' ' + self.items[t] for t in xrange(len(self.items)) if t == 11 ])
        self.drawitems.extend([self.items[t] for t in xrange(len(self.items)) if t >= 12 ])
        self.itemfnt = [font for x in itempares]
        self.itemic = [[None, None] for x in itempares]
        self.callbacks = [x[1] for x in itempares]
        self.callid = None
        self.call = False
        self.itcount = len(itempares)
        self.cicled = True
        self.sp_l = 2
        self.sp_r = 2
        self.sp_u = 2
        self.sp_d = 2
        self.sp_bl = 2
        self.sp_sb_lr = 1
        self.sp_sb_ud = 1
        self.hdn = False
        self.curit = 0
        self.sbx = self.x
        self.sby = self.y
        self.firstit = None
        Ttextlist.iteminlist(self, len(self.items))
        self._getmaxtextwidth()
        self._gettextheight()
        self._updatewidth()
        self._updateheight()
        self.font(font)
        self.clrs = [None, 3238597, 0, 16777215, 8355711]
        self.moving = False
        self.blckd = False
        self.movespd = 0
        self.movex = 0
        self.movey = 0
        self.keybrd = Keyboard()
        self.call = False
        self.startdown = None
        self.startup = None
        self.startscroll = 0
        self.key = {}
        self.key['up'] = key_codes.EScancodeUpArrow
        self.key['down'] = key_codes.EScancodeDownArrow
        self.key['select'] = key_codes.EScancodeSelect
        self.key['select2'] = key_codes.EScancodeLeftSoftkey




    def gettextheight(self, font):
        s = self.canv.measure_text(u'WTFPLljyp!,\xc0\xd4\xc4\xd9\xc9\xf0\xf3,', font = font)
        return (s[0][3] - s[0][1])




    def _getmaxtextwidth(self):
        w = 0
        for t in xrange(self.itcount):
            s = self.canv.measure_text(self.drawitems[t], font = self.itemfnt[t])
            tw = (s[0][2] - s[0][0])
            w = max(tw, w)
        self.textw = w
        return self.textw




    def _gettextheight(self):
        self.texth = self.gettextheight(self.itemfnt[0])
        self.lineh = self.texth + self.sp_bl
        return self.texth




    def getitemheight(self):
        return self.lineh




    def forcetextheight(self, h):
        self.texth = h
        self.lineh = h + self.sp_bl
        self.h = (self.texth * self.itcount) + (self.sp_bl * (self.itcount - 1)) + self.sp_d + self.sp_u




    def _updatewidth(self):
        self.w = self._getmaxtextwidth() + self.sp_l + self.sp_r
        return self.w




    def _updateheight(self):
        self.h = (self._gettextheight() * self.itinlist) + (self.sp_bl * (self.itinlist - 1)) + self.sp_d + self.sp_u
        return self.h




    def iteminlist(self, val = None):
        if val is not None : 
            self.itinlist = val
            if self.itinlist > len(self.items) : 
                self.itinlist = len(self.items)
            self.firstit = 0
        elif val == 'full' or val == 'fill' : 
            self.itinlist = (self.h / self.itemhg[0])
        return self.itinlist




    def size(self, sz = None):
        if sz is not None : 
            if sz[0] is not None : 
                self.w = sz[0]
            if sz[1] is not None : 
                self.h = sz[1]
            pass
        return (self.w, self.h)




    def font(self, fnt = None):
        if fnt is not None : 
            for t in xrange(self.itcount):
                self.itemfont(t, fnt)
            self.textw = self._getmaxtextwidth()
            self.texth = self._gettextheight()
            self._updatewidth()
            self._updateheight()
        else : 
            return self.itemfnt[0]




    def itemfont(self, t, fnt = None):
        if fnt is not None : 
            self.itemfnt[t] = fnt
        return self.itemfnt[t]




    def itemicon(self, t, img = None, mask = None):
        if img is not None : 
            self.itemic[t][0] = img
            self.itemic[t][1] = mask
            self.sp_l = (img.size[0] + 2)
        return self.itemic[t]




    def draw(self):
        self._control()
        self.sbx = (self.x + 1)
        self.sby = self.y + self.sp_u + ((self.curit - self.firstit) * self.texth) + ((self.curit - self.firstit) * self.sp_bl)
        self.canv.rectangle((self.sbx, (self.sby - self.sp_sb_ud), (self.sbx + self.w - 2), self.sby + self.texth + self.sp_sb_ud), outline = self.clrs[0], fill = self.clrs[1], width = 1)
        for n in xrange(self.firstit, self.firstit + self.itinlist):
            t = (n - self.firstit)
            if self.itemic[n][0] is not None : 
                self.canv.blit(self.itemic[n][0], target = (self.x, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * t) - 1)), mask = self.itemic[n][1])
            if n == self.curit : 
                if self.itemblckd[n] is True : 
                    self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 1)), self.drawitems[n], fill = self.clrs[4], font = self.itemfnt[n])
                else : 
                    self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 1)), self.drawitems[n], fill = self.clrs[3], font = self.itemfnt[n])
                pass
            elif self.itemblckd[n] is True : 
                self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 1)), self.drawitems[n], fill = self.clrs[4], font = self.itemfnt[n])
            else : 
                self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 1)), self.drawitems[n], fill = self.clrs[2], font = self.itemfnt[n])




    def nextitem(self):
        self.curit += 1
        if self.curit > (self.firstit + self.itinlist - 1) : 
            self.firstit += 1
        if self.curit > (self.itcount - 1) : 
            if self.cicled is True : 
                self.curit = 0
                self.firstit = 0
            else : 
                self.curit = (self.itcount - 1)
            pass




    def previtem(self):
        self.curit -= 1
        if self.curit < self.firstit : 
            self.firstit -= 1
        if self.curit < 0 : 
            if self.cicled is True : 
                self.curit = (self.itcount - 1)
                self.firstit = (self.itcount - self.itinlist)
            else : 
                self.curit = 0
            pass




    def gotoitem(self, it, fst = None):
        self.curit = it
        if fst is None : 
            self.firstit = (self.curit - (self.itinlist / 2))
        else : 
            self.firstit = fst
        if self.firstit > (self.itcount - self.itinlist) : 
            self.firstit = (self.itcount - self.itinlist)
        elif self.firstit < 0 : 
            self.firstit = 0




    def keylessitem(self, it, state = True):
        self.keylessit[it] = state
        if state == True : 
            self.drawitems[it] = self.drawitems[it][2 : ]




    def tryshortcut(self, it):
        it = self._correctitem(it)
        if self.keylessit[it] is True : 
            return False
        self.gotoitem(it)
        return True




    def _correctitem(self, it):
        if it > (self.itcount - 1) : 
            it = (self.itcount - 1)
        elif it < 0 : 
            it = 0
        return it




    def _control(self):
        if  not (self.blckd) : 
            if self.startdown is not None : 
                if (clock() - self.startdown) > 0.26 : 
                    if (clock() - self.startscroll) > 0.1 : 
                        self.startscroll = clock()
                        self.nextitem()
                    pass
                pass
            elif self.startup is not None : 
                if (clock() - self.startup) > 0.26 : 
                    if (clock() - self.startscroll) > 0.1 : 
                        self.startscroll = clock()
                        self.previtem()
                    pass
                pass
            pass




    def callperversion(self):
        if self.call : 
            self.call = False
            self.callbacks[self.callid]()




    def _in(self):
        if  not (callable(self.callbacks[self.curit]) and self.itemblckd[self.curit]) : 
            self.callid = self.curit
            self.call = True
            return Nullevent()




    def control(self, evt):
        self.callperversion()
        if  not (self.blckd) : 
            self.keybrd.handle_event(evt)
            if evt['type'] == appuifw.EEventKeyUp : 
                self.startdown = None
                self.startup = None
            if evt['type'] == appuifw.EEventKeyDown : 
                if evt['scancode'] == self.key['down'] : 
                    self.nextitem()
                    self.startdown = clock()
                elif evt['scancode'] == self.key['up'] : 
                    self.previtem()
                    self.startup = clock()
                if evt['scancode'] == key_codes.EScancode1 : 
                    if  not (self.tryshortcut(0)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode2 : 
                    if  not (self.tryshortcut(1)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode3 : 
                    if  not (self.tryshortcut(2)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode4 : 
                    if  not (self.tryshortcut(3)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode5 : 
                    if  not (self.tryshortcut(4)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode6 : 
                    if  not (self.tryshortcut(5)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode7 : 
                    if  not (self.tryshortcut(6)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode8 : 
                    if  not (self.tryshortcut(7)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode9 : 
                    if  not (self.tryshortcut(8)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancode0 : 
                    if  not (self.tryshortcut(9)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancodeStar : 
                    if  not (self.tryshortcut(10)) : 
                        return Nullevent()
                    self._in()
                elif evt['scancode'] == key_codes.EScancodeHash : 
                    if  not (self.tryshortcut(11)) : 
                        return Nullevent()
                    self._in()
                pass
            if evt['type'] == appuifw.EEventKeyDown : 
                if evt['scancode'] == self.key['select'] or evt['scancode'] == self.key['select2'] : 
                    if self.call : 
                        self.call = False
                    if  not (callable(self.callbacks[self.curit]) and self.itemblckd[self.curit]) : 
                        self.callid = self.curit
                        self.call = True
                        return Nullevent()
                    pass
                pass
            pass
        return evt




    def coord(self, crd = None):
        if crd is not None : 
            if crd[0] is not None : 
                self.x = crd[0]
            if crd[1] is not None : 
                self.y = crd[1]
            pass
        else : 
            return (self.x, self.y)




    def moveto(self, x, y, spd):
        self.movex = x
        self.movey = y
        self.movespd = spd
        self.moving = True




    def _move(self, x, y, spd):
        if self.moving is True : 
            value = (self.x - self.sbx)
            dy = (self.y - self.sby)
            if self.x < x : 
                self.x += spd
                if self.x >= x : 
                    self.x = x
                pass
            if self.y < y : 
                self.y += spd
                if self.y >= y : 
                    self.y = y
                pass
            if self.x > x : 
                self.x -= spd
                if self.x <= x : 
                    self.x = x
                pass
            if self.y > y : 
                self.y -= spd
                if self.y <= y : 
                    self.y = y
                pass
            self.sbx = (self.x - value)
            self.sby = (self.y - dy)
            if self.x == x and self.y == y : 
                self.moving = False
            pass




    def curitem(self, cur = None):
        if cur is not None : 
            self.curit = cur
        return self.curit




    def curitemname(self, name = None):
        if name is not None : 
            self.items[self.curit] = name
        return self.items[self.curit]




    def getitemindex(self, name):
        return self.items.index(name)




    def colors(self, color = None):
        if color is not None : 
            for t in xrange(len(color)):
                self.clrs[t] = color[t]
            pass
        return self.clrs




    def spaces(self, sps):
        if sps is not None : 
            if sps[0] is not None : 
                self.sp_l = sps[0]
            if sps[1] is not None : 
                self.sp_r = sps[1]
            if sps[2] is not None : 
                self.sp_u = sps[2]
            if sps[3] is not None : 
                self.sp_d = sps[3]
            if sps[4] is not None : 
                self.sp_bl = sps[4]
            self._updatewidth()
            self._updateheight()
        else : 
            return [self.sp_l, self.sp_r, self.sp_u, self.sp_d]




    def hiden(self, hd = None):
        if hd is not None : 
            self.hdn = hd
            if self.hdn is True : 
                self.blckd = True
            else : 
                self.blckd = False
            pass
        return self.hdn




    def itemblocked(self, it, bl = None):
        if bl is not None : 
            self.itemblckd[it] = bl
        return self.itemblckd[it]




    def blocked(self, bl = None):
        if bl is not None : 
            self.blckd = bl
        return self.blckd




    def setitemfunct(self, it, funct):
        if type(it) == type(1) : 
            self.callbacks[it] = funct
        else : 
            try :
                i = self.items.index(it)
                if i != -1 : 
                    self.callbacks[i] = funct
            except :
                pass
            pass






class Tscrolltextlist(Ttextlist, ) :


    __module__ = __name__
    def __init__(self, coord, canv, itempares, font = None):
        self._define(coord, canv, itempares, font)




    def _define(self, coord, canv, itempares, font = None):
        Ttextlist._define(self, coord, canv, itempares, font)
        self.scroll = None
        x = coord[0] + self.w
        if x > (canv.size[0] - 4) : 
            x = (canv.size[0] - 4)
        y = coord[1]
        if self.itcount > self.itinlist : 
            count = (self.itcount - self.itinlist)
            self.scroll = Tbar(x, y, (x + 4), y + (self.itinlist * self.texth), (0, count), self.itinlist, canv, True)
            self.scroll.scrollwidth(((self.scroll.barw * self.itinlist) / self.itcount))




    def iteminlist(self, val = None):
        Ttextlist.iteminlist(self, val)
        x = self.coord()[0] + self.w
        if x > (self.canv.size[0] - 4) : 
            x = (self.canv.size[0] - 4)
        y = self.coord()[1]
        if self.itcount > self.itinlist : 
            count = (self.itcount - self.itinlist)
            self.scroll = Tbar(x, y, (x + 4), y + (self.itinlist * self.texth), (0, count), self.itinlist, self.canv, True)
            self.scroll.scrollwidth(((self.scroll.barw * self.itinlist) / self.itcount))




    def draw(self):
        Ttextlist.draw(self)
        if self.scroll is not None : 
            self.scroll.draw()




    def control(self, evt):
        evt = Ttextlist.control(self, evt)
        if self.scroll is not None : 
            self.scroll.value(self.firstit)
        return evt






class Ttextlistex(Ttextlist, ) :


    __module__ = __name__
    def __init__(self, coord, canv, itempares, font = None):
        self._define(coord, canv, itempares, font)




    def _define(self, coord, canv, itempares, font = None):
        Ttextlist._define(self, coord, canv, itempares, font)
        self.markedit = [False for t in self.items]
        self.parentlist = None
        self.itchildlist = [None for t in self.items]
        self.parentline = None




    def draw(self):
        Ttextlist.draw(self)
        for t in xrange(self.itcount):
            if self.itchildlist[t] is not None : 
                s = (self.lineh / 5)
                h = self.lineh
                if t == self.curit : 
                    self.canv.polygon(([(self.x + self.w - h) + (3 * s), (self.y + (h * t) + (2 * s) + 1)], [(self.x + self.w - h) + (4 * s), (self.y + (h * t) + (3 * s) + 1)], [(self.x + self.w - h) + (3 * s), (self.y + (h * t) + (4 * s) + 1)]), outline = self.clrs[3], fill = self.clrs[3])
                else : 
                    self.canv.polygon(([(self.x + self.w - h) + (3 * s), (self.y + (h * t) + (2 * s) + 1)], [(self.x + self.w - h) + (4 * s), (self.y + (h * t) + (3 * s) + 1)], [(self.x + self.w - h) + (3 * s), (self.y + (h * t) + (4 * s) + 1)]), outline = self.clrs[2], fill = self.clrs[2])
                pass




    def setchild(self, it, ch):
        self.itchildlist[it] = ch
        ch.setparent(it, self)




    def setparent(self, it, par):
        self.parentlist = par
        self.parentline = it
        self.setlevel((par.level + 1))






class Tmenulist(Ttextlistex, ) :


    __module__ = __name__
    def __init__(self, coord, canv, itempares, font = None):
        self._define(coord, canv, itempares, font)
        self.level = 0




    def _define(self, coord, canv, itempares, font = None):
        Ttextlistex._define(self, coord, canv, itempares, font)
        self.formclrs = [2171169, 11184810, 0]




    def setlevel(self, lev):
        self.level = lev




    def draw(self):
        if self.hdn != True : 
            if self.curit != -1 : 
                self._move(self.movex, self.movey, self.movespd)
                self.canv.rectangle(((self.x + 2), (self.y + 2), (self.x + self.w + 2), (self.y + self.h + 2)), outline = None, fill = self.formclrs[2], width = 0)
                self.canv.rectangle((self.x, self.y, self.x + self.w, self.y + self.h), outline = self.formclrs[0], fill = self.formclrs[1], width = 1)
                Ttextlistex.draw(self)
            pass




    def colors(self, color = None):
        if color[0] is not None : 
            for t in xrange(len(color[0])):
                self.formclrs[t] = color[0][t]
            Ttextlistex.colors(self, color[1])
        return (self.formclrs, self.clrs)






class Tmultimenu(object, ) :


    __module__ = __name__
    def __init__(self, coord, canv, key, itempares, font = None):
        self._define(coord, canv, key, itempares, font)




    def _define(self, coord, canv, key, itempares, font = None):
        self.canv = canv
        self.callback = None
        self.items = itempares
        self.mcount = len(itempares)
        self.mlistcount = 1
        self.crd = coord
        self.fnt = font
        self.dspace = 0
        self.x = 0
        self.y = 0
        self._createmenus(font)
        self.resetpos()
        self.bindtokey(key)
        self.keybrd = Keyboard()
        self.onhide = None
        self.onshow = None
        self.currentmenu = None




    def coord(self, crd = None):
        if crd is not None : 
            self.crd = crd
            self.resetpos()
        return self._coord()




    def resetpos(self):
        if len(self.crd) > 2 : 
            if self.crd == 'leftup' : 
                self.x = 1
                self.y = 1
            elif self.crd == 'leftbottom' : 
                self.x = 1
                self.y = ((self.canv.size[1] - self.mlists[0].h) - 1)
            elif self.crd == 'rightup' : 
                self.x = ((self.canv.size[0] - self.mlists[0].w) + 1)
                self.y = 1
            elif self.crd == 'rightbottom' : 
                self.x = ((self.canv.size[0] - self.mlists[0].w) - 3)
                self.y = ((self.canv.size[1] - self.mlists[0].h) - 1)
            elif self.crd == 'center' : 
                self.x = ((self.canv.size[0] / 2) - (self.mlists[0].w / 2))
                self.y = ((self.canv.size[1] / 2) - (self.mlists[0].h / 2))
            self._coord([self.x, self.y])
        else : 
            self.x = self.crd[0]
            self.y = self.crd[1]
            self._coord([self.x, self.y])




    def bindtokey(self, key):
        self.key = key




    def _createmenus(self, font):
        self.mlists = []
        self._createmenu_recursive((self.x, self.y), self.items)
        self.w = self.mlists[0].w
        self.h = self.mlists[0].h
        self.mlistcount = len(self.mlists)




    def _createmenu_recursive(self, coord, itempares):
        menu = self._createmenu(coord, itempares)
        self.mlists.append(menu)
        menu.hiden(True)
        for t in xrange(len(itempares)):
            if  not (callable(itempares[t][1])) : 
                childmenu = self._createmenu_recursive(((menu.x + menu.w - menu.texth), menu.y + (menu.lineh * t)), itempares[t][1])
                menu.setchild(t, childmenu)
        return menu




    def _createmenu(self, coord, itempares):
        if  not (callable(itempares)) : 
            lst = Tmenulist(coord, self.canv, itempares, self.fnt)
            self.defspaces(lst)
            return lst




    def defspaces(self, lst):
        lst.sp_r = lst.lineh
        lst.sp_l = (lst.lineh / 4)
        lst._updatewidth()




    def draw(self):
        for lst in self.mlists:
            lst.draw()
        self.x = self.mlists[0].x
        self.y = self.mlists[0].y




    def _in(self):
        cur = self.mlists[0].curit
        for t in xrange(len(self.mlists)):
            if  not ( not (self.mlists[t].hiden()) and self.mlists[t].blocked()) : 
                if  not (self.mlists[t].itchildlist[self.mlists[t].curit] is not None and self.mlists[t].itemblckd[self.mlists[t].curit]) : 
                    self.mlists[t].itchildlist[self.mlists[t].curit].hiden(False)
                    self.mlists[t].blocked(True)
                    return None
                elif  not (self.mlists[t].itchildlist[self.mlists[t].curit] is None and self.mlists[t].itemblckd[self.mlists[t].curit]) : 
                    self.hiden(True)
                    return Nullevent()
                pass




    def _out(self):
        cur = self.mlists[0].curit
        if  not (self.mlists[0].blocked()) : 
            self.hiden(True)
            return Nullevent()
        else : 
            for t in xrange(1, len(self.mlists)):
                if  not ( not (self.mlists[t].hiden()) and self.mlists[t].blocked()) : 
                    if  not (self.mlists[t].parentlist is not None and self.mlists[t].parentlist.itemblckd[self.mlists[t].parentlist.curit]) : 
                        self.mlists[t].hiden(True)
                        self.mlists[t].curit = 0
                        self.mlists[t].parentlist.blocked(False)
                        return None
                    pass
            pass




    def control(self, evt):
        for lst in self.mlists:
            evt = lst.control(evt)
            if evt['type'] is None : 
                self.hiden(True)
                return evt
        kcode = evt['scancode']
        once = 0
        if  not (self.hiden()) : 
            if evt['type'] == appuifw.EEventKeyDown : 
                if evt['scancode'] == key_codes.EScancode1 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode2 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode3 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode4 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode5 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode6 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode7 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode8 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode9 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancode0 : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancodeStar : 
                    self._in()
                elif evt['scancode'] == key_codes.EScancodeHash : 
                    self._in()
                if kcode == key_codes.EScancodeRightArrow or kcode == key_codes.EScancodeSelect or kcode == key_codes.EScancodeLeftSoftkey : 
                    self._in()
                elif kcode == key_codes.EScancodeLeftArrow : 
                    self._out()
                elif kcode == key_codes.EScancodeUpArrow : 
                    pass
                elif kcode == key_codes.EScancodeDownArrow : 
                    pass
                elif kcode == key_codes.EScancodeRightSoftkey : 
                    self.hiden(True)
                pass
            pass
        elif evt['type'] == appuifw.EEventKeyDown and kcode == self.key : 
            self.hiden(False)
        return evt




    def setonhide(self, funct):
        if callable(funct) : 
            self.onhide = funct




    def setonshow(self, funct):
        if callable(funct) : 
            self.onshow = funct




    def hiden(self, state = None):
        if state is True : 
            self.resetcurit()
            for lst in self.mlists:
                lst.hiden(state)
            if callable(self.onhide) : 
                self.onhide()
            pass
        elif state is False : 
            self.mlists[0].hiden(state)
            if callable(self.onshow) : 
                self.onshow()
            pass
        return self.mlists[0].hiden()




    def itemblocked(self, mn, it, state = None):
        return self.mlists[mn].itemblocked(it, state)




    def keylessitem(self, mn, it, state = True):
        self.mlists[mn].keylessitem(it, state)




    def getitemindex(self, i, name):
        return self.mlists[i].getitemindex(name)




    def resetcurit(self):
        for t in xrange(len(self.mlists)):
            self.mlists[t].curit = 0




    def moveto(self, x, y, spd):
        self.mlists[0].moveto(x, y, spd)




    def _coord(self, crd = None):
        if crd is not None : 
            oldcrd = self.mlists[0].coord()
            dcrd = [(crd[0] - oldcrd[0]), (crd[1] - oldcrd[1])]
            self.mlists[0].coord(crd)
            self.correctcoord(self.mlists[0])
            self.x = self.mlists[0].x
            self.y = self.mlists[0].y
            for t in xrange(1, len(self.mlists)):
                self.mlists[t].x = (self.mlists[t].parentlist.x + self.mlists[t].parentlist.w - min(((self.mlists[t].parentlist.w * 2) / 3), ((self.mlists[t].w * 2) / 3)))
                self.mlists[t].y = self.mlists[t].parentlist.y + (self.mlists[t].parentlist.lineh * self.mlists[t].parentline)
                self.correctcoord(self.mlists[t])
            pass
        else : 
            return (self.x, self.y)




    def correctcoord(self, mlists):
        if mlists.x < 1 : 
            mlists.x = 1
        if mlists.x > ((self.canv.size[0] - mlists.w) - 1) : 
            mlists.x = ((self.canv.size[0] - mlists.w) - 1)
        if mlists.y < 1 : 
            mlists.y = 1
        if mlists.y > (((self.canv.size[1] - self.dspace) - mlists.h) - 1) : 
            mlists.y = (((self.canv.size[1] - self.dspace) - mlists.h) - 1)




    def size(self, ind, sz = None):
        return self.mlists[ind].size(sz)




    def sizeall(self, sz):
        for t in xrange(len(self.mlists)):
            self.mlists[t].size(sz)




    def font(self, fnt = None):
        if fnt is not None : 
            self.fnt = fnt
            for t in xrange(len(self.mlists)):
                self.mlists[t].font(fnt)
                self.mlists[t].sp_r = self.lineh
            pass
        else : 
            return self.fnt




    def colors(self, color = None):
        if color is not None : 
            self.clr = color
            for t in xrange(len(self.mlists)):
                self.mlists[t].colors(color)
            pass
        else : 
            return self.clr




    def spaces(self, sps = None):
        if sps is not None : 
            for t in xrange(len(self.mlists)):
                self.mlists[t].spaces(sps)
            pass
        else : 
            return self.mlists[0].spaces()




    def sidespace(self, sp = None):
        if sp is not None : 
            self.dspace = sp
        return self.dspace




    def forcetextheight(self, h):
        for t in xrange(len(self.mlists)):
            self.mlists[t].forcetextheight(h)
        self.resetpos()




    def setitemfunct(self, m, it, funct):
        self.mlists[m].setitemfunct(it, funct)






class Tsysmenu(Tmultimenu, ) :


    __module__ = __name__
    mlist = []
    current = [None, None]
    blocked = [False, False]
    count = 0
    tcanv = None
    x = 0
    y = 0
    onhide = None
    onshow = None
    def __init__(self, soft, coord, tcanv, canv, itempares, font = None):
        self.createmenu(soft, coord, canv, itempares, font)
        Tsysmenu.addmenu(self)
        Tsysmenu.tcanv = tcanv




    def createmenu(self, soft, coord, canv, itempares, font = None):
        self.soft = soft
        if soft == 0 : 
            key = key_codes.EScancodeLeftSoftkey
        elif soft == 1 : 
            key = key_codes.EScancodeRightSoftkey
        Tmultimenu._define(self, coord, canv, key, itempares, font)




    def addmenu(menu):
        Tsysmenu.mlist.append(menu)
        Tsysmenu.count = len(Tsysmenu.mlist)




    addmenu = staticmethod(addmenu)
    def setcurrent(soft, menu):
        if menu is None : 
            if soft < 2 : 
                Tsysmenu.current[soft] = None
            pass
        elif soft < 2 : 
            Tsysmenu.current[soft] = menu




    setcurrent = staticmethod(setcurrent)
    def draw():
        for t in xrange(2):
            if Tsysmenu.current[t] is not None : 
                Tmultimenu.draw(Tsysmenu.current[t])




    draw = staticmethod(draw)
    def control(evt):
        if Tsysmenu.current[0] is None : 
            Tsysmenu.blocked[1] = False
        else : 
            Tsysmenu.blocked[1] =  not (Tsysmenu.current[0].hiden())
        if Tsysmenu.current[1] is None : 
            Tsysmenu.blocked[0] = False
        else : 
            Tsysmenu.blocked[0] =  not (Tsysmenu.current[1].hiden())
        for t in xrange(2):
            if Tsysmenu.current[t] is not None : 
                if  not (Tsysmenu.blocked[t]) : 
                    evt = Tmultimenu.control(Tsysmenu.current[t], evt)
                pass
        return evt




    control = staticmethod(control)
    def hidenall():
        for t in xrange(2):
            if Tsysmenu.current[t] is not None : 
                if Tsysmenu.current[t].hiden() is False : 
                    return False
                pass
        return True


    hidenall = staticmethod(hidenall)

