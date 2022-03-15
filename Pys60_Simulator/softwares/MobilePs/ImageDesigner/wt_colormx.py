# -*- coding: utf-8 -*-

import graphics
import appuifw
from e32 import ao_sleep as ao_sleep
import key_codes
import wt_ui
from sysinfo import display_pixels as display_pixels
__version__ = 1.4
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






def redraw(rect):
    buff.clear(10066329)
    bar[0].draw()
    bar[1].draw()
    bar[2].draw()
    buff.blit(pall, target = (65, 5))
    buff.blit(pal, target = (35, 5))
    buff.blit(pa, target = (5, 5))
    buff.rectangle((100, 50, 160, 110), fill = old_color, outline = None)
    buff.rectangle((100, 110, 160, 170), fill = color, outline = None)
    buff.text((90, 20), (u'RGB: %d,%d,%d' % color))
    c = (65536 * color[0]) + (256 * color[1]) + color[2]
    buff.text((90, 35), (u'Hex: %06x' % c))
    canv.blit(buff)




def event(evt):
    keybrd.handle_event(evt)




def exit(f = False):
    appuifw.app.screen = scr
    appuifw.app.body = None
    running = 0
    if f is True : 
        color = None
    global running, color




def palette(w, s, c, kind = True, vert = True):


    def setcol(c1, c2, c3):
        if c1 > 255 : 
            c1 = 255
        elif c1 < 0 : 
            c1 = 0
        if c2 > 255 : 
            c2 = 255
        elif c2 < 0 : 
            c2 = 0
        if c3 > 255 : 
            c3 = 255
        elif c3 < 0 : 
            c3 = 0
        return (c1, c2, c3)


    if kind == True : 
        h = s
        dy = ((h / 6) + 1)
        n = (256 / dy)
    else : 
        n = s
        dy = (256 / n)
        h = (dy * 6)
    if vert == True : 
        image = graphics.Image.new((w, h))
    line = image.line
    for t in xrange(dy):
        line((0, t, w, t), outline = setcol(c[0], (t * n), 0))
    for t in xrange(dy):
        line((0, dy + t, w, dy + t), outline = setcol((c[0] - (t * n)), c[0], 0))
    for t in xrange(dy):
        line((0, (2 * dy) + t, w, (2 * dy) + t), outline = setcol(0, c[0], (t * n)))
    for t in xrange(dy):
        line((0, (3 * dy) + t, w, (3 * dy) + t), outline = setcol(0, (c[0] - (t * n)), c[0]))
    for t in xrange(dy):
        line((0, (4 * dy) + t, w, (4 * dy) + t), outline = setcol((t * n), 0, c[0]))
    for t in xrange(dy):
        line((0, (5 * dy) + t, w, (5 * dy) + t), outline = setcol(c[0], 0, (c[0] - (t * n))))
    return image




def palette2(w, dd, c, kind = True, vert = True):


    def brightness(c, val):
        col = [c[0], c[1], c[2]]
        for t in xrange(3):
            col[t] = (col[t] + 255 - val)
            if col[t] > 255 : 
                col[t] = 255
            if col[t] < 0 : 
                col[t] = 0
        return (col[0], col[1], col[2])




    def saturation(c, val):
        col = [c[0], c[1], c[2]]
        for t in xrange(3):
            col[t] = (col[t] - val)
            if col[t] < 0 : 
                col[t] = 0
        return (col[0], col[1], col[2])


    if kind == True : 
        d = (dd / 2)
        s = (255.0 / d)
    else : 
        d = (255.0 / dd)
        s = (255.0 / d)
    if vert == True : 
        image = graphics.Image.new((w, (d * 2)))
        line = image.line
        for t in xrange(0, d):
            line((0, t, w, t), outline = brightness(c, (t * s)))
            line((0, d + t, w, d + t), outline = saturation(c, (t * s)))
        pass
    else : 
        image = graphics.Image.new(((d * 2), w))
        line = image.line
        for t in xrange(0, d):
            line((t, 0, t, w), outline = brightness(c, (t * s)))
            line((d + t, 0, d + t, w), outline = saturation(c, (t * s)))
        pass
    return image




def palette3(w, dd, c, kind = True, vert = True):


    def gray(c, val):
        col = [c[0], c[1], c[2]]
        for t in xrange(3):
            col[t] = (col[t] - val)
            if col[t] > 255 : 
                col[t] = 255
            if col[t] < 0 : 
                col[t] = 0
        return (col[0], col[1], col[2])


    if kind == True : 
        d = dd
        s = (255.0 / d)
    else : 
        d = (255.0 / dd)
        s = (255.0 / d)
    if vert == True : 
        image = graphics.Image.new((w, d))
        line = image.line
        for t in xrange(0, d):
            line((0, t, w, t), outline = gray(c, (t * s)))
        pass
    else : 
        image = graphics.Image.new((d, w))
        line = image.line
        for t in xrange(0, d):
            line((t, 0, t, w), outline = gray(c, (t * s)))
        pass
    return image




def switchbar(d):
    count = count + d
    if count > 2 : 
        count = 2
    if count < 0 : 
        count = 0
    for t in xrange(len(bar)):
        bar[t].color([None, 0, None])
    bar[count].color([0, 0, None])
    global count




def value(dv, d = True):
    if d is True : 
        bar[count].value(bar[count].value() + dv)
    else : 
        bar[count].value(dv)
    updatebar(bar[count])




def updatebar(br):
    if br == bar[0] : 
        c = pa.getpixel((0, bar[0].value()))[0]
        pal = palette(14, 200, c, True, True)
        color = pall.getpixel((0, bar[2].value()))[0]
    elif br == bar[1] : 
        c = pal.getpixel((0, bar[1].value()))[0]
        pall = palette2(14, 200, c, True, True)
        color = pall.getpixel((0, bar[2].value()))[0]
    elif br == bar[2] : 
        color = pall.getpixel((0, bar[2].value()))[0]
    return None
    global pal, color, pall




def setcolor(col, d = False):
    c = [color[0], color[1], color[2]]
    for t in xrange(len(c)):
        if col[t] is not None : 
            if d is False : 
                c[t] = col[t]
            else : 
                c[t] = c[t] + col[t]
            if c[t] > 255 : 
                c[t] = 255
            elif c[t] < 0 : 
                c[t] = 0
            pass
    color = (c[0], c[1], c[2])
    global color




def create_bar2():
    bar[2] = wt_ui.Tbar(61, 4, 83, 206, (0, 199), 200, buff, True, 0)
    bar[2].color([None, 0, None])
    bar[2].scrollwidth(1)
    bar[2].value(0)




def create_bar1():
    bar[1] = wt_ui.Tbar(31, 4, 53, 206, (0, 199), 200, buff, True, 0)
    bar[1].color([None, 0, None])
    bar[1].scrollwidth(1)
    bar[1].value(0)




def create_bar3():
    bar[0] = wt_ui.Tbar(1, 4, 23, 206, (0, 199), 200, buff, True, 0)
    bar[0].color([None, 0, None])
    bar[0].scrollwidth(1)
    bar[0].value(0)




def init(col, text):
    keybrd = Keyboard()
    buff = graphics.Image.new(display_pixels())
    old_color = col
    count = -1
    bar = [0, 0, 0]
    create_bar1()
    create_bar2()
    create_bar3()
    switchbar(1)
    pa = palette3(14, 200, (255, 255, 255), True, True)
    pall = palette2(14, 200, (255, 0, 0), True, True)
    pal = palette(14, 200, (255, 0, 0), True, True)
    color = pall.getpixel((0, bar[2].value()))[0]
    scr = appuifw.app.screen
    appuifw.app.screen = 'full'
    appuifw.app.body = canv = appuifw.Canvas(redraw_callback = redraw, event_callback = event)
    appuifw.app.exit_key_handler = exit
    appuifw.app.menu = [(text['ok'], lambda  : exit(False) ), (text['cancel'], lambda  : exit(True) )]
    canv.bind(key_codes.EKeyLeftArrow, lambda  : switchbar(-1) )
    canv.bind(key_codes.EKeyRightArrow, lambda  : switchbar(1) )
    canv.bind(key_codes.EKeyDownArrow, lambda  : value(1) )
    canv.bind(key_codes.EKeyUpArrow, lambda  : value(-1) )
    canv.bind(key_codes.EKey1, lambda  : value(-10) )
    canv.bind(key_codes.EKey2, lambda  : value(99, False) )
    canv.bind(key_codes.EKey3, lambda  : value(10) )
    canv.bind(key_codes.EKey4, lambda  : setcolor((1, None, None), True) )
    canv.bind(key_codes.EKey7, lambda  : setcolor((127, None, None)) )
    canv.bind(key_codes.EKeyStar, lambda  : setcolor((-1, None, None), True) )
    canv.bind(key_codes.EKey5, lambda  : setcolor((None, 1, None), True) )
    canv.bind(key_codes.EKey8, lambda  : setcolor((None, 127, None)) )
    canv.bind(key_codes.EKey0, lambda  : setcolor((None, -1, None), True) )
    canv.bind(key_codes.EKey6, lambda  : setcolor((None, None, 1), True) )
    canv.bind(key_codes.EKey9, lambda  : setcolor((None, None, 127)) )
    canv.bind(key_codes.EKeyHash, lambda  : setcolor((None, None, -1), True) )
    running = 1
    while running == 1 : 
        redraw(None)
        ao_sleep(0.001)
    return color
    global keybrd, buff, old_color, count, bar, pa, pall, pal, color, scr, canv, running

