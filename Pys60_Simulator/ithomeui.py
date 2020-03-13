# -*- coding: utf-8 -*-

zt = u"Sans MT 936_s60", 15, 1
import appuifw as ui, e32
import os
import graphics as ph, base64, thread, os, random
# from BingyiApp import *
import akntextutils2
from graphics import *

cn = lambda x: x.decode("u8")
sleep = e32.ao_sleep
mypath = u"..\\python\\pysoft\\ithome\\"
if (os.name != 'nt'):
    mypath = u"e:\\python\\pysoft\\ithome\\"
cachePath = mypath + "cache\\"
import ithomenet

itnet = ithomenet.IthomeNet()


class ithomeUi(object, ):
    def __init__(self, path):
        self.running = 1
        self.selectedIndex = 0
        self.loading = 0
        ui.app.screen = "full"
        self.menuL = [(cn("刷新"), lambda: self.refush()),
                      (cn("到顶部"), lambda: self.toTop()),
                      (cn("清除缓存"), lambda: self.delCache()),
                      (cn("退出"), lambda: self.exit())]
        screen = ui.app.layout(ui.EScreen)[0]

        self.width = screen[0]
        self.height = screen[1]
        self.img = ph.Image.new((self.width, self.height))
        self.background = ph.Image.new((self.width, self.height))
        self.background.clear(0xeeeeee)
        self.x = -1
        self.y = 0
        self.baseCornor = 5
        self.newsCornor = 2
        self.SlideHeight = 80
        self.newsHeight = 60
        self.newImgHeight = self.newsHeight - self.newsCornor * 2
        self.newImgWidth = self.newImgHeight
        self.newsWidth = self.width - self.baseCornor * 2
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.SlideIndex = 0
        self.__canvas = ui.Canvas(self.__redraw, self.key)
        ui.app.body = self.__canvas
        self.blit(ph.Image.open(path))

    def delCache(self):  # 清除缓存
        pass

    def refush(self):  # 刷新
        pass

    def blit(self, img):
        self.__canvas.blit(img)

    def genImg(self):
        if (self.x == -1):
            self.drawMain()
        else:
            self.drawNewsList()

    def __redraw(self, size=0):  # 重绘界面
        self.blit(self.img)

    def redraw(self):  # 重绘界面
        self.img.blit(self.background, (0, 0))

        self.genImg()
        self.__redraw()

    def drawSlide(self):  # 绘制顶部滚动图
        if (self.nowtime >= 1):
            self.nowtime = 0
            self.SlideIndex += 1
        if (self.SlideIndex >= len(self.SlideList)):
            self.SlideIndex = 0
        self.SlideWidth = self.width - self.baseCornor * 2
        imgurl = self.SlideList[self.SlideIndex].image
        self.SlideImg = itnet.getPic(imgurl, (self.SlideWidth, self.SlideHeight))
        # self.SlideImg.clear(0xff0000)
        self.img.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))

    def drawMain(self):  # 绘制第一页主页
        self.drawSlide()
        self.drawNewsList()

    def genNewsListImg(self):
        showNewsCount = int(self.height / self.newsHeight) + 1  # 要显示的新闻数量
        NewsListImg = []
        for i in range(showNewsCount):
            nowIndex = i + self.x
            if (nowIndex < 0):
                continue
            if (nowIndex >= len(self.newsList.newslist)):
                break
            imgurl = self.newsList.newslist[nowIndex].image
            newimg = ph.Image.new((self.newsWidth, self.newsHeight))
            # print itnet.getPic(imgurl)
            newTopImg = itnet.getPic(imgurl, (self.newImgWidth, self.newImgHeight))
            # newTopImg1.clear(0xff0000)
            newimg.blit(newTopImg, (0 - self.newsCornor, 0 - self.newsCornor))
            del newTopImg
            textBasePos = (self.newsCornor * 2 + self.newImgHeight, self.newsCornor)
            textWidth = self.newsWidth - self.newImgWidth + 30
            textHeight = self.newsHeight - self.newsCornor * 2
            title = self.newsList.newslist[nowIndex].title
            titlelist = akntextutils2.to_array(title, "dense", textWidth)
            for j in range(len(titlelist)):
                newimg.text((textBasePos[0], textBasePos[1] + (j + 1) * 15), titlelist[j], 0x0,
                            ("dense", 15, FONT_ANTIALIAS))
            NewsListImg.append(newimg)
            del newimg
        return NewsListImg

    def drawNewsList(self):  # 绘制下面的新闻列表
        self.NewsBasePos = (0, 0)
        if (self.x == -1):
            self.NewsBasePos = (self.baseCornor, self.SlideHeight + self.baseCornor * 2)
        else:
            self.NewsBasePos = (self.baseCornor, self.baseCornor)
        nowX = self.NewsBasePos[1] + (self.selectedIndex - self.x - 1) * (self.newsHeight + self.newsCornor * 2)
        col = 0xee0000
        self.img.rectangle((2, nowX - 2, self.width - 2, nowX + self.newsCornor * 2 - 2 + self.newsHeight), col,
                           fill=col)
        newListImg = self.genNewsListImg()

        for i in range(len(newListImg)):
            self.img.blit(newListImg[i], (
            0 - self.NewsBasePos[0], 0 - (self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2))))
            self.img.line((self.NewsBasePos[0], self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2),
                           self.NewsBasePos[0] + self.newsWidth,
                           self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2)), 0xdddddd, width=1)
        del newListImg

    def toTop(self):  # 到顶部
        pass

    def main(self):
        self.nowtime = 0
        self.redraw1()
        # while 1:
        #    self.drawMain()
        #    e32.ao_yield()
        #    sleep(0.05)

    def redraw1(self):
        self.img.blit(self.background, (0, 0))
        self.redraw()
        # self.img.save("d:\\a.png")
        self.nowtime += 0.1

    def key(self, event):
        if (self.loading == 1):
            return
        key = event["keycode"]
        scan = event["scancode"]
        type = event["type"]
        if scan == 164 and type == 3:
            pass
            # 菜单
            # app.menu(self.menuL)
        if (key == 0x32 or key == 63497):
            self.selectedIndex -= 1
            if (self.selectedIndex < 0):
                self.selectedIndex = 0
            if (self.selectedIndex < self.x + 1):
                self.x -= 1
            if (self.x < -1):
                self.x = -1
        elif (key == 0x38 or key == 63498):
            self.selectedIndex += 1
            if (self.selectedIndex > len(self.newsList.newslist)):
                self.selectedIndex = len(self.newsList.newslist)
            if (self.x == -1):
                if (self.selectedIndex > self.x + int(self.height / self.newsHeight) - 2):
                    self.x += 1
            else:
                if (self.selectedIndex > self.x + int(self.height / self.newsHeight) - 1):
                    self.x += 1
            t = int(self.height / self.newsHeight) - 1
            if (self.x > len(self.newsList.newslist) - t):
                self.x = len(self.newsList.newslist) - t
        self.loading = 1
        self.redraw()
        self.loading = 0

    def exit(self):
        if ui.query(cn("要退出吗？"), "query"):
            self.running = 0
            os.abort()


# app=App(mypath+'splash.png',0)
app = ithomeUi(mypath + 'splash.png')
app.TitleName = cn("IT之家")
# app.keyType=0
app.main()
ui.app.exit_key_handler = app.exit
e32.Ao_lock().wait()
