# -*- coding: utf-8 -*-

zt = u"Sans MT 936_s60", 15, 1
import appuifw as ui, e32
import os
import graphics as ph, base64, thread, os, random
# from BingyiApp import *
import akntextutils2
import math
from graphics import *

# import fontSize

cn = lambda x: x.decode("u8")
sleep = e32.ao_sleep

import mypath
mypath = mypath.getmypath("\\python\\pysoft\\pyqq\\")
cachePath = mypath + "cache\\"
#圆角矩形
def rim(a,b,c,d,e=1):
    if (a,b)<(c,d):
        if e==1:return (a,b+1,a+1,b+1,a+1,b,c-1,b,c-1,b+1,c,b+1,c,d-1,c-1,d-1,c-1,d,a+1,d,a+1,d-1,a,d-1)
        elif e==2:return (a,b+2,a+1,b+1,a+2,b,c-2,b,c-1,b+1,c,b+2,c,d-2,c-1,d-1,c-2,d,a+2,d,a+1,d-1,a,d-2)
        elif e==3:return (a,b+2,a+1,b+1,a+2,b,c-2,b,c-1,b+1,c,b+2,c,d,a,d)
        elif e==4:return (a,b+2,a-1,b+1,a-2,b,c-2,b,c-1,b+1,c,b+2,c,d-2,c+1,d-1,c+2,d,a+2,d,a+1,d-1,a,d-2)

class QQSkin:
    def __init__(self):
        #三角箭头颜色
        self.ArrowColor = 0x2996CE
        # 文字颜色
        self.textColor = 0xA5D7F7
        # 背景颜色
        self.bgColor = 0x215D84
        # 分隔栏颜色1
        self.splitColor1 = 0x105584
        # 分隔栏颜色2
        self.splitColor2 = 0x216994
        # 选中行背景颜色
        self.selectedBgColor = 0xCEEBFF
        # 选中行文字颜色
        self.selectedTextColor = 0x002052
        # 菜单背景颜色
        self.menuBgColor = 0x0F334F
        # 菜单文字颜色
        self.menuTextColor = 0xA5D5F3
        # 菜单选中背景颜色
        self.menuSelectedBgColor = 0x2982BD
        # 菜单选中文字颜色
        self.menuSelectedTextColor = 0xFFFFFF

        # 菜单包围颜色1（外层）
        self.menuBgAroundColor1 = 0x031421
        # 菜单包围颜色2（内层）
        self.menuBgAroundColor2 = 0x21597D

        # 底栏颜色
        self.barBgColor = 0x082842
        # 底栏文字颜色
        self.barTextColor = 0xA5D7F7

qqSkin = QQSkin()

# 所有界面状态
class AllForm:
    def __init__(self):
        #启动页面
        self.splash = 5
        # 加载界面
        self.loading = 0
        #登录界面
        self.login = 5
        # 主界面
        self.main = 1
        # 菜单
        self.menu = 2
        # 刷新的加载界面
        self.refushLoading = 4


class QQUi(object, ):
    def __init__(self):
        self.TitleName = "PYQQ"
        self.running = 1
        ui.app.exit_key_handler = self.exit
        # 当前选择项目的index
        self.selectedIndex = 0
        self.loading = 0

        ui.app.screen = "full"
        self.allForm = AllForm()
        self.RunningForm =self.allForm.main
        self.loginMenuL = [(cn("登录"), self.loginEvent),
                             (cn("退出"), self.exit2)]

        self.mainMenu = [(cn("刷新消息"), self.refushMsg),
                         (cn("刷新好友列表"), self.refushFriendList),
                         (cn("刷新群列表"), self.refushGroupList),
                         (cn("退出"), self.exit2)]

        self.menuL = self.mainMenu

        self.lock = e32.Ao_lock()
        screen = ui.app.layout(ui.EScreen)[0]
        self.width = screen[0]
        self.height = screen[1]
        self.img = ph.Image.new((self.width, self.height))
        self.background = ph.Image.new((self.width, self.height))

        self.bgcolor = qqSkin.bgColor
        self.background.clear(self.bgcolor)
        if(self.width == 240):
            self.splashImg = ph.Image.open(mypath + "splash_1.png")
        else:
            self.splashImg = ph.Image.open(mypath + "splash_2.png")
        self.isRefush = 0
        self.maskImg = Image.new(screen, "L")
        self.maskImg.clear(0x888888)
        self.deepMaskImg = Image.new(screen, "L")
        self.deepMaskImg.clear(0x333333)
        self.tempImg = ph.Image.new((1, 1))
        self.minMenuWidth = 0
        self.menuHeight = 30
        self.menuSpeed = 40
        self.__canvas = ui.Canvas(self.__redraw, self.key)
        ui.app.body = self.__canvas
        self.imgOld = Image.new(screen)
        self.img.blit(self.splashImg)
        self.__redraw()
        sleep(0)

    def refushMsg(self):
        print ('刷新消息')
    def refushFriendList(self):
        print ('刷新好友列表')

    def refushGroupList(self):
        print ('刷新群列表')

    def blit(self, img):
        self.__canvas.blit(img)

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
            self.background.clear(0)
            self.background.blit(self.imgOld, mask=self.deepMaskImg)
            center = [int(self.width / 2), int(self.height / 2)]
            allxy = self.genAllEllipseXy(center)

            for i in allxy:
                r = 6
                color = self.getColor(index)
                if (index % 8 == 0):
                    r = 8
                    self.background.ellipse((i[0] - r, i[1] - r, i[0] + r, i[1] + r), color, color)
                else:
                    self.background.ellipse((i[0] - r, i[1] - r, i[0] + r, i[1] + r), color, color)
                index += 1
            sleep(0.1)
            self.img.blit(self.background)
            self.__redraw()

        self.loading = 0

    def drawMain(self):
        self.background.clear(self.bgcolor)
        self.img.blit(self.background)

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
            self.drawMain();
            self.__redraw()
            self.imgOld.blit(self.img)
        elif (self.RunningForm == self.allForm.menu):
            self.drawMenu()
        if (self.RunningForm != self.allForm.menu):
            self.lastRunningForm = self.RunningForm
        self.loading = 0

    def text_to_array(self, content, dense, width):
        return akntextutils2.to_array(content,dense,width)


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
        length = self.tempImg.measure_text(content, font)[0]
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
            t = self.textLen(i,('dense',17))
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
        imgTemp.clear(qqSkin.menuBgAroundColor1)
        imgTemp.rectangle((1,1,self.RealMenuWidth-1, self.RealMenuHeight-1),qqSkin.menuBgAroundColor2,qqSkin.menuBgAroundColor2)
        imgTemp.rectangle((2, 2, self.RealMenuWidth - 2, self.RealMenuHeight -2), qqSkin.menuBgColor,
                          qqSkin.menuBgColor)

        for i in range(len(self.listName)):
            color = qqSkin.menuTextColor
            if (i == self.menuIndex):
                color = qqSkin.menuSelectedTextColor
                imgTemp.rectangle((3,i * self.menuHeight + 3,self.RealMenuWidth - 3,i * self.menuHeight + self.menuHeight+3),qqSkin.menuSelectedBgColor,qqSkin.menuSelectedBgColor)
            imgTemp.text((5, i * self.menuHeight + self.menuHeight / 2 + 11), self.listName[i], color, ('dense',15))

        x = 0 - (menuPos - self.RealMenuWidth + 3)
        y = 0 - (self.height - self.RealMenuHeight - 5)
        # print x,y
        self.img.blit(imgTemp, (x, y))
        del imgTemp

    def InvokeMenu(self):
        self.listEvent[self.menuIndex]()


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

        if (key == 0x32 or key == 63497):
            if (self.RunningForm == self.allForm.main):
                self.keyUp()
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex -= 1
                if (self.menuIndex < 0):
                    self.menuIndex = len(self.listName) - 1
        # 8或下
        elif (key == 0x38 or key == 63498):
            if (self.RunningForm == self.allForm.main):
                self.keyDown()
            elif (self.RunningForm == self.allForm.menu):
                self.menuIndex += 1
                if (self.menuIndex > len(self.listName) - 1):
                    self.menuIndex = 0

        self.redraw()

    def keyUp(self):
        print('keyup')

    def keyDown(self):
        print('keyDown')

    def loginEvent(self):
        print("开始登录")
        pass

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


qqUi = QQUi()
qqUi.TitleName = cn("PYQQ")
qqUi.main()

e32.Ao_lock().wait()
