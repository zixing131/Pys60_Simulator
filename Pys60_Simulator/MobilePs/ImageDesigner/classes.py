# -*- coding: utf-8 -*-

import appuifw
import graphics
import key_codes
import sys
__version__ = 1.4
def new_image(size, mode = 'RGB16'):
    try :
        return graphics.Image.new(size, mode)
    except :
        appuifw.note(dtext['e_lowmemory'], 'error')
        return None




def copy_image(img):
    im = new_image(img.size)
    if im is not None : 
        im.blit(img)
    return im




class Keyboard(object, ) :


    __module__ = __name__
    def __init__(self, onevent = lambda  : None ):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}
        self._onevent = onevent
        self.evt = {'keycode' : None, 'scancode' : None, 'type' : None}




    def handle_event(self, event):
        self.evt = event
        self._downs = {}
        if event['type'] == appuifw.EEventKeyDown : 
            self._state = event['scancode']
            if  not (self._keyboard_state.get(self._state, False)) : 
                self._downs[self._state] = True
            self._keyboard_state[self._state] = True
        elif event['type'] == appuifw.EEventKeyUp : 
            self._keyboard_state[event['scancode']] = False
            self._state = None
        if self._state is None : 
            self._check = True




    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, False)




    def pressed(self, scancode):
        return self._downs.get(scancode, False)




    def state(self):
        return self._state




    def freedown(self, scancode):
        if self._check : 
            if self._downs.get(scancode, False) : 
                self._check = False
                return True
            pass
        return False




    def keycode(self, code):
        if self.evt['keycode'] == code : 
            return True
        return False




    def scancode(self, code):
        if self.evt['scancode'] == code : 
            return True
        return False




    def resetkeys(self):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}






def rect(canv, cr, outline = None, fill = None, width = 1, pattern = None):
    if cr[0] != cr[2] and cr[1] != cr[3] : 
        canv.rectangle([min(cr[0], cr[2]), min(cr[1], cr[3]), (max(cr[0], cr[2]) + 1), (max(cr[1], cr[3]) + 1)], outline, fill, width)
    else : 
        line(canv, [cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)




def ellps(canv, cr, outline = None, fill = None, width = 1, pattern = None):
    if cr[0] != cr[2] and cr[1] != cr[3] : 
        canv.ellipse([min(cr[0], cr[2]), min(cr[1], cr[3]), max(cr[0], cr[2]), max(cr[1], cr[3])], outline, fill, width)
    else : 
        line(canv, [cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)




def line(can, cr, outline, width):
    can.line([cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)
    can.point((cr[2], cr[3]), outline = outline, width = width)




def fromrgb(c):
    return ((c[0] * 256) * 256) + (c[1] * 256) + c[2]




def torgb(color):
    b = (color % 256)
    g = ((color / 256) % 256)
    r = (((color / 256) / 256) % 256)
    return (r, g, b)




class TSelectorTool(object, ) :


    __module__ = __name__
    def __init__(self, keyboard, buff, img, iw, mes_callback):
        self.tls = [0, 0, 0, 0]
        self.tls[0] = TSelector(keyboard, buff, img, 0)
        self.tls[1] = TSelector(keyboard, buff, img, 1)
        self.tls[2] = TLassoSelector(keyboard, buff, img)
        self.tls[3] = TMagicrod(keyboard, buff, img, mes_callback)
        self.tool = None
        self.iw = iw




    def set(self, ind):
        for t in self.tls:
            t.enabled(False)
        if ind is None : 
            self.tool = None
        else : 
            self.tool = self.tls[ind]
            self.tool.enabled(True)




    def get(self):
        for t in xrange(len(self.tls)):
            if self.tls[t].enabled() : 
                return t
        return None




    def control(self):
        if self.tool is None : 
            return None
        self.tool.eventcontrol(self.iw)




    def draw(self):
        if self.tool is None : 
            return None
        self.tool.draw(self.iw)




    def clippaste(self):
        if self.tool is None : 
            return None
        self.tool.clippaste(self.iw)




    def clipcopy(self):
        if self.tool is None : 
            return None
        self.tool.clipcopy(self.iw)




    def clipclear(self, col):
        if self.tool is None : 
            return None
        self.tool.clipclear(self.iw, col)




    def clipcut(self, col):
        if self.tool is None : 
            return None
        self.tool.clipcut(self.iw, col)




    def selectall(self):
        self.set(0)
        self.tool.selectall(self.iw)




    def invert_selection(self):
        if self.tool is None : 
            return None
        self.tool.invert_selection(self.iw)




    def isactive(self):
        if self.tool is None : 
            return False
        if self.tool.drawing or self.tool.render : 
            return True




    def getimage(self, replace = False, blend = 16777215):
        if self.tool is None : 
            if replace : 
                return (self.iw.img, None)
            else : 
                return None
            pass
        elif self.isactive() : 
            return self.tool.getimage(self.iw, blend)
        elif replace : 
            return (self.iw.img, None)
        elif  not (replace) : 
            return None




    def setimage(self,ff, replace = False, blend = 16777215):
        img, msk =ff
        if self.tool is None : 
            if replace : 
                self.iw.img.blit(img)
            else : 
                return None
            pass
        elif self.isactive() : 
            self.tool.setimage(self.iw, (img, msk))
        elif replace : 
            self.iw.img.blit(img)
        elif  not (replace) : 
            return None




    def getcoord(self):
        if self.tool is None : 
            return None
        return self.tool.getcoord()




    def deselect(self):
        if self.tool is None : 
            return None
        self.tool.deselect()




    def setcallback(self, funct, mode = 'onfix'):
        if mode == 'onfix' : 
            for t in self.tls:
                t.onfix = funct
            pass




    def setblend(self, val):
        for t in self.tls:
            t.setblend(val)






class TUniSlector(object, ) :


    __module__ = __name__
    copybuff = None
    buffmsk = None
    def __init__(self, keyboard, buff, img, stype = 0):
        self.stype = stype
        self.buff = buff
        self.img = img
        self.blend = 16777215
        self.enbld = False
        self.keybrd = keyboard
        self.render = False
        self.drawing = False
        self.moving = False
        self.showbuff = False
        self.movebuff = False
        self.movable = False
        self.col = 0
        self.coldown = False
        self.onfix = None




    def enabled(self, state = None):
        if state is False : 
            self.drawing = state
            self.render = state
            if self.movable : 
                self.moving = state
            pass
        if state is not None : 
            self.enbld = state
        else : 
            return self.enbld




    def _drawselector(self, blinkspeed, fromcol, tocol, step, drawfunct):
        if self.coldown is False : 
            self.col += (step * blinkspeed)
            if self.col > tocol : 
                self.col = tocol
                self.coldown = True
            pass
        else : 
            self.col -= (step * blinkspeed)
            if self.col < fromcol : 
                self.col = fromcol
                self.coldown = False
            pass
        drawfunct()




    def _drawto(self, drawfunct):
        if self.render is False : 
            self._drawselector(15, 0, 16777215, 65793, drawfunct)
        else : 
            self._drawselector(20, 16711680, 16777215, 257, drawfunct)




    def resetcol(self):
        self.col = 16777215




    def showbuffer(self, state):
        if TUniSlector.copybuff is not None : 
            self.showbuff = state




    def movebuffer(self, state):
        if TUniSlector.copybuff is not None : 
            self.showbuff = state
            self.movebuff = state




    def deselect(self):
        self.drawing = False
        self.render = False
        self.moving = False




    def invert_selection(self, iw):
        pass




    def fixselection(self):
        self.drawing = True
        self.render = True
        if self.movable : 
            self.moving = True




    def unfixselection(self):
        self.drawing = True
        self.render = False
        self.moving = False




    def setblend(self, val):
        self.blend = val






class TSelector(TUniSlector, ) :


    __module__ = __name__
    def __init__(self, keyboard, buff, img, stype = 0):
        TUniSlector.__init__(self, keyboard, buff, img, stype)
        self.coord = [0, 0, 0, 0]
        self.size = [0, 0]
        self.bcoord = [0, 0, 0, 0]




    def eventcontrol(self, iw):
        if self.enbld is False : 
            return None
        if self.keybrd.freedown(key_codes.EScancodeSelect) : 
            if self.movebuff is True : 
                self.movebuffer(False)
                self._clippaste(iw)
                self.drawing = False
                self.render = False
            elif self.drawing is False and self.render is False : 
                self.drawing = True
                self.resetcol()
            elif self.drawing is True and self.render is False : 
                self.render = True
                self.resetcol()
                if callable(self.onfix) : 
                    self.onfix()
                pass
            elif self.drawing is True and self.render is True : 
                self.drawing = False
                self.render = False
                self.moving = False
            if self.drawing is True and self.render is False : 
                self.coord = [iw.curs.x + iw.imx, iw.curs.y + iw.imy, iw.curs.x + iw.imx, iw.curs.y + iw.imy]
                self.bcoord = [iw.curs.x, iw.curs.y, iw.curs.x, iw.curs.y]
            elif self.drawing is True and self.render is True : 
                self.coord[-2 :] = [iw.curs.x + iw.imx, iw.curs.y + iw.imy]
                self.size = [(self.coord[2] - self.coord[0]), (self.coord[3] - self.coord[1])]
                if self.movable : 
                    self.moving = True
                pass
            pass
        elif self.keybrd.freedown(key_codes.EScancodeBackspace) : 
            if self.movebuff is True : 
                self.movebuffer(False)
                self.drawing = False
                self.render = False
            pass
        if self.moving is True : 
            dx = (iw.curs.x + iw.imx - self.coord[2])
            dy = (iw.curs.y + iw.imy - self.coord[3])
            self.coord[0] += dx
            self.coord[1] += dy
            self.coord[2] += dx
            self.coord[3] += dy




    def selectall(self, iw):
        self.coord[0] = 0
        self.coord[1] = 0
        self.coord[2] = (iw.img.size[0] - 1)
        self.coord[3] = (iw.img.size[1] - 1)
        self.drawing = True
        self.render = True
        self.resetcol()




    def setcoord(self, c):
        self.coord = [c[2], c[3], c[0], c[1]]




    def getcoord(self):
        x = min(self.coord[0], self.coord[2])
        y = min(self.coord[1], self.coord[3])
        x1 = (max(self.coord[0], self.coord[2]) + 1)
        y1 = (max(self.coord[1], self.coord[3]) + 1)
        return (x, y, x1, y1)




    def getimage(self, iw, blend):
        w = abs((self.coord[0] - self.coord[2]))
        h = abs((self.coord[1] - self.coord[3]))
        if self.stype == 0 : 
            w += 1
            h += 1
        smask = graphics.Image.new((w, h), 'L')
        smask.clear(0)
        tempim = graphics.Image.new((w, h))
        image = graphics.Image.new((w, h))
        if self.stype == 0 : 
            rect(smask, (0, 0, w, h), outline = blend, fill = blend, width = 1)
        else : 
            ellps(smask, (0, 0, w, h), outline = blend, fill = blend, width = 1)
        tempim.blit(iw.img, source = self.getcoord())
        image.blit(tempim, mask = smask)
        del tempim
        return (image, smask)




    def setimage(self, iw,gg):
        img, msk =gg
        iw.img.blit(img, target = self.getcoord(), mask = msk)




    def clipcopy(self, iw):
        TUniSlector.copybuff, TUniSlector.buffmsk = self.getimage(iw, self.blend)




    def clipcut(self, iw, col):
        iw._backupimage()
        self.clipcopy(iw)
        if self.stype == 0 : 
            rect(iw.img, self.coord, outline = col, fill = col, width = 1)
        else : 
            ellps(iw.img, self.coord, outline = col, fill = col, width = 1)




    def _clippaste(self, iw):
        iw._backupimage()
        iw.img.blit(TUniSlector.copybuff, target = ((iw.curs.x - iw.x) + iw.imx, (iw.curs.y - iw.y) + iw.imy), mask = TUniSlector.buffmsk)




    def clippaste(self, iw):
        self.movebuffer(True)




    def clipclear(self, iw, col):
        iw._backupimage()
        if self.stype == 0 : 
            rect(iw.img, self.coord, outline = col, fill = col, width = 1)
        else : 
            ellps(iw.img, self.coord, outline = col, fill = col, width = 1)




    def draw(self, iw):
        if self.enbld is False : 
            return None
        if self.drawing is True : 
            if self.render is False : 
                self.bcoord = [(self.coord[0] - iw.imx), (self.coord[1] - iw.imy), iw.curs.x, iw.curs.y]
            else : 
                self.bcoord = [(self.coord[0] - iw.imx), (self.coord[1] - iw.imy), (self.coord[2] - iw.imx), (self.coord[3] - iw.imy)]
            if self.stype == 0 : 
                self._drawto(lambda  :  rect(self.buff, self.bcoord, outline = self.col, width = 1) )
            else : 
                self._drawto(lambda  :  ellps(self.buff, self.bcoord, outline = self.col, width = 1) )
            pass
        if self.showbuff is True : 
            if self.movebuff is True : 
                self.buff.blit(TUniSlector.copybuff, target = (iw.curs.x, iw.curs.y), mask = TUniSlector.buffmsk)
            pass






class TLassoSelector(TUniSlector, ) :


    __module__ = __name__
    def __init__(self, keyboard, buff, img, stype = 0):
        TUniSlector.__init__(self, keyboard, buff, img, stype)
        self.coord = []
        self.bcoord = []
        self.msk = None




    def eventcontrol(self, iw):
        if self.enbld is False : 
            return None
        if self.keybrd.freedown(key_codes.EScancodeSelect) : 
            if self.movebuff is True : 
                self.movebuffer(False)
                self._clippaste(iw)
                self.drawing = False
                self.render = False
                self.reset()
            elif self.drawing is False and self.render is False : 
                self.drawing = True
                self.resetcol()
            elif self.drawing is True and self.render is True : 
                self.drawing = False
                self.render = False
                self.moving = False
                self.reset()
            if self.drawing is True and self.render is False : 
                if len(self.bcoord) == 0 : 
                    self.bcoord.append([0, 0])
                if len(self.coord) : 
                    if self.coord[-1] == [iw.curs.x + iw.imx, iw.curs.y + iw.imy] : 
                        self.coord.pop()
                        self.bcoord.pop()
                        self.bcoord.pop()
                        self.render = True
                        self.resetcol()
                        if callable(self.onfix) : 
                            self.onfix()
                        pass
                    pass
                self.coord.append([iw.curs.x + iw.imx, iw.curs.y + iw.imy])
                self.bcoord.append([0, 0])
            pass
        elif self.keybrd.freedown(key_codes.EScancodeBackspace) : 
            if self.drawing is True and self.render is False : 
                self.coord.pop()
                self.bcoord.pop()
            if self.movebuff is True : 
                self.movebuffer(False)
                self.drawing = False
                self.render = False
                self.reset()
            pass
        if self.moving is True : 
            dx = (iw.curs.x + iw.imx - self.coord[2])
            dy = (iw.curs.y + iw.imy - self.coord[3])
            for p in self.coord:
                p[0] += dx
                p[1] += dy
            pass




    def getimage(self, iw, blend):
        l, u, r, b = self.getcoord()
        crd = [x[ : ] for x in self.coord]
        for t in xrange(len(self.coord)):
            crd[t][0] -= l
            crd[t][1] -= u
        w = abs((r - l))
        h = abs((b - u))
        smask = graphics.Image.new((w, h), 'L')
        smask.clear(0)
        image = graphics.Image.new((w, h))
        tempim = graphics.Image.new((w, h))
        if smask is None : 
            return None
        smask.polygon(crd, outline = blend, fill = blend, width = 1)
        tempim.blit(iw.img, source = (l, u, r, b))
        image.blit(tempim, mask = smask)
        del tempim
        return (image, smask)




    def setimage(self, iw,gg):
        img, msk =gg
        iw.img.blit(img, target = self.getcoord(), mask = msk)




    def getcoord(self):
        l = self.img.size[0]
        r = 0
        u = self.img.size[1]
        b = 0
        for p in self.coord:
            l = min(l, p[0])
            r = (max(r, p[0]) + 1)
            u = min(u, p[1])
            b = (max(b, p[1]) + 1)
        return (l, u, r, b)




    def clipcopy(self, iw):
        TUniSlector.copybuff, TUniSlector.buffmsk = self.getimage(iw, self.blend)




    def clipcut(self, iw, col):
        iw._backupimage()
        self.clipcopy(iw)
        iw.img.polygon(self.coord, outline = col, fill = col, width = 1)




    def _clippaste(self, iw):
        iw._backupimage()
        iw.img.blit(TUniSlector.copybuff, target = ((iw.curs.x - iw.x) + iw.imx, (iw.curs.y - iw.y) + iw.imy), mask = TUniSlector.buffmsk)




    def clippaste(self, iw):
        self.movebuffer(True)




    def clipclear(self, iw, col):
        iw._backupimage()
        iw.img.polygon(self.coord, outline = col, fill = col, width = 1)




    def reset(self):
        self.coord = []
        self.bcoord = []




    def draw(self, iw):
        if self.enbld is False : 
            return None
        if self.drawing is True : 
            for t in xrange(len(self.coord)):
                self.bcoord[t][0] = (self.coord[t][0] - iw.imx)
                self.bcoord[t][1] = (self.coord[t][1] - iw.imy)
            if  not (self.render) : 
                self.bcoord[-1][0] = iw.curs.x
                self.bcoord[-1][1] = iw.curs.y
            if self.render : 
                self._drawto(lambda  :  self.buff.polygon(self.bcoord, outline = self.col, fill = None, width = 1) )
            else : 
                self._drawto(lambda  :  self.buff.line(self.bcoord, outline = self.col, fill = None, width = 1) )
            pass
        if self.showbuff is True : 
            if self.movebuff is True : 
                self.buff.blit(TUniSlector.copybuff, target = (iw.curs.x, iw.curs.y), mask = TUniSlector.buffmsk)
            pass




    def enabled(self, state = None):
        self.reset()
        TUniSlector.enabled(self, state)






class TMagicrod(TUniSlector, ) :


    __module__ = __name__
    def __init__(self, keyboard, buff, img, mes_callback):
        TUniSlector.__init__(self, keyboard, buff, img)
        self.coord = [(img.size[0] + 1), (img.size[1] + 1), -1, -1]
        self._fill_width = None
        self._fill_height = None
        self._fill_queue = None
        self.body = None
        self.mask = None
        self.message = mes_callback




    def _fill_check(self, img,gg, c, flabel):
        x, yu, yd =gg
        iu = yu
        getpixel = img.getpixel
        fqueue = self._fill_queue
        fheight = self._fill_height
        if iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c : 
            f = 0
        else : 
            f = 1
        while iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c : 
            iu -= 1
        iu += 1
        i = iu
        id = yu
        for id in xrange(yu, yd):
            if flabel[x][id] == 0 and getpixel((x, id))[0] == c : 
                if f : 
                    f = 0
                    i = id
                pass
            elif f == 0 : 
                fqueue += [(x, i, id)]
                f = 1
        if f == 0 : 
            while id < fheight and flabel[x][id] == 0 and getpixel((x, id))[0] == c : 
                id += 1
            fqueue += [(x, i, id)]
        self._fill_queue = fqueue
        flabel[x][iu : id] = ((id - iu) * [1])
        return flabel




    def mrod_select(self, img,gg, color, callback = None):
        x, y =gg
        self.coord = [(img.size[0] + 1), (img.size[1] + 1), -1, -1]
        msk = graphics.Image.new(img.size, 'L')
        msk.clear(0)
        self._fill_width, self._fill_height = img.size
        if 0 <= x < self._fill_width : 
            if  not (0 <= y < self._fill_height) : 
                return 0
            if type(color) == type(1) : 
                cr = (color / 65536)
                cg = ((color % 65536) / 256)
                cb = (color % 256)
                color = (cr, cg, cb)
            c = img.getpixel((x, y))[0]
            self._fill_queue = []
            flabel = []
            for i in xrange(self._fill_width):
                s = []
                for j in xrange(self._fill_height):
                    s += [0]
                flabel += [s]
            flabel = self._fill_check(img, (x, y, (y + 1)), c, flabel)
            while self._fill_queue : 
                x, yu, yd = self._fill_queue[0]
                self._fill_queue = self._fill_queue[1 : ]
                if callback : 
                    if callback() : 
                        return None
                    pass
                self.coord[0] = min(self.coord[0], x)
                self.coord[1] = min(self.coord[1], yu)
                self.coord[2] = max(self.coord[2], x)
                self.coord[3] = max(self.coord[3], yd)
                msk.line((x, yu, x, yd), color)
                flabel[x][yu : yd] = ((yd - yu) * [1])
                if x > 0 : 
                    flabel = self._fill_check(img, ((x - 1), yu, yd), c, flabel)
                if x < (self._fill_width - 1) : 
                    flabel = self._fill_check(img, ((x + 1), yu, yd), c, flabel)
            if callback : 
                callback()
            self.coord[2] += 1
            self.mask = graphics.Image.new(((self.coord[2] - self.coord[0]), (self.coord[3] - self.coord[1])), 'L')
            self.mask.blit(msk, source = self.coord)
            self.body = copy_image(self.mask)




        def eventcontrol(self, iw):
            if self.enbld is False : 
                return None
            if self.keybrd.freedown(key_codes.EScancodeSelect) : 
                if self.movebuff is True : 
                    self.movebuffer(False)
                    self._clippaste(iw)
                    self.render = False
                elif self.render is False : 
                    self.render = True
                    self.resetcol()
                    self.mrod_select(iw.img, (iw.curs.x + iw.imx, iw.curs.y + iw.imy), self.blend)
                elif self.render is True : 
                    self.render = False
                    self.moving = False
                pass




        def getimage(self, iw, blend):
            img = copy_image(self.mask)
            img.blit(iw.img, source = self.coord)
            return (img, self.mask)




        def invert_selection(self, iw):
            img, msk = self.getimage(iw, self.blend)
            self.mask = new_image(iw.img.size, 'L')
            filler = new_image(msk.size, 'L')
            filler.clear(0)
            self.mask.blit(filler, target = self.coord, mask = msk)
            self.body = copy_image(self.mask)
            self.coord = [0, 0, iw.img.size[0], iw.img.size[1]]
            return (iw.img, self.mask)




        def setimage(self, iw,gg):
            img, msk =gg
            iw.img.blit(img, target = self.coord, mask = msk)




        def getcoord(self):
            return self.coord




        def clipcopy(self, iw):
            TUniSlector.copybuff, TUniSlector.buffmsk = self.getimage(iw, self.blend)




        def clipcut(self, iw, col):
            iw._backupimage()
            self.clipcopy(iw)
            clearer = graphics.Image.new(TUniSlector.copybuff.size, mode = 'RGB16')
            clearer.clear(col)
            iw.img.blit(clearer, target = self.coord, mask = TUniSlector.buffmsk)




        def _clippaste(self, iw):
            iw._backupimage()
            iw.img.blit(TUniSlector.copybuff, target = ((iw.curs.x - iw.x) + iw.imx, (iw.curs.y - iw.y) + iw.imy), mask = TUniSlector.buffmsk)




        def clippaste(self, iw):
            self.render = False
            self.moving = False
            self.movebuffer(True)




        def clipclear(self, iw, col):
            iw._backupimage()
            img, msk = self.getimage(iw, self.blend)
            clearer = graphics.Image.new(img.size, mode = 'RGB16')
            clearer.clear(col)
            iw.img.blit(clearer, target = self.coord, mask = msk)




        def draw(self, iw):
            if self.enbld is False : 
                return None
            if self.render : 
                self.body.clear(self.col)
                self._drawto(lambda  :  self.buff.blit(self.body, target = ((self.coord[0] + iw.x - iw.imx), (self.coord[1] + iw.y - iw.imy)), mask = self.mask) )
            if self.showbuff is True : 
                if self.movebuff is True : 
                    self.buff.blit(TUniSlector.copybuff, target = (iw.curs.x, iw.curs.y), mask = TUniSlector.buffmsk)
                pass




        def enabled(self, state = None):
            TUniSlector.enabled(self, state)



