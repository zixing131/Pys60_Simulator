#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 20:42
# @Author  : zixing
# @QQun    : 140369358
# @File    : qqui.py
# @Software: PyCharm

zt = u"Sans MT 936_s60", 15, 1
import appuifw as ui, e32
import os
import graphics as ph, base64, thread, os, random
# from BingyiApp import *
import akntextutils2
import math
from graphics import *
from qqcontrols import *
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

        # 文本编辑框文本颜色
        self.textboxTextColor = 0x002157
        #文本编辑框背景颜色
        self.textboxBgColor = 0xD6EFFE
        # 文本编辑框边框颜色
        self.textboxOutlineColor = 0xB5D3E7
        #选中的边框颜色
        self.selectedOutlineColor = 0x4AFFFF
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
        self.splash = 3
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
        self.screen = ui.app.layout(ui.EScreen)[0]
        self.width = self.screen[0]
        self.height = self.screen[1]
        self.RunningForm = self.splash
        self.genForms()

    def genForms(self):
        self.MainForm = Form("PYQQ",(0,0),self.screen)
        bgImage = ''
        if (self.width == 240):
            bgImage = mypath + "splash_1.png"
        else:
            bgImage = mypath + "splash_2.png"
        self.SplashPanel = Panel(cn('启动界面'),(0,0),self.screen,bgImage=bgImage)
        self.MainForm.addControl(self.SplashPanel)

        self.LoginPanel = Panel(cn("登陆界面"), (0, 0), self.screen,qqSkin.bgColor)
        if(self.width==240):
            labelUsername = Label(cn('账号：'),(38,70),qqSkin.textColor,16)
            self.LoginPanel.addControl(labelUsername)
            labelPassword = Label(cn('密码：'),(38,100),qqSkin.textColor,16)
            self.LoginPanel.addControl(labelPassword)
            textboxUsername = Textbox(cn(''),(85,53),(100,20), qqSkin.textboxTextColor,qqSkin.textboxBgColor,qqSkin.textboxOutlineColor,qqSkin.selectedOutlineColor, 15)
            self.LoginPanel.addControl(textboxUsername)
            textboxPassword = PasswordBox(cn(''),'', (85, 83),(100,20), qqSkin.textboxTextColor,qqSkin.textboxBgColor,qqSkin.textboxOutlineColor,qqSkin.selectedOutlineColor, 15)
            self.LoginPanel.addControl(textboxPassword)
        else:
            labelUsername = Label(cn('账号：'), (38, 71), qqSkin.textColor, 16)
            self.LoginPanel.addControl(labelUsername)
            labelPassword = Label(cn('密码：'), (38, 100), qqSkin.textColor, 16)
            self.LoginPanel.addControl(labelPassword)
        self.MainForm.addControl(self.LoginPanel)

    def getMainForm(self):
        return self.MainForm
    def setSplashPanel(self):
        self.RunningForm = self.splash
        self.MainForm.HideAllChildrenExcept(self.SplashPanel)
        self.MainForm.redraw()

    def setLoginPanel(self):
        self.RunningForm = self.login
        self.MainForm.HideAllChildrenExcept(self.LoginPanel)
        self.MainForm.redraw()




class QQUi(object, ):
    def __init__(self):
        self.TitleName = "PYQQ"
        screen = ui.app.layout(ui.EScreen)[0]
        self.width = screen[0]
        self.height = screen[1]
        self.loginMenuL = [(cn("登录"), self.loginEvent),
                           (cn("退出"), self.exit2)]

        self.mainMenu = [(cn("刷新消息"), self.refushMsg),
                         (cn("刷新好友列表"), self.refushFriendList),
                         (cn("刷新群列表"), self.refushGroupList),
                         (cn("退出"), self.exit2)]

        self.img = ph.Image.new(screen)
        self.allForm = AllForm()
        self.MainForm = self.allForm.getMainForm()
        self.MainForm._redraw = self.__redraw
        self.MainForm._blit=self.blit
        self.allForm.setSplashPanel()
        self.MainForm.show()
        self.redraw()
        sleep(0)
        self.allForm.setLoginPanel()
        self.redraw()

    def __redraw(self, size=0):  # 重绘界面
        self.blit(self.img)

    def blit(self, img):
        self.MainForm._Form__canvas.blit(img)

    def key(self, event):
        pass

    def loginEvent(self):
        print("开始登录")
        pass

    def exit2(self):
        if ui.query(cn("要退出吗？"), "query"):
            self.running = 0
            os.abort()

    def refushMsg(self):
        print ('刷新消息')

    def refushFriendList(self):
        print ('刷新好友列表')

    def refushGroupList(self):
        print ('刷新群列表')

    def show(self):
        self.MainForm.run()
        self._redraw()
    def _redraw(self):
        self.img.blit(self.MainForm.getPaintImg())
        self.redraw()

    def redraw(self):  # 重绘界面
        if (self.allForm.RunningForm == self.allForm.splash):
            self.allForm.setSplashPanel()
            self.img.blit(self.MainForm.getPaintImg())
        elif (self.allForm.RunningForm == self.allForm.login):
            self.allForm.setLoginPanel()
            self.img.blit(self.MainForm.getPaintImg())

        self.__redraw()


qqUi = QQUi()
qqUi.TitleName = cn("PYQQ")
qqUi.show()
e32.Ao_lock().wait()
