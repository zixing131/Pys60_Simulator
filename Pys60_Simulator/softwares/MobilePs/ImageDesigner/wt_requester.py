# -*- coding: utf-8 -*-

import graphics
import appuifw
import key_codes
import os
from e32 import Ao_timer as Ao_timer
from e32 import drive_list as drive_list
from e32 import s60_version_info as s60_version_info
from e32 import ao_sleep as ao_sleep
from sysinfo import display_pixels as display_pixels
from time import clock as clock
import sys
import traceback
__version__ = 1.4
def ru(s):
    return s.decode('utf-8')




def ur(s):
    return s.encode('utf-8')




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






class Tbar :


    __module__ = __name__
    def __init__(self, x, y, x1, y1,ee, scrv, canv, vert = True, kind = 0):
        minv, maxv =ee
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




    def draw(self):
        self.canv.rectangle((self.x, self.y, self.x1, self.y1), outline = self.clr[0], fill = self.clr[2], width = self.linew)
        if self.kind == 0 : 
            if self.vert is True : 
                self.canv.rectangle((self.x + self.linew, self.y + self.linew + self.dcor, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = None, fill = self.clr[1])
            else : 
                self.canv.rectangle((self.x + self.linew + self.dcor, self.y + self.linew, self.x + self.linew + self.dcor + self.scrollw, (self.y1 - self.linew)), outline = None, fill = self.clr[1])
            pass
        elif self.kind == 1 : 
            if self.vert is True : 
                self.canv.line(((self.x1 - self.linew), self.y + self.linew + self.dcor, (self.x1 - self.linew), self.y + self.linew + self.dcor + self.scrollw), outline = self.clr[1])
            else : 
                self.canv.line((self.x + self.linew + self.dcor + self.scrollw, self.y + self.linew, self.x + self.linew + self.dcor + self.scrollw, (self.y1 - self.linew)), outline = self.clr[1])
            pass




    def percent(self, perc = None):
        if perc is not None : 
            self.perc = perc
            if perc < 0.0 : 
                self.perc = 0.0
            if perc > 100.0 : 
                self.perc = 100.0
            self.dcor = ((self.perc * (self.barw - self.scrollw)) / 100.0)
            if self.dcor > (self.barw - self.scrollw) : 
                self.dcor = (self.barw - self.scrollw)
            pass
        else : 
            return self.perc




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






class Ttextlist :


    __module__ = __name__
    def __init__(self, coord, canv, itempares, font = None, multisel = False):
        self.canv = canv
        self.x = coord[0]
        self.y = coord[1]
        self.w = 0
        self.h = 0
        self.texth = 0
        self.lineh = 0
        self.items = [x[0] for x in itempares]
        self.itemfnt = [font for x in itempares]
        self.itemic = [[None, None] for x in itempares]
        self.callbacks = [x[1] for x in itempares]
        self.multisel = multisel
        self.itemmark = [False for x in itempares]
        self.itcount = len(itempares)
        self.cycled = True
        self.sp_l = 2
        self.sp_r = 2
        self.sp_u = 2
        self.sp_d = 2
        self.sp_bl = 2
        self.sp_sb_lr = 1
        self.sp_sb_ud = 1
        self.curit = 0
        self.sbx = self.x
        self.sby = self.y
        self.firstit = None
        self.scroll = None
        Ttextlist.iteminlist(self, len(self.items))
        self._getmaxtextwidth()
        self._gettextheight()
        self._updatewidth()
        self._updateheight()
        self.font(font)
        self.clrs = [None, 3238597, 0, 16777215, 112]
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
        self.key['mark'] = key_codes.EScancode0




    def gettextheight(self, font):
        s = self.canv.measure_text(u'WTFPLljyp!,\xc0\xd4\xc4\xd9\xc9\xf0\xf3,', font = font)
        return (s[0][3] - s[0][1])




    def _getmaxtextwidth(self):
        w = 0
        for t in xrange(self.itcount):
            s = self.canv.measure_text(self.items[t], font = self.itemfnt[t])
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




    def _updateheight(self, flag = False):
        if flag is False : 
            self.h = (self._gettextheight() * self.itinlist) + (self.sp_bl * (self.itinlist - 1)) + self.sp_d + self.sp_u
        else : 
            self.h = (self.texth * self.itinlist) + (self.sp_bl * (self.itinlist - 1)) + self.sp_d + self.sp_u
        return self.h




    def iteminlist(self, val = None):
        if val is not None : 
            self.itinlist = val
            if self.itinlist > len(self.items) : 
                self.itinlist = len(self.items)
            self.firstit = 0
        elif val == 'full' or val == 'fill' : 
            self.itinlist = (self.h / self.itemhg[0])
        if val is not None : 
            x = self.coord()[0] + self.w
            if x > (self.canv.size[0] - 4) : 
                x = (self.canv.size[0] - 4)
            y = self.coord()[1]
            if self.itcount > self.itinlist : 
                count = (self.itcount - self.itinlist)
                self.scroll = Tbar(x, y, (x + 4), y + (self.itinlist * self.texth), (0, count), self.itinlist, self.canv, True)
                self.scroll.scrollw = ((self.scroll.barw * self.itinlist) / self.itcount)
            pass
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
            self.icsize = img.size
            if (img.size[0] + 2) > self.sp_l : 
                self.sp_l = (img.size[0] + 2)
            if img.size[1] > self.lineh : 
                self.forcetextheight(((img.size[1] - self.sp_bl) + 1))
            pass
        return self.itemic[t]




    def draw(self):
        self._control()
        self.sbx = (self.x + 1)
        self.sby = self.y + self.sp_u + ((self.curit - self.firstit) * self.texth) + ((self.curit - self.firstit) * self.sp_bl)
        self.canv.rectangle(((self.sbx - 2), (self.sby - self.sp_sb_ud), (self.sbx + self.w - 2), self.sby + self.texth + self.sp_sb_ud), outline = self.clrs[0], fill = self.clrs[1], width = 1)
        for n in xrange(self.firstit, self.firstit + self.itinlist):
            t = (n - self.firstit)
            if self.itemmark[n] is True : 
                self.sbx = (self.x + 1)
                self.sby = self.y + self.sp_u + ((n - self.firstit) * self.texth) + ((n - self.firstit) * self.sp_bl)
                self.canv.rectangle(((self.sbx - 2), (self.sby - self.sp_sb_ud), (self.canv.size[0] - 2), self.sby + self.texth + self.sp_sb_ud), outline = self.clrs[0], fill = self.clrs[4], width = 1)
            if self.itemic[n][0] is not None : 
                self.canv.blit(self.itemic[n][0], target = (self.x, (self.y + self.sp_u + ((self.sp_bl + self.texth) * t) + (self.texth / 2) - (self.icsize[1] / 2))), mask = self.itemic[n][1])
            if n == self.curit : 
                self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 2)), self.items[n], fill = self.clrs[3], font = self.itemfnt[n])
            else : 
                self.canv.text((self.x + self.sp_l, (self.y + self.sp_u + (self.sp_bl * t) + (self.texth * (t + 1)) - 2)), self.items[n], fill = self.clrs[2], font = self.itemfnt[n])
        if self.scroll is not None : 
            self.scroll.draw()




    def nextitem(self):
        self.curit += 1
        if self.curit > (self.firstit + self.itinlist - 1) : 
            self.firstit += 1
        if self.curit > (self.itcount - 1) : 
            if self.cycled is True : 
                self.curit = 0
                self.firstit = 0
            else : 
                self.curit = (self.itcount - 1)
                self.firstit = (self.itcount - self.itinlist)
            pass




    def previtem(self):
        self.curit -= 1
        if self.curit < self.firstit : 
            self.firstit -= 1
        if self.curit < 0 : 
            if self.cycled is True : 
                self.curit = (self.itcount - 1)
                self.firstit = (self.itcount - self.itinlist)
            else : 
                self.curit = 0
                self.firstit = 0
            pass




    def gotoitem(self, it, fst = None):
        it = self._correctitem(it)
        self.curit = it
        if fst is None : 
            self.firstit = (self.curit - (self.itinlist / 2))
        else : 
            self.firstit = fst
        if self.firstit > (self.itcount - self.itinlist) : 
            self.firstit = (self.itcount - self.itinlist)
        elif self.firstit < 0 : 
            self.firstit = 0




    def _correctitem(self, it):
        if it > (self.itcount - 1) : 
            it = (self.itcount - 1)
        elif it < 0 : 
            it = 0
        return it




    def _control(self):
        if self.startdown != None : 
            if (clock() - self.startdown) > 0.26 : 
                if (clock() - self.startscroll) > 0.1 : 
                    self.startscroll = clock()
                    self.nextitem()
                pass
            pass
        elif self.startup != None : 
            if (clock() - self.startup) > 0.26 : 
                if (clock() - self.startscroll) > 0.1 : 
                    self.startscroll = clock()
                    self.previtem()
                pass
            pass




    def control(self, evt):
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
            elif evt['scancode'] == self.key['mark'] : 
                if self.multisel is True : 
                    self.itemmark[self.curit] =  not (self.itemmark[self.curit])
                    self.nextitem()
                pass
            pass
        if evt['type'] == appuifw.EEventKeyDown : 
            if evt['scancode'] == self.key['select'] or evt['scancode'] == self.key['select2'] : 
                self.call = True
            pass
        if evt['type'] == appuifw.EEventKeyUp : 
            if evt['scancode'] == key_codes.EScancodeSelect or evt['scancode'] == key_codes.EScancodeLeftSoftkey : 
                if self.call is True : 
                    self.call = False
                    if callable(self.callbacks[self.curit]) : 
                        self.callbacks[self.curit]()
                        return True
                    pass
                pass
            pass
        if self.scroll is not None : 
            self.scroll.value(self.firstit)




    def coord(self, crd = None):
        if crd is not None : 
            if crd[0] is not None : 
                self.x = crd[0]
            if crd[1] is not None : 
                self.y = crd[1]
            pass
        else : 
            return (self.x, self.y)




    def curitem(self, cur = None):
        if cur is not None : 
            self.curit = cur
        return self.curit




    def curitemname(self, name = None):
        if name is not None : 
            self.items[self.curit] = name
        return self.items[self.curit]




    def getmarked(self):
        result = []
        for t in xrange(self.itcount):
            if self.itemmark[t] is True : 
                result.append(self.items[t])
        if len(result) == 0 : 
            return None
        return result




    def markall(self):
        for t in xrange(1, self.itcount):
            self.itemmark[t] = True




    def unmark(self):
        for t in xrange(self.itcount):
            self.itemmark[t] = False




    def invertmark(self):
        for t in xrange(1, self.itcount):
            self.itemmark[t] =  not (self.itemmark[t])




    def markfromcurrent(self):
        for t in xrange(self.curit, self.itcount):
            self.itemmark[t] = True




    def markbeforecurrent(self):
        for t in xrange(1, self.curit):
            self.itemmark[t] = True






class requester :


    __module__ = __name__
    def __init__(self, text, multisel = False):
        self.itemlist = None
        self.exit = False
        self.multi = multisel
        self.preview = False
        self.pimage = None
        self.keybrd = Keyboard()
        self.curdir = 'drive_list'
        self.updir = None
        self.olditem = []
        self.oldfirstit = []
        self.menu_open = None
        self.menu_save = None
        self.menu_close = None
        self.ext = ''
        self.lastpath = 'e:\\'
        self.icon = None
        self.result = None
        self.cycled = True
        self.btwlinespace = 2
        self.itemcolors = [None, 6052184, 0, 16777215, 112]
        self.scrollbarcolors = [0, 2113648, 16777215]
        self.backcolor = 11315624
        self.infobarcolor = 10262936
        self.atimer = Ao_timer()
        if s60_version_info == (3, 0) : 
            self.font = ('dense', None, graphics.FONT_NO_ANTIALIAS)
            self.font_bold = ('dense', None, graphics.FONT_BOLD)
        else : 
            self.font = (u'LatinPlain12', None)
            self.font_bold = (u'LatinBold12', None)
        self.maincycle = self.maincycle_shell
        self.createmenu(text)




    def colors(self, col = None):
        if col is not None : 
            self.backcolor = col[0]
            self.infobarcolor = col[1]
            self.itemcolors = col[2]
            self.scrollbarcolors = col[3]
        return [self.backcolor, self.infobarcolor, self.itemcolors, self.scrollbarcolors]




    def _define(self, ex):
        self.ext = ex
        self.buff = graphics.Image.new(display_pixels())
        self.parameters_save()
        self.scr = appuifw.app.screen
        appuifw.app.screen = 'full'
        appuifw.app.body = self.canv = appuifw.Canvas(redraw_callback = self.redraw, event_callback = self.event)
        appuifw.app.exit_key_handler = self.toexit
        self.exit = False
        self.canv.bind(key_codes.EKeyLeftArrow, self._up)
        self.canv.bind(key_codes.EKeyRightArrow, self._in)
        self.canv.bind(key_codes.EKeyBackspace, self._remove)
        self.canv.bind(key_codes.EKeyStar, self._pgup)
        self.canv.bind(key_codes.EKeyHash, self._pgdn)
        self._calcheight()




    def gettextheight(self, font):
        s = self.canv.measure_text(u'[WTFPLljyp!|,???]', font = font)
        return (s[0][3] - s[0][1])




    def _calcheight(self):
        self.textheight = self.gettextheight(self.font_bold)
        self.statusbarh = (self.textheight + 5)
        self.list_y = (self.statusbarh + 1)




    def createmenu(self, text):
        self.text = text
        self.menu_close = [(text['close'], self.toexit)]
        self.menu_open = [(text['open'], self._in), (text['preview'], self.switch_preview), (text['select'], ((text['selectall'], self._markall), (text['beforecursor'], self._markbeforecurrent), (text['fromcursor'], self._markfromcurrent), (text['invert'], self._invertmark), (text['deselect'], self._unmark))), (text['createfolder'], self._createfolder), (text['rename'], self._rename), (text['delete'], self._remove), (text['close'], self.toexit)]
        self.menu_save = [((u'%s%s' % (text['save'], '...')), self._returnfolder), (text['createfolder'], self._createfolder), (text['rename'], self._rename), (text['delete'], self._remove), (text['close'], self.toexit)]




    def _createfolder(self):
        self.preview = False
        fname = appuifw.query(self.text['foldername'], 'text', u'new folder')
        if fname is None : 
            return None
        fname = ur(self.curdir + '\\' + fname)
        if os.path.exists(fname) : 
            appuifw.note(self.text['folderexists'])
            return None
        os.mkdir(fname)
        self._update()




    def _markall(self):
        if self.itemlist is not None : 
            self.itemlist.markall()




    def _unmark(self):
        if self.itemlist is not None : 
            self.itemlist.unmark()




    def _invertmark(self):
        if self.itemlist is not None : 
            self.itemlist.invertmark()




    def _markfromcurrent(self):
        if self.itemlist is not None : 
            self.itemlist.markfromcurrent()




    def _markbeforecurrent(self):
        if self.itemlist is not None : 
            self.itemlist.markbeforecurrent()




    def _rename(self):
        self.preview = False
        fname = appuifw.query(self.text['newname'], 'text', self.itemlist.curitemname())
        if fname is None : 
            return None
        fname = self.curdir + '\\' + fname
        if os.path.exists(ur(fname)) : 
            appuifw.note(self.text['folderexists'])
            return None
        os.rename(ur(self.curitemname_abs()), ur(fname))
        self._update()




    def _remove(self):
        self.preview = False
        marked = self.itemlist.getmarked()
        if marked is not None : 
            ans = appuifw.query(self.text['deleteconfirm'] + self.text['allselfiles'] + u'?', 'query')
            if ans is None : 
                return None
            for t in marked:
                if os.path.isdir(ur(os.path.join(self.curdir, t))) : 
                    os.rmdir(ur(os.path.join(self.curdir, t)))
                elif os.path.isfile(ur(os.path.join(self.curdir, t))) : 
                    os.remove(ur(os.path.join(self.curdir, t)))
            pass
        else : 
            ans = appuifw.query(self.text['deleteconfirm'] + self.itemlist.curitemname(), 'query')
            if ans is None : 
                return None
            if os.path.isdir(ur(self.curitemname_abs())) : 
                os.rmdir(ur(self.curitemname_abs()))
            elif os.path.isfile(ur(self.curitemname_abs())) : 
                os.remove(ur(self.curitemname_abs()))
            pass
        self._update()




    def seticons(self, icon):
        self.icon = icon




    def _drive_list(self):
        itpares = [[x, self._in] for x in drive_list()]
        drlist = Ttextlist((1, self.list_y), self.buff, itpares, self.font_bold, self.multi)
        drlist.key['select2'] = None
        drlist.size((display_pixels()[0], 100))
        drlist.clrs = self.itemcolors
        drlist.cycled = self.cycled
        drlist.sp_bl = self.btwlinespace
        drlist._updateheight(True)
        if drlist.scroll is not None : 
            drlist.scroll.clr = self.scrollbarcolors
        return drlist




    def _sort_list(self, curdir, itlist):
        sortlist = []
        lastdir = None
        dirind = -1
        pathjoin = os.path.join
        isdir = os.path.isdir
        for t in itlist:
            if isdir(pathjoin(curdir, t)) : 
                dirind += 1
                sortlist.insert(dirind, t)
                lastdir = dirind
            elif (t[(t.rfind('.') + 1) : ]).lower() in self.ext or self.ext[-1] == '*' : 
                sortlist.append(t)
        sortlist.insert(-1, '..')
        dirind += 1
        return (sortlist, dirind)




    def _create_list(self, path):
        path = os.path.normpath(path)
        if path == 'drive_list' or path is None : 
            self.itemlist = self._drive_list()
            self.curdir = ru(path)
            self.updir = None
            if self.icon is not None : 
                for t in xrange(self.itemlist.itcount):
                    self.itemlist.itemicon(t, self.icon[0][0], self.icon[0][1])
                pass
            appuifw.app.menu = self.menu_close
        elif os.path.isdir(path) : 
            self.curdir = ru(path)
            self.updir = os.path.split(self.curdir)[0]
            if self.curdir == self.updir : 
                self.updir = 'drive_list'
            path += '\\'
            path = path.replace('\\\\', '\\')
            itlist = os.listdir(path)
            srtd = self._sort_list(path, itlist)
            itlist = srtd[0]
            lastdir = srtd[1]
            itpares = [[x.decode('utf-8'), self._in] for x in itlist]
            self.itemlist = Ttextlist((1, self.list_y), self.buff, itpares, self.font, self.multi)
            self.itemlist.key['select2'] = None
            self.itemlist.clrs = self.itemcolors
            self.itemlist.cycled = self.cycled
            self.itemlist.sp_bl = self.btwlinespace
            self.itemlist._updateheight(True)
            itemfont = self.itemlist.itemfont
            itemicon = self.itemlist.itemicon
            itcount = self.itemlist.itcount
            icon = self.icon
            ext = self.ext
            if icon is not None : 
                for t in xrange(itcount):
                    if t <= lastdir : 
                        itemfont(t, self.font_bold)
                        itemicon(t, icon[1][0], icon[1][1])
                    else : 
                        try :
                            ind = (ext.index((itlist[t][(itlist[t].rfind('.') + 1) : ]).lower()) + 2)
                            itemicon(t, icon[ind][0], icon[ind][1])
                        except ValueError : 
                            itemicon(t, icon[-1][0], icon[-1][1])
                        pass
                pass
            else : 
                for t in xrange(itcount):
                    if t <= lastdir : 
                        itemfont(t, self.font_bold)
                pass
            self.itemheight = self.itemlist.getitemheight()
            self.itemsonpage = ((display_pixels()[1] - self.statusbarh) / self.itemheight)
            self.itemlist.size((display_pixels()[0], (display_pixels()[1] - self.statusbarh)))
            self.itemlist.iteminlist(self.itemsonpage)
            if self.itemlist.scroll is not None : 
                self.itemlist.scroll.size((None, None, None, (display_pixels()[1] - 1)), False)
                self.itemlist.scroll.clr = self.scrollbarcolors
            if self.kind == 'open' : 
                appuifw.app.menu = self.menu_open
            else : 
                appuifw.app.menu = self.menu_save
            pass




    def parameters_save(self):
        self.paramtuple = (appuifw.app.screen, appuifw.app.body, appuifw.app.menu, appuifw.app.title, appuifw.app.exit_key_handler)




    def parameters_restore(self):
        appuifw.app.screen = self.paramtuple[0]
        appuifw.app.body = self.paramtuple[1]
        appuifw.app.menu = self.paramtuple[2]
        appuifw.app.title = self.paramtuple[3]
        appuifw.app.exit_key_handler = self.paramtuple[4]




    def open(self, path = None, ext = [], kind = 'open'):
        if path is None : 
            path = self.lastpath
        try :
            path = ur(path)
        except :
            pass
        if  not (os.path.isdir(path)) : 
            path = self.lastpath
        self.kind = kind
        self._define(ext)
        self._create_list(path)
        self.maincycle()
        self.parameters_restore()
        return self.result




    def maincycle_sdln(self):
        self.redraw(None)
        self.atimer.after(0.01, self.maincycle_sdln)




    def maincycle_shell(self):
        while self.exit is False : 
            if self.preview : 
                self.show_preview()
            self.redraw(None)
            ao_sleep(0.01)




    def toexit(self):
        self.preview = False
        self.exit = True
        self.result = None
        self.atimer.cancel()




    def _pgup(self):
        self.itemlist.gotoitem((self.curitem() - self.itemlist.itinlist))




    def _pgdn(self):
        self.itemlist.gotoitem(self.curitem() + self.itemlist.itinlist)




    def _in(self):
        self.preview = False
        marked = self.itemlist.getmarked()
        if marked is not None : 
            self.result = []
            for t in marked:
                self.result.append(os.path.join(self.curdir, t))
            self.exit = True
            self.atimer.cancel()
        elif os.path.isfile(ur(self.curitemname_abs())) : 
            self.result = self.curitemname_abs()
            self.lastpath = self.curdir + '\\'
            self.exit = True
            self.atimer.cancel()
        elif self.itemlist.curitemname() == '..' : 
            self._up()
        else : 
            self.olditem.append(self.curitem())
            self.oldfirstit.append(self.itemlist.firstit)
            try :
                self._create_list(self.curitemname_abs().encode('utf-8'))
            except :
                self._create_list(self.curitemname_abs())
            pass




    def _returnfolder(self):
        self.result = self.curdir + '\\'
        self.result = self.result.replace('\\\\', '\\')
        if os.path.isdir(ur(self.result)) : 
            self.lastpath = self.result
            self.exit = True
            self.atimer.cancel()




    def _update(self):
        olditem = self.curitem()
        fst = self.itemlist.firstit
        try :
            self._create_list(self.curdir.encode('utf-8'))
        except :
            self._create_list(self.curdir)
        if olditem < self.itemlist.itcount : 
            self.itemlist.gotoitem(olditem, fst)
        else : 
            self.itemlist.gotoitem((olditem - 1), (fst - 1))




    def _up(self):
        if self.updir is None : 
            return None
        try :
            self._create_list(self.updir.encode('utf-8'))
        except :
            self._create_list(self.updir)
        if len(self.olditem) > 0 : 
            self.curitem(self.olditem.pop())
            self.itemlist.firstit = self.oldfirstit.pop()




    def redraw(self, rect):
        if self.itemlist is not None : 
            self.buff.clear(self.backcolor)
            self.buff.rectangle((-1, -1, (display_pixels()[0] + 1), self.statusbarh), fill = self.infobarcolor, outline = 0)
            self.buff.text((2, self.textheight), self.curitemname_abs(), font = self.font, fill = 0)
            self.itemlist.draw()
            self.canv.blit(self.buff)




    def event(self, evt):
        if self.itemlist is not None : 
            self.keybrd.handle_event(evt)
            if  not (self.preview) : 
                self.itemlist.control(evt)
                if self.keybrd.pressed(key_codes.EScancode5) : 
                    self.load_preview()
                pass
            else : 
                if evt['scancode'] == key_codes.EScancodeSelect or self.keybrd.pressed(key_codes.EScancodeRightSoftkey) or self.keybrd.pressed(key_codes.EScancode5) : 
                    self.preview = False
                if evt['scancode'] == key_codes.EScancodeLeftArrow : 
                    self.preview = False
                if evt['scancode'] == key_codes.EScancodeUpArrow or evt['scancode'] == key_codes.EScancodeDownArrow : 
                    self.itemlist.control(evt)
                    if self.pitemname != self.curitemname_abs() : 
                        self.load_preview()
                    pass
                pass
            pass




    def switch_preview(self):
        self.preview =  not (self.preview)
        if self.preview is True : 
            self.load_preview()




    def load_preview(self):
        try :
            pimage = graphics.Image.open(self.curitemname_abs())
            self.preview = True
            self.pitemname = self.curitemname_abs()
            self.pimage, self.prevcoord = self.calc_preview(pimage, self.canv)
        except Exception : 
            traceback.print_exc(sys.stderr)
            return None




    def show_preview(self):
        if self.pimage is None : 
            return None
        while self.preview : 
            ao_sleep(0.1)
            self.buff.clear(10066329)
            self.buff.blit(self.pimage, target = self.prevcoord, scale = 0)
            self.canv.blit(self.buff)
        del self.pimage
        self.preview = False




    def calc_preview(self, img, canv):
        aspect_x = (float(img.size[0]) / float(canv.size[0]))
        aspect_y = (float(img.size[1]) / float(canv.size[1]))
        aspect = max(aspect_x, aspect_y)
        if aspect < 1 : 
            aspect = 1
        prev_image = graphics.Image.new(((img.size[0] / aspect), (img.size[1] / aspect)))
        if prev_image is None : 
            return False
        prev_image.blit(img, scale = 1)
        prev_coord = [((canv.size[0] / 2) - (prev_image.size[0] / 2)), ((canv.size[1] / 2) - (prev_image.size[1] / 2))]
        return (prev_image, prev_coord)




    def curitem(self, it = None):
        return self.itemlist.curitem(it)




    def curitemname_abs(self):
        if self.curdir == 'drive_list' : 
            return self.itemlist.curitemname() + '\\'
        return os.path.join(self.curdir, self.itemlist.curitemname())



