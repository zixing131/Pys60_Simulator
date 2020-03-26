#!/usr/bin/env python
# encoding: utf-8
# 如果觉得不错，可以推荐给你的朋友！http://tool.lu/pyc
import lloader
import appuifw
import graphics
import sys
from sysinfo import display_pixels
import key_codes
import e32
s60_version_info = e32.s60_version_info
from e32 import ao_sleep, Ao_lock, ao_yield, file_copy
from os import path, listdir, abort, stat, rename, remove, mkdir
from random import gauss, uniform
import iniparser
from langimp import lang_load, lang_readfromfile
import wt_ui
import wt_colormx
import wt_requester
import classes
from time import clock
import zlib
import struct
import SV_TRANS
import improc
import conf
import batch
import mbm
import kconfig
import traceback

__version__ = 1.4
_beta = 2
_version_ = u'%.2f ' % __version__
if _beta > 1:
    _version_ += u'beta %d\xe4\xb8\xad\xe6\x96\x87\xe7\x89\x88' % _beta

if path.exists('C:\\System\\Apps\\ImageDesigner\\palette.dat'):
    drive = 'c:\\'
else:
    drive = 'e:\\'
program_path = drive + 'System\\Apps\\ImageDesigner\\'
import os,sys
path1 = os.getcwd()
index = path1.rfind('\\')
mypath=path1[:index]
mypath2=path1+"\\ImageDesigner\\"
sys.path.append(mypath)
sys.path.append(mypath2)
program_path = mypath2
#sys.stderr = open(program_path + 'error.log', 'wt')
__selfmodlist__ = (
'improc', 'classes', 'wt_requester', 'wt_colormx', 'wt_ui', 'iniparser', 'langimp', 'SV_TRANS', 'conf', 'batch', 'mbm',
'kconfig')
for t in __selfmodlist__:

    try:
        if sys.modules[t].__version__ != __version__:
            appuifw.note(u'Incorect version of module: ' + unicode(t) + u'. Reinstall application.', 'error')
            abort()
    except:
        None
        None
        None
        appuifw.note(u'Incorect version of module: ' + unicode(t) + u'. Reinstall application.', 'error')
        abort()


def logout(par1, par2='', par3='', par4=''):
    print >> sys.stderr, par1, par2, par3, par4
    print >> sys.stderr, par1, par2, par3, par4


def redraw(a=None):
    pass


def new_image(size, mode='RGB16'):
    try:
        return graphics.Image.new(size, mode)
    except:
        None
        None
        None
        appuifw.note(dtext['e_lowmemory'], 'error')
        return None


def copy_image(img):
    im = new_image(img.size)
    if im is not None:
        im.blit(img)

    return im


class Keyboard(object):

    def __init__(self, onevent=(lambda: None)):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}
        self._onevent = onevent
        self.evt = {
            'keycode': None,
            'scancode': None,
            'type': None}

    def handle_event(self, event):
        self.evt = event
        self._downs = {}
        if event['type'] == appuifw.EEventKeyDown:
            self._state = event['scancode']
            if not self._keyboard_state.get(self._state, False):
                self._downs[self._state] = True

            self._keyboard_state[self._state] = True
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']] = False
            self._state = None

        if self._state is None:
            self._check = True

    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, False)

    def pressed(self, scancode):
        return self._downs.get(scancode, False)

    def state(self):
        return self._state

    def freedown(self, scancode):
        if self._check:
            if self._downs.get(scancode, False):
                self._check = False
                return True

        return False

    def keycode(self, code):
        if self.evt['keycode'] == code:
            return True

        return False

    def scancode(self, code):
        if self.evt['scancode'] == code:
            return True

        return False

    def resetkeys(self):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}


class TCursor:

    def __init__(self, canv, img, x, y, w, h, size=3):
        self.x = x
        self.y = y
        self.canv = canv
        self.img = img
        self.wx = x
        self.wy = y
        self.ww = w
        self.wh = h
        self.kind = 0
        self.size = size
        self.oldsize = None
        self.col = 0
        self.cold = 0
        self.hiden = False

    def draw(self, imx, imy):
        if self.hiden is True:
            return None

        if self.kind == 0:
            if self.size > 1:
                self.canv.rectangle((self.x - self.size - 2, self.y - 1, self.x + (self.size - 1), self.y + 2),
                                    16777215)
                self.canv.rectangle((self.x - 1, self.y - self.size - 2, self.x + 2, self.y + (self.size - 1)),
                                    16777215)

            self.canv.line((self.x - self.size - 1, self.y, self.x + self.size, self.y), 0)
            self.canv.line((self.x, self.y - self.size - 1, self.x, self.y + self.size), 0)
        elif self.kind == 1:
            if self.cold == 0:
                self.col += 15 * 65793
                if self.col > 16777215:
                    self.cold = 1
                    self.col = 16777215

            else:
                self.col -= 15 * 65793
                if self.col < 0:
                    self.cold = 0
                    self.col = 0

            self.canv.line((self.x - self.size - 1, self.y, self.x + self.size, self.y), self.col)
            self.canv.line((self.x, self.y - self.size - 1, self.x, self.y + self.size), self.col)
        elif self.kind == 2:
            for t in xrange(-(self.size - 1), self.size):
                col = self.img.getpixel((self.x + t + imx, self.y + imy))[0]
                col = (255 - col[0], 255 - col[1], 255 - col[2])
                self.canv.point((self.x + t, self.y), col)
                col = self.img.getpixel((self.x + imx, self.y + t + imy))[0]
                col = (255 - col[0], 255 - col[1], 255 - col[2])
                self.canv.point((self.x, self.y + t), col)

    def coord(self, cr=None):
        if cr is not None:
            if cr[0] is not None:
                self.x = cr[0]

            if cr[1] is not None:
                self.y = cr[1]

        else:
            return (self.x, self.y)

    def zone(self, sz=None):
        if sz is not None:
            if sz[0] is not None:
                self.wx = sz[0]
                self.x = sz[0]

            if sz[1] is not None:
                self.wy = sz[1]
                self.y = sz[1]

            if sz[2] is not None:
                self.ww = sz[2]

            if sz[3] is not None:
                self.wh = sz[3]

        else:
            return (self.wx, self.wy, self.ww, self.wh)

    def move(self, d, s):
        if d == 0:
            if self.x > self.wx:
                self.x -= s
                if self.x < self.wx:
                    self.x = self.wx

            else:
                return d
        elif d == 1:
            if self.x < self.wx + self.ww - 1:
                self.x += s
                if self.x > self.wx + self.ww - 1:
                    self.x = self.wx + self.ww - 1

            else:
                return d
        elif d == 2:
            if self.y > self.wy:
                self.y -= s
                if self.y < self.wy:
                    self.y = self.wy

            else:
                return d
        elif d == 3:
            if self.y < self.wy + self.wh - 1:
                self.y += s
                if self.y > self.wy + self.wh - 1:
                    self.y = self.wy + self.wh - 1

            else:
                return d

        return None


class TTool(object):

    def _define(self, buff, img):
        self.buff = buff
        self.img = img
        self.enbld = False
        self.render = False
        self.drawing = False

    def enabled(self, state=None):
        if state is not None:
            self.enbld = state
        else:
            return self.enbld


class TGraphtool(TTool):

    def __init__(self, buff, img, tool):
        TTool._define(self, buff, img)
        self.coord = [
            0,
            0,
            0,
            0]
        self.bcoord = [
            0,
            0,
            0,
            0]
        self.tool = tool
        self.easydraw = False

    def _drawto(self, canv, coord, iw):
        if self.tool == 0:
            line(canv, coord, outline=foreclr, width=iw.bsize)
        elif self.tool == 1:
            rect(canv, coord, outline=foreclr, fill=backclr, width=iw.bsize)
        elif self.tool == 2:
            ellps(canv, coord, outline=foreclr, fill=backclr, width=iw.bsize)

    def eventcontrol(self, evt, iw):
        if self.enbld is False and not (toolslist.hdn) or not (colorgrid.hdn):
            return None

        if keyboard.pressed(key_codes.EScancodeSelect):
            self.drawing = not (self.drawing)
            if self.drawing is True:
                self.coord = [
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy,
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy]
                self.bcoord = [
                    iw.curs.x,
                    iw.curs.y,
                    iw.curs.x,
                    iw.curs.y]
                self.render = False
            else:
                self.coord[-2:] = [
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy]
                self.bcoord = [
                    self.coord[0] - iw.imx,
                    self.coord[1] - iw.imy,
                    iw.curs.x,
                    iw.curs.y]
                self.render = True

    def draw(self, iw):
        if self.enbld is False:
            return None

        if self.drawing is True:
            if self.easydraw is False:
                xx = iw.curs.x
                yy = iw.curs.y
            else:
                x = iw.curs.x - self.coord[0] - iw.imx
                y = iw.curs.y - self.coord[1] - iw.imy
                xx = max(x, y) + (self.coord[0] - iw.imx)
                yy = max(x, y) + (self.coord[1] - iw.imy)
            self.bcoord = [
                self.coord[0] - iw.imx,
                self.coord[1] - iw.imy,
                xx,
                yy]
            self._drawto(self.buff, self.bcoord, iw)

        if self.render is True:
            self.render = False
            self._drawto(iw.img, self.coord, iw)

    def enabled(self, state=None):
        if state is False and self.drawing is True:
            self.drawing = state
            self.render = state

        if state is not None:
            self.enbld = state
        else:
            return self.enbld


class Controllable:
    focusedon = None

    def setfocusto(instance):
        focusedon = instance

    setfocusto = staticmethod(setfocusto)

    def getfocused():
        return focusedon

    getfocused = staticmethod(getfocused)

    def activate(self):
        Controllable.setfocusto(self)

    def isactive(self):
        return self == Controllable.getfocused()


class TImageWindow:

    def __init__(self, img, canv, x, y, w, h):
        self.name = ''
        self.filename = None
        self.frmt = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.imx = 0
        self.imy = 0
        self.old_imx = 0
        self.old_imy = 0
        self.blckd = False
        self.hdn = False
        self.img = img
        self.editsize = [
            w,
            h]
        self.canv = canv
        self.undostack = [
            None]
        self.redostack = [
            None]
        self.undosize = 1
        self.objx = x
        self.objy = y
        self.obj = 0
        self.obj_text = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
        self.obj_point = []
        if s60_version_info == (3, 0):
            self.obj_font = (appuifw.available_fonts()[0], 14)
        else:
            self.obj_font = appuifw.available_fonts()[0]
        self.drawing = False
        self.bsize = 1
        self.ersize = 8
        self.sbx = 0
        self.sby = 0
        self.sbt = 0
        self.moving = None
        self.move_step = 0
        self.cursor_ptime = 0
        self.cursor_speedid = 0
        self.cursor_delayscount = len(con.curs_del)
        self.zoom = 1
        self.scale = False
        self.curs = TCursor(canv, img, self.x, self.y, self.w, self.h)
        self.keyboard = Keyboard()
        self.lastfile = None
        self.navigation = False
        self.imagemodified = False
        self.selector = classes.TSelectorTool(keyboard, canv, img, self, mbox_percent)
        self.waitpickerchoose = False
        self.pickercallback = None

    def destruct(self):
        del self.curs
        del self.selector
        del self.keyboard

    def draw(self):
        if self.hdn is False:
            self.canv.blit(self.img, target=(self.x, self.y),
                           source=(self.imx, self.imy, self.imx + self.w, self.imy + self.h), scale=False)
            if self.drawing is True:
                self.draw_object(self.canv)

            if self.drawing is True and self.obj == tool['paintbrush']:
                self.draw_object(self.img, self.imx, self.imy)
            elif self.obj == tool['eraser'] or self.obj == tool['text']:
                self.draw_object(self.canv)
            elif self.drawing is True and self.obj == tool['spray']:
                self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
            elif self.obj == tool['templet']:
                self.draw_object(self.canv)

            self.selector.draw()
            self.curs.draw(self.imx, self.imy)

    def setundosize(self, size):
        self.undosize = size
        u = self.undostack[:]
        r = self.redostack[:]
        #continue
        self.undostack = [None for x in xrange(self.undosize)]
        #continue
        self.redostack = [None for x in xrange(self.undosize)]
        self.undostack.extend(u)
        self.undostack = self.undostack[len(u):]
        self.redostack.extend(r)
        self.redostack = self.redostack[len(r):]

    def _backupimage(self):
        self.imagemodified = True
        if self.undosize != 0:
            buff = copy_image(self.img)
            if buff is not None:
                buff.blit(self.img)
                self.undostack.pop(0)
                self.undostack.append(buff)

    def undo(self):
        if self.undostack[-1] is None:
            return None

        buff = self.undostack.pop()
        self.undostack.insert(-1, None)
        if buff is not None:
            self.redostack.pop(0)
            self.redostack.append(copy_image(self.img))
            self.img.blit(buff)

    def redo(self):
        if self.redostack[-1] is None:
            return None

        buff = self.redostack.pop()
        self.redostack.insert(-1, None)
        if buff is not None:
            self.undostack.pop(0)
            self.undostack.append(copy_image(self.img))
            self.img.blit(buff)

    def brushsize(self, size=None):
        if size is not None:
            self.bsize = size

        return self.bsize

    def draw_object(self, canv, dx=0, dy=0, opt=None):
        if self.obj == tool['pencil']:
            canv.point([
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)

        if self.obj == tool['paintbrush']:
            line(canv, [
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['eraser']:
            if opt == 0:
                rect(canv, [
                    self.curs.x + dx,
                    self.curs.y + dy,
                    self.curs.x + self.ersize + dx,
                    self.curs.y + self.ersize + dy], outline=backclr, fill=backclr, width=1)
            else:
                rect(canv, [
                    self.curs.x + dx,
                    self.curs.y + dy,
                    self.curs.x + self.ersize + dx,
                    self.curs.y + self.ersize + dy], outline=0, fill=16777215, width=1)
        elif self.obj == tool['text']:
            if bmpfont is None:
                canv.text([
                    self.curs.x + dx,
                    self.curs.y + dy], self.obj_text, fill=foreclr, font=self.obj_font)
            elif fontbuff is not None:
                canv.blit(fontbuff, target=(self.curs.x + dx, self.curs.y + dy), mask=fontbuffmsk)

        elif self.obj == tool['polygon']:
            canv.line([
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['brokenline']:
            canv.line([
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['spray']:
            x = self.curs.x + dx
            y = self.curs.y + dy
            sigma = self.bsize
            for t in xrange(3):
                canv.point([
                    gauss(x + 1, sigma),
                    gauss(y + 1, sigma)], outline=foreclr, width=1)

        elif self.obj == tool['polygon_']:
            point = self.obj_point
            for t in xrange(len(point)):
                point[t][0] += dx
                point[t][1] += dy

            canv.polygon(point, outline=foreclr, fill=backclr, width=self.bsize)
        elif self.obj == tool['templet']:
            if templet is not None:
                templet_draw(canv, self.curs.x + dx, self.curs.y + dy)

    def param(self, x=None, y=None, w=None, h=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if w is not None:
            self.w = w

        if h is not None:
            self.h = h

        if x is None and y is None and w is None and h is None:
            return [
                self.x,
                self.y,
                self.w,
                self.h]

    def image_coord(self, x=None, y=None):
        if x is not None:
            self.imx = x

        if y is not None:
            self.imy = y

        if x is None and y is None:
            return (self.imx, self.imy)

    def image_correctcoord(self):
        x = self.imx
        y = self.imy
        if self.imx < 0:
            self.imx = 0

        if self.imy < 0:
            self.imy = 0

        if self.imx > self.img.size[0] - self.w:
            self.imx = self.img.size[0] - self.w

        if self.imy > self.img.size[1] - self.h:
            self.imy = self.img.size[1] - self.h

        return (x - self.imx, y - self.imy)

    def coord(self, cr=None):
        if cr is not None:
            if cr[0] is not None:
                self.x = cr[0]

            if cr[1] is not None:
                self.y = cr[1]

            self.curs.zone((self.x, self.y, self.w, self.h))
        else:
            return (self.x, self.y)

    def size(self, sz=None, edz=True):
        if sz is not None:
            if sz[0] is not None:
                self.w = sz[0]

            if sz[1] is not None:
                self.h = sz[1]

            if edz is True:
                self.editsize = [
                    self.w,
                    self.h]

            self.curs.zone((self.x, self.y, self.w, self.h))
        else:
            return (self.w, self.h)

    def image_move(self, d, s):
        if d == 0:
            if self.imx > 0:
                self.imx -= s
                if self.imx < 0:
                    self.imx = 0


        elif d == 1:
            if self.imx < self.img.size[0] - self.w:
                self.imx += s
                if self.imx > self.img.size[0] - self.w:
                    self.imx = self.img.size[0] - self.w


        elif d == 2:
            if self.imy > 0:
                self.imy -= s
                if self.imy < 0:
                    self.imy = 0


        elif d == 3:
            if self.imy < self.img.size[1] - self.h:
                self.imy += s
                if self.imy > self.img.size[1] - self.h:
                    self.imy = self.img.size[1] - self.h

        return None

    def cursor_move(self, d, s=1):
        if self.curs.move(d, s) is not None:
            self.image_move(d, s)

    def cursor_hiden(self, state=None):
        if state is not None:
            self.curs.hiden = state

        return self.curs.hiden

    def hiden(self, hd=None):
        if hd is not None:
            self.hdn = hd
            if self.hdn is True:
                self.blckd = True
            else:
                self.blckd = False

        return self.hdn

    def blocked(self, state=None):
        if state is not None:
            self.blckd = state

        return self.blckd

    def navigation_switch(self):
        self.navigation = not (self.navigation)
        if self.navigation is True:
            self.old_imx = self.imx
            self.old_imy = self.imy
            self.cursor_hiden(True)
            showtipex(dtext['navigation'])
        else:
            self.imx = self.old_imx
            self.imy = self.old_imy
            self.cursor_hiden(False)
            showtipex(dtext['edit'])

    def _cursor_move(self, d):
        self.cursor_ptime += 1
        if self.cursor_ptime > con.curs_del[self.cursor_speedid]:
            if self.cursor_speedid < con.curs_lastdelind:
                self.cursor_speedid += 1

        if self.cursor_speedid != 0:
            self.move_step = con.curs_step[self.cursor_speedid]

        self.cursor_move(d, self.move_step)
        self.moving = True
        self.move_step = 0

    def navigationcontrol(self, evt=None):
        if self.blckd is False:
            if self.navigation is True:
                if keyboard.is_down(key_codes.EScancodeLeftArrow):
                    self.image_move(0, 10)
                elif keyboard.is_down(key_codes.EScancodeRightArrow):
                    self.image_move(1, 10)
                elif keyboard.is_down(key_codes.EScancodeUpArrow):
                    self.image_move(2, 10)
                elif keyboard.is_down(key_codes.EScancodeDownArrow):
                    self.image_move(3, 10)

                if keyboard.is_down(key_codes.EScancodeSelect):
                    self.navigation = False
                    self.cursor_hiden(False)
                    showtipex(dtext['edit'])

            elif not keyboard.is_down(key_codes.EScancodeLeftArrow) and not keyboard.is_down(
                    key_codes.EScancodeRightArrow) and not keyboard.is_down(
                    key_codes.EScancodeUpArrow) and not keyboard.is_down(key_codes.EScancodeDownArrow):
                self.move_step = 1
                self.cursor_ptime = 0
                self.cursor_speedid = 0
                self.moving = False
                if self.obj == tool['paintbrush'] and self.drawing is True:
                    self.objx = self.curs.x
                    self.objy = self.curs.y
                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

            if keyboard.is_down(key_codes.EScancodeLeftArrow):
                self._cursor_move(0)

            if keyboard.is_down(key_codes.EScancodeRightArrow):
                self._cursor_move(1)

            if keyboard.is_down(key_codes.EScancodeUpArrow):
                self._cursor_move(2)

            if keyboard.is_down(key_codes.EScancodeDownArrow):
                self._cursor_move(3)

    def keyboardevent(self, evt=None):
        global foreclr
        if self.blckd is False:
            if self.navigation is False:
                self.selector.control()
                if keyboard.freedown(key_codes.EScancodeSelect):
                    if self.obj != tool['pencil'] and self.obj != tool['picker'] and self.obj != tool[
                        'eraser'] and self.obj != tool['templet'] and self.obj != tool['polygon_']:
                        self.drawing = not (self.drawing)
                        if self.drawing is True:
                            self.objx = self.curs.x
                            self.objy = self.curs.y
                            if self.obj == tool['paintbrush'] or self.obj == tool['spray']:
                                self._backupimage()

                        elif self.drawing is False:
                            if self.obj == tool['brokenline']:
                                self._backupimage()
                                if self.objx == self.curs.x and self.objy == self.curs.y:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                else:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.objx = self.curs.x
                                    self.objy = self.curs.y
                                    self.drawing = not (self.drawing)
                            elif self.obj == tool['polygon']:
                                self._backupimage()
                                if self.objx == self.curs.x and self.objy == self.curs.y:
                                    self.obj_point.append([
                                        self.objx,
                                        self.objy])
                                    self.obj = tool['polygon_']
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.obj_point = []
                                    self.obj = tool['polygon']
                                else:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.obj_point.append([
                                        self.objx,
                                        self.objy])
                                    self.objx = self.curs.x
                                    self.objy = self.curs.y
                                    self.drawing = not (self.drawing)
                            elif self.obj != tool['paintbrush'] and self.obj != tool['spray']:
                                self._backupimage()
                                self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)


                    elif self.obj != tool['paintbrush'] and self.obj != tool['spray'] and self.obj != tool['pencil']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['pencil']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['picker']:
                        c = self.img.getpixel(((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy))[0]
                        c = 256 * 256 * c[0] + 256 * c[1] + c[2]
                        foreclr = c
                        if self.waitpickerchoose is True:
                            if callable(self.pickercallback):
                                self.waitpickerchoose = False
                                self.pickercallback()
                                self.pickercallback = None

                    if self.obj == tool['paintbucket']:
                        self._backupimage()
                        canv.clear(10066329)
                        fillimage(self.img, ((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy),
                                  foreclr, (lambda: canv.blit(imwin.img)))

                    if self.obj == tool['magicrod']:
                        self._backupimage()
                        canv.clear(10066329)
                        mrod_select(self.img, ((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy),
                                    foreclr, (lambda: canv.blit(imwin.img)))

                    if self.obj == tool['eraser']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy, 0)

                    if self.obj == tool['text']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['templet']:
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        if templet is not None:
                            self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                if keyboard.pressed(key_codes.EScancodeBackspace):
                    if self.drawing is True:
                        if self.obj == tool['brokenline']:
                            self.drawing = False
                        elif self.obj == tool['polygon']:
                            self.obj_point.append([
                                self.objx,
                                self.objy])
                            self.objx = self.curs.x
                            self.objy = self.curs.y
                            self.obj = tool['polygon_']
                            self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                            self.obj_point = []
                            self.obj = tool['polygon']
                            self.drawing = False

                        if self.obj == tool['brokenline']:
                            self.drawing = False


def setblend():
    global blendval
    val = appuifw.query(dtext['blend'], 'number', 100 - inttorgb(blendval)[0] * 100 / 255)
    if val is None:
        return None

    if val > 100 or val < 0:
        appuifw.note(dtext['badvalue'], 'error')

    val = 255 - val * 255 / 100
    blendval = rgbtoint((val, val, val))
    imwin.selector.setblend(blendval)


def clipcopy():
    imwin.selector.clipcopy()


def clippaste():
    imwin.selector.clippaste()


def clipcut():
    imwin.selector.clipcut(backclr)


def clipclear():
    imwin.selector.clipclear(backclr)


def selectall():
    global curtool
    tool_line.enabled(False)
    tool_rect.enabled(False)
    tool_ellps.enabled(False)
    toolslist.curitem((0, 6))
    curtool = tool['selector']
    imwin.obj = tool['selector']
    imwin.drawing = False
    imwin.selector.selectall()


def selectsize():
    w = appuifw.query(dtext['width'], 'number', con.screen_size[0])
    if w is None:
        return None

    w -= 1
    if w > imwin.img.size[0]:
        w = imwin.img.size[0]
    elif w < 1:
        w = 1

    h = appuifw.query(dtext['height'], 'number', con.screen_size[1])
    if h is None:
        return None

    h -= 1
    if h > imwin.img.size[1]:
        h = imwin.img.size[1]
    elif h < 1:
        h = 1

    toolslist.curitem((0, 6))
    tools_set()
    x = -(imwin.x) + imwin.imx + imwin.curs.x
    y = -(imwin.y) + imwin.imy + imwin.curs.y
    imwin.selector.set(0)
    imwin.selector.tool.setcoord((x, y, x + w, y + h))
    imwin.selector.tool.fixselection()
    imwin.selector.tool.moving = True


def brush_size():
    if imwin.obj == tool['selector']:
        selectsize()
    elif imwin.obj == tool['text']:
        text = appuifw.query(dtext['entertext'], 'text', imwin.obj_text)
        if text is not None:
            imwin.obj_text = text
            font_updatemess(text)

    elif imwin.obj == tool['eraser']:
        size = appuifw.query(dtext['brushsize'], 'number', imwin.ersize)
        if size is not None:
            imwin.ersize = size

    else:
        size = appuifw.query(dtext['brushsize'], 'number', imwin.brushsize())
        if size is not None:
            imwin.brushsize(size)


def settext():
    text = appuifw.query(dtext['entertext'], 'text', imwin.obj_text)
    if text is not None:
        imwin.obj_text = text
        font_updatemess(text)


def rect(canv, cr, outline=None, fill=None, width=1, pattern=None):
    if cr[0] != cr[2] and cr[1] != cr[3]:
        canv.rectangle([
            min(cr[0], cr[2]),
            min(cr[1], cr[3]),
            max(cr[0], cr[2]) + 1,
            max(cr[1], cr[3]) + 1], outline, fill, width)
    else:
        line(canv, [
            cr[0],
            cr[1],
            cr[2],
            cr[3]], outline=outline, width=width)


def softrect(canv, _2, outline=0, fill=16777215, width=1, corner=1):
    (x, y, x1, y1) = _2
    canv.polygon(((x + corner, y), (x, y + corner), (x, y1 - corner), (x + corner, y1), (x1 - corner, y1),
                  (x1, y1 - corner), (x1, y + corner), (x1 - corner, y)), outline=outline, fill=fill, width=width)


def ellps(canv, cr, outline=None, fill=None, width=1, pattern=None):
    if cr[0] != cr[2] and cr[1] != cr[3]:
        canv.ellipse([
            min(cr[0], cr[2]),
            min(cr[1], cr[3]),
            max(cr[0], cr[2]),
            max(cr[1], cr[3])], outline, fill, width)
    else:
        line(canv, [
            cr[0],
            cr[1],
            cr[2],
            cr[3]], outline=outline, width=width)


def line(can, cr, outline, width):
    can.line([
        cr[0],
        cr[1],
        cr[2],
        cr[3]], outline=outline, width=width)
    can.point((cr[2], cr[3]), outline=outline, width=width)


def parameters_save():
    global paramtuple
    paramtuple = (
    appuifw.app.screen, appuifw.app.body, appuifw.app.menu, appuifw.app.title, appuifw.app.exit_key_handler)


def parameters_restore():
    appuifw.app.screen = paramtuple[0]
    appuifw.app.body = paramtuple[1]
    appuifw.app.menu = paramtuple[2]
    appuifw.app.title = paramtuple[3]
    appuifw.app.exit_key_handler = paramtuple[4]


def help():
    parameters_save()
    appuifw.app.title = dtext['help']
    appuifw.app.screen = 'normal'
    appuifw.app.body = appuifw.Text()
    t = appuifw.Text()

    appuifw.app.exit_key_handler = lambda: parameters_restore()
    readfile(t, 'help.txt')
    appuifw.app.menu = [
        (dtext['help'], (lambda: readfile(t, 'help.txt'))),
        (dtext['license'], (lambda: readfile(t, 'license.txt'))),
        (dtext['history'], (lambda: readfile(t, 'history.txt'))),
        (dtext['close'], (lambda: parameters_restore()))]


def readfile(t, name):
    hf = open(program_path + name)
    txt = hf.read()
    hf.close()
    t.clear()
    t.font = con.ui_menu_font
    t.add(ru(txt))
    t.set_pos(0)


def switchhelp(state=None):
    global showhlp
    if state is None:
        showhlp = not showhlp
    else:
        showhlp = state


def tools_set():
    global curtool
    curtool = toolslist.curitem()[0] * len(tool) / 2 + toolslist.curitem()[1]
    imwin.obj = curtool
    imwin.drawing = False
    imwin.selector.set(None)
    if curtool == tool['line']:
        tool_line.enabled(True)
    else:
        tool_line.enabled(False)
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)

    if curtool == tool['rectangle']:
        tool_rect.enabled(True)
    else:
        tool_rect.enabled(False)
    if curtool == tool['ellipse']:
        tool_ellps.enabled(True)
    else:
        tool_ellps.enabled(False)
    if curtool == tool['text']:
        font_updatemess(imwin.obj_text)

    if curtool == tool['stamp']:
        appuifw.note(u'Work in progress:)')
        appuifw.note(u'Work in progress:)')


def swap_colors():
    global foreclr, backclr
    if backclr is not None:
        c = foreclr
        foreclr = backclr
        backclr = c


def color_set(state=None):
    global foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr
    (indx, indy) = colorgrid.curitem()
    if indy == 0:
        if indx == 0:
            c = query_rgb(dtext['outlinecolor'], foreclr)
            if c is not None:
                foreclr = c

        elif indx == 2:
            c = query_rgb(dtext['fillcolor'], backclr)
            if c is not None:
                backclr = c

        elif indx == 1:
            swap_colors()
        elif indx == 3:
            foreclr = 0
            backclr = 16777215
        elif indx == 5:
            backclr = None
        elif indx > 5:
            if con.custompal[indx - 6] != '':
                if _palette_load(program_path + 'Palette\\' + con.custompal[indx - 6]):
                    colorload()
                    palette_update()

    if indy == 0 and indx == 4:
        if state == 0:
            foreclr = 0
        elif state == 1:
            backclr = 0

    if indy != 0:
        if state == 0:
            foreclr = col[indx][indy]
        elif state == 1:
            backclr = col[indx][indy]

        if fontbuff is not None:
            fontbuff.clear(foreclr)


def _setforecolor():
    global foreclr
    foreclr = col[colorgrid.curitem()[0]][colorgrid.curitem()[1]]


def _setbackcolor():
    global backclr
    backclr = col[colorgrid.curitem()[0]][colorgrid.curitem()[1]]


def palette_createcell():
    size = 12
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            col[n].append(16777215)
            colors[n].append(new_image((size, size)))


def palette_update():
    c = colors
    icon = colorgrid.icon
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            icon((n, t), c[n][t])


def palette_reset():
    colorgen()
    palette_update()


def palette_save():
    _palette_save(program_path + 'palette.dat')


def palette_load():
    return _palette_load(program_path + 'palette.dat')


def palette_export():
    global lastpath_pal
    dirpath = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'save')
    if dirpath is None:
        return None

    if path.isfile(ur(dirpath)):
        defname = path.split(dirpath)[1]
        dirpath = path.split(dirpath)[0] + '\\'
    else:
        defname = u'ID_palette'
    dirpath = dirpath.replace('\\\\', '\\')
    lastpath_pal = dirpath
    name = appuifw.query(dtext['entername'], 'text', defname)
    if name is None:
        return None

    if name[-4:].lower() != '.dat':
        name = name + '.dat'

    _palette_save(dirpath + name)
    appuifw.note(dtext['palsavedas'] + name)


def palette_import():
    global lastpath_pal
    filename = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'open')
    if filename is None:
        return None

    lastpath_pal = path.split(filename)[0]
    if _palette_load(filename):
        colorload()
        palette_update()
    else:
        appuifw.note(dtext['palbroken'], 'error')


def palette_setcustom(i, filename):
    path = program_path + 'Palette\\' + filename
    if _palette_load(path):
        palette_checkcustom(i, filename)
    else:
        appuifw.note(dtext['palbroken'], 'error')


def palette_checkcustom(i, filename):
    folder = program_path + 'Palette\\' + filename
    if path.exists(folder):
        con.custompal[i] = filename
        colorgrid.icon((i + 6, 0), image_n[i])
    else:
        appuifw.note(dtext['palnotexist'], 'error')
        palette_clearcustom()


def palette_selectcustom():
    global lastpath_pal
    filename = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'open')
    if filename is None:
        return None

    name = path.split(filename)[1]
    lastpath_pal = path.split(filename)[0]
    palette_setcustom(colorgrid.curitem()[0] - 6, name)


def palette_clearcustom():
    i = colorgrid.curitem()[0] - 6
    con.custompal[i] = ''
    colorgrid.icon(colorgrid.curitem(), image_w)


def _palette_save(path):
    f = open(path, 'wt')
    for x in xrange(0, palette_size[0]):
        for y in xrange(0, palette_size[1]):
            if x == palette_size[0] - 1 and y == palette_size[1] - 1:
                delim = ''
            else:
                delim = ','
            if col[x][y] is not None:
                c = col[x][y]
                f.write(str(c) + delim)
            else:
                f.write(str(16777215) + delim)

    f.close()


def _palette_load(path):
    try:
        f = open(path, 'rt')
        line = f.readline()
        clist = line.split(',')
        #continue
        colorlist = [int(v) for v in clist]
        for x in xrange(0, palette_size[0]):
            for y in xrange(1, palette_size[1]):
                col[x][y] = colorlist[y + x * palette_size[1]]

        f.close()
        return True
    except:
        None
        None
        None
        appuifw.note(dtext['palbroken'], 'error')
        return False


def palette_setcell():
    size = 12
    col[colorgrid.curitem()[0]][colorgrid.curitem()[1]] = foreclr
    im = new_image((size, size))
    im.rectangle((0, 0, size, size), outline=0, fill=0)
    im.rectangle((1, 0, size, size - 1), outline=foreclr, fill=foreclr)
    colorgrid.icon(colorgrid.curitem(), im)


def colormixer():
    parameters_save()
    cc = wt_colormx.init(col[colorgrid.curitem()[0]][colorgrid.curitem()[1]], mtext)
    if cc is not None:
        c = 256 * 256 * cc[0] + 256 * cc[1] + cc[2]
        size = 12
        im = new_image((size, size))
        im.rectangle((0, 0, size, size), outline=0, fill=0)
        im.rectangle((1, 0, size, size - 1), outline=c, fill=c)

        try:
            if colorgrid.curitem()[1] != 0:
                colorgrid.icon(colorgrid.curitem(), im)
                col[colorgrid.curitem()[0]][colorgrid.curitem()[1]] = c
        except:
            None
            None
            None
            running = 0

    parameters_restore()


def scrollbar_resize():
    scrollbar_imw[0].maxvalue(imwin.img.size[0])
    scrollbar_imw[1].maxvalue(imwin.img.size[1])
    scrollbar_imw[0].screenvalue(workzone[0])
    scrollbar_imw[1].screenvalue(workzone[1])


def scrollbar_update():
    maxx = imwin.img.size[0] - imwin.w
    maxy = imwin.img.size[1] - imwin.h
    if maxx > 0:
        scrollbar_imw[0].percent(imwin.imx * 100 / maxx)

    if maxy > 0:
        scrollbar_imw[1].percent(imwin.imy * 100 / maxy)


def scrollbar_draw():
    if imwin.img.size[0] * imwin.zoom > workzone[0]:
        scrollbar_imw[0].draw()

    if imwin.img.size[1] * imwin.zoom > workzone[1]:
        scrollbar_imw[1].draw()


def tools_update(evt):
    if not (gradgrid.blckd):
        if keyboard.pressed(key_codes.EScancodeSelect):
            image_gradient(gradgrid.curindex())

    if not (colorgrid.blckd):
        if keyboard.freedown(key_codes.EScancodeSelect):
            onnextcicle_do((lambda: color_set(0)))

        if keyboard.freedown(key_codes.EScancode5):
            onnextcicle_do((lambda: color_set(1)))


def grid_palette_onhide(state=None):
    imwin.blocked(False)
    wt_ui.Tsysmenu.setcurrent(0, mainmenu)
    wt_ui.Tsysmenu.setcurrent(1, popupmenu)
    onnextcicle_do(con.keyconfig.hotkeys_on)


def grid_palette_onshow(state=None):
    imwin.blocked(True)
    wt_ui.Tsysmenu.setcurrent(0, menu_palette)
    con.keyconfig.hotkeys_off()


def grid_palette_onchangeitem():
    (indx, indy) = colorgrid.curitem()
    if indy == 0:
        if indx > 5:
            wt_ui.Tsysmenu.setcurrent(0, menu_palette2)
        else:
            wt_ui.Tsysmenu.setcurrent(0, menu_palette3)
    else:
        wt_ui.Tsysmenu.setcurrent(0, menu_palette)


def exit():
    global running
    if con.exitconfirm:
        ans = appuifw.query(dtext['exitconf'], 'query')
        if ans is None:
            return None

    try:
        mbox_percent.draw(dtext['saving'])
        redraw_main()
        con.save(program_path + 'config.ini')
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(u"Can't write to config.ini")

    try:
        palette_save()
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(u"Can't write to palette.dat")

    running = 0

    try:
        appuifw.app.set_exit()
    finally:
        sys.stderr.close()
        abort()


def message(buff, cr, col):
    if gtext is not None:
        buff.text(cr, gtext, col)


def redraw_main(clear=True):
    buff.clear(con.ui_form_color[2])
    imwin.draw()
    tool_line.draw(imwin)
    tool_rect.draw(imwin)
    tool_ellps.draw(imwin)
    if imwin.zoom > 1:
        zoombuff.blit(buff, source=zoomzone, scale=1)
        buff.blit(zoombuff)

    statusbar()
    scrollbar_draw()
    toolslist.draw(buff)
    colorgrid.draw(buff)
    gradgrid.draw(buff)
    wt_ui.Tsysmenu.draw()
    menu_selection.draw()
    mess_info.draw()
    mess_tip.draw()
    canv.blit(buff)


def redraw_about():
    if menu_about.ciclecount == 2:
        menu_about.ciclecount = 3
        menu_about.message(mess_eegg, con.ui_menu_font)
    elif menu_about.ciclecount == 0:
        if len(menu_about.mess[7]) != 27:
            abort()

    buff.clear(con.ui_form_color[2])
    menu_about.draw()
    canv.blit(buff)


def redraw_start():
    buff.clear(con.ui_form_color[2])
    menu_start.draw()
    canv.blit(buff)


def redraw_preview():
    buff.clear(con.ui_form_color[2])
    buff.blit(prev_image, target=prev_coord, scale=0)
    wt_ui.Tsysmenu.draw()
    canv.blit(buff)


def event_main(evt):
    global kevent
    kevent = wt_ui.Tsysmenu.control(evt)
    menu_selection.control(evt)
    imwin.keyboardevent()
    if main_event_proc:
        keyboard.handle_event(kevent)
        tools_update(kevent)
        wt_ui.Ticongrid.showcontrol(kevent)
        tool_line.eventcontrol(kevent, imwin)
        tool_rect.eventcontrol(kevent, imwin)
        tool_ellps.eventcontrol(kevent, imwin)
    elif not menu_about.hiden():
        menu_about.control(kevent)
    elif not mess_info.hiden():
        mess_info.control(kevent)
    elif not preview_exit:
        preview_control(kevent)


def imwindow_center():
    if imwin.img.size[0] < workzone[0]:
        x = (workzone[0] - imwin.img.size[0]) / 2

    if imwin.img.size[1] < workzone[1]:
        y = (workzone[1] - imwin.img.size[1]) / 2

    imwin.coord((x, y))
    imwin.curs.coord((0, 0))


def imwindow_saveparam():
    global temp_imwinpar
    temp_imwinpar = []
    if imwin is not None:
        temp_imwinpar.append(imwin.obj)
        temp_imwinpar.append(imwin.bsize)
        temp_imwinpar.append(imwin.curs.kind)
        temp_imwinpar.append(imwin.curs.size)
        temp_imwinpar.append(foreclr)
        temp_imwinpar.append(backclr)
        temp_imwinpar.append(imwin.undosize)
        temp_imwinpar.append(imwin.selector.get())


def imwindow_restoreparam():
    global foreclr, backclr, temp_imwinpar
    if len(temp_imwinpar) > 0:
        imwin.obj = temp_imwinpar[0]
        imwin.bsize = temp_imwinpar[1]
        imwin.curs.kind = temp_imwinpar[2]
        imwin.curs.size = temp_imwinpar[3]
        foreclr = temp_imwinpar[4]
        backclr = temp_imwinpar[5]
        imwin.undosize = temp_imwinpar[6]
        imwin.setundosize(imwin.undosize)
        imwin.selector.set(temp_imwinpar[7])
        temp_imwinpar = []
        if curtool == tool['selector']:
            imwin.selector.set(0)
        elif curtool == tool['elselector']:
            imwin.selector.set(1)
        elif curtool == tool['lasso']:
            imwin.selector.set(2)
        elif curtool == tool['magicrod']:
            imwin.selector.set(3)


def imwindow_new(image, win=None, restore=True):
    global editzone, scrollbar_imw, imwin, curwin
    x = 0
    y = 0
    editzone = [
        workzone[0],
        workzone[1]]
    scrollbar_imw = [
        None,
        None]
    if image.size[0] < workzone[0]:
        editzone[0] = image.size[0]

    scrollbar_imw[0] = wt_ui.Tbar(0, workzone[1], con.screen_size[0] - scrollbarwidth, workzone[1] + scrollbarwidth,
                                  (0, image.size[0]), workzone[0], buff, False)
    if image.size[1] < workzone[1]:
        editzone[1] = image.size[1]

    scrollbar_imw[1] = wt_ui.Tbar(workzone[0], 0, con.screen_size[0], workzone[1], (0, image.size[1]), workzone[1],
                                  buff, True)
    scrollbar_imw[0].color(con.ui_form_color[3])
    scrollbar_imw[1].color(con.ui_form_color[3])
    if restore is True:
        imwindow_saveparam()

    if imwin and not win:
        imwin.destruct()

    imwin = TImageWindow(image, buff, x, y, editzone[0], editzone[1])
    imwin.selector.setcallback((lambda: menu_selection.hiden(False)))
    del image
    if win is True:
        imagewindow.append(imwin)
        imwin.name = unicode(len(imagewindow))
        curwin = len(imagewindow) - 1
    elif len(imagewindow) == 0:
        imagewindow.append(None)

    imagewindow[curwin] = imwin
    imwin.name = unicode(curwin + 1)
    if restore is True:
        imwindow_restoreparam()

    return imwin


def imwindow_clone():
    imwindow_new(imwin.img, True, True)


def imwindow_copy():
    imwindow_new(copy_image(imwin.img), True, True)


def imwindow_close(win=None):
    global imwin, curwin, imwin, curwin
    if win is None:
        if len(imagewindow) > 1:
            if curwin == len(imagewindow) - 1:
                cwin = curwin - 1
            else:
                cwin = curwin
            del imagewindow[curwin]
            imwin.destruct()
            imwin = imagewindow[cwin]
            curwin = cwin
            if imwin.zoom > 1:
                zoom_multiply(imwin.zoom)


    elif win > 0 and win < len(imagewindow):
        if len(imagewindow) > 1:
            if curwin == len(imagewindow) - 1:
                cwin = curwin - 1
            else:
                cwin = curwin
            del imagewindow[win]
            imwin = imagewindow[curwin]
            curwin = cwin
            if imwin.zoom > 1:
                zoom_multiply(imwin.zoom)


def imwindow_switchto(win):
    global imwin, curwin
    oldwin = imwin
    imagewindow[curwin] = imwin
    imwin = win
    curwin = imagewindow.index(imwin)
    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()


def imwindow_next():
    global imwin, curwin
    oldwin = imwin
    nextwin = curwin + 1
    if nextwin > len(imagewindow) - 1:
        nextwin = 0

    imagewindow[curwin] = imwin
    imwin = imagewindow[nextwin]
    curwin = nextwin
    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)

    showtipex(dtext['win'] + u': ' + imwin.name)
    mainproc_start()


def imwindow_change(win=None):
    global imwin, curwin, imwin, curwin
    oldwin = imwin
    if win is None:
        nextwin = curwin + 1
        if nextwin > len(imagewindow) - 1:
            nextwin = 0

        imagewindow[curwin] = imwin
        imwin = imagewindow[nextwin]
        curwin = nextwin
    elif win > 0 and win < len(imagewindow):
        if imagewindow[win] is not None:
            imagewindow[curwin] = imwin
            imwin = imagewindow[win]
            curwin = win

    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)


def showtip(text):
    mess_tip.pos = None
    mess_tip.coord = [
        con.screen_size[0] - 100,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    mess_tip.messtimeout = 1
    mess_tip.hiden(False)


def hidetip():
    mess_tip.hiden(True)


def showtipex(text, timeout=1):
    mess_tip.pos = None
    mess_tip.coord = [
        con.screen_size[0] - 100,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    w = mess_tip.rectcoord[2] - mess_tip.rectcoord[0]
    mess_tip.coord = [
        con.screen_size[0] - w - 10,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    mess_tip.messtimeout = timeout
    mess_tip.hiden(False)


def check_imwincount():
    if mainmenu is not None:
        if len(imagewindow) == 1:
            mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['close']), True)
        else:
            mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['close']), False)


def file_new(w, h, win):
    image = new_image((w, h))
    if image is None:
        return None

    imwindow_new(image, win)
    del image
    check_imwincount()


def file_close(win=None):
    imwindow_close(win)
    check_imwincount()


def _file_open(filename, new_win):
    if filename is None:
        return None

    mbox_percent.style = 'center'
    mbox_percent.draw(dtext['loading'] + u'...')
    mbox_percent.style = 'up'

    try:
        image = graphics.Image.open(filename)
        file_addrecent(filename)
    except SymbianError:
        None
        None
        None
        appuifw.note(u"Could' to open image", 'error')
        return None
    except:
        None

    imwindow_new(image, new_win)
    del image
    imwin.filename = filename
    imwin.lastfile = filename
    check_imwincount()
    return imwin


def file_open(new_win=False):
    try:
        filename = dialog.open(path=ur(con.lastpath_img), ext=[
            'jpg',
            'png',
            'gif',
            'bmp',
            'mbm',
            'jpeg'], kind='open')
    except:
        None
        None
        None
        filename = dialog.open(path=con.lastpath_img, ext=[
            'jpg',
            'png',
            'gif',
            'bmp',
            'mbm',
            'jpeg'], kind='open')

    if filename is None:
        return None

    if type(filename) == type('') or type(filename) == type(u''):
        if path.splitext(filename)[1].lower() == '.mbm':
            appuifw.note(dtext['unpacking'] + '...')
            filename = mbm.Unmake(filename, con.lastpath_img + '\\')

    if type(filename) == type('') or type(filename) == type(u''):
        con.lastpath_img = path.split(filename)[0]
        redraw_main()
        if imwin.filename is not None and new_win == False:
            if appuifw.query(dtext['q_flnotsaved'], 'query'):
                file_saveas(trans=False)

        _file_open(filename, new_win)
    else:
        con.lastpath_img = path.split(filename[0])[0]
        redraw_main()
        if imwin.filename is not None and new_win == False:
            if appuifw.query(dtext['q_flnotsaved'], 'query'):
                file_saveas(trans=False)

        first = False
        for t in filename:
            if path.isfile(t):
                if first is False:
                    _file_open(t, new_win)
                    first = True
                else:
                    _file_open(t, True)

    return imwin


def file_addrecent(filename):
    try:
        for t in xrange(len(con.recentfiles)):
            con.recentfiles.remove(filename.lower())
    except:
        None
        None
        None

    con.recentfiles.insert(0, filename.lower())
    if len(con.recentfiles) > 10:
        del con.recentfiles[10:len(con.recentfiles)]


def file_reopen(win):
    if imwin.lastfile is not None:
        _file_open(imwin.lastfile, win)


def file_format_select(frmt):
    if frmt.upper() == 'JPEG':
        def_quality = 75
        def_quality = appuifw.query(dtext['quality'], 'number', def_quality)
        if def_quality is None:
            return None

        if 1 > def_quality:
            pass
        def_quality > 100
        if 1:
            appuifw.note(dtext['e_wrongqual'], 'error')
            return None

        return {
            'format': frmt,
            'quality': def_quality}
    elif frmt.upper() == 'PNG':
        def_bpp = 24
        bpp = [
            24,
            8,
            1]
        name = [
            dtext['bpp_24'],
            dtext['bpp_8'],
            dtext['bpp_1']]
        ind = appuifw.popup_menu(name, dtext['bpp'])
        if ind is None:
            return None

        def_bpp = bpp[ind]
        def_compression = 2
        compr = [
            'no',
            'fast',
            'default',
            'best']
        name = [
            dtext['comp_no'],
            dtext['comp_fast'],
            dtext['comp_def'],
            dtext['comp_best']]
        ind = appuifw.popup_menu(name, dtext['compression'])
        if ind is None:
            return None

        compression = compr[ind]
        return {
            'format': frmt,
            'bpp': def_bpp,
            'compression': compression}


def file_save(frmt=None, trans=True):
    if imwin.filename is None:
        file_saveas(True)
    elif frmt is None:
        if imwin.filename.lower().endswith('.png'):
            frmt = 'PNG'
        elif imwin.filename.lower().endswith('.jpg') or imwin.filename.lower().endswith('.jpeg'):
            frmt = 'JPEG'
        elif not file_saveas(True):
            return None

    param = file_format_select(frmt)

    try:
        if param['format'] == 'PNG':
            imwin.img.save(imwin.filename, bpp=param['bpp'], compression=param['compression'], format=param['format'])
            if trans:
                if not AskTransparent():
                    appuifw.note(dtext['saved'] + unicode(imwin.filename))

            else:
                appuifw.note(dtext['saved'] + unicode(imwin.filename))
        elif param['format'] == 'JPEG':
            imwin.img.save(imwin.filename, quality=param['quality'], format=param['format'])
            appuifw.note(dtext['saved'] + unicode(imwin.filename))
    except:
        None
        None
        None
        appuifw.note(dtext['cantsave'], 'error')


def file_saveas(trans=True):
    dirname = dialog.open(path=ur(con.lastpath_img), ext=[
        'jpg',
        'png',
        'gif',
        'bmp',
        'mbm',
        'jpeg'], kind='save')
    if dirname is None:
        return False

    if path.isfile(ur(dirname)):
        defname = path.split(dirname)[1]
    else:
        defname = u'image_'
    dirname = path.split(dirname)[0] + '\\'
    dirname = dirname.replace('\\\\', '\\')
    con.lastpath_img = dirname
    confirm = False
    while not confirm:
        name = appuifw.query(dtext['entername'], 'text', defname)
        if name is None:
            return False

        imwin.filename = dirname + name
        name = [
            u'PNG - Portable Network Graphics',
            u'JPG - JPEG']
        ind = appuifw.popup_menu(name, dtext['format'])
        if ind is None:
            return False
        elif ind == 0:
            imwin.frmt = 'PNG'
            if not imwin.filename.lower().endswith('.png'):
                imwin.filename += '.png'

        elif ind == 1:
            imwin.frmt = 'JPEG'
            if not imwin.filename.lower().endswith('.jpg') and not imwin.filename.lower().endswith('.jpeg'):
                imwin.filename += '.jpg'

        if path.exists(ur(imwin.filename)):
            confirm = appuifw.query(dtext['owconfirm'], 'query')
        else:
            confirm = True
        continue
        None
    file_save(frmt=imwin.frmt, trans=trans)
    return True


def AskTransparent():
    name = [
        dtext['wotrans'],
        dtext['addtrans']]
    ind = appuifw.popup_menu(name, dtext['usetrans'])
    if ind is None:
        return False
    elif ind == 0:
        return False
    elif ind == 1:
        ChoseColor(dtext['colchoosetip'])
        return True


def ChoseColor(text):
    global curtool
    appuifw.note(text)
    oldforeclr = foreclr
    oldtool = curtool
    curtool = tool['picker']
    imwin.obj = tool['picker']
    imwin.drawing = False
    imwin.selector.set(None)
    imwin.waitpickerchoose = True

    imwin.pickercallback = lambda: UseTransparent(oldforeclr, oldtool)


def UseTransparent(oldforeclr, oldtool):
    global foreclr
    SV_TRANS.file_transparent(imwin.filename, inttorgb(foreclr), progressbar.update, dtext)
    appuifw.note(dtext['saved'] + unicode(imwin.filename))
    foreclr = oldforeclr
    curtool = oldtool
    imwin.obj = oldtool


def query_file_new(win):
    size = con.screen_size
    if classes.TUniSlector.copybuff != None:
        size = classes.TUniSlector.copybuff.size

    w = appuifw.query(dtext['width'], 'number', size[0])
    if w is not None:
        h = appuifw.query(dtext['height'], 'number', size[1])
        if h is not None:
            file_new(w, h, win)


def image_tobpp(img, bpp):
    im = new_image(img.size, mode=bpp)
    if im is None:
        return None

    im.blit(img)
    img = im
    return img


def fontstd_select():
    global bmpfont
    appuifw.app.screen = 'normal'
    fonts = appuifw.available_fonts()
    ind = appuifw.selection_list(fonts)
    if ind is not None:
        if s60_version_info == (3, 0):
            imwin.obj_font = (fonts[ind], stdfontsize, graphics.FONT_ANTIALIAS)
        else:
            imwin.obj_font = fonts[ind]
        bmpfont = None

    appuifw.app.screen = 'full'


def fontstd_opt():
    global stdfontsize, fontflags
    if s60_version_info != (3, 0):
        return None

    foptcont = [
        (dtext['size'], 'number', stdfontsize),
        (dtext['italic'], 'combo', ([
                                        dtext['no'],
                                        dtext['yes']], fontflags[0])),
        (dtext['bold'], 'combo', ([
                                      dtext['no'],
                                      dtext['yes']], fontflags[1])),
        (dtext['antialias'], 'combo', ([
                                           dtext['no'],
                                           dtext['yes']], fontflags[2]))]
    foptform = appuifw.Form(foptcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    appuifw.app.screen = 'normal'
    appuifw.app.title = dtext['font']
    foptform.execute()
    fg = 0
    if foptform[1][2][1] == 1:
        fg = fg | graphics.FONT_ITALIC

    if foptform[2][2][1] == 1:
        fg = fg | graphics.FONT_BOLD

    if foptform[3][2][1] == 1:
        fg = fg | graphics.FONT_ANTIALIAS

    stdfontsize = int(foptform[0][2])
    fontflags = [
        int(foptform[1][2][1]),
        int(foptform[2][2][1]),
        int(foptform[3][2][1])]
    appuifw.app.screen = 'full'
    appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
    imwin.obj_font = (imwin.obj_font[0], stdfontsize, fg)


def changebpp():
    bpp = [
        '1',
        'L',
        'RGB12',
        'RGB16',
        'RGB']
    name = [
        dtext['bpp_1'],
        dtext['bpp_8'],
        dtext['bpp_12'],
        dtext['bpp_16'],
        dtext['bpp_24']]
    ind = appuifw.popup_menu(name, dtext['bpp'])
    if ind is not None:
        imwin.img = image_tobpp(imwin.img, bpp[ind])


def query_rgb(text, source=(0, 0, 0)):
    if type(source) is type(1):
        src = u'%06x' % source
    else:
        src = rgbtohex(source)
    color = appuifw.query(text, 'text', src)
    if color is None:
        return None

    if color.find('.') != -1:

        try:
            #continue
            color = []([int(x) for x in color.split('.')])
            if len(color) != 3:
                appuifw.note(dtext['error_unexpchars'], 'error')
                return None
        except:
            None
            None
            None
            appuifw.note(dtext['error_unexpchars'], 'error')
            return None

    else:

        try:
            color = inttorgb(int(color, 16))
        except:
            None
            None
            None
            appuifw.note(dtext['error_unexpchars'], 'error')
            return None

    return color


def inttorgb(color):
    b = color % 256
    g = color / 256 % 256
    r = color / 256 / 256 % 256
    return (r, g, b)


def rgbtoint(c):
    return c[0] * 65536 + c[1] * 256 + c[2]


def rgbtohex(c):
    return u'%06x' % (c[0] * 65536 + c[1] * 256 + c[2])


def hextorgb(color):
    return inttorgb(int(color, 16))


def updatecallback(cur, total):
    mbox_percent.draw(dtext['processing'])
    progressbar.percent(cur * 100 / total)
    progressbar.draw()


def image_tomask():
    imwin._backupimage()
    name = [
        dtext['normal'],
        dtext['invert']]
    ind = appuifw.popup_menu(name, dtext['masktype'])
    if ind is None:
        return None

    mbox_percent.draw(dtext['processing'])
    if ind == 0:
        (img, msk) = improc._image_tomaskblack(GetSelectedImage(), inttorgb(foreclr), updatecallback)
    else:
        (img, msk) = improc._image_tomaskwhite(GetSelectedImage(), inttorgb(foreclr), updatecallback)
    imwin.selector.setimage((img, msk))


def image_invertcolors():
    name = [
        dtext['full'],
        dtext['singlech']]
    ind = appuifw.popup_menu(name, dtext['invertmode'])
    if ind is None:
        return None

    if ind == 0:
        imwin._backupimage()
        mbox_percent.draw(dtext['processing'])
        (img, msk) = improc._image_invertcolors(GetSelectedImage(), updatecallback)
    elif ind == 1:
        name = [
            dtext['red'],
            dtext['green'],
            dtext['blue']]
        ind = appuifw.popup_menu(name, dtext['invertcolorch'])
        if ind is None:
            return None

        imwin._backupimage()
        mbox_percent.draw(dtext['processing'])
        (img, msk) = improc._image_invertcolor_channel(GetSelectedImage(), updatecallback, ind)

    imwin.selector.setimage((img, msk))


def image_colorbalance():
    col = query_rgb(u'R.G.B (-100.-100.-100)-(100.100.100)', (0, 0, 0))
    if col is None:
        return None

    for val in col:
        if val > 100 or val < -100:
            appuifw.note(dtext['badvalue'], 'error')
            return None

    imwin._backupimage()
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_colorbalance(GetSelectedImage(), col, updatecallback)
    imwin.selector.setimage((img, msk))


def image_saturation():
    val = appuifw.query(dtext['enterval'] + u'(0-200)', 'number', 100)
    if val is None:
        return None

    if val > 200:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_saturation(GetSelectedImage(), val, updatecallback)
    imwin.selector.setimage((img, msk))


def image_sepia():
    imwin._backupimage()
    (img, msk) = improc._image_sepia(GetSelectedImage(), updatecallback)
    imwin.selector.setimage((img, msk))


def image_posterize():
    imwin._backupimage()
    (img, msk) = improc._image_posterize(GetSelectedImage(), updatecallback)
    imwin.selector.setimage((img, msk))


def image_fractal():
    name = [
        dtext['red'],
        dtext['green'],
        dtext['blue'],
        dtext['entercolor']]
    ind = appuifw.popup_menu(name, dtext['color'] + u':')
    if ind is None:
        return None
    elif ind == 0:
        col = hextorgb('0x070000')
    elif ind == 1:
        col = hextorgb('0x000700')
    elif ind == 2:
        col = hextorgb('0x000007')
    elif ind == 3:
        rgb = [
            0,
            0,
            0]
        rgb[int(uniform(0, 3))] = int(uniform(0, 256))
        col = query_rgb(dtext['color'] + u':', tuple(rgb))

    if col is None:
        return None

    imwin._backupimage()
    (img, msk) = improc._image_fractal(GetSelectedImage(), col, updatecallback)
    imwin.selector.setimage((img, msk))


def image_fractal_mandelbrot():
    imwin._backupimage()
    (img, msk) = improc._image_fractal_mandelbrot(GetSelectedImage(), iterations=25, scale=60, callback=updatecallback)
    imwin.selector.setimage((img, msk))


def image_gradient(knd):
    if knd == 0:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 0))
    elif knd == 1:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 2))
    elif knd == 2:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 1))
    elif knd == 3:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 3))

    imwin.selector.setimage((img, msk))


def image_replacecolor():
    source = imwin.img.getpixel((imwin.curs.x, imwin.curs.y))[0]
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_replacecolor(GetSelectedImage(), source, inttorgb(foreclr), updatecallback)
    imwin.selector.setimage((img, msk))


def image_replacecolor_query():
    source = imwin.img.getpixel((imwin.curs.x + imwin.imx, imwin.curs.y + imwin.imy))[0]
    repcolor = query_rgb(dtext['repcolor'], source)
    if repcolor is None:
        return None

    descolor = query_rgb(dtext['descolor'], foreclr)
    if descolor is None:
        return None

    imwin._backupimage()
    mbox_percent.draw(dtext['replacecolor'])
    (img, msk) = improc._image_replacecolor(GetSelectedImage(), repcolor, descolor, updatecallback)
    imwin.selector.setimage((img, msk))


def image_convertbpp(im, bpp):
    img = new_image(im.size, mode=bpp)
    if img is None:
        return None

    img.blit(im)
    return img


def image_flip():
    ind = appuifw.popup_menu([
        dtext['vertical'],
        dtext['horizontal']], dtext['flip'])
    if ind is None:
        return None

    imwin._backupimage()
    if ind == 1:
        (img, msk) = improc._image_flip(graphics.FLIP_LEFT_RIGHT, imwin)
    elif ind == 0:
        (img, msk) = improc._image_flip(graphics.FLIP_TOP_BOTTOM, imwin)


def image_rotate_():
    imwin._backupimage()
    name = [
        dtext['rotateright'],
        dtext['rotateleft']]
    ind = appuifw.popup_menu(name, dtext['rotate'])
    if ind == 1:
        (img, msk) = improc._image_rotate(graphics.ROTATE_90, imwin, workzone)
    elif ind == 0:
        (img, msk) = improc._image_rotate(graphics.ROTATE_270, imwin, workzone)


def image_rotate():
    imwin._backupimage()
    if imwin.selector.isactive():
        angle = appuifw.query(u'\xe8\xbe\x93\xe5\x85\xa5\xe6\x97\x8b\xe8\xbd\xac\xe8\xa7\x92\xe5\xba\xa6', 'number', 0)
        if angle is None:
            return None

        mode = 0
        (img, msk) = improc._image_rotateangle(GetSelectedImage(), angle, backclr, updatecallback, mode)
        Selection_SetImageCenter((img, msk))
    else:
        image_rotate_()


def image_resize_query():
    name = [
        u'\xe5\x83\x8f\xe7\xb4\xa0',
        u'%']
    ind = appuifw.popup_menu(name, dtext['resize'])
    if ind == 0:
        width = appuifw.query(dtext['width'], 'number', imwin.img.size[0])
        if width is not None:
            height = appuifw.query(dtext['height'], 'number', imwin.img.size[1])
            if height is not None:
                asp = appuifw.query(dtext['keepaspect'], 'query')
                if asp is None:
                    asp = 0
                else:
                    asp = 1
                imwin._backupimage()
                (img, msk) = improc._image_resize(GetSelectedImage(), ((width, height), asp, workzone), imwin)
                imwin.selector.setimage((img, msk))


    elif ind == 1:
        size = imwin.img.size
        width = appuifw.query(dtext['width'] + u'(%)', 'number', 100)
        if width is not None:
            height = appuifw.query(dtext['height'] + u'(%)', 'number', 100)
            if height is not None:
                asp = appuifw.query(dtext['keepaspect'], 'query')
                if asp is None:
                    asp = 0
                else:
                    asp = 1
                imwin._backupimage()
                (img, msk) = improc._image_resize(GetSelectedImage(),
                                                  ((size[0] * width / 100, size[1] * height / 100), asp, workzone),
                                                  imwin)
                imwin.selector.setimage((img, msk))


def image_resizecanvas(sz):
    im = new_image(sz)
    if im is None:
        return None

    imwin.size((min(im.size[0], workzone[0]), min(im.size[1], workzone[1])))
    im.blit(imwin.img)
    imwin.img = im
    imwin.image_coord(0, 0)


def image_resizecanvas_query():
    name = [
        u'\xe5\x83\x8f\xe7\xb4\xa0',
        u'%']
    ind = appuifw.popup_menu(name, dtext['resizecanvas'])
    if ind == 0:
        width = appuifw.query(dtext['width'], 'number', imwin.img.size[0])
        if width is not None:
            height = appuifw.query(dtext['height'], 'number', imwin.img.size[1])
            if height is not None:
                image_resizecanvas((width, height))


    elif ind == 1:
        size = imwin.img.size
        width = appuifw.query(dtext['width'] + u'(%)', 'number', 100)
        if width is not None:
            height = appuifw.query(dtext['height'] + u'(%)', 'number', 100)
            if height is not None:
                image_resizecanvas((width * size[0] / 100, height * size[1] / 100))


def image_crop():
    if imwin.selector.isactive():
        imwin._backupimage()
        (image, mask) = imwin.selector.getimage()
        image_resizecanvas(image.size)
        imwin.img = image
        imwin.selector.tool.deselect()
        imwin.image_coord(0, 0)


def image_bpp(bpp):
    imwin._backupimage()
    (image, mask) = GetSelectedImage()
    img = new_image(image.size, mode=bpp)
    img.blit(image)
    im = new_image(image.size, mode='RGB16')
    im.blit(img)
    imwin.selector.setimage((im, mask), replace=True)


def image_lightness_query():
    value = appuifw.query(dtext['enterval'] + '(0%-100%)', 'number', 0)
    if value is None:
        return None

    if value > 100:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    value = 255 * value / 100
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_lightness_slow(GetSelectedImage(), value)
    else:
        (img, msk) = improc._image_lightness(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_darkness_query():
    value = appuifw.query(dtext['enterval'] + u'(0%-100%)', 'number', 0)
    if value is None:
        return None

    if value > 100:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    value = 255 * value / 100
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_darkness_slow(GetSelectedImage(), value)
    else:
        (img, msk) = improc._image_darkness(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_blur_query():
    imwin._backupimage()
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_blur_bysizing(imwin.img)
    else:
        value = 100
        (img, msk) = improc._image_blur(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_displacement():
    vert = appuifw.popup_menu([
        dtext['horizontal'],
        dtext['vertical']], dtext['displacement'])
    if vert is None:
        return None

    value = appuifw.query(dtext['angle'], 'number', 0)
    if value is None:
        return None

    imwin._backupimage()
    (img, msk) = improc._image_displacement(GetSelectedImage(), value, vert, backclr, updatecallback)
    imwin.selector.setimage((img, msk))


def GetSelectedImage():
    (image, mask) = imwin.selector.getimage(replace=True)
    return (image, mask)


def Selection_SetImageCenter(_0):
    (im, ms) = _0
    (image, mask) = imwin.selector.getimage(replace=True)
    dx = (im.size[0] - image.size[0]) / 2
    dy = (im.size[1] - image.size[1]) / 2
    (x1, y1, x2, y2) = imwin.selector.getcoord()
    imwin.img.blit(im, target=(x1 - dx, y1 - dy), mask=ms)


def theme_open():
    fname = dialog_misc.open(path=program_path + 'Themes\\', ext=[
        'thm'], kind='open')
    if fname is None:
        return None

    if theme_load(fname):
        ui_colors_update()


def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args + fargs, **args + fargs)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def plugins_findmods():
    plugins = []
    if path.exists(program_path + 'Plugins\\dontloadplugins'):
        return plugins

    for x in listdir(program_path + 'Plugins\\'):
        if path.isfile(program_path + 'Plugins\\' + x):
            if x.lower().endswith('.py') or x.lower().endswith('.pyc'):
                plugins.append(path.splitext(x)[0])

    return plugins


def plugins_importmods(plugins):
    modules = []
    sys.path.insert(0, program_path + 'Plugins\\')
    for t in plugins:

        try:
            modules.append(__import__(t))
        except Exception:
            None
            exc = None
            None
            traceback.print_exc(sys.stderr)
            appuifw.note(dtext['invalidplugin'] + ': ' + t)
        except:
            None

    return modules


def plugins_splittext(text, num):
    words = text.split(' ')
    delmt = u' '
    text = u''
    info = []
    for t in xrange(len(words)):
        text += words[t] + delmt
        if len(text) > num:
            text = text[:-1]
            info.append(text)
            text = u''
        elif len(text) <= num and t == len(words) - 1:
            text = text[:-1]
            info.append(text)

    return info


def plugins_function(m):
    try:
        imwin._backupimage()
        if m.__version_info__[3] == '1.0':
            (img, msk) = m.Execute(GetSelectedImage(), ProgressCallback)
        elif m.__version_info__[3] == '1.1':
            (img, msk) = m.Execute((GetSelectedImage(), (foreclr, backclr), imwin.bsize, ProgressCallback))

        imwin.selector.setimage((img, msk), replace=True)
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(dtext['invalidplugin'], 'error')


def plugins_createmenu(modules, files):
    if modules:
        it = []
        ab = [
            u'',
            u'Plugins and Contributors:',
            u'']
        for t in xrange(len(modules)):

            try:
                it.append((modules[t].__version_info__[1], partial(plugins_function, modules[t])))
                if modules[t].__version_info__[0] == u'internal':
                    continue

                info = plugins_splittext(
                    u'  ' + modules[t].__version_info__[1] + ' ' + modules[t].__version_info__[2] + ' - ' +
                    modules[t].__version_info__[0], 22)
                ab.extend(info)
                ab.append('')
            except Exception:
                None
                exc = None
                None
                traceback.print_exc(sys.stderr)
                appuifw.note(dtext['invalidplugin'] + ': ' + files[t], 'error')
                continue
            except:
                None

        if len(ab) == 3:
            ab = []
        else:
            ab.append(u'')
        items = tuple(it)
        return ((dtext['plugins'], items), ab)
    else:
        return ((dtext['plugins'], (lambda: None)), [
            u''])


def plugins_load():
    f = plugins_findmods()
    m = plugins_importmods(f)
    menu = plugins_createmenu(m, f)
    return menu


def ProgressCallback(cur, total):
    mbox_percent.draw(dtext['processing'])
    progressbar.percent(cur * 100 / total)
    progressbar.draw()
    if keyboard.is_down(key_codes.EScancodeRightSoftkey):
        return False

    ao_sleep(0.001)


def skin_select():
    #continue
    name = []
    ind = appuifw.popup_menu(name, dtext['skinselect'])
    if ind is None:
        return None

    if not skin_check(program_path + 'skin\\' + name[ind] + '\\'):
        return None

    oldskin = con.skin
    con.skin = name[ind]
    file_copy(program_path + 'skin\\id_logo.png', program_path + 'skin\\' + con.skin + '\\id_logo.png')
    appuifw.note(dtext['restart'])


def skin_check(folder):
    files = (
    'Pencil_32.png', 'Brush_32.png', 'Erase_32.png', 'Line2_32.png', 'Rect_32.png', 'Ellipse_32.png', 'Select_32.png',
    'El_Select.png', 'Cstamp_32.png', 'Picker_32.png', 'Notemlet_32.png', 'Text_32.png', 'Polygon_32.png',
    'Broken_32.png', 'PaintBucket_32.png', 'Spray_32.png', 'Lasso.png', 'mrod.png', 'Grad_vert.png', 'Grad_cir.png',
    'Grad_gor.png', 'Grad_rect.png', 'f.png', 'c.png', 'b.png', 'black-white.png', 'color_black.png', 't.png',
    'color_white.png', 'drive.png', 'drive_mask.png', 'dir.png', 'dir_mask.png', 'im_green.png', 'im_blue.png',
    'im_red.png', 'im_yellow.png', 'im_gray.png', '1.png', '2.png', '3.png', '4.png', '5.png', '6.png')
    missed = ''
    for f in files:
        if not path.exists(folder + f):
            missed += f + ', '

    if missed != '':
        missed = missed[:-2]
        appuifw.note(dtext['invalidskin'] + ' ' + unicode(missed), 'error')
        return False

    return True


def theme_load(theme):
    if theme is None:
        return None

    try:
        parser = iniparser.TIniParser()
        parser.open(ur(theme))
        parser.readgroup('UI_COLORS')
        con.ui_menu_color = [
            [
                0,
                0,
                0],
            [
                0,
                0,
                0,
                0,
                0]]
        con.ui_form_color = [
            0,
            0,
            0,
            [
                0,
                0,
                0]]
        con.ui_menu_color[0][0] = parser.readint('menu_form_out', 16)
        con.ui_menu_color[0][1] = parser.readint('menu_form_in', 16)
        con.ui_menu_color[0][2] = parser.readint('menu_form_shade', 16)
        con.ui_menu_color[1][0] = parser.readint('menu_selbox_out', 16)
        con.ui_menu_color[1][1] = parser.readint('menu_selbox_in', 16)
        con.ui_menu_color[1][2] = parser.readint('menu_item', 16)
        con.ui_menu_color[1][3] = parser.readint('menu_selitem', 16)
        con.ui_menu_color[1][4] = parser.readint('menu_blckitem', 16)
        con.ui_form_color[2] = parser.readint('backgr_form', 16)
        con.ui_form_color[0] = parser.readint('status_form', 16)
        con.ui_form_color[1] = parser.readint('status_font', 16)
        con.ui_form_color[3][0] = parser.readint('editor_scroll_outline', 16)
        con.ui_form_color[3][1] = parser.readint('editor_scroll_slider', 16)
        con.ui_form_color[3][2] = parser.readint('editor_scroll_fill', 16)
        con.ui_grid_color = parser.readint('grid_selector_color', 16)
        con.ui_req_color = [
            0,
            0,
            [
                0,
                0,
                0,
                0,
                0,
                0],
            [
                0,
                0,
                0]]
        con.ui_req_color[0] = parser.readint('fileman_background', 16)
        con.ui_req_color[1] = parser.readint('fileman_infobar', 16)
        con.ui_req_color[2][0] = parser.readint('fileman_selbox_out', 16)
        con.ui_req_color[2][1] = parser.readint('fileman_selbox_in', 16)
        con.ui_req_color[2][2] = parser.readint('fileman_item', 16)
        con.ui_req_color[2][3] = parser.readint('fileman_selitem', 16)
        con.ui_req_color[2][4] = parser.readint('fileman_markitem', 16)
        con.ui_req_color[3][0] = parser.readint('fileman_scroll_outline', 16)
        con.ui_req_color[3][1] = parser.readint('fileman_scroll_slider', 16)
        con.ui_req_color[3][2] = parser.readint('fileman_scroll_fill', 16)
        con.ui_prog_color[0] = parser.readint('progressbar_out', 16)
        con.ui_prog_color[1] = parser.readint('progressbar_slider', 16)
        con.ui_prog_color[2] = parser.readint('progressbar_fill', 16)
        parser.close()
        return True
    except:
        None
        None
        None
        appuifw.note(dtext['invalidplugin'], 'error')
        return False


def ui_colors_update():
    mainmenu.colors(con.ui_menu_color)
    menu_preview.colors(con.ui_menu_color)
    menu_palette.colors(con.ui_menu_color)
    popupmenu.colors(con.ui_menu_color)
    mbox_percent.clrs = [
        con.ui_menu_color[1][2],
        con.ui_menu_color[1][1],
        con.ui_menu_color[1][3]]
    dialog.colors(con.ui_req_color)
    dialog_tmp.colors(con.ui_req_color)
    dialog_pal.colors(con.ui_req_color)
    dialog_img.colors(con.ui_req_color)
    dialog_misc.colors(con.ui_req_color)
    scrollbar_imw[0].color(con.ui_form_color[3])
    scrollbar_imw[1].color(con.ui_form_color[3])
    menu_about.clrs = (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2])
    mess_info.clrs = (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2])
    toolslist.rectcolor(con.ui_grid_color)
    colorgrid.rectcolor(con.ui_grid_color)
    gradgrid.rectcolor(con.ui_grid_color)


def font_open():
    fname = dialog_misc.open(path=ur(lastpath_fnt), ext=[
        'rfn'], kind='open')
    if fname is None:
        return None

    font_load(fname)


def font_load(pth):
    global bmpfont, fontname, codemap
    bmpfont = graphics.Image.open(pth)
    fontname = path.splitext(path.split(pth)[1])[0]
    font_parse(bmpfont)
    if not path.isfile(program_path + 'chars.map'):
        appuifw.note(u'Chars.map not found!')

    codef = open(program_path + 'chars.map', 'rt')
    codeline = codef.readline().decode('utf-8')
    codef.close()
    codemap = codeline
    font_updatemess(imwin.obj_text)


def font_parse(img):
    if font_loadchache():
        return None

    tcoord = 0
    pdraw = progressbar.draw
    percent = progressbar.percent
    mbox_percent.draw(dtext['fontcaching'])
    cellh = img.size[1] / 14
    cellw = img.size[0] / 16
    ao_sleep(0.001)
    backcol = img.getpixel((0, 0))[0]
    y = 0
    for n in xrange(16):
        x = 0
        y1 = cellh * n
        y2 = cellh * (n + 1)
        for t in xrange(16):
            (x1, x2) = ip_getcolumnx2(img, (cellw * t, cellw * (t + 1) - 5, y1, y2), backcol)
            if x1 is not None:
                symbols[16 * n + t] = (x1, y1, x2, y2)
                tcoord = (tcoord + x2 - x1) + 1

        percent(n * 100 / 15)
        pdraw()
        if keyboard.is_down(key_codes.EScancodeRightSoftkey):
            return False

        ao_sleep(0.001)

    symbols[0][0] = 0
    symbols[0][1] = 0
    symbols[0][2] = cellw / 3
    symbols[0][3] = cellh
    font_savechache()
    appuifw.note(dtext['fontloaded'])


def font_savechache():
    pars = iniparser.TIniParser()
    pars.create(program_path + 'Fonts\\' + fontname + '.cch')
    pars.writegroup('SYMBOLS')
    n = 0
    for t in symbols:
        pars.writeint(str(n), t)
        n += 1

    pars.close()


def font_loadchache():
    pdraw = progressbar.draw
    percent = progressbar.percent
    pars = iniparser.TIniParser()
    if not path.isfile(program_path + 'Fonts\\' + fontname + '.cch'):
        return False

    pars.open(program_path + 'Fonts\\' + fontname + '.cch')
    dic = pars.getdict('SYMBOLS')
    pars.close()
    for t in xrange(0, 256):
        continue
        symbols[t] = [int(x) for x in dic[str(t)].split(',')]

    return True


def font_updatemess(text):
    global fontbuff, fontbuffmsk, graymask
    if text is None:
        return None

    if bmpfont is not None:
        ordlist = []
        twidth = 0
        theight = 0
        for t in xrange(len(text)):
            ind = codemap.find(text[t])
            if ind == -1:
                ind = 31

            ordlist.append(ind - 1)

        for t in ordlist:
            twidth += (symbols[t][2] - symbols[t][0]) * fontscalex + fntsymbolsdelay
            theight = max(theight, (symbols[t][3] - symbols[t][1]) * fontscaley)

        fontbuff = new_image((twidth, theight))
        fontbuff.clear(0)
        fontbuffmsk = new_image((twidth, theight), 'L')
        graymask = new_image(bmpfont.size, 'L')
        coordx = 0
        for t in ordlist:
            if fontscalex != 1 or fontscaley != 1:
                tmpimg = new_image(
                    ((symbols[t][2] - symbols[t][0]) * fontscalex, (symbols[t][3] - symbols[t][1]) * fontscaley), '1')
                tmpimg.blit(bmpfont, source=symbols[t], scale=1)
                fontbuff.blit(tmpimg, target=(coordx, 0))
                coordx += (symbols[t][2] - symbols[t][0]) * fontscalex + fntsymbolsdelay
            else:
                fontbuff.blit(bmpfont, source=symbols[t], target=(coordx, 0), mask=graymask)
                coordx += (symbols[t][2] - symbols[t][0]) + fntsymbolsdelay

        fontbuffmsk.blit(fontbuff)
        fontbuff.clear(foreclr)


def font_opt():
    global fntsymbolsdelay, fontscalex, fontscaley
    foptcont = [
        (dtext['extfont_ldelay'], 'number', fntsymbolsdelay),
        (dtext['extfont_scalex'], 'number', int(fontscalex * 100)),
        (dtext['extfont_scaley'], 'number', int(fontscaley * 100))]
    foptform = appuifw.Form(foptcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    appuifw.app.screen = 'normal'
    appuifw.app.title = dtext['font']
    foptform.execute()
    fntsymbolsdelay = int(foptform[0][2])
    fontscalex = float(foptform[1][2]) / 100.0
    fontscaley = float(foptform[2][2]) / 100.0
    appuifw.app.screen = 'full'
    appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
    font_updatemess(imwin.obj_text)


def ip_isemptyline(img, y, _4, backcol):
    (x1, x2) = _4
    for x in xrange(x1, x2):
        col = img.getpixel((x, y))[0]
        if col != backcol:
            return (x, y)

    return True


def ip_isemptycolumn(img, x, _4, backcol):
    (y1, y2) = _4
    for y in xrange(y1, y2):
        col = img.getpixel((x, y))[0]
        if col != backcol:
            return (x, y)

    return True


def ip_getliney(img, sy, _4, backcol):
    (x1, x2) = _4
    top = True
    y1 = None
    y2 = None
    for y in xrange(sy, img.size[1]):
        top = ip_isemptyline(img, y, (x1, x2), backcol)
        if top == True:
            pass
        1
        y1 = top[1]
        break

    if y1 is None:
        return (None, None)

    for yy in xrange(y1, img.size[1]):
        top = ip_isemptyline(img, yy, (x1, x2), backcol)
        if top != True:
            y2 = top[1]
        else:
            break

    return (y1, y2)


def ip_getcolumnx2(img, _2, backcol):
    (sx, ex, y1, y2) = _2
    dot = None
    x1 = None
    x2 = None
    for x in xrange(sx, ex):
        for y in xrange(y1, y2):
            col = img.getpixel((x, y))[0]
            if col != backcol:
                dot = (x, y)

        if dot is not None:
            x1 = dot[0]
            break

    if x1 is None:
        return (None, None)

    for xx in xrange(x1, ex):
        for y in xrange(y1, y2):
            col = img.getpixel((xx, y))[0]
            if col != backcol:
                dot = (xx, y)

        if dot is not None:
            x2 = dot[0] + 1

    return (x1, x2)


def ip_getcolumnx(img, sx, _4, backcol):
    (y1, y2) = _4
    top = True
    x1 = None
    x2 = None
    for x in xrange(sx, img.size[0]):
        top = ip_isemptycolumn(img, x, (y1, y2), backcol)
        if top == True:
            pass
        1
        x1 = top[0]
        break

    if x1 is None:
        return (None, None)

    for xx in xrange(x1, img.size[0]):
        top = ip_isemptycolumn(img, xx, (y1, y2), backcol)
        if top != True:
            x2 = top[0] + 1
        else:
            break

    return (x1, x2)


def undo():
    imwin.undo()


def redo():
    imwin.redo()


def _fill_check(img, _2, c, flabel):
    global _fill_queue
    (x, yu, yd) = _2
    iu = yu
    getpixel = img.getpixel
    fqueue = _fill_queue
    fheight = _fill_height
    if iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c:
        f = 0
    else:
        f = 1
    while iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c:
        iu -= 1
        continue
        None
    iu += 1
    i = iu
    id = yu
    for id in xrange(yu, yd):
        if flabel[x][id] == 0 and getpixel((x, id))[0] == c:
            if f:
                f = 0
                i = id

        elif f == 0:
            fqueue += [
                (x, i, id)]
            f = 1

    if f == 0:
        while id < fheight and flabel[x][id] == 0 and getpixel((x, id))[0] == c:
            id += 1
            continue
            None
        fqueue += [
            (x, i, id)]

    _fill_queue = fqueue
    flabel[x][iu:id] = (id - iu) * [
        1]
    return flabel


def fillimage(img, _2, color, callback=None):
    global _fill_width, _fill_height, _fill_queue
    (x, y) = _2
    line = img.line
    (_fill_width, _fill_height) = img.size
    if 0 <= x:
        pass
    x < _fill_width
    if 1:
        if 0 <= y:
            pass
        y < _fill_height
    if not 1:
        return 0

    if type(color) == type(1):
        cr = color / 65536
        cg = (color % 65536) / 256
        cb = color % 256
        color = (cr, cg, cb)

    c = img.getpixel((x, y))[0]
    if color == c:
        return 0

    _fill_queue = []
    flabel = []
    for i in xrange(_fill_width):
        s = []
        for j in xrange(_fill_height):
            s += [
                0]

        flabel += [
            s]

    flabel = _fill_check(img, (x, y, y + 1), c, flabel)
    while _fill_queue:
        (x, yu, yd) = _fill_queue[0]
        _fill_queue = _fill_queue[1:]
        if callback:
            if callback():
                return None

        line((x, yu, x, yd), color)
        flabel[x][yu:yd] = (yd - yu) * [
            1]
        if x > 0:
            flabel = _fill_check(img, (x - 1, yu, yd), c, flabel)

        if x < _fill_width - 1:
            flabel = _fill_check(img, (x + 1, yu, yd), c, flabel)

        continue
        None
    if callback:
        callback()


def mrod_select(img, _2, color, callback=None):
    global _fill_width, _fill_height, _fill_queue
    (x, y) = _2
    mask = graphics.Image.new(img.size, '1')
    mask.clear(0)
    (_fill_width, _fill_height) = img.size
    if 0 <= x:
        pass
    x < _fill_width
    if 1:
        if 0 <= y:
            pass
        y < _fill_height
    if not 1:
        return 0

    if type(color) == type(1):
        cr = color / 65536
        cg = (color % 65536) / 256
        cb = color % 256
        color = (cr, cg, cb)

    c = img.getpixel((x, y))[0]
    if color == c:
        return 0

    _fill_queue = []
    flabel = []
    for i in xrange(_fill_width):
        s = []
        for j in xrange(_fill_height):
            s += [
                0]

        flabel += [
            s]

    flabel = _fill_check(img, (x, y, y + 1), c, flabel)
    while _fill_queue:
        (x, yu, yd) = _fill_queue[0]
        _fill_queue = _fill_queue[1:]
        if callback:
            if callback():
                return None

        mask.line((x, yu, x, yd), color)
        flabel[x][yu:yd] = (yd - yu) * [
            1]
        if x > 0:
            flabel = _fill_check(img, (x - 1, yu, yd), c, flabel)

        if x < _fill_width - 1:
            flabel = _fill_check(img, (x + 1, yu, yd), c, flabel)

        continue
        None
    if callback:
        callback()

    return (img, mask)


def zoomimage():
    name = [
        dtext['zoomin'],
        dtext['zoomout'],
        dtext['zoom_multiply'],
        dtext['zoom_1_1']]
    ind = appuifw.popup_menu(name, dtext['zoom'])
    if ind == 0:
        zoom_in()
    elif ind == 1:
        zoom_out()
    elif ind == 2:
        zoom_multiply_query()
    elif ind == 3:
        zoom_1_1()


def changecursor():
    if con.cursormultiplier > 1:
        if imwin.zoom >= con.cursormultiplier and imwin.curs.oldsize is None:
            imwin.curs.oldsize = imwin.curs.size
            imwin.curs.size = 1
        elif imwin.zoom < con.cursormultiplier and imwin.curs.oldsize is not None:
            imwin.curs.size = imwin.curs.oldsize
            imwin.curs.oldsize = None


def _zoom():
    global zoomzone, zoombuff, zoomzone, zoombuff
    if imwin.zoom >= 1:
        zoom = 1 * imwin.zoom
        zoom_w = workzone[0] / zoom
        zoom_h = workzone[1] / zoom
        zoomzone = (0, 0, zoom_w, zoom_h)
        zoomsize = (zoom_w, zoom_h)
        zoombuff = new_image(workzone)
        if zoombuff is None:
            return None

        cursc = (imwin.curs.x, imwin.curs.y)
        imwin.image_coord(imwin.curs.x + imwin.imx - zoomsize[0] / 2, imwin.curs.y + imwin.imy - zoomsize[1] / 2)
        imwin.size((min(zoomsize[0], imwin.editsize[0]), min(zoomsize[1], imwin.editsize[1])), False)
        cor = imwin.image_correctcoord()
        imwin.curs.coord((zoomsize[0] / 2 + cor[0], zoomsize[1] / 2 + cor[1]))
        imwin.scale = False
        scrollbar_imw[0].maxvalue(imwin.img.size[0] * zoom)
        scrollbar_imw[1].maxvalue(imwin.img.size[1] * zoom)
        changecursor()
        showtipex(dtext['zoom'] + u': x' + unicode(imwin.zoom))
    else:
        zoom = imwin.zoom
        zoom_w = workzone[0] / zoom
        zoom_h = workzone[1] / zoom
        z = 1
        zz = 1
        if zoom_w > imwin.img.size[0]:
            zoom_w = imwin.img.size[0]
            imwin.zoom = float(workzone[0]) / zoom_w
            zoom = float(workzone[0]) / zoom_w
            zoom_h = workzone[1] / zoom

        if zoom_h > imwin.img.size[1]:
            zoom_h = imwin.img.size[1]
            imwin.zoom = float(workzone[1]) / zoom_h
            zoom = float(workzone[1]) / zoom_h
            zoom_w = workzone[0] / zoom

        zoomzone = (0, 0, zoom_w, zoom_h)
        zoomsize = (zoom_w, zoom_h)
        zoombuff = new_image(workzone)
        if zoombuff is None:
            return None

        cursc = (imwin.curs.x, imwin.curs.y)
        imwin.image_coord(imwin.curs.x + imwin.imx - zoomsize[0] / 2, imwin.curs.y + imwin.imy - zoomsize[1] / 2)
        curszone = imwin.curs.zone()
        imwin.size((zoomsize[0], zoomsize[1]), False)
        cor = imwin.image_correctcoord()
        imwin.curs.coord((zoomsize[0] / 2 + cor[0], zoomsize[1] / 2 + cor[1]))
        imwin.curs.zone(curszone)
        imwin.scale = True
        scrollbar_imw[0].maxvalue(imwin.img.size[0] * zoom)
        scrollbar_imw[1].maxvalue(imwin.img.size[1] * zoom)
        changecursor()


def zoom_in():
    if imwin.zoom < 64:
        imwin.zoom *= 2
        if imwin.zoom > 1 and imwin.zoom < 2:
            imwin.zoom = 1

        _zoom()


def zoom_out():
    if imwin.zoom >= 2:
        imwin.zoom = imwin.zoom / 2

    _zoom()


def zoom_1_1():
    imwin.zoom = 1
    _zoom()


def zoom_multiply(z):
    imwin.zoom = z
    if imwin.zoom > 64:
        imwin.zoom = 64

    if imwin.zoom < 1:
        imwin.zoom = 1

    _zoom()


def preview_hide(state=True):
    onnextcicle_do((lambda: _preview_hide(state)))


def _preview_hide(state=True):
    global preview_exit, prev_vert, preview_exit, redraw, prev_image, prev_coord
    preview_exit = state
    prev_vert = False
    if preview_calc() == False:
        preview_exit = True

    if preview_exit is False:
        redraw = redraw_preview
        wt_ui.Tsysmenu.setcurrent(0, menu_preview)
        wt_ui.Tsysmenu.setcurrent(1, None)
        mainproc_stop()
    else:
        redraw = redraw_main
        wt_ui.Tsysmenu.setcurrent(0, mainmenu)
        wt_ui.Tsysmenu.setcurrent(1, popupmenu)
        del prev_image
        del prev_coord
        mainproc_start()


def preview_calc():
    global prev_image, prev_coord, prev_vert
    if prev_vert is True:
        img = imwin.img.transpose(graphics.ROTATE_270)
    else:
        img = imwin.img
    aspect_x = float(img.size[0]) / float(canv.size[0])
    aspect_y = float(img.size[1]) / float(canv.size[1])
    aspect = max(aspect_x, aspect_y)
    if aspect < 1:
        return False
    elif prev_vert is True:
        prev_image = new_image((img.size[0] / aspect, img.size[1] / aspect))
    else:
        prev_image = new_image((img.size[0] / aspect, img.size[1] / aspect))
    if prev_image is None:
        return False

    prev_image.blit(img, scale=1)
    prev_coord = [
        canv.size[0] / 2 - prev_image.size[0] / 2,
        canv.size[1] / 2 - prev_image.size[1] / 2]
    prev_vert = not prev_vert
    return True


def preview_control(evt):
    if evt['scancode'] == key_codes.EScancodeRightSoftkey:
        preview_hide(True)


def zoom_multiply_query():
    z = appuifw.query(dtext['zoom_multiply'], 'number', imwin.zoom)
    zoom_multiply(z)


def templet_create():
    mbox_percent.draw(dtext['templet'])
    (img, msk) = GetSelectedImage()
    image = copy_image(img)
    (mask, msk) = improc._image_tomaskwhite((image, msk), inttorgb(foreclr), updatecallback)
    templet_save(img, mask)


def templet_save(img, mask):
    global lastpath_temp
    dirname = dialog_tmp.open(path=ur(lastpath_temp), ext=[
        'tmb'], kind='save')
    if dirname is None:
        return None

    if path.isfile(ur(dirname)):
        defname = path.split(dirname)[1]
    else:
        defname = u'templet'
    dirname = path.split(dirname)[0] + '\\'
    dirname = dirname.replace('\\\\', '\\')
    lastpath_temp = dirname
    name = appuifw.query(dtext['entername'], 'text', defname)
    if name is None:
        return None

    fname = dirname + name
    mname = dirname + name
    if fname[-4:].lower() != '.tmb':
        fname = fname + '.tmb'

    if mname[-4:].lower() != '.tmb':
        mname = mname + '.msk'
    else:
        mname = mname[:len(mname) - 4] + '.msk'
    appuifw.note(dtext['saved'] + unicode(fname))
    img.save(fname, format='PNG')
    mask.save(mname, format='PNG', bpp=8)


def templet_load():
    global lastpath_temp, templet
    fname = dialog_tmp.open(path=ur(lastpath_temp), ext=[
        'tmb'], kind='open')
    if fname is None:
        return None

    lastpath_temp = path.split(fname)[0]
    templet = [
        None,
        None]
    templet[0] = graphics.Image.open(fname)
    if templet[0] is None:
        appuifw.note(dtext['tempbroken'], 'error')
        return None

    templet[1] = graphics.Image.open(fname[:len(fname) - 4] + '.msk')
    if templet[1] is None:
        appuifw.note(dtext['tempbroken'], 'error')
        return None

    templet[1] = image_convertbpp(templet[1], 'L')
    if appuifw.query(dtext['originalcolors'], 'query') is None:
        templet[0].clear(foreclr)

    im = new_image(iconsize)
    if im is None:
        return None

    im2 = new_image(templet[0].size)
    if im2 is None:
        return None

    im2.blit(templet[0], mask=templet[1])
    im2 = im2.resize(iconsize)
    im.blit(im2)
    im.rectangle((-1, -1, iconsize[0], iconsize[1]), fill=None, outline=0)

    try:
        toolslist.icon((1, 1), im)
    except:
        None
        None
        None
        appuifw.note(u"Can't create icon")
        return None


def templet_draw(canv, x, y):
    if templet is not None:
        canv.blit(templet[0], target=(x, y), mask=templet[1])


def templet_fromfile():
    global templet
    fname = dialog.open(path=ur(con.lastpath_img), ext=[
        'jpg',
        'png',
        'gif',
        'bmp',
        'mbm',
        'jpeg'], kind='open')
    if fname is None:
        return None

    con.lastpath_img = path.split(fname)[0]
    templet = [
        None,
        None]
    templet[0] = graphics.Image.open(fname)
    image = new_image(templet[0].size)
    if image is None:
        return None

    templet[1] = image
    templet[1] = image_convertbpp(templet[1], 'L')
    im = new_image((24, 24))
    if im is None:
        return None

    im2 = new_image(templet[0].size)
    if im2 is None:
        return None

    im2.blit(templet[0], mask=templet[1])
    im2 = im2.resize((24, 24))
    im.blit(im2)
    im.rectangle((0, 0, 24, 24), fill=None, outline=0)

    try:
        toolslist.icon((1, 1), im)
    except:
        None
        None
        None
        return imwin


def colorgen():
    rgb = [
        255,
        255,
        255]
    size = 12
    dd = 48
    hh = dd / 2
    maxc = 576
    midc = 271
    minc = 288
    for t in xrange(1, palette_size[1]):
        if t == 1:
            rgb = [
                255,
                255,
                255]
            d = [
                hh,
                hh,
                hh]
        elif t == 3:
            rgb = [
                maxc,
                minc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 5:
            rgb = [
                maxc,
                maxc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 7:
            rgb = [
                minc,
                maxc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 9:
            rgb = [
                minc,
                maxc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 11:
            rgb = [
                minc,
                minc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 13:
            rgb = [
                maxc,
                minc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 4:
            rgb = [
                maxc,
                midc,
                minc]
            d = [
                dd,
                hh,
                dd]
        elif t == 6:
            rgb = [
                midc,
                maxc,
                minc]
            d = [
                hh,
                dd,
                dd]
        elif t == 8:
            rgb = [
                minc,
                maxc,
                midc]
            d = [
                dd,
                dd,
                hh]
        elif t == 10:
            rgb = [
                minc,
                midc,
                maxc]
            d = [
                dd,
                hh,
                dd]
        elif t == 12:
            rgb = [
                midc,
                minc,
                maxc]
            d = [
                hh,
                dd,
                dd]
        elif t == 2:
            rgb = [
                maxc,
                minc,
                midc]
            d = [
                dd,
                dd,
                hh]

        for n in xrange(palette_size[0]):
            if n < palette_size[0]:
                c = [
                    0,
                    0,
                    0]
                for i in xrange(3):
                    c[i] = rgb[i] - d[i] * n
                    if c[i] > 255:
                        c[i] = 255

                    if c[i] < 0:
                        c[i] = 0

                cc = 256 * 256 * c[0] + 256 * c[1] + c[2]
                col[n][t] = cc
                colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
                colors[n][t].rectangle((1, 0, size, size - 1), outline=cc, fill=cc)
            else:
                c = [
                    255,
                    255,
                    255]
                cc = 256 * 256 * c[0] + 256 * c[1] + c[2]
                col[n][t] = cc
                colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
                colors[n][t].rectangle((1, 0, size, size - 1), outline=cc, fill=cc)


def colorload():
    rgb = [
        255,
        255,
        255]
    size = 12
    d = 64
    maxc = 383
    minc = 128
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
            colors[n][t].rectangle((1, 0, size, size - 1), outline=col[n][t], fill=col[n][t])


def statusbar():
    buff.rectangle((0, workzone[1], con.screen_size[0], con.screen_size[1]), outline=0, fill=con.ui_form_color[0])
    buff.rectangle((15, con.screen_size[1] - 12, 22, con.screen_size[1] - 2), outline=0, fill=foreclr)
    buff.rectangle((23, con.screen_size[1] - 12, 30, con.screen_size[1] - 2), outline=0, fill=backclr)
    if colorgrid.hdn:
        msg = u'%d:%d' % ((imwin.curs.x - imwin.x) + imwin.imx, (imwin.curs.y - imwin.y) + imwin.imy)
        if curtool == tool['lasso']:
            if imwin.selector.isactive():
                (l, u, r, b) = imwin.selector.getcoord()
                msg += u' %dx%d' % ((r - l) + 1, (b - u) + 1)

        elif curtool == tool['selector'] or curtool == tool['elselector']:
            if imwin.selector.isactive():
                msg += u' %dx%d' % (abs(imwin.selector.tool.bcoord[2] - imwin.selector.tool.bcoord[0]) + 1,
                                    abs(imwin.selector.tool.bcoord[3] - imwin.selector.tool.bcoord[1]) + 1)

        elif tool_line.enabled():
            msg += u' %dx%d' % (
            abs(tool_line.bcoord[2] - tool_line.bcoord[0]) + 1, abs(tool_line.bcoord[3] - tool_line.bcoord[1]) + 1)
        elif tool_ellps.enabled():
            msg += u' %dx%d' % (
            abs(tool_ellps.bcoord[2] - tool_ellps.bcoord[0]) + 1, abs(tool_ellps.bcoord[3] - tool_ellps.bcoord[1]) + 1)
        elif tool_rect.enabled():
            msg += u' %dx%d' % (
            abs(tool_rect.bcoord[2] - tool_rect.bcoord[0]) + 1, abs(tool_rect.bcoord[3] - tool_rect.bcoord[1]) + 1)
        elif curtool == tool['picker']:
            msg += unicode(
                imwin.img.getpixel(((imwin.curs.x - imwin.x) + imwin.imx, (imwin.curs.y - imwin.y) + imwin.imy))[0])

        buff.text((33, statustexty), msg, font=con.ui_status_font, fill=con.ui_form_color[1])
    else:
        x = colorgrid.curitem()[0]
        y = colorgrid.curitem()[1]
        if y > 0:
            buff.text((33, statustexty), u'%s' % (inttorgb(col[x][y]),), font=con.ui_status_font,
                      fill=con.ui_form_color[1])

    if icon_tool is not None:
        buff.blit(icon_tool[toolslist.curitem()[0] * toolslist.lst[0].itcnt + toolslist.curitem()[1]],
                  target=(0, con.screen_size[1] - 14))

    if imwin.drawing:
        buff.rectangle((0, con.screen_size[1] - 13, 14, con.screen_size[1]), outline=16711680, fill=None, width=1)


def config():
    appuifw.app.screen = 'normal'
    optform.execute()
    config_updatefromform()
    menu_create()
    appuifw.app.screen = 'full'
    clist = []
    conflist = config_getlist()
    for t in conflist:
        clist.append(int(t))

    config_reset(clist)


def config_updatefromform():
    global dtext, mtext
    con.toolbar_slidespeed = int(optform[1][2][1]) + 1
    gradgrid.setslidespeed(gradgrid.getsize()[0] / con.toolbar_slidespeed)
    colorgrid.setslidespeed(colorgrid.getsize()[0] / con.toolbar_slidespeed)
    toolslist.setslidespeed(toolslist.getsize()[0] / con.toolbar_slidespeed)
    imwin.curs.kind = optform[2][2][1]
    con.cursor = optform[2][2][1]
    imwin.curs.size = int(optform[3][2][1]) + 1
    con.cursorsize = int(optform[3][2][1]) + 1
    con.cursormultiplier = optform[4][2]
    con.undo_size = int(optform[5][2][1])
    imwin.setundosize(con.undo_size)
    con.rectselecttype = int(optform[6][2][1])
    con.exitconfirm = int(optform[7][2][1])
    newlang = con.lang_list[optform[0][2][1]]
    if con.lang != newlang:
        con.lang = newlang
        dtext = lang_readfromfile(program_path, con.lang, __version__)
        mtext = {
            'ok': dtext['ok'],
            'cancel': dtext['cancel']}

    for t in xrange(len(con.custompal)):
        if con.custompal[t] != '':
            palette_checkcustom(t, con.custompal[t])

    dialog.createmenu(dtext)
    dialog_tmp.createmenu(dtext)
    dialog_pal.createmenu(dtext)
    dialog_img.createmenu(dtext)


def config_getlist():
    valuelist = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0]
    valuelist[0] = optform[0][2][1]
    valuelist[1] = optform[1][2][1]
    valuelist[2] = optform[2][2][1]
    valuelist[3] = optform[3][2][1]
    valuelist[4] = optform[4][2]
    valuelist[5] = optform[5][2][1]
    valuelist[6] = optform[6][2][1]
    valuelist[7] = optform[7][2][1]
    return valuelist


def config_reset(valuelist=None):
    global optcont, optform
    if valuelist is None:
        valuelist = [
            con.lang_list.index(u'english'),
            2,
            0,
            4,
            5,
            1,
            0,
            1]

    optcont = [
        (dtext['language'], 'combo', (con.lang_list, valuelist[0])),
        (dtext['toolslidespeed'], 'combo', ([
                                                dtext['immediately'],
                                                dtext['veryfast'],
                                                dtext['fast'],
                                                dtext['medium'],
                                                dtext['slow'],
                                                dtext['veryslow']], valuelist[1])),
        (dtext['cursortype'], 'combo', ([
                                            dtext['cursor_bw'],
                                            dtext['cursor_blink'],
                                            dtext['cursor_invers']], valuelist[2])),
        (dtext['cursorsize'], 'combo', ([
                                            u'1',
                                            u'2',
                                            u'3',
                                            u'4',
                                            u'5'], valuelist[3])),
        (dtext['changecursor'], 'number', valuelist[4]),
        (dtext['undosize'], 'combo', ([
                                          u'0',
                                          u'1',
                                          u'2',
                                          u'3',
                                          u'4',
                                          u'5'], valuelist[5])),
        (dtext['rectselect'], 'combo', ([
                                            dtext['immobile'],
                                            dtext['mobile']], valuelist[6])),
        (dtext['confirmonexit'], 'combo', ([
                                               dtext['no'],
                                               dtext['yes']], valuelist[7]))]
    optform = appuifw.Form(optcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    return valuelist


def he(state):
    if state is None:
        return 'None'

    return '%06x' % state


def config_load():
    try:
        valuelist = con.load(program_path)
        config_reset(valuelist)
        config_updatefromform()
        config_reset(valuelist)
    except Exception:
        None
        exc = None
        None
        traceback.print_exc(sys.stderr)
        con.lastpath_img = 'C:\\'
        ans = appuifw.query(dtext['confbroken'], 'query')
        if ans is None:
            sys.stderr.close()
            abort()

        config_reset()
        config_updatefromform()
    except:
        None


def define_screen_size():
    try:
        parser = iniparser.TIniParser()
        parser.open(program_path + 'config.ini')
        parser.readgroup('DISPLAY')
        val = parser.readstr('force_display_size', None, ',')
        if val != [
            'None']:

            try:
                size = (int(val[0]), int(val[1]))
                con.screen_size = size
            except:
                None
                None
                None
                con.screen_size = display_pixels()

        else:
            con.screen_size = display_pixels()
        parser.close()
    except:
        None
        None
        None
        con.screen_size = display_pixels()


def focusaction(state):
    if state == 0:
        applock.wait()
    else:
        applock.signal()


def menu_recent():
    if con.recentfiles:
        #continue
        rfiles = [path.split(x)[1] for x in con.recentfiles]
        ind = appuifw.popup_menu(rfiles, dtext['recentfiles'] + ':')
        if ind is None:
            return None
        else:
            _file_open(con.recentfiles[ind], False)
    else:
        showtipex(u'No recents')


def menu_start_hide():
    global redraw
    mainproc_start()
    redraw = redraw_main


def joke():
    appuifw.note(dtext['joke'])


def menu_create():
    global mainmenu, menu_palette, menu_palette2, menu_palette3, menu_preview, popupmenu, menu_start, menu_selection, menu_about, mess_info, mess_tip
    (extmenu, extabout) = plugins_load()
    mainmenu = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, ((dtext['file'], (
    (dtext['open'], (lambda: file_open(False))), (dtext['openinnew'], (lambda: file_open(True))),
    (dtext['reopen'], (lambda: file_reopen(False))), (dtext['new'], (lambda: query_file_new(False))),
    (dtext['newinnew'], (lambda: query_file_new(True))), (dtext['save'], (lambda: file_save())),
    (u'%s%s' % (dtext['saveas'], '...'), (lambda: file_saveas(True))),
    (u'%s%s' % (dtext['recentfiles'], '...'), menu_recent), (dtext['close'], file_close))), (dtext['edit'], (
    (dtext['undo'], undo), (dtext['redo'], redo), (dtext['cut'], clipcut), (dtext['copy'], clipcopy),
    (dtext['paste'], clippaste), (dtext['clear'], clipclear), (dtext['blend'], setblend))), (dtext['select'], (
    (u'%s%s' % (dtext['select'], '...'), selectsize), (dtext['selectall'], selectall),
    (dtext['invert'], (lambda: imwin.selector.invert_selection())),
    (dtext['deselect'], (lambda: imwin.selector.deselect())))), (dtext['zoom'], (
    (dtext['zoomin'], zoom_in), (dtext['zoomout'], zoom_out), (dtext['zoom_multiply'], zoom_multiply_query),
    (dtext['zoom_1_1'], zoom_1_1))), (dtext['font'], (
    (dtext['entertext'], settext), (dtext['stdfont'], fontstd_select), (dtext['extfont'], font_open),
    (dtext['stdfontopt'], fontstd_opt), (dtext['extfontopt'], font_opt))), (dtext['tools'], (
    (dtext['templet'], templet_create), (dtext['loadtemplet'], templet_load),
    (dtext['templetfromfile'], templet_fromfile), (dtext['exportpal'], palette_export),
    (dtext['importpal'], palette_import),
    (u'%s%s' % (dtext['batchproc'], '...'), (lambda: batch.open(con.lastpath_img))))), (dtext['image'], (
    (dtext['info'], fileinfo), (dtext['preview'], (lambda: preview_hide(False))), (dtext['resize'], image_resize_query),
    (dtext['resizecanvas'], image_resizecanvas_query), (dtext['cropsel'], image_crop), (dtext['rotate'], image_rotate),
    (dtext['flip'], image_flip), (dtext['displacement'], image_displacement),
    (dtext['replacecolor'], image_replacecolor_query), (dtext['makemask'], image_tomask))), (dtext['filter'], (
    (dtext['blur'], image_blur_query), (dtext['lightness'], image_lightness_query),
    (dtext['darkness'], image_darkness_query), (dtext['blackwhite'], (lambda: image_bpp('1'))),
    (dtext['grayscale'], (lambda: image_bpp('L'))), (dtext['posterize'], image_posterize),
    (dtext['invertcolors'], image_invertcolors), (dtext['colorbalance'], image_colorbalance),
    (dtext['saturation'], image_saturation), (dtext['sepia'], image_sepia), (dtext['gradient'], gradgrid.unlockandshow),
    (dtext['fractal'], ((dtext['julia'], image_fractal), (dtext['mandelbrot'], image_fractal_mandelbrot))))), extmenu, (
                                                            dtext['option'], ((dtext['config'], config), (
                                                            dtext['keyconfig'], (lambda: con.keyconfig.execute())), (
                                                                              u'%s%s' % (dtext['skinselect'], '...'),
                                                                              skin_select),
                                                                              (dtext['colortheme'], theme_open),
                                                                              (dtext['help'], help), (dtext['about'], (
                                                                lambda: about_hide(False))))),
                                                            (dtext['switchwin'], imwindow_next), (dtext['exit'], exit)),
                              con.ui_menu_font)
    mainmenu.keylessitem(0, mainmenu.getitemindex(0, dtext['exit']))
    mainmenu.hiden(True)
    mainmenu.spaces(def_spaces)
    mainmenu.sidespace(18)
    mainmenu.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        mainmenu.forcetextheight(con.ui_menu_font_fheight)

    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        mainmenu.itemblocked(8, mainmenu.getitemindex(8, dtext['blur']), True)

    if s60_version_info != (3, 0):
        mainmenu.itemblocked(5, mainmenu.getitemindex(5, dtext['stdfontopt']), True)

    def menu_main_hide():
        mainproc_start()
        keyboard.resetkeys()

    mainmenu.onhide = menu_main_hide
    mainmenu.onshow = menu_main_onshow
    wt_ui.Tsysmenu.setcurrent(0, mainmenu)
    menu_palette = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, (
    (dtext['settoforecolor'], _setforecolor), (dtext['settobackcolor'], _setbackcolor),
    (dtext['setfromforecolor'], palette_setcell), (dtext['change'], colormixer), (dtext['exportpal'], palette_export),
    (dtext['importpal'], palette_import), (dtext['reset'], palette_reset), (dtext['cancel'], colorgrid.hideandblock)),
                                  con.ui_menu_font)
    menu_palette.hiden(True)
    menu_palette.spaces(def_spaces)
    menu_palette.sidespace(18)
    menu_palette.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette.forcetextheight(con.ui_menu_font_fheight)

    menu_palette.onhide = mainproc_start
    menu_palette.onshow = mainproc_stop
    menu_palette2 = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, (
    (dtext['setcustompal'], palette_selectcustom), (dtext['clear'], palette_clearcustom),
    (dtext['cancel'], colorgrid.hideandblock)), con.ui_menu_font)
    menu_palette2.hiden(True)
    menu_palette2.spaces(def_spaces)
    menu_palette2.sidespace(18)
    menu_palette2.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette2.forcetextheight(con.ui_menu_font_fheight)

    menu_palette2.onhide = mainproc_start
    menu_palette2.onshow = mainproc_stop
    menu_palette3 = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff,
                                   ((u'  joke ;)', joke), (dtext['cancel'], colorgrid.hideandblock)), con.ui_menu_font)
    menu_palette3.hiden(True)
    menu_palette3.spaces(def_spaces)
    menu_palette3.sidespace(18)
    menu_palette3.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette3.forcetextheight(con.ui_menu_font_fheight)

    menu_palette3.onhide = mainproc_start
    menu_palette3.onshow = mainproc_stop
    menu_preview = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff,
                                  ((dtext['rotate'], preview_calc), (dtext['close'], preview_hide)), con.ui_menu_font)
    menu_preview.spaces(def_spaces)
    menu_preview.sidespace(18)
    menu_preview.coord('leftbottom')
    menu_preview.hiden(True)
    if con.ui_menu_font_fheight is not None:
        menu_preview.forcetextheight(con.ui_menu_font_fheight)

    menu_preview.onhide = mainproc_start
    menu_preview.onshow = mainproc_stop
    rmenupares = ((dtext['undo'], undo), (dtext['redo'], redo), (dtext['cut'], clipcut), (dtext['copy'], clipcopy),
                  (dtext['paste'], clippaste), (dtext['clear'], clipclear))
    popupmenu = wt_ui.Tsysmenu(1, 'rightbottom', canv, buff, rmenupares, con.ui_menu_font)
    popupmenu.hiden(True)
    popupmenu.spaces(def_spaces)
    popupmenu.sidespace(18)
    popupmenu.coord('rightbottom')
    if con.ui_menu_font_fheight is not None:
        popupmenu.forcetextheight(con.ui_menu_font_fheight)

    def menu_popup_hide():
        mainproc_start()
        keyboard.resetkeys()

    popupmenu.onhide = menu_popup_hide
    popupmenu.onshow = menu_popup_onshow
    wt_ui.Tsysmenu.setcurrent(1, popupmenu)
    if menu_start_off is False:
        smenupares = (
        (dtext['open'].upper(), (lambda: file_open(False))), (dtext['new'].upper(), (lambda: query_file_new(False))),
        (dtext['exit'].upper(), exit))
        menu_start = wt_ui.Tmultimenu('center', buff, None, smenupares, con.ui_menu_font)
        menu_start.spaces(def_spaces)
        menu_start.sidespace(18)
        menu_start.coord('center')
        menu_start.onhide = menu_start_hide
        menu_start.colors(con.ui_menu_color)

    menu_selection_pares = ((dtext['cut'], clipcut), (dtext['copy'], clipcopy), (dtext['clear'], clipclear), (
    dtext['select'], ((u'%s%s' % (dtext['select'], '...'), selectsize), (dtext['selectall'], selectall),
                      (dtext['invert'], (lambda: imwin.selector.invert_selection())),
                      (dtext['deselect'], (lambda: imwin.selector.deselect())))), (dtext['image'], (
    (dtext['cropsel'], image_crop), (dtext['rotate'], image_rotate), (dtext['flip'], image_flip),
    (dtext['displacement'], image_displacement), (dtext['makemask'], image_tomask))), (dtext['filter'], (
    (dtext['blur'], image_blur_query), (dtext['lightness'], image_lightness_query),
    (dtext['darkness'], image_darkness_query), (dtext['blackwhite'], (lambda: image_bpp('1'))),
    (dtext['grayscale'], (lambda: image_bpp('L'))), (dtext['posterize'], image_posterize),
    (dtext['invertcolors'], image_invertcolors), (dtext['colorbalance'], image_colorbalance),
    (dtext['saturation'], image_saturation), (dtext['sepia'], image_sepia), (dtext['gradient'], gradgrid.unlockandshow),
    (dtext['fractal'], ((dtext['julia'], image_fractal), (dtext['mandelbrot'], image_fractal_mandelbrot))))), extmenu)
    menu_selection = wt_ui.Tmultimenu('center', buff, None, menu_selection_pares, con.ui_menu_font)
    menu_selection.spaces(def_spaces)
    menu_selection.sidespace(18)
    menu_selection.coord('center')
    menu_selection.colors(con.ui_menu_color)
    menu_selection.hiden(True)

    def menu_selection_hide():
        mainproc_start()
        keyboard.resetkeys()

    menu_selection.onhide = menu_selection_hide
    menu_selection.onshow = mainproc_stop
    mainmenu.colors(con.ui_menu_color)
    menu_preview.colors(con.ui_menu_color)
    menu_palette.colors(con.ui_menu_color)
    menu_palette2.colors(con.ui_menu_color)
    menu_palette3.colors(con.ui_menu_color)
    popupmenu.colors(con.ui_menu_color)
    mbox_percent.clrs = [
        con.ui_menu_color[1][2],
        con.ui_menu_color[1][1],
        con.ui_menu_color[1][3]]
    progressbar.color(con.ui_prog_color)
    mess = [
        u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe ' + app_versionstr,
        u'',
        u'\xe5\x85\x8d\xe8\xb4\xb9\xe7\x9a\x84\xe5\x9b\xbe\xe5\x83\x8f\xe7\xbc\x96\xe8\xbe\x91\xe8\xbd\xaf\xe4\xbb\xb6',
        u'\xc2\xa9 2007-2009 Plyaskin Anton',
        u'',
        u'',
        u'\xe4\xbd\x9c\xe8\x80\x85\xef\xbc\x9a',
        u'  Plyaskin Anton aka werton',
        u'\xe7\xbd\x91\xe7\xab\x99\xef\xbc\x9a',
        u'  www.werton.wen.ru',
        u'',
        u'\xe6\x84\x9f\xe8\xb0\xa2\xef\xbc\x9a',
        u'',
        u'  Sveark - \xe6\x8f\x90\xe4\xbe\x9bPNG',
        u'\xe9\x80\x8f\xe6\x98\x8e\xe5\xba\xa6\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  _killed_ - \xe6\x8f\x90\xe4\xbe\x9bMBM',
        u'\xe8\xbe\x9e\xe5\x85\xb8',
        u'',
        u'  MACTEP3230 - \xe6\x8f\x90\xe4\xbe\x9b\xe5\xa1\xab\xe5\x85\x85',
        u'\xe5\x87\xbd\xe6\x95\xb0\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  Deftrue - \xe6\x8f\x90\xe4\xbe\x9b\xe7\xba\xbf\xe6\x80\xa7',
        u'\xe6\xbb\xa4\xe6\xb3\xa2\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  Troicat - \xe6\x8f\x90\xe4\xbe\x9bs60 v3',
        u'\xe7\xa8\x8b\xe5\xba\x8f\xe5\x9b\xbe\xe6\xa0\x87',
        u'',
        u'  Trojan_73 - \xe6\x94\xb6\xe9\x9b\x86\xe8\xb0\x83\xe8\x89\xb2\xe6\x9d\xbf',
        u'\xe5\xb9\xb6\xe5\xb8\xae\xe5\x8a\xa9\xe5\x8d\x87\xe7\xba\xa7',
        u'',
        u'',
        u'\xe6\x84\x9f\xe8\xb0\xa2\xe4\xbb\xa5\xe4\xb8\x8b\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98\xef\xbc\x9a',
        u'',
        u'  Slavasyrota',
        u'  7755',
        u'  Trojan_73',
        u'  Armen-82.08',
        u'  EDGE84',
        u'  kuharsanek',
        u'  kusya1612',
        u'  filja2',
        u'',
        u'',
        u'\xe9\x83\xa8\xe5\x88\x86\xe5\x9b\xbe\xe6\xa0\x87\xe6\x9d\xa5\xe8\x87\xaa',
        u'\xe6\x88\x96\xe5\x9f\xba\xe4\xba\x8eGIMP 2.6',
        u'\xc2\xa9 1995-2008 Spencer Kimball',
        u'Peter Mattis & GIMP devteam',
        u'']
    ind = mess.index(
        u'\xe6\x84\x9f\xe8\xb0\xa2\xe4\xbb\xa5\xe4\xb8\x8b\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98\xef\xbc\x9a')
    ind -= 1
    mess[ind:ind] = extabout
    mess_eegg[:] = mess
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'\xe6\xb1\x89\xe5\x8c\x96\xef\xbc\x9aSeawave;)')
    menu_about = wt_ui.Tmessageform('center', buff,
                                    (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2]), mess,
                                    con.ui_menu_font)
    menu_about.hiden(True)
    menu_about.setcallback(about_hide)
    menu_about.scrollspd = 1
    mess = [
        u'File name: ']
    mess_info = wt_ui.Tmessageform('center', buff,
                                   (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2]), mess,
                                   con.ui_menu_font)
    mess_info.blspace = 4
    mess_info.message(mess, con.ui_menu_font)
    mess_info.hiden(True)
    mess_info.setcallback(mainproc_start)
    mess_tip = wt_ui.Tmessageform('center', buff,
                                  (con.ui_form_color[0], con.ui_menu_color[0][1], con.ui_menu_color[1][3]), [
                                      u''], con.ui_menu_font)
    mess_tip.boxstyle = 1
    mess_tip.borderwidth = 2
    mess_tip.corner = 2
    mess_tip.blspace = 2
    mess_tip.message([
        u'Wellcome to',
        u'ImageDesigner!'], con.ui_menu_font_bold)
    mess_tip.messtimeout = 1
    mess_tip.hiden(True)
    check_imwincount()


def rightmenu():
    if mainmenu.hiden() is False:
        mainmenu.hiden(True)


def fileinfo():
    if imwin.filename is not None:
        mess = [
            u'%s: %s' % (dtext['name'], path.split(imwin.filename)[1]),
            u'%s: %d %s ' % (dtext['size'], stat(ur(imwin.filename))[6] / 1024, dtext['kb']),
            u'%s: %d x %d' % (dtext['resolution'], imwin.img.size[0], imwin.img.size[1])]
    else:
        mess = [
            u'%s:' % dtext['name'],
            u'%s:' % dtext['size'],
            u'%s: %d x %d' % (dtext['resolution'], imwin.img.size[0], imwin.img.size[1])]
    mess_info.blspace = 4
    mess_info.message(mess, con.ui_menu_font)
    mess_info.setcallback(mainproc_start)
    mess_info.hiden(False)
    mainproc_stop()


def menu_main_onshow():
    wt_ui.Ticongrid.hideall()
    mainproc_stop()
    if len(imagewindow) == 1:
        mainmenu.itemblocked(0, mainmenu.getitemindex(0, dtext['switchwin']), True)
    else:
        mainmenu.itemblocked(0, mainmenu.getitemindex(0, dtext['switchwin']), False)
    if not (con.recentfiles):
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['recentfiles'] + '...'), True)
    else:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['recentfiles'] + '...'), False)
    if imwin.zoom == 1:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomout']), True)
    else:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomout']), False)
    if imwin.zoom == 50:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomin']), True)
    else:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomin']), False)
    if not imwin.selector.isactive():
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['deselect']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['copy']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['cut']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['clear']), True)
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), True)
    else:
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['deselect']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['copy']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['cut']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['clear']), False)
        if curtool == tool['magicrod']:
            mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), False)
        else:
            mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), True)
    if classes.TUniSlector.copybuff is None:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['paste']), True)
    else:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['paste']), False)
    if imwin.filename is None:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['reopen']), True)
    else:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['reopen']), False)
    if imwin.undosize != 0:
        if imwin.redostack[-1] is None:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), True)
        else:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), False)
        if imwin.undostack[-1] is None:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), True)
        else:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), False)
    else:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), True)


def menu_popup_onshow():
    mainproc_stop()
    if not imwin.selector.isactive():
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['copy']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['cut']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['clear']), True)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['copy']), False)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['cut']), False)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['clear']), False)
    if classes.TUniSlector.copybuff is None:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['paste']), True)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['paste']), False)
    if imwin.undosize != 0:
        if imwin.redostack[-1] is None:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), True)
        else:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), False)
        if imwin.undostack[-1] is None:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), True)
        else:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), False)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), True)


def menu_palette_onshow():
    mainproc_stop()


def mainproc_start():
    onnextcicle_do(_mainproc_start)


def mainproc_stop():
    onnextcicle_do(_mainproc_stop)


def _mainproc_start():
    global main_event_proc
    main_event_proc = True
    if wt_ui.Ticongrid.isallhiden():
        imwin.blckd = False
        con.keyconfig.hotkeys_on()


def _mainproc_stop():
    global main_event_proc
    main_event_proc = False
    imwin.blckd = True
    con.keyconfig.hotkeys_clear()


def nextcicle_waiter():
    global ciclefunctions
    if ciclefunctions:
        for t in ciclefunctions:
            t()

        ciclefunctions = []


def onnextcicle_do(funct):
    ciclefunctions.append(funct)


def about_hide(state=True):
    global redraw
    menu_about.hiden(state)
    if menu_about.hiden():
        redraw = redraw_main
        mainproc_start()
    else:
        redraw = redraw_about
        mainproc_stop()


def ru(s):
    return s.decode('utf-8')


def ur(s):
    return s.encode('utf-8')


def skin_load(folder):
    imopen = graphics.Image.open
    icon = [
        imopen(folder + 'Pencil_32.png'),
        imopen(folder + 'Brush_32.png'),
        imopen(folder + 'Erase_32.png'),
        imopen(folder + 'Line2_32.png'),
        imopen(folder + 'Rect_32.png'),
        imopen(folder + 'Ellipse_32.png'),
        imopen(folder + 'Select_32.png'),
        imopen(folder + 'El_Select.png'),
        imopen(folder + 'Cstamp_32.png')]
    pbar.percent(30)
    pbar.draw()
    icon2 = [
        imopen(folder + 'Picker_32.png'),
        imopen(folder + 'Notemlet_32.png'),
        imopen(folder + 'Text_32.png'),
        imopen(folder + 'Polygon_32.png'),
        imopen(folder + 'Broken_32.png'),
        imopen(folder + 'PaintBucket_32.png'),
        imopen(folder + 'Spray_32.png'),
        imopen(folder + 'Lasso.png'),
        imopen(folder + 'mrod.png')]
    icon3 = [
        imopen(folder + 'Grad_vert.png'),
        imopen(folder + 'Grad_cir.png')]
    icon4 = [
        imopen(folder + 'Grad_gor.png'),
        imopen(folder + 'Grad_rect.png')]
    icon5 = []
    icon5.append(imopen(folder + 'f.png'))
    icon5.append(imopen(folder + 'c.png'))
    icon5.append(imopen(folder + 'b.png'))
    icon5.append(imopen(folder + 'black-white.png'))
    icon5.append(imopen(folder + 'color_black.png'))
    icon5.append(imopen(folder + 't.png'))
    icon6 = imopen(folder + 'color_white.png')
    pbar.percent(60)
    pbar.draw()
    icon7 = [
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None]]
    icon7[0][0] = imopen(folder + 'drive.png')
    icon7[0][1] = new_image(icon7[0][0].size, '1')
    icon7[0][1].load(folder + 'drive_mask.png')
    icon7[1][0] = imopen(folder + 'dir.png')
    icon7[1][1] = new_image(icon7[1][0].size, '1')
    icon7[1][1].load(folder + 'dir_mask.png')
    icon7[2][0] = imopen(folder + 'im_green.png')
    icon7[3][0] = imopen(folder + 'im_blue.png')
    icon7[4][0] = imopen(folder + 'im_red.png')
    icon7[5][0] = imopen(folder + 'im_yellow.png')
    icon7[6][0] = imopen(folder + 'im_gray.png')
    icon7[7][0] = icon7[2][0]
    icon7[2][1] = new_image(icon7[2][0].size, '1')
    icon7[3][1] = new_image(icon7[2][0].size, '1')
    icon7[4][1] = new_image(icon7[2][0].size, '1')
    icon7[5][1] = new_image(icon7[2][0].size, '1')
    icon7[6][1] = new_image(icon7[2][0].size, '1')
    icon7[7][1] = new_image(icon7[2][0].size, '1')
    icon8 = [
        None,
        None,
        None,
        None,
        None,
        None]
    for t in (1, 2, 3, 4, 5, 6):
        icon8[t - 1] = imopen(folder + str(t) + '.png')

    return (icon, icon2, icon3, icon4, icon5, icon6, icon7, icon8)


def skin_define(program_path):
    parser = iniparser.TIniParser()

    try:
        parser.open(program_path + 'config.ini')
        parser.readgroup('MISC')
        con.skin = parser.readstr('skin', 'default')
    except:
        None
        None
        None
        con.skin = 'default'

    return con.skin


app_versionstr = u'v.%s' % _version_
con = conf.Cconf()
(con.lang_list, con.lang, dtext) = lang_load(program_path, __version__)
mtext = {
    'ok': dtext['ok'],
    'cancel': dtext['cancel']}
define_screen_size()
if s60_version_info == (1, 2) or s60_version_info == (2, 0):
    appuifw.note(u'S60 1st and 2nd edition fp1 are no supported.', 'error')
    abort()

if s60_version_info == (3, 0):
    con.ui_menu_font = (u'Nokia Hindi S60', None, graphics.FONT_NO_ANTIALIAS)
    con.ui_menu_font_bold = ('dense', None, graphics.FONT_BOLD)
    con.ui_status_font = (u'Nokia Hindi S60', 13)
else:
    con.ui_menu_font = (u'Sans MT 936_s60', None)
    con.ui_menu_font_bold = (u'LatinBold12', None)
    con.ui_status_font = (u'Sans MT 936_s60', None)
lastpath_temp = program_path + 'templet\\'
lastpath_fnt = program_path + 'Fonts\\'
lastpath_pal = program_path + 'Palette\\'
noicon = False
iconsize = (28, 28)
con.undo_size = 1
con.cursormultiplier = 8
con.cursor = 0
con.cursorsize = 3
con.custompal = [
    '',
    '',
    '',
    '',
    '',
    '']
con.lastpath_img = 'c:\\'
scrollbarwidth = 4
workzone = [
    con.screen_size[0] - scrollbarwidth,
    con.screen_size[1] - 17]
updatezone = (0, 0, workzone[0], workzone[1])
fontflags = [
    0,
    0,
    0]
stdfontsize = 14
fntsymbolsdelay = 1
statustexty = con.screen_size[1] - 2
menu_start_off = True
foreclr = 0
backclr = 16777215
kevent = None
preview_exit = True
prev_vert = False
prev_image = None
prev_coord = None
icon_tool = None
con.rectselecttype = 0
templet = None
gtext = None
filename = ''
palette_size = [
    12,
    14]
#continue
symbols = [[
    0,
    0,
    0,
    0] for x in xrange(256)]
con.recentfiles = []
batch_filelist = []
redrawcount = 1
bmpfont = None
fontbuffmsk = None
fontbuff = None
fontname = None
fontscalex = 1.0
fontscaley = 1.0
fontblurint = 0
fontblnd = 0
blendval = 16777215
codemap = None
graymask = None
menu_main = None
mainmenu = None
popupmenu = None
menu_colorch = None
menu_preview = None
menu_about = None
menu_start = None
menu_selection = None
menu_palette = None
menu_palette1 = None
menu_palette2 = None
menu_palette3 = None
mess_info = None
mess_tip = None
mess_eegg = []
main_event_proc = True
_fill_queue = []
_fill_width = 0
_fill_height = 0
ciclefunctions = []
con.ui_req_color = [
    11315624,
    10262936,
    [
        None,
        6052184,
        0,
        16777215,
        0],
    [
        0,
        2113648,
        16777215]]
con.ui_form_color = [
    9210248,
    0,
    11315624,
    [
        0,
        2113648,
        16777215]]
con.ui_menu_font_fheight = None
def_spaces = (4, 4, 3, 3, 2)
def_colors = [
    [
        0,
        11315624,
        2171169],
    [
        None,
        6052184,
        0,
        16777215,
        8355711]]
con.ui_menu_color = def_colors
con.ui_prog_color = [
    0,
    40960,
    16777215]
con.ui_grid_color = 16711680
con.curs_del = [
    5,
    20,
    40,
    60,
    80,
    100,
    120,
    150,
    150]
con.curs_step = [
    0,
    1,
    2,
    3,
    4,
    6,
    8,
    10,
    12]
con.toolbar_slidespeed = 2
keyboard = Keyboard()
buff = new_image((con.screen_size[0], con.screen_size[1]))
applock = Ao_lock()
appuifw.app.screen = 'full'
appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
event = event_main
appuifw.app.body = appuifw.Canvas(redraw_callback=redraw, event_callback=event_main)
canv = appuifw.Canvas(redraw_callback=redraw, event_callback=event_main)
canv.blit(lloader.logo,
          target=((con.screen_size[0] - lloader.logo.size[0]) / 2, (con.screen_size[1] - lloader.logo.size[1]) / 2))
del lloader.logo
del lloader.canv
appuifw.app.exit_key_handler = rightmenu
progressbar = wt_ui.Tbar(con.screen_size[0] / 2 - con.screen_size[0] / 4 - 25, con.screen_size[1] / 2 - 11,
                         con.screen_size[0] * 3 / 4 + 25, con.screen_size[1] / 2 + 10, (0, 100), 10, canv, False, 3)
progressbar.color(con.ui_prog_color)
progressbar.linewidth(2)
progressbar.space = 1
progressbar.corner = 2
progressbar.scrollwidth(0)
pbar = wt_ui.Tbar(con.screen_size[0] * 1 / 20, con.screen_size[1] - 14, con.screen_size[0] * 19 / 20,
                  con.screen_size[1] - 3, (0, 100), 10, canv, False, 3)
pbar.color((0, 255, 16777215))
pbar.linewidth(2)
pbar.space = 1
pbar.corner = 2
pbar.scrollwidth(0)
pbar.percent(0)
pbar.draw()
mbox_percent = wt_ui.Tmessagebox([
    15,
    con.screen_size[1] / 2 - 37,
    con.screen_size[0] - 30,
    52], canv, con.ui_menu_color[0], con.ui_menu_font_bold)
mbox_percent.style = 'up'
mbox_percent.boxstyle = 1
curwin = 0
imagewindow = []
imwin = None
file_new(con.screen_size[0], con.screen_size[1], 1)
tool_line = TGraphtool(buff, imwin.img, 0)
tool_rect = TGraphtool(buff, imwin.img, 1)
tool_ellps = TGraphtool(buff, imwin.img, 2)
mess = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe ' + app_versionstr
canv.text((13, con.screen_size[1] - 20), mess, fill=0, font=None)
pbar.percent(10)
pbar.draw()
tool = {}
tool['pencil'] = 0
tool['paintbrush'] = 1
tool['eraser'] = 2
tool['line'] = 3
tool['rectangle'] = 4
tool['ellipse'] = 5
tool['selector'] = 6
tool['elselector'] = 7
tool['stamp'] = 8
tool['picker'] = 9
tool['templet'] = 10
tool['text'] = 11
tool['polygon'] = 12
tool['brokenline'] = 13
tool['paintbucket'] = 14
tool['spray'] = 15
tool['lasso'] = 16
tool['magicrod'] = 17
tool['polygon_'] = 99
skin_define(program_path)
if not skin_check(program_path + 'skin\\' + con.skin + '\\'):
    abort()

(icon, icon2, icn1, icn2, icon5, image_w, icon7, image_n) = skin_load(program_path + 'skin\\' + con.skin + '\\')
pbar.percent(90)
pbar.draw()
del pbar
if noicon is False:
    icon_tool = []
    for t in xrange(len(icon)):
        icon_tool.append(icon[t].resize((14, 14)))

    for t in xrange(len(icon2)):
        icon_tool.append(icon2[t].resize((14, 14)))

if con.screen_size[1] < 320:
    iconsize = (24, 24)
    for t in xrange(len(icon)):
        icon[t] = icon[t].resize(iconsize)

    for t in xrange(len(icon2)):
        icon2[t] = icon2[t].resize(iconsize)


def panel_onshow():
    imwin.blocked(True)
    con.keyconfig.hotkeys_off()


def panel_onhide():
    imwin.blocked(False)
    con.keyconfig.hotkeys_on()
    keyboard.resetkeys()


toolslist = wt_ui.Ticongrid(0, 0, [
    icon,
    icon2])
toolslist.setcourse(0, 0, -toolslist.getsize()[0], 0, toolslist.getsize()[0] / con.toolbar_slidespeed,
                    key_codes.EKeyStar)
toolslist.callback(panel_onshow, panel_onhide, tools_set)
toolslist.rectcolor(con.ui_grid_color)
del icon
del icon2
tools_set()
gradgrid = wt_ui.Ticongrid(-64, 0, [
    icn1,
    icn2])
gradgrid.setcourse(0, 0, -gradgrid.getsize()[0], 0, gradgrid.getsize()[0] / con.toolbar_slidespeed, None)
gradgrid.callback(panel_onshow, panel_onhide)
gradgrid.rectcolor(con.ui_grid_color)
col = [
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None]]
colors = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []]
#continue
[colors[x].append(icon5[x]) for x in xrange(len(icon5))]
#continue
[colors[x].append(image_w) for x in xrange(6, 12)]
dialog = wt_requester.requester(dtext, multisel=True)
dialog_tmp = wt_requester.requester(dtext)
dialog_pal = wt_requester.requester(dtext)
dialog_img = wt_requester.requester(dtext)
dialog_misc = wt_requester.requester(dtext)
dialog.seticons(icon7)
dialog_tmp.seticons(icon7)
dialog_pal.seticons(icon7)
dialog_img.seticons(icon7)
dialog_misc.seticons(icon7)
del icon7
palette_createcell()
if palette_load():
    colorload()
else:
    colorgen()
colorgrid = wt_ui.Ticongrid(126, 0, [
    colors[0],
    colors[1],
    colors[2],
    colors[3],
    colors[4],
    colors[5],
    colors[6],
    colors[7],
    colors[8],
    colors[9],
    colors[10],
    colors[11]])
colorgrid.setcourse(con.screen_size[0] - colorgrid.getsize()[0], 0, con.screen_size[0], 0,
                    colorgrid.getsize()[0] / con.toolbar_slidespeed, key_codes.EKeyHash)
colorgrid.curitem((3, 0))
colorgrid.rectcolor(con.ui_grid_color)
colorgrid.rectoffset((1, -1))
sz = colorgrid.rectsize()
colorgrid.rectsize((sz[0], sz[1] + 1))
colorgrid.callback(grid_palette_onshow, grid_palette_onhide)
colorgrid.setcallback_onchangeitem(grid_palette_onchangeitem, grid_palette_onchangeitem)
for x in (6, 7, 8, 9, 10, 11):
    colorgrid.setexcludeitem([
        x,
        0])

functlist = [
    [
        dtext['tools'],
        toolslist.switch,
        key_codes.EKeyStar,
        None],
    [
        dtext['colorspanel'],
        colorgrid.switch,
        key_codes.EKeyHash,
        None],
    [
        dtext['brushsize'],
        brush_size,
        key_codes.EKey0,
        None],
    [
        dtext['open'],
        (lambda: file_open(False)),
        None,
        None],
    [
        dtext['openinnew'],
        (lambda: file_open(True)),
        None,
        None],
    [
        dtext['reopen'],
        (lambda: file_reopen(False)),
        None,
        None],
    [
        dtext['new'],
        (lambda: query_file_new(False)),
        None,
        None],
    [
        dtext['newinnew'],
        (lambda: query_file_new(True)),
        None,
        None],
    [
        dtext['save'],
        (lambda: file_save()),
        None,
        None],
    [
        dtext['saveas'],
        (lambda: file_saveas(True)),
        None,
        None],
    [
        dtext['recentfiles'],
        menu_recent,
        None,
        None],
    [
        dtext['close'],
        file_close,
        None,
        None],
    [
        dtext['undo'],
        undo,
        None,
        None],
    [
        dtext['redo'],
        redo,
        None,
        None],
    [
        dtext['cut'],
        clipcut,
        None,
        None],
    [
        dtext['copy'],
        clipcopy,
        None,
        None],
    [
        dtext['paste'],
        clippaste,
        None,
        None],
    [
        dtext['clear'],
        clipclear,
        None,
        None],
    [
        dtext['blend'],
        setblend,
        None,
        None],
    [
        dtext['select'],
        selectsize,
        None,
        None],
    [
        dtext['selectall'],
        selectall,
        None,
        None],
    [
        dtext['invert'],
        (lambda: imwin.selector.invert_selection()),
        None,
        None],
    [
        dtext['deselect'],
        (lambda: imwin.selector.deselect()),
        None,
        None],
    [
        dtext['zoomin'],
        zoom_in,
        None,
        None],
    [
        dtext['zoomout'],
        zoom_out,
        None,
        None],
    [
        dtext['zoom_multiply'],
        zoom_multiply_query,
        None,
        None],
    [
        dtext['zoom_1_1'],
        zoom_1_1,
        None,
        None],
    [
        dtext['entertext'],
        settext,
        None,
        None],
    [
        dtext['stdfont'],
        fontstd_select,
        None,
        None],
    [
        dtext['extfont'],
        font_open,
        None,
        None],
    [
        dtext['stdfontopt'],
        fontstd_opt,
        None,
        None],
    [
        dtext['extfontopt'],
        font_opt,
        None,
        None],
    [
        dtext['templet'],
        templet_create,
        None,
        None],
    [
        dtext['loadtemplet'],
        templet_load,
        None,
        None],
    [
        dtext['templetfromfile'],
        templet_fromfile,
        None,
        None],
    [
        dtext['exportpal'],
        palette_export,
        None,
        None],
    [
        dtext['importpal'],
        palette_import,
        None,
        None],
    [
        dtext['batchproc'],
        (lambda: batch.open(con.lastpath_img)),
        None,
        None],
    [
        dtext['info'],
        fileinfo,
        None,
        None],
    [
        dtext['preview'],
        (lambda: preview_hide(False)),
        None,
        None],
    [
        dtext['resize'],
        image_resize_query,
        None,
        None],
    [
        dtext['resizecanvas'],
        image_resizecanvas_query,
        None,
        None],
    [
        dtext['cropsel'],
        image_crop,
        None,
        None],
    [
        dtext['rotate'],
        image_rotate,
        None,
        None],
    [
        dtext['flip'],
        image_flip,
        None,
        None],
    [
        dtext['displacement'],
        image_displacement,
        None,
        None],
    [
        dtext['replacecolor'],
        image_replacecolor_query,
        None,
        None],
    [
        dtext['makemask'],
        image_tomask,
        None,
        None],
    [
        dtext['blur'],
        image_blur_query,
        None,
        None],
    [
        dtext['lightness'],
        image_lightness_query,
        None,
        None],
    [
        dtext['darkness'],
        image_darkness_query,
        None,
        None],
    [
        dtext['blackwhite'],
        (lambda: image_bpp('1')),
        None,
        None],
    [
        dtext['grayscale'],
        (lambda: image_bpp('L')),
        None,
        None],
    [
        dtext['posterize'],
        image_posterize,
        None,
        None],
    [
        dtext['invertcolors'],
        image_invertcolors,
        None,
        None],
    [
        dtext['colorbalance'],
        image_colorbalance,
        None,
        None],
    [
        dtext['saturation'],
        image_saturation,
        None,
        None],
    [
        dtext['sepia'],
        image_sepia,
        None,
        None],
    [
        dtext['gradient'],
        gradgrid.unlockandshow,
        None,
        None],
    [
        dtext['config'],
        config,
        None,
        None],
    [
        dtext['keyconfig'],
        (lambda: con.keyconfig.execute()),
        None,
        None],
    [
        dtext['skinselect'],
        skin_select,
        None,
        None],
    [
        dtext['colortheme'],
        theme_open,
        None,
        None],
    [
        dtext['help'],
        help,
        None,
        None],
    [
        dtext['switchwin'],
        imwindow_next,
        key_codes.EKey1,
        None],
    [
        dtext['swapcolors'],
        swap_colors,
        None,
        None],
    [
        dtext['navigation'],
        (lambda: imwin.navigation_switch()),
        key_codes.EKey7,
        None],
    [
        dtext['exit'],
        exit,
        0,
        0]]
con.keyconfig = kconfig.CKeyConfig(appuifw.app, canv, functlist, dtext)
con.keyconfig.hotkeys_set()
toolslist.keycode = key_codes.EScancodeStar
colorgrid.keycode = key_codes.EScancodeHash
con.keyconfig.onmod_callback = showtipex
con.keyconfig.offmod_callback = hidetip
running = 1
config_load()
batch = batch.Cbatch_processor(dtext, dialog)
menu_create()
ui_colors_update()
gradgrid.hideandblock()
colorgrid.hideandblock()
toolslist.hideandblock()
if con.firststart:
    mess_tip.hiden(False)

if menu_start_off is False:
    redraw = redraw_start
    mainproc_stop()
else:
    redraw = redraw_main
while running == 1:
    imwin.navigationcontrol()
    scrollbar_update()
    redraw()
    con.keyconfig.timeout_tick()
    nextcicle_waiter()
    keyboard._downs = {}
    ao_sleep(0.001)
    continue
    []
import lloader
import appuifw
import graphics
import sys
from sysinfo import display_pixels
import key_codes

s60_version_info = s60_version_info
from e32 import ao_sleep, Ao_lock, ao_yield, file_copy
from os import path, listdir, abort, stat, rename, remove, mkdir
from random import gauss, uniform
import iniparser
from langimp import lang_load, lang_readfromfile
import wt_ui
import wt_colormx
import wt_requester
import classes
from time import clock
import zlib
import struct
import SV_TRANS
import improc
import conf
import batch
import mbm
import kconfig
import traceback

__version__ = 1.4
_beta = 2
_version_ = u'%.2f ' % __version__
if _beta > 1:
    _version_ += u'beta %d\xe4\xb8\xad\xe6\x96\x87\xe7\x89\x88' % _beta

if path.exists('C:\\System\\Apps\\ImageDesigner\\palette.dat'):
    drive = 'c:\\'
else:
    drive = 'e:\\'
program_path = drive + 'System\\Apps\\ImageDesigner\\'
sys.stderr = open(program_path + 'error.log', 'wt')
__selfmodlist__ = (
'improc', 'classes', 'wt_requester', 'wt_colormx', 'wt_ui', 'iniparser', 'langimp', 'SV_TRANS', 'conf', 'batch', 'mbm',
'kconfig')
for t in __selfmodlist__:

    try:
        if sys.modules[t].__version__ != __version__:
            appuifw.note(u'Incorect version of module: ' + unicode(t) + u'. Reinstall application.', 'error')
            abort()
    except:
        None
        None
        None
        appuifw.note(u'Incorect version of module: ' + unicode(t) + u'. Reinstall application.', 'error')
        abort()


def logout(par1, par2='', par3='', par4=''):
    print >> sys.stderr, par1, par2, par3, par4


def redraw(a=None):
    pass


def new_image(size, mode='RGB16'):
    try:
        return graphics.Image.new(size, mode)
    except:
        None
        None
        None
        appuifw.note(dtext['e_lowmemory'], 'error')
        return None


def copy_image(img):
    im = new_image(img.size)
    if im is not None:
        im.blit(img)

    return im


class Keyboard(object):

    def __init__(self, onevent=(lambda: None)):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}
        self._onevent = onevent
        self.evt = {
            'keycode': None,
            'scancode': None,
            'type': None}

    def handle_event(self, event):
        self.evt = event
        self._downs = {}
        if event['type'] == appuifw.EEventKeyDown:
            self._state = event['scancode']
            if not self._keyboard_state.get(self._state, False):
                self._downs[self._state] = True

            self._keyboard_state[self._state] = True
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']] = False
            self._state = None

        if self._state is None:
            self._check = True

    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, False)

    def pressed(self, scancode):
        return self._downs.get(scancode, False)

    def state(self):
        return self._state

    def freedown(self, scancode):
        if self._check:
            if self._downs.get(scancode, False):
                self._check = False
                return True

        return False

    def keycode(self, code):
        if self.evt['keycode'] == code:
            return True

        return False

    def scancode(self, code):
        if self.evt['scancode'] == code:
            return True

        return False

    def resetkeys(self):
        self._keyboard_state = {}
        self._state = None
        self._check = False
        self._downs = {}


class TCursor:

    def __init__(self, canv, img, x, y, w, h, size=3):
        self.x = x
        self.y = y
        self.canv = canv
        self.img = img
        self.wx = x
        self.wy = y
        self.ww = w
        self.wh = h
        self.kind = 0
        self.size = size
        self.oldsize = None
        self.col = 0
        self.cold = 0
        self.hiden = False

    def draw(self, imx, imy):
        if self.hiden is True:
            return None

        if self.kind == 0:
            if self.size > 1:
                self.canv.rectangle((self.x - self.size - 2, self.y - 1, self.x + (self.size - 1), self.y + 2),
                                    16777215)
                self.canv.rectangle((self.x - 1, self.y - self.size - 2, self.x + 2, self.y + (self.size - 1)),
                                    16777215)

            self.canv.line((self.x - self.size - 1, self.y, self.x + self.size, self.y), 0)
            self.canv.line((self.x, self.y - self.size - 1, self.x, self.y + self.size), 0)
        elif self.kind == 1:
            if self.cold == 0:
                self.col += 15 * 65793
                if self.col > 16777215:
                    self.cold = 1
                    self.col = 16777215

            else:
                self.col -= 15 * 65793
                if self.col < 0:
                    self.cold = 0
                    self.col = 0

            self.canv.line((self.x - self.size - 1, self.y, self.x + self.size, self.y), self.col)
            self.canv.line((self.x, self.y - self.size - 1, self.x, self.y + self.size), self.col)
        elif self.kind == 2:
            for t in xrange(-(self.size - 1), self.size):
                col = self.img.getpixel((self.x + t + imx, self.y + imy))[0]
                col = (255 - col[0], 255 - col[1], 255 - col[2])
                self.canv.point((self.x + t, self.y), col)
                col = self.img.getpixel((self.x + imx, self.y + t + imy))[0]
                col = (255 - col[0], 255 - col[1], 255 - col[2])
                self.canv.point((self.x, self.y + t), col)

    def coord(self, cr=None):
        if cr is not None:
            if cr[0] is not None:
                self.x = cr[0]

            if cr[1] is not None:
                self.y = cr[1]

        else:
            return (self.x, self.y)

    def zone(self, sz=None):
        if sz is not None:
            if sz[0] is not None:
                self.wx = sz[0]
                self.x = sz[0]

            if sz[1] is not None:
                self.wy = sz[1]
                self.y = sz[1]

            if sz[2] is not None:
                self.ww = sz[2]

            if sz[3] is not None:
                self.wh = sz[3]

        else:
            return (self.wx, self.wy, self.ww, self.wh)

    def move(self, d, s):
        if d == 0:
            if self.x > self.wx:
                self.x -= s
                if self.x < self.wx:
                    self.x = self.wx

            else:
                return d
        elif d == 1:
            if self.x < self.wx + self.ww - 1:
                self.x += s
                if self.x > self.wx + self.ww - 1:
                    self.x = self.wx + self.ww - 1

            else:
                return d
        elif d == 2:
            if self.y > self.wy:
                self.y -= s
                if self.y < self.wy:
                    self.y = self.wy

            else:
                return d
        elif d == 3:
            if self.y < self.wy + self.wh - 1:
                self.y += s
                if self.y > self.wy + self.wh - 1:
                    self.y = self.wy + self.wh - 1

            else:
                return d

        return None


class TTool(object):

    def _define(self, buff, img):
        self.buff = buff
        self.img = img
        self.enbld = False
        self.render = False
        self.drawing = False

    def enabled(self, state=None):
        if state is not None:
            self.enbld = state
        else:
            return self.enbld


class TGraphtool(TTool):

    def __init__(self, buff, img, tool):
        TTool._define(self, buff, img)
        self.coord = [
            0,
            0,
            0,
            0]
        self.bcoord = [
            0,
            0,
            0,
            0]
        self.tool = tool
        self.easydraw = False

    def _drawto(self, canv, coord, iw):
        if self.tool == 0:
            line(canv, coord, outline=foreclr, width=iw.bsize)
        elif self.tool == 1:
            rect(canv, coord, outline=foreclr, fill=backclr, width=iw.bsize)
        elif self.tool == 2:
            ellps(canv, coord, outline=foreclr, fill=backclr, width=iw.bsize)

    def eventcontrol(self, evt, iw):
        if self.enbld is False and not (toolslist.hdn) or not (colorgrid.hdn):
            return None

        if keyboard.pressed(key_codes.EScancodeSelect):
            self.drawing = not (self.drawing)
            if self.drawing is True:
                self.coord = [
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy,
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy]
                self.bcoord = [
                    iw.curs.x,
                    iw.curs.y,
                    iw.curs.x,
                    iw.curs.y]
                self.render = False
            else:
                self.coord[-2:] = [
                    iw.curs.x + iw.imx,
                    iw.curs.y + iw.imy]
                self.bcoord = [
                    self.coord[0] - iw.imx,
                    self.coord[1] - iw.imy,
                    iw.curs.x,
                    iw.curs.y]
                self.render = True

    def draw(self, iw):
        if self.enbld is False:
            return None

        if self.drawing is True:
            if self.easydraw is False:
                xx = iw.curs.x
                yy = iw.curs.y
            else:
                x = iw.curs.x - self.coord[0] - iw.imx
                y = iw.curs.y - self.coord[1] - iw.imy
                xx = max(x, y) + (self.coord[0] - iw.imx)
                yy = max(x, y) + (self.coord[1] - iw.imy)
            self.bcoord = [
                self.coord[0] - iw.imx,
                self.coord[1] - iw.imy,
                xx,
                yy]
            self._drawto(self.buff, self.bcoord, iw)

        if self.render is True:
            self.render = False
            self._drawto(iw.img, self.coord, iw)

    def enabled(self, state=None):
        if state is False and self.drawing is True:
            self.drawing = state
            self.render = state

        if state is not None:
            self.enbld = state
        else:
            return self.enbld


class Controllable:
    focusedon = None

    def setfocusto(instance):
        focusedon = instance

    setfocusto = staticmethod(setfocusto)

    def getfocused():
        return focusedon

    getfocused = staticmethod(getfocused)

    def activate(self):
        Controllable.setfocusto(self)

    def isactive(self):
        return self == Controllable.getfocused()


class TImageWindow:

    def __init__(self, img, canv, x, y, w, h):
        self.name = ''
        self.filename = None
        self.frmt = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.imx = 0
        self.imy = 0
        self.old_imx = 0
        self.old_imy = 0
        self.blckd = False
        self.hdn = False
        self.img = img
        self.editsize = [
            w,
            h]
        self.canv = canv
        self.undostack = [
            None]
        self.redostack = [
            None]
        self.undosize = 1
        self.objx = x
        self.objy = y
        self.obj = 0
        self.obj_text = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
        self.obj_point = []
        if s60_version_info == (3, 0):
            self.obj_font = (appuifw.available_fonts()[0], 14)
        else:
            self.obj_font = appuifw.available_fonts()[0]
        self.drawing = False
        self.bsize = 1
        self.ersize = 8
        self.sbx = 0
        self.sby = 0
        self.sbt = 0
        self.moving = None
        self.move_step = 0
        self.cursor_ptime = 0
        self.cursor_speedid = 0
        self.cursor_delayscount = len(con.curs_del)
        self.zoom = 1
        self.scale = False
        self.curs = TCursor(canv, img, self.x, self.y, self.w, self.h)
        self.keyboard = Keyboard()
        self.lastfile = None
        self.navigation = False
        self.imagemodified = False
        self.selector = classes.TSelectorTool(keyboard, canv, img, self, mbox_percent)
        self.waitpickerchoose = False
        self.pickercallback = None

    def destruct(self):
        del self.curs
        del self.selector
        del self.keyboard

    def draw(self):
        if self.hdn is False:
            self.canv.blit(self.img, target=(self.x, self.y),
                           source=(self.imx, self.imy, self.imx + self.w, self.imy + self.h), scale=False)
            if self.drawing is True:
                self.draw_object(self.canv)

            if self.drawing is True and self.obj == tool['paintbrush']:
                self.draw_object(self.img, self.imx, self.imy)
            elif self.obj == tool['eraser'] or self.obj == tool['text']:
                self.draw_object(self.canv)
            elif self.drawing is True and self.obj == tool['spray']:
                self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
            elif self.obj == tool['templet']:
                self.draw_object(self.canv)

            self.selector.draw()
            self.curs.draw(self.imx, self.imy)

    def setundosize(self, size):
        self.undosize = size
        u = self.undostack[:]
        r = self.redostack[:]
        #continue
        self.undostack = [None for x in xrange(self.undosize)]
       # continue
        self.redostack = [None for x in xrange(self.undosize)]
        self.undostack.extend(u)
        self.undostack = self.undostack[len(u):]
        self.redostack.extend(r)
        self.redostack = self.redostack[len(r):]

    def _backupimage(self):
        self.imagemodified = True
        if self.undosize != 0:
            buff = copy_image(self.img)
            if buff is not None:
                buff.blit(self.img)
                self.undostack.pop(0)
                self.undostack.append(buff)

    def undo(self):
        if self.undostack[-1] is None:
            return None

        buff = self.undostack.pop()
        self.undostack.insert(-1, None)
        if buff is not None:
            self.redostack.pop(0)
            self.redostack.append(copy_image(self.img))
            self.img.blit(buff)

    def redo(self):
        if self.redostack[-1] is None:
            return None

        buff = self.redostack.pop()
        self.redostack.insert(-1, None)
        if buff is not None:
            self.undostack.pop(0)
            self.undostack.append(copy_image(self.img))
            self.img.blit(buff)

    def brushsize(self, size=None):
        if size is not None:
            self.bsize = size

        return self.bsize

    def draw_object(self, canv, dx=0, dy=0, opt=None):
        if self.obj == tool['pencil']:
            canv.point([
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)

        if self.obj == tool['paintbrush']:
            line(canv, [
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['eraser']:
            if opt == 0:
                rect(canv, [
                    self.curs.x + dx,
                    self.curs.y + dy,
                    self.curs.x + self.ersize + dx,
                    self.curs.y + self.ersize + dy], outline=backclr, fill=backclr, width=1)
            else:
                rect(canv, [
                    self.curs.x + dx,
                    self.curs.y + dy,
                    self.curs.x + self.ersize + dx,
                    self.curs.y + self.ersize + dy], outline=0, fill=16777215, width=1)
        elif self.obj == tool['text']:
            if bmpfont is None:
                canv.text([
                    self.curs.x + dx,
                    self.curs.y + dy], self.obj_text, fill=foreclr, font=self.obj_font)
            elif fontbuff is not None:
                canv.blit(fontbuff, target=(self.curs.x + dx, self.curs.y + dy), mask=fontbuffmsk)

        elif self.obj == tool['polygon']:
            canv.line([
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['brokenline']:
            canv.line([
                self.objx + dx,
                self.objy + dy,
                self.curs.x + dx,
                self.curs.y + dy], outline=foreclr, width=self.bsize)
        elif self.obj == tool['spray']:
            x = self.curs.x + dx
            y = self.curs.y + dy
            sigma = self.bsize
            for t in xrange(3):
                canv.point([
                    gauss(x + 1, sigma),
                    gauss(y + 1, sigma)], outline=foreclr, width=1)

        elif self.obj == tool['polygon_']:
            point = self.obj_point
            for t in xrange(len(point)):
                point[t][0] += dx
                point[t][1] += dy

            canv.polygon(point, outline=foreclr, fill=backclr, width=self.bsize)
        elif self.obj == tool['templet']:
            if templet is not None:
                templet_draw(canv, self.curs.x + dx, self.curs.y + dy)

    def param(self, x=None, y=None, w=None, h=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if w is not None:
            self.w = w

        if h is not None:
            self.h = h

        if x is None and y is None and w is None and h is None:
            return [
                self.x,
                self.y,
                self.w,
                self.h]

    def image_coord(self, x=None, y=None):
        if x is not None:
            self.imx = x

        if y is not None:
            self.imy = y

        if x is None and y is None:
            return (self.imx, self.imy)

    def image_correctcoord(self):
        x = self.imx
        y = self.imy
        if self.imx < 0:
            self.imx = 0

        if self.imy < 0:
            self.imy = 0

        if self.imx > self.img.size[0] - self.w:
            self.imx = self.img.size[0] - self.w

        if self.imy > self.img.size[1] - self.h:
            self.imy = self.img.size[1] - self.h

        return (x - self.imx, y - self.imy)

    def coord(self, cr=None):
        if cr is not None:
            if cr[0] is not None:
                self.x = cr[0]

            if cr[1] is not None:
                self.y = cr[1]

            self.curs.zone((self.x, self.y, self.w, self.h))
        else:
            return (self.x, self.y)

    def size(self, sz=None, edz=True):
        if sz is not None:
            if sz[0] is not None:
                self.w = sz[0]

            if sz[1] is not None:
                self.h = sz[1]

            if edz is True:
                self.editsize = [
                    self.w,
                    self.h]

            self.curs.zone((self.x, self.y, self.w, self.h))
        else:
            return (self.w, self.h)

    def image_move(self, d, s):
        if d == 0:
            if self.imx > 0:
                self.imx -= s
                if self.imx < 0:
                    self.imx = 0


        elif d == 1:
            if self.imx < self.img.size[0] - self.w:
                self.imx += s
                if self.imx > self.img.size[0] - self.w:
                    self.imx = self.img.size[0] - self.w


        elif d == 2:
            if self.imy > 0:
                self.imy -= s
                if self.imy < 0:
                    self.imy = 0


        elif d == 3:
            if self.imy < self.img.size[1] - self.h:
                self.imy += s
                if self.imy > self.img.size[1] - self.h:
                    self.imy = self.img.size[1] - self.h

        return None

    def cursor_move(self, d, s=1):
        if self.curs.move(d, s) is not None:
            self.image_move(d, s)

    def cursor_hiden(self, state=None):
        if state is not None:
            self.curs.hiden = state

        return self.curs.hiden

    def hiden(self, hd=None):
        if hd is not None:
            self.hdn = hd
            if self.hdn is True:
                self.blckd = True
            else:
                self.blckd = False

        return self.hdn

    def blocked(self, state=None):
        if state is not None:
            self.blckd = state

        return self.blckd

    def navigation_switch(self):
        self.navigation = not (self.navigation)
        if self.navigation is True:
            self.old_imx = self.imx
            self.old_imy = self.imy
            self.cursor_hiden(True)
            showtipex(dtext['navigation'])
        else:
            self.imx = self.old_imx
            self.imy = self.old_imy
            self.cursor_hiden(False)
            showtipex(dtext['edit'])

    def _cursor_move(self, d):
        self.cursor_ptime += 1
        if self.cursor_ptime > con.curs_del[self.cursor_speedid]:
            if self.cursor_speedid < con.curs_lastdelind:
                self.cursor_speedid += 1

        if self.cursor_speedid != 0:
            self.move_step = con.curs_step[self.cursor_speedid]

        self.cursor_move(d, self.move_step)
        self.moving = True
        self.move_step = 0

    def navigationcontrol(self, evt=None):
        if self.blckd is False:
            if self.navigation is True:
                if keyboard.is_down(key_codes.EScancodeLeftArrow):
                    self.image_move(0, 10)
                elif keyboard.is_down(key_codes.EScancodeRightArrow):
                    self.image_move(1, 10)
                elif keyboard.is_down(key_codes.EScancodeUpArrow):
                    self.image_move(2, 10)
                elif keyboard.is_down(key_codes.EScancodeDownArrow):
                    self.image_move(3, 10)

                if keyboard.is_down(key_codes.EScancodeSelect):
                    self.navigation = False
                    self.cursor_hiden(False)
                    showtipex(dtext['edit'])

            elif not keyboard.is_down(key_codes.EScancodeLeftArrow) and not keyboard.is_down(
                    key_codes.EScancodeRightArrow) and not keyboard.is_down(
                    key_codes.EScancodeUpArrow) and not keyboard.is_down(key_codes.EScancodeDownArrow):
                self.move_step = 1
                self.cursor_ptime = 0
                self.cursor_speedid = 0
                self.moving = False
                if self.obj == tool['paintbrush'] and self.drawing is True:
                    self.objx = self.curs.x
                    self.objy = self.curs.y
                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

            if keyboard.is_down(key_codes.EScancodeLeftArrow):
                self._cursor_move(0)

            if keyboard.is_down(key_codes.EScancodeRightArrow):
                self._cursor_move(1)

            if keyboard.is_down(key_codes.EScancodeUpArrow):
                self._cursor_move(2)

            if keyboard.is_down(key_codes.EScancodeDownArrow):
                self._cursor_move(3)

    def keyboardevent(self, evt=None):
        global foreclr
        if self.blckd is False:
            if self.navigation is False:
                self.selector.control()
                if keyboard.freedown(key_codes.EScancodeSelect):
                    if self.obj != tool['pencil'] and self.obj != tool['picker'] and self.obj != tool[
                        'eraser'] and self.obj != tool['templet'] and self.obj != tool['polygon_']:
                        self.drawing = not (self.drawing)
                        if self.drawing is True:
                            self.objx = self.curs.x
                            self.objy = self.curs.y
                            if self.obj == tool['paintbrush'] or self.obj == tool['spray']:
                                self._backupimage()

                        elif self.drawing is False:
                            if self.obj == tool['brokenline']:
                                self._backupimage()
                                if self.objx == self.curs.x and self.objy == self.curs.y:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                else:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.objx = self.curs.x
                                    self.objy = self.curs.y
                                    self.drawing = not (self.drawing)
                            elif self.obj == tool['polygon']:
                                self._backupimage()
                                if self.objx == self.curs.x and self.objy == self.curs.y:
                                    self.obj_point.append([
                                        self.objx,
                                        self.objy])
                                    self.obj = tool['polygon_']
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.obj_point = []
                                    self.obj = tool['polygon']
                                else:
                                    self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                                    self.obj_point.append([
                                        self.objx,
                                        self.objy])
                                    self.objx = self.curs.x
                                    self.objy = self.curs.y
                                    self.drawing = not (self.drawing)
                            elif self.obj != tool['paintbrush'] and self.obj != tool['spray']:
                                self._backupimage()
                                self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)


                    elif self.obj != tool['paintbrush'] and self.obj != tool['spray'] and self.obj != tool['pencil']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['pencil']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['picker']:
                        c = self.img.getpixel(((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy))[0]
                        c = 256 * 256 * c[0] + 256 * c[1] + c[2]
                        foreclr = c
                        if self.waitpickerchoose is True:
                            if callable(self.pickercallback):
                                self.waitpickerchoose = False
                                self.pickercallback()
                                self.pickercallback = None

                    if self.obj == tool['paintbucket']:
                        self._backupimage()
                        canv.clear(10066329)
                        fillimage(self.img, ((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy),
                                  foreclr, (lambda: canv.blit(imwin.img)))

                    if self.obj == tool['magicrod']:
                        self._backupimage()
                        canv.clear(10066329)
                        mrod_select(self.img, ((self.curs.x - self.x) + self.imx, (self.curs.y - self.y) + self.imy),
                                    foreclr, (lambda: canv.blit(imwin.img)))

                    if self.obj == tool['eraser']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy, 0)

                    if self.obj == tool['text']:
                        self._backupimage()
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                    if self.obj == tool['templet']:
                        self.objx = self.curs.x
                        self.objy = self.curs.y
                        if templet is not None:
                            self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)

                if keyboard.pressed(key_codes.EScancodeBackspace):
                    if self.drawing is True:
                        if self.obj == tool['brokenline']:
                            self.drawing = False
                        elif self.obj == tool['polygon']:
                            self.obj_point.append([
                                self.objx,
                                self.objy])
                            self.objx = self.curs.x
                            self.objy = self.curs.y
                            self.obj = tool['polygon_']
                            self.draw_object(self.img, -(self.x) + self.imx, -(self.y) + self.imy)
                            self.obj_point = []
                            self.obj = tool['polygon']
                            self.drawing = False

                        if self.obj == tool['brokenline']:
                            self.drawing = False


def setblend():
    global blendval
    val = appuifw.query(dtext['blend'], 'number', 100 - inttorgb(blendval)[0] * 100 / 255)
    if val is None:
        return None

    if val > 100 or val < 0:
        appuifw.note(dtext['badvalue'], 'error')

    val = 255 - val * 255 / 100
    blendval = rgbtoint((val, val, val))
    imwin.selector.setblend(blendval)


def clipcopy():
    imwin.selector.clipcopy()


def clippaste():
    imwin.selector.clippaste()


def clipcut():
    imwin.selector.clipcut(backclr)


def clipclear():
    imwin.selector.clipclear(backclr)


def selectall():
    global curtool
    tool_line.enabled(False)
    tool_rect.enabled(False)
    tool_ellps.enabled(False)
    toolslist.curitem((0, 6))
    curtool = tool['selector']
    imwin.obj = tool['selector']
    imwin.drawing = False
    imwin.selector.selectall()


def selectsize():
    w = appuifw.query(dtext['width'], 'number', con.screen_size[0])
    if w is None:
        return None

    w -= 1
    if w > imwin.img.size[0]:
        w = imwin.img.size[0]
    elif w < 1:
        w = 1

    h = appuifw.query(dtext['height'], 'number', con.screen_size[1])
    if h is None:
        return None

    h -= 1
    if h > imwin.img.size[1]:
        h = imwin.img.size[1]
    elif h < 1:
        h = 1

    toolslist.curitem((0, 6))
    tools_set()
    x = -(imwin.x) + imwin.imx + imwin.curs.x
    y = -(imwin.y) + imwin.imy + imwin.curs.y
    imwin.selector.set(0)
    imwin.selector.tool.setcoord((x, y, x + w, y + h))
    imwin.selector.tool.fixselection()
    imwin.selector.tool.moving = True


def brush_size():
    if imwin.obj == tool['selector']:
        selectsize()
    elif imwin.obj == tool['text']:
        text = appuifw.query(dtext['entertext'], 'text', imwin.obj_text)
        if text is not None:
            imwin.obj_text = text
            font_updatemess(text)

    elif imwin.obj == tool['eraser']:
        size = appuifw.query(dtext['brushsize'], 'number', imwin.ersize)
        if size is not None:
            imwin.ersize = size

    else:
        size = appuifw.query(dtext['brushsize'], 'number', imwin.brushsize())
        if size is not None:
            imwin.brushsize(size)


def settext():
    text = appuifw.query(dtext['entertext'], 'text', imwin.obj_text)
    if text is not None:
        imwin.obj_text = text
        font_updatemess(text)


def rect(canv, cr, outline=None, fill=None, width=1, pattern=None):
    if cr[0] != cr[2] and cr[1] != cr[3]:
        canv.rectangle([
            min(cr[0], cr[2]),
            min(cr[1], cr[3]),
            max(cr[0], cr[2]) + 1,
            max(cr[1], cr[3]) + 1], outline, fill, width)
    else:
        line(canv, [
            cr[0],
            cr[1],
            cr[2],
            cr[3]], outline=outline, width=width)


def softrect(canv, _2, outline=0, fill=16777215, width=1, corner=1):
    (x, y, x1, y1) = _2
    canv.polygon(((x + corner, y), (x, y + corner), (x, y1 - corner), (x + corner, y1), (x1 - corner, y1),
                  (x1, y1 - corner), (x1, y + corner), (x1 - corner, y)), outline=outline, fill=fill, width=width)


def ellps(canv, cr, outline=None, fill=None, width=1, pattern=None):
    if cr[0] != cr[2] and cr[1] != cr[3]:
        canv.ellipse([
            min(cr[0], cr[2]),
            min(cr[1], cr[3]),
            max(cr[0], cr[2]),
            max(cr[1], cr[3])], outline, fill, width)
    else:
        line(canv, [
            cr[0],
            cr[1],
            cr[2],
            cr[3]], outline=outline, width=width)


def line(can, cr, outline, width):
    can.line([
        cr[0],
        cr[1],
        cr[2],
        cr[3]], outline=outline, width=width)
    can.point((cr[2], cr[3]), outline=outline, width=width)


def parameters_save():
    global paramtuple
    paramtuple = (
    appuifw.app.screen, appuifw.app.body, appuifw.app.menu, appuifw.app.title, appuifw.app.exit_key_handler)


def parameters_restore():
    appuifw.app.screen = paramtuple[0]
    appuifw.app.body = paramtuple[1]
    appuifw.app.menu = paramtuple[2]
    appuifw.app.title = paramtuple[3]
    appuifw.app.exit_key_handler = paramtuple[4]


def help():
    parameters_save()
    appuifw.app.title = dtext['help']
    appuifw.app.screen = 'normal'
    appuifw.app.body = appuifw.Text()
    t = appuifw.Text()

    appuifw.app.exit_key_handler = lambda: parameters_restore()
    readfile(t, 'help.txt')
    appuifw.app.menu = [
        (dtext['help'], (lambda: readfile(t, 'help.txt'))),
        (dtext['license'], (lambda: readfile(t, 'license.txt'))),
        (dtext['history'], (lambda: readfile(t, 'history.txt'))),
        (dtext['close'], (lambda: parameters_restore()))]


def readfile(t, name):
    hf = open(program_path + name)
    txt = hf.read()
    hf.close()
    t.clear()
    t.font = con.ui_menu_font
    t.add(ru(txt))
    t.set_pos(0)


def switchhelp(state=None):
    global showhlp
    if state is None:
        showhlp = not showhlp
    else:
        showhlp = state


def tools_set():
    global curtool
    curtool = toolslist.curitem()[0] * len(tool) / 2 + toolslist.curitem()[1]
    imwin.obj = curtool
    imwin.drawing = False
    imwin.selector.set(None)
    if curtool == tool['line']:
        tool_line.enabled(True)
    else:
        tool_line.enabled(False)
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)

    if curtool == tool['rectangle']:
        tool_rect.enabled(True)
    else:
        tool_rect.enabled(False)
    if curtool == tool['ellipse']:
        tool_ellps.enabled(True)
    else:
        tool_ellps.enabled(False)
    if curtool == tool['text']:
        font_updatemess(imwin.obj_text)

    if curtool == tool['stamp']:
        appuifw.note(u'Work in progress:)')
        appuifw.note(u'Work in progress:)')


def swap_colors():
    global foreclr, backclr, foreclr, backclr
    if backclr is not None:
        c = foreclr
        foreclr = backclr
        backclr = c


def color_set(state=None):
    global foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr, foreclr, backclr
    (indx, indy) = colorgrid.curitem()
    if indy == 0:
        if indx == 0:
            c = query_rgb(dtext['outlinecolor'], foreclr)
            if c is not None:
                foreclr = c

        elif indx == 2:
            c = query_rgb(dtext['fillcolor'], backclr)
            if c is not None:
                backclr = c

        elif indx == 1:
            swap_colors()
        elif indx == 3:
            foreclr = 0
            backclr = 16777215
        elif indx == 5:
            backclr = None
        elif indx > 5:
            if con.custompal[indx - 6] != '':
                if _palette_load(program_path + 'Palette\\' + con.custompal[indx - 6]):
                    colorload()
                    palette_update()

    if indy == 0 and indx == 4:
        if state == 0:
            foreclr = 0
        elif state == 1:
            backclr = 0

    if indy != 0:
        if state == 0:
            foreclr = col[indx][indy]
        elif state == 1:
            backclr = col[indx][indy]

        if fontbuff is not None:
            fontbuff.clear(foreclr)


def _setforecolor():
    global foreclr
    foreclr = col[colorgrid.curitem()[0]][colorgrid.curitem()[1]]


def _setbackcolor():
    global backclr
    backclr = col[colorgrid.curitem()[0]][colorgrid.curitem()[1]]


def palette_createcell():
    size = 12
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            col[n].append(16777215)
            colors[n].append(new_image((size, size)))


def palette_update():
    c = colors
    icon = colorgrid.icon
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            icon((n, t), c[n][t])


def palette_reset():
    colorgen()
    palette_update()


def palette_save():
    _palette_save(program_path + 'palette.dat')


def palette_load():
    return _palette_load(program_path + 'palette.dat')


def palette_export():
    global lastpath_pal
    dirpath = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'save')
    if dirpath is None:
        return None

    if path.isfile(ur(dirpath)):
        defname = path.split(dirpath)[1]
        dirpath = path.split(dirpath)[0] + '\\'
    else:
        defname = u'ID_palette'
    dirpath = dirpath.replace('\\\\', '\\')
    lastpath_pal = dirpath
    name = appuifw.query(dtext['entername'], 'text', defname)
    if name is None:
        return None

    if name[-4:].lower() != '.dat':
        name = name + '.dat'

    _palette_save(dirpath + name)
    appuifw.note(dtext['palsavedas'] + name)


def palette_import():
    global lastpath_pal
    filename = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'open')
    if filename is None:
        return None

    lastpath_pal = path.split(filename)[0]
    if _palette_load(filename):
        colorload()
        palette_update()
    else:
        appuifw.note(dtext['palbroken'], 'error')


def palette_setcustom(i, filename):
    path = program_path + 'Palette\\' + filename
    if _palette_load(path):
        palette_checkcustom(i, filename)
    else:
        appuifw.note(dtext['palbroken'], 'error')


def palette_checkcustom(i, filename):
    folder = program_path + 'Palette\\' + filename
    if path.exists(folder):
        con.custompal[i] = filename
        colorgrid.icon((i + 6, 0), image_n[i])
    else:
        appuifw.note(dtext['palnotexist'], 'error')
        palette_clearcustom()


def palette_selectcustom():
    global lastpath_pal
    filename = dialog_pal.open(ur(lastpath_pal), [
        'dat'], 'open')
    if filename is None:
        return None

    name = path.split(filename)[1]
    lastpath_pal = path.split(filename)[0]
    palette_setcustom(colorgrid.curitem()[0] - 6, name)


def palette_clearcustom():
    i = colorgrid.curitem()[0] - 6
    con.custompal[i] = ''
    colorgrid.icon(colorgrid.curitem(), image_w)


def _palette_save(path):
    f = open(path, 'wt')
    for x in xrange(0, palette_size[0]):
        for y in xrange(0, palette_size[1]):
            if x == palette_size[0] - 1 and y == palette_size[1] - 1:
                delim = ''
            else:
                delim = ','
            if col[x][y] is not None:
                c = col[x][y]
                f.write(str(c) + delim)
            else:
                f.write(str(16777215) + delim)

    f.close()


def _palette_load(path):
    try:
        f = open(path, 'rt')
        line = f.readline()
        clist = line.split(',')
        #continue
        colorlist = [int(v) for v in clist]
        for x in xrange(0, palette_size[0]):
            for y in xrange(1, palette_size[1]):
                col[x][y] = colorlist[y + x * palette_size[1]]

        f.close()
        return True
    except:
        None
        None
        None
        appuifw.note(dtext['palbroken'], 'error')
        return False


def palette_setcell():
    size = 12
    col[colorgrid.curitem()[0]][colorgrid.curitem()[1]] = foreclr
    im = new_image((size, size))
    im.rectangle((0, 0, size, size), outline=0, fill=0)
    im.rectangle((1, 0, size, size - 1), outline=foreclr, fill=foreclr)
    colorgrid.icon(colorgrid.curitem(), im)


def colormixer():
    parameters_save()
    cc = wt_colormx.init(col[colorgrid.curitem()[0]][colorgrid.curitem()[1]], mtext)
    if cc is not None:
        c = 256 * 256 * cc[0] + 256 * cc[1] + cc[2]
        size = 12
        im = new_image((size, size))
        im.rectangle((0, 0, size, size), outline=0, fill=0)
        im.rectangle((1, 0, size, size - 1), outline=c, fill=c)

        try:
            if colorgrid.curitem()[1] != 0:
                colorgrid.icon(colorgrid.curitem(), im)
                col[colorgrid.curitem()[0]][colorgrid.curitem()[1]] = c
        except:
            None
            None
            None
            running = 0

    parameters_restore()


def scrollbar_resize():
    scrollbar_imw[0].maxvalue(imwin.img.size[0])
    scrollbar_imw[1].maxvalue(imwin.img.size[1])
    scrollbar_imw[0].screenvalue(workzone[0])
    scrollbar_imw[1].screenvalue(workzone[1])


def scrollbar_update():
    maxx = imwin.img.size[0] - imwin.w
    maxy = imwin.img.size[1] - imwin.h
    if maxx > 0:
        scrollbar_imw[0].percent(imwin.imx * 100 / maxx)

    if maxy > 0:
        scrollbar_imw[1].percent(imwin.imy * 100 / maxy)


def scrollbar_draw():
    if imwin.img.size[0] * imwin.zoom > workzone[0]:
        scrollbar_imw[0].draw()

    if imwin.img.size[1] * imwin.zoom > workzone[1]:
        scrollbar_imw[1].draw()


def tools_update(evt):
    if not (gradgrid.blckd):
        if keyboard.pressed(key_codes.EScancodeSelect):
            image_gradient(gradgrid.curindex())

    if not (colorgrid.blckd):
        if keyboard.freedown(key_codes.EScancodeSelect):
            onnextcicle_do((lambda: color_set(0)))

        if keyboard.freedown(key_codes.EScancode5):
            onnextcicle_do((lambda: color_set(1)))


def grid_palette_onhide(state=None):
    imwin.blocked(False)
    wt_ui.Tsysmenu.setcurrent(0, mainmenu)
    wt_ui.Tsysmenu.setcurrent(1, popupmenu)
    onnextcicle_do(con.keyconfig.hotkeys_on)


def grid_palette_onshow(state=None):
    imwin.blocked(True)
    wt_ui.Tsysmenu.setcurrent(0, menu_palette)
    con.keyconfig.hotkeys_off()


def grid_palette_onchangeitem():
    (indx, indy) = colorgrid.curitem()
    if indy == 0:
        if indx > 5:
            wt_ui.Tsysmenu.setcurrent(0, menu_palette2)
        else:
            wt_ui.Tsysmenu.setcurrent(0, menu_palette3)
    else:
        wt_ui.Tsysmenu.setcurrent(0, menu_palette)


def exit():
    global running
    if con.exitconfirm:
        ans = appuifw.query(dtext['exitconf'], 'query')
        if ans is None:
            return None

    try:
        mbox_percent.draw(dtext['saving'])
        redraw_main()
        con.save(program_path + 'config.ini')
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(u"Can't write to config.ini")

    try:
        palette_save()
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(u"Can't write to palette.dat")

    running = 0

    try:
        appuifw.app.set_exit()
    finally:
        sys.stderr.close()
        abort()


def message(buff, cr, col):
    if gtext is not None:
        buff.text(cr, gtext, col)


def redraw_main(clear=True):
    buff.clear(con.ui_form_color[2])
    imwin.draw()
    tool_line.draw(imwin)
    tool_rect.draw(imwin)
    tool_ellps.draw(imwin)
    if imwin.zoom > 1:
        zoombuff.blit(buff, source=zoomzone, scale=1)
        buff.blit(zoombuff)

    statusbar()
    scrollbar_draw()
    toolslist.draw(buff)
    colorgrid.draw(buff)
    gradgrid.draw(buff)
    wt_ui.Tsysmenu.draw()
    menu_selection.draw()
    mess_info.draw()
    mess_tip.draw()
    canv.blit(buff)


def redraw_about():
    if menu_about.ciclecount == 2:
        menu_about.ciclecount = 3
        menu_about.message(mess_eegg, con.ui_menu_font)
    elif menu_about.ciclecount == 0:
        if len(menu_about.mess[7]) != 27:
            abort()

    buff.clear(con.ui_form_color[2])
    menu_about.draw()
    canv.blit(buff)


def redraw_start():
    buff.clear(con.ui_form_color[2])
    menu_start.draw()
    canv.blit(buff)


def redraw_preview():
    buff.clear(con.ui_form_color[2])
    buff.blit(prev_image, target=prev_coord, scale=0)
    wt_ui.Tsysmenu.draw()
    canv.blit(buff)


def event_main(evt):
    global kevent
    kevent = wt_ui.Tsysmenu.control(evt)
    menu_selection.control(evt)
    imwin.keyboardevent()
    if main_event_proc:
        keyboard.handle_event(kevent)
        tools_update(kevent)
        wt_ui.Ticongrid.showcontrol(kevent)
        tool_line.eventcontrol(kevent, imwin)
        tool_rect.eventcontrol(kevent, imwin)
        tool_ellps.eventcontrol(kevent, imwin)
    elif not menu_about.hiden():
        menu_about.control(kevent)
    elif not mess_info.hiden():
        mess_info.control(kevent)
    elif not preview_exit:
        preview_control(kevent)


def imwindow_center():
    if imwin.img.size[0] < workzone[0]:
        x = (workzone[0] - imwin.img.size[0]) / 2

    if imwin.img.size[1] < workzone[1]:
        y = (workzone[1] - imwin.img.size[1]) / 2

    imwin.coord((x, y))
    imwin.curs.coord((0, 0))


def imwindow_saveparam():
    global temp_imwinpar
    temp_imwinpar = []
    if imwin is not None:
        temp_imwinpar.append(imwin.obj)
        temp_imwinpar.append(imwin.bsize)
        temp_imwinpar.append(imwin.curs.kind)
        temp_imwinpar.append(imwin.curs.size)
        temp_imwinpar.append(foreclr)
        temp_imwinpar.append(backclr)
        temp_imwinpar.append(imwin.undosize)
        temp_imwinpar.append(imwin.selector.get())


def imwindow_restoreparam():
    global foreclr, backclr, temp_imwinpar, foreclr, backclr, temp_imwinpar
    if len(temp_imwinpar) > 0:
        imwin.obj = temp_imwinpar[0]
        imwin.bsize = temp_imwinpar[1]
        imwin.curs.kind = temp_imwinpar[2]
        imwin.curs.size = temp_imwinpar[3]
        foreclr = temp_imwinpar[4]
        backclr = temp_imwinpar[5]
        imwin.undosize = temp_imwinpar[6]
        imwin.setundosize(imwin.undosize)
        imwin.selector.set(temp_imwinpar[7])
        temp_imwinpar = []
        if curtool == tool['selector']:
            imwin.selector.set(0)
        elif curtool == tool['elselector']:
            imwin.selector.set(1)
        elif curtool == tool['lasso']:
            imwin.selector.set(2)
        elif curtool == tool['magicrod']:
            imwin.selector.set(3)


def imwindow_new(image, win=None, restore=True):
    global editzone, scrollbar_imw, imwin, curwin, editzone, scrollbar_imw, imwin, curwin
    x = 0
    y = 0
    editzone = [
        workzone[0],
        workzone[1]]
    scrollbar_imw = [
        None,
        None]
    if image.size[0] < workzone[0]:
        editzone[0] = image.size[0]

    scrollbar_imw[0] = wt_ui.Tbar(0, workzone[1], con.screen_size[0] - scrollbarwidth, workzone[1] + scrollbarwidth,
                                  (0, image.size[0]), workzone[0], buff, False)
    if image.size[1] < workzone[1]:
        editzone[1] = image.size[1]

    scrollbar_imw[1] = wt_ui.Tbar(workzone[0], 0, con.screen_size[0], workzone[1], (0, image.size[1]), workzone[1],
                                  buff, True)
    scrollbar_imw[0].color(con.ui_form_color[3])
    scrollbar_imw[1].color(con.ui_form_color[3])
    if restore is True:
        imwindow_saveparam()

    if imwin and not win:
        imwin.destruct()

    imwin = TImageWindow(image, buff, x, y, editzone[0], editzone[1])
    imwin.selector.setcallback((lambda: menu_selection.hiden(False)))
    del image
    if win is True:
        imagewindow.append(imwin)
        imwin.name = unicode(len(imagewindow))
        curwin = len(imagewindow) - 1
    elif len(imagewindow) == 0:
        imagewindow.append(None)

    imagewindow[curwin] = imwin
    imwin.name = unicode(curwin + 1)
    if restore is True:
        imwindow_restoreparam()

    return imwin


def imwindow_clone():
    imwindow_new(imwin.img, True, True)


def imwindow_copy():
    imwindow_new(copy_image(imwin.img), True, True)


def imwindow_close(win=None):
    global imwin, curwin, imwin, curwin, imwin, curwin, imwin, curwin
    if win is None:
        if len(imagewindow) > 1:
            if curwin == len(imagewindow) - 1:
                cwin = curwin - 1
            else:
                cwin = curwin
            del imagewindow[curwin]
            imwin.destruct()
            imwin = imagewindow[cwin]
            curwin = cwin
            if imwin.zoom > 1:
                zoom_multiply(imwin.zoom)


    elif win > 0 and win < len(imagewindow):
        if len(imagewindow) > 1:
            if curwin == len(imagewindow) - 1:
                cwin = curwin - 1
            else:
                cwin = curwin
            del imagewindow[win]
            imwin = imagewindow[curwin]
            curwin = cwin
            if imwin.zoom > 1:
                zoom_multiply(imwin.zoom)


def imwindow_switchto(win):
    global imwin, curwin, imwin, curwin
    oldwin = imwin
    imagewindow[curwin] = imwin
    imwin = win
    curwin = imagewindow.index(imwin)
    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()


def imwindow_next():
    global imwin, curwin, imwin, curwin
    oldwin = imwin
    nextwin = curwin + 1
    if nextwin > len(imagewindow) - 1:
        nextwin = 0

    imagewindow[curwin] = imwin
    imwin = imagewindow[nextwin]
    curwin = nextwin
    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)

    showtipex(dtext['win'] + u': ' + imwin.name)
    mainproc_start()


def imwindow_change(win=None):
    global imwin, curwin, imwin, curwin, imwin, curwin, imwin, curwin
    oldwin = imwin
    if win is None:
        nextwin = curwin + 1
        if nextwin > len(imagewindow) - 1:
            nextwin = 0

        imagewindow[curwin] = imwin
        imwin = imagewindow[nextwin]
        curwin = nextwin
    elif win > 0 and win < len(imagewindow):
        if imagewindow[win] is not None:
            imagewindow[curwin] = imwin
            imwin = imagewindow[win]
            curwin = win

    if imwin.zoom > 1:
        zoom_multiply(imwin.zoom)

    imwin.curs.kind = oldwin.curs.kind
    imwin.curs.size = oldwin.curs.size
    imwin.bsize = oldwin.bsize
    imwin.obj = oldwin.obj
    scrollbar_resize()
    if curtool == tool['selector']:
        imwin.selector.set(0)
    elif curtool == tool['elselector']:
        imwin.selector.set(1)
    elif curtool == tool['lasso']:
        imwin.selector.set(2)
    elif curtool == tool['magicrod']:
        imwin.selector.set(3)


def showtip(text):
    mess_tip.pos = None
    mess_tip.coord = [
        con.screen_size[0] - 100,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    mess_tip.messtimeout = 1
    mess_tip.hiden(False)


def hidetip():
    mess_tip.hiden(True)


def showtipex(text, timeout=1):
    mess_tip.pos = None
    mess_tip.coord = [
        con.screen_size[0] - 100,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    w = mess_tip.rectcoord[2] - mess_tip.rectcoord[0]
    mess_tip.coord = [
        con.screen_size[0] - w - 10,
        10,
        con.screen_size[0] - 10,
        30]
    mess_tip.message([
        text], con.ui_menu_font)
    mess_tip.messtimeout = timeout
    mess_tip.hiden(False)


def check_imwincount():
    if mainmenu is not None:
        if len(imagewindow) == 1:
            mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['close']), True)
        else:
            mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['close']), False)


def file_new(w, h, win):
    image = new_image((w, h))
    if image is None:
        return None

    imwindow_new(image, win)
    del image
    check_imwincount()


def file_close(win=None):
    imwindow_close(win)
    check_imwincount()


def _file_open(filename, new_win):
    if filename is None:
        return None

    mbox_percent.style = 'center'
    mbox_percent.draw(dtext['loading'] + u'...')
    mbox_percent.style = 'up'

    try:
        image = graphics.Image.open(filename)
        file_addrecent(filename)
    except SymbianError:
        None
        None
        None
        appuifw.note(u"Could' to open image", 'error')
        return None
    except:
        None

    imwindow_new(image, new_win)
    del image
    imwin.filename = filename
    imwin.lastfile = filename
    check_imwincount()
    return imwin


def file_open(new_win=False):
    try:
        filename = dialog.open(path=ur(con.lastpath_img), ext=[
            'jpg',
            'png',
            'gif',
            'bmp',
            'mbm',
            'jpeg'], kind='open')
    except:
        None
        None
        None
        filename = dialog.open(path=con.lastpath_img, ext=[
            'jpg',
            'png',
            'gif',
            'bmp',
            'mbm',
            'jpeg'], kind='open')

    if filename is None:
        return None

    if type(filename) == type('') or type(filename) == type(u''):
        if path.splitext(filename)[1].lower() == '.mbm':
            appuifw.note(dtext['unpacking'] + '...')
            filename = mbm.Unmake(filename, con.lastpath_img + '\\')

    if type(filename) == type('') or type(filename) == type(u''):
        con.lastpath_img = path.split(filename)[0]
        redraw_main()
        if imwin.filename is not None and new_win == False:
            if appuifw.query(dtext['q_flnotsaved'], 'query'):
                file_saveas(trans=False)

        _file_open(filename, new_win)
    else:
        con.lastpath_img = path.split(filename[0])[0]
        redraw_main()
        if imwin.filename is not None and new_win == False:
            if appuifw.query(dtext['q_flnotsaved'], 'query'):
                file_saveas(trans=False)

        first = False
        for t in filename:
            if path.isfile(t):
                if first is False:
                    _file_open(t, new_win)
                    first = True
                else:
                    _file_open(t, True)

    return imwin


def file_addrecent(filename):
    try:
        for t in xrange(len(con.recentfiles)):
            con.recentfiles.remove(filename.lower())
    except:
        None
        None
        None

    con.recentfiles.insert(0, filename.lower())
    if len(con.recentfiles) > 10:
        del con.recentfiles[10:len(con.recentfiles)]


def file_reopen(win):
    if imwin.lastfile is not None:
        _file_open(imwin.lastfile, win)


def file_format_select(frmt):
    if frmt.upper() == 'JPEG':
        def_quality = 75
        def_quality = appuifw.query(dtext['quality'], 'number', def_quality)
        if def_quality is None:
            return None

        if 1 > def_quality:
            pass
        def_quality > 100
        if 1:
            appuifw.note(dtext['e_wrongqual'], 'error')
            return None

        return {
            'format': frmt,
            'quality': def_quality}
    elif frmt.upper() == 'PNG':
        def_bpp = 24
        bpp = [
            24,
            8,
            1]
        name = [
            dtext['bpp_24'],
            dtext['bpp_8'],
            dtext['bpp_1']]
        ind = appuifw.popup_menu(name, dtext['bpp'])
        if ind is None:
            return None

        def_bpp = bpp[ind]
        def_compression = 2
        compr = [
            'no',
            'fast',
            'default',
            'best']
        name = [
            dtext['comp_no'],
            dtext['comp_fast'],
            dtext['comp_def'],
            dtext['comp_best']]
        ind = appuifw.popup_menu(name, dtext['compression'])
        if ind is None:
            return None

        compression = compr[ind]
        return {
            'format': frmt,
            'bpp': def_bpp,
            'compression': compression}


def file_save(frmt=None, trans=True):
    if imwin.filename is None:
        file_saveas(True)
    elif frmt is None:
        if imwin.filename.lower().endswith('.png'):
            frmt = 'PNG'
        elif imwin.filename.lower().endswith('.jpg') or imwin.filename.lower().endswith('.jpeg'):
            frmt = 'JPEG'
        elif not file_saveas(True):
            return None

    param = file_format_select(frmt)

    try:
        if param['format'] == 'PNG':
            imwin.img.save(imwin.filename, bpp=param['bpp'], compression=param['compression'], format=param['format'])
            if trans:
                if not AskTransparent():
                    appuifw.note(dtext['saved'] + unicode(imwin.filename))

            else:
                appuifw.note(dtext['saved'] + unicode(imwin.filename))
        elif param['format'] == 'JPEG':
            imwin.img.save(imwin.filename, quality=param['quality'], format=param['format'])
            appuifw.note(dtext['saved'] + unicode(imwin.filename))
    except:
        None
        None
        None
        appuifw.note(dtext['cantsave'], 'error')


def file_saveas(trans=True):
    dirname = dialog.open(path=ur(con.lastpath_img), ext=[
        'jpg',
        'png',
        'gif',
        'bmp',
        'mbm',
        'jpeg'], kind='save')
    if dirname is None:
        return False

    if path.isfile(ur(dirname)):
        defname = path.split(dirname)[1]
    else:
        defname = u'image_'
    dirname = path.split(dirname)[0] + '\\'
    dirname = dirname.replace('\\\\', '\\')
    con.lastpath_img = dirname
    confirm = False
    while not confirm:
        name = appuifw.query(dtext['entername'], 'text', defname)
        if name is None:
            return False

        imwin.filename = dirname + name
        name = [
            u'PNG - Portable Network Graphics',
            u'JPG - JPEG']
        ind = appuifw.popup_menu(name, dtext['format'])
        if ind is None:
            return False
        elif ind == 0:
            imwin.frmt = 'PNG'
            if not imwin.filename.lower().endswith('.png'):
                imwin.filename += '.png'

        elif ind == 1:
            imwin.frmt = 'JPEG'
            if not imwin.filename.lower().endswith('.jpg') and not imwin.filename.lower().endswith('.jpeg'):
                imwin.filename += '.jpg'

        if path.exists(ur(imwin.filename)):
            confirm = appuifw.query(dtext['owconfirm'], 'query')
        else:
            confirm = True
        continue
        None
    file_save(frmt=imwin.frmt, trans=trans)
    return True


def AskTransparent():
    name = [
        dtext['wotrans'],
        dtext['addtrans']]
    ind = appuifw.popup_menu(name, dtext['usetrans'])
    if ind is None:
        return False
    elif ind == 0:
        return False
    elif ind == 1:
        ChoseColor(dtext['colchoosetip'])
        return True


def ChoseColor(text):
    global curtool
    appuifw.note(text)
    oldforeclr = foreclr
    oldtool = curtool
    curtool = tool['picker']
    imwin.obj = tool['picker']
    imwin.drawing = False
    imwin.selector.set(None)
    imwin.waitpickerchoose = True

    imwin.pickercallback = lambda: UseTransparent(oldforeclr, oldtool)


def UseTransparent(oldforeclr, oldtool):
    global foreclr
    SV_TRANS.file_transparent(imwin.filename, inttorgb(foreclr), progressbar.update, dtext)
    appuifw.note(dtext['saved'] + unicode(imwin.filename))
    foreclr = oldforeclr
    curtool = oldtool
    imwin.obj = oldtool


def query_file_new(win):
    size = con.screen_size
    if classes.TUniSlector.copybuff != None:
        size = classes.TUniSlector.copybuff.size

    w = appuifw.query(dtext['width'], 'number', size[0])
    if w is not None:
        h = appuifw.query(dtext['height'], 'number', size[1])
        if h is not None:
            file_new(w, h, win)


def image_tobpp(img, bpp):
    im = new_image(img.size, mode=bpp)
    if im is None:
        return None

    im.blit(img)
    img = im
    return img


def fontstd_select():
    global bmpfont
    appuifw.app.screen = 'normal'
    fonts = appuifw.available_fonts()
    ind = appuifw.selection_list(fonts)
    if ind is not None:
        if s60_version_info == (3, 0):
            imwin.obj_font = (fonts[ind], stdfontsize, graphics.FONT_ANTIALIAS)
        else:
            imwin.obj_font = fonts[ind]
        bmpfont = None

    appuifw.app.screen = 'full'


def fontstd_opt():
    global stdfontsize, fontflags, stdfontsize, fontflags
    if s60_version_info != (3, 0):
        return None

    foptcont = [
        (dtext['size'], 'number', stdfontsize),
        (dtext['italic'], 'combo', ([
                                        dtext['no'],
                                        dtext['yes']], fontflags[0])),
        (dtext['bold'], 'combo', ([
                                      dtext['no'],
                                      dtext['yes']], fontflags[1])),
        (dtext['antialias'], 'combo', ([
                                           dtext['no'],
                                           dtext['yes']], fontflags[2]))]
    foptform = appuifw.Form(foptcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    appuifw.app.screen = 'normal'
    appuifw.app.title = dtext['font']
    foptform.execute()
    fg = 0
    if foptform[1][2][1] == 1:
        fg = fg | graphics.FONT_ITALIC

    if foptform[2][2][1] == 1:
        fg = fg | graphics.FONT_BOLD

    if foptform[3][2][1] == 1:
        fg = fg | graphics.FONT_ANTIALIAS

    stdfontsize = int(foptform[0][2])
    fontflags = [
        int(foptform[1][2][1]),
        int(foptform[2][2][1]),
        int(foptform[3][2][1])]
    appuifw.app.screen = 'full'
    appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
    imwin.obj_font = (imwin.obj_font[0], stdfontsize, fg)


def changebpp():
    bpp = [
        '1',
        'L',
        'RGB12',
        'RGB16',
        'RGB']
    name = [
        dtext['bpp_1'],
        dtext['bpp_8'],
        dtext['bpp_12'],
        dtext['bpp_16'],
        dtext['bpp_24']]
    ind = appuifw.popup_menu(name, dtext['bpp'])
    if ind is not None:
        imwin.img = image_tobpp(imwin.img, bpp[ind])


def query_rgb(text, source=(0, 0, 0)):
    if type(source) is type(1):
        src = u'%06x' % source
    else:
        src = rgbtohex(source)
    color = appuifw.query(text, 'text', src)
    if color is None:
        return None

    if color.find('.') != -1:

        try:
           # continue
            color = []([int(x) for x in color.split('.')])
            if len(color) != 3:
                appuifw.note(dtext['error_unexpchars'], 'error')
                return None
        except:
            None
            None
            None
            appuifw.note(dtext['error_unexpchars'], 'error')
            return None

    else:

        try:
            color = inttorgb(int(color, 16))
        except:
            None
            None
            None
            appuifw.note(dtext['error_unexpchars'], 'error')
            return None

    return color


def inttorgb(color):
    b = color % 256
    g = color / 256 % 256
    r = color / 256 / 256 % 256
    return (r, g, b)


def rgbtoint(c):
    return c[0] * 65536 + c[1] * 256 + c[2]


def rgbtohex(c):
    return u'%06x' % (c[0] * 65536 + c[1] * 256 + c[2])


def hextorgb(color):
    return inttorgb(int(color, 16))


def updatecallback(cur, total):
    mbox_percent.draw(dtext['processing'])
    progressbar.percent(cur * 100 / total)
    progressbar.draw()


def image_tomask():
    imwin._backupimage()
    name = [
        dtext['normal'],
        dtext['invert']]
    ind = appuifw.popup_menu(name, dtext['masktype'])
    if ind is None:
        return None

    mbox_percent.draw(dtext['processing'])
    if ind == 0:
        (img, msk) = improc._image_tomaskblack(GetSelectedImage(), inttorgb(foreclr), updatecallback)
    else:
        (img, msk) = improc._image_tomaskwhite(GetSelectedImage(), inttorgb(foreclr), updatecallback)
    imwin.selector.setimage((img, msk))


def image_invertcolors():
    name = [
        dtext['full'],
        dtext['singlech']]
    ind = appuifw.popup_menu(name, dtext['invertmode'])
    if ind is None:
        return None

    if ind == 0:
        imwin._backupimage()
        mbox_percent.draw(dtext['processing'])
        (img, msk) = improc._image_invertcolors(GetSelectedImage(), updatecallback)
    elif ind == 1:
        name = [
            dtext['red'],
            dtext['green'],
            dtext['blue']]
        ind = appuifw.popup_menu(name, dtext['invertcolorch'])
        if ind is None:
            return None

        imwin._backupimage()
        mbox_percent.draw(dtext['processing'])
        (img, msk) = improc._image_invertcolor_channel(GetSelectedImage(), updatecallback, ind)

    imwin.selector.setimage((img, msk))


def image_colorbalance():
    col = query_rgb(u'R.G.B (-100.-100.-100)-(100.100.100)', (0, 0, 0))
    if col is None:
        return None

    for val in col:
        if val > 100 or val < -100:
            appuifw.note(dtext['badvalue'], 'error')
            return None

    imwin._backupimage()
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_colorbalance(GetSelectedImage(), col, updatecallback)
    imwin.selector.setimage((img, msk))


def image_saturation():
    val = appuifw.query(dtext['enterval'] + u'(0-200)', 'number', 100)
    if val is None:
        return None

    if val > 200:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_saturation(GetSelectedImage(), val, updatecallback)
    imwin.selector.setimage((img, msk))


def image_sepia():
    imwin._backupimage()
    (img, msk) = improc._image_sepia(GetSelectedImage(), updatecallback)
    imwin.selector.setimage((img, msk))


def image_posterize():
    imwin._backupimage()
    (img, msk) = improc._image_posterize(GetSelectedImage(), updatecallback)
    imwin.selector.setimage((img, msk))


def image_fractal():
    name = [
        dtext['red'],
        dtext['green'],
        dtext['blue'],
        dtext['entercolor']]
    ind = appuifw.popup_menu(name, dtext['color'] + u':')
    if ind is None:
        return None
    elif ind == 0:
        col = hextorgb('0x070000')
    elif ind == 1:
        col = hextorgb('0x000700')
    elif ind == 2:
        col = hextorgb('0x000007')
    elif ind == 3:
        rgb = [
            0,
            0,
            0]
        rgb[int(uniform(0, 3))] = int(uniform(0, 256))
        col = query_rgb(dtext['color'] + u':', tuple(rgb))

    if col is None:
        return None

    imwin._backupimage()
    (img, msk) = improc._image_fractal(GetSelectedImage(), col, updatecallback)
    imwin.selector.setimage((img, msk))


def image_fractal_mandelbrot():
    imwin._backupimage()
    (img, msk) = improc._image_fractal_mandelbrot(GetSelectedImage(), iterations=25, scale=60, callback=updatecallback)
    imwin.selector.setimage((img, msk))


def image_gradient(knd):
    if knd == 0:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 0))
    elif knd == 1:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 2))
    elif knd == 2:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 1))
    elif knd == 3:
        imwin._backupimage()
        (img, msk) = improc._image_gradient(GetSelectedImage(), (foreclr, backclr, 3))

    imwin.selector.setimage((img, msk))


def image_replacecolor():
    source = imwin.img.getpixel((imwin.curs.x, imwin.curs.y))[0]
    mbox_percent.draw(dtext['processing'])
    (img, msk) = improc._image_replacecolor(GetSelectedImage(), source, inttorgb(foreclr), updatecallback)
    imwin.selector.setimage((img, msk))


def image_replacecolor_query():
    source = imwin.img.getpixel((imwin.curs.x + imwin.imx, imwin.curs.y + imwin.imy))[0]
    repcolor = query_rgb(dtext['repcolor'], source)
    if repcolor is None:
        return None

    descolor = query_rgb(dtext['descolor'], foreclr)
    if descolor is None:
        return None

    imwin._backupimage()
    mbox_percent.draw(dtext['replacecolor'])
    (img, msk) = improc._image_replacecolor(GetSelectedImage(), repcolor, descolor, updatecallback)
    imwin.selector.setimage((img, msk))


def image_convertbpp(im, bpp):
    img = new_image(im.size, mode=bpp)
    if img is None:
        return None

    img.blit(im)
    return img


def image_flip():
    ind = appuifw.popup_menu([
        dtext['vertical'],
        dtext['horizontal']], dtext['flip'])
    if ind is None:
        return None

    imwin._backupimage()
    if ind == 1:
        (img, msk) = improc._image_flip(graphics.FLIP_LEFT_RIGHT, imwin)
    elif ind == 0:
        (img, msk) = improc._image_flip(graphics.FLIP_TOP_BOTTOM, imwin)


def image_rotate_():
    imwin._backupimage()
    name = [
        dtext['rotateright'],
        dtext['rotateleft']]
    ind = appuifw.popup_menu(name, dtext['rotate'])
    if ind == 1:
        (img, msk) = improc._image_rotate(graphics.ROTATE_90, imwin, workzone)
    elif ind == 0:
        (img, msk) = improc._image_rotate(graphics.ROTATE_270, imwin, workzone)


def image_rotate():
    imwin._backupimage()
    if imwin.selector.isactive():
        angle = appuifw.query(u'\xe8\xbe\x93\xe5\x85\xa5\xe6\x97\x8b\xe8\xbd\xac\xe8\xa7\x92\xe5\xba\xa6', 'number', 0)
        if angle is None:
            return None

        mode = 0
        (img, msk) = improc._image_rotateangle(GetSelectedImage(), angle, backclr, updatecallback, mode)
        Selection_SetImageCenter((img, msk))
    else:
        image_rotate_()


def image_resize_query():
    name = [
        u'\xe5\x83\x8f\xe7\xb4\xa0',
        u'%']
    ind = appuifw.popup_menu(name, dtext['resize'])
    if ind == 0:
        width = appuifw.query(dtext['width'], 'number', imwin.img.size[0])
        if width is not None:
            height = appuifw.query(dtext['height'], 'number', imwin.img.size[1])
            if height is not None:
                asp = appuifw.query(dtext['keepaspect'], 'query')
                if asp is None:
                    asp = 0
                else:
                    asp = 1
                imwin._backupimage()
                (img, msk) = improc._image_resize(GetSelectedImage(), ((width, height), asp, workzone), imwin)
                imwin.selector.setimage((img, msk))


    elif ind == 1:
        size = imwin.img.size
        width = appuifw.query(dtext['width'] + u'(%)', 'number', 100)
        if width is not None:
            height = appuifw.query(dtext['height'] + u'(%)', 'number', 100)
            if height is not None:
                asp = appuifw.query(dtext['keepaspect'], 'query')
                if asp is None:
                    asp = 0
                else:
                    asp = 1
                imwin._backupimage()
                (img, msk) = improc._image_resize(GetSelectedImage(),
                                                  ((size[0] * width / 100, size[1] * height / 100), asp, workzone),
                                                  imwin)
                imwin.selector.setimage((img, msk))


def image_resizecanvas(sz):
    im = new_image(sz)
    if im is None:
        return None

    imwin.size((min(im.size[0], workzone[0]), min(im.size[1], workzone[1])))
    im.blit(imwin.img)
    imwin.img = im
    imwin.image_coord(0, 0)


def image_resizecanvas_query():
    name = [
        u'\xe5\x83\x8f\xe7\xb4\xa0',
        u'%']
    ind = appuifw.popup_menu(name, dtext['resizecanvas'])
    if ind == 0:
        width = appuifw.query(dtext['width'], 'number', imwin.img.size[0])
        if width is not None:
            height = appuifw.query(dtext['height'], 'number', imwin.img.size[1])
            if height is not None:
                image_resizecanvas((width, height))


    elif ind == 1:
        size = imwin.img.size
        width = appuifw.query(dtext['width'] + u'(%)', 'number', 100)
        if width is not None:
            height = appuifw.query(dtext['height'] + u'(%)', 'number', 100)
            if height is not None:
                image_resizecanvas((width * size[0] / 100, height * size[1] / 100))


def image_crop():
    if imwin.selector.isactive():
        imwin._backupimage()
        (image, mask) = imwin.selector.getimage()
        image_resizecanvas(image.size)
        imwin.img = image
        imwin.selector.tool.deselect()
        imwin.image_coord(0, 0)


def image_bpp(bpp):
    imwin._backupimage()
    (image, mask) = GetSelectedImage()
    img = new_image(image.size, mode=bpp)
    img.blit(image)
    im = new_image(image.size, mode='RGB16')
    im.blit(img)
    imwin.selector.setimage((im, mask), replace=True)


def image_lightness_query():
    value = appuifw.query(dtext['enterval'] + '(0%-100%)', 'number', 0)
    if value is None:
        return None

    if value > 100:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    value = 255 * value / 100
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_lightness_slow(GetSelectedImage(), value)
    else:
        (img, msk) = improc._image_lightness(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_darkness_query():
    value = appuifw.query(dtext['enterval'] + u'(0%-100%)', 'number', 0)
    if value is None:
        return None

    if value > 100:
        appuifw.note(dtext['badvalue'], 'error')
        return None

    imwin._backupimage()
    value = 255 * value / 100
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_darkness_slow(GetSelectedImage(), value)
    else:
        (img, msk) = improc._image_darkness(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_blur_query():
    imwin._backupimage()
    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        (img, msk) = improc._image_blur_bysizing(imwin.img)
    else:
        value = 100
        (img, msk) = improc._image_blur(GetSelectedImage(), value)
    imwin.selector.setimage((img, msk))


def image_displacement():
    vert = appuifw.popup_menu([
        dtext['horizontal'],
        dtext['vertical']], dtext['displacement'])
    if vert is None:
        return None

    value = appuifw.query(dtext['angle'], 'number', 0)
    if value is None:
        return None

    imwin._backupimage()
    (img, msk) = improc._image_displacement(GetSelectedImage(), value, vert, backclr, updatecallback)
    imwin.selector.setimage((img, msk))


def GetSelectedImage():
    (image, mask) = imwin.selector.getimage(replace=True)
    return (image, mask)


def Selection_SetImageCenter(_0):
    (im, ms) = _0
    (image, mask) = imwin.selector.getimage(replace=True)
    dx = (im.size[0] - image.size[0]) / 2
    dy = (im.size[1] - image.size[1]) / 2
    (x1, y1, x2, y2) = imwin.selector.getcoord()
    imwin.img.blit(im, target=(x1 - dx, y1 - dy), mask=ms)


def theme_open():
    fname = dialog_misc.open(path=program_path + 'Themes\\', ext=[
        'thm'], kind='open')
    if fname is None:
        return None

    if theme_load(fname):
        ui_colors_update()


def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args + fargs, **args + fargs)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def plugins_findmods():
    plugins = []
    if path.exists(program_path + 'Plugins\\dontloadplugins'):
        return plugins

    for x in listdir(program_path + 'Plugins\\'):
        if path.isfile(program_path + 'Plugins\\' + x):
            if x.lower().endswith('.py') or x.lower().endswith('.pyc'):
                plugins.append(path.splitext(x)[0])

    return plugins


def plugins_importmods(plugins):
    modules = []
    sys.path.insert(0, program_path + 'Plugins\\')
    for t in plugins:

        try:
            modules.append(__import__(t))
        except Exception:
            None
            exc = None
            None
            traceback.print_exc(sys.stderr)
            appuifw.note(dtext['invalidplugin'] + ': ' + t)
        except:
            None

    return modules


def plugins_splittext(text, num):
    words = text.split(' ')
    delmt = u' '
    text = u''
    info = []
    for t in xrange(len(words)):
        text += words[t] + delmt
        if len(text) > num:
            text = text[:-1]
            info.append(text)
            text = u''
        elif len(text) <= num and t == len(words) - 1:
            text = text[:-1]
            info.append(text)

    return info


def plugins_function(m):
    try:
        imwin._backupimage()
        if m.__version_info__[3] == '1.0':
            (img, msk) = m.Execute(GetSelectedImage(), ProgressCallback)
        elif m.__version_info__[3] == '1.1':
            (img, msk) = m.Execute((GetSelectedImage(), (foreclr, backclr), imwin.bsize, ProgressCallback))

        imwin.selector.setimage((img, msk), replace=True)
    except:
        None
        None
        None
        traceback.print_exc(sys.stderr)
        appuifw.note(dtext['invalidplugin'], 'error')


def plugins_createmenu(modules, files):
    if modules:
        it = []
        ab = [
            u'',
            u'Plugins and Contributors:',
            u'']
        for t in xrange(len(modules)):

            try:
                it.append((modules[t].__version_info__[1], partial(plugins_function, modules[t])))
                if modules[t].__version_info__[0] == u'internal':
                    continue

                info = plugins_splittext(
                    u'  ' + modules[t].__version_info__[1] + ' ' + modules[t].__version_info__[2] + ' - ' +
                    modules[t].__version_info__[0], 22)
                ab.extend(info)
                ab.append('')
            except Exception:
                None
                exc = None
                None
                traceback.print_exc(sys.stderr)
                appuifw.note(dtext['invalidplugin'] + ': ' + files[t], 'error')
                continue
            except:
                None

        if len(ab) == 3:
            ab = []
        else:
            ab.append(u'')
        items = tuple(it)
        return ((dtext['plugins'], items), ab)
    else:
        return ((dtext['plugins'], (lambda: None)), [
            u''])


def plugins_load():
    f = plugins_findmods()
    m = plugins_importmods(f)
    menu = plugins_createmenu(m, f)
    return menu


def ProgressCallback(cur, total):
    mbox_percent.draw(dtext['processing'])
    progressbar.percent(cur * 100 / total)
    progressbar.draw()
    if keyboard.is_down(key_codes.EScancodeRightSoftkey):
        return False

    ao_sleep(0.001)


def skin_select():
    #continue
    name = []
    ind = appuifw.popup_menu(name, dtext['skinselect'])
    if ind is None:
        return None

    if not skin_check(program_path + 'skin\\' + name[ind] + '\\'):
        return None

    oldskin = con.skin
    con.skin = name[ind]
    file_copy(program_path + 'skin\\id_logo.png', program_path + 'skin\\' + con.skin + '\\id_logo.png')
    appuifw.note(dtext['restart'])


def skin_check(folder):
    files = (
    'Pencil_32.png', 'Brush_32.png', 'Erase_32.png', 'Line2_32.png', 'Rect_32.png', 'Ellipse_32.png', 'Select_32.png',
    'El_Select.png', 'Cstamp_32.png', 'Picker_32.png', 'Notemlet_32.png', 'Text_32.png', 'Polygon_32.png',
    'Broken_32.png', 'PaintBucket_32.png', 'Spray_32.png', 'Lasso.png', 'mrod.png', 'Grad_vert.png', 'Grad_cir.png',
    'Grad_gor.png', 'Grad_rect.png', 'f.png', 'c.png', 'b.png', 'black-white.png', 'color_black.png', 't.png',
    'color_white.png', 'drive.png', 'drive_mask.png', 'dir.png', 'dir_mask.png', 'im_green.png', 'im_blue.png',
    'im_red.png', 'im_yellow.png', 'im_gray.png', '1.png', '2.png', '3.png', '4.png', '5.png', '6.png')
    missed = ''
    for f in files:
        if not path.exists(folder + f):
            missed += f + ', '

    if missed != '':
        missed = missed[:-2]
        appuifw.note(dtext['invalidskin'] + ' ' + unicode(missed), 'error')
        return False

    return True


def theme_load(theme):
    if theme is None:
        return None

    try:
        parser = iniparser.TIniParser()
        parser.open(ur(theme))
        parser.readgroup('UI_COLORS')
        con.ui_menu_color = [
            [
                0,
                0,
                0],
            [
                0,
                0,
                0,
                0,
                0]]
        con.ui_form_color = [
            0,
            0,
            0,
            [
                0,
                0,
                0]]
        con.ui_menu_color[0][0] = parser.readint('menu_form_out', 16)
        con.ui_menu_color[0][1] = parser.readint('menu_form_in', 16)
        con.ui_menu_color[0][2] = parser.readint('menu_form_shade', 16)
        con.ui_menu_color[1][0] = parser.readint('menu_selbox_out', 16)
        con.ui_menu_color[1][1] = parser.readint('menu_selbox_in', 16)
        con.ui_menu_color[1][2] = parser.readint('menu_item', 16)
        con.ui_menu_color[1][3] = parser.readint('menu_selitem', 16)
        con.ui_menu_color[1][4] = parser.readint('menu_blckitem', 16)
        con.ui_form_color[2] = parser.readint('backgr_form', 16)
        con.ui_form_color[0] = parser.readint('status_form', 16)
        con.ui_form_color[1] = parser.readint('status_font', 16)
        con.ui_form_color[3][0] = parser.readint('editor_scroll_outline', 16)
        con.ui_form_color[3][1] = parser.readint('editor_scroll_slider', 16)
        con.ui_form_color[3][2] = parser.readint('editor_scroll_fill', 16)
        con.ui_grid_color = parser.readint('grid_selector_color', 16)
        con.ui_req_color = [
            0,
            0,
            [
                0,
                0,
                0,
                0,
                0,
                0],
            [
                0,
                0,
                0]]
        con.ui_req_color[0] = parser.readint('fileman_background', 16)
        con.ui_req_color[1] = parser.readint('fileman_infobar', 16)
        con.ui_req_color[2][0] = parser.readint('fileman_selbox_out', 16)
        con.ui_req_color[2][1] = parser.readint('fileman_selbox_in', 16)
        con.ui_req_color[2][2] = parser.readint('fileman_item', 16)
        con.ui_req_color[2][3] = parser.readint('fileman_selitem', 16)
        con.ui_req_color[2][4] = parser.readint('fileman_markitem', 16)
        con.ui_req_color[3][0] = parser.readint('fileman_scroll_outline', 16)
        con.ui_req_color[3][1] = parser.readint('fileman_scroll_slider', 16)
        con.ui_req_color[3][2] = parser.readint('fileman_scroll_fill', 16)
        con.ui_prog_color[0] = parser.readint('progressbar_out', 16)
        con.ui_prog_color[1] = parser.readint('progressbar_slider', 16)
        con.ui_prog_color[2] = parser.readint('progressbar_fill', 16)
        parser.close()
        return True
    except:
        None
        None
        None
        appuifw.note(dtext['invalidplugin'], 'error')
        return False


def ui_colors_update():
    mainmenu.colors(con.ui_menu_color)
    menu_preview.colors(con.ui_menu_color)
    menu_palette.colors(con.ui_menu_color)
    popupmenu.colors(con.ui_menu_color)
    mbox_percent.clrs = [
        con.ui_menu_color[1][2],
        con.ui_menu_color[1][1],
        con.ui_menu_color[1][3]]
    dialog.colors(con.ui_req_color)
    dialog_tmp.colors(con.ui_req_color)
    dialog_pal.colors(con.ui_req_color)
    dialog_img.colors(con.ui_req_color)
    dialog_misc.colors(con.ui_req_color)
    scrollbar_imw[0].color(con.ui_form_color[3])
    scrollbar_imw[1].color(con.ui_form_color[3])
    menu_about.clrs = (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2])
    mess_info.clrs = (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2])
    toolslist.rectcolor(con.ui_grid_color)
    colorgrid.rectcolor(con.ui_grid_color)
    gradgrid.rectcolor(con.ui_grid_color)


def font_open():
    fname = dialog_misc.open(path=ur(lastpath_fnt), ext=[
        'rfn'], kind='open')
    if fname is None:
        return None

    font_load(fname)


def font_load(pth):
    global bmpfont, fontname, codemap, bmpfont, fontname, codemap
    bmpfont = graphics.Image.open(pth)
    fontname = path.splitext(path.split(pth)[1])[0]
    font_parse(bmpfont)
    if not path.isfile(program_path + 'chars.map'):
        appuifw.note(u'Chars.map not found!')

    codef = open(program_path + 'chars.map', 'rt')
    codeline = codef.readline().decode('utf-8')
    codef.close()
    codemap = codeline
    font_updatemess(imwin.obj_text)


def font_parse(img):
    if font_loadchache():
        return None

    tcoord = 0
    pdraw = progressbar.draw
    percent = progressbar.percent
    mbox_percent.draw(dtext['fontcaching'])
    cellh = img.size[1] / 14
    cellw = img.size[0] / 16
    ao_sleep(0.001)
    backcol = img.getpixel((0, 0))[0]
    y = 0
    for n in xrange(16):
        x = 0
        y1 = cellh * n
        y2 = cellh * (n + 1)
        for t in xrange(16):
            (x1, x2) = ip_getcolumnx2(img, (cellw * t, cellw * (t + 1) - 5, y1, y2), backcol)
            if x1 is not None:
                symbols[16 * n + t] = (x1, y1, x2, y2)
                tcoord = (tcoord + x2 - x1) + 1

        percent(n * 100 / 15)
        pdraw()
        if keyboard.is_down(key_codes.EScancodeRightSoftkey):
            return False

        ao_sleep(0.001)

    symbols[0][0] = 0
    symbols[0][1] = 0
    symbols[0][2] = cellw / 3
    symbols[0][3] = cellh
    font_savechache()
    appuifw.note(dtext['fontloaded'])


def font_savechache():
    pars = iniparser.TIniParser()
    pars.create(program_path + 'Fonts\\' + fontname + '.cch')
    pars.writegroup('SYMBOLS')
    n = 0
    for t in symbols:
        pars.writeint(str(n), t)
        n += 1

    pars.close()


def font_loadchache():
    pdraw = progressbar.draw
    percent = progressbar.percent
    pars = iniparser.TIniParser()
    if not path.isfile(program_path + 'Fonts\\' + fontname + '.cch'):
        return False

    pars.open(program_path + 'Fonts\\' + fontname + '.cch')
    dic = pars.getdict('SYMBOLS')
    pars.close()
    for t in xrange(0, 256):
        continue
        symbols[t] = [int(x) for x in dic[str(t)].split(',')]

    return True


def font_updatemess(text):
    global fontbuff, fontbuffmsk, graymask, fontbuff, fontbuffmsk, graymask
    if text is None:
        return None

    if bmpfont is not None:
        ordlist = []
        twidth = 0
        theight = 0
        for t in xrange(len(text)):
            ind = codemap.find(text[t])
            if ind == -1:
                ind = 31

            ordlist.append(ind - 1)

        for t in ordlist:
            twidth += (symbols[t][2] - symbols[t][0]) * fontscalex + fntsymbolsdelay
            theight = max(theight, (symbols[t][3] - symbols[t][1]) * fontscaley)

        fontbuff = new_image((twidth, theight))
        fontbuff.clear(0)
        fontbuffmsk = new_image((twidth, theight), 'L')
        graymask = new_image(bmpfont.size, 'L')
        coordx = 0
        for t in ordlist:
            if fontscalex != 1 or fontscaley != 1:
                tmpimg = new_image(
                    ((symbols[t][2] - symbols[t][0]) * fontscalex, (symbols[t][3] - symbols[t][1]) * fontscaley), '1')
                tmpimg.blit(bmpfont, source=symbols[t], scale=1)
                fontbuff.blit(tmpimg, target=(coordx, 0))
                coordx += (symbols[t][2] - symbols[t][0]) * fontscalex + fntsymbolsdelay
            else:
                fontbuff.blit(bmpfont, source=symbols[t], target=(coordx, 0), mask=graymask)
                coordx += (symbols[t][2] - symbols[t][0]) + fntsymbolsdelay

        fontbuffmsk.blit(fontbuff)
        fontbuff.clear(foreclr)


def font_opt():
    global fntsymbolsdelay, fontscalex, fontscaley, fntsymbolsdelay, fontscalex, fontscaley
    foptcont = [
        (dtext['extfont_ldelay'], 'number', fntsymbolsdelay),
        (dtext['extfont_scalex'], 'number', int(fontscalex * 100)),
        (dtext['extfont_scaley'], 'number', int(fontscaley * 100))]
    foptform = appuifw.Form(foptcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    appuifw.app.screen = 'normal'
    appuifw.app.title = dtext['font']
    foptform.execute()
    fntsymbolsdelay = int(foptform[0][2])
    fontscalex = float(foptform[1][2]) / 100.0
    fontscaley = float(foptform[2][2]) / 100.0
    appuifw.app.screen = 'full'
    appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
    font_updatemess(imwin.obj_text)


def ip_isemptyline(img, y, _4, backcol):
    (x1, x2) = _4
    for x in xrange(x1, x2):
        col = img.getpixel((x, y))[0]
        if col != backcol:
            return (x, y)

    return True


def ip_isemptycolumn(img, x, _4, backcol):
    (y1, y2) = _4
    for y in xrange(y1, y2):
        col = img.getpixel((x, y))[0]
        if col != backcol:
            return (x, y)

    return True


def ip_getliney(img, sy, _4, backcol):
    (x1, x2) = _4
    top = True
    y1 = None
    y2 = None
    for y in xrange(sy, img.size[1]):
        top = ip_isemptyline(img, y, (x1, x2), backcol)
        if top == True:
            pass
        1
        y1 = top[1]
        break

    if y1 is None:
        return (None, None)

    for yy in xrange(y1, img.size[1]):
        top = ip_isemptyline(img, yy, (x1, x2), backcol)
        if top != True:
            y2 = top[1]
        else:
            break

    return (y1, y2)


def ip_getcolumnx2(img, _2, backcol):
    (sx, ex, y1, y2) = _2
    dot = None
    x1 = None
    x2 = None
    for x in xrange(sx, ex):
        for y in xrange(y1, y2):
            col = img.getpixel((x, y))[0]
            if col != backcol:
                dot = (x, y)

        if dot is not None:
            x1 = dot[0]
            break

    if x1 is None:
        return (None, None)

    for xx in xrange(x1, ex):
        for y in xrange(y1, y2):
            col = img.getpixel((xx, y))[0]
            if col != backcol:
                dot = (xx, y)

        if dot is not None:
            x2 = dot[0] + 1

    return (x1, x2)


def ip_getcolumnx(img, sx, _4, backcol):
    (y1, y2) = _4
    top = True
    x1 = None
    x2 = None
    for x in xrange(sx, img.size[0]):
        top = ip_isemptycolumn(img, x, (y1, y2), backcol)
        if top == True:
            pass
        1
        x1 = top[0]
        break

    if x1 is None:
        return (None, None)

    for xx in xrange(x1, img.size[0]):
        top = ip_isemptycolumn(img, xx, (y1, y2), backcol)
        if top != True:
            x2 = top[0] + 1
        else:
            break

    return (x1, x2)


def undo():
    imwin.undo()


def redo():
    imwin.redo()


def _fill_check(img, _2, c, flabel):
    global _fill_queue
    (x, yu, yd) = _2
    iu = yu
    getpixel = img.getpixel
    fqueue = _fill_queue
    fheight = _fill_height
    if iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c:
        f = 0
    else:
        f = 1
    while iu >= 0 and flabel[x][iu] == 0 and getpixel((x, iu))[0] == c:
        iu -= 1
        continue
        None
    iu += 1
    i = iu
    id = yu
    for id in xrange(yu, yd):
        if flabel[x][id] == 0 and getpixel((x, id))[0] == c:
            if f:
                f = 0
                i = id

        elif f == 0:
            fqueue += [
                (x, i, id)]
            f = 1

    if f == 0:
        while id < fheight and flabel[x][id] == 0 and getpixel((x, id))[0] == c:
            id += 1
            continue
            None
        fqueue += [
            (x, i, id)]

    _fill_queue = fqueue
    flabel[x][iu:id] = (id - iu) * [
        1]
    return flabel


def fillimage(img, _2, color, callback=None):
    global _fill_width, _fill_height, _fill_queue, _fill_width, _fill_height, _fill_queue
    (x, y) = _2
    line = img.line
    (_fill_width, _fill_height) = img.size
    if 0 <= x:
        pass
    x < _fill_width
    if 1:
        if 0 <= y:
            pass
        y < _fill_height
    if not 1:
        return 0

    if type(color) == type(1):
        cr = color / 65536
        cg = (color % 65536) / 256
        cb = color % 256
        color = (cr, cg, cb)

    c = img.getpixel((x, y))[0]
    if color == c:
        return 0

    _fill_queue = []
    flabel = []
    for i in xrange(_fill_width):
        s = []
        for j in xrange(_fill_height):
            s += [
                0]

        flabel += [
            s]

    flabel = _fill_check(img, (x, y, y + 1), c, flabel)
    while _fill_queue:
        (x, yu, yd) = _fill_queue[0]
        _fill_queue = _fill_queue[1:]
        if callback:
            if callback():
                return None

        line((x, yu, x, yd), color)
        flabel[x][yu:yd] = (yd - yu) * [
            1]
        if x > 0:
            flabel = _fill_check(img, (x - 1, yu, yd), c, flabel)

        if x < _fill_width - 1:
            flabel = _fill_check(img, (x + 1, yu, yd), c, flabel)

        continue
        None
    if callback:
        callback()


def mrod_select(img, _2, color, callback=None):
    global _fill_width, _fill_height, _fill_queue, _fill_width, _fill_height, _fill_queue
    (x, y) = _2
    mask = graphics.Image.new(img.size, '1')
    mask.clear(0)
    (_fill_width, _fill_height) = img.size
    if 0 <= x:
        pass
    x < _fill_width
    if 1:
        if 0 <= y:
            pass
        y < _fill_height
    if not 1:
        return 0

    if type(color) == type(1):
        cr = color / 65536
        cg = (color % 65536) / 256
        cb = color % 256
        color = (cr, cg, cb)

    c = img.getpixel((x, y))[0]
    if color == c:
        return 0

    _fill_queue = []
    flabel = []
    for i in xrange(_fill_width):
        s = []
        for j in xrange(_fill_height):
            s += [
                0]

        flabel += [
            s]

    flabel = _fill_check(img, (x, y, y + 1), c, flabel)
    while _fill_queue:
        (x, yu, yd) = _fill_queue[0]
        _fill_queue = _fill_queue[1:]
        if callback:
            if callback():
                return None

        mask.line((x, yu, x, yd), color)
        flabel[x][yu:yd] = (yd - yu) * [
            1]
        if x > 0:
            flabel = _fill_check(img, (x - 1, yu, yd), c, flabel)

        if x < _fill_width - 1:
            flabel = _fill_check(img, (x + 1, yu, yd), c, flabel)

        continue
        None
    if callback:
        callback()

    return (img, mask)


def zoomimage():
    name = [
        dtext['zoomin'],
        dtext['zoomout'],
        dtext['zoom_multiply'],
        dtext['zoom_1_1']]
    ind = appuifw.popup_menu(name, dtext['zoom'])
    if ind == 0:
        zoom_in()
    elif ind == 1:
        zoom_out()
    elif ind == 2:
        zoom_multiply_query()
    elif ind == 3:
        zoom_1_1()


def changecursor():
    if con.cursormultiplier > 1:
        if imwin.zoom >= con.cursormultiplier and imwin.curs.oldsize is None:
            imwin.curs.oldsize = imwin.curs.size
            imwin.curs.size = 1
        elif imwin.zoom < con.cursormultiplier and imwin.curs.oldsize is not None:
            imwin.curs.size = imwin.curs.oldsize
            imwin.curs.oldsize = None


def _zoom():
    global zoomzone, zoombuff, zoomzone, zoombuff, zoomzone, zoombuff, zoomzone, zoombuff
    if imwin.zoom >= 1:
        zoom = 1 * imwin.zoom
        zoom_w = workzone[0] / zoom
        zoom_h = workzone[1] / zoom
        zoomzone = (0, 0, zoom_w, zoom_h)
        zoomsize = (zoom_w, zoom_h)
        zoombuff = new_image(workzone)
        if zoombuff is None:
            return None

        cursc = (imwin.curs.x, imwin.curs.y)
        imwin.image_coord(imwin.curs.x + imwin.imx - zoomsize[0] / 2, imwin.curs.y + imwin.imy - zoomsize[1] / 2)
        imwin.size((min(zoomsize[0], imwin.editsize[0]), min(zoomsize[1], imwin.editsize[1])), False)
        cor = imwin.image_correctcoord()
        imwin.curs.coord((zoomsize[0] / 2 + cor[0], zoomsize[1] / 2 + cor[1]))
        imwin.scale = False
        scrollbar_imw[0].maxvalue(imwin.img.size[0] * zoom)
        scrollbar_imw[1].maxvalue(imwin.img.size[1] * zoom)
        changecursor()
        showtipex(dtext['zoom'] + u': x' + unicode(imwin.zoom))
    else:
        zoom = imwin.zoom
        zoom_w = workzone[0] / zoom
        zoom_h = workzone[1] / zoom
        z = 1
        zz = 1
        if zoom_w > imwin.img.size[0]:
            zoom_w = imwin.img.size[0]
            imwin.zoom = float(workzone[0]) / zoom_w
            zoom = float(workzone[0]) / zoom_w
            zoom_h = workzone[1] / zoom

        if zoom_h > imwin.img.size[1]:
            zoom_h = imwin.img.size[1]
            imwin.zoom = float(workzone[1]) / zoom_h
            zoom = float(workzone[1]) / zoom_h
            zoom_w = workzone[0] / zoom

        zoomzone = (0, 0, zoom_w, zoom_h)
        zoomsize = (zoom_w, zoom_h)
        zoombuff = new_image(workzone)
        if zoombuff is None:
            return None

        cursc = (imwin.curs.x, imwin.curs.y)
        imwin.image_coord(imwin.curs.x + imwin.imx - zoomsize[0] / 2, imwin.curs.y + imwin.imy - zoomsize[1] / 2)
        curszone = imwin.curs.zone()
        imwin.size((zoomsize[0], zoomsize[1]), False)
        cor = imwin.image_correctcoord()
        imwin.curs.coord((zoomsize[0] / 2 + cor[0], zoomsize[1] / 2 + cor[1]))
        imwin.curs.zone(curszone)
        imwin.scale = True
        scrollbar_imw[0].maxvalue(imwin.img.size[0] * zoom)
        scrollbar_imw[1].maxvalue(imwin.img.size[1] * zoom)
        changecursor()


def zoom_in():
    if imwin.zoom < 64:
        imwin.zoom *= 2
        if imwin.zoom > 1 and imwin.zoom < 2:
            imwin.zoom = 1

        _zoom()


def zoom_out():
    if imwin.zoom >= 2:
        imwin.zoom = imwin.zoom / 2

    _zoom()


def zoom_1_1():
    imwin.zoom = 1
    _zoom()


def zoom_multiply(z):
    imwin.zoom = z
    if imwin.zoom > 64:
        imwin.zoom = 64

    if imwin.zoom < 1:
        imwin.zoom = 1

    _zoom()


def preview_hide(state=True):
    onnextcicle_do((lambda: _preview_hide(state)))


def _preview_hide(state=True):
    global preview_exit, prev_vert, preview_exit, redraw, prev_image, prev_coord, preview_exit, prev_vert, preview_exit, redraw, prev_image, prev_coord
    preview_exit = state
    prev_vert = False
    if preview_calc() == False:
        preview_exit = True

    if preview_exit is False:
        redraw = redraw_preview
        wt_ui.Tsysmenu.setcurrent(0, menu_preview)
        wt_ui.Tsysmenu.setcurrent(1, None)
        mainproc_stop()
    else:
        redraw = redraw_main
        wt_ui.Tsysmenu.setcurrent(0, mainmenu)
        wt_ui.Tsysmenu.setcurrent(1, popupmenu)
        del prev_image
        del prev_coord
        mainproc_start()


def preview_calc():
    global prev_image, prev_coord, prev_vert, prev_image, prev_coord, prev_vert
    if prev_vert is True:
        img = imwin.img.transpose(graphics.ROTATE_270)
    else:
        img = imwin.img
    aspect_x = float(img.size[0]) / float(canv.size[0])
    aspect_y = float(img.size[1]) / float(canv.size[1])
    aspect = max(aspect_x, aspect_y)
    if aspect < 1:
        return False
    elif prev_vert is True:
        prev_image = new_image((img.size[0] / aspect, img.size[1] / aspect))
    else:
        prev_image = new_image((img.size[0] / aspect, img.size[1] / aspect))
    if prev_image is None:
        return False

    prev_image.blit(img, scale=1)
    prev_coord = [
        canv.size[0] / 2 - prev_image.size[0] / 2,
        canv.size[1] / 2 - prev_image.size[1] / 2]
    prev_vert = not prev_vert
    return True


def preview_control(evt):
    if evt['scancode'] == key_codes.EScancodeRightSoftkey:
        preview_hide(True)


def zoom_multiply_query():
    z = appuifw.query(dtext['zoom_multiply'], 'number', imwin.zoom)
    zoom_multiply(z)


def templet_create():
    mbox_percent.draw(dtext['templet'])
    (img, msk) = GetSelectedImage()
    image = copy_image(img)
    (mask, msk) = improc._image_tomaskwhite((image, msk), inttorgb(foreclr), updatecallback)
    templet_save(img, mask)


def templet_save(img, mask):
    global lastpath_temp
    dirname = dialog_tmp.open(path=ur(lastpath_temp), ext=[
        'tmb'], kind='save')
    if dirname is None:
        return None

    if path.isfile(ur(dirname)):
        defname = path.split(dirname)[1]
    else:
        defname = u'templet'
    dirname = path.split(dirname)[0] + '\\'
    dirname = dirname.replace('\\\\', '\\')
    lastpath_temp = dirname
    name = appuifw.query(dtext['entername'], 'text', defname)
    if name is None:
        return None

    fname = dirname + name
    mname = dirname + name
    if fname[-4:].lower() != '.tmb':
        fname = fname + '.tmb'

    if mname[-4:].lower() != '.tmb':
        mname = mname + '.msk'
    else:
        mname = mname[:len(mname) - 4] + '.msk'
    appuifw.note(dtext['saved'] + unicode(fname))
    img.save(fname, format='PNG')
    mask.save(mname, format='PNG', bpp=8)


def templet_load():
    global lastpath_temp, templet, lastpath_temp, templet
    fname = dialog_tmp.open(path=ur(lastpath_temp), ext=[
        'tmb'], kind='open')
    if fname is None:
        return None

    lastpath_temp = path.split(fname)[0]
    templet = [
        None,
        None]
    templet[0] = graphics.Image.open(fname)
    if templet[0] is None:
        appuifw.note(dtext['tempbroken'], 'error')
        return None

    templet[1] = graphics.Image.open(fname[:len(fname) - 4] + '.msk')
    if templet[1] is None:
        appuifw.note(dtext['tempbroken'], 'error')
        return None

    templet[1] = image_convertbpp(templet[1], 'L')
    if appuifw.query(dtext['originalcolors'], 'query') is None:
        templet[0].clear(foreclr)

    im = new_image(iconsize)
    if im is None:
        return None

    im2 = new_image(templet[0].size)
    if im2 is None:
        return None

    im2.blit(templet[0], mask=templet[1])
    im2 = im2.resize(iconsize)
    im.blit(im2)
    im.rectangle((-1, -1, iconsize[0], iconsize[1]), fill=None, outline=0)

    try:
        toolslist.icon((1, 1), im)
    except:
        None
        None
        None
        appuifw.note(u"Can't create icon")
        return None


def templet_draw(canv, x, y):
    if templet is not None:
        canv.blit(templet[0], target=(x, y), mask=templet[1])


def templet_fromfile():
    global templet
    fname = dialog.open(path=ur(con.lastpath_img), ext=[
        'jpg',
        'png',
        'gif',
        'bmp',
        'mbm',
        'jpeg'], kind='open')
    if fname is None:
        return None

    con.lastpath_img = path.split(fname)[0]
    templet = [
        None,
        None]
    templet[0] = graphics.Image.open(fname)
    image = new_image(templet[0].size)
    if image is None:
        return None

    templet[1] = image
    templet[1] = image_convertbpp(templet[1], 'L')
    im = new_image((24, 24))
    if im is None:
        return None

    im2 = new_image(templet[0].size)
    if im2 is None:
        return None

    im2.blit(templet[0], mask=templet[1])
    im2 = im2.resize((24, 24))
    im.blit(im2)
    im.rectangle((0, 0, 24, 24), fill=None, outline=0)

    try:
        toolslist.icon((1, 1), im)
    except:
        None
        None
        None
        return imwin


def colorgen():
    rgb = [
        255,
        255,
        255]
    size = 12
    dd = 48
    hh = dd / 2
    maxc = 576
    midc = 271
    minc = 288
    for t in xrange(1, palette_size[1]):
        if t == 1:
            rgb = [
                255,
                255,
                255]
            d = [
                hh,
                hh,
                hh]
        elif t == 3:
            rgb = [
                maxc,
                minc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 5:
            rgb = [
                maxc,
                maxc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 7:
            rgb = [
                minc,
                maxc,
                minc]
            d = [
                dd,
                dd,
                dd]
        elif t == 9:
            rgb = [
                minc,
                maxc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 11:
            rgb = [
                minc,
                minc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 13:
            rgb = [
                maxc,
                minc,
                maxc]
            d = [
                dd,
                dd,
                dd]
        elif t == 4:
            rgb = [
                maxc,
                midc,
                minc]
            d = [
                dd,
                hh,
                dd]
        elif t == 6:
            rgb = [
                midc,
                maxc,
                minc]
            d = [
                hh,
                dd,
                dd]
        elif t == 8:
            rgb = [
                minc,
                maxc,
                midc]
            d = [
                dd,
                dd,
                hh]
        elif t == 10:
            rgb = [
                minc,
                midc,
                maxc]
            d = [
                dd,
                hh,
                dd]
        elif t == 12:
            rgb = [
                midc,
                minc,
                maxc]
            d = [
                hh,
                dd,
                dd]
        elif t == 2:
            rgb = [
                maxc,
                minc,
                midc]
            d = [
                dd,
                dd,
                hh]

        for n in xrange(palette_size[0]):
            if n < palette_size[0]:
                c = [
                    0,
                    0,
                    0]
                for i in xrange(3):
                    c[i] = rgb[i] - d[i] * n
                    if c[i] > 255:
                        c[i] = 255

                    if c[i] < 0:
                        c[i] = 0

                cc = 256 * 256 * c[0] + 256 * c[1] + c[2]
                col[n][t] = cc
                colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
                colors[n][t].rectangle((1, 0, size, size - 1), outline=cc, fill=cc)
            else:
                c = [
                    255,
                    255,
                    255]
                cc = 256 * 256 * c[0] + 256 * c[1] + c[2]
                col[n][t] = cc
                colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
                colors[n][t].rectangle((1, 0, size, size - 1), outline=cc, fill=cc)


def colorload():
    rgb = [
        255,
        255,
        255]
    size = 12
    d = 64
    maxc = 383
    minc = 128
    for n in xrange(0, palette_size[0]):
        for t in xrange(1, palette_size[1]):
            colors[n][t].rectangle((0, 0, size, size), outline=0, fill=0)
            colors[n][t].rectangle((1, 0, size, size - 1), outline=col[n][t], fill=col[n][t])


def statusbar():
    buff.rectangle((0, workzone[1], con.screen_size[0], con.screen_size[1]), outline=0, fill=con.ui_form_color[0])
    buff.rectangle((15, con.screen_size[1] - 12, 22, con.screen_size[1] - 2), outline=0, fill=foreclr)
    buff.rectangle((23, con.screen_size[1] - 12, 30, con.screen_size[1] - 2), outline=0, fill=backclr)
    if colorgrid.hdn:
        msg = u'%d:%d' % ((imwin.curs.x - imwin.x) + imwin.imx, (imwin.curs.y - imwin.y) + imwin.imy)
        if curtool == tool['lasso']:
            if imwin.selector.isactive():
                (l, u, r, b) = imwin.selector.getcoord()
                msg += u' %dx%d' % ((r - l) + 1, (b - u) + 1)

        elif curtool == tool['selector'] or curtool == tool['elselector']:
            if imwin.selector.isactive():
                msg += u' %dx%d' % (abs(imwin.selector.tool.bcoord[2] - imwin.selector.tool.bcoord[0]) + 1,
                                    abs(imwin.selector.tool.bcoord[3] - imwin.selector.tool.bcoord[1]) + 1)

        elif tool_line.enabled():
            msg += u' %dx%d' % (
            abs(tool_line.bcoord[2] - tool_line.bcoord[0]) + 1, abs(tool_line.bcoord[3] - tool_line.bcoord[1]) + 1)
        elif tool_ellps.enabled():
            msg += u' %dx%d' % (
            abs(tool_ellps.bcoord[2] - tool_ellps.bcoord[0]) + 1, abs(tool_ellps.bcoord[3] - tool_ellps.bcoord[1]) + 1)
        elif tool_rect.enabled():
            msg += u' %dx%d' % (
            abs(tool_rect.bcoord[2] - tool_rect.bcoord[0]) + 1, abs(tool_rect.bcoord[3] - tool_rect.bcoord[1]) + 1)
        elif curtool == tool['picker']:
            msg += unicode(
                imwin.img.getpixel(((imwin.curs.x - imwin.x) + imwin.imx, (imwin.curs.y - imwin.y) + imwin.imy))[0])

        buff.text((33, statustexty), msg, font=con.ui_status_font, fill=con.ui_form_color[1])
    else:
        x = colorgrid.curitem()[0]
        y = colorgrid.curitem()[1]
        if y > 0:
            buff.text((33, statustexty), u'%s' % (inttorgb(col[x][y]),), font=con.ui_status_font,
                      fill=con.ui_form_color[1])

    if icon_tool is not None:
        buff.blit(icon_tool[toolslist.curitem()[0] * toolslist.lst[0].itcnt + toolslist.curitem()[1]],
                  target=(0, con.screen_size[1] - 14))

    if imwin.drawing:
        buff.rectangle((0, con.screen_size[1] - 13, 14, con.screen_size[1]), outline=16711680, fill=None, width=1)


def config():
    appuifw.app.screen = 'normal'
    optform.execute()
    config_updatefromform()
    menu_create()
    appuifw.app.screen = 'full'
    clist = []
    conflist = config_getlist()
    for t in conflist:
        clist.append(int(t))

    config_reset(clist)


def config_updatefromform():
    global dtext, mtext, dtext, mtext
    con.toolbar_slidespeed = int(optform[1][2][1]) + 1
    gradgrid.setslidespeed(gradgrid.getsize()[0] / con.toolbar_slidespeed)
    colorgrid.setslidespeed(colorgrid.getsize()[0] / con.toolbar_slidespeed)
    toolslist.setslidespeed(toolslist.getsize()[0] / con.toolbar_slidespeed)
    imwin.curs.kind = optform[2][2][1]
    con.cursor = optform[2][2][1]
    imwin.curs.size = int(optform[3][2][1]) + 1
    con.cursorsize = int(optform[3][2][1]) + 1
    con.cursormultiplier = optform[4][2]
    con.undo_size = int(optform[5][2][1])
    imwin.setundosize(con.undo_size)
    con.rectselecttype = int(optform[6][2][1])
    con.exitconfirm = int(optform[7][2][1])
    newlang = con.lang_list[optform[0][2][1]]
    if con.lang != newlang:
        con.lang = newlang
        dtext = lang_readfromfile(program_path, con.lang, __version__)
        mtext = {
            'ok': dtext['ok'],
            'cancel': dtext['cancel']}

    for t in xrange(len(con.custompal)):
        if con.custompal[t] != '':
            palette_checkcustom(t, con.custompal[t])

    dialog.createmenu(dtext)
    dialog_tmp.createmenu(dtext)
    dialog_pal.createmenu(dtext)
    dialog_img.createmenu(dtext)


def config_getlist():
    valuelist = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0]
    valuelist[0] = optform[0][2][1]
    valuelist[1] = optform[1][2][1]
    valuelist[2] = optform[2][2][1]
    valuelist[3] = optform[3][2][1]
    valuelist[4] = optform[4][2]
    valuelist[5] = optform[5][2][1]
    valuelist[6] = optform[6][2][1]
    valuelist[7] = optform[7][2][1]
    return valuelist


def config_reset(valuelist=None):
    global optcont, optform, optcont, optform
    if valuelist is None:
        valuelist = [
            con.lang_list.index(u'english'),
            2,
            0,
            4,
            5,
            1,
            0,
            1]

    optcont = [
        (dtext['language'], 'combo', (con.lang_list, valuelist[0])),
        (dtext['toolslidespeed'], 'combo', ([
                                                dtext['immediately'],
                                                dtext['veryfast'],
                                                dtext['fast'],
                                                dtext['medium'],
                                                dtext['slow'],
                                                dtext['veryslow']], valuelist[1])),
        (dtext['cursortype'], 'combo', ([
                                            dtext['cursor_bw'],
                                            dtext['cursor_blink'],
                                            dtext['cursor_invers']], valuelist[2])),
        (dtext['cursorsize'], 'combo', ([
                                            u'1',
                                            u'2',
                                            u'3',
                                            u'4',
                                            u'5'], valuelist[3])),
        (dtext['changecursor'], 'number', valuelist[4]),
        (dtext['undosize'], 'combo', ([
                                          u'0',
                                          u'1',
                                          u'2',
                                          u'3',
                                          u'4',
                                          u'5'], valuelist[5])),
        (dtext['rectselect'], 'combo', ([
                                            dtext['immobile'],
                                            dtext['mobile']], valuelist[6])),
        (dtext['confirmonexit'], 'combo', ([
                                               dtext['no'],
                                               dtext['yes']], valuelist[7]))]
    optform = appuifw.Form(optcont, flags=appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced)
    return valuelist


def he(state):
    if state is None:
        return 'None'

    return '%06x' % state


def config_load():
    try:
        valuelist = con.load(program_path)
        config_reset(valuelist)
        config_updatefromform()
        config_reset(valuelist)
    except Exception:
        None
        exc = None
        None
        traceback.print_exc(sys.stderr)
        con.lastpath_img = 'C:\\'
        ans = appuifw.query(dtext['confbroken'], 'query')
        if ans is None:
            sys.stderr.close()
            abort()

        config_reset()
        config_updatefromform()
    except:
        None


def define_screen_size():
    try:
        parser = iniparser.TIniParser()
        parser.open(program_path + 'config.ini')
        parser.readgroup('DISPLAY')
        val = parser.readstr('force_display_size', None, ',')
        if val != [
            'None']:

            try:
                size = (int(val[0]), int(val[1]))
                con.screen_size = size
            except:
                None
                None
                None
                con.screen_size = display_pixels()

        else:
            con.screen_size = display_pixels()
        parser.close()
    except:
        None
        None
        None
        con.screen_size = display_pixels()


def focusaction(state):
    if state == 0:
        applock.wait()
    else:
        applock.signal()


def menu_recent():
    if con.recentfiles:
       # continue
        rfiles = [path.split(x)[1] for x in con.recentfiles]
        ind = appuifw.popup_menu(rfiles, dtext['recentfiles'] + ':')
        if ind is None:
            return None
        else:
            _file_open(con.recentfiles[ind], False)
    else:
        showtipex(u'No recents')


def menu_start_hide():
    global redraw
    mainproc_start()
    redraw = redraw_main


def joke():
    appuifw.note(dtext['joke'])


def menu_create():
    global mainmenu, menu_palette, menu_palette2, menu_palette3, menu_preview, popupmenu, menu_start, menu_selection, menu_about, mess_info, mess_tip, mainmenu, menu_palette, menu_palette2, menu_palette3, menu_preview, popupmenu, menu_start, menu_selection, menu_about, mess_info, mess_tip
    (extmenu, extabout) = plugins_load()
    mainmenu = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, ((dtext['file'], (
    (dtext['open'], (lambda: file_open(False))), (dtext['openinnew'], (lambda: file_open(True))),
    (dtext['reopen'], (lambda: file_reopen(False))), (dtext['new'], (lambda: query_file_new(False))),
    (dtext['newinnew'], (lambda: query_file_new(True))), (dtext['save'], (lambda: file_save())),
    (u'%s%s' % (dtext['saveas'], '...'), (lambda: file_saveas(True))),
    (u'%s%s' % (dtext['recentfiles'], '...'), menu_recent), (dtext['close'], file_close))), (dtext['edit'], (
    (dtext['undo'], undo), (dtext['redo'], redo), (dtext['cut'], clipcut), (dtext['copy'], clipcopy),
    (dtext['paste'], clippaste), (dtext['clear'], clipclear), (dtext['blend'], setblend))), (dtext['select'], (
    (u'%s%s' % (dtext['select'], '...'), selectsize), (dtext['selectall'], selectall),
    (dtext['invert'], (lambda: imwin.selector.invert_selection())),
    (dtext['deselect'], (lambda: imwin.selector.deselect())))), (dtext['zoom'], (
    (dtext['zoomin'], zoom_in), (dtext['zoomout'], zoom_out), (dtext['zoom_multiply'], zoom_multiply_query),
    (dtext['zoom_1_1'], zoom_1_1))), (dtext['font'], (
    (dtext['entertext'], settext), (dtext['stdfont'], fontstd_select), (dtext['extfont'], font_open),
    (dtext['stdfontopt'], fontstd_opt), (dtext['extfontopt'], font_opt))), (dtext['tools'], (
    (dtext['templet'], templet_create), (dtext['loadtemplet'], templet_load),
    (dtext['templetfromfile'], templet_fromfile), (dtext['exportpal'], palette_export),
    (dtext['importpal'], palette_import),
    (u'%s%s' % (dtext['batchproc'], '...'), (lambda: batch.open(con.lastpath_img))))), (dtext['image'], (
    (dtext['info'], fileinfo), (dtext['preview'], (lambda: preview_hide(False))), (dtext['resize'], image_resize_query),
    (dtext['resizecanvas'], image_resizecanvas_query), (dtext['cropsel'], image_crop), (dtext['rotate'], image_rotate),
    (dtext['flip'], image_flip), (dtext['displacement'], image_displacement),
    (dtext['replacecolor'], image_replacecolor_query), (dtext['makemask'], image_tomask))), (dtext['filter'], (
    (dtext['blur'], image_blur_query), (dtext['lightness'], image_lightness_query),
    (dtext['darkness'], image_darkness_query), (dtext['blackwhite'], (lambda: image_bpp('1'))),
    (dtext['grayscale'], (lambda: image_bpp('L'))), (dtext['posterize'], image_posterize),
    (dtext['invertcolors'], image_invertcolors), (dtext['colorbalance'], image_colorbalance),
    (dtext['saturation'], image_saturation), (dtext['sepia'], image_sepia), (dtext['gradient'], gradgrid.unlockandshow),
    (dtext['fractal'], ((dtext['julia'], image_fractal), (dtext['mandelbrot'], image_fractal_mandelbrot))))), extmenu, (
                                                            dtext['option'], ((dtext['config'], config), (
                                                            dtext['keyconfig'], (lambda: con.keyconfig.execute())), (
                                                                              u'%s%s' % (dtext['skinselect'], '...'),
                                                                              skin_select),
                                                                              (dtext['colortheme'], theme_open),
                                                                              (dtext['help'], help), (dtext['about'], (
                                                                lambda: about_hide(False))))),
                                                            (dtext['switchwin'], imwindow_next), (dtext['exit'], exit)),
                              con.ui_menu_font)
    mainmenu.keylessitem(0, mainmenu.getitemindex(0, dtext['exit']))
    mainmenu.hiden(True)
    mainmenu.spaces(def_spaces)
    mainmenu.sidespace(18)
    mainmenu.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        mainmenu.forcetextheight(con.ui_menu_font_fheight)

    if s60_version_info == (1, 2) or s60_version_info == (2, 0):
        mainmenu.itemblocked(8, mainmenu.getitemindex(8, dtext['blur']), True)

    if s60_version_info != (3, 0):
        mainmenu.itemblocked(5, mainmenu.getitemindex(5, dtext['stdfontopt']), True)

    def menu_main_hide():
        mainproc_start()
        keyboard.resetkeys()

    mainmenu.onhide = menu_main_hide
    mainmenu.onshow = menu_main_onshow
    wt_ui.Tsysmenu.setcurrent(0, mainmenu)
    menu_palette = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, (
    (dtext['settoforecolor'], _setforecolor), (dtext['settobackcolor'], _setbackcolor),
    (dtext['setfromforecolor'], palette_setcell), (dtext['change'], colormixer), (dtext['exportpal'], palette_export),
    (dtext['importpal'], palette_import), (dtext['reset'], palette_reset), (dtext['cancel'], colorgrid.hideandblock)),
                                  con.ui_menu_font)
    menu_palette.hiden(True)
    menu_palette.spaces(def_spaces)
    menu_palette.sidespace(18)
    menu_palette.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette.forcetextheight(con.ui_menu_font_fheight)

    menu_palette.onhide = mainproc_start
    menu_palette.onshow = mainproc_stop
    menu_palette2 = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff, (
    (dtext['setcustompal'], palette_selectcustom), (dtext['clear'], palette_clearcustom),
    (dtext['cancel'], colorgrid.hideandblock)), con.ui_menu_font)
    menu_palette2.hiden(True)
    menu_palette2.spaces(def_spaces)
    menu_palette2.sidespace(18)
    menu_palette2.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette2.forcetextheight(con.ui_menu_font_fheight)

    menu_palette2.onhide = mainproc_start
    menu_palette2.onshow = mainproc_stop
    menu_palette3 = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff,
                                   ((u'  joke ;)', joke), (dtext['cancel'], colorgrid.hideandblock)), con.ui_menu_font)
    menu_palette3.hiden(True)
    menu_palette3.spaces(def_spaces)
    menu_palette3.sidespace(18)
    menu_palette3.coord('leftbottom')
    if con.ui_menu_font_fheight is not None:
        menu_palette3.forcetextheight(con.ui_menu_font_fheight)

    menu_palette3.onhide = mainproc_start
    menu_palette3.onshow = mainproc_stop
    menu_preview = wt_ui.Tsysmenu(0, 'leftbottom', canv, buff,
                                  ((dtext['rotate'], preview_calc), (dtext['close'], preview_hide)), con.ui_menu_font)
    menu_preview.spaces(def_spaces)
    menu_preview.sidespace(18)
    menu_preview.coord('leftbottom')
    menu_preview.hiden(True)
    if con.ui_menu_font_fheight is not None:
        menu_preview.forcetextheight(con.ui_menu_font_fheight)

    menu_preview.onhide = mainproc_start
    menu_preview.onshow = mainproc_stop
    rmenupares = ((dtext['undo'], undo), (dtext['redo'], redo), (dtext['cut'], clipcut), (dtext['copy'], clipcopy),
                  (dtext['paste'], clippaste), (dtext['clear'], clipclear))
    popupmenu = wt_ui.Tsysmenu(1, 'rightbottom', canv, buff, rmenupares, con.ui_menu_font)
    popupmenu.hiden(True)
    popupmenu.spaces(def_spaces)
    popupmenu.sidespace(18)
    popupmenu.coord('rightbottom')
    if con.ui_menu_font_fheight is not None:
        popupmenu.forcetextheight(con.ui_menu_font_fheight)

    def menu_popup_hide():
        mainproc_start()
        keyboard.resetkeys()

    popupmenu.onhide = menu_popup_hide
    popupmenu.onshow = menu_popup_onshow
    wt_ui.Tsysmenu.setcurrent(1, popupmenu)
    if menu_start_off is False:
        smenupares = (
        (dtext['open'].upper(), (lambda: file_open(False))), (dtext['new'].upper(), (lambda: query_file_new(False))),
        (dtext['exit'].upper(), exit))
        menu_start = wt_ui.Tmultimenu('center', buff, None, smenupares, con.ui_menu_font)
        menu_start.spaces(def_spaces)
        menu_start.sidespace(18)
        menu_start.coord('center')
        menu_start.onhide = menu_start_hide
        menu_start.colors(con.ui_menu_color)

    menu_selection_pares = ((dtext['cut'], clipcut), (dtext['copy'], clipcopy), (dtext['clear'], clipclear), (
    dtext['select'], ((u'%s%s' % (dtext['select'], '...'), selectsize), (dtext['selectall'], selectall),
                      (dtext['invert'], (lambda: imwin.selector.invert_selection())),
                      (dtext['deselect'], (lambda: imwin.selector.deselect())))), (dtext['image'], (
    (dtext['cropsel'], image_crop), (dtext['rotate'], image_rotate), (dtext['flip'], image_flip),
    (dtext['displacement'], image_displacement), (dtext['makemask'], image_tomask))), (dtext['filter'], (
    (dtext['blur'], image_blur_query), (dtext['lightness'], image_lightness_query),
    (dtext['darkness'], image_darkness_query), (dtext['blackwhite'], (lambda: image_bpp('1'))),
    (dtext['grayscale'], (lambda: image_bpp('L'))), (dtext['posterize'], image_posterize),
    (dtext['invertcolors'], image_invertcolors), (dtext['colorbalance'], image_colorbalance),
    (dtext['saturation'], image_saturation), (dtext['sepia'], image_sepia), (dtext['gradient'], gradgrid.unlockandshow),
    (dtext['fractal'], ((dtext['julia'], image_fractal), (dtext['mandelbrot'], image_fractal_mandelbrot))))), extmenu)
    menu_selection = wt_ui.Tmultimenu('center', buff, None, menu_selection_pares, con.ui_menu_font)
    menu_selection.spaces(def_spaces)
    menu_selection.sidespace(18)
    menu_selection.coord('center')
    menu_selection.colors(con.ui_menu_color)
    menu_selection.hiden(True)

    def menu_selection_hide():
        mainproc_start()
        keyboard.resetkeys()

    menu_selection.onhide = menu_selection_hide
    menu_selection.onshow = mainproc_stop
    mainmenu.colors(con.ui_menu_color)
    menu_preview.colors(con.ui_menu_color)
    menu_palette.colors(con.ui_menu_color)
    menu_palette2.colors(con.ui_menu_color)
    menu_palette3.colors(con.ui_menu_color)
    popupmenu.colors(con.ui_menu_color)
    mbox_percent.clrs = [
        con.ui_menu_color[1][2],
        con.ui_menu_color[1][1],
        con.ui_menu_color[1][3]]
    progressbar.color(con.ui_prog_color)
    mess = [
        u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe ' + app_versionstr,
        u'',
        u'\xe5\x85\x8d\xe8\xb4\xb9\xe7\x9a\x84\xe5\x9b\xbe\xe5\x83\x8f\xe7\xbc\x96\xe8\xbe\x91\xe8\xbd\xaf\xe4\xbb\xb6',
        u'\xc2\xa9 2007-2009 Plyaskin Anton',
        u'',
        u'',
        u'\xe4\xbd\x9c\xe8\x80\x85\xef\xbc\x9a',
        u'  Plyaskin Anton aka werton',
        u'\xe7\xbd\x91\xe7\xab\x99\xef\xbc\x9a',
        u'  www.werton.wen.ru',
        u'',
        u'\xe6\x84\x9f\xe8\xb0\xa2\xef\xbc\x9a',
        u'',
        u'  Sveark - \xe6\x8f\x90\xe4\xbe\x9bPNG',
        u'\xe9\x80\x8f\xe6\x98\x8e\xe5\xba\xa6\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  _killed_ - \xe6\x8f\x90\xe4\xbe\x9bMBM',
        u'\xe8\xbe\x9e\xe5\x85\xb8',
        u'',
        u'  MACTEP3230 - \xe6\x8f\x90\xe4\xbe\x9b\xe5\xa1\xab\xe5\x85\x85',
        u'\xe5\x87\xbd\xe6\x95\xb0\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  Deftrue - \xe6\x8f\x90\xe4\xbe\x9b\xe7\xba\xbf\xe6\x80\xa7',
        u'\xe6\xbb\xa4\xe6\xb3\xa2\xe7\xae\x97\xe6\xb3\x95',
        u'',
        u'  Troicat - \xe6\x8f\x90\xe4\xbe\x9bs60 v3',
        u'\xe7\xa8\x8b\xe5\xba\x8f\xe5\x9b\xbe\xe6\xa0\x87',
        u'',
        u'  Trojan_73 - \xe6\x94\xb6\xe9\x9b\x86\xe8\xb0\x83\xe8\x89\xb2\xe6\x9d\xbf',
        u'\xe5\xb9\xb6\xe5\xb8\xae\xe5\x8a\xa9\xe5\x8d\x87\xe7\xba\xa7',
        u'',
        u'',
        u'\xe6\x84\x9f\xe8\xb0\xa2\xe4\xbb\xa5\xe4\xb8\x8b\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98\xef\xbc\x9a',
        u'',
        u'  Slavasyrota',
        u'  7755',
        u'  Trojan_73',
        u'  Armen-82.08',
        u'  EDGE84',
        u'  kuharsanek',
        u'  kusya1612',
        u'  filja2',
        u'',
        u'',
        u'\xe9\x83\xa8\xe5\x88\x86\xe5\x9b\xbe\xe6\xa0\x87\xe6\x9d\xa5\xe8\x87\xaa',
        u'\xe6\x88\x96\xe5\x9f\xba\xe4\xba\x8eGIMP 2.6',
        u'\xc2\xa9 1995-2008 Spencer Kimball',
        u'Peter Mattis & GIMP devteam',
        u'']
    ind = mess.index(
        u'\xe6\x84\x9f\xe8\xb0\xa2\xe4\xbb\xa5\xe4\xb8\x8b\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98\xef\xbc\x9a')
    ind -= 1
    mess[ind:ind] = extabout
    mess_eegg[:] = mess
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'')
    mess_eegg.append(u'\xe6\xb1\x89\xe5\x8c\x96\xef\xbc\x9aSeawave;)')
    menu_about = wt_ui.Tmessageform('center', buff,
                                    (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2]), mess,
                                    con.ui_menu_font)
    menu_about.hiden(True)
    menu_about.setcallback(about_hide)
    menu_about.scrollspd = 1
    mess = [
        u'File name: ']
    mess_info = wt_ui.Tmessageform('center', buff,
                                   (con.ui_menu_color[0][0], con.ui_menu_color[0][1], con.ui_menu_color[1][2]), mess,
                                   con.ui_menu_font)
    mess_info.blspace = 4
    mess_info.message(mess, con.ui_menu_font)
    mess_info.hiden(True)
    mess_info.setcallback(mainproc_start)
    mess_tip = wt_ui.Tmessageform('center', buff,
                                  (con.ui_form_color[0], con.ui_menu_color[0][1], con.ui_menu_color[1][3]), [
                                      u''], con.ui_menu_font)
    mess_tip.boxstyle = 1
    mess_tip.borderwidth = 2
    mess_tip.corner = 2
    mess_tip.blspace = 2
    mess_tip.message([
        u'Wellcome to',
        u'ImageDesigner!'], con.ui_menu_font_bold)
    mess_tip.messtimeout = 1
    mess_tip.hiden(True)
    check_imwincount()


def rightmenu():
    if mainmenu.hiden() is False:
        mainmenu.hiden(True)


def fileinfo():
    if imwin.filename is not None:
        mess = [
            u'%s: %s' % (dtext['name'], path.split(imwin.filename)[1]),
            u'%s: %d %s ' % (dtext['size'], stat(ur(imwin.filename))[6] / 1024, dtext['kb']),
            u'%s: %d x %d' % (dtext['resolution'], imwin.img.size[0], imwin.img.size[1])]
    else:
        mess = [
            u'%s:' % dtext['name'],
            u'%s:' % dtext['size'],
            u'%s: %d x %d' % (dtext['resolution'], imwin.img.size[0], imwin.img.size[1])]
    mess_info.blspace = 4
    mess_info.message(mess, con.ui_menu_font)
    mess_info.setcallback(mainproc_start)
    mess_info.hiden(False)
    mainproc_stop()


def menu_main_onshow():
    wt_ui.Ticongrid.hideall()
    mainproc_stop()
    if len(imagewindow) == 1:
        mainmenu.itemblocked(0, mainmenu.getitemindex(0, dtext['switchwin']), True)
    else:
        mainmenu.itemblocked(0, mainmenu.getitemindex(0, dtext['switchwin']), False)
    if not (con.recentfiles):
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['recentfiles'] + '...'), True)
    else:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['recentfiles'] + '...'), False)
    if imwin.zoom == 1:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomout']), True)
    else:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomout']), False)
    if imwin.zoom == 50:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomin']), True)
    else:
        mainmenu.itemblocked(4, mainmenu.getitemindex(4, dtext['zoomin']), False)
    if not imwin.selector.isactive():
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['deselect']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['copy']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['cut']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['clear']), True)
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), True)
    else:
        mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['deselect']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['copy']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['cut']), False)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['clear']), False)
        if curtool == tool['magicrod']:
            mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), False)
        else:
            mainmenu.itemblocked(3, mainmenu.getitemindex(3, dtext['invert']), True)
    if classes.TUniSlector.copybuff is None:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['paste']), True)
    else:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['paste']), False)
    if imwin.filename is None:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['reopen']), True)
    else:
        mainmenu.itemblocked(1, mainmenu.getitemindex(1, dtext['reopen']), False)
    if imwin.undosize != 0:
        if imwin.redostack[-1] is None:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), True)
        else:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), False)
        if imwin.undostack[-1] is None:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), True)
        else:
            mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), False)
    else:
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['redo']), True)
        mainmenu.itemblocked(2, mainmenu.getitemindex(2, dtext['undo']), True)


def menu_popup_onshow():
    mainproc_stop()
    if not imwin.selector.isactive():
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['copy']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['cut']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['clear']), True)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['copy']), False)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['cut']), False)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['clear']), False)
    if classes.TUniSlector.copybuff is None:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['paste']), True)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['paste']), False)
    if imwin.undosize != 0:
        if imwin.redostack[-1] is None:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), True)
        else:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), False)
        if imwin.undostack[-1] is None:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), True)
        else:
            popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), False)
    else:
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['redo']), True)
        popupmenu.itemblocked(0, popupmenu.getitemindex(0, dtext['undo']), True)


def menu_palette_onshow():
    mainproc_stop()


def mainproc_start():
    onnextcicle_do(_mainproc_start)


def mainproc_stop():
    onnextcicle_do(_mainproc_stop)


def _mainproc_start():
    global main_event_proc
    main_event_proc = True
    if wt_ui.Ticongrid.isallhiden():
        imwin.blckd = False
        con.keyconfig.hotkeys_on()


def _mainproc_stop():
    global main_event_proc
    main_event_proc = False
    imwin.blckd = True
    con.keyconfig.hotkeys_clear()


def nextcicle_waiter():
    global ciclefunctions
    if ciclefunctions:
        for t in ciclefunctions:
            t()

        ciclefunctions = []


def onnextcicle_do(funct):
    ciclefunctions.append(funct)


def about_hide(state=True):
    global redraw
    menu_about.hiden(state)
    if menu_about.hiden():
        redraw = redraw_main
        mainproc_start()
    else:
        redraw = redraw_about
        mainproc_stop()


def ru(s):
    return s.decode('utf-8')


def ur(s):
    return s.encode('utf-8')


def skin_load(folder):
    imopen = graphics.Image.open
    icon = [
        imopen(folder + 'Pencil_32.png'),
        imopen(folder + 'Brush_32.png'),
        imopen(folder + 'Erase_32.png'),
        imopen(folder + 'Line2_32.png'),
        imopen(folder + 'Rect_32.png'),
        imopen(folder + 'Ellipse_32.png'),
        imopen(folder + 'Select_32.png'),
        imopen(folder + 'El_Select.png'),
        imopen(folder + 'Cstamp_32.png')]
    pbar.percent(30)
    pbar.draw()
    icon2 = [
        imopen(folder + 'Picker_32.png'),
        imopen(folder + 'Notemlet_32.png'),
        imopen(folder + 'Text_32.png'),
        imopen(folder + 'Polygon_32.png'),
        imopen(folder + 'Broken_32.png'),
        imopen(folder + 'PaintBucket_32.png'),
        imopen(folder + 'Spray_32.png'),
        imopen(folder + 'Lasso.png'),
        imopen(folder + 'mrod.png')]
    icon3 = [
        imopen(folder + 'Grad_vert.png'),
        imopen(folder + 'Grad_cir.png')]
    icon4 = [
        imopen(folder + 'Grad_gor.png'),
        imopen(folder + 'Grad_rect.png')]
    icon5 = []
    icon5.append(imopen(folder + 'f.png'))
    icon5.append(imopen(folder + 'c.png'))
    icon5.append(imopen(folder + 'b.png'))
    icon5.append(imopen(folder + 'black-white.png'))
    icon5.append(imopen(folder + 'color_black.png'))
    icon5.append(imopen(folder + 't.png'))
    icon6 = imopen(folder + 'color_white.png')
    pbar.percent(60)
    pbar.draw()
    icon7 = [
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None],
        [
            None,
            None]]
    icon7[0][0] = imopen(folder + 'drive.png')
    icon7[0][1] = new_image(icon7[0][0].size, '1')
    icon7[0][1].load(folder + 'drive_mask.png')
    icon7[1][0] = imopen(folder + 'dir.png')
    icon7[1][1] = new_image(icon7[1][0].size, '1')
    icon7[1][1].load(folder + 'dir_mask.png')
    icon7[2][0] = imopen(folder + 'im_green.png')
    icon7[3][0] = imopen(folder + 'im_blue.png')
    icon7[4][0] = imopen(folder + 'im_red.png')
    icon7[5][0] = imopen(folder + 'im_yellow.png')
    icon7[6][0] = imopen(folder + 'im_gray.png')
    icon7[7][0] = icon7[2][0]
    icon7[2][1] = new_image(icon7[2][0].size, '1')
    icon7[3][1] = new_image(icon7[2][0].size, '1')
    icon7[4][1] = new_image(icon7[2][0].size, '1')
    icon7[5][1] = new_image(icon7[2][0].size, '1')
    icon7[6][1] = new_image(icon7[2][0].size, '1')
    icon7[7][1] = new_image(icon7[2][0].size, '1')
    icon8 = [
        None,
        None,
        None,
        None,
        None,
        None]
    for t in (1, 2, 3, 4, 5, 6):
        icon8[t - 1] = imopen(folder + str(t) + '.png')

    return (icon, icon2, icon3, icon4, icon5, icon6, icon7, icon8)


def skin_define(program_path):
    parser = iniparser.TIniParser()

    try:
        parser.open(program_path + 'config.ini')
        parser.readgroup('MISC')
        con.skin = parser.readstr('skin', 'default')
    except:
        None
        None
        None
        con.skin = 'default'

    return con.skin


app_versionstr = u'v.%s' % _version_
con = conf.Cconf()
(con.lang_list, con.lang, dtext) = lang_load(program_path, __version__)
mtext = {
    'ok': dtext['ok'],
    'cancel': dtext['cancel']}
define_screen_size()
if s60_version_info == (1, 2) or s60_version_info == (2, 0):
    appuifw.note(u'S60 1st and 2nd edition fp1 are no supported.', 'error')
    abort()

if s60_version_info == (3, 0):
    con.ui_menu_font = (u'Nokia Hindi S60', None, graphics.FONT_NO_ANTIALIAS)
    con.ui_menu_font_bold = ('dense', None, graphics.FONT_BOLD)
    con.ui_status_font = (u'Nokia Hindi S60', 13)
else:
    con.ui_menu_font = (u'Sans MT 936_s60', None)
    con.ui_menu_font_bold = (u'LatinBold12', None)
    con.ui_status_font = (u'Sans MT 936_s60', None)
lastpath_temp = program_path + 'templet\\'
lastpath_fnt = program_path + 'Fonts\\'
lastpath_pal = program_path + 'Palette\\'
noicon = False
iconsize = (28, 28)
con.undo_size = 1
con.cursormultiplier = 8
con.cursor = 0
con.cursorsize = 3
con.custompal = [
    '',
    '',
    '',
    '',
    '',
    '']
con.lastpath_img = 'c:\\'
scrollbarwidth = 4
workzone = [
    con.screen_size[0] - scrollbarwidth,
    con.screen_size[1] - 17]
updatezone = (0, 0, workzone[0], workzone[1])
fontflags = [
    0,
    0,
    0]
stdfontsize = 14
fntsymbolsdelay = 1
statustexty = con.screen_size[1] - 2
menu_start_off = True
foreclr = 0
backclr = 16777215
kevent = None
preview_exit = True
prev_vert = False
prev_image = None
prev_coord = None
icon_tool = None
con.rectselecttype = 0
templet = None
gtext = None
filename = ''
palette_size = [
    12,
    14]
#continue
symbols = [[
    0,
    0,
    0,
    0] for x in xrange(256)]
con.recentfiles = []
batch_filelist = []
redrawcount = 1
bmpfont = None
fontbuffmsk = None
fontbuff = None
fontname = None
fontscalex = 1.0
fontscaley = 1.0
fontblurint = 0
fontblnd = 0
blendval = 16777215
codemap = None
graymask = None
menu_main = None
mainmenu = None
popupmenu = None
menu_colorch = None
menu_preview = None
menu_about = None
menu_start = None
menu_selection = None
menu_palette = None
menu_palette1 = None
menu_palette2 = None
menu_palette3 = None
mess_info = None
mess_tip = None
mess_eegg = []
main_event_proc = True
_fill_queue = []
_fill_width = 0
_fill_height = 0
ciclefunctions = []
con.ui_req_color = [
    11315624,
    10262936,
    [
        None,
        6052184,
        0,
        16777215,
        0],
    [
        0,
        2113648,
        16777215]]
con.ui_form_color = [
    9210248,
    0,
    11315624,
    [
        0,
        2113648,
        16777215]]
con.ui_menu_font_fheight = None
def_spaces = (4, 4, 3, 3, 2)
def_colors = [
    [
        0,
        11315624,
        2171169],
    [
        None,
        6052184,
        0,
        16777215,
        8355711]]
con.ui_menu_color = def_colors
con.ui_prog_color = [
    0,
    40960,
    16777215]
con.ui_grid_color = 16711680
con.curs_del = [
    5,
    20,
    40,
    60,
    80,
    100,
    120,
    150,
    150]
con.curs_step = [
    0,
    1,
    2,
    3,
    4,
    6,
    8,
    10,
    12]
con.toolbar_slidespeed = 2
keyboard = Keyboard()
buff = new_image((con.screen_size[0], con.screen_size[1]))
applock = Ao_lock()
appuifw.app.screen = 'full'
appuifw.app.title = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe'
event = event_main
appuifw.app.body = appuifw.Canvas(redraw_callback=redraw, event_callback=event_main)
canv = appuifw.Canvas(redraw_callback=redraw, event_callback=event_main)
canv.blit(lloader.logo,
          target=((con.screen_size[0] - lloader.logo.size[0]) / 2, (con.screen_size[1] - lloader.logo.size[1]) / 2))
del lloader.logo
del lloader.canv
appuifw.app.exit_key_handler = rightmenu
progressbar = wt_ui.Tbar(con.screen_size[0] / 2 - con.screen_size[0] / 4 - 25, con.screen_size[1] / 2 - 11,
                         con.screen_size[0] * 3 / 4 + 25, con.screen_size[1] / 2 + 10, (0, 100), 10, canv, False, 3)
progressbar.color(con.ui_prog_color)
progressbar.linewidth(2)
progressbar.space = 1
progressbar.corner = 2
progressbar.scrollwidth(0)
pbar = wt_ui.Tbar(con.screen_size[0] * 1 / 20, con.screen_size[1] - 14, con.screen_size[0] * 19 / 20,
                  con.screen_size[1] - 3, (0, 100), 10, canv, False, 3)
pbar.color((0, 255, 16777215))
pbar.linewidth(2)
pbar.space = 1
pbar.corner = 2
pbar.scrollwidth(0)
pbar.percent(0)
pbar.draw()
mbox_percent = wt_ui.Tmessagebox([
    15,
    con.screen_size[1] / 2 - 37,
    con.screen_size[0] - 30,
    52], canv, con.ui_menu_color[0], con.ui_menu_font_bold)
mbox_percent.style = 'up'
mbox_percent.boxstyle = 1
curwin = 0
imagewindow = []
imwin = None
file_new(con.screen_size[0], con.screen_size[1], 1)
tool_line = TGraphtool(buff, imwin.img, 0)
tool_rect = TGraphtool(buff, imwin.img, 1)
tool_ellps = TGraphtool(buff, imwin.img, 2)
mess = u'\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x98\xe5\x9b\xbe ' + app_versionstr
canv.text((13, con.screen_size[1] - 20), mess, fill=0, font=None)
pbar.percent(10)
pbar.draw()
tool = {}
tool['pencil'] = 0
tool['paintbrush'] = 1
tool['eraser'] = 2
tool['line'] = 3
tool['rectangle'] = 4
tool['ellipse'] = 5
tool['selector'] = 6
tool['elselector'] = 7
tool['stamp'] = 8
tool['picker'] = 9
tool['templet'] = 10
tool['text'] = 11
tool['polygon'] = 12
tool['brokenline'] = 13
tool['paintbucket'] = 14
tool['spray'] = 15
tool['lasso'] = 16
tool['magicrod'] = 17
tool['polygon_'] = 99
skin_define(program_path)
if not skin_check(program_path + 'skin\\' + con.skin + '\\'):
    abort()

(icon, icon2, icn1, icn2, icon5, image_w, icon7, image_n) = skin_load(program_path + 'skin\\' + con.skin + '\\')
pbar.percent(90)
pbar.draw()
del pbar
if noicon is False:
    icon_tool = []
    for t in xrange(len(icon)):
        icon_tool.append(icon[t].resize((14, 14)))

    for t in xrange(len(icon2)):
        icon_tool.append(icon2[t].resize((14, 14)))

if con.screen_size[1] < 320:
    iconsize = (24, 24)
    for t in xrange(len(icon)):
        icon[t] = icon[t].resize(iconsize)

    for t in xrange(len(icon2)):
        icon2[t] = icon2[t].resize(iconsize)


def panel_onshow():
    imwin.blocked(True)
    con.keyconfig.hotkeys_off()


def panel_onhide():
    imwin.blocked(False)
    con.keyconfig.hotkeys_on()
    keyboard.resetkeys()


toolslist = wt_ui.Ticongrid(0, 0, [
    icon,
    icon2])
toolslist.setcourse(0, 0, -toolslist.getsize()[0], 0, toolslist.getsize()[0] / con.toolbar_slidespeed,
                    key_codes.EKeyStar)
toolslist.callback(panel_onshow, panel_onhide, tools_set)
toolslist.rectcolor(con.ui_grid_color)
del icon
del icon2
tools_set()
gradgrid = wt_ui.Ticongrid(-64, 0, [
    icn1,
    icn2])
gradgrid.setcourse(0, 0, -gradgrid.getsize()[0], 0, gradgrid.getsize()[0] / con.toolbar_slidespeed, None)
gradgrid.callback(panel_onshow, panel_onhide)
gradgrid.rectcolor(con.ui_grid_color)
col = [
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None],
    [
        None]]
colors = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []]
#continue
[colors[x].append(icon5[x]) for x in xrange(len(icon5))]
#continue
[colors[x].append(image_w) for x in xrange(6, 12)]
dialog = wt_requester.requester(dtext, multisel=True)
dialog_tmp = wt_requester.requester(dtext)
dialog_pal = wt_requester.requester(dtext)
dialog_img = wt_requester.requester(dtext)
dialog_misc = wt_requester.requester(dtext)
dialog.seticons(icon7)
dialog_tmp.seticons(icon7)
dialog_pal.seticons(icon7)
dialog_img.seticons(icon7)
dialog_misc.seticons(icon7)
del icon7
palette_createcell()
if palette_load():
    colorload()
else:
    colorgen()
colorgrid = wt_ui.Ticongrid(126, 0, [
    colors[0],
    colors[1],
    colors[2],
    colors[3],
    colors[4],
    colors[5],
    colors[6],
    colors[7],
    colors[8],
    colors[9],
    colors[10],
    colors[11]])
colorgrid.setcourse(con.screen_size[0] - colorgrid.getsize()[0], 0, con.screen_size[0], 0,
                    colorgrid.getsize()[0] / con.toolbar_slidespeed, key_codes.EKeyHash)
colorgrid.curitem((3, 0))
colorgrid.rectcolor(con.ui_grid_color)
colorgrid.rectoffset((1, -1))
sz = colorgrid.rectsize()
colorgrid.rectsize((sz[0], sz[1] + 1))
colorgrid.callback(grid_palette_onshow, grid_palette_onhide)
colorgrid.setcallback_onchangeitem(grid_palette_onchangeitem, grid_palette_onchangeitem)
for x in (6, 7, 8, 9, 10, 11):
    colorgrid.setexcludeitem([
        x,
        0])

functlist = [
    [
        dtext['tools'],
        toolslist.switch,
        key_codes.EKeyStar,
        None],
    [
        dtext['colorspanel'],
        colorgrid.switch,
        key_codes.EKeyHash,
        None],
    [
        dtext['brushsize'],
        brush_size,
        key_codes.EKey0,
        None],
    [
        dtext['open'],
        (lambda: file_open(False)),
        None,
        None],
    [
        dtext['openinnew'],
        (lambda: file_open(True)),
        None,
        None],
    [
        dtext['reopen'],
        (lambda: file_reopen(False)),
        None,
        None],
    [
        dtext['new'],
        (lambda: query_file_new(False)),
        None,
        None],
    [
        dtext['newinnew'],
        (lambda: query_file_new(True)),
        None,
        None],
    [
        dtext['save'],
        (lambda: file_save()),
        None,
        None],
    [
        dtext['saveas'],
        (lambda: file_saveas(True)),
        None,
        None],
    [
        dtext['recentfiles'],
        menu_recent,
        None,
        None],
    [
        dtext['close'],
        file_close,
        None,
        None],
    [
        dtext['undo'],
        undo,
        None,
        None],
    [
        dtext['redo'],
        redo,
        None,
        None],
    [
        dtext['cut'],
        clipcut,
        None,
        None],
    [
        dtext['copy'],
        clipcopy,
        None,
        None],
    [
        dtext['paste'],
        clippaste,
        None,
        None],
    [
        dtext['clear'],
        clipclear,
        None,
        None],
    [
        dtext['blend'],
        setblend,
        None,
        None],
    [
        dtext['select'],
        selectsize,
        None,
        None],
    [
        dtext['selectall'],
        selectall,
        None,
        None],
    [
        dtext['invert'],
        (lambda: imwin.selector.invert_selection()),
        None,
        None],
    [
        dtext['deselect'],
        (lambda: imwin.selector.deselect()),
        None,
        None],
    [
        dtext['zoomin'],
        zoom_in,
        None,
        None],
    [
        dtext['zoomout'],
        zoom_out,
        None,
        None],
    [
        dtext['zoom_multiply'],
        zoom_multiply_query,
        None,
        None],
    [
        dtext['zoom_1_1'],
        zoom_1_1,
        None,
        None],
    [
        dtext['entertext'],
        settext,
        None,
        None],
    [
        dtext['stdfont'],
        fontstd_select,
        None,
        None],
    [
        dtext['extfont'],
        font_open,
        None,
        None],
    [
        dtext['stdfontopt'],
        fontstd_opt,
        None,
        None],
    [
        dtext['extfontopt'],
        font_opt,
        None,
        None],
    [
        dtext['templet'],
        templet_create,
        None,
        None],
    [
        dtext['loadtemplet'],
        templet_load,
        None,
        None],
    [
        dtext['templetfromfile'],
        templet_fromfile,
        None,
        None],
    [
        dtext['exportpal'],
        palette_export,
        None,
        None],
    [
        dtext['importpal'],
        palette_import,
        None,
        None],
    [
        dtext['batchproc'],
        (lambda: batch.open(con.lastpath_img)),
        None,
        None],
    [
        dtext['info'],
        fileinfo,
        None,
        None],
    [
        dtext['preview'],
        (lambda: preview_hide(False)),
        None,
        None],
    [
        dtext['resize'],
        image_resize_query,
        None,
        None],
    [
        dtext['resizecanvas'],
        image_resizecanvas_query,
        None,
        None],
    [
        dtext['cropsel'],
        image_crop,
        None,
        None],
    [
        dtext['rotate'],
        image_rotate,
        None,
        None],
    [
        dtext['flip'],
        image_flip,
        None,
        None],
    [
        dtext['displacement'],
        image_displacement,
        None,
        None],
    [
        dtext['replacecolor'],
        image_replacecolor_query,
        None,
        None],
    [
        dtext['makemask'],
        image_tomask,
        None,
        None],
    [
        dtext['blur'],
        image_blur_query,
        None,
        None],
    [
        dtext['lightness'],
        image_lightness_query,
        None,
        None],
    [
        dtext['darkness'],
        image_darkness_query,
        None,
        None],
    [
        dtext['blackwhite'],
        (lambda: image_bpp('1')),
        None,
        None],
    [
        dtext['grayscale'],
        (lambda: image_bpp('L')),
        None,
        None],
    [
        dtext['posterize'],
        image_posterize,
        None,
        None],
    [
        dtext['invertcolors'],
        image_invertcolors,
        None,
        None],
    [
        dtext['colorbalance'],
        image_colorbalance,
        None,
        None],
    [
        dtext['saturation'],
        image_saturation,
        None,
        None],
    [
        dtext['sepia'],
        image_sepia,
        None,
        None],
    [
        dtext['gradient'],
        gradgrid.unlockandshow,
        None,
        None],
    [
        dtext['config'],
        config,
        None,
        None],
    [
        dtext['keyconfig'],
        (lambda: con.keyconfig.execute()),
        None,
        None],
    [
        dtext['skinselect'],
        skin_select,
        None,
        None],
    [
        dtext['colortheme'],
        theme_open,
        None,
        None],
    [
        dtext['help'],
        help,
        None,
        None],
    [
        dtext['switchwin'],
        imwindow_next,
        key_codes.EKey1,
        None],
    [
        dtext['swapcolors'],
        swap_colors,
        None,
        None],
    [
        dtext['navigation'],
        (lambda: imwin.navigation_switch()),
        key_codes.EKey7,
        None],
    [
        dtext['exit'],
        exit,
        0,
        0]]
con.keyconfig = kconfig.CKeyConfig(appuifw.app, canv, functlist, dtext)
con.keyconfig.hotkeys_set()
toolslist.keycode = key_codes.EScancodeStar
colorgrid.keycode = key_codes.EScancodeHash
con.keyconfig.onmod_callback = showtipex
con.keyconfig.offmod_callback = hidetip
running = 1
config_load()
batch = batch.Cbatch_processor(dtext, dialog)
menu_create()
ui_colors_update()
gradgrid.hideandblock()
colorgrid.hideandblock()
toolslist.hideandblock()
if con.firststart:
    mess_tip.hiden(False)

if menu_start_off is False:
    redraw = redraw_start
    mainproc_stop()
else:
    redraw = redraw_main
while running == 1:
    imwin.navigationcontrol()
    scrollbar_update()
    redraw()
    con.keyconfig.timeout_tick()
    nextcicle_waiter()
    keyboard._downs = {}
    ao_sleep(0.001)
    continue
    []