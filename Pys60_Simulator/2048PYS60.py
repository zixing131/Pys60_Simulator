# -*- coding: utf-8 -*-
import appuifw as ap
import graphics as gr 
import e32
import random
import key_codes as kc

def cn(string):
    return string.decode('utf-8')
W,H = ap.Canvas().size
TILE = min(W, H)/4

BG_CLR = (25,24,24)
BOARD_CLR = (255,204,204)
SQR_CLR = 0xD2691E
NUM_CLR = 0x000000
MAINFONT_CLR = 0xFFFFFF
SHADOW = 0x666666
tc = {2:(255,255,255), 4:(255,204,51), 8:(255,105,180), 16:(0,255,165), 32:(0,255,255),
64:(240,128,128), 128:(255,0,255), 256:(255,69,0), 512:(254,251,0), 1024:(0,160,233),
2048:(165,42,42), 4096:(0,0,192), 8192:(0,0,0), 16384:(0,153,68), 2014:(240,128,128) }

TITLE = '2048 (PyS60)'
TIP = 'Press DELETE/BACKSPACE'
COPYRIGHT = 'Copyright (c) 2014-2048 Nobody'
FONT = 'normal'

directx = 0
directy = 0
start = 0
launched = 0
is_move = 0
lx = W/2 - TILE*2
ty = H/2 - TILE*2
rx = lx + 4*TILE
by = ty + 4*TILE
dat = [[0]*4 for i in range(4)]
loc = [[[0,0] for i in range(4)] for i in range(4)]
for i in range(len(loc)):
    for j in range(len(loc)):
        loc[i][j] = lx + i*TILE, ty + j*TILE
numlist = [2,2,2,2,4]
loclist = [0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3]

img = gr.Image.new((W, H))
img.clear(BG_CLR)

def fitx(text, (x0,x1)):
    f = img.measure_text(text,font = FONT)
    fit_x = (x0+x1)/2 - f[1]/2
    return fit_x
def fity(text, (y0,y1)):
    f = img.measure_text(text,font = FONT)
    fit_y = (y0+y1)/2 + (f[0][3]-f[0][1])/2
    return fit_y

def paint(rect):
    canvas.blit(img)
class Tile:
    def __init__(self):
        self.value = random.choice(numlist)
        self.index = 0
        self.blx = random.randrange(4)
        self.bly = random.randrange(4)
        self.x, self.y = loc[self.blx][self.bly]
        self.visible = 0
    def move(self):
        global is_move
        if directx == -1:
            if dat[self.blx-1][self.bly]:
                if dat[self.blx-1][self.bly].value == dat[self.blx][self.bly].value:
                    dat[self.blx-1][self.bly].value *= 2
                    dat[self.blx][self.bly].visible = 0
                    dat[self.blx][self.bly] = 0
                    is_move = 1
            else:
                dat[self.blx-1][self.bly] = dat[self.blx][self.bly]
                dat[self.blx][self.bly] = 0
                self.blx -= 1
                is_move = 1
        elif directx == 1:
            if dat[self.blx+1][self.bly]:
                if dat[self.blx+1][self.bly].value == dat[self.blx][self.bly].value:
                    dat[self.blx+1][self.bly].value *= 2
                    dat[self.blx][self.bly].visible = 0
                    dat[self.blx][self.bly] = 0
                    is_move = 1
            else:
                dat[self.blx+1][self.bly] = dat[self.blx][self.bly]
                dat[self.blx][self.bly] = 0
                self.blx += 1
                is_move = 1
        elif directy == -1:
            if dat[self.blx][self.bly-1]:
                if dat[self.blx][self.bly-1].value == dat[self.blx][self.bly].value:
                    dat[self.blx][self.bly-1].value *= 2
                    dat[self.blx][self.bly].visible = 0
                    dat[self.blx][self.bly] = 0
                    is_move = 1
            else:
                dat[self.blx][self.bly-1] = dat[self.blx][self.bly]
                dat[self.blx][self.bly] = 0
                self.bly -= 1
                is_move = 1
        elif directy == 1:
            if dat[self.blx][self.bly+1]:
                if dat[self.blx][self.bly+1].value == dat[self.blx][self.bly].value:
                    dat[self.blx][self.bly+1].value *= 2
                    dat[self.blx][self.bly].visible = 0
                    dat[self.blx][self.bly] = 0
                    is_move = 1
            else:
                dat[self.blx][self.bly+1] = dat[self.blx][self.bly]
                dat[self.blx][self.bly] = 0
                self.bly += 1
                is_move = 1
        self.x , self.y = loc[self.blx][self.bly]
        self.draw()
    def draw(self):
        global NUM_CLR
        if self.value > 512:
            NUM_CLR = 0xFFFFFF
        else:
            NUM_CLR = 0x000000
        if self.visible:
            if self.value < 30000:
                img.rectangle((self.x,self.y, self.x+TILE,self.y+TILE), BOARD_CLR, fill = tc[self.value])
                img.text((fitx(cn(str(self.value)), (self.x, self.x+TILE))\
                    ,     fity(cn(str(self.value)), (self.y, self.y+TILE)))\
                    ,          cn(str(self.value)), fill = NUM_CLR, font = FONT)
            else:
                img.rectangle((self.x,self.y, self.x+TILE,self.y+TILE), BOARD_CLR, fill = tc[2014])
                for i in range(10):
                    img.polygon((self.x+i, self.y, self.x+TILE, self.y+TILE-i, self.x+TILE, self.y)\
                        , (150+i*10, 130+i*10, 140))
                img.text((fitx(cn('END'), (self.x, self.x+TILE))\
                    ,     fity(cn('END'), (self.y, self.y+TILE)))\
                    ,          cn('END'), fill = MAINFONT_CLR, font = FONT)
    def appear(self):
        global loclist
        random.shuffle(loclist)
        self.blx = random.choice(loclist)
        self.bly = random.choice(loclist)
        while dat[self.blx][self.bly]:
            self.blx = random.choice(loclist)
            self.bly = random.choice(loclist)
        dat[self.blx][self.bly] = self
        dat[self.blx][self.bly].value = random.choice(numlist)
        self.x, self.y = loc[self.blx][self.bly]
        self.visible = 1

def draw_board():
    img.rectangle((lx,ty, rx,by), BOARD_CLR, fill = SQR_CLR)

def canmove():
    can = 0

    for d in dat:
        if not d:
            can = 1
            break
    if can:
        return 1
    else:
        for i in range(4):
            for j in range(3):
                if dat[i][j]:
                    if dat[i][j+1]:
                        if dat[i][j].value == dat[i][j+1].value:
                            can = 1
                            break
                    else:
                        can = 1
                        break
                else:
                    can = 1
                    break
    if can:
        return 1
    else:
        for i in range(3):
            for j in range(4):
                if dat[i][j]:
                    if dat[i+1][j]:
                        if dat[i][j].value == dat[i+1][j].value:
                            can = 1
                            break
                    else:
                        can = 1
                        break
                else:
                    can = 1
                    break

    if can:
        return 1
    else:
        return 0

def end():
    img.clear(BG_CLR)
    for i in range(10):
        draw_board()
        for t in ts:
            if t.visible:
                t.draw()
        img.rectangle( (0,H/2-i*2, W,H/2+i*2), fill = 0x000000 )
        img.text( ( fitx( cn('Game Over!'), (0,W) ), fity( cn('Game Over!'), (H/2-20,H/2+20) ) )\
        , cn('Game Over!'), fill = 0xFFFFFF, font = FONT )
        paint(())
        e32.ao_sleep(0.01)
    updatemenu()

def draw_ui(event):
    global start
    global launched
    global directx
    global directy
    global is_move
    global flag
    is_move = 0
    directx = 0
    directy = 0
    if start:
        if event == 2:
            directx = 0
            directy = -1
            go()
        elif event == 4:
            directx = 0
            directy = 1
            go()
        elif event == 1:
            directx = -1
            directy = 0
            go()
        elif event == 3:
            directx = 1
            directy = 0
            go()
    elif event and not launched:
        start = 1
        launched = 1
        rematch()
    if not canmove():
        end()

def go():
    global flag
    for i in range(3):
        img.clear(BG_CLR)
        draw_board()
        if directx == -1:
            for x in range(1, 4):
                for y in range(4):
                    if dat[x][y]:
                        dat[x][y].move()
                    if dat[0][y]:
                        dat[0][y].draw()
        elif directx == 1:
            for x in range(2, -1, -1):
                for y in range(len(dat)):
                    if dat[x][y]:
                        dat[x][y].move()
                    if dat[3][y]:
                        dat[3][y].draw()
        elif directy == -1:
            for y in range(1, 4):
                for x in range(4):
                    if dat[x][y]:
                        dat[x][y].move()
                    if dat[x][0]:
                        dat[x][0].draw()
        elif directy == 1:
            for y in range(2, -1, -1):
                for x in range(4):
                    if dat[x][y]:
                        dat[x][y].move()
                    if dat[x][3]:
                        dat[x][3].draw()
        paint(())
        e32.ao_sleep(0.01)

    if is_move:
        for t in ts:
            if not t.visible and canmove():#####是否有冗余判断？
                t.appear()
                for i in range(3, 0, -1):
                    img.rectangle( (t.x+i*TILE/8 , t.y+i*TILE/8,\
                                    t.x+i*TILE/8+(4-i)*TILE/4 , t.y+i*TILE/8+(4-i)*TILE/4),\
                                    BOARD_CLR, fill = tc[t.value])
                    paint(())
                    e32.ao_sleep(0.01)
                t.draw()
                break
    paint(())

def rematch():
    global dat
    img.clear(BG_CLR)
    draw_board()
    dat = [[0]*4 for i in range(4)]
    for t in ts:
        t.value = random.choice(numlist)
        t.visible = 0
    t01.appear()
    t01.draw()
    t02.appear()
    t02.draw()
    paint(())
    updatemenu()

def cheat():
    img.clear(BG_CLR)
    draw_board()
    for t in ts:
        if t.value < 250:
            t.value = 64
        t.draw()
    paint(())
    updatemenu()

def draw_welcome():
    wel_col = 1
    while not start:
        img.text((fitx(cn(TITLE),(0,W)), H/4+1), cn(TITLE), fill = SHADOW, font = FONT)
        img.text((fitx(cn(TITLE),(0,W))+1, H/4), cn(TITLE), fill = MAINFONT_CLR, font = FONT)
        fsym = img.measure_text(cn(TIP), font = 'symbol')
        fsym2 = img.measure_text(cn(COPYRIGHT))
        img.text(((W/2-fsym[1]/2), H*4/5), cn(TIP), fill = (0, 100*wel_col, 0), font = 'symbol')
        img.text(((W/2-fsym2[1]/2), H*19/20), cn(COPYRIGHT), fill = SHADOW)
        paint(())
        wel_col += 1
        if wel_col == 3:
            wel_col = 1
        e32.ao_yield()
        e32.ao_sleep(0.1)
    while 1:
        e32.ao_yield()

def exit():
    if ap.query( (cn('确定退出？(Exit?)')) , 'query' ):
        ap.app.set_exit()

def about():
    ap.query(cn('2048(PyS60)\nv1.2\n\nMade by MyGodFalling'), 'query')

def updatemenu():
    if canmove():
        ap.app.menu = [m_rematch, m_about_1, m_exit]
    else:
        ap.app.menu = [m_rematch, m_about_2, m_exit]

m_rematch = (cn('重新开始(Restart)'), rematch)
m_about_1 = (cn('关于(About)'), about)
m_about_2 = (cn('关于(About)'), ( (cn('About'),about), (cn('God Mode'),cheat) ) )
m_exit = ((cn('退出(Exit)'), exit))

canvas = ap.Canvas(redraw_callback = paint)
ap.app.body = canvas
ap.app.title = cn(TITLE)
updatemenu()
ap.app.exit_key_handler = exit
canvas.bind(63495, lambda:draw_ui(1))
canvas.bind(63497, lambda:draw_ui(2))
canvas.bind(63496, lambda:draw_ui(3))
canvas.bind(63498, lambda:draw_ui(4))
canvas.bind(63557, lambda:draw_ui(63557))
canvas.bind(8, lambda:draw_ui(8))
t01 = Tile()
t02 = Tile()
t03 = Tile()
t04 = Tile()
t05 = Tile()
t06 = Tile()
t07 = Tile()
t08 = Tile()
t09 = Tile()
t10 = Tile()
t11 = Tile()
t12 = Tile()
t13 = Tile()
t14 = Tile()
t15 = Tile()
t16 = Tile()
ts = (t01,t02,t03,t04,t05,t06,t07,t08,t09,t10,t11,t12,t13,t14,t15,t16)

tempindex = 1
for t in ts:
    t.index = tempindex
    tempindex += 1
t01.visible = 1
t02.visible = 1

draw_welcome()