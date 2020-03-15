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

#所有界面状态
class AllForm:
    def __init__(self):
        #主界面
        self.main = 1
        #菜单
        self.menu = 2

class ithomeUi(object, ):
    def __init__(self, path):
        self.TitleName = "IThome"
        self.running = 1
        self.selectedIndex = 0
        self.loading = 0
        ui.app.screen = "full"
        self.menuL = [(cn("刷新"), lambda: self.refush()),
                      (cn("到顶部"), lambda: self.toTop()),
                      (cn("清除缓存"), lambda: self.delCache()),
                      (cn("退出"), lambda: self.exit2())]

        screen = ui.app.layout(ui.EScreen)[0]

        self.width = screen[0]
        self.height = screen[1]
        self.img = ph.Image.new((self.width, self.height))
        self.background = ph.Image.new((self.width, self.height))
        self.bgcolor = 0xeeeeee
        self.selectedColor = 0xbbbbbb
        self.background.clear(self.bgcolor)
        self.x = -1
        self.y = 0
        self.baseCornor = 5
        self.newsCornor = 2
        self.SlideHeight = 80
        self.SlideWidth = self.width - self.baseCornor * 2
        self.newsHeight = 60
        self.newImgHeight = self.newsHeight - self.newsCornor * 2
        self.newImgWidth = int(self.newImgHeight/0.75)
        self.loadingImg = ph.Image.open(mypath+"image_loading.jpg").resize((self.newImgWidth,self.newImgHeight))

        self.maskImg = Image.new(screen, "L")
        self.maskImg.clear(0x888888)

        self.newsWidth = self.width - self.baseCornor * 2
        self.SlideIndex = 0
        self.nowtime=0
        self.__canvas = ui.Canvas(self.__redraw, self.key)
        ui.app.body = self.__canvas
        self.imgOld = Image.new(screen)
        self.startUpImg = ph.Image.open(path)
        self.img.blit(self.startUpImg)

        itnet.newImgHeight = self.newImgHeight
        itnet.newImgWidth = self.newImgWidth
        itnet.SlideHeight = self.SlideHeight
        itnet.SlideWidth = self.SlideWidth
        self.allForm = AllForm()
        self.menuIndex = 0
        self.minMenuWidth = 0
        self.menuHeight = 35

        self.menuSpeed = 5
        self.RunningForm = self.allForm.main
        self.AsyncLoad(10)
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.slideChangeThread = e32.Ao_timer()
        self.genMenuList()
        self.lastX=self.selectedIndex-1
        itnet.loadImg(self.AsyncLoad)

    def AsyncLoad(self,percent):
        self.background.blit(self.startUpImg)
        x1=10
        y1=self.height-80
        x2=self.width-10
        y2=self.height-60
        self.background.rectangle((x1,y1,x2,y2),0xc3c3c3,fill=0xc3c3c3)

        x2 = ((self.width-20)*(float(percent)/float(100)))+10
        self.background.rectangle((x1, y1, x2, y2), 0x20C602,  fill = 0x20C602)

        self.img.blit(self.background)
        self.blit(self.img)
        if(percent>=100):
            self.lastX = self.selectedIndex - 1
            self.redraw()
            self.slideChangeThread.after(3,self.slideChange)
    def slideChange(self):
        if(self.RunningForm == self.allForm.main):
            self.SlideIndex += 1
            if (self.SlideIndex >= len(self.SlideList)):
                self.SlideIndex = 0
            self.redraw()
        self.slideChangeThread.after(3, self.slideChange)


    def delCache(self):  # 清除缓存
        ui.note(cn('清除成功！'))

    def refush(self):  # 刷新
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.lastX = self.selectedIndex - 1
        #itnet.loadImg(self.AsyncLoad)
        self.redraw()

    def blit(self, img):
        self.__canvas.blit(img)

    def genImg(self):
        if (self.x == -1):
            self.drawMain()
        else:
            if (self.lastX != self.selectedIndex):
                self.background.clear(self.bgcolor)
                self.drawNewsList()
        self.lastX = self.selectedIndex

    def __redraw(self, size=0):  # 重绘界面
        self.blit(self.img)

    def redraw(self):  # 重绘界面
        if(self.loading == 1):
            return
        self.loading = 1
        #self.img.blit(self.background, (0, 0))
        if(self.RunningForm ==  self.allForm.main):
            self.genImg()
            self.__redraw()
            self.imgOld.blit(self.img)
        elif(self.RunningForm ==  self.allForm.menu):
            self.drawMenu()
        self.loading = 0

    def drawSlide(self):  # 绘制顶部滚动图
        if(len(self.SlideList)<1):
            return
        if (self.nowtime >= 1):
            self.nowtime = 0
            self.SlideIndex += 1
        if (self.SlideIndex >= len(self.SlideList)):
            self.SlideIndex = 0
        imgurl = self.SlideList[self.SlideIndex].image
        self.SlideImg = itnet.getPic(imgurl, (self.SlideWidth, self.SlideHeight))
        # self.SlideImg.clear(0xff0000)
        timg = ph.Image.new((self.width,  self.SlideHeight + self.baseCornor))
        timg.clear(self.bgcolor)
        self.background.blit(timg, (0, 0))
        self.img.blit(timg, (0, 0))
        del timg
        self.background.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))
        self.img.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))

    def drawMain(self):  # 绘制第一页主页
        self.background.clear(self.bgcolor)
        self.drawSlide()
        if(self.lastX != self.selectedIndex):
            self.drawNewsList()

    def genNewsListImg(self):
        showNewsCount = int(self.height / self.newsHeight) + 1  # 要显示的新闻数量
        NewsListImg = []
        if(len(self.newsList.newslist)<1):
            return NewsListImg
        for i in range(showNewsCount):
            nowIndex = i + self.x
            if (nowIndex < 0):
                continue
            if (nowIndex >= len(self.newsList.newslist)):
                break
            imgurl = self.newsList.newslist[nowIndex].image
            newimg = ph.Image.new((self.newsWidth, self.newsHeight))
            #print nowIndex,self.selectedIndex
            if(self.x == -1):
                if(nowIndex  == self.selectedIndex):
                    newimg.clear(self.selectedColor)
            else:
                if (nowIndex+1 == self.selectedIndex):
                    newimg.clear(self.selectedColor)

            # print itnet.getPic(imgurl)
            newTopImg = itnet.getPic(imgurl, (self.newImgWidth, self.newImgHeight))

            #newTopImg = self.loadingImg
            # newTopImg1.clear(0xff0000)
            newimg.blit(newTopImg, (0 - self.newsCornor, 0 - self.newsCornor))
            del newTopImg
            textBasePos = (self.newsCornor * 2 + self.newImgWidth , self.newsCornor)
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
        timg=ph.Image.new((self.width,self.height-self.SlideHeight))
        timg.clear(self.bgcolor)
        self.background.blit(timg,(0,0-self.SlideHeight-self.baseCornor))
        del timg
        self.background.rectangle((2, nowX - 2, self.width - 2, nowX + self.newsCornor * 2 - 2 + self.newsHeight), self.selectedColor,
                           fill=self.selectedColor)
        newListImg = self.genNewsListImg()
        for i in range(len(newListImg)):
            self.background.blit(newListImg[i], (
            0 - self.NewsBasePos[0], 0 - (self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2))))
            self.background.line((self.NewsBasePos[0], self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2),
                           self.NewsBasePos[0] + self.newsWidth,
                           self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2)), 0xdddddd, width=1)
        self.img.blit(self.background)
        del newListImg

    def toTop(self):  # 到顶部
        self.RunningForm = self.allForm.main
        while(self.selectedIndex>0):
            self.selectedIndex -= 1
            if (self.selectedIndex < 0):
                self.selectedIndex = 0
            if (self.selectedIndex < self.x + 1):
                self.x -= 1
            if (self.x < -1):
                self.x = -1
            sleep(0)
            self.redraw()

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

    def textLen(self, content=u'', font='dense'):
        length = self.img.measure_text(content, font)[0]
        return length[2]

    def genMenuList(self):
        self.listName = []
        self.listEvent = []
        index = 1
        for i in self.menuL:
            self.listName.append(cn(str(index) + '. ') + i[0])
            self.listEvent.append(i[1])
            index += 1
        self.RealMenuWidth = self.getMenuWidth()
        self.RealMenuHeight = len(self.listName) * self.menuHeight

    def drawMenu(self):
        self.loading = 1
        menuPos = 0
        if(self.RunningForm == self.allForm.main):
            while(menuPos<self.RealMenuWidth):
                menuPos+=self.menuSpeed
                #menuPos = self.RealMenuWidth
                self._drawMenu(menuPos)
                self.__redraw()
        elif(self.RunningForm == self.allForm.menu):
            self._drawMenu(self.RealMenuWidth)
            self.__redraw()
        self.loading = 0

    def closeMenu(self):
        self.loading = 1
        menuPos = self.RealMenuWidth
        while (menuPos > 0):
            menuPos -= self.menuSpeed
            # menuPos = self.RealMenuWidth
            self._drawMenu(menuPos)
            self.__redraw()

        self.loading = 0
    def getMenuWidth(self):
        l = self.minMenuWidth
        for i in self.listName:
            t=self.textLen(i)
            if(l<t):
                l=t
            if(l>self.width):
                return self.width
        return l


    def _drawMenu(self,menuPos):
        #self.imgOld.blit(self.img)
        self.img.clear(0X0)
        self.img.blit(self.imgOld,mask=self.maskImg)

        imgTemp = ph.Image.new((self.RealMenuWidth,self.RealMenuHeight))
        imgTemp.clear(0)
        for i in range(len(self.listName)):
            color = 0xffffff
            if(i==self.menuIndex):
                color = 0xff0000
            imgTemp.text((5,i*self.menuHeight + self.menuHeight/2 + 5), self.listName[i],color , zt)

        x=0-(menuPos - self.RealMenuWidth)
        y=0-(self.height - self.RealMenuHeight)
        #print x,y
        self.img.blit(imgTemp,(x,y))
        del imgTemp

    def InvokeMenu(self):
        self.listEvent[self.menuIndex]()
    def key(self, event):
        if (self.loading == 1):
            return
        key = event["keycode"]
        scan = event["scancode"]
        type = event["type"]
        if scan == 164 and type == 3:
            if(self.RunningForm ==  self.allForm.main):
                self.drawMenu()
                self.RunningForm =  self.allForm.menu
            elif(self.RunningForm ==  self.allForm.menu):
                self.InvokeMenu()
                self.lastX = -1
                self.RunningForm = self.allForm.main
        if (key == 0x32 or key == 63497):
            if (self.RunningForm == self.allForm.main):
                self.selectedIndex -= 1
                if (self.selectedIndex < 0):
                    self.selectedIndex = 0
                if (self.selectedIndex < self.x + 1):
                    self.x -= 1
                if (self.x < -1):
                    self.x = -1
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex-=1
                if(self.menuIndex<0):
                    self.menuIndex =len(self.listName)-1

        elif (key == 0x38 or key == 63498):
            if (self.RunningForm == self.allForm.main):
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
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex += 1
                if (self.menuIndex > len(self.listName)-1):
                    self.menuIndex = 0

        self.redraw()
    def exit2(self):
        if ui.query(cn("要退出吗？"), "query"):
            self.running = 0
            os.abort()

    def exit(self):
        if(self.RunningForm == self.allForm.main):
            if ui.query(cn("要退出吗？"), "query"):
                self.running = 0
                os.abort()
        elif(self.RunningForm == self.allForm.menu):
            self.closeMenu()
            self.RunningForm = self.allForm.main
            self.lastX = -1
            self.redraw()


# app=App(mypath+'splash.png',0)
ithome = ithomeUi(mypath + 'splash.png')
ithome.TitleName = cn("IT之家")
# app.keyType=0
ithome.main()
ui.app.exit_key_handler = ithome.exit
e32.Ao_lock().wait()
