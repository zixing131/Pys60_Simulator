# -*- coding: utf-8 -*-

zt=u"Sans MT 936_s60",15,1
import appuifw as ui,e32
import graphics as ph,base64,thread,os,random
from BingyiApp import *
cn=lambda x:x.decode("u8")
sleep=e32.ao_sleep
mypath=u"..\\python\\pysoft\\ithome\\"
cachePath = mypath+"cache\\"
import ithomenet
itnet = ithomenet.IthomeNet()


class ithomeUi(object,):
    def __init__(self):
        self.running = 1
        self.menuL = [(cn("刷新"), lambda: self.refush()),
                      (cn("到顶部"), lambda: self.toTop()),
                      (cn("清除缓存"), lambda: self.delCache()),
                   (cn("退出"), lambda: self.exit())]
        self.width = 240
        self.height = 320
        self.img = ph.Image.new((self.width, self.height))
        self.background = ph.Image.new((self.width, self.height))
        self.background.clear(0xffffff)
        self.x = -1
        self.y = 0
        self.baseCornor = 5
        self.newsCornor = 2
        self.SlideHeight = 80
        self.newsHeight = 60
        self.newImgHeight = self.newsHeight - self.newsCornor *2
        self.newImgWidth = self.newImgHeight
        self.newsWidth = self.width - self.baseCornor*2
        self.newsList = itnet.getNewList()
        self.SlideList = itnet.getSlide()
        self.SlideIndex = 0

    def delCache(self): #清除缓存
        pass
    def refush(self): #刷新
        pass
    def redraw(self):#重绘界面
        if(self.x == -1):
            self.drawMain()
        else:
            self.drawNewsList()
    def drawSlide(self): #绘制顶部滚动图
        if(self.nowtime>=1):
            self.nowtime = 0
            self.SlideIndex += 1
        if(self.SlideIndex>=len(self.SlideList)):
            self.SlideIndex = 0
        self.SlideWidth = self.width - self.baseCornor*2
        imgurl = self.SlideList[self.SlideIndex].image
        self.SlideImg = ph.Image.open(itnet.getPic(imgurl))
        self.SlideImg = self.SlideImg.resize((self.SlideWidth, self.SlideHeight))
        #self.SlideImg.clear(0xff0000)
        self.img.blit(self.SlideImg, (0 - self.baseCornor, 0 - self.baseCornor))
    def drawMain(self):#绘制第一页主页
        self.drawSlide()
        self.drawNewsList()
    def genNewsListImg(self):
        showNewsCount = int(self.height/self.newsHeight) + 1 #要显示的新闻数量
        NewsListImg = []
        for i in range(showNewsCount):
            nowIndex = i + self.x
            if(nowIndex<0):
                continue
            if(nowIndex >= len(self.newsList.newslist)):
                break
            imgurl = self.newsList.newslist[nowIndex].image
            newimg = ph.Image.new((self.newsWidth,self.newsHeight))
            newTopImg = ph.Image.open(itnet.getPic(imgurl))
            #newTopImg.clear(0xff0000)
            newTopImg = newTopImg.resize((self.newImgWidth,self.newImgHeight))
            newimg.blit(newTopImg,(0-self.newsCornor,0-self.newsCornor))
            textBasePos = (self.newsCornor*2 + self.newImgHeight,self.newsCornor)
            textWidth = self.newsWidth - self.newImgWidth - self.newsCornor*3
            textHeight = self.newsHeight - self.newsCornor*2
            title=self.newsList.newslist[nowIndex].title
            titlelist = akntextutils.wrap_text_to_array(title.decode("u8"), "dense", textWidth)
            for j in range(len(titlelist)):
                newimg.text((textBasePos[0],textBasePos[1]+(j+1)*15),titlelist[j],0x0,("dense",15,FONT_ANTIALIAS))
            NewsListImg.append(newimg)
        return NewsListImg

    def drawNewsList(self):#绘制下面的新闻列表
        self.NewsBasePos = (0,0)
        if(self.x == -1):
            self.NewsBasePos = (self.baseCornor, self.SlideHeight + self.baseCornor*2)
        else:
            self.NewsBasePos = (self.baseCornor, self.baseCornor)
        newListImg = self.genNewsListImg()
        for i in range(len(newListImg)):
            self.img.blit(newListImg[i],(0-self.NewsBasePos[0],0-(self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor*2))))
            self.img.line((self.NewsBasePos[0],self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor*2),self.NewsBasePos[0]+self.newsWidth,self.NewsBasePos[1] + i * (self.newsHeight + self.newsCornor*2)),0xdddddd,width=1)

    def toTop(self):#到顶部
        pass

    def main(self):
        app.keyType = 1
        self.nowtime = 0
        while self.running:
            self.img.blit(self.background, (0, 0))
            self.redraw()
            app.blit(self.img)
            sleep(0.1)
            self.nowtime+=0.1
            break


    def key(self, event):
        key = event["keycode"]
        scan = event["scancode"]
        type = event["type"]
        if scan == 164 and type == 3:
            #菜单
            app.menu(self.menuL)
        if(key == 0x32 or key == 63497):
            self.x-=1
            if (self.x <-1):
                self.x = -1
        elif(key == 0x38 or key == 63498):
            self.x+=1
            if(self.x> len(self.newsList.newslist)-4):
                self.x= len(self.newsList.newslist)-4
        self.img.blit(self.background, (0, 0))
        self.redraw()
        app.blit(self.img)

    def exit(self):
        if app.query2(cn("要退出吗？")):
            self.running = 0
            os.abort()

app=App(mypath+'splash.png',0)
app.TitleName=cn("IT之家")
#app.keyType=0
app.allClass([ithomeUi])
app.main()
e32.Ao_lock().wait()
