# -*- coding: utf-8 -*-
import appuifw2 as appuifw
import e32
# aotimertmp = e32.Ao_timer()
# aotimertmp.after(0,lambda:appuifw.note(('程序加载中…').decode('utf-8')))
import graphics
import sys, os
import TopWindow 

if sys.path[1].find('neteaseDebug') == -1:
    sys.path[1:1] = [os.path.abspath("e:\\neteaseDebug")]

from util import *
if UTILINITED:
    try:
        reload(api)
        reload(playlist)
    except:
        pass
    
utilInit()

foreground = True
def switchForeground_(whetherForeground):
    global foreground
    if whetherForeground:
        foreground = True
        try:
            splashScreen.show()
        except:
            logs('splash Error')
    else:
        foreground = False
        splashScreen.hide()   
appuifw.app.focus = switchForeground_
#appuifw.app.screen = "full"
splashScreen = TopWindow.TopWindow()
splashScreen.size = (200,65)
canvassize=appuifw.Canvas().size
splashScreen.position = (canvassize[0] / 2 - 100, canvassize[1] / 2 - 32)
del canvassize
splashScreen.background_color=0xffffff
splashScreen.add_image(graphics.Image.open(sys.path[0] + '\\pic\\SplashScreen.scale-100.bmp'), (0,0))
splashScreen.show()
aotimertmp = e32.Ao_timer()
aotimertmp.after(0,lambda:appuifw.note(cn('程序加载中………')))
logs(u'splashScreen Loaded')
# import sys
# import os

import api
import playlist
import httplib
import socket
try:
    # sys.path[0:0] = [os.path.abspath("e:\\neteaseDebug")]
    import e32
    
except:
    pass
import key_codes
import audio
import time
import copy
import math
import simplejson as json

logs(u'modules Imported')
'''
一些重要变量定义
'''

threadRunning = True

#rotatingUnit * 4 = 旋转图片的数量
rotatingUnit = 4
rotatingImages = rotatingUnit * 4
#AngleSins = [sin(0), sin(pi/2 * 1/n), sin(pi/2 * 2/n) ...]
AngleSins = [math.sin(Pi /2. * (x) / rotatingUnit) for x in range(rotatingUnit)]
AngleCoss = [math.cos(Pi /2. * (x) / rotatingUnit) for x in range(rotatingUnit)]
logs(u'vars Defined')

'''
画图函数
'''

def definePlots():
    #初始时：画图元素的载入

    #关于屏幕适配像素点数列plots的说明
    #plots[0]: img1的宽高，为plots[1]宽高的73/112
    #plots[1]: img3的宽高，为画布高的50%
    #plots[2]: img7的宽，为plots[1]39/112，img7高以51:39换算过来
    #plots[3]: img3的mask的边距留空，为plots[1]宽高的1/56
    #plots[4]: canvas的宽高，是一个tuple
    #plots[5]: 唱盘的圆心，在(0.5x, 0.45y)，是一个tuple
    #plots[6]: img1的开始绘制位置，按照圆心和img1宽高换算得到
    #plots[7]: img3的开始绘制位置，参照上条
    #plots[8]: img5的开始绘制位置，位于圆心上33/56，右3/16的位置
    #plots[9]: img7的开始绘制位置，位于圆心上33/56，右59/112的位置
    #plots[10]: Text的开始绘制位置，位于画布的(0.06x, 0)的位置
    #plots[11]: 提示Toast的宽度，等于120
    #plots[12]: 提示Toast的高度，等于40
    #plots[13]: 提示Toast开始绘制的位置，位于画布的(0.5x-plots[11]/2, 0.8y - plots[12]/2)的位置
    
    #plots[15]是红心图标等的开始绘制的纵坐标 0.75y
    #plots[16]是红心等图标的宽和高 plots[1]*0.1
    #plots[17]是左图标开始绘制的横坐标 0.15x-plots[16]*0.5
    #plots[18]是右图标开始绘制的横坐标 0.85x-plots[16]*0.5
    # plots[19]是中图标开始绘制的横坐标 0.5x-plots[16]*0.5
    # plots[20]是进度条的纵坐标 y * 0.72
    
    global buf, plots, img
    buf = graphics.Image.new(appuifw.Canvas().size)
    plots = range(0,100)
    (screen_x, screen_y) = appuifw.Canvas().size
    plots[1] = screen_y /2
    plots[0] = plots[1] * 75 /112
    plots[2] = plots[1] * 30 /112
    plots[3] = plots[1] * 1 /56
    plots[4] = (screen_x, screen_y)
    plots[5] = (screen_x * 0.5, screen_y * 0.45)
    plots[6] = (plots[5][0] - plots[0] / 2. -0.5, plots[5][1] - plots[0] / 2. -0.5)
    plots[7] = (plots[5][0] - plots[1] / 2, plots[5][1] - plots[1] / 2)
    plots[8] = (plots[5][0] + plots[1] * 4 / 16, plots[5][1] - plots[1] * 28 / 56)
    plots[9] = (plots[5][0] + plots[1] * 57 / 112, plots[5][1] - plots[1] * 28 / 56)
    plots[10] = (screen_x * 0.06, 0)
    plots[11] = screen_x
    plots[12] = 70
    plots[13] = (0.5*screen_x-plots[11]/2, 0.85*screen_y - plots[12]/2)
    plots[14] = plots[12] * 1. * 3 / 5
    
    plots[15] = screen_y * 0.75
    plots[16] = int(plots[1] * 0.4)
    plots[17] = 0.15 * screen_x - plots[16]/2
    plots[18] = 0.85 * screen_x - plots[16]/2
    plots[19] = 0.5 * screen_x - plots[16]/2
    plots[20] = 0.72 * screen_y
    img = range(0,100)
    
    #img1为AlbumArt，img2作为裁切其为圆形的mask
    #img3是唱盘，img4作为其mask
    #img5是唱针，img6作为其mask，img6_是临时图片，blit到8位img6上用的
    #img7 img8 是img5 img6的副本，在下面会将img5和img6旋转270°作为播放时的唱针
    #img10是模糊化的AlbumArt，作为背景；img11是黯淡化遮罩
    #img12是模糊化的AlbumArt，作为背景2；img13是黯淡化遮罩
    #img14和img15分别为提示Toast和其遮罩
    
    #img21-24是空的红心图标 遮罩 红的红心图标 遮罩 
    #img25-30是播放顺序图标: 列循 单循 随机 和其遮罩（间）
    #img31-32是待定图标
    
    #buf是缓冲图形，blit到canvas用
    
    img[0] = graphics.Image.open(sys.path[0] + '\\pic\\pic.bmp').resize((plots[0],plots[0]))
    img[1] = img[0]
    img[2] = graphics.Image.new((plots[0],plots[0]),mode='1')
    img[3] = graphics.Image.open(sys.path[0] + '\\pic\\play_disc.png').resize((plots[1] ,plots[1]))
    img[4] = graphics.Image.new((plots[1],plots[1]),mode='1')
    img[5] = graphics.Image.open(sys.path[0] + '\\pic\\play_needle.png').resize((plots[2] ,plots[2] * 51 / 39))
    img6_ = graphics.Image.open(sys.path[0] + '\\pic\\play_needle_.png').resize((plots[2] ,plots[2] * 51 / 39))
    img[6] = graphics.Image.new(img6_.size, 'L')
    img[6].blit(img6_)
    img[7] = graphics.Image.new(img[5].size)
    img[7].blit(img[5])
    img[8] = graphics.Image.new(img[6].size, 'L')
    img[8].blit(img[6])
    img[5] = img[5].transpose(graphics.ROTATE_270)
    img[6] = img[6].transpose(graphics.ROTATE_270)
    img[10] = img[1].resize((16,16)).resize(appuifw.Canvas().size)
    img[11] = graphics.Image.new(appuifw.Canvas().size, 'L')
    img[11].clear(0x303030)
    img[12] = img[1].resize((22,22)).resize(appuifw.Canvas().size)
    img[13] = graphics.Image.new(appuifw.Canvas().size, 'L')
    img[13].clear(0x7A7A7A)

    img[14] = graphics.Image.new((plots[11], plots[12]))
    img[15] = graphics.Image.new((plots[11], plots[12]), 'L')
    img[14].clear(0x000000)
    img[15].clear(0xC1C1C1)
    
    
    #表示进度的扇形及其中的进度数字, 还有三个临时图层, plots[14] 表示扇形宽高
    img[16] = graphics.Image.new((plots[14],plots[14]), 'L')
    img[17] = graphics.Image.new((plots[14],plots[14]), 'L')
    img[18] = graphics.Image.new((plots[14],plots[14]), 'L')
    img[19] = graphics.Image.new((plots[14],plots[14]), 'L')
    img[20] = graphics.Image.new((plots[14],plots[14]), '1')
    
    img[21] = graphics.Image.open(sys.path[0] + '\\pic\\play_icn_love.bmp')
    img[22] = graphics.Image.new(img[21].size, 'L')
    img[22].load(sys.path[0] + '\\pic\\play_icn_love_.bmp')
    img[21] = img[21].resize((plots[16], plots[16]))
    img[22] = img[22].resize((plots[16], plots[16]))
    img[23] = graphics.Image.open(sys.path[0] + '\\pic\\play_icn_loved.bmp')
    img[24] = graphics.Image.new(img[23].size, 'L')
    img[24].load(sys.path[0] + '\\pic\\play_icn_loved_.bmp')
    img[23] = img[23].resize((plots[16], plots[16]))
    img[24] = img[24].resize((plots[16], plots[16]))
    
    img[25] = graphics.Image.open(sys.path[0] + '\\pic\\play_icn_loop.bmp')
    img[26] = graphics.Image.new(img[25].size, 'L')
    img[26].load(sys.path[0] + '\\pic\\play_icn_loop_.bmp')
    img[25] = img[25].resize((plots[16], plots[16]))
    img[26] = img[26].resize((plots[16], plots[16]))
    
    img[27] = graphics.Image.open(sys.path[0] + '\\pic\\play_icn_one.bmp')
    img[28] = graphics.Image.new(img[27].size, 'L')
    img[28].load(sys.path[0] + '\\pic\\play_icn_one_.bmp')
    img[27] = img[27].resize((plots[16], plots[16]))
    img[28] = img[28].resize((plots[16], plots[16]))
    
    img[29] = graphics.Image.open(sys.path[0] + '\\pic\\play_icn_shuffle.bmp')
    img[30] = graphics.Image.new(img[29].size, 'L')
    img[30].load(sys.path[0] + '\\pic\\play_icn_shuffle_.bmp')
    img[29] = img[29].resize((plots[16], plots[16]))
    img[30] = img[30].resize((plots[16], plots[16]))
    
    img[31] = graphics.Image.open(sys.path[0] + '\\pic\\list_detail_icn_fav.bmp')
    img[32] = graphics.Image.new(img[31].size, 'L')
    img[32].load(sys.path[0] + '\\pic\\list_detail_icn_fav_.bmp')
    img[31] = img[31].resize((plots[16], plots[16]))
    img[32] = img[32].resize((plots[16], plots[16]))
    
    img[33] = graphics.Image.open(sys.path[0] + '\\pic\\list_detail_icn_faved.bmp')
    img[34] = graphics.Image.new(img[33].size, 'L')
    img[34].load(sys.path[0] + '\\pic\\list_detail_icn_faved_.bmp')
    img[33] = img[33].resize((plots[16], plots[16]))
    img[34] = img[34].resize((plots[16], plots[16]))
    
    
    #img35是一个List，包括旋转过的专辑封面图片
    img[35] = range(rotatingImages)
    
    #img36是进度条
    img[36] = graphics.Image.new((appuifw.Canvas().size[0], 5))
    img[36].clear(0x000000)
    img[37] = graphics.Image.new((appuifw.Canvas().size[0], 5),  'L')
    img[37].clear(0xFFFFFF)
    buf = graphics.Image.new(appuifw.Canvas().size)

FONT_MEDIUM = 0
FONT_SMALL = 0

def initDraw():
    global img,buf, plots
    
    #此时开始画img1的mask
    img[2].clear(0x000000)
    img[2].ellipse((0,0,plots[0],plots[0]),fill=0xffffff)
    #此时开始画img3的mask
    img[4].clear(0x000000)
    img[4].ellipse((plots[3],plots[3],plots[1] - plots[3],plots[1] - plots[3]),fill=0xffffff)
    img[4].ellipse((plots[1]/2 - plots[0] /2,plots[1]/2 - plots[0] /2,plots[1]/2 + plots[0] /2,plots[1]/2 + plots[0] /2),fill=0x000000)
    
    #正式开始画buf
    buf.clear(0x303030)
    buf.blit(img[10],mask=img[11])
    buf.blit(img[3],target = plots[7], source=((0,0),(plots[1],plots[1])),mask=img[4])
    buf.blit(img[1],target = plots[6], source=((0,0),(plots[0],plots[0])),mask=img[2])
    # buf.blit(img5,target = (185,20), source=((0,0),(51,39)),mask=img6)
    #开始时的默认唱针，暂停时
    buf.blit(img[7],target = plots[9], source=((0,0),(plots[2] ,plots[2] * 51 / 39)),mask=img[8])
    # buf.blit(img9,target = (5,20))
    buf.blit(img[12],target = (0,0), source=((0,0),(plots[4][0],plots[4][1] *0.18)),mask=img[13])
    
    gap1 = (plots[4][0] + plots[4][1])  * 15 / 560
    gap2 = gap1 * 0.8
    
    buf.text((plots[10][0],plots[10][1]+gap1 + 2), cn('网易云音乐'),fill=0xffffff,font=("normal",gap1,graphics.FONT_BOLD|graphics.FONT_ANTIALIAS))
    buf.text((plots[10][0]+15,plots[10][1]+gap1+gap2 + 4), cn('请选择左键菜单中的启动连接') ,fill=0xffffff,font=("normal",gap2,None))
    buf.text((plots[10][0]+15,plots[10][1]+gap2+gap2+gap1 +6), cn('选项-设置-帮助关于 可以看使用帮助'),fill=0xffffff,font=("normal",gap2,None))
    lyricBlit(currLrc)
    redraw()
    
drawRotationToWhere = -1
def drawRotation():
    global img, drawRotationToWhere
    R = img[1].size[0]
    # pixelEdited = [ [False for a in range(R)] for b in range(R)]
    for x in range(rotatingImages):
        img[35][x] = img[0]
        
    aotimer3.cancel()
    aotimer3.after(0, loopRotate)
        
    img[35][0] = img[1]
    drawRotationToWhere = 0
    for x in range(1, rotatingImages):
        img[35][x] = graphics.Image.new(img[1].size)
        img[35][x].clear(0x000000)
        
    rgb = range(img[1].size[1])
    for i in range(img[1].size[0]):
        rgb[i] = img[1].getpixel([(i,k) for k in range(img[1].size[1])])
        e32.ao_yield()
        
    for x in range(1, rotatingUnit):
        cos = AngleCoss[x]
        sin = AngleSins[x]
        for i in range(img[1].size[0]):
            icos = (i - R / 2.) * cos
            isin = (i - R / 2.) * sin
            for j in range(img[1].size[1]):
                jcos = (j - R / 2.) * cos
                jsin = (j - R / 2.) * sin
                thisPlotX = int(icos - jsin + R / 2.)
                thisPlotY = int(jcos + isin + R / 2.)
                if thisPlotX >= R or thisPlotY >=R or thisPlotX <0 or thisPlotY <0:
                    pass
                else:
                    img[35][x].point((thisPlotX, thisPlotY), width = 2, outline = rgb[i][j])
                e32.ao_yield()
        drawRotationToWhere = x
        # logs('drawn to %s' % drawRotationToWhere)
    del rgb
    for x in range(rotatingUnit, rotatingImages):
        img[35][x] = img[35][x-rotatingUnit].transpose(graphics.ROTATE_270)
        drawRotationToWhere = x
        # logs('drawn to %s' % drawRotationToWhere)
    
    
rotateCycle = 2 #REFRESH ROTATE EVERY 3 SECONDS
tmpRotateVar = 0
def loopRotate():

    global img, currRotation,tmpRotateVar
    if not('npl' in globals()): return
    if npl.player and npl.player.state() == audio.EPlaying and not(toastVisibility):
        if tmpRotateVar == 0:
            # logs('currRotate to %s, drawn to %s' % (currRotation, drawRotationToWhere))
            if currRotation <= drawRotationToWhere:
                # logs('draw')
                redrawRotate()
                currRotation = (currRotation + 1) % rotatingImages
        else:
            pass
        tmpRotateVar = (tmpRotateVar + 1) % rotateCycle
    else:
        pass
        
    # logs('loopRotated - %s' % readableTime2(npl.player.current_position()/1000))
    redrawPosition()
    redraw()
    
    if npl.player != False and npl.player.state() == audio.EPlaying and not(toastVisibility) and foreground:
        aotimer3.cancel()
        aotimer3.after(1, loopRotate)
    
def redrawRotate():
    global img,buf,plots
    buf.blit(img[35][currRotation],target = plots[6], source=((0,0),(plots[0],plots[0])),mask=img[2])
    
    
    # redraw((plots[6][0],plots[6][1],plots[6][0]+plots[0],plots[6][1]+plots[0]))
    
    
def redrawPosition():
    #计算播放进度
    
    if not('npl' in globals()) or not(npl.player):
        return
    duration = npl.player.duration()
    
    if npl.player and npl.player.state() == audio.EPlaying:
        position = npl.player.current_position()
    else:
        position = npl.currPos
    posScale = position * 1. / duration
    
    #img11: 临时图像，全黑供clear buf用
    img11 = graphics.Image.new(mainCanvas.size)
    img11.clear(0x303030)
    #给buf相应部分clear，然后重绘背景
    buf.blit(img11, target = (0,plots[20]), source=((0,0), (mainCanvas.size[0], 9)))
    buf.blit(img[10], target = (0,plots[20]), source=((0,plots[20]), (mainCanvas.size[0], plots[20] +9)))
    
    img[37].clear(0x5E5E5E)
    buf.blit(img[36], target = (0,plots[20]), source=((0,0), (mainCanvas.size[0], 2)), mask=img[37])
    buf.blit(img[36], target = (0,plots[20] + 2 + 5), source=((0,0), (mainCanvas.size[0], 2)), mask=img[37])
    
    img[37].clear(0x989898)
    buf.blit(img[36], target = (posScale * mainCanvas.size[0],plots[20] + 2), source=((0,0), (mainCanvas.size[0], 5)), mask=img[37])
    
    
    buf.text((10+1,plots[20] +9+1), cn(readableTime2(position / 1000)),fill=0x000000,font=("normal",FONT_SMALL,None))
    buf.text((mainCanvas.size[0] - 10 - 20 +1,plots[20] +9+1), u'-' + cn(readableTime2((duration - position) / 1000)),fill=0x000000,font=("normal",FONT_SMALL,None))
    buf.text((mainCanvas.size[0] / 2 - 10+1,plots[20] +9+1),cn(readableTime2((duration ) / 1000)),fill=0x000000,font=("normal",FONT_SMALL,None))
    
    buf.text((10,plots[20] +9), cn(readableTime2(position / 1000)),fill=0xffffff,font=("normal",FONT_SMALL,None))
    buf.text((mainCanvas.size[0] - 10 - 20,plots[20] +9), u'-' + cn(readableTime2((duration - position) / 1000)),fill=0xffffff,font=("normal",FONT_SMALL,None))
    buf.text((mainCanvas.size[0] / 2 - 10,plots[20] +9),cn(readableTime2((duration ) / 1000)),fill=0xffffff,font=("normal",FONT_SMALL,None))

liked = False
faved = False
currOrder = 0
def refreshButtonsStatus():
    global liked, faved, currOrder
    songIndex = npl.songIndex
    likeResult = nma.like(npl.songList[songIndex], True)
    if likeResult.get('songs') == []:
        #表示之前没有喜欢
        likeResult = nma.like(npl.songList[songIndex], False)
        liked = False
    else:
        #之前已经喜欢了
        liked = True
    currOrder = npl.order
        
def drawButtons():
    
    
    #重画下面的三个图标
    if liked:
        buf.blit(img[23],target = (plots[19],plots[15]),mask=img[24])
    else:
        buf.blit(img[21],target = (plots[19],plots[15]),mask=img[22])
        
    if False and faved:
        buf.blit(img[33],target = (plots[17],plots[15]),mask=img[34])
    else:
        buf.blit(img[31],target = (plots[17],plots[15]),mask=img[32]) 
        
    
    
    buf.blit(img[25+currOrder*2],target = (plots[18],plots[15]),mask=img[25+currOrder*2 +1])
    
currRotation = 0
def redrawSong(pl):
    #在切歌时重画画布，更换AlbumArt
    
    global img,buf,plots
    songDict = pl.getCurrentInfo()
    
    
    #重获取img1
    img[1] = pl.fetchPicImage()
    
    img[35][0] = img[1]
                
    #img[1] = img[35][1]
    img[10] = img[1].resize((16,16)).resize(mainCanvas.size)
    img[11].clear(0x303030)
    img[12] = img[1].resize((22,22)).resize(mainCanvas.size)
    img[13] = graphics.Image.new(mainCanvas.size, 'L')
    img[13].clear(0x303030)
    #开始画buf
    buf.clear(0x303030)
    buf.blit(img[10],mask=img[11])
    buf.blit(img[3],target = plots[7], source=((0,0),(plots[1],plots[1])),mask=img[4])
    buf.blit(img[35][currRotation],target = plots[6], source=((0,0),(plots[0],plots[0])),mask=img[2])
    #根据播放暂停状态选择唱针
    if pl.player.state() == audio.EPlaying:
        buf.blit(img[5],target = plots[8], source=((0,0),(plots[2] * 51 / 39, plots[2])),mask=img[6])
    else:
        buf.blit(img[7],target = plots[9], source=((0,0),(plots[2] ,plots[2] * 51 / 39)),mask=img[8])
    # buf.blit(img9,target = (5,20))
    buf.blit(img[12],target = (0,0), source=((0,0),(plots[4][0],plots[4][1] *0.18)),mask=img[13])


    redrawPosition()
    drawButtons()
    
    gap1 = (plots[4][0] + plots[4][1])  * 15 / 560
    gap2 = gap1 * 0.8

    buf.text((plots[10][0],plots[10][1]+gap1 + 2), cn(songDict['name']),fill=0xffffff,font=("normal",gap1,graphics.FONT_BOLD|graphics.FONT_ANTIALIAS))
    buf.text((plots[10][0]+15,plots[10][1]+gap1+4 + gap2), cn(' & ').join([cn(artist['name']) for artist in songDict['artists']]) ,fill=0xffffff,font=("normal",gap2,None))
    buf.text((plots[10][0]+15,plots[10][1]+gap1+6+gap2+gap2), cn(songDict['album']['name']) + cn(' #') + str(songDict['no']),fill=0xffffff,font=("normal",gap2,None))
    redraw()
    e32.ao_sleep(0, drawRotation)
    
def redrawPause(pl):
    #在暂停和继续播放时更新画布使唱针旋转
    #修正使其只更新(plots[8][0], plots[8][1])-(plots[9][0] + plots[2], plots[7][1] + plots[2] * 51 / 39)部分的内容
    global img,buf,plots
    songDict = pl.getCurrentInfo()
    if songDict == None:return
    #img11: 临时图像，全黑供clear buf用
    img11 = graphics.Image.new(mainCanvas.size)
    img11.clear(0x303030)
    #给buf相应部分clear，然后重绘背景
    buf.blit(img11, target = (plots[8][0], plots[8][1]), source=((plots[8][0], plots[8][1]), (plots[9][0] + plots[2], plots[9][1] + plots[2] * 51 / 39)))
    buf.blit(img[10], target = (plots[8][0], plots[8][1]), source=((plots[8][0], plots[8][1]), (plots[9][0] + plots[2], plots[9][1] + plots[2] * 51 / 39)), mask=img[11])
    #画唱盘
    buf.blit(img[3],target = plots[7], source=((0,0),(plots[1],plots[1])),mask=img[4])
    buf.blit(img[35][currRotation],target = plots[6], source=((0,0),(plots[0],plots[0])),mask=img[2])
    #画唱针
    if pl.player.state() == audio.EPlaying:
        buf.blit(img[5],target = plots[8], source=((0,0),(plots[2] * 51 / 39, plots[2])),mask=img[6])
    else:
        buf.blit(img[7],target = plots[9], source=((0,0),(plots[2] ,plots[2] * 51 / 39)),mask=img[8])
    #redraw指定区域(是否还需要在之前重绘文字？)
    redraw((plots[8][0], plots[8][1], plots[9][0] + plots[2], plots[9][1] + plots[2] * 51 / 39))
    
    
def redraw(rect=(0,0,appuifw.Canvas().size[0],appuifw.Canvas().size[1])):
    #将buf最终blit到画布上
    global tabIndex, buf
    if tabIndex == 2:
        mainCanvas.blit(buf, target = (rect[0],rect[1]), source=((rect[0],rect[1]), (rect[2], rect[3])))
        
        
'''
画图函数结束
'''

definePlots()
FONT_MEDIUM = 18
FONT_SMALL = 14
logs(u'plots Defined')
'''
在播放器界面弹出的小提示框Toast的画图函数
包括下载进度的显示函数
'''

toastVisibility = False
def setToastVisible(visibility, needBlit = True):
    #显示或隐藏Toast，visibility分别为True或False
    global img, plots, toastVisibility, tmpWhetherThereIsProgressBar
    
    if (visibility ^ toastVisibility):
        toastVisibility = visibility
        if needBlit:
            if visibility:
                buf.blit(img[14], target = plots[13], mask=img[15])
            else:
                #img11: 临时图像，全黑供clear buf用
                img11 = graphics.Image.new(mainCanvas.size)
                img11.clear(0x303030)
                #给buf相应部分clear，然后重绘背景
                buf.blit(img11, target = plots[13], source=((0,0), (plots[11], plots[12])))
                buf.blit(img[10], target = plots[13], source=(plots[13], (plots[13][0] + plots[11], plots[13][1] + plots[12])), mask=img[11])
                #重画下面的三个图标
                try:
                    drawButtons()
                    aotimer3.cancel()
                    aotimer3.after(0, loopRotate)
                except:
                    pass
            
        redraw((plots[13][0], plots[13][1], plots[13][0] + plots[11], plots[13][1] + plots[12]))

def refreshToast():
    setToastVisible(False)
    setToastVisible(True)
    
def setToastText(strList, fontScale = 0.3, secondFontScale = 0.2):
    #设置Toast
    img[14].clear(0x000000)
    textHeight = fontScale + secondFontScale * 1.1 * (len(strList) -1)
    img[14].text((plots[11] *0.18, plots[12] * ((1-textHeight)/2 + fontScale)), strList[0],fill=0xffffff,font=("normal",plots[12]*fontScale,None))
    for k,v in enumerate(strList[1:]):        
        img[14].text((plots[11] *0.22, plots[12] * ((1-textHeight)/2 + fontScale + secondFontScale * 1.1 * (k+1)) ), v,fill=0xffffff,font=("normal",plots[12]*secondFontScale,None))
    refreshToast()
    
progRunning = False
def downProgWrapper(strList_):
    global img, plots, Pi
    global nowProg, nowTime, nowTimeGap, nowSpeed, nowSize, nowSizeGap, progRunning
    progRunning = False
    strList = copy.copy(strList_)
    def progBlit(percent, strList):
        if not foreground: return
        img[14].clear(0x000000)
        img[16].clear(0x000000)
        img[17].clear(0x000000)
        img[19].clear(0x000000)
        img[20].clear(0x000000)
        if percent != 0:
            img[16].pieslice((0,0,plots[14],plots[14]), Pi /2 - Pi * 2 * percent / 100, Pi /2, fill=0xFFFFFF)
        if percent == 100:percent = ''
        img[17].text((plots[14] * (1./2 - 1./(2*1.4142)), plots[14] * (1. / 2 + 1./ (2*1.4142))) , unicode(percent) ,fill=0xffffff,font=("normal",plots[14] / 1.4142,graphics.FONT_BOLD|graphics.FONT_ANTIALIAS) )
        img[19].blit(img[17])
        img[17].blit(img[20], mask=img[16])
        img[16].blit(img[17], mask=img[19])
        img[14].blit(img[16], target=(plots[11] *0.03, (plots[12] - plots[14])/2), mask=img[16])
        
        img[14].text((plots[11] *0.22, plots[12]*0.18 + plots[12]*0.24), strList[0],fill=0xffffff,font=("normal",plots[12]*0.2,None))
        for k,v in enumerate(strList[1:]):
            img[14].text((plots[11] *0.25, plots[12]*0.18 + plots[12]*0.24 +plots[12]*0.17*(k+1)), v,fill=0xffffff,font=("normal",plots[12]*0.15,None))
        refreshToast()
        
    def loopProg():
        global nowProg, nowTime, nowTimeGap, nowSpeed, nowSize, nowSizeGap, progRunning, nowBlockNum, nowBlockSize, nowTotalSize
        nowProg_ = nowProg
        nowTime_ = nowTime
        nowTimeGap_ = nowTimeGap
        nowSize_ = nowSize
        nowBlockNum_ = nowBlockNum
        nowBlockSize_ = nowBlockSize
        nowTotalSize_ = nowTotalSize
        strList = copy.copy(strList_)
        
        percent = nowBlockNum_ * nowBlockSize_ * 100 / nowTotalSize_
        # logs('percent: %s nowProg: %s ' % (percent, nowProg))
        if percent > 100:
            percent = 100
        totalinmb = float(nowTotalSize_) /1024 /1024
        if nowProg != percent:
            if nowBlockNum_ == 0:
                downToast = cn('%.2f MB, -- KB/s, -- %%, ') % (totalinmb  ) + cn('还剩 -- ')
                strList.append(downToast)
                progBlit(percent, strList)
            else:
                nowTimeGap = time.clock() - nowTime_
                nowTime = time.clock()
                nowSizeGap = nowBlockNum_ * nowBlockSize_ - nowSize_
                nowSize = nowBlockNum_ * nowBlockSize_ #每更新1%便刷新一次，以总文件的1%需要多少秒来计算即时速度
                if nowTimeGap != 0:
                    nowSpeed = float(nowSizeGap)/1024/nowTimeGap
                else:
                    nowSpeed = 1
                nowProg = percent
                downToast = cn('%.2f MB, %.2f KB/s, %s %%, ') % (totalinmb, nowSpeed, percent  ) + cn('还剩') + unicode(readableTime( long((nowTotalSize_ - nowBlockNum_ * nowBlockSize_) * 1. / (nowSpeed * 1024) * 1000) ))
                strList.append(downToast)
                progBlit(percent, strList)
        
        # e32.ao_yield()
        # logs('progRunning: %s percent: %s ' % (progRunning, percent))
        if progRunning:
            # logs('will refresh prog')
            # e32.ao_sleep(0.5, loopProg)
            aotimer4.cancel()
            aotimer4.after(0.8, loopProg)
        if percent == 100:
            progRunning = False
            setToastVisible(False)
            
        # e32.ao_yield()
        
    def downProgUpdater(blocknum, blocksize, totalsize):
        global nowProg, nowTime, nowTimeGap, nowSpeed, nowSize, nowSizeGap, progRunning, nowBlockNum, nowBlockSize, nowTotalSize
        nowBlockNum = blocknum
        nowBlockSize = blocksize
        nowTotalSize = totalsize
        if blocknum == 0:
            nowProg = -1
            nowTime = time.clock()
            nowTimeGap = 0
            nowSpeed = 0
            nowSize = -1
            nowSizeGap = 0
            progRunning = True
            loopProg()
            logs('Reset Progress Bar')
        # logs('updater: progress %s %s' % (nowBlockNum * nowBlockSize, nowTotalSize))
        e32.ao_yield()
        
    return downProgUpdater
    
    
'''
Toast结束
'''
'''
按钮控制
播放操作
'''
def selOrder():
    order = npl.order
    orderList = [cn('列表循环'), cn('单曲循环'), cn('随机播放')]
    orderList[order] = cn('→') + orderList[order]
    selOrderIndex = appuifw.popup_menu(orderList, cn('选择播放顺序'))
    if selOrderIndex is not None:
        if currentFM and selOrderIndex == 2:
            appuifw.note(cn('私人FM不能随机播放哦'))
            return
        npl.updateOrder(selOrderIndex)
        refreshButtonsStatus()
        setToastText([cn('成功选择') + orderList[npl.order]])
        # aotimer.cancel()
        e32.ao_sleep(1, lambda:setToastVisible(False))

def pressButton(buttonDict):
    global npl
    if buttonDict['type']==appuifw.EEventKey:
        try:
            if buttonDict['keycode']==key_codes.EKeySelect:
                pauseCont()
            if buttonDict['keycode']==key_codes.EKey5:
                pauseCont()
            if buttonDict['keycode']==key_codes.EKey4:
                prevSong()
            if buttonDict['keycode']==key_codes.EKey6:
                nextSong()
            if buttonDict['keycode']==key_codes.EKey2:
                volumeUp()
            if buttonDict['keycode']==key_codes.EKey8:
                volumeDown()
        except:
            pass
            
def pauseCont():
    if 'npl' in globals():
        npl.pauseCont()
        redrawPause(npl)
        # aotimer3.after(0, loopRotate)
        
def pause():
    if 'npl' in globals():
        npl.pause()
        redrawPause(npl)
        # aotimer3.after(0, loopRotate)
        
def cont():
    if 'npl' in globals():
        npl.cont()
        redrawPause(npl)
        # aotimer3.after(0, loopRotate)

songSwitchHangedon = False
def nextSong(manual = True):
    global checkLI, songSwitchHangedon
    logs_('nextSong, sSH: '+repr(songSwitchHangedon))
    if not songSwitchHangedon:
        if 'npl' in globals():
            songSwitchHangedon = True
            if not(currentFM):
                npl.next(manual)
            else:
                npl.nextFM(manual)
            checkLI = -3
            songSwitchHangedon = False
            
def prevSong():
    global checkLI, songSwitchHangedon
    logs_('prevSong, sSH: '+repr(songSwitchHangedon))
    if not songSwitchHangedon:
        if 'npl' in globals():
            songSwitchHangedon = True
            if not(currentFM):
                npl.previous()
            else:
                setToastText([cn('私人FM不能播放上一曲哦')])
                e32.ao_sleep(1, lambda:setToastVisible(False))
            checkLI = -3
            
            songSwitchHangedon = False
            
def volumeUp():
    if 'npl' in globals():
        npl.volumeAdjust(1)
        currConfig['volume'] = npl.volume
        writeConfig()
        setToastText([cn('音量 ') + unicode(npl.volume)])
        e32.ao_sleep(1, lambda:setToastVisible(False))
def volumeDown():
    if 'npl' in globals():
        npl.volumeAdjust(-1)
        currConfig['volume'] = npl.volume
        writeConfig()
        setToastText([cn('音量 ') + unicode(npl.volume)])
        e32.ao_sleep(1, lambda:setToastVisible(False))
    
def setVolume():
    inputVolume = appuifw.query(cn('输入音量(s60v3 0-10, s^3 0-10000)'), 'number', currConfig['volume'])
    if inputVolume==None:
        return
    currConfig['volume'] = inputVolume
    writeConfig()
    if 'npl' in globals():
        npl.volumeAdjustTo(currConfig['volume'])
        setToastText([cn('音量 ') + unicode(npl.volume)])
        currConfig['volume'] = npl.volume
        e32.ao_sleep(1, lambda:setToastVisible(False))
    appuifw.note(cn('成功。当前音量为 ') + unicode(currConfig['volume']))
    
def insertSong():
    currPlaylistIndex = currPlaylistListbox.current()
    try:
        if 'npl' in globals():
            npl.insertSong(currPlaylistIndex)
        refreshCurrPlaylist()
        # setToastText([cn('下一首播放设置成功')])
        # e32.ao_sleep(1, lambda:setToastVisible(False))
        appuifw.note(cn('下一首播放设置成功'))
    except Exception, e:
        printException(Exception, e, cn('ErrorWithinsertSong'))
        
#在播放暂停和切歌操作时audio自动调用的callback
#可以控制歌词界面的显示和是否刷新
currentPlaying = -1
def playCallback():
    global npl, lyricText, lyricCanvas, lyricPage, checkLI, currentPlaying, currRotation, drawRotationToWhere
    
    if (len(npl.songList) > (npl.songIndex) and npl.songList[npl.songIndex] != currentPlaying) or not(bool(npl.songList[npl.songIndex])) or currentPlaying == -1:
        logs_('id Different')
        if npl.isScroll == False:
            lyricPage = lyricText
            lyricText.set(cn(npl.lrcList))
        else:
            lyricPage = lyricCanvas
        currentPlaying = npl.songList[npl.songIndex]
        checkLI = -3
        currRotation = 0
        drawRotationToWhere = -1
        if tabType[3] == 0: tab[3] = lyricPage
        changeTabs()
        aotimer3.cancel()
        refreshButtonsStatus()
        redrawSong(npl)
        
        aotimer2.cancel()
        if npl.isScroll:refreshLyric()
        refreshCurrPlaylist()
    else:
        pass
        
def songCallback(prevState, nowState, errCode):
    logs('songCallback: %s, %s, %s' % (repr(prevState), repr(nowState), repr(errCode)))
    if prevState == audio.EPlaying and nowState == audio.EOpen:
        nextSong(False)
    else:
        refreshLyric()
        aotimer3.cancel()
        aotimer3.after(0, loopRotate)
        playCallback()
    
'''
按钮控制结束
'''

'''
关于UI的一系列函数
包括各个Tab的变换函数；切换界面（包括页面和左右键操作所调用的函数/菜单）；刷新界面等重要函数

tabIndex存储当前tab的编号
tab为各个tab对应页面组成数组
tabKey存储各个tab对应的左右选项键操作
tabBackup为界面的备份存储list，存储了之前状态的tab和tabKey，在退出当前一个界面后可以还原到上一个界面
'''
tabLabelOptions = [[cn('查找')], [cn('歌单'), cn('详情')],[cn('播放')],[cn('歌词'), cn('列表'), cn('评论')]]
def changeTabs(i = -1):
    global tabIndex, tabLabelOptions, tab
    #不带参数的时候可以用来在不清楚当前Tab是什么时刷新目标Tabs
    #删掉最左边
    if i != -1:
        i = i + 1
        tabIndex = i
    else:
        i = tabIndex
    refreshKeyHandler(i)
    appuifw.app.body = tab[i]

def refreshTabTag():
    tabLabels = [tabLabelOptions[x][tabType[x]] for x in [0,1,2,3]]
    logs(tabLabels)
    # appuifw.app.set_tabs(tabLabels,changeTabs)
    appuifw.app.set_tabs(tabLabels[1:],changeTabs)
    
    
def refreshAllTabs():
    #从python命令行载入这个py的时候会有错位，用这个refresh一下，可能打包后这个问题就不存在了
    for x in range(0,4-1):
        changeTabs(x)
    return
    pass
    
def printHandler():
    logs_('tab[2] exit_key_handler: (variable)' + repr(tabKey[2][1]))
    logs_('tabKey: ' + repr(tabKey))
    logs_('now exit_key_handler: (real)' + repr(appuifw.app.exit_key_handler))
    
#将tabKey中存储的左右选项键操作同步到当前的左右键
def refreshKeyHandler(i=-1):
    if i == -1:
        i = tabIndex
    appuifw.app.menu = tabKey[i][0]
    appuifw.app.exit_key_handler = tabKey[i][1]
    appuifw.app.menu_key_text = tabKey[i][2]
    appuifw.app.exit_key_text = tabKey[i][3]
    appuifw.app.menu_key_handler = tabKey[i][4]
    appuifw.app.title = tabKey[i][5]
    

    
#打开如评论详情的临时页面时候会备份页面到tabBackup，此处将其还原，一般用作tab的exit_key_handler
def tmpPageBackup(i, replaceExit = True, replaceExitText=cn('返回')):
    global tab, tabKey, tabBackup
    tabBackup[i].append((tab[i], copy.copy(tabKey[i])))
    if replaceExit:
        tabKey[i][1] = lambda:tmpPageRestore(i)
        tabKey[i][3] = replaceExitText
    refreshKeyHandler()
    
def tmpPageRestore(i):
    global tab, tabKey,  tabBackup
    tabRestore = tabBackup[i].pop()
    tab[i] = tabRestore[0]
    tabKey[i] = tabRestore[1]
    changeTabs(i-1)
    
def tmpPageRestoreAll(i):
    #还原所有的页面（撤销所有的临时窗口）并清空备份队列，用在需要切换Tab3类型的时候
    global tab, tabKey,  tabBackup
    #非空
    if tabBackup[i]:
        tabRestore = tabBackup[i][0]
        tab[i] = tabRestore[0]
        tabKey[i] = tabRestore[1]
        # tabBackup = [0,0,0,0]
        tabBackup[i] = []
        changeTabs(i-1)
'''
UI控制结束
'''

'''
程序各种实用功能相关函数，如联网、写入记录
'''

#读入接入点，没有就创建一个空文件
currConfig = {'ap': -1,  'username': '', 'password': '', 'cellphone': False, 'volume':1, 'bps':96000, 'api':1}
def loadConfig():
    global currConfig
    if not os.path.exists('e:\\netease\\data\\config.txt'):
        writeConfig()
        
    else:
        file1=open('e:\\netease\\data\\config.txt','r')
        currConfig = json.loads(file1.read())
        file1.close()
    return currConfig
    
def writeConfig():
    file1=open('e:\\netease\\data\\config.txt','wb')
    file1.write(json.dumps(currConfig))
    file1.close()
    
#写入接入点
def writeAp(str1):
    global currConfig
    currConfig['ap'] =  int(str1)
    writeConfig()
    
#删掉接入点记录文件
def delAp():
    writeAp('-1')
    return None
    
#对一个url发送一次HTTP请求，返回Tuple
def rawHttpReq(url):
    urlhost = url.split("/")[2]
    conn1 = httplib.HTTPConnection(urlhost, 80, 3)
    conn1.request(method, url, params, header)
    resp1=conn1.getresponse()
    result = (resp1.getheader('set-cookie'), resp1.read())
    conn1.close()
    return result
    
    
#测试网络，成功后开始播放歌曲
def checkComm():
    global nma, npl, apo
    #nma和npl 是本程序中关于 api 和 playlist 的两个实例
    logs('Start Checking Network')
    connectivity = False
    currAp = currConfig['ap']
    if currAp==None or currAp==-1:
        currAp = selAp()
    if currAp != -1:
        apo = socket.access_point(int(currAp))
        socket.set_default_access_point(apo)
        # apo.start()
        try:
            conn1 = httplib.HTTPConnection('music.163.com', 80, 3)
            conn1.request('GET', 'http://music.163.com/api/song/lyric?id=0&lv=-1&kv=-1&tv=-1', '', {})
            resp1=conn1.getresponse()
            conn1.close()
            connectivity = True
        except:
            # apo.stop()
            appuifw.note(cn('不能连接网络！'))
    return connectivity
        
#选择接入点
def selAp(tip=False):
    currAp = socket.select_access_point()
    if currAp==None:
        appuifw.note(cn('你没有选择！'))
        currAp = -1
    else:
        writeAp(currAp)
        # tabKey[2][0] = menu1
        # tabKey[1][0] = menu1
        refreshKeyHandler()
    return currAp
    
    
def setBps():
    if not(appuifw.query(cn('选择音质需要重启后生效，并且所有音乐需要重新缓冲播放。确定？'),'query')):return
    if not(appuifw.query(cn('另外，由于服务器限制，选择160Kbps以上音质用旧API有很大概率无法有效下载播放。继续选择吗？'),'query')):return
    bpsValues = [96000, 128000, 160000, 320000]
    bpsTexts = [u'96Kbps', u'128Kbps', u'160Kbps', u'320Kbps']
    bpsIndex = bpsValues.index(currConfig['bps'])
    bpsTexts[bpsIndex] = cn('→') + bpsTexts[bpsIndex]
    newBpsIndex = appuifw.popup_menu(bpsTexts, cn('选择音质'))
    if newBpsIndex == None:return
    currConfig['bps'] = bpsValues[newBpsIndex]
    writeConfig()
    appuifw.note(cn('选择音质') + bpsTexts[newBpsIndex] + cn('成功'))
    
def helpText():
    appuifw.query(cn('网易云音乐Python S60 Alpha版\n目前支持歌单播放、私人FM等功能。'),'query')
    appuifw.query(cn('进入界面后选择左选单中的‘启动连接’，将登录并获取每日推荐歌单信息。'),'query')
    appuifw.query(cn('主界面分三个标签页，分别为【歌单】【播放器】 【列表、歌词、评论】。'),'query')
    appuifw.query(cn('播放器页内（s60v3）：\nOK, 5-播放暂停, 2, 8-音量增减\n4, 6-上曲下曲'),'query')
    appuifw.query(cn('s60v5和s^3机型注意，这些机型的音量数目最高是10000，而v3是10。'),'query')
    appuifw.query(cn('本程序照顾s60v3机型，所以高版本机型请在设置-播放设置-音量调节以满分10000按比例调节音量。'),'query')
    
def aboutText():
    appuifw.query(cn('网易云音乐PyS60_1 0.0.9版\nBy 顺\n 2022-11-28 紫星修复'),'query')

def selAPI():
    appuifw.query(cn('新的API修复部分音乐的高音质，但造成下架音乐无法读取和下载歌曲IDv3信息错误，还会使加载速度变慢。'),'query')
    appuifw.query(cn('旧的API不支持部分歌曲的高音质，但是对于低音质几乎所有歌曲都能读取。'),'query')
    
    apiList = [cn('旧Api'), cn('新Api')]
    apiList[(0,1)[currConfig['api']]] = cn('→') + apiList[(0,1)[currConfig['api']]]
    apiSel = appuifw.popup_menu(apiList, cn('启用API'))
    if apiSel == None: return
    currConfig['api'] = int(apiSel)
    writeConfig()
    tmpStr = (cn('旧'),cn('新'))[apiSel]
    appuifw.note(cn('换用') + tmpStr + cn('API成功。'))
    
    
def settings():
    settingsList = [
        [cn('播放设置'), [[cn('音量大小'), setVolume],[cn('音质设置'), setBps]]],
        [cn('账号设置'), [[cn('更换账号'), getLoginData]]],
        [cn('连接设置'), [[cn('切换接入点'), lambda:selAp(True)], [cn('更换API'), selAPI]]],
        [cn('清除缓存'), [[cn('清除缓存并退出'), clearCache]]],
        [cn('帮助关于'), [[cn('帮助'), helpText], [cn('关于'), aboutText]]],
        
    ]
    setSel=[0,0]
    while True:
        #第一层
        setSel[0] = appuifw.popup_menu([x[0] for x in settingsList], cn('设置'))
        if setSel[0] == None:
            break
        currSettList = settingsList[setSel[0]]
        while True:
            #第二层
            setSel[1] = appuifw.popup_menu([x[0] for x in currSettList[1]], currSettList[0])
            if setSel[1] == None:
                break
            else:
                currSettList[1][setSel[1]][1]()
            
        
    
'''
实用功能结束
'''
'''
与具体功能有关的函数1
'''

def getLoginData():
    global currConfig
    username = appuifw.query(cn('登录邮箱或手机：'), 'text', currConfig['username'])
    if username==None: return (-1,-1,-1)
    password = appuifw.query(cn('密码：'), 'code', currConfig['password'])
    if password==None: return (-1,-1,-1)
    if appuifw.query(cn('是否用的手机号码登录？\n 是->确认  否 ->取消'), 'query'):
        cellphone = True
    else:
        cellphone = False
    currConfig['username'] = username
    currConfig['password'] = password
    currConfig['cellphone'] = cellphone
    
    writeConfig()
    
    file1=open('e:\\netease\\data\\cookie.txt','wb')
    file1.write('')
    file1.close()
    
    return (username, password, cellphone)

def login():
    global nma
    logs('Start Logining')
    loginUsername = currConfig['username']
    if not loginUsername:
        loginUsername, loginPassword, loginCellphone = getLoginData()
        if loginUsername  == -1:return -1
    else:
        loginPassword = currConfig['password']
        loginCellphone = currConfig['cellphone']
    try:
        nma = api.NEApi(loginUsername,loginPassword,loginCellphone, False, bool(currConfig['api']))
        if nma.loginSucceed == False:
            raise Exception
    except Exception, e:
        printException(Exception, e, cn('ErrorWithLogin'))
        # currConfig['username'] = ''
        # currConfig['password'] = ''
        # currConfig['cellphone'] = False
        # writeConfig()
        return -1
    return 0

def getUserPLs():
    global userPlaylists, userCreatePLs, userSubPLs
    logs('Getting UserPLs')
    userCreatePLs = []
    userSubPLs = []
    try:
        userPlaylists = nma.getUserPLs()['playlist']
        for x in userPlaylists:
            if x['subscribed']:
                userSubPLs.append(x)
            else:
                userCreatePLs.append(x)
    except Exception, e:
        printException(Exception, e, cn('ErrorWithgetUserPLs'))
        

def updateUserPLs():
    if showCreatePLs:
        playlistListbox_ = [x['name'] for x in userCreatePLs]
    else:
        playlistListbox_ = [x['name'] for x in userSubPLs]
    playlistListbox.set_list(playlistListbox_)
    
def refreshUserPLs():
    getUserPLs()
    updateUserPLs()
    
def loadPlaylist(startNow = True, playlistIDInput = -1):
    global toastIndex, currentPlaying, currentFM
    playlistIndex = playlistListbox.current()
    currentFM = False
    
    
    toastList = [cn('暂停播放器'), cn('获取歌单信息'), cn('获取下载地址并创建播放列表'), cn('播放第一首歌')]
    toastTitle = cn('加载中')
    toastIndex = 0
    currentPlaying = -1
    
    if playlistIDInput == -1:
        if showCreatePLs:
            playlistDict_ = userCreatePLs[playlistIndex]
        else:
            playlistDict_ = userSubPLs[playlistIndex]
        playlistId = playlistDict_['id']
        if playlistDict_['trackCount'] > 70:
            if not(appuifw.query(cn('歌单过大，若点播需要较长的时间载入和分析数据，几百首歌的歌单甚至可能需要几分钟。确定点播吗？'), 'query')):
                return
    else:
        playlistId = playlistIDInput
    try:
        appuifw.app.activate_tab(2-1)
        changeTabs(2-1)
        toastNext(toastTitle, toastList)
        if npl.player:
            pause()
        toastNext(toastTitle, toastList)
        playlistDict = nma.getPlaylist(playlistId)
        toastNext(toastTitle, toastList)
        npl.updateListByDict(playlistDict['tracks'])
        npl.setPlaylistName(cn(playlistDict['name']))
        toastNext(toastTitle, toastList)
        refreshCurrPlaylist()
        if startNow:firstSong()
        setToastVisible(False)
        
    except Exception, e:
        printException(Exception, e, cn('ErrorWithloadPlaylist'))

currentFM = False
def loadFM(startNow = True):
    global currentFM, toastIndex
    currentFM = True
    toastList = [cn('暂停播放器'), cn('获取私人FM信息'), cn('播放第一首歌')]
    toastTitle = cn('私人FM准备中')
    toastIndex = 0
    try:
        appuifw.app.activate_tab(2-1)
        changeTabs(2-1)
        toastNext(toastTitle, toastList)
        if npl.player:
            pause()
        toastNext(toastTitle, toastList)
        npl.initFM()
        npl.setPlaylistName(cn('私人FM'))
        toastNext(toastTitle, toastList)
        if startNow:firstSong()
        setToastVisible(False)
        
    except Exception, e:
        printException(Exception, e, cn('ErrorWithloadFM'))
        
def dailyRec(startNow = True):
    global toastIndex
    toastList = [cn('暂停播放器'), cn('获取推荐信息'), cn('获取下载地址并创建播放列表'), cn('播放第一首歌')]
    toastTitle = cn('加载中')
    toastIndex = 0
    try:
        appuifw.app.activate_tab(2-1)
        changeTabs(2-1)
        toastNext(toastTitle, toastList)
        if npl.player:
            pause()
        toastNext(toastTitle, toastList)
        playlistDict = nma.getRecomPL()
        toastNext(toastTitle, toastList)
        npl.updateListByDict(playlistDict)
        npl.setPlaylistName(cn('每日推荐'))
        toastNext(toastTitle, toastList)
        if startNow:firstSong()
        setToastVisible(False)
        
    except Exception, e:
        printException(Exception, e, cn('ErrorWithdailyRec'))
        
def loadSong():
    global songSwitchHangedon, checkLI
    # appuifw.note(cn('正在载入歌曲，切换到播放标签页可以看到进度……'))
    currPlaylistIndex = currPlaylistListbox.current()
    try:
        if not songSwitchHangedon:
            if 'npl' in globals():
                songSwitchHangedon = True
                refreshCurrPlaylist(True, currPlaylistIndex)
                npl.pickupPlay(currPlaylistIndex)
                checkLI = -3
                songSwitchHangedon = False
            # refreshCurrPlaylist()
            # appuifw.app.activate_tab(2-1)
            # changeTabs(2-1)
    except Exception, e:
        printException(Exception, e, cn('ErrorWithloadSong'))
        
def firstSong():
    if len(npl.songList) != 0:
        npl.firstSong()
    else:
        appuifw.note(cn('这个列表没有歌哦，去点播另一个列表吧'))
    
    
def playlistDetail(whetherGetSongs = False):
    global nma, npl, tab, tabType
    playlistIndex = playlistListbox.current()
    if showCreatePLs:
        playlistDict = userCreatePLs[playlistIndex]
    else:
        playlistDict = userSubPLs[playlistIndex]
    
    
    createTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(playlistDict['createTime'] / 1000))
    updateTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(playlistDict['updateTime'] / 1000))
    
    plDetailTitles  = ['列表名称','创建用户','是否自创','创建时间','更新时间','订阅次数','歌曲数目','播放次数']
    plDetailContents =  [playlistDict['name'], playlistDict['creator']['nickname'],['是', '否'][playlistDict['subscribed']], createTime, updateTime,  playlistDict['subscribedCount'], playlistDict['trackCount'],  playlistDict['playCount']]
    
    if whetherGetSongs:
        plDetailTitles.append('')
        plDetailContents.append('曲目列表')
        e32.ao_sleep(0,lambda:appuifw.note(cn('请耐心等待，获取曲目信息中')))
        playlistSongsDict = nma.getPlaylist(playlistDict['id'])['tracks']
        appuifw.note(cn('获取曲目信息成功'))
        for i, song in enumerate(playlistSongsDict):
            plDetailTitles.append(unicode(i))
            
            tmpPLDetailContent = cn(song['name']) + u' - ' + cn(song['artists'][0]['name'])
            if len(song['artists']) > 1: tmpPLDetailContent += cn('等')
            plDetailContents.append(tmpPLDetailContent)
        
    tmpPageBackup(1)
    plDetailListbox = detailInfoTable(plDetailTitles, plDetailContents)
    tab[1] = plDetailListbox
    tabKey[1][0] = [(cn('查看详情'), lambda:(lambda i:None)(detailInfoListbox.current()))]
    tabKey[1][5] = cn('歌单详情')
    appuifw.app.activate_tab(1-1)
    changeTabs(1-1)
    refreshKeyHandler()
    
   
def switchPlaylist():
    global showCreatePLs
    showCreatePLs = not(showCreatePLs)
    updateUserPLs()
        
def getFirstPlaylist():
    global playlistDict
    logs('Getting FirstPlaylist')
    try:
        playlistDict = nma.getRecomPL()
        # playlistDict = nma.getPlaylist(431670482)['tracks']
    except Exception, e:
        printException(Exception, e, cn('ErrorWithgetFirstPlaylist'))
        
def createNpl():
    global npl
    npl = playlist.Playlist([], nma, 0, 73, currConfig['bps'], currConfig['volume'])
    npl.updateListByDict(playlistDict)
    npl.setPlaylistName(cn('每日推荐'))
    npl.downCallbackWrapper = downProgWrapper
    npl.writeCallbackWrapper = downProgWrapper
    npl.playCallback = playCallback
    npl.songCallback = songCallback
    npl.errCallback = lambda:appuifw.note(cn('出现常见网络错误，文件可能不完整！'))
    npl.picSize = plots[0]
    
def detailInfoTable(titleList, valueList):
    #用来显示详细信息列表，返回要传递给app.body的listbox实例
    if len(titleList) != len(valueList): raise ValueError, u'titleList s length dont equal to valueList s'
    
    def viewDetailInfoItem():
        try:
            detailInfoListboxCurrent = detailInfoListbox.current()
            appuifw.query(titleList[detailInfoListboxCurrent], 'text', valueList[detailInfoListboxCurrent])
        except:
            pass
        
    
    titleList = cnList(titleList)
    valueList = cnList(valueList)
    
    # titleMaxLength = max([getStringWidth(x) for x in titleList])
    # titleList_ = [fillUnicodeByWidth(x, titleMaxLength) for x in titleList]
    
    detailInfoList = map(lambda x,y:x+u': '+y, titleList, valueList)
    if detailInfoList == []: detailInfoList = [cn('没有信息')]
    detailInfoListbox = appuifw.Listbox(detailInfoList, viewDetailInfoItem)
    
    return detailInfoListbox

    
def likeSong():
    songIndex = npl.songIndex
    likeResult = nma.like(npl.songList[songIndex], True)
    if likeResult.get('songs') == []:
        #表示之前没有喜欢
        #待添加异常处理
        refreshButtonsStatus()
        setToastText([cn('喜欢成功')])
        
    else:
        #之前已经喜欢了
        likeResult = nma.like(npl.songList[songIndex], False)
        refreshButtonsStatus()
        setToastText([cn('取消喜欢成功')])
        
    #已经隐含了刷新三个按钮图标的任务
    # aotimer.cancel()
    e32.ao_sleep(1, lambda:setToastVisible(False))
    
def favoriteSong():
    songIDList = [npl.songList[npl.songIndex]]
    playlistIndex = playlistListbox.current()
    if showCreatePLs:
        playlistID = userCreatePLs[playlistIndex]['id']
    else:
        playlistID = userSubPLs[playlistIndex]['id']
    manCode = nma.manipulatePlaylist(playlistID, songIDList, 'add')
    if manCode == -1:
        appuifw.note(cn('收藏成功'))
    elif manCode == 502:
        appuifw.note(cn('收藏失败。好像已经收藏过了'))
    else:
        appuifw.note(cn('收藏失败。错误码：') + unicode(manCode))
        
    
def favoriteSong_ById(songId):
    songIDList = [songId]
    playlistIndex = playlistListbox.current()
    if showCreatePLs:
        playlistID = userCreatePLs[playlistIndex]['id']
    else:
        playlistID = userSubPLs[playlistIndex]['id']
    manCode = nma.manipulatePlaylist(playlistID, songIDList, 'add')
    if manCode == -1:
        appuifw.note(cn('收藏成功'))
    elif manCode == 502:
        appuifw.note(cn('收藏失败。好像已经收藏过了'))
    else:
        appuifw.note(cn('收藏失败。错误码：') + unicode(manCode))
    
def deleteSong():
    #待完成。
    pass
    
def saveSong():
    try:
        e32.ao_sleep(0,npl.saveSong)
        appuifw.note(cn('复制歌曲文件需要一段时间，请稍微等候'))
    except:
        pass
        
def favorPlaylist():
    plId = appuifw.query(cn('输入歌单ID'), 'number')
    if plId==None: return
    favorResult = nma.favorPlaylist(plId)
    if favorResult==200:
        appuifw.note(cn('收藏歌单成功！'))
    else:
        appuifw.note(cn('收藏失败！错误代码') + unicode(favorResult))
    refreshUserPLs()
    pass
    
def betaFunc():
    #应设置检测输入非空
    funcTexts = [cn('搜索'), cn('收藏歌单'),cn('输入歌单ID播放'),cn('输入ID收藏曲目')]
    funcCalls = [search, favorPlaylist,lambda:loadPlaylist(True, appuifw.query(cn('输入歌单ID'), 'number')),lambda:favoriteSong_ById(appuifw.query(cn('输入曲目ID'), 'number'))]
    funcIndex = appuifw.popup_menu(funcTexts, cn('测试功能'))
    if funcIndex == None:return
    funcCalls[funcIndex]()
    
def search():
    codeMap  = [1,10,100,1000,1002]
    keyMap = ['songs', 'albums', 'artists', 'playlists', 'userprofiles']
    queryString = appuifw.query(cn('搜索关键字：'),'text',cn('歌曲'))
    if not queryString :return None
    queryString = nc(queryString)
    searchTypeList = [cn('歌曲'),cn('专辑'),cn('歌手'),cn('歌单'),cn('用户')]
    queryType = appuifw.popup_menu(searchTypeList, cn('你要搜索什么 ？'))
    if queryType==None: return None
    queryKey = keyMap[queryType]
    queryType = codeMap[queryType]
    searchResult = nma.search(queryString, queryType)[queryKey]
    resultNameList = [cn(x['name']) for x in searchResult]
    resultIdList = [cn(x['name'])+ cn(', ID=') + cn(x['id']) for x in searchResult]
    appuifw.query(resultIdList[appuifw.popup_menu(resultNameList, cn('搜索结果'))], 'query')
    # if queryType == 1:
        
    
def songInfo(songIndex = -1):
    global nma, npl, tab, tabType
    if songIndex == -1:
        songIndex = npl.songIndex
    else:
        songIndex = currPlaylistListbox.current()
    songDict = npl.listdetail[songIndex]
    try:
        duration = npl.player.duration() / 1000
    except:
        duration = songDict['duration']
    duration = readableTime(duration, True, True)
    if 'reason' in songDict.keys():
        reason = songDict['reason']
    else:
        reason = '无'
    try:
        alias = u', '.join([cn(x) for x in songDict.get('alias')])
        artists = '& '.join([x['name'] for x in songDict['artists']])
        
        songInfoTitles = ['曲名','歌手','专辑','碟片序号','轨道序号','长度','ID','人气值','推荐理由','别名','MP3路径','专辑图路径','歌词路径']
        songInfoContents = [songDict['name'],artists,songDict['album']['name'],songDict['disc'],songDict['no'],duration,songDict['id'],songDict['popularity'],reason,alias,npl.songPath,npl.picPath,npl.lrcPath]
        
        tmpPageBackup(tabIndex)
        detailInfoListbox = detailInfoTable(songInfoTitles, songInfoContents)
        tab[tabIndex] = detailInfoListbox
        tabKey[tabIndex][0] = [(cn('查看详情'), lambda:(lambda i:None)(detailInfoListbox.current()))]
        tabKey[tabIndex][5] = cn('歌曲详情')
        appuifw.app.activate_tab(tabIndex-1)
        changeTabs(tabIndex-1)
    except Exception, e:
        printException(Exception, e, cn('ErrorWithsongInfo'))
'''
具体函数结束
'''

'''
与评论有关的函数
'''
def commSel():
    global tabType, commListbox, CommList, CommTitle, tabKey, tabBackup, tab
    CommIndex = commListbox.current()
    if len(CommList) == 0: return
    stars = (cn('☆'), cn('★'))
    replying = (cn(''), cn('[回复]'))
        
    Text = '%s: \n%s(%s, %s)\n%s%s\n' % (cn(CommList[CommIndex]['user']['nickname']), cn(CommList[CommIndex]['content']), time.strftime('%Y-%m-%d %H:%M', time.localtime(CommList[CommIndex]['time'] / 1000)), fuzzyTime( CommList[CommIndex]['time'] / 1000 ), stars[CommList[CommIndex]['liked']], unicode(CommList[CommIndex]['likedCount']))
    
    if len(CommList[CommIndex]['beReplied']) != 0:
        Text += cn('回复: \n"')
        Text += '%s: \n%s\n' % (cn(CommList[CommIndex]['beReplied'][0]['user']['nickname']), cn(CommList[CommIndex]['beReplied'][0]['content']))
        Text += cn('"')
    tmpPageBackup(3)
    tab[3] = appuifw.Text_display(text=Text, skinned=True)
    tabKey[3][0] = commDetailMenu
    tabKey[3][5] = cn('评论详情')
    changeTabs(3-1)
    refreshKeyHandler()
    
commListbox = appuifw.Listbox([(u'List1', u'List1Desc')], commSel)
CommList = []
tabBackup = [[],[],[],[]]
commMenu = [(cn('下一页'), lambda:commOper(0)), (cn('上一页'), lambda:commOper(1)), (cn('跳转'), lambda:commOper(2)), (cn('点赞/取消点赞'), lambda:commOper(3))]
commDetailMenu = [(cn('点赞/取消点赞'), lambda:commOper(3)),(cn('复制评论'), lambda:commOper(4))]
#仅针对最新评论
commOffset = 0
commLimit = 10
#commOper
#0: 下一页
#1: 上一页
#2: 跳转
#3: 点赞/取消点赞
def commOper(operNo):
    global commViewingId, CommIndex, CommList, threadId, CommType, commOffset, commLimit, totalNum
    if len(CommList) == 0: return
    try:
        if CommType == 0:
            if operNo == 0:
                if haveMore:
                    commOffset += commLimit
                    viewCommWrapper(CommType, -2, threadId)()
            if operNo == 1:
                if commOffset >= commLimit:
                    commOffset -= commLimit
                    viewCommWrapper(CommType, -2, threadId)()
                else:
                    commOffset = 0
                    viewCommWrapper(CommType, -2, threadId)()
        if operNo == 2:
            currpage = int(math.ceil(commOffset * 1. / commLimit))
            totalpage = int(math.ceil(totalNum * 1. / commLimit))
            queryString = cn('当前#') + cn(str(commOffset +1))
            queryString += cn('@页') + cn(str(currpage +1))
            queryString += cn('，共#') + cn(str(totalNum)) + cn('@页.') + cn(str(totalpage)) + cn('\n')
            queryString += cn('跳到第几页？')
            jumpToPage = appuifw.query(queryString, 'number', 1)
            if jumpToPage and jumpToPage >= 1 and jumpToPage <= totalpage:
                jumpToPage -= 1
                commOffset = jumpToPage * 10
                viewCommWrapper(CommType, -2, threadId)()
        if operNo == 3:
            CommIndex = commListbox.current()
            favorSuc, favorMsg_ = nma.favorComment(CommList[CommIndex]['commentId'], threadId, not(CommList[CommIndex]['liked']))
            favorMsg = [cn('点赞'), cn('取消点赞')][CommList[CommIndex]['liked']] + [cn('失败'), cn('成功')][favorSuc]
            if not(favorSuc):
                favorMsg = favorMsg + cn('，返回信息或代码：') + favorMsg_
            appuifw.note(favorMsg)
        if operNo == 4:
            CommIndex = commListbox.current()
            appuifw.query(cn('复制评论'), 'text', cn(CommList[CommIndex]['content']))
    except Exception, e:
        printException(Exception, e, cn('ErrorWithcommOper'))
    
def viewPLCommWrapper(hot = False):
    def viewPLComm():
        playlistIndex = playlistListbox.current()
        if showCreatePLs:
            playlistDict = userCreatePLs[playlistIndex]
        else:
            playlistDict = userSubPLs[playlistIndex]
        viewCommWrapper(hot, -2, playlistDict['commentThreadId'], playlistDict['name'])()
    return viewPLComm
            
def viewCommWrapper(hot=False, songid=-1, threadid='_', additionalParam = ''):
    def viewComm():
        global nma, npl, tab3Type, commListbox, CommList, CommType, threadId, commMenu, tabKey
        global commOffset, commLimit, totalNum, haveMore, commViewingId
        #从主界面调用的时候不传songId，默认为-1即换歌的标志，于是offset和limit恢复为初始状态
        #当在查看歌手/专辑等非歌曲的评论时，可以换为-2，此时根据threadId来获取评论
        
        threadId = threadid
        songId = songid
        if songId == -1:
            songId = currentPlaying
            commOffset = 0
            commLimit = 10
        commViewingId = songId
        commOffset_ = commOffset
        if hot:commOffset_ = 0
        
        (hotCommList, ordCommList, totalnum, havemore) = nma.getComments(commViewingId, threadId, commOffset_, False, commLimit)
        
        totalNum = totalnum
        haveMore = havemore
        
        if threadId == '_':
            threadId = 'R_SO_4_%s' % commViewingId

        if hot:
            CommList = hotCommList
            CommType = 1
            #CommType : 1=Hot, 0=Latest
        else:
            CommList = ordCommList
            CommType = 0
        stars = (cn('☆'), cn('★'))
        replying = (cn(''), cn('[回复]'))
        listboxList = [
            ( cn(x['content']), 
                fuzzyTime( x['time'] / 1000 ) + u', ' + stars[x['liked']] + str(x['likedCount']) + u' ' + cn(x['user']['nickname']) + replying[bool(x['beReplied'])]
            ) for x in CommList
            ]
        if not listboxList: listboxList = [(cn('没有评论'), cn('未获取到评论'))]
        commMenu = [(cn('下一页'), lambda:commOper(0)), (cn('上一页'), lambda:commOper(1)), (cn('跳转(') + cn(str(totalNum)) + cn(')'), lambda:commOper(2)), (cn('点赞/取消点赞'), lambda:commOper(3))]
        tabType[3] = 2
        
        refreshTabTag()
        tmpPageRestoreAll(3)
        tabKey[3][0] = commMenu
        if threadId[0:6] == 'R_SO_4':
            commTitleText = cn('歌曲评论:"') + cn(npl.listdetail[npl.songIndex]['name']) + u'"'
        elif threadId[0:6] == 'A_PL_0':
            commTitleText = cn('歌单评论:"') + cn(additionalParam) + u'"'
        elif threadId[0:6] == 'R_AL_3':
            commTitleText = cn('专辑评论:"') + cn(additionalParam) + u'"'
        else:
            commTitleText = cn('评论')
        tabKey[3][5] = commTitleText
        commListbox.set_list( listboxList )
        tab[3] = commListbox
        appuifw.app.activate_tab(3-1)
        changeTabs(3-1)
    return viewComm
'''
评论有关函数结束
'''

'''
歌词有关函数
'''
lyricMenu = [(cn('待加'), lambda:None)]
def viewLyric():
    global tabType
    global tab
    tabType[3] = 0
    
    refreshTabTag()
    tab[3] = lyricPage
    tabKey[3][0] = lyricMenu
    tabKey[3][5] = cn('网易云音乐')
    appuifw.app.activate_tab(3-1)
    changeTabs(3-1)
    if npl.isScroll:
        aotimer2.cancel()
        aotimer2.after(0.2, refreshLyric)
    
#scale: 歌词字体高度对应屏幕高度的比例
#height: 绝对高度
#line: 换行时的间隔 等于height+行距
#width
lyricScale = 1. / 15
lyricHeight = plots[4][1] * lyricScale
lyricLine = lyricHeight * 1.125
lyricWidth = lyricHeight /2.125
lyricMaxCharPerLine = int(plots[4][0] / lyricWidth) - 5

lyricLineGap = plots[4][1] * lyricScale *2 /3
 
tlyricScale = 1. / 18
tlyricHeight = plots[4][1] * tlyricScale
tlyricLine = tlyricHeight * 1.125
tlyricWidth = tlyricHeight / 2.125
tlyricMaxCharPerLine = int(plots[4][0] / tlyricWidth) -3

lyricBuf = graphics.Image.new(appuifw.Canvas().size)
def lyricBlit(currLrc):
    global plots, lyricBuf
    #根据屏幕大小来给7句歌词分配显示空间
    #这个很烦，因为要考虑歌词换行，歌词翻译……
    #先处理最中间的歌词 currLrc[0] = ('Lyric', 'TranslatedLyric')
    centralLyric = currLrc[0]
    
    #将每句歌词按照屏幕宽度劈成几行
    currLyricSplitted = splitUnicodeByWidth(cn(centralLyric[0]), lyricMaxCharPerLine)
    if centralLyric[1]:
        currTLyricSplitted = splitUnicodeByWidth(cn(centralLyric[1]), tlyricMaxCharPerLine)
    else:
        currTLyricSplitted = []
    
    #歌词行（包括翻译）的总高度
    lyricTotalHeight = len(currLyricSplitted) * lyricLine + len(currTLyricSplitted) * tlyricLine
    tlyricHeightOffset = len(currLyricSplitted) * lyricLine
    
    lyricBuf.clear(0x303030)
    lyricBuf.blit(img[10],mask=img[11])
    for i, v in enumerate(currLyricSplitted):
        start_y = plots[4][1] / 2 - lyricTotalHeight / 2 + (i+1) * lyricLine
        start_x = plots[4][0] / 2 - (lyricWidth * getStringWidth_(v)) / 2
        lyricBuf.text( (start_x, start_y ) , v , fill=0xbbffbb, font=('normal', lyricHeight, None) )
    for i, v in enumerate(currTLyricSplitted):
        start_y = tlyricHeightOffset + plots[4][1] / 2 - lyricTotalHeight / 2 + (i+1) * tlyricLine
        start_x = plots[4][0] / 2 - (tlyricWidth * getStringWidth_(v)) / 2
        lyricBuf.text( (start_x, start_y ) , v , fill=0xbbffbb, font=('normal', tlyricHeight, None) )
    lyricInitialOffset = lyricTotalHeight / 2 + lyricLineGap
    lyricOffset = lyricInitialOffset
    #现在开始处理当前歌词往前的歌词
    for prevLyric in currLrc[1]:
        currLyricSplitted = splitUnicodeByWidth(cn(prevLyric[0]), lyricMaxCharPerLine)
        if prevLyric[1]:
            currTLyricSplitted = splitUnicodeByWidth(cn(prevLyric[1]), tlyricMaxCharPerLine)
        else:
            currTLyricSplitted = []
        lyricTotalHeight = len(currLyricSplitted) * lyricLine + len(currTLyricSplitted) * tlyricLine
        tlyricHeightOffset = len(currLyricSplitted) * lyricLine
        
        for i, v in enumerate(currLyricSplitted):
            start_y = plots[4][1] / 2 - lyricOffset - lyricTotalHeight + (i+1) * lyricLine
            start_x = plots[4][0] / 2 - (lyricWidth * getStringWidth_(v)) / 2
            lyricBuf.text( (start_x, start_y ) , v , fill=0xffffff, font=('normal', lyricHeight, None) )
        for i, v in enumerate(currTLyricSplitted):
            start_y = tlyricHeightOffset + plots[4][1] / 2 - lyricOffset - lyricTotalHeight + (i+1) * tlyricLine
            start_x = plots[4][0] / 2 - (tlyricWidth * getStringWidth_(v)) / 2
            lyricBuf.text( (start_x, start_y ) , v , fill=0xffffff, font=('normal', tlyricHeight, None) )
        lyricOffset += lyricTotalHeight + lyricLineGap
        
    lyricOffset = lyricInitialOffset
    #现在开始处理当前歌词往后的歌词
    for nextLyric in currLrc[2]:
        currLyricSplitted = splitUnicodeByWidth(cn(nextLyric[0]), lyricMaxCharPerLine)
        if nextLyric[1]:
            currTLyricSplitted = splitUnicodeByWidth(cn(nextLyric[1]), tlyricMaxCharPerLine)
        else:
            currTLyricSplitted = []
        lyricTotalHeight = len(currLyricSplitted) * lyricLine + len(currTLyricSplitted) * tlyricLine
        tlyricHeightOffset = len(currLyricSplitted) * lyricLine
        
        for i, v in enumerate(currLyricSplitted):
            start_y = plots[4][1] / 2 + lyricOffset + (i+1) * lyricLine
            start_x = plots[4][0] / 2 - (lyricWidth * getStringWidth_(v)) / 2
            lyricBuf.text( (start_x, start_y ) , v , fill=0xffffff, font=('normal', lyricHeight, None) )
        for i, v in enumerate(currTLyricSplitted):
            start_y = tlyricHeightOffset + plots[4][1] / 2 + lyricOffset + (i+1) * tlyricLine
            start_x = plots[4][0] / 2 - (tlyricWidth * getStringWidth_(v)) / 2
            lyricBuf.text( (start_x, start_y ) , v , fill=0xffffff, font=('normal', tlyricHeight, None) )
        lyricOffset += lyricTotalHeight + lyricLineGap
    #处理完毕
    
def updateTextLyric():
    global npl, lyricText
    lrcText = cn(npl.lrcList)
    tab[3] = lyricText
    lyricText.set(lrcText)
    changeTabs()

currLrc = [(cn(' - NetEase Cloud Music - '),None),[],[]]
currLI = -1
lyricText = appuifw.Text_display(text=cn(''), skinned=True)
#checkLI十分重要，它是用来判断歌词内容有没有修改的，换歌时也要修改它的值为-3来更新歌词内容
checkLI = -3
def redrawLyric(rect = None):
    global currLrc, currLI, checkLI, lyricText
    if tabType[3] == 0 and 'npl' in globals():
        currLI = npl.getCurrLyric()
        if currLI == -2:
            #非滚动歌词，不需要blit
            checkLI = currLI
            #updateTextLyric()
        else:
            if currLI == -1:
                if checkLI >= 0:
                    currLI = checkLI
                else:
                    currLI = 0
            if checkLI != currLI:
                checkLI = currLI
                minLI = max(0, currLI-5)
                maxLI = min(len(npl.lrcList) -1, currLI+5)
                #currLrc 的格式：[当前歌词tuple, [当前歌词之前的歌词tuple（最多5条）], [之后的歌词tuple]]
                #并且前后歌词按照从中往外的顺序排序
                tmpRange = range(minLI, currLI)
                tmpRange.reverse()
                tmpRange2 = range(maxLI, currLI, -1)
                tmpRange2.reverse()
                currLrc = [npl.lrcList[currLI][1], [npl.lrcList[i][1] for i in tmpRange], [npl.lrcList[i][1] for i in tmpRange2]]
                #这样就生成了本条及前后的最多11条歌词（若当前歌词位于靠近头/尾的部分则可能少于）
                lyricBlit(currLrc)
    if tabIndex ==3 and tabType[3] == 0 and currLI != -2:
            lyricCanvas.blit(lyricBuf)

def refreshLyric():
    if tabType[3] == 0:
        if npl.isScroll:
            if npl.player and npl.player.state() == audio.EPlaying and foreground:
                redrawLyric()
                aotimer2.cancel()
                aotimer2.after(0.2, refreshLyric)
            
'''
歌词有关函数结束
'''

'''
与显示当前播放列表有关的函数
'''



def refreshCurrPlaylist(busy = False, songIndex = -1):
    global currPlaylistListbox
    currPlaylist = [appuifw.Item(cn(x['name'])) for x in npl.listdetail]
    symbol = (cn('→ '), cn('◎ '))[busy]
    if songIndex == -1:
        songIndex = npl.songIndex
    currPlaylist[songIndex].title = symbol + currPlaylist[songIndex].title
    currPlaylistListbox.begin_update()
    currPlaylistListbox.clear()
    for x in currPlaylist:
        currPlaylistListbox.append(x)
    currPlaylistListbox.set_current(songIndex)
    currPlaylistListbox.end_update()
    tabKey[3][5] = cn(npl.playlistName)
    
def viewCurrPlaylist():
    global tabType, tab, tabKey
    try:
        refreshCurrPlaylist()
        tabType[3] = 1

        refreshTabTag()
        tmpPageRestoreAll(3)
        tabKey[3][0] = currPLMenu
        tabKey[3][5] = cn('播放列表')
        tabKey[3][5] = cn(npl.playlistName)
        tab[3] = currPlaylistListbox
        appuifw.app.activate_tab(3-1)
        changeTabs(3-1)
    except Exception, e:
        printException(Exception, e)
        
def playlistSearch():
    searchQuery = appuifw.query(cn('输入要查找的关键字'), 'text', cn('歌曲'))
    if not searchQuery : return None
    searchResult = []
    for i, songDict in enumerate(npl.listdetail):
        songName = cn(songDict['name'])
        if songName.find(searchQuery) != -1:
            searchResult.append((i, songName))
    if searchResult:
        searchSel = appuifw.popup_menu([x[1] for x in searchResult])
        if searchSel != None:
            resultIndex = searchResult[searchSel][0]
            currPlaylistListbox.set_current(resultIndex)

def playlistJump():
    jumpQuery = appuifw.query(cn('跳到第几条歌曲？'), 'number', cn('询问'))
    if not(jumpQuery) or jumpQuery <= 0 or jumpQuery > len(npl.listdetail): return None
    jumpQuery = jumpQuery -1
    currPlaylistListbox.set_current(jumpQuery)
    
    
'''
程序流程控制函数
  负责在用户执行某些操作后按一定顺序执行功能函数
'''
def toastNext(toastTitle, toastList):
    global toastIndex
    currToastList = [toastTitle]
    if toastIndex - 1 < 0:
        prevToast = ''
    else:prevToast = toastList[toastIndex - 1]
    if toastIndex + 1 >= len(toastList):
        nextToast = ''
    else:
        nextToast = toastList[toastIndex + 1]
    currToastList[1:] = [prevToast, toastList[toastIndex], nextToast]
    currToastList[2] = currToastList[2] + u'...'
    if currToastList[1] != '':currToastList[1] = currToastList[1] + u'OK'
    setToastText(currToastList, 0.22, 0.18)
    toastIndex += 1

#在菜单处点开始连接调用的函数，此时将检测网络并执行登录、获取歌单等操作
def startConn():
    global toastIndex, currConfig
    toastList = [cn('测试网络'), cn('登录'), cn('获取用户歌单信息'), cn('加载每日推荐歌单'), cn('获取下载地址并创建播放列表'), cn('播放第一首歌')]
    toastTitle = cn('启动中')
    toastIndex = 0
    toastNext(toastTitle, toastList)
    connectivity = checkComm()
    if not connectivity: return None
    toastNext(toastTitle, toastList)
    loginReturn = login()
    if loginReturn == -1:
        currConfig['username'] = ''
        currConfig['password'] = ''
        writeConfig()
        setToastVisible(False)
        return None
        
    toastNext(toastTitle, toastList)
    refreshUserPLs()
    toastNext(toastTitle, toastList)
    
    getFirstPlaylist()
    createNpl()
    toastNext(toastTitle, toastList)
    # firstSong()
    setToastVisible(False)

    tabKey[2][0] = menu2
    tabKey[1][0] = menu3
    viewCurrPlaylist()
    refreshKeyHandler()
    
def clearCache(exit = True):
    clearCache_()
    if exit:
        main_Exit(False)
    
#退出时需执行的操作：释放lock，停止音乐播放等
def main_Exit(confirm = True):
    if confirm:
        whetherExit = appuifw.query(cn('您确定要退出吗？'), 'query')
        if progRunning and whetherExit:
            whetherExit = appuifw.query(cn('有文件正在下载，退出可能导致文件损坏播放出错，需要清除缓存才能解决！确定退出？'), 'query')
    else:
        whetherExit = True
    
    if whetherExit:
        logs('===== End ======')
        writeConfig()
        aotimer3.cancel()
        aotimer4.cancel()
        aotimer2.cancel()
        aotimer.cancel()
        if 'npl' in globals():
            if npl.player:
                npl.player.stop()

        # if 'apo' in globals():
            # apo.stop()
        aolock.signal()
        appuifw.app.set_exit()
    
foreground = True
def switchForeground(whetherForeground):
    global foreground
    if whetherForeground:
        foreground = True
        try:
            refreshLyric()
            loopRotate()
        except:
            logs('refresh Error')
    else:
        foreground = False
        splashScreen.hide()
        
logs(u'functions Defined')
#正文开始

try:
    try:
        #设定好tabs和几个画图函数
        aolock = e32.Ao_lock()
        #aotimer: 用于toast的显隐
        aotimer = e32.Ao_timer()
        #aotimer2: 用于歌词
        aotimer2 = e32.Ao_timer()
        #aotimer3: 用于旋转唱盘
        aotimer3 = e32.Ao_timer()
        #aotimer4: 用于下载进度条
        aotimer4 = e32.Ao_timer()
        appuifw.app.exit_key_handler = main_Exit
        #各个tab下的菜单键触发菜单和退出键的callback
        tabKeyMother = [[], main_Exit, cn('选项'), cn('退出'), lambda:None, cn('网易云音乐')]
        tabKey = [copy.copy(tabKeyMother) for i in range(0,4)]
        tab=[None, None, None, None]
        tabKey[1][5] = cn('我的歌单')
        # tabKey[3][5] = cn('歌词')
                
        loadConfig()
                
        logs_('Start Loading UI')
        appuifw.app.title = cn('网易云音乐')
        appuifw.app.focus = switchForeground
        tabIndex = 0
        #画图
        #tab3可以是歌词页面0、播放列表页面1、评论页面2等

        playlistListbox = appuifw.Listbox([cn('Playlist1')], loadPlaylist)
        currPlaylistListbox = appuifw.Listbox2([], loadSong)
        

        menu1 = [(cn('启动连接'), startConn), (cn('更改登录账户'), getLoginData),(cn('设置'), settings),]
        menu2 = [
            (cn('播放控制'), ((cn('播放/暂停'), pauseCont), (cn('下曲'), nextSong), (cn('上曲'), prevSong), (cn('播放顺序'), selOrder), (cn('音量加'), volumeUp), (cn('音量减'), volumeDown))),
            (cn('歌曲信息'), songInfo),
            (cn('歌词'), viewLyric),
            (cn('喜欢/取消喜欢'), likeSong),
            (cn('评论'), ((cn('热门评论'), viewCommWrapper(True)), (cn('最新评论'), viewCommWrapper()))),
            (cn('播放列表'), viewCurrPlaylist),
            (cn('保存歌曲'), saveSong),
            (cn('设置'), settings),
            (cn('退出'), main_Exit),
        ]
        menu3 = [(cn('详细信息'), ((cn('显示曲目信息'),lambda:playlistDetail(True)), (cn('不显示曲目信息'),lambda:playlistDetail()))), (cn('操作'), ((cn('播放'), loadPlaylist), (cn('收藏当前曲目到此'), favoriteSong),(cn('刷新我的歌单'), refreshUserPLs)  )), (cn('自创/收藏 切换'), switchPlaylist) ,(cn('评论'), ((cn('热门评论'), viewPLCommWrapper(True)), (cn('最新评论'), viewPLCommWrapper()))), (cn('每日推荐'), lambda:dailyRec()), (cn('私人FM'), lambda:loadFM()), (cn('测试功能'), betaFunc),]
        
        currPLMenu = [(cn('播放'), loadSong), (cn('下一首播放'), insertSong), (cn('歌曲信息'), lambda:songInfo(0)), (cn('查找'), playlistSearch), (cn('跳转'), playlistJump)]

        tabType=[0,0,0,0]
        lyricCanvas = appuifw.Canvas(redraw_callback=redrawLyric)
        lyricPage = lyricCanvas
        tab[3] = lyricPage
        mainCanvas = appuifw.Canvas(redraw_callback=redraw, event_callback=pressButton)
        tab[2] = mainCanvas
        #貌似应该把Canvas的定义放在前面，因为Canvas定义以后即使没有赋值给body也会绘出，而且是错位的，疑似bug
        tab[0] = appuifw.Text(cn('初始界面：选单'))
        tab[1] = playlistListbox

        initDraw()
        
        #开始载入用户界面
    
        # appuifw.app.set_tabs([cn('找单'),cn('歌单'),cn('播放'),cn('歌词')],changeTabs)
        appuifw.app.set_tabs([cn('歌单'),cn('播放'),cn('歌词')],changeTabs)
        appuifw.app.activate_tab(2-1)

        showCreatePLs = True

        tabKey[2][0] = menu1
        tabKey[1][0] = menu1
        refreshAllTabs()
        changeTabs(2-1)
        redraw()
        logs_('End Drawing UI')
        splashScreen.hide()
        aolock.wait()
        #菜单载入完成
    except Exception, e:
        printException(Exception, e, str(e))
finally:
    pass
    # main_Exit()