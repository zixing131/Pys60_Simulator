# -*- coding: utf-8 -*-

import os, graphics as gr
import time

import e32
from keymap import *
from sysinfo import display_pixels
from akntextutils import wrap_text_to_array as wrapList
import mypath
RES_PATH = mypath.getmypath("\\python\\pysoft\\woaijidanci\\")
(W, H) = display_pixels()
KEY_TYPE = H > W and 1 or 0
KeyMap = KEY_TYPE and KeyMap_number or KeyMap_qwerty
LARGEFONT_SIZE = 26
LARGEFONT = ('title', LARGEFONT_SIZE, 1)
MAINFONT_SIZE = 18
MAINFONT = ('normal', MAINFONT_SIZE)
SMALLFONT_SIZE = 16
SMALLFONT = ('dense', SMALLFONT_SIZE)
TINYFONT_SIZE = 14
TINYFONT = ('dense', TINYFONT_SIZE)
HIGHLIGHT = 16777215
SHADOW = 0
BG_CLR = 15658734
BANNER_CLR = 2129952
MAINWORD_CLR = 1250337
LX = 10
RX = W - 10
TY = 22
BY = H - 22
TEXT_WIDE = W - 20
LINE_DIST = 5
TITLE_HEIGHT = TY
Title_pos = (3, TITLE_HEIGHT - 2)
TBanner_pos = (0, 0)
Buttom_pos = (3, H - 2)
BBanner_pos = (0, H - TITLE_HEIGHT)
DicList_pos = (LX, 50)
Selection_pos = (LX - 5, DicList_pos[1] - MAINFONT_SIZE - LINE_DIST / 2)
Record_pos = (LX, H - 22 - 5 - 36)
Mwbg_pos = (0, 25)
MainWord_pos = (0, 56)
PhoneticSymbol_pos = (0, 83)
WordClass_pos = (0, 62)
SMatter_pos = (LX / 2, 18)
SMatterImg_pos = (LX, 90)
if KEY_TYPE == 1:
    SMatterImg_pos = (LX, 87)
Space_pos = (LX, 54)
Tick_pos = (W / 2, MainWord_pos[1])
Cross_pos = (W / 2 - 100, MainWord_pos[1])
UI_flag = 0
busy = 0
isRight = 0
FinishTimes = 0
haveWrong = 0
OneShots = 0
DicList = []
DicAmount = 0
WordLines = []
RecentList = []
Selection = 0
Blanks = []
Blks = 0
XPlace = 0
XLine = 0
XLines = 0
Level = 1
Fragmentary = 0
Title = ''
Extra_string = '○●'
Extra_string_list = ('○', '○●', '○●●', '☆')
word = ''
phonetic_symbol = ''
word_class = ''
straight_matter_part = ''
straight_matter_all = ''
n_word = ''
n_phonetic_symbol = ''
n_word_class = ''
n_smatter = ''
hf_word = ''
history = []
input_buf = []
TapState = 0
TapDelay = 0.9
clock_0 = 0
clock_1 = 0
USERCODE = 'utf-8'

def cn(string):
    return string.decode('utf-8')


def cng(string):
    return string.decode('gbk')


def cnx(string, coding='gb2312'):
    return string.decode(coding)


mwbg_pic = gr.Image.open(RES_PATH + '\\mwbg.png')
space_pic = gr.Image.open(RES_PATH + '\\space.png')
watermark_pic = gr.Image.open(RES_PATH + '\\watermark.png')
help_pic = gr.Image.open(RES_PATH + '\\help.png')
readyimg = gr.Image.new((W, H))
screen_bak = gr.Image.new((W, H))
screen_mask = gr.Image.new((W, H), 'L')
splashimg = gr.Image.new((W, H))
bg = gr.Image.new((W, H))
DEFAULT_BG = gr.Image.new((W, H))
playing_bg = gr.Image.new((W, H))
watermarkimg = gr.Image.new((320, 100))
watermark_mask = gr.Image.new(watermarkimg.size, 'L')
headimg = gr.Image.new((W, TITLE_HEIGHT))
buttomimg = gr.Image.new((W, TITLE_HEIGHT))
buttomimg0 = gr.Image.new((W, TITLE_HEIGHT))
buttomimg1 = gr.Image.new((W, TITLE_HEIGHT))
buttomimg2 = gr.Image.new((W, TITLE_HEIGHT))
buttomimg3 = gr.Image.new((W, TITLE_HEIGHT))
cursorimg = gr.Image.new((TEXT_WIDE, TITLE_HEIGHT))
cursor_mask = gr.Image.new((TEXT_WIDE + 10, TITLE_HEIGHT), 'L')
mwbgimg = gr.Image.new((mwbg_pic.size[0] / 2, mwbg_pic.size[1]))
mwbg_mask = gr.Image.new(mwbgimg.size, 'L')
underlineimg = gr.Image.new((W, 2))
underline_mask = gr.Image.new(underlineimg.size, 'L')
smatterimg = gr.Image.new((W - 20, 20 * H))
spaceimg = gr.Image.new((space_pic.size[0] / 2, space_pic.size[1]))
space_mask = gr.Image.new(spaceimg.size, 'L')
pieceimg = gr.Image.new((8, 8))
helpimg = gr.Image.new((W, H))

def allotImg(img0, img1, img2):
    (w, h) = img0.size
    img1.blit(img0, source=(0, 0, w / 2, h))
    img2.blit(img0, source=(w / 2, 0, w, h))
    return (img1, img2)


buttomimg0.clear(BANNER_CLR)
buttomimg0.text(Title_pos, cn('菜单'), HIGHLIGHT, font=MAINFONT)
buttomimg0.text((W - 38, Title_pos[1]), cn('退出'), HIGHLIGHT, font=MAINFONT)
buttomimg1.clear(BANNER_CLR)
buttomimg1.text(Title_pos, cn('菜单'), HIGHLIGHT, font=MAINFONT)
buttomimg1.text((W / 2 - 18, Title_pos[1]), cn('确定'), HIGHLIGHT, font=MAINFONT)
buttomimg1.text((W - 38, Title_pos[1]), cn('返回'), HIGHLIGHT, font=MAINFONT)
buttomimg2.clear(BANNER_CLR)
buttomimg2.text(Title_pos, cn('菜单'), HIGHLIGHT, font=MAINFONT)
buttomimg2.text((W / 2 - 24, Title_pos[1]), cn('下一个'), HIGHLIGHT, font=MAINFONT)
buttomimg2.text((W - 38, Title_pos[1]), cn('返回'), HIGHLIGHT, font=MAINFONT)
cursorimg.clear(SHADOW)
cursor_mask.rectangle((0, 0, cursorimg.size[0], cursorimg.size[1]), HIGHLIGHT, fill=2829099)
DEFAULT_BG.clear(BG_CLR)
underlineimg.clear(16716947)
(mwbgimg, mwbg_mask) = allotImg(mwbg_pic, mwbgimg, mwbg_mask)
Mwbg_pos = ((W - mwbgimg.size[0]) / 2, Mwbg_pos[1])
(spaceimg, space_mask) = allotImg(space_pic, spaceimg, space_mask)
(watermarkimg, watermark_mask) = allotImg(watermark_pic, watermarkimg, watermark_mask)
(pw, ph) = pieceimg.size

def makePieceimg():
    pieceimg.clear(BG_CLR)
    pieceimg.line((0, 0, 0, ph), 14540253)
    pieceimg.line((0, 0, pw, 0), 14540253)


def drawWatermark(img):
    img.blit(watermarkimg, target=(img.size[0] - watermarkimg.size[0], img.size[1] - watermarkimg.size[1] - TITLE_HEIGHT), mask=watermark_mask)


def getBg(background=None, title_string=' ', extra_string=' '):
    if background == None:
        bg.blit(DEFAULT_BG)
    else:
        bg.blit(background)
    headimg.clear(BANNER_CLR)
    headimg.text(Title_pos, cn(title_string), HIGHLIGHT, font=MAINFONT)
    headimg.text((W - getSize(cn(extra_string), fnt=MAINFONT) - 2, Title_pos[1]), cn(extra_string), HIGHLIGHT, font=MAINFONT)
    bg.blit(headimg, target=TBanner_pos)
    bg.blit(buttomimg, target=BBanner_pos)
    return bg

def chooseButtom(img):
    buttomimg.blit(img)


def drawMwbg():
    readyimg.blit(mwbgimg, target=Mwbg_pos, mask=mwbg_mask)


def drawWord(wrd):
    readyimg.text(((W - getSize(wrd)) / 2, MainWord_pos[1]), wrd, MAINWORD_CLR, font=LARGEFONT)


def drawUnderline(wrd, ls):
    underline_mask.clear(0)
    for i in ls:
        x0 = W / 2 - getSize(wrd) / 2 + getSize(wrd[:i]) + 1
        x1 = x0 + getSize(wrd[i]) - 1
        underline_mask.line((x0, 0, x1, 0), 16777215)
        underline_mask.line((x0, 1, x1, 1), 16777215)

    readyimg.blit(underlineimg, target=(0, MainWord_pos[1] - 4), mask=underline_mask)


def drawSpacePointer(xplc, hfwrd):
    readyimg.blit(spaceimg, target=((W - getSize(hfwrd)) / 2 + getSize(hfwrd[:xplc]) + getSize(hfwrd[xplc]) / 2 - CursorWide / 2, Space_pos[1]), mask=space_mask)


def drawWordClass(wrd_clss):
    readyimg.text(((W + mwbgimg.size[0]) / 2 - getSize(wrd_clss, fnt=SMALLFONT) - 5, WordClass_pos[1]), wrd_clss, SHADOW, font=SMALLFONT)


def drawPhoneticSymbol(phntc_smbl):
    readyimg.text(((W - getSize(phntc_smbl, fnt=('dense', 16, 1))) / 2, PhoneticSymbol_pos[1]), phntc_smbl, SHADOW, font=('dense', 16, 1))


def initSMatterImg(txts):
    smatterimg.clear(HIGHLIGHT)
    line = 0
    wrp = wrapList(txts, SMALLFONT[0], W)
    for txt in wrp:
        smatterimg.text((SMatter_pos[0], SMatter_pos[1] + line * (SMALLFONT_SIZE + LINE_DIST)), txt, SHADOW, font=SMALLFONT)
        line += 1

    return len(wrp)


def drawSMatter(line=0):
    loc = (SMALLFONT_SIZE + LINE_DIST) * line
    readyimg.blit(smatterimg, target=SMatterImg_pos, source=(0, loc, W, H - TITLE_HEIGHT - SMatterImg_pos[1] + loc))


def drawTick(img):
    img.line((Tick_pos[0], Tick_pos[1], Tick_pos[0] + 40, Tick_pos[1] + 40, W, 0), 65280, width=10)


def drawCross(img, part):
    if part == 0:
        tmp_pos = (Cross_pos[0] + 40, Cross_pos[1], Cross_pos[0] + 20, Cross_pos[1] + 20)
    elif part == 1:
        tmp_pos = (Cross_pos[0] + 20, Cross_pos[1] + 20, Cross_pos[0], Cross_pos[1] + 40)
    elif part == 2:
        tmp_pos = (Cross_pos[0], Cross_pos[1], Cross_pos[0] + 20, Cross_pos[1] + 20)
    elif part == 3:
        tmp_pos = (Cross_pos[0] + 20, Cross_pos[1] + 20, Cross_pos[0] + 40, Cross_pos[1] + 40)
    img.line(tmp_pos, 16711680, width=8)


def drawSplashScreen():
    readyimg.clear(6591981)
    screen_bak.clear(6591981)
    drawWatermark(screen_bak)
    txt = cn('我爱记单词')
    screen_bak.text((W / 2 - getSize(txt) / 2, H / 8), txt, HIGHLIGHT, font=LARGEFONT)
    txt = cn('v1.0')
    screen_bak.text((W / 2 - getSize(txt, fnt=SMALLFONT) / 2, H / 8 + SMALLFONT_SIZE), txt, BG_CLR, font=SMALLFONT)
    txt = cn('献给还在用Symbian的朋友们!')
    screen_bak.text((W / 2 - getSize(txt, fnt=TINYFONT) / 2, H / 2), txt, BG_CLR, font=TINYFONT)
    txt = cn('- MyGodFalling -')
    screen_bak.text((W / 2 - getSize(txt, fnt=('dense', 16, 1)) / 2, H - 2 * TITLE_HEIGHT), txt, HIGHLIGHT, font=('dense', 16, 1))
    readyimg.blit(screen_bak, target=(0, TITLE_HEIGHT))
    #e32.ao_sleep(1)


def drawHelp(img=readyimg):
    img.clear(7105644)
    img.blit(help_pic, target=(W / 2 - help_pic.size[0] / 2, H / 2 - help_pic.size[1] / 2))
    img.text((W - getSize(cn('返回'), fnt=SMALLFONT) - 2, H - 2), cn('返回'), HIGHLIGHT, font=SMALLFONT)


def getSize(wrd, fnt=LARGEFONT):
    return readyimg.measure_text(wrd, font=fnt)[1]


def rp(wrd, idx, char):
    return wrd[:idx] + char + wrd[idx + 1:]


CursorWide = spaceimg.size[0]
