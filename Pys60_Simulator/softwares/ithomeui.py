# -*- coding: utf-8 -*-
import pys60Core
zt = u"Sans MT 936_s60", 15, 1
import thread
import graphics as ph, appuifw as ui, e32
# from BingyiApp import *
# import akntextutils2
import math
from graphics import *
#import fontSize

cn = lambda x: x.decode("u8")
sleep = e32.ao_sleep

import mypath

mypath = mypath.getmypath("\\python\\pysoft\\ithome\\")

cachePath = mypath + "cache\\"
import ithomenet

itnet = ithomenet.IthomeNet()


# 所有界面状态
class AllForm:
    def __init__(self):
        # 加载界面
        self.loading = 0
        # 主界面
        self.main = 1
        # 菜单
        self.menu = 2
        # 读文章
        self.article = 3
        # 刷新的加载界面
        self.refushLoading = 4


class ithomeUi(object, ):
    def __init__(self, path):
        self.TitleName = "IThome"
        self.running = 1
        ui.app.exit_key_handler = self.exit
        # 当前选择项目的index
        self.selectedIndex = 0
        self.loading = 0
        ui.app.screen = "full"

        self.articleMenuL = [(cn("刷新"), self.refushArticle),
                             (cn("清除缓存"), self.delCache),
                             (cn("退出"), self.exit2)]
        self.mainMenu = [(cn("刷新"), self.refush),
                         (cn("到顶部"), self.toTop),
                         (cn("到底部"), self.toBottom),
                         (cn("清除缓存"), self.delCache),
                         (cn("退出"), self.exit2)]

        self.menuL = self.mainMenu

        self.lock = e32.Ao_lock()
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
        self.newImgWidth = int(self.newImgHeight / 0.75)
        self.loadingImg = ph.Image.open(mypath + "image_loading.jpg").resize((self.newImgWidth, self.newImgHeight))
        self.articleContent = ""
        self.maskImg = Image.new(screen, "L")
        self.maskImg.clear(0x888888)
        self.deepMaskImg = Image.new(screen, "L")
        self.deepMaskImg.clear(0x333333)

        self.newsWidth = self.width - self.baseCornor * 2
        self.SlideIndex = 0
        self.nowtime = 0
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
        # 是否在刷新界面
        self.isRefush = 0
        # 文章最顶部高度
        self.articleMinIndex = 5
        # 文章index
        self.articleIndex = self.articleMinIndex
        # 文章上下走动的step
        self.articleStep = 60
        self.articleMinStep = 10
        self.articleMaxIndex = self.height + self.articleStep
        self.tempImg = ph.Image.new((1, 1))
        self.menuSpeed = 40
        self.RunningForm = self.allForm.loading
        self.drawAsyncLoad(10)
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.fontSizeCache = {}
        self.slideChangeThread = e32.Ao_timer()
        #self.refushListThread = e32.Ao_timer()
        self.genMenuList()
        self.lastRunningForm = self.RunningForm
        self.lastX = self.selectedIndex - 1
        itnet.loadImg() 
        self.AsyncLoad()

    def refushArticleThread(self):
        self.articleIndex = self.articleMinIndex

        newsid = self.newsList.newslist[self.selectedIndex].newsid
        self.NewsContent = itnet.getNewsContent(newsid)

        self.articleTime = self.newsList.newslist[self.selectedIndex].postdate.replace('T', ' ').split('.')[0]
        newsid = self.newsList.newslist[self.selectedIndex].newsid
        self.newsauthor = self.NewsContent.newssource + ' ( ' + self.NewsContent.newsauthor + ' ) '
        self.articleDetial = self.NewsContent.detail.replace('<p>', '  ').replace('</p>', '\n')

        #sleep(0.5)
        self.isRefush = 0
        self.RunningForm = self.allForm.article
        self.lastRunningForm = self.RunningForm

    def refushArticle(self):
        self.loading = 1
        self.isRefush = 1
        thread.start_new_thread(self.refushArticleThread, ())
        self.drawRefushLoading()
        self.loading = 0

    def drawAsyncLoad(self,precent):
        self.background.blit(self.startUpImg)
        x1 = 10
        y1 = self.height - 80
        x2 = self.width - 10
        y2 = self.height - 60
        self.background.rectangle((x1, y1, x2, y2), 0xc3c3c3, fill=0xc3c3c3)
        # print(percent)
        x2 = ((self.width - 20) * (float(precent) / float(100))) + 10
        self.background.rectangle((x1, y1, x2, y2), 0x20C602, fill=0x20C602)
        self.img.blit(self.background)
        self.blit(self.img)

    def AsyncLoad(self):

        lastprecent = 0
        nowprecent  = itnet.loadingPrecent

        while(1):

            nowprecent = itnet.loadingPrecent
            if(lastprecent == nowprecent and lastprecent<100 and nowprecent<100):
                sleep(0.1)
                e32.ao_yield()
                continue
            itnet.resizePic(itnet.nowUrl[0], itnet.nowUrl[1])
            self.drawAsyncLoad(nowprecent)
            if (nowprecent >= 100):
                self.loading = 0
                self.RunningForm = self.allForm.main
                self.lastRunningForm = self.RunningForm
                self.lastX = self.selectedIndex - 1
                self.redraw()
                self.slideChangeThread.after(3, self.slideChange)
                break
            lastprecent = nowprecent
            sleep(0.1)
            e32.ao_yield()

    def slideChange(self):
        if (self.RunningForm == self.allForm.main):
            self.SlideIndex += 1
            if (self.SlideIndex >= len(self.SlideList)):
                self.SlideIndex = 0
            self.redraw()
        self.slideChangeThread.after(3, self.slideChange)

    def delCache(self):  # 清除缓存
        ui.note(cn('清除成功！'))

    def refushList(self):
        # e32.ao_yield()
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.x = -1
        self.selectedIndex = 0
        self.lastX = self.selectedIndex - 1
        #sleep(0.5)
        self.isRefush = 0

    def refush(self):  # 刷新
        self.isRefush = 1
        thread.start_new_thread(self.refushList, ())
        # self.refushListThread.after(0,self.refushList)

        self.drawRefushLoading()

        # self.redraw()

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

    def getColor(self, idx):
        color = [0xffffff, 0xeeeeee, 0xdddddd, 0xcccccc, 0xbbbbbb, 0xaaaaaa, 0x999999, 0x888888]
        return color[idx % len(color)]

    def genAllEllipseXy(self, posbase):
        l = []
        r = 30
        for i in range(0, 2 * 314, int(2 * 314 / 8)):
            t = float(i) / float(100)
            x = posbase[0] + r * math.cos(t)
            y = posbase[1] + r * math.sin(t)
            l.append((x, y))
        return l

    def drawRefushLoading(self):
        self.loading = 1
        self.imgOld.blit(self.img)  # 当前背景

        index = 0
        while (self.isRefush):
            self.background.clear(0x0)
            self.background.blit(self.imgOld, mask=self.deepMaskImg)
            center = [int(self.width / 2), int(self.height / 2)]
            allxy = self.genAllEllipseXy(center)

            for i in allxy:
                r = 6
                color = self.getColor(index)
                if(index%8==0):
                    r = 8
                    self.background.ellipse((i[0] - r, i[1] - r, i[0] + r, i[1] + r), color, color)
                else:
                    self.background.ellipse((i[0] - r, i[1] - r, i[0] + r, i[1] + r), color, color)
                index += 1
            sleep(0.1)
            self.img.blit(self.background)
            self.__redraw()

        self.articleName = self.text_to_array(self.newsList.newslist[self.selectedIndex].title, ('dense', 20),
                                              self.width - 10)
        self.articleData = self.text_to_array(self.articleDetial, ('dense', 15), self.width - 10)

        self.loading = 0

    def redraw(self):  # 重绘界面
        if (self.loading == 1):
            return
        self.loading = 1
        # self.img.blit(self.background, (0, 0))
        if (self.RunningForm == self.allForm.loading):
            pass
        elif (self.RunningForm == self.allForm.refushLoading):
            pass
        elif (self.RunningForm == self.allForm.main):
            self.genImg()
            self.__redraw()
            self.imgOld.blit(self.img)
        elif (self.RunningForm == self.allForm.menu):
            self.drawMenu()
        elif (self.RunningForm == self.allForm.article):
            self.drawArticle()
            self.imgOld.blit(self.img)
        if (self.RunningForm != self.allForm.menu):
            self.lastRunningForm = self.RunningForm
        self.loading = 0

    def myMeasure_text(self,text,fot): 
        dense = fot[1]
        if(dense in self.fontSizeCache):
            if(text in self.fontSizeCache[dense]):
                return self.fontSizeCache[dense][text]
            else:
                w = self.tempImg.measure_text(text, fot)[0][2]
                self.fontSizeCache[dense][text] = w
                return w
        else:
            self.fontSizeCache[dense] = {}
            w = self.tempImg.measure_text(text, fot)[0][2]
            self.fontSizeCache[dense][text] = w
            return w
         

    def text_to_array(self, content, dense, width):
        if(width<dense[1]):
            width = dense[1]

        w = self.myMeasure_text(content,dense)
        if (w <= width):
            return [content]
        result = []
        #先扫描一遍\n
        #content = u'一加新 Logo 中文使用指南曝光一加 8 手机'
        content = content.split('\n')

        for contenti in content:
            nowtext = ''
            nowwidth = 0
            i = 0
            lasti = i
            while(i<=len(contenti)):
                if(i == 0 or nowwidth<=dense[1]):
                    i += int(width/dense[1]) #从这里开始计算

                else:
                    i+=int(math.ceil((width - nowwidth)/dense[1]))

                nowtext = contenti[lasti:i]

                w=self.myMeasure_text(nowtext, dense)
                nowwidth = w
                if (nowwidth == width):
                    result.append(nowtext)
                    nowwidth = 0
                    lasti = i
                elif (nowwidth > width):
                    result.append(nowtext[:-1])
                    i -= 1
                    lasti = i
                    nowwidth = 0
                else:
                    i+=1
            if (nowtext != ''):
                result.append(nowtext)

        return result

    def drawArticle(self):
        self.background.clear(self.bgcolor)

        nowline = 1
        titleLineHeight = 20
        articleLineHeight = 15

        nowY = titleLineHeight + self.articleIndex

        for i in range(len(self.articleName)):
            # 离屏不绘制
            if (nowY < 0 or nowY > self.height + titleLineHeight):
                nowY += titleLineHeight
                continue
            self.background.text((5, nowY), self.articleName[i], 0, font=("dense", 20))
            nowY += titleLineHeight
        # 离屏不绘制
        if (nowY > 0 or nowY < self.height + titleLineHeight):
            dateAndAuthor = self.articleTime + ' ' + self.newsauthor
            self.background.text((5, nowY - 7), dateAndAuthor, 0x888888, font=("dense", 10))
        nowY += 10

        for i in range(len(self.articleData)):
            # 离屏不绘制
            if (nowY < 0 or nowY > self.height + articleLineHeight):
                nowY += articleLineHeight
                continue
            self.background.text((5, nowY), self.articleData[i], 0)
            nowY += articleLineHeight

        self.articleMaxIndex = nowY - self.articleIndex

        if (self.articleMaxIndex < self.height):
            self.articleMaxIndex = self.height

        self.img.blit(self.background)
        self.__redraw()

    def drawSlide(self):  # 绘制顶部滚动图
        if (len(self.SlideList) < 1):
            return
        if (self.nowtime >= 1):
            self.nowtime = 0
            self.SlideIndex += 1
        if (self.SlideIndex >= len(self.SlideList)):
            self.SlideIndex = 0
        imgurl = self.SlideList[self.SlideIndex].image
        self.SlideImg = itnet.getLocalPicByUrl(imgurl, 2)
        # self.SlideImg.clear(0xff0000)
        timg = ph.Image.new((self.width, self.SlideHeight + self.baseCornor))
        timg.clear(self.bgcolor)
        self.background.blit(timg, (0, 0))
        self.img.blit(timg, (0, 0))
        del timg
        self.background.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))
        self.img.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))

    def drawMain(self):  # 绘制第一页主页
        self.background.clear(self.bgcolor)
        self.drawSlide()
        if (self.lastX != self.selectedIndex):
            self.drawNewsList()

    def genNewsListImg(self):
        showNewsCount = int(self.height / self.newsHeight) + 1  # 要显示的新闻数量
        NewsListImg = []
        if (len(self.newsList.newslist) < 1):
            return NewsListImg
        for i in range(showNewsCount):
            nowIndex = i + self.x
            if (nowIndex < 0):
                continue
            if (nowIndex >= len(self.newsList.newslist)):
                break
            imgurl = self.newsList.newslist[nowIndex].image
            newimg = ph.Image.new((self.newsWidth, self.newsHeight))
            # print nowIndex,self.selectedIndex

            if (nowIndex == self.selectedIndex):
                newimg.clear(self.selectedColor)

            # print itnet.getPic(imgurl)
            newTopImg = itnet.getLocalPicByUrl(imgurl,1)

            # newTopImg = self.loadingImg
            # newTopImg1.clear(0xff0000)
            newimg.blit(newTopImg, (0 - self.newsCornor, 0 - self.newsCornor))
            del newTopImg
            textBasePos = (self.newsCornor * 2 + self.newImgWidth, self.newsCornor)
            textWidth = self.newsWidth - self.newImgWidth - self.baseCornor
            textHeight = self.newsHeight - self.newsCornor * 2
            title = self.newsList.newslist[nowIndex].title
            titlelist = self.text_to_array(title, ("dense", 15), textWidth)
            for j in range(len(titlelist)):
                if(self.newsList.newslist[nowIndex].istop==1):
                    newimg.text((textBasePos[0], textBasePos[1] + (j + 1) * 15), titlelist[j], 0xcc2222,
                                ("dense", 15, FONT_ANTIALIAS))
                else:
                    newimg.text((textBasePos[0], textBasePos[1] + (j + 1) * 15), titlelist[j], 0x0,
                            ("dense", 15, FONT_ANTIALIAS))
            NewsListImg.append(newimg)
            del newimg
        return NewsListImg

    def drawNewsList(self):  # 绘制下面的新闻列表
        self.NewsBasePos = (0, 0)
        # 当前选择位置的x坐标
        nowX = 0
        if (self.x == -1):
            self.NewsBasePos = (self.baseCornor, self.SlideHeight + self.baseCornor * 2)
            nowX = self.NewsBasePos[1] + (self.selectedIndex - self.x - 1) * (self.newsHeight + self.newsCornor * 2)
        else:
            self.NewsBasePos = (self.baseCornor, self.baseCornor)
            nowX = self.NewsBasePos[1] + (self.selectedIndex - self.x) * (self.newsHeight + self.newsCornor * 2)

        timg = ph.Image.new((self.width, self.height - self.SlideHeight))
        timg.clear(self.bgcolor)
        self.background.blit(timg, (0, 0 - self.SlideHeight - self.baseCornor))
        del timg
        # 绘制选择的矩形框
        self.background.rectangle((2, nowX - 2, self.width - 2, nowX + self.newsCornor * 2 - 2 + self.newsHeight),
                                  self.selectedColor, fill=self.selectedColor)

        newListImg = self.genNewsListImg()
        for i in range(len(newListImg)):
            # 将新闻绘制到界面上
            self.background.blit(newListImg[i], (
                0 - self.NewsBasePos[0], 0 - (self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2))))
            # 绘制新闻下面的间隔
            self.background.line(
                (self.NewsBasePos[0], self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2),
                 self.NewsBasePos[0] + self.newsWidth,
                 self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor * 2)), 0xdddddd, width=1)
        self.img.blit(self.background)
        del newListImg

    def toTop(self):  # 到顶部
        self.loading = 1
        self.RunningForm = self.allForm.main
        while (self.selectedIndex > 0):
            self.keyUp()
            self.genImg()
            self.__redraw()
            self.imgOld.blit(self.img)
        self.loading = 0

    def toBottom(self):  # 到底部
        self.loading = 1
        self.RunningForm = self.allForm.main
        while (self.selectedIndex < len(self.newsList.newslist) - 1):
            self.keyDown()
            self.genImg()
            self.__redraw()
            self.imgOld.blit(self.img)
        self.loading = 0

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
        if (self.RunningForm == self.allForm.main):
            while (menuPos < self.RealMenuWidth):
                menuPos += self.menuSpeed
                if (menuPos >= self.RealMenuWidth):
                    menuPos = self.RealMenuWidth
                # menuPos = self.RealMenuWidth
                self._drawMenu(menuPos)
                self.__redraw()
        elif (self.RunningForm == self.allForm.menu):
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
            t = self.textLen(i)
            if (l < t):
                l = t
            if (l > self.width):
                return self.width
        return l

    def _drawMenu(self, menuPos):
        # self.imgOld.blit(self.img)
        self.img.clear(0X0)
        self.img.blit(self.imgOld, mask=self.maskImg)

        imgTemp = ph.Image.new((self.RealMenuWidth, self.RealMenuHeight))
        imgTemp.clear(0)
        for i in range(len(self.listName)):
            color = 0xffffff
            if (i == self.menuIndex):
                color = 0xff0000
            imgTemp.text((5, i * self.menuHeight + self.menuHeight / 2 + 8), self.listName[i], color, zt)

        x = 0 - (menuPos - self.RealMenuWidth)
        y = 0 - (self.height - self.RealMenuHeight)
        # print x,y
        self.img.blit(imgTemp, (x, y))
        del imgTemp

    def InvokeMenu(self):
        self.listEvent[self.menuIndex]()

    def keyUp(self):
        self.selectedIndex -= 1
        if (self.selectedIndex < 0):
            self.selectedIndex = 0

        if (self.selectedIndex < self.x):
            self.x -= 1
        if (self.x == 0):
            self.x = -1
        if (self.x <= -1):
            self.x = -1

    def keyDown(self):
        self.selectedIndex += 1
        if (self.selectedIndex >= len(self.newsList.newslist)):
            self.selectedIndex = len(self.newsList.newslist) - 1

        if (self.selectedIndex > self.x + int(self.height / self.newsHeight) - 2):
            self.x += 1

        t = int(self.height / self.newsHeight) - 1
        if (self.x > len(self.newsList.newslist) - t):
            self.x = len(self.newsList.newslist) - t

    def key(self, event):
        if (self.RunningForm == self.allForm.loading):
            return
        if (self.loading == 1):
            return
        key = event["keycode"]
        scan = event["scancode"]
        type = event["type"]
        # ok button
        if key == 63557:
            if (self.RunningForm == self.allForm.main):
                # 加载数据
                # self.articleContent = self.newsList.newslist[self.selectedIndex].url
                self.loading = 1
                self.refushArticle()
                self.loading = 0

            elif (self.RunningForm == self.allForm.menu):
                # self.InvokeMenu()
                self.lastX = -1
                self.RunningForm = self.lastRunningForm
                self.lock.signal()

        # 左键
        if scan == 164 and type == 3:
            if (self.RunningForm == self.allForm.main):
                self.menuIndex = 0
                self.menuL = self.mainMenu
                self.genMenuList()
                self.drawMenu()
                self.RunningForm = self.allForm.menu
                self.lock.wait()
                if (self.menuIndex != -1):
                    self.InvokeMenu()

            elif (self.RunningForm == self.allForm.menu):
                self.lastX = -1
                self.RunningForm = self.lastRunningForm
                self.lock.signal()
            elif (self.RunningForm == self.allForm.article):
                self.menuIndex = 0
                self.menuL = self.articleMenuL
                self.genMenuList()
                self.drawMenu()
                self.RunningForm = self.allForm.menu
                self.lock.wait()
                if (self.menuIndex != -1):
                    self.InvokeMenu()
                    # 2或上
        if (key == 0x32 or key == 63497):
            if (self.RunningForm == self.allForm.main):
                self.keyUp()
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex -= 1
                if (self.menuIndex < 0):
                    self.menuIndex = len(self.listName) - 1
            elif (self.RunningForm == self.allForm.article):
                self.articleKeyUp()
        # 8或下
        elif (key == 0x38 or key == 63498):
            if (self.RunningForm == self.allForm.main):
                self.keyDown()
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex += 1
                if (self.menuIndex > len(self.listName) - 1):
                    self.menuIndex = 0
            elif (self.RunningForm == self.allForm.article):
                self.articleKeyDown()

        self.redraw()

    def articleKeyUp(self):
        self.loading = 1
        if (self.articleIndex >= self.articleMinIndex):
            self.articleIndex = self.articleMinIndex
        else:
            for i in range(0, self.articleStep, self.articleMinStep):
                self.articleIndex += self.articleMinStep
                self.drawArticle()
            if (self.articleIndex > self.articleMinIndex):
                self.articleIndex = self.articleMinIndex
        self.loading = 0

    def articleKeyDown(self):
        self.loading = 1
        if (self.articleIndex <= 0 - (self.articleMaxIndex - self.height)):
            self.articleIndex = 0 - (self.articleMaxIndex - self.height)
        else:
            for i in range(0, self.articleStep, self.articleMinStep):
                self.articleIndex -= self.articleMinStep
                self.drawArticle()

            if (self.articleIndex <= 0 - (self.articleMaxIndex - self.height)):
                self.articleIndex = 0 - (self.articleMaxIndex - self.height)
        self.loading = 0

    def exit2(self):
        if ui.query(cn("要退出吗？"), "query"):
            self.running = 0
            os.abort()

    def exit(self):
        if (self.RunningForm == self.allForm.main or self.RunningForm == self.allForm.loading):
            if ui.query(cn("要退出吗？"), "query"):
                self.running = 0
                os.abort()
        elif (self.RunningForm == self.allForm.menu):
            self.closeMenu()
            self.RunningForm = self.lastRunningForm
            self.lastX = -1
            self.menuIndex = -1
            self.lock.signal()
            self.redraw()
        elif (self.RunningForm == self.allForm.article):
            self.lastX = -1
            self.RunningForm = self.allForm.main
            self.lastRunningForm = self.RunningForm
            self.redraw()


# app=App(mypath+'splash.png',0)
ithome = ithomeUi(mypath + 'splash.png')
ithome.TitleName = cn("IT之家")
# app.keyType=0
ithome.main()

e32.Ao_lock().wait()
