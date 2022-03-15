# -*- coding: utf-8 -*-

import appuifw
import graphics
import e32
import os
import time
import sys
import clipboard

if __name__=='__main__':
    #调试
    sys.stdout=open('e:/aaa/ai/调试.log','a')
    sys.path.append('e:\\aaa\\组件//游戏\\历古仙穹//')


def dec(t):
    try:
        return t.decode('utf-8','replace')
    except:
        return t

def enc(t):
    try:
        return t.encode('utf-8', 'replace')
    except :
        return t




lock=e32.Ao_lock()
class Keyboard(object) :
    __module__=__name__
    def __init__(s):
        s.b=None
        s.d=[]
    def handle_event(s,e):
        s.e = e
        s.code = s.e['scancode']
        s.type = s.e['type']
        s.kc = s.e['keycode']
        s.mod = s.e['modifiers']
        if s.type == 3 : 
            s.b = time.clock()
            s.d.append(s.code)
        elif s.type == 1 : 
            if (time.clock() - 0.5) > s.b : 
                s.d.append(s.code)
                s.d.append(s.code)
                s.d.append(s.code)
                s.d.append(s.code)
                s.d.append(s.code)
                s.d.append(s.code)
                s.d.append(s.code)
            pass
        elif s.type == 2 : 
            s.b = None
            s.d = []
        lock.signal()
    def key(s):
        try :
            return s.d.pop(0)
        except :
            return None


kb = Keyboard()
app = None
def handle_redraw(rect=None):
    if app : 
        if app.rot : 
            img = app.img.transpose(app.rot)
        else : 
            img = app.img
        can.blit(img, target = (app.x, app.y))

def p():
    pass

def abort():
    os.abort()


appuifw.app.screen = 'full'
can = appuifw.Canvas(event_callback = kb.handle_event, redraw_callback = handle_redraw)
appuifw.app.body = can
w, h = can.size
class Screen(object):
    __module__ = __name__
    def __init__(s):
        s.x, s.y, s.w, s.h = (0, 0, w, h)
        s.rot = None
        s.bg = None
        s.mask = None
        s.img = graphics.Image.new((s.w, s.h))
        s.color = [15658734, 8388608]
        s.text_color = 0
        s.link_color = 128
        s.title_color = 16768426
        s.text_font = u''
        s.link_font = u''
        s.title_font = u''
        s.cur_color = [11184810, 13421772]
        s.status = 'screen'
        s.cur_status = 'w'
        s.cur_pos = 0
        s.mar = 15
        s.start = 0
        s.pos = 0
        s.ty = 20
        s.objects = []
        s.title = 'wif-screen'
        s.funcs = []
        s.exit = lambda  : hide()
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = s.cur_left
        s.funcs[15] = s.cur_right
        s.funcs[16] = s.cur_up
        s.funcs[17] = s.cur_down
        s.funcs[18] = p
        s.funcs[42] = lambda  :  s.scroll_up(175) 
        s.funcs[48] = p
        s.funcs[49] = p
        s.funcs[50] = p
        s.funcs[51] = p
        s.funcs[52] = p
        s.funcs[53] = p
        s.funcs[54] = p
        s.funcs[55] = p
        s.funcs[56] = p
        s.funcs[57] = p
        s.funcs[127] = lambda  :  s.scroll_down(175) 
        s.funcs[164] = s.menu
        s.funcs[167] = s.select
        s.funcs[196] = lambda  : screenshot() 
        s.gh = ((s.h - s.mar) - 2)
        s.nl = None
        s.pl = None


    def set_bg(s, im, mask = None):
        s.bg = im
        if mask : 
            s.mask = mask
        else : 
            s.mask = graphics.Image.new(s.bg.size, mode = '1')
            s.mask.clear(16777215)




    def del_bg(s):
        s.bg, s.mask = (None, None)




    def rotate(s, rotat):
        if rotat == 0 : 
            s.rot, s.w, s.h = (None, w, h)
            s.funcs[14] = s.cur_left
            s.funcs[15] = s.cur_right
            s.funcs[16] = s.cur_up
            s.funcs[17] = s.cur_down
        elif rotat == 90 : 
            s.rot, s.w, s.h = (graphics.ROTATE_90, h, w)
            s.funcs[14] = s.cur_up
            s.funcs[15] = s.cur_down
            s.funcs[16] = s.cur_right
            s.funcs[17] = s.cur_left
        elif rotat == 180 : 
            s.rot, s.w, s.h = (graphics.ROTATE_180, w, h)
            s.funcs[14] = s.cur_right
            s.funcs[15] = s.cur_left
            s.funcs[16] = s.cur_down
            s.funcs[17] = s.cur_up
        elif rotat == 270 : 
            s.rot, s.w, s.h = (graphics.ROTATE_270, h, w)
            s.funcs[14] = s.cur_down
            s.funcs[15] = s.cur_up
            s.funcs[16] = s.cur_left
            s.funcs[17] = s.cur_right
        s.set_size((s.x, s.y, s.w, s.h))




    def bind(s, k, f):
        s.funcs[k] = f




    def clear(s):
        s.objects = []
        s.pos = 0
        s.start = 0
        s.cur_pos = 0
        s.ty = 20




    def set_size(s, size):
        s.x, s.y, s.w, s.h = size
        s.img = graphics.Image.new((s.w, s.h))
        s.mask = graphics.Image.new((w, h), mode = '1')
        s.mask.clear(16777215)
        s.gh = ((s.h - s.mar) - 2)




    def cur_up(s):
        if s.objects[s.cur_pos][0] == 'table' : 
            if s.objects[s.cur_pos][2].ul != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].ul
            elif s.objects[s.cur_pos][2].pll != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pll
            elif s.objects[s.cur_pos][2].pfl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pfl
            elif s.pl != None : 
                s.cur_pos = s.pl
            else : 
                s.scroll_up()
            pass
        elif s.objects[s.cur_pos][0] == 'check' : 
            if s.objects[s.cur_pos][2].pc != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pc
            elif s.pl != None : 
                s.cur_pos = s.pl
            else : 
                s.scroll_up()
            pass
        elif s.pl != None : 
            s.cur_pos = s.pl
        else : 
            s.scroll_up()




    def cur_down(s):
        if s.objects[s.cur_pos][0] == 'table' : 
            if s.objects[s.cur_pos][2].dl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].dl
            elif s.objects[s.cur_pos][2].nfl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nfl
            elif s.objects[s.cur_pos][2].nll != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nll
            elif s.nl : 
                s.cur_pos = s.nl
            else : 
                s.scroll_down()
            pass
        elif s.objects[s.cur_pos][0] == 'check' : 
            if s.objects[s.cur_pos][2].nc != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nc
            elif s.nl : 
                s.cur_pos = s.nl
            else : 
                s.scroll_down()
            pass
        elif s.nl : 
            s.cur_pos = s.nl
        else : 
            s.scroll_down()




    def cur_left(s):
        if s.objects[s.cur_pos][0] == 'table' : 
            if s.objects[s.cur_pos][2].pl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pl
            elif s.objects[s.cur_pos][2].pll != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pll
            elif s.objects[s.cur_pos][2].pfl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].pfl
            pass




    def cur_right(s):
        if s.objects[s.cur_pos][0] == 'table' : 
            if s.objects[s.cur_pos][2].nl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nl
            elif s.objects[s.cur_pos][2].nfl != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nfl
            elif s.objects[s.cur_pos][2].nll != None : 
                s.objects[s.cur_pos][2].cur_pos = s.objects[s.cur_pos][2].nll
            pass




    def scroll_up(s, t = 12):
        if s.start > 0 : 
            s.start -= t
            if s.start < 0 : 
                s.start = 0
            for i in xrange(len(s.objects)):
                if s.start + s.mar < s.objects[i][1][3] : 
                    s.pos = i
                    if s.pos < 0 : 
                        s.pos = 0
                    break
            pass




    def scroll_down(s, t = 12):
        if s.start + s.gh + s.mar < s.ty : 
            s.start += t
            for i in xrange(len(s.objects)):
                if s.start + s.mar < s.objects[i][1][3] : 
                    s.pos = i
                    if s.pos < 0 : 
                        s.pos = 0
                    break
            pass




    def scroll_left(s):
        pass




    def scroll_right(s):
        pass




    def scroll_bar(s):
        if s.gh + s.mar < s.ty : 
            s.img.rectangle(((s.w - 5), (s.mar + 1), s.w, (s.h - 1)), 0)
            sh = round(((s.gh * s.gh) / s.ty))
            ss = (round(((s.start * s.gh) / s.ty)) + s.mar + 2)
            s.img.rectangle(((s.w - 4), ss, (s.w - 1), ss + sh), 0, 0)




    def select(s):
        if len(s.objects) > 0 and s.objects[s.cur_pos][0] == 'link' : 
            s.objects[s.cur_pos][5]()
        elif len(s.objects) > 0 and s.objects[s.cur_pos][0] == 'glink' : 
            s.objects[s.cur_pos][4]()
        elif len(s.objects) > 0 and s.objects[s.cur_pos][0] == 'table' : 
            t = s.objects[s.cur_pos][2]
            if t.objects[t.cur_pos[1]][t.cur_pos[0]][0] == 'link' : 
                t.objects[t.cur_pos[1]][t.cur_pos[0]][5]()
            if t.objects[t.cur_pos[1]][t.cur_pos[0]][0] == 'glink' : 
                t.objects[t.cur_pos[1]][t.cur_pos[0]][4]()
            pass
        elif len(s.objects) > 0 and s.objects[s.cur_pos][0] == 'check' : 
            if s.objects[s.cur_pos][2].type == 'multicheck' : 
                if s.objects[s.cur_pos][2].checked[s.objects[s.cur_pos][2].cur_pos] == 0 : 
                    s.objects[s.cur_pos][2].checked[s.objects[s.cur_pos][2].cur_pos] = 1
                else : 
                    s.objects[s.cur_pos][2].checked[s.objects[s.cur_pos][2].cur_pos] = 0
                pass
            else : 
                for k in range(len(s.objects[s.cur_pos][2].checked)):
                    s.objects[s.cur_pos][2].checked[k] = 0
                s.objects[s.cur_pos][2].checked[s.objects[s.cur_pos][2].cur_pos] = 1
            pass




    def menu(s):
        pass




    def top_line(s):
        s.img.rectangle((0, 0, s.w, s.mar), 0, s.color[1])
        s.img.text((5, (s.mar - 2)), dec(s.title), s.title_color, font = s.title_font)




    def text(s, text, color = None, font = None, align = 'left'):
        if font == None : 
            font = s.text_font
        if color == None : 
            color = s.text_color
        t = ''
        sp = ''
        try :
            text = text.decode('utf-8', 'replace')
        except :
            pass
        while text.startswith(dec(' ')) : 
            sp += dec(' ')
            text = text[1 : ]
        text = text.strip()
        ts = text.split()
        tt = []
        ho = 0
        wo = 0
        tty = s.ty
        ttx = s.w
        mh = ((s.img.measure_text(u'A', font = font)[0][1] * -1) + 3)
        while len(ts) > 0 : 
            try :
                mw = (s.img.measure_text(sp + t + ts[0], font = font)[1] + 3)
            except :
                mw = 1000
            try :
                long = (s.img.measure_text(sp + t + ts[0], font = font)[1] + 3)
            except :
                long = 3
            if long > (s.w - 12) : 
                ind = ((s.img.measure_text(ts[0], font = font, maxwidth = (s.w - 12))[2] - len(t)) - len(sp))
                t = ts[0][0 : ind]
                ts[0] = ts[0][ind : ]
                mw = (s.img.measure_text(sp + t, font = font)[1] + 3)
                if wo < mw : 
                    wo = mw
                if align == 'left' : 
                    tx = 5
                    ttx = tx
                elif align == 'center' : 
                    tx = round(((s.w - mw) / 2))
                    if ttx > tx : 
                        ttx = tx
                    pass
                elif align == 'right' : 
                    tx = ((s.w - mw) - 7)
                    if ttx > tx : 
                        ttx = tx
                    pass
                cor = (tx, (s.ty + mh - 2))
                s.ty += mh
                tt.append([cor, sp + t.rstrip()])
                t = ''
                sp = ''
                if len(ts) == 0 : 
                    break
                pass
            else : 
                while mw < (s.w - 10) : 
                    try :
                        t += ts.pop(0) + dec(' ')
                        mw = (s.img.measure_text(sp + t + ts[0], font = font)[0][2] + 3)
                    except IndexError : 
                        break
                mw = s.img.measure_text(sp + t, font = font)[1]
                if wo < mw : 
                    wo = mw
                if align == 'left' : 
                    tx = 5
                    ttx = tx
                elif align == 'center' : 
                    tx = round(((s.w - mw) / 2))
                    if ttx > tx : 
                        ttx = tx
                    pass
                elif align == 'right' : 
                    tx = ((s.w - mw) - 7)
                    if ttx > tx : 
                        ttx = tx
                    pass
                cor = (tx, (s.ty + mh - 2))
                s.ty = s.ty + mh
                tt.append([cor, sp + t.rstrip()])
                t = ''
                sp = ''
                if len(ts) == 0 : 
                    break
                pass
        ho = (mh * len(tt))
        s.objects.append(['text', [ttx, tty, ttx + wo, tty + ho], tt, color, font])




    def link(s, text, f, color = None, font = None, align = 'left'):
        if font == None : 
            font = s.link_font
        if color == None : 
            color = s.link_color
        t = ''
        sp = ''
        try :
            text = text.decode('utf-8', 'replace')
        except :
            pass
        while text.startswith(dec(' ')) : 
            sp += dec(' ')
            text = text[1 : ]
        text = text.strip()
        ts = text.split()
        tt = []
        ho = 0
        wo = 0
        tty = s.ty
        ttx = s.w
        mh = ((s.img.measure_text(dec('A'), font = font)[0][1] * -1) + 3)
        while len(ts) > 0 : 
            try :
                mw = (s.img.measure_text(sp + t + ts[0], font = font)[1] + 3)
            except :
                mw = 1000
            try :
                long = (s.img.measure_text(sp + t + ts[0], font = font)[1] + 3)
            except :
                long = 3
            if long > (s.w - 12) : 
                ind = ((s.img.measure_text(ts[0], font = font, maxwidth = (s.w - 12))[2] - len(t)) - len(sp))
                t = ts[0][0 : ind]
                ts[0] = ts[0][ind : ]
                mw = (s.img.measure_text(sp + t, font = font)[1] + 3)
                if wo < mw : 
                    wo = mw
                if align == 'left' : 
                    tx = 5
                    ttx = tx
                elif align == 'center' : 
                    tx = round(((s.w - mw) / 2))
                    if ttx > tx : 
                        ttx = tx
                    pass
                elif align == 'right' : 
                    tx = ((s.w - mw) - 7)
                    if ttx > tx : 
                        ttx = tx
                    pass
                cor = ((tx + 3), (s.ty + mh - 2))
                s.ty += mh
                tt.append([cor, sp + t.rstrip()])
                t = ''
                sp = ''
                if len(ts) == 0 : 
                    break
                pass
            else : 
                while mw < (s.w - 10) : 
                    try :
                        t += ts.pop(0) + dec(' ')
                        mw = (s.img.measure_text(sp + t + ts[0], font = font)[0][2] + 3)
                    except IndexError : 
                        break
                mw = s.img.measure_text(sp + t, font = font)[1]
                if wo < mw : 
                    wo = mw
                if align == 'left' : 
                    tx = 5
                    ttx = tx
                elif align == 'center' : 
                    tx = round(((s.w - mw) / 2))
                    if ttx > tx : 
                        ttx = tx
                    pass
                elif align == 'right' : 
                    tx = ((s.w - mw) - 7)
                    if ttx > tx : 
                        ttx = tx
                    pass
                cor = ((tx + 3), (s.ty + mh - 2))
                s.ty = s.ty + mh
                tt.append([cor, sp + t.rstrip()])
                t = ''
                sp = ''
                if len(ts) == 0 : 
                    break
                pass
        ho = (mh * len(tt))
        s.objects.append(['link', [ttx, tty, ttx + wo, tty + ho], tt, color, font, f])




    def row_link(s, text, func, color = None, font = None, align = 'left'):
        if color : 
            col = color
        else : 
            col = s.link_color
        if font : 
            fon = font
        else : 
            fon = s.link_font
        try :
            text = dec(text)
        except :
            pass
        mw = s.img.measure_text(text, font = fon, maxwidth = (s.w - 12))
        if align == 'left' : 
            ttx = 5
        elif align == 'center' : 
            ttx = round(((s.w - mw[1]) / 2))
        elif align == 'right' : 
            ttx = ((s.w - mw[1]) - 5)
        mh = ((s.img.measure_text(u'A', font = fon)[0][1] * -1) + 3)
        coor = (ttx, s.ty, (ttx + mw[1] + 4), s.ty + mh)
        s.ty += mh
        t = text[0 : mw[2]]
        if len(text) > len(t) : 
            t = t[0 : -1] + u'...'
        tt = [[((ttx + 2), (s.ty - 2)), t]]
        s.objects.append(('link', coor, tt, col, fon, func))




    def image(s, im, mask = None, align = 'left'):
        if mask == None : 
            mask = graphics.Image.new(im.size, mode = '1')
            mask.clear(16777215)
        elif py_info < (2, 6) : 
            mk = graphics.Image.new(im.size, mode = '1')
            mk.blit(mask)
            mask = mk
            del mk
        mw, mh = im.size
        if align == 'left' : 
            tx = 5
        elif align == 'center' : 
            tx = round(((s.w - mw) / 2))
        elif align == 'right' : 
            tx = ((s.w - mw) - 7)
        s.objects.append(('image', (tx, s.ty, tx + mw, s.ty + mh), im, mask))
        s.ty += mh




    def glink(s, im, f, mask = None, align = 'left'):
        if mask == None : 
            mask = graphics.Image.new((im.size[0], im.size[1]), mode = '1')
            mask.clear(16777215)
        elif py_info < (2, 6) : 
            mk = graphics.Image.new(im.size, mode = '1')
            mk.blit(mask)
            mask = mk
            del mk
        mw, mh = im.size
        if align == 'left' : 
            tx = 5
        elif align == 'center' : 
            tx = round(((s.w - mw) / 2))
        elif align == 'right' : 
            tx = ((s.w - mw) - 7)
        s.objects.append(('glink', (tx, s.ty, tx + mw, s.ty + mh), im, mask, f))
        s.ty += mh




    def table(s, tab):
        s.ty += 5
        cor = (tab.x, s.ty, tab.x + tab.w, s.ty + tab.ty)
        s.objects.append(('table', cor, tab))
        s.ty += tab.ty + 5




    def checkbox(s, check):
        s.ty += 5
        cor = (check.tx, s.ty, ((w - 7) - check.tx), s.ty + check.ty)
        s.objects.append(('check', cor, check))
        s.ty = (s.ty + check.ty + 5)




    def paint(s):
        appuifw.app.exit_key_handler = s.exit
        s.fl = None
        s.ll = None
        s.pl = None
        s.nl = None
        s.img.rectangle((0, 0, s.w, s.h), 0, s.color[0])
        if s.bg : 
            s.img.blit(s.bg, mask = s.mask)
        for i in xrange(s.pos, len(s.objects)):
            el = s.objects[i]
            if el[1][1] >= (s.start + s.h - 10) : 
                break
            if el[0] == 'check' : 
                if  not (s.fl) : 
                    s.fl = i
                s.ll = i
                if i < s.cur_pos : 
                    s.pl = i
                elif s.nl == None and i > s.cur_pos : 
                    s.nl = i
                e = el[2].objects
                el[2].pc = None
                el[2].nc = None
                for j in xrange(len(e)):
                    if e[j][0][1] + el[1][1] < (15 + s.start) : 
                        continue
                    elif e[j][0][0] + el[1][1] > h + s.start : 
                        break
                    if j < el[2].cur_pos : 
                        el[2].pc = j
                    if j > el[2].cur_pos and el[2].nc == None : 
                        el[2].nc = j
                    s.img.rectangle((el[2].cx, ((el[1][1] + e[j][1][0][0][1] - el[2].check_size) - s.start), el[2].cx + el[2].check_size, (el[1][1] + e[j][1][0][0][1] - s.start)), el[2].check_color)
                    if el[2].checked[j] == 1 : 
                        s.img.rectangle(((el[2].cx + 2), (((el[1][1] + e[j][1][0][0][1] - el[2].check_size) - s.start) + 2), (el[2].cx + el[2].check_size - 2), ((el[1][1] + e[j][1][0][0][1] - s.start) - 2)), el[2].check_color, el[2].check_color)
                    if i == s.cur_pos and j == el[2].cur_pos : 
                        s.img.rectangle(((el[2].cx - 1), (((el[1][1] + e[j][1][0][0][1] - el[2].check_size) - s.start) - 1), (el[2].cx + el[2].check_size + 1), ((el[1][1] + e[j][1][0][0][1] - s.start) + 1)), s.cur_color[0])
                    for k in xrange(len(e[j][1])):
                        s.img.text((e[j][1][k][0][0], (e[j][1][k][0][1] + el[1][1] - s.start)), e[j][1][k][1], el[2].color, el[2].font)
                pass
            if el[0] == 'table' : 
                if  not (s.fl) : 
                    s.fl = i
                s.ll = i
                if i < s.cur_pos : 
                    s.pl = i
                elif s.nl == None and i > s.cur_pos : 
                    s.nl = i
                if el[2].bg_color != None : 
                    s.img.rectangle((el[1][0], (el[1][1] - s.start), el[1][2], (el[1][3] - s.start)), el[2].bg_color, el[2].bg_color)
                if el[2].border_color != None : 
                    s.img.rectangle(((el[1][0] - 1), ((el[1][1] - s.start) - 1), (el[1][2] + 1), ((el[1][3] - s.start) + 1)), el[2].border_color)
                    s.img.rectangle(((el[1][0] - 2), ((el[1][1] - s.start) - 2), (el[1][2] + 2), ((el[1][3] - s.start) + 2)), el[2].border_color)
                if el[2].line_color != None : 
                    s.img.rectangle((el[1][0], (el[1][1] - s.start), el[1][2], (el[1][3] - s.start)), el[2].line_color)
                    s.img.rectangle(((el[1][0] - 2), ((el[1][1] - s.start) - 2), (el[1][2] + 2), ((el[1][3] - s.start) + 2)), el[2].line_color)
                    tempx = el[2].x
                    for a in xrange(len(el[2].cols)):
                        s.img.line(((tempx + el[2].cols[a] - 1), (el[1][1] - s.start), (tempx + el[2].cols[a] - 1), (el[1][3] - s.start)), el[2].line_color)
                        tempx += el[2].cols[a]
                    tempy = el[1][1]
                    for a in xrange(len(el[2].rows)):
                        s.img.line((el[2].x, ((tempy + el[2].rows[a] - s.start) - 1), el[2].x + el[2].w, ((tempy + el[2].rows[a] - s.start) - 1)), el[2].line_color)
                        tempy += el[2].rows[a]
                    pass
                el[2].fl = None
                el[2].ll = None
                el[2].pl = None
                el[2].nl = None
                el[2].pfl = None
                el[2].pll = None
                el[2].nfl = None
                el[2].nll = None
                el[2].ul = None
                el[2].dl = None
                for r in xrange(len(el[2].objects)):
                    if (el[1][1] + el[2].objects[r][1][1][3] - s.start) <= 15 : 
                        continue
                    if (el[1][1] + el[2].objects[r][1][1][1] - s.start) >= s.h : 
                        break
                    for c in xrange(len(el[2].objects[r])):
                        e = el[2].objects[r][c]
                        if e[0] == 'text' : 
                            t = e[2]
                            for j in xrange(len(t)):
                                s.img.text(((el[2].x + 2) + t[j][0][0], (el[1][1] + t[j][0][1] - s.start)), t[j][1], e[3], e[4])
                            pass
                        if e[0] == 'link' : 
                            if el[2].fl == None : 
                                el[2].fl = [c, r]
                            if el[2].cur_pos == [0, 0] : 
                                el[2].cur_pos = el[2].fl
                            el[2].ll = [c, r]
                            if r == el[2].cur_pos[1] and c < el[2].cur_pos[0] : 
                                el[2].pl = [c, r]
                            if r == el[2].cur_pos[1] and c > el[2].cur_pos[0] and el[2].nl == None : 
                                el[2].nl = [c, r]
                            if r < el[2].cur_pos[1] : 
                                el[2].pfl = [c, r]
                            if (r + 1) == el[2].cur_pos[1] : 
                                el[2].pll = [c, r]
                            if (r - 1) == el[2].cur_pos[1] and el[2].nfl == None : 
                                el[2].nfl = [c, r]
                            if r > el[2].cur_pos[1] and el[2].nll == None : 
                                el[2].nll = [c, r]
                            elif (r + 1) == el[2].cur_pos[1] and c == el[2].cur_pos[0] : 
                                el[2].ul = [c, r]
                            elif (r - 1) == el[2].cur_pos[1] and c == el[2].cur_pos[0] : 
                                el[2].dl = [c, r]
                            t = e[2]
                            if i == s.cur_pos and c == el[2].cur_pos[0] and r == el[2].cur_pos[1] : 
                                s.img.rectangle(((e[1][0] + el[2].x + 1), (e[1][1] - s.start) + el[1][1], (e[1][2] + el[2].x - 1), ((e[1][3] - s.start) + el[1][1] - 1)), s.cur_color[0], s.cur_color[1])
                            for j in xrange(len(t)):
                                s.img.text(((el[2].x + 2) + t[j][0][0], (el[1][1] + t[j][0][1] - s.start)), t[j][1], e[3], e[4])
                            pass
                        if e[0] == 'image' : 
                            s.img.blit(e[2], target = ((e[1][0] + el[2].x + 2), ((e[1][1] + el[1][1] + 2) - s.start)), mask = e[3])
                        if e[0] == 'glink' : 
                            if el[2].fl == None : 
                                el[2].fl = [c, r]
                            if el[2].cur_pos == [0, 0] : 
                                el[2].cur_pos = el[2].fl
                            el[2].ll = [c, r]
                            if r == el[2].cur_pos[1] and c < el[2].cur_pos[0] : 
                                el[2].pl = [c, r]
                            if r == el[2].cur_pos[1] and c > el[2].cur_pos[0] and el[2].nl == None : 
                                el[2].nl = [c, r]
                            if r < el[2].cur_pos[1] : 
                                el[2].pfl = [c, r]
                            if (r + 1) == el[2].cur_pos[1] : 
                                el[2].pll = [c, r]
                            if (r - 1) == el[2].cur_pos[1] and el[2].nfl == None : 
                                el[2].nfl = [c, r]
                            if r > el[2].cur_pos[1] and el[2].nll == None : 
                                el[2].nll = [c, r]
                            elif (r + 1) == el[2].cur_pos[1] and c == el[2].cur_pos[0] : 
                                el[2].ul = [c, r]
                            elif (r - 1) == el[2].cur_pos[1] and c == el[2].cur_pos[0] : 
                                el[2].dl = [c, r]
                            s.img.blit(e[2], target = ((e[1][0] + el[2].x + 2), ((e[1][1] + el[1][1] + 2) - s.start)), mask = e[3])
                            if i == s.cur_pos and c == el[2].cur_pos[0] and r == el[2].cur_pos[1] : 
                                s.img.rectangle(((e[1][0] + el[2].x + 3), ((e[1][1] - s.start) + el[1][1] + 2), (e[1][2] + el[2].x - 3), ((e[1][3] - s.start) + el[1][1] - 3)), s.cur_color[0])
                            pass
                pass
            elif el[0] == 'text' : 
                for i in xrange(len(el[2])):
                    s.img.text((el[2][i][0][0], (el[2][i][0][1] - s.start)), el[2][i][1], el[3], el[4])
                pass
            elif el[0] == 'link' : 
                if  not (s.fl) : 
                    s.fl = i
                s.ll = i
                if i < s.cur_pos : 
                    s.pl = i
                elif s.nl == None and i > s.cur_pos : 
                    s.nl = i
                elif i == s.cur_pos : 
                    s.img.rectangle((el[1][0], (el[1][1] - s.start), el[1][2], (el[1][3] - s.start)), s.cur_color[0], s.cur_color[1])
                for i in xrange(len(el[2])):
                    s.img.text((el[2][i][0][0], (el[2][i][0][1] - s.start)), el[2][i][1], el[3], el[4])
                pass
            elif el[0] == 'image' : 
                s.img.blit(el[2], target = (el[1][0], (el[1][1] - s.start)), mask = el[3])
            elif el[0] == 'glink' : 
                if  not (s.fl) : 
                    s.fl = i
                s.ll = i
                if i < s.cur_pos : 
                    s.pl = i
                elif i > s.cur_pos and s.nl == None : 
                    s.nl = i
                s.img.blit(el[2], target = (el[1][0], (el[1][1] - s.start)), mask = el[3])
                if i == s.cur_pos : 
                    s.img.rectangle((el[1][0], (el[1][1] - s.start), el[1][2], (el[1][3] - s.start)), s.cur_color[0])
                pass
        s.top_line()
        s.scroll_bar()
        if s.status == 'screen' and len(history['window']) > 0 : 
            obj = history['window'][(len(history['window']) - 1)]
            if obj.timeout : 
                if obj.timeout <= time.clock() : 
                    hide(obj)
                    return None
                pass
            obj.paint()
            s.img.blit(obj.img, target = (obj.x, obj.y))
            s.img.rectangle((obj.x + obj.w, (obj.y + 4), (obj.x + obj.w + 4), (obj.y + obj.h + 4)), 6316128, 6316128)
            s.img.rectangle(((obj.x + 4), obj.y + obj.h, (obj.x + obj.w + 4), (obj.y + obj.h + 4)), 6316128, 6316128)
            if obj == inp : 
                s.img.rectangle((0, (s.h - 15), s.w, s.h), s.color[1], s.color[1])
                s.img.text((5, (s.h - 3)), dec('复制副本'), 15658624, u'')
                s.img.text((((s.w / 2) - 5), (s.h - 3)), dec('ok'), 15658624, u'')
                s.img.text(((s.w - 50), (s.h - 3)), dec('插入'), 15658624, u'')
            obj.shad = 1
        elif s.status == 'screen' and len(history['menu']) > 0 : 
            obj = history['menu'][(len(history['menu']) - 1)]
            obj.paint()
            s.img.blit(obj.img, target = (obj.x, obj.y))
            s.img.rectangle((obj.x + obj.w, (obj.y + 4), (obj.x + obj.w + 4), (obj.y + obj.h + 4)), 6316128, 6316128)
            s.img.rectangle(((obj.x + 4), obj.y + obj.h, (obj.x + obj.w + 4), (obj.y + obj.h + 4)), 6316128, 6316128)
            obj.shad = 1
        else : 
            obj = None
        if s.status == 'screen' : 
            handle_redraw(())






class Window(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.x, s.y, s.w, s.h = (5, 30, (w - 10), 100)
        s.bg = None
        s.mask = None
        s.timeout = None
        s.img = graphics.Image.new((s.w, s.h))
        s.color = [15658734, 8388608]
        s.text_color = 0
        s.link_color = 128
        s.title_color = 16768426
        s.text_font = u''
        s.link_font = u''
        s.title_font = u''
        s.cur_color = [11184810, 13421772]
        s.status = 'window'
        s.cur_status = 'w'
        s.cur_pos = 0
        s.mar = 15
        s.start = 0
        s.pos = 0
        s.ty = 20
        s.objects = []
        s.title = 'wif-window'
        s.funcs = []
        s.exit = lambda  : hide('window') 
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = s.cur_left
        s.funcs[15] = s.cur_right
        s.funcs[16] = s.cur_up
        s.funcs[17] = s.cur_down
        s.funcs[18] = p
        s.funcs[42] = s.scroll_up
        s.funcs[48] = p
        s.funcs[49] = p
        s.funcs[50] = p
        s.funcs[51] = p
        s.funcs[52] = p
        s.funcs[53] = p
        s.funcs[54] = p
        s.funcs[55] = p
        s.funcs[56] = p
        s.funcs[57] = p
        s.funcs[127] = s.scroll_down
        s.funcs[164] = lambda  : hide('window') 
        s.funcs[167] = lambda  : hide('window') 
        s.funcs[196] = lambda  : screenshot() 
        s.gh = ((s.h - s.mar) - 2)
        s.ttx = 5
        s.shad = 0






class Menu(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.x, s.y, s.w, s.h = (1, 16, 110, 190)
        s.bg = None
        s.mask = None
        s.img = graphics.Image.new((s.w, s.h))
        s.color = [15658734, 8388608]
        s.text_color = 0
        s.link_color = 128
        s.title_color = 16768426
        s.text_font = u''
        s.link_font = u''
        s.title_font = u''
        s.cur_color = [11184810, 13421772]
        s.status = 'menu'
        s.cur_status = 'w'
        s.cur_pos = 0
        s.mar = 15
        s.start = 0
        s.pos = 0
        s.ty = 20
        s.objects = []
        s.title = 'wif-menu'
        s.exit = lambda  : hide('menu') 
        s.funcs = []
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = s.cur_left
        s.funcs[15] = s.cur_right
        s.funcs[16] = s.cur_up
        s.funcs[17] = s.cur_down
        s.funcs[18] = p
        s.funcs[42] = s.scroll_up
        s.funcs[48] = p
        s.funcs[49] = p
        s.funcs[50] = p
        s.funcs[51] = p
        s.funcs[52] = p
        s.funcs[53] = p
        s.funcs[54] = p
        s.funcs[55] = p
        s.funcs[56] = p
        s.funcs[57] = p
        s.funcs[127] = s.scroll_down
        s.funcs[164] = s.select
        s.funcs[167] = s.select
        s.funcs[196] = lambda  : screenshot() 
        s.gh = ((s.h - s.mar) - 2)
        s.ttx = 5
        s.shad = 0






class Confirm(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.x, s.y, s.w, s.h = (5, 50, (w - 10), 80)
        s.bg = None
        s.mask = None
        s.timeout = None
        s.img = graphics.Image.new((s.w, s.h))
        s.color = [15658734, 8388608]
        s.text_color = 0
        s.link_color = 128
        s.title_color = 16768426
        s.text_font = u''
        s.link_font = u''
        s.title_font = u''
        s.cur_color = [11184810, 13421772]
        s.status = 'window'
        s.cur_status = 'w'
        s.cur_pos = 0
        s.mar = 15
        s.start = 0
        s.pos = 0
        s.ty = 20
        s.objects = []
        s.title = 'wif-confirm'
        s.funcs = []
        s.exit = lambda  :  s.cancel() 
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = s.cur_left
        s.funcs[15] = s.cur_right
        s.funcs[16] = s.cur_up
        s.funcs[17] = s.cur_down
        s.funcs[18] = p
        s.funcs[42] = p
        s.funcs[48] = p
        s.funcs[49] = p
        s.funcs[50] = p
        s.funcs[51] = p
        s.funcs[52] = p
        s.funcs[53] = p
        s.funcs[54] = p
        s.funcs[55] = p
        s.funcs[56] = p
        s.funcs[57] = p
        s.funcs[127] = p
        s.funcs[164] = lambda  :  s.ok() 
        s.funcs[167] = lambda  :  s.no() 
        s.funcs[196] = lambda  : screenshot() 
        s.gh = ((s.h - s.mar) - 2)
        s.ttx = 5
        s.result = None
        s.cur = 0
        s.shad = 0




    def ok(s):
        s.result = 'ok'
        signal()




    def no(s):
        s.result = 'no'
        signal()




    def cancel(s):
        s.result = 'cancel'
        signal()




    def top_line(s):
        s.img.rectangle((0, 0, s.w, s.mar), 0, s.color[1])
        s.img.text((5, (s.mar - 2)), dec(s.title), s.title_color, font = s.title_font)
        s.img.rectangle((2, (s.h - 17), (s.w - 2), (s.h - 2)), 0)
        s.img.text(((round(((s.w - 4) / 2)) - 5), (s.h - 4)), dec('否'), 0, u'')
        s.img.text(((s.w - 50), (s.h - 4)), dec('返回'), 0, u'')
        s.img.text((10, (s.h - 4)), dec('是'), 0, u'')






class Input(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.timeout = None
        s.eng = ([dec(' 0\\@()<>[]{}#'), dec('.,?!:;\'"=-+/*1'), dec('ABC2'), dec('DEF3'), dec('GHI4'), dec('JKL5'), dec('MNO6'), dec('PQRS7'), dec('TUV8'), dec('WXYZ9')], [dec(' 0\\@()<>[]{}#'), dec('.,?!:;\'"=-+/*1'), dec('abc2'), dec('def3'), dec('ghi4'), dec('jkl5'), dec('mno6'), dec('pqrs7'), dec('tuv8'), dec('wxyz9')])
        s.rus = ([dec(' 0\\@()<>[]{}#'), dec('.,?!:;\'"=-+/*1'), dec('АБВГ2'), dec('ДЕЖЗ3'), dec('ИЙКЛ4'), dec('МНОП5'), dec('РСТУ6'), dec('ФХЦЧ7'), dec('ШЩЪЫ8'), dec('ЬЭЮЯ9')], [dec(' 0\\@()<>[]{}#'), dec('.,?!:;\'"=-+/*1'), dec('абвг2'), dec('дежз3'), dec('ийкл4'), dec('мноп5'), dec('рсту6'), dec('фхцч7'), dec('шщъы8'), dec('ьэюя9')])
        s.num = ([dec('0'), dec('1'), dec('2'), dec('3'), dec('4'), dec('5'), dec('6'), dec('7'), dec('8'), dec('9')], [dec('0'), dec('1'), dec('2'), dec('3'), dec('4'), dec('5'), dec('6'), dec('7'), dec('8'), dec('9')])
        s.liter = [s.eng, s.rus, s.num]
        s.lang = 0
        s.act = 0
        s.color = [16777215, 128]
        s.text_color = 0
        s.title_color = 16768426
        s.text_font = u''
        s.title_font = u''
        s.cur_color = 255
        s.status = 'window'
        s.title = '返回'
        s.funcs = []
        s.exit = lambda  :  s.insert() 
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = lambda  :  s.key('c') 
        s.funcs[14] = lambda  :  s.cur_left() 
        s.funcs[15] = lambda  :  s.cur_right() 
        s.funcs[16] = lambda  :  s.cur_up() 
        s.funcs[17] = lambda  :  s.cur_down() 
        s.funcs[18] = lambda  :  s.key('abc') 
        s.funcs[42] = lambda  :  s.key('star') 
        s.funcs[48] = lambda  :  s.key(0) 
        s.funcs[49] = lambda  :  s.key(1) 
        s.funcs[50] = lambda  :  s.key(2) 
        s.funcs[51] = lambda  :  s.key(3) 
        s.funcs[52] = lambda  :  s.key(4) 
        s.funcs[53] = lambda  :  s.key(5) 
        s.funcs[54] = lambda  :  s.key(6) 
        s.funcs[55] = lambda  :  s.key(7) 
        s.funcs[56] = lambda  :  s.key(8) 
        s.funcs[57] = lambda  :  s.key(9) 
        s.funcs[127] = lambda  :  s.key('hash') 
        s.funcs[164] = lambda  :  s.copy() 
        s.funcs[167] = lambda  :  s.key('select')
        s.funcs[196] = lambda  : screenshot() 
        s.text = u''
        s.txt = []
        s.img = graphics.Image.new((176, 208))
        s.th = ((s.img.measure_text(u'A', font = s.text_font)[0][1] * -1) + 3)
        s.x, s.y, s.w, s.h = (5, (((h - 20) - s.th) - 30), (w - 10), (s.th + 30))
        s.img = graphics.Image.new((s.w, s.h))
        s.pos = 0
        s.cur_pos = 0
        s.ltime = 0
        s.lkey = 20
        s.ptime = 0
        s.pkey = 0
        s.max = 1024
        s.start = 0
        s.gh = s.th
        s.rows = 1
        s.lcx = 3
        s.lcy = 27




    def copy(s):
        clipboard.Set(s.text)




    def insert(s):
        buf = clipboard.Get()
        s.text = s.text[0 : s.cur_pos] + buf + s.text[s.cur_pos : ]
        s.cur_pos += len(buf)




    def key(s, k):
        s.pkey = k
        s.ptime = time.clock()
        if s.pkey == 'abc' : 
            s.pos = 0
            s.ltime = 0
            s.lkey = 20
            if s.lang < (len(s.liter) - 1) : 
                s.lang += 1
            else : 
                s.lang = 0
            if s.max <= len(s.text) : 
                return None
            return None
        elif s.pkey == 'c' : 
            if s.cur_pos == 0 : 
                return None
            s.cur_pos -= 1
            s.text = s.text[0 : s.cur_pos] + s.text[(s.cur_pos + 1) : ]
            s.ltime = 0
            s.lkey = 20
            s.paint()
            s.start = (len(s.txt) - s.rows)
            if s.start < 0 : 
                s.start = 0
            s.resize()
            return None
        elif s.pkey == 'hash' : 
            if s.act < (len(s.liter[s.lang]) - 1) : 
                s.act += 1
            else : 
                s.act = 0
            s.pos = 0
            s.ltime = 0
            s.lkey = 20
            return None
        elif s.pkey == 'star' : 
            s.ltime = 0
            s.lkey = 20
            return None
        elif s.pkey == 'select' : 
            signal()
            return None
        if s.max == len(s.text) and s.ltime < (s.ptime - time.clock()) : 
            return None
        try :
            a = int(s.pkey)
        except :
            return None
        if s.h >= (h - 10) and s.lcx >= (s.w - 15) and s.lcy >= (s.h - 32) : 
            s.start += 1
        if (s.ptime - 1.5) < s.ltime and s.pkey == s.lkey : 
            s.pos += 1
            if s.pos > (len(s.liter[s.lang][s.act][s.pkey]) - 1) : 
                s.pos = 0
            s.cur_pos -= 1
            s.text = s.text[0 : s.cur_pos] + s.text[(s.cur_pos + 1) : ]
            s.text = s.text[0 : s.cur_pos] + s.liter[s.lang][s.act][s.pkey][s.pos] + s.text[s.cur_pos : ]
        else : 
            s.pos = 0
            s.text = s.text[0 : s.cur_pos] + s.liter[s.lang][s.act][s.pkey][s.pos] + s.text[s.cur_pos : ]
        s.cur_pos += 1
        s.lkey = s.pkey
        s.ltime = s.ptime
        if s.lang == 2 : 
            s.lkey = 20




    def cur_up(s):
        if s.start > 0 : 
            s.start -= 1




    def cur_down(s):
        if s.start + s.rows < len(s.txt) : 
            s.start += 1




    def cur_left(s):
        if s.cur_pos > 0 : 
            s.cur_pos -= 1




    def cur_right(s):
        if s.cur_pos < len(s.text) : 
            s.cur_pos += 1




    def resize(s):
        if s.h < (h - 25) or len(s.txt) < s.rows : 
            s.h = ((len(s.txt) * s.th) + 30)
            s.y = ((h - s.h) - 20)
            s.rows = round(((s.h - 30) / s.th))
            s.img = graphics.Image.new((s.w, s.h))




    def paint(s):
        appuifw.app.exit_key_handler = s.exit
        s.txt = []
        t = s.text[0 : s.cur_pos] + u'|' + s.text[s.cur_pos : ]
        while len(t) > 0 : 
            ind = s.img.measure_text(t, font = s.text_font, maxwidth = (s.w - 10))[2]
            s.txt.append(t[0 : ind])
            t = t[ind : ]
        if len(s.txt) > s.rows : 
            s.resize()
        s.img.clear(s.color[0])
        s.img.rectangle((0, 0, s.w, s.h), 0)
        s.img.rectangle((0, 0, s.w, 15), 0, s.color[1])
        for i in xrange(s.start, len(s.txt)):
            s.lcx = s.img.measure_text(s.txt[i], font = s.text_font)[1]
            s.lcy = (((15 + s.th) + (i * s.th) - 2) - (s.start * s.th))
            s.img.text((5, s.lcy), s.txt[i], s.text_color, s.text_font)
            try :
                ind = s.txt[i].index(u'|')
                cm = (s.img.measure_text(s.txt[i][0 : ind], font = s.text_font)[1] + 5)
                if (time.clock() - 1.5) < s.ltime : 
                    col = 14483456
                else : 
                    col = 221
                s.img.rectangle((cm, (s.lcy - 10), (cm + 3), (s.lcy + 2)), col, col)
            except :
                pass
        s.img.rectangle((0, (s.h - 15), s.w, s.h), 0, s.color[1])
        s.img.text((5, 12), dec(s.title), s.title_color, s.title_font)
        temp = s.liter[s.lang][s.act][2]
        if len(temp) > 3 : 
            temp = temp[0 : 3]
        s.img.rectangle(((s.w - 30), (s.h - 14), (s.w - 1), (s.h - 1)), 16777120, 16777120)
        s.img.text(((s.w - 25), (s.h - 3)), dec(temp), 0, font = u'')
        s.img.rectangle(((s.w - 30), 1, (s.w - 1), 14), 16777120, 16777120)
        s.img.text(((s.w - 27), 12), str((s.max - len(s.text))).decode('utf-8'), 0)
        try :
            if (s.ltime + 1.5) > time.clock() : 
                s.img.rectangle(((5 + (s.pos * 8)), (s.h - 14), (5 + (s.pos * 8) + 8), (s.h - 1)), 41120, fill = 41120)
                for i in xrange(len(s.liter[s.lang][s.act][s.pkey])):
                    s.img.text(((7 + (i * 8)), (s.h - 2)), s.liter[s.lang][s.act][s.pkey][i], s.title_color, font = u'')
                pass
        except :
            pass






class Input_time(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.objects = ['input']
        s.timeout = None
        s.color = [16777215, 128]
        s.text_color = 0
        s.title_color = 16768426
        s.text_font = u''
        s.title_font = u''
        s.cur_color = 12303291
        s.status = 'window'
        s.title = '返回'
        s.funcs = []
        s.exit = lambda  : hide('menu') 
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = p
        s.funcs[15] = p
        s.funcs[16] = p
        s.funcs[17] = p
        s.funcs[18] = p
        s.funcs[42] = p
        s.funcs[48] = lambda  :  s.key(0) 
        s.funcs[49] = lambda  :  s.key(1) 
        s.funcs[50] = lambda  :  s.key(2) 
        s.funcs[51] = lambda  :  s.key(3) 
        s.funcs[52] = lambda  :  s.key(4) 
        s.funcs[53] = lambda  :  s.key(5) 
        s.funcs[54] = lambda  :  s.key(6) 
        s.funcs[55] = lambda  :  s.key(7) 
        s.funcs[56] = lambda  :  s.key(8) 
        s.funcs[57] = lambda  :  s.key(9) 
        s.funcs[127] = p
        s.funcs[164] = p
        s.funcs[167] = lambda  :  s.key('select') 
        s.funcs[196] = lambda  : screenshot() 
        s.text = [dec('0'), dec('0'), dec('.'), dec('0'), dec('0')]
        s.x, s.y, s.w, s.h = (10, 120, (w - 20), 55)
        s.img = graphics.Image.new((s.w, s.h))
        s.cur_pos = 0
        s.tw = 50
        s.tx = round(((s.w - s.tw) / 2))




    def key(s, k):
        if k == 'select' : 
            signal()
            return None
        if s.cur_pos == 0 : 
            if k > 2 : 
                return None
            pass
        elif s.cur_pos == 1 : 
            if s.text[0] == dec('2') : 
                if k > 3 : 
                    return None
                pass
            pass
        elif s.cur_pos == 3 : 
            if k > 5 : 
                return None
            pass
        s.text[s.cur_pos] = dec(str(k))
        s.cur_pos += 1
        if s.cur_pos == 2 : 
            s.cur_pos = 3
        if s.cur_pos == 5 : 
            s.cur_pos = 0




    def cur_up(s):
        pass




    def cur_down(s):
        pass




    def cur_left(s):
        pass




    def cur_rigit(s):
        pass




    def paint(s):
        s.img.clear(s.color[0])
        s.img.rectangle((0, 0, s.w, s.h), 0)
        s.img.rectangle((0, 0, s.w, 15), 0, s.color[1])
        s.img.text((5, 12), s.title.decode('utf-8'), s.title_color, s.title_font)
        for i in xrange(len(s.text)):
            if i == s.cur_pos : 
                s.img.rectangle((s.tx + (i * 10), (s.h - 38), (s.tx + 10) + (i * 10), (s.h - 2)), 0, s.cur_color)
            s.img.text((s.tx + (i * 10), (s.h - 5)), s.text[i], s.text_color, s.text_font)






class Input_date(Screen, ) :


    __module__ = __name__
    def __init__(s):
        s.objects = ['input']
        s.timeout = None
        s.color = [16777215, 128]
        s.text_color = 0
        s.title_color = 16768426
        s.text_font = u''
        s.title_font = u''
        s.cur_color = 12303291
        s.status = 'window'
        s.title = '输入'
        s.funcs = []
        s.exit = lambda  : hide('menu') 
        for i in xrange(0, 200):
            s.funcs.append(p)
        s.funcs[1] = p
        s.funcs[14] = p
        s.funcs[15] = p
        s.funcs[16] = p
        s.funcs[17] = p
        s.funcs[18] = p
        s.funcs[42] = p
        s.funcs[48] = lambda  :  s.key(0) 
        s.funcs[49] = lambda  :  s.key(1) 
        s.funcs[50] = lambda  :  s.key(2) 
        s.funcs[51] = lambda  :  s.key(3) 
        s.funcs[52] = lambda  :  s.key(4) 
        s.funcs[53] = lambda  :  s.key(5) 
        s.funcs[54] = lambda  :  s.key(6) 
        s.funcs[55] = lambda  :  s.key(7) 
        s.funcs[56] = lambda  :  s.key(8) 
        s.funcs[57] = lambda  :  s.key(9) 
        s.funcs[127] = p
        s.funcs[164] = p
        s.funcs[167] = lambda  :  s.key('select') 
        s.funcs[196] = lambda  : screenshot() 
        s.text = [dec('0'), dec('0'), dec('.'), dec('0'), dec('0'), dec('.'), dec('0'), dec('0'), dec('0'), dec('0')]
        s.x, s.y, s.w, s.h = (10, 120, (w - 20), 55)
        s.img = graphics.Image.new((s.w, s.h))
        s.cur_pos = 0
        s.tw = 100
        s.tx = round(((s.w - s.tw) / 2))




    def cur_up(s):
        pass




    def cur_down(s):
        pass




    def cur_left(s):
        pass




    def cur_rigit(s):
        pass




    def key(s, k):
        if k == 'select' : 
            signal()
            return None
        if s.cur_pos == 0 : 
            if k > 3 : 
                return None
            pass
        elif s.cur_pos == 1 : 
            if s.text[0] == dec('3') : 
                if k > 1 : 
                    return None
                pass
            if s.text[0] == dec('0') : 
                if k == 0 : 
                    return None
                pass
            pass
        elif s.cur_pos == 3 : 
            if k > 1 : 
                return None
            pass
        elif s.cur_pos == 4 : 
            if s.text[3] == dec('1') : 
                if k > 2 : 
                    return None
                pass
            if s.text[3] == dec('0') : 
                if k == 0 : 
                    return None
                pass
            pass
        s.text[s.cur_pos] = dec(str(k))
        s.cur_pos += 1
        if s.cur_pos == 2 : 
            s.cur_pos = 3
        if s.cur_pos == 5 : 
            s.cur_pos = 6
        if s.cur_pos == 10 : 
            s.cur_pos = 0




    def paint(s):
        s.img.clear(s.color[0])
        s.img.rectangle((0, 0, s.w, s.h), 0)
        s.img.rectangle((0, 0, s.w, 15), 0, s.color[1])
        s.img.text((5, 12), s.title.decode('utf-8'), s.title_color, s.title_font)
        for i in xrange(len(s.text)):
            if i == s.cur_pos : 
                s.img.rectangle((s.tx + (i * 10), (s.h - 38), (s.tx + 10) + (i * 10), (s.h - 2)), 0, s.cur_color)
            s.img.text((s.tx + (i * 10), (s.h - 5)), s.text[i], s.text_color, s.text_font)






class Fill(object):


    __module__ = __name__
    def __init__(s):
        s.x, s.y, s.w, s.h = (10, 80, 156, 40)
        s.img = graphics.Image.new((s.w, s.h))
        #不是很确定翻译是否正确
        s.title = '进度条'
        s.f = [u'', u'']
        s.color = [0x555555, 0x111111]




    def paint(s, n, o):
        per = float((round((((100 * float(n)) / float(o)) * 100)) / 100))
        s.img.rectangle((0, 0, s.w, s.h), 0, s.color[0])
        s.img.rectangle((0, 0, s.w, 15), 0, s.color[1])
        s.img.rectangle(((s.w - 102), (s.h - 38), (s.w - 2), (s.h - 2)), 0)
        s.img.rectangle(((s.w - 102), (s.h - 38), (s.w - 102) + per, (s.h - 2)), 0, 0xff0000)
        s.img.text((5, 12), s.title.decode('utf-8'), 0x333333, font = s.f[0])
        app.img.rectangle((s.x + s.w, (s.y + 4), (s.x + s.w + 4), (s.y + s.h + 4)), 0x999999, 0x999999)
        app.img.rectangle(((s.x + 4), s.y + s.h, (s.x + s.w + 4), (s.y + s.h + 4)), 0x999999, 0x999999)
        app.img.blit(s.img, target = (s.x, s.y))
        app.img.text(((s.x + 10), (s.y + s.h - 5)), str(per).decode('utf-8'), 0, font = s.f[1])
        handle_redraw(())






class Table(object, ) :


    __module__ = __name__
    def __init__(s, cols):
        s.cols = cols
        s.rows = []
        s.x = 5
        s.y = 0
        s.h = 0
        s.w = 0
        for i in xrange(len(s.cols)):
            s.w += s.cols[i]
        s.objects = []
        s.text_color = 0
        s.link_color = 238
        s.font = u''
        s.ty = 0
        s.line_color = 0x0
        s.bg_color = None
        s.border_color = None
        s.cur_pos = [0, 0]




    def clear(s):
        s.rows = []
        s.x = 5
        s.y = 0
        s.h = 0
        s.objects = []
        s.ty = 0
        s.cur_pos = [0, 0]




    def row(s, r):
        rh = 0
        maxh = 0
        tempx = 0
        buf = []
        for i in xrange(len(r)):
            e = r[i]
            if e[0] == 'text' : 
                if len(e) == 4 : 
                    font, color = (e[3], e[2])
                elif len(e) == 3 : 
                    font, color = (s.font, e[2])
                elif len(e) == 2 : 
                    font, color = (s.font, s.text_color)
                h = ((app.img.measure_text(u'A', font)[0][1] * -1) + 2)
                t = []
                k = 0
                text = dec(e[1])
                while len(text) > 0 : 
                    ind = app.img.measure_text(text, font, maxwidth = (s.cols[i] - 5))[2]
                    cor = ((tempx + 2), s.ty + h + (h * k))
                    t.append((cor, text[0 : ind]))
                    k += 1
                    text = text[ind : ]
                rh = ((h * len(t)) + 2)
                if maxh < rh : 
                    maxh = rh
                cor = [tempx, s.ty, tempx + s.cols[i], s.ty + rh]
                buf.append(('text', cor, t, color, font))
                tempx += s.cols[i]
            if e[0] == 'link' : 
                if len(e) == 5 : 
                    font, color = (e[4], e[3])
                elif len(e) == 4 : 
                    font, color = (s.font, e[3])
                elif len(e) == 3 : 
                    font, color = (s.font, s.link_color)
                h = ((app.img.measure_text(u'A', font)[0][1] * -1) + 2)
                t = []
                k = 0
                text = dec(e[1])
                func = e[2]
                while len(text) > 0 : 
                    ind = app.img.measure_text(text, font, maxwidth = (s.cols[i] - 5))[2]
                    cor = ((tempx + 2), s.ty + h + (h * k))
                    t.append((cor, text[0 : ind]))
                    k += 1
                    text = text[ind : ]
                rh = ((h * len(t)) + 2)
                if maxh < rh : 
                    maxh = rh
                cor = [tempx, s.ty, tempx + s.cols[i], s.ty + rh]
                buf.append(('link', cor, t, color, font, func))
                tempx += s.cols[i]
            if e[0] == 'image' : 
                h = (e[1].size[1] + 4)
                w = (e[1].size[0] + 4)
                if maxh < h : 
                    maxh = h
                cor = [tempx, s.ty, tempx + s.cols[i], s.ty + rh]
                buf.append(('image', cor, e[1], e[2]))
                tempx += s.cols[i]
            if e[0] == 'glink' : 
                h = (e[1].size[1] + 4)
                w = (e[1].size[0] + 4)
                if maxh < h : 
                    maxh = h
                cor = [tempx, s.ty, tempx + s.cols[i], s.ty + rh]
                buf.append(('glink', cor, e[1], e[2], e[3]))
                tempx += s.cols[i]
        for j in xrange(len(buf)):
            buf[j][1][3] = s.ty + maxh
        s.objects.append(buf)
        s.ty += maxh
        s.rows.append(maxh)






class Checkbox(object, ) :


    __module__ = __name__
    def __init__(s, type = 'multicheck'):
        s.type = type
        s.font = u''
        s.color = 0
        s.check_color = 0
        s.objects = []
        s.checked = []
        s.cur_pos = 0
        s.check_size = 12
        s.cx = 5
        s.tx = 22
        s.ty = 0
        s.h = 0




    def clear(s):
        s.objects = []
        s.checked = []
        s.cur_pos = 0
        s.ty = 0
        s.h = 0




    def row(s, r):
        try :
            text = dec(r)
        except :
            text = r
        s.check_size = (app.img.measure_text(u'A', s.font)[0][1] * -1)
        mh = (s.check_size + 3)
        s.tx = (s.cx + s.check_size + 5)
        tt = []
        k = 0
        while len(text) > 0 : 
            ind = app.img.measure_text(text, s.font, maxwidth = ((w - s.tx) - 7))[2]
            cor = (s.tx, s.ty + mh + (k * mh))
            tt.append((cor, text[0 : ind]))
            text = text[ind : ]
            k += 1
        oh = (mh * len(tt))
        s.ty += oh
        s.objects.append((((s.ty - oh), s.ty), tt))
        s.checked.append(0)
        return (len(s.objects) - 1)






app = None
history = {}
history['screen'] = []
history['window'] = []
history['menu'] = []
run = 0
def wait():
    global run
    run = 1
    while run : 
        app.paint()
        e32.ao_yield()
        lock.wait()
        while len(kb.d) > 0 : 
            f = kb.key()
            if f:
                if len(history['window']) > 0 : 
                    obj = history['window'][-1]
                    obj.funcs[f]()
                elif len(history['menu']) > 0 : 
                    obj = history['menu'][-1]
                    obj.funcs[f]()
                else : 
                    obj = None
                    app.funcs[f]()
                pass
            app.paint()
            #e32.ao_yield()
            e32.ao_sleep(0.1)




def signal():
    global run
    run = 0




def show(o):
    global app
    if o.status == 'screen' : 
        history['menu'] = []
        history['window'] = []
    history[o.status].append(o)
    if o.status != 'screen' : 
        if app.rot == None : 
            o.funcs[14] = o.cur_left
            o.funcs[15] = o.cur_right
            o.funcs[16] = o.cur_up
            o.funcs[17] = o.cur_down
        elif app.rot == graphics.ROTATE_90 : 
            o.funcs[14] = o.cur_up
            o.funcs[15] = o.cur_down
            o.funcs[16] = o.cur_right
            o.funcs[17] = o.cur_left
        elif app.rot == graphics.ROTATE_180 : 
            o.funcs[14] = o.cur_right
            o.funcs[15] = o.cur_left
            o.funcs[16] = o.cur_down
            o.funcs[17] = o.cur_up
        elif app.rot == graphics.ROTATE_270 : 
            o.funcs[14] = o.cur_down
            o.funcs[15] = o.cur_up
            o.funcs[16] = o.cur_left
            o.funcs[17] = o.cur_right
        pass
    app=history['screen'][-1]
    e32.ao_yield()



hide_funcsx=None
def funcsx(func):
    """hide每次退出刷新页面"""
    global hide_funcsx
    hide_funcsx=func


def hide(o = None,func=None):
    global app,hide_funcsx
    if o:
        if o == 'menu' : 
            history['menu'] = []
        elif o == 'window' : 
            history['window'] = []
        else:
            try:
                del history[o.status][history[o.status].index(o)]
            except:
                pass
    else : 
        history['menu'] = []
        history['window'] = []
        if len(history['screen'])>1:
            history['screen'].pop()
        else:
            e32.ao_sleep(0.1)
            #pdexit=confirm('你确定要退出？')
            
            if (not func) and (not hide_funcsx):
                pdexit=appuifw.query(dec("你确定要退出？"),"query")
            else:
                pdexit=0
            if pdexit==1:
                abort()
    app=history['screen'][-1]
    if not func:
        if hide_funcsx:
            func=hide_funcsx
    if func and (not o):
        hide_funcsx=None
        if type(func)==type([]):
            for na in func:
                na()
        elif type(func)==type(hide):
            func()
        else:
            pass


def confirm(t, title='询问'):
    global run
    conf=Confirm()
    conf.result = None
    conf.clear()
    conf.text(t, align = 'center')
    conf.title = title
    show(conf)
    wait()
    run = 1
    hide('window')
    return conf.result




win = Window()
def note(t, title = '信息', timeout = None):
    if timeout : 
        win.timeout = timeout + time.clock()
    else : 
        win.timeout = None
    win.clear()
    win.color = [13421772, 238]
    win.text_color = 0
    win.title_color = 13421772
    win.title = title
    win.text(t, align = 'center')
    show(win)
    wait()
    run = 1




def warning(t, title = '警告', timeout = None):
    if timeout : 
        win.timeout = timeout + time.clock()
    else : 
        win.timeout = None
    win.clear()
    win.color = [13421772, 15658496]
    win.text_color = 0
    win.title_color = 0
    win.title = title
    win.text(t, align = 'center')
    show(win)
    wait()
    run = 1




def error(t, title = '错误', timeout = None):
    if timeout : 
        win.timeout = timeout + time.clock()
    else : 
        win.timeout = None
    win.clear()
    win.color = [13421772, 15597568]
    win.text_color = 0
    win.title_color = 13421772
    win.title = title
    win.text(t, align = 'center')
    show(win)
    wait()
    run = 1




inp = Input()
def input(text = '', title = 'Ввод', mode = 'рус', max = 1024):
    global run
    inp.text = text
    inp.cur_pos = len(text)
    inp.title = title
    inp.max = max
    if mode == 'рус' : 
        inp.lang = 1
        inp.act = 1
    if mode == 'РУС' : 
        inp.lang = 1
        inp.act = 0
    if mode == 'eng' : 
        inp.lang = 0
        inp.act = 1
    if mode == 'ENG' : 
        inp.lang = 0
        inp.act = 0
    if mode == '123' : 
        inp.lang = 2
        inp.act = 1
    show(inp)
    wait()
    run = 1
    hide('window')
    return inp.text



fil = Fill()
def fill(n, o):
    fil.paint(n, o)




def screenshot():
    try:
        shot = graphics.screenshot()
        name ='E:\\Images\\%s.png'%(str(time.time()))
        shot.save(name,callback=1)
        note('屏幕截图的保存路径:e:/Images/')
        #del shot
        #del name
        
    except:
        import traceback
        a=traceback.format_exc()
        b='出现异常：%s'%(str(a))
        app.text(b)




def input_time(title = '输入时间'):
    global run
    it = Input_time()
    it.title = title
    show(it)
    wait()
    run = 1
    hide(it)
    t = ''
    for i in xrange(len(it.text)):
        t = t + it.text[i]
    return t




def input_date(title = '输入日期'):
    global run
    it = Input_date()
    it.title = title
    show(it)
    wait()
    run = 1
    hide(it)
    t = ''
    for i in xrange(len(it.text)):
        t = t + it.text[i]
    return t




def start_up(p = None):
    try :
        path = dec(p)
    except :
        path = p
    try :
        ps = graphics.Image.open(path)
    except :
        ps = None
    sim = graphics.Image.new(can.size)
    for i in xrange(16777215, 0, -1052688):
        sim.clear(i)
        e32.ao_sleep(0.02)
        can.blit(sim)
    try :
        if ps : 
            mask = graphics.Image.new(ps.size, mode = 'L')
            for i in xrange(0, 16777215, 1052688):
                mask.clear(i)
                sim.blit(ps, target = (((w - ps.size[0]) / 2), ((h - ps.size[1]) / 2)), mask = mask)
                can.blit(sim)
                e32.ao_yield()
            pass
    except :
        if ps : 
            while y > ((h - ps.size[1]) / 2) : 
                sim.clear(0)
                sim.blit(ps, target = (((w - ps.size[0]) / 2), round(y)))
                y -= 1
                can.blit(sim)
                e32.ao_yield()
            e32.ao_sleep(1)
        pass
    e32.ao_sleep(1)


scr = Screen()
show(scr)
