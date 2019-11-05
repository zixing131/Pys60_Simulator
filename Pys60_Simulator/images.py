# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########
import graphics as gr
import os
from init_game import TILE as TILE
from init_game import W as W
from init_game import H as H
from init_game import portrait as portrait
if portrait : 
    RltX, RltY = (0, 40)
else : 
    RltX, RltY = (40, 0)


def cn2(string):
    return string.decode('utf-8')


RES_PATH = os.getcwd()[0] + ':\\RESOURCE\\APPS\\SlideTiles_2.0'
MAP_PATH = os.getcwd()[0] + ':\\data\\2048_maps'
BG_PATH = os.getcwd()[0] + ':\\data\\2048_bg'
mypath=u"..\\python\\pygame\\2048_maps\\"
RES_PATH = mypath
MAP_PATH =mypath
BG_PATH =mypath
PicFrame = RES_PATH + '\\bg_frame.png'
PicPiece = RES_PATH + '\\piece.png'
PicDigit = RES_PATH + '\\DIGITS.PNG'
PicMouse = RES_PATH + '\\mouse.png'
PicLoading = RES_PATH + '\\loading.png'
bg = gr.Image.new((W, H))
bg2 = gr.Image.new((W, H))
tmpimg = gr.Image.open(PicFrame)
tw, th = tmpimg.size
bg_frame = gr.Image.new(((tw / 2), th))
bg_frame_mask = gr.Image.new((tw/2, th), 'L')
bg_frame.blit(tmpimg, source = (0, 0, (tw / 2), th))
bg_frame_mask.blit(tmpimg, source = ((tw / 2), 0, tw, th))
readyimg = gr.Image.new((W, H))
screen_back = gr.Image.new((W, H))
longimg = gr.Image.new((W, (4 * H)))
piece = gr.Image.open(PicPiece)
tw, th = piece.size
DEFAULT_BG = gr.Image.new((W, H))
for i in xrange(0, W + tw, tw):
    for j in xrange(0, H + th, th):
        DEFAULT_BG.blit(piece, target = (i, j))


def setBg():
    bg.blit(DEFAULT_BG)




def setBg2():
    bg2.blit(bg)
    bg2.blit(bg_frame, target = (RltX, RltY), mask = bg_frame_mask)
    bg2.text((4, (H - 4)), cn2('菜单'), FONTCLR, font = (u'', 12))
    bg2.text(((W - 32), (H - 4)), cn2('退出'), FONTCLR, font = (u'', 12))




def selectBg(bgpath):
    try :
        bg.blit(gr.Image.open(bgpath).resize((W, H)))
    except :
        setBg()
    setBg2()


dgt_0 = gr.Image.new((8, 8))
dgt_1 = gr.Image.new((8, 8))
dgt_2 = gr.Image.new((8, 8))
dgt_3 = gr.Image.new((8, 8))
dgt_4 = gr.Image.new((8, 8))
dgt_5 = gr.Image.new((8, 8))
dgt_6 = gr.Image.new((8, 8))
dgt_7 = gr.Image.new((8, 8))
dgt_8 = gr.Image.new((8, 8))
dgt_9 = gr.Image.new((8, 8))
sym_score = gr.Image.new((8, 8))
sym_back1 = gr.Image.new((8, 8))
sym_back2 = gr.Image.new((8, 8))
sym_staff = gr.Image.new((8, 8))
sym_clock = gr.Image.new((8, 8))
sym_colon = gr.Image.new((8, 8))
dgt_0_mask = gr.Image.new((8, 8), '1')
dgt_1_mask = gr.Image.new((8, 8), '1')
dgt_2_mask = gr.Image.new((8, 8), '1')
dgt_3_mask = gr.Image.new((8, 8), '1')
dgt_4_mask = gr.Image.new((8, 8), '1')
dgt_5_mask = gr.Image.new((8, 8), '1')
dgt_6_mask = gr.Image.new((8, 8), '1')
dgt_7_mask = gr.Image.new((8, 8), '1')
dgt_8_mask = gr.Image.new((8, 8), '1')
dgt_9_mask = gr.Image.new((8, 8), '1')
sym_score_mask = gr.Image.new((8, 8), '1')
sym_back1_mask = gr.Image.new((8, 8), '1')
sym_back2_mask = gr.Image.new((8, 8), '1')
sym_staff_mask = gr.Image.new((8, 8), '1')
sym_clock_mask = gr.Image.new((8, 8), '1')
sym_colon_mask = gr.Image.new((8, 8), '1')
DgtList = (dgt_0, dgt_1, dgt_2, dgt_3, dgt_4, dgt_5, dgt_6, dgt_7, dgt_8, dgt_9, sym_staff, sym_back1, sym_back2, sym_score, sym_clock, sym_colon)
Dgt_maskList = (dgt_0_mask, dgt_1_mask, dgt_2_mask, dgt_3_mask, dgt_4_mask, dgt_5_mask, dgt_6_mask, dgt_7_mask, dgt_8_mask, dgt_9_mask, sym_staff_mask, sym_back1_mask, sym_back2_mask, sym_score_mask, sym_clock_mask, sym_colon_mask)
dgts = gr.Image.open(PicDigit)
dgt_masks = gr.Image.new(dgts.size, '1')
dgt_masks.clear(0)
for i in xrange(dgts.size[0]):
    for j in xrange(dgts.size[1]):
        tmp = dgts.getpixel((i, j))[0]
        if tmp[0] != 0 and tmp[1] != 0 and tmp[2] != 0 : 
            dgt_masks.point((i, j), 16777215)
for i in xrange(len(DgtList)):
    DgtList[i].blit(dgts, source = ((i * 8), 0))
    Dgt_maskList[i].blit(dgt_masks, source = ((i * 8), 0))


nm = gr.Image.new((64, 8))
nm_mask = gr.Image.new((64, 8), '1')
def numImg(num):
    string = str(num)
    nm.clear(0)
    nm_mask.clear(0)
    for i in xrange(7):
        if i < len(string) : 
            nm.blit(DgtList[int(string[i])], target = ((i * 8), 0))
            nm_mask.blit(Dgt_maskList[int(string[i])], target = ((i * 8), 0))
        else : 
            break
    return (nm, nm_mask)


tiles = {}
tile_masks = {}
for i in xrange(16):
    tiles[(2 ** (i + 1))] = gr.Image.new((TILE, TILE))
    tile_masks[(2 ** (i + 1))] = gr.Image.new((TILE, TILE), 'L')


tmpimg = gr.Image.open(PicLoading)
tw, th = tmpimg.size
ld = gr.Image.new(((tw / 2), th))
ld_mask = gr.Image.new(((tw / 2), th), 'L')
ld.blit(tmpimg, source = (0, 0, (tw / 2), th))
ld_mask.blit(tmpimg, source = ((tw / 2), 0, tw, th))
ld_back = gr.Image.new(ld.size)
ld_y = ld.size[1]
mnbg = gr.Image.new((W, H))
mnbg.clear(2829099)
mnbg_back = gr.Image.new((W, H))
mnbg_back.blit(mnbg)
menu = gr.Image.open(RES_PATH + '\\menu.png')
menu_mask = gr.Image.new(menu.size, 'L')
menu_mask.blit(gr.Image.open(RES_PATH + '\\menu_mask.png'))
barslot = [gr.Image.open(RES_PATH + '\\barslot1.png'), gr.Image.open(RES_PATH + '\\barslot2.png')]
barslot_mask = gr.Image.new(barslot[1].size, '1')
selection = gr.Image.new((220, 20))
selection.rectangle((0, 0, selection.size[0], selection.size[1]), 0, fill = 16777215)
selection_mask = gr.Image.new((220, 20), 'L')
selection_mask.clear(3947580)
bar_loc = (((107 + RltX), 110), ((107 + RltX), 140))
barnote1_x, barnote1_y = ((195 + RltX), 113)
barnote2_x, barnote2_y = ((195 + RltX), 143)
barslot_w, barslot_h = barslot[0].size
selection_size = selection.size
selection_loc = ((0, 0), (0, 0), ((10 + RltX), 105), ((10 + RltX), 135), ((10 + RltX), 165))
tmpimg = gr.Image.open(PicMouse)
tw, th = tmpimg.size
mouse = gr.Image.new(((tw / 2), th))
mouse_mask = gr.Image.new(((tw / 2), th), 'L')
mouse.blit(tmpimg, source = (0, 0, (tw / 2), th))
mouse_mask.blit(tmpimg, source = ((tw / 2), 0, tw, th))
mouse_loc = ((((93 + RltX), 68), ((114 + RltX), 68), ((136 + RltX), 68)), (((93 + RltX), 86), ((114 + RltX), 86), ((136 + RltX), 86)))
redlamb = gr.Image.open(RES_PATH + '\\redlamb.png')
greenlamb = gr.Image.open(RES_PATH + '\\greenlamb.png')
led_mask = gr.Image.new((12, 12), 'L')
led_mask.blit(gr.Image.open(RES_PATH + '\\led_mask.png'))
led_loc = ((((87 + RltX), 63), ((108 + RltX), 63), ((130 + RltX), 63)), (((87 + RltX), 80), ((108 + RltX), 80), ((130 + RltX), 80)))
def barProgressMask(ploc):
    barslot_mask.clear(0)
    barslot_mask.rectangle((0, 0, ploc, barslot_h), fill = 16777215)
    return barslot_mask




sign = gr.Image.open(RES_PATH + '\\sign.png')
sign_mask = gr.Image.new(sign.size, 'L')
sign_mask.blit(gr.Image.open(RES_PATH + '\\sign_mask.png'))
sign_loc = (((W / 2) - (sign.size[0] / 2)), (H - sign.size[1]))
def selectMenuBg(img):
    mnbg_back.blit(img)
    mnbg_back.blit(menu, target = (RltX, 0), mask = menu_mask)
    mnbg_back.blit(sign, target = sign_loc, mask = sign_mask)
    mnbg_back.text(((W - 32), (H - 4)), cn2('返回'), FONTCLR, font = (u'', 14))


FONTCLR = 15658734
hpbg = gr.Image.new((W, H))
hpbg.clear(2829099)
strings = '1.通过方向键或数字键2、4、6、8移动方块，*键重新开始，0键切换方块，1键查看排行榜，5键切换背景图，7键撤退，C键删除存档或排行榜\n2.“最多后退次数”只能在下一局生效\n3.方块元素图位于/data/2048_maps/目录下，背景图在/data/2048_bg/目录下，可自行修改方块的内容和游戏的背景'
strings2 = unicode(strings, 'utf-8')
xflag, yflag = (10, 66)
hpbg.rectangle((0, 0, W, 42), fill = 3947580)
hpbg.rectangle((0, (H - 42), W, H), fill = 3947580)
hslimg = gr.Image.new((W, H))

for s in strings2:
    if s == '\n' : 
        xflag = 10
        yflag += 18
        if (xflag + 20) >= W : 
            xflag = 26
            yflag += 18
            hpbg.text((xflag, yflag), s, FONTCLR, font = (u'', 14))
            if s >= '一'.decode('utf8') and s <= '龥'.decode('utf8') : 
                xflag += 14
                xflag += 8
                continue
                hpbg.text((((W / 2) - 60), 22), cn2('2048 (PyS60)'), FONTCLR, font = (u'', 20))
                hpbg.text((((W / 2) - 14), 38), cn2('v2.1'), FONTCLR, font = (u'', 14))
                hpbg.text((2, (H - 20)), cn2('塞班论坛：bbs.dospy.com'), FONTCLR, font = (u'', 12))
                hpbg.text((2, (H - 4)), cn2('百度贴吧：塞班S60v3吧'), FONTCLR, font = (u'', 12))
                hpbg.text(((W - 95), (H - 4)), cn2('By MyGodFalling'), FONTCLR, font = (u'', 14))
                hslimg = gr.Image.new((W, H))
                hsl_back = gr.Image.new((W, H))
                hsl_mask = gr.Image.new((W, H), 'L')
                hsl_mask.clear(16777215)
                hsl_mask.rectangle((0, 0, W, 38), fill = 10066329)
                hsl_mask.rectangle((0, (H - 22), W, H), fill = 10066329)
                hslimg.clear(0)
                hslimg.blit(DEFAULT_BG, mask = hsl_mask)
                hslimg.text((((W / 2) - 31), 31), cn2('排行榜'), FONTCLR, font = (u'', 20))
                hslimg.text(((W - 32), (H - 4)), cn2('返回'), FONTCLR, font = (u'', 14))
                hsl_back.blit(hslimg)
                wimg1 = gr.Image.new((W, H))
                wimg2 = gr.Image.new((W, H))
                wimg_mask1 = gr.Image.new((W, H), 'L')
                wimg_mask2 = gr.Image.new((W, H), 'L')
                wimg1.clear(0)
                wimg1.text((((W / 2) - 35), (H / 3)), cn2('胜利!!'), fill = 16777215, font = (u'', 24, 1))
                wimg_mask1.clear(9013641)
                wimg_mask1.text((((W / 2) - 35), (H / 3)), cn2('胜利!!'), fill = 16777215, font = (u'', 24, 1))
                wimg_mask1.text(((((W / 2) - 35) + 1), ((H / 3) + 1)), cn2('胜利!!'), fill = 16777215, font = (u'', 24, 1))
                wimg2.clear(0)
                wimg2.text((((W / 2) - 100), (H / 3)), cn2('恭喜，又前进了一步！'), fill = 16777215, font = (u'', 22, 1))
                wimg_mask2.blit(wimg2)
                wimg_mask2.text(((((W / 2) - 100) + 1), ((H / 3) + 1)), cn2('恭喜，又前进了一步！'), fill = 16777215, font = (u'', 22, 1))