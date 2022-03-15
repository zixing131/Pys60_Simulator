#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 20:42
# @Author  : zixing
# @QQun    : 140369358
# @File    : qqui.py
# @Software: PyCharm
import pys60Core
import time

from qqsdk import QQSDK

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
        #checkbox 选中的时候的文本颜色
        self.cbk_CheckedTextColor = 0xFFFFFF
        #checkbox的文本颜色
        self.cbk_TextColor = 0xA5D7F7
        #checkbox 勾的颜色
        self.cbk_checkColor = 0x10456B
        # checkbox 勾的内部颜色
        self.cbk_checkInlineColor = 0xD6EFFF



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

        self.qsdk = QQSDK()

        #启动页面
        self.splash = 3
        # 加载界面
        self.loading = 0
        #登录界面
        self.login = 5

        #好友列表界面
        self.friendlist = 7

        #正在登录的界面
        self.logining = 6
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
        self.redrawAll = None
        self.loginCancel = 0

    def loginEvent(self):
        print("开始登录")
        self.loginCancel = 0
        self.menuLogin.hide()
        qq = self.textboxUsername.text
        pwd = self.textboxPassword.text
        self.qsdk.init(qq.encode('u8'),pwd.encode('u8'))
        self.qsdk.login()

        headimgpath = self.qsdk.getHeadImgPath()

        img = ph.Image.open(headimgpath)
        img = img.resize((32, 32))
        img.save('miniheadimgpath.jpg')
        miniheadimgpath = 'miniheadimgpath.jpg'
        self.imgHead.bgImage = miniheadimgpath
        # 昵称
        self.labelNickName.text = cn(self.qsdk.getNickName())
        self.friendListControl.setFriendList(self.qsdk.getFriendList())
        self.setLoginingPanel()

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


    def genForms(self):
        self.MainForm = Form("PYQQ",(0,0),self.screen)
        bgImage = ''
        if (self.width == 240):
            bgImage = mypath + "splash_1.png"
        else:
            bgImage = mypath + "splash_2.png"
        self.SplashPanel = Panel(cn('启动界面'),(0,0),self.screen,bgImage=bgImage)
        self.MainForm.addControl(self.SplashPanel)

        self.genLoginPanel()
        self.genLoginingPanel()
        self.genMainPanel()
        self.genFrindListPanel()

        self.MainForm.addControl(self.LoginPanel)
        self.MainForm.addControl(self.LoginingPanel)
        self.MainForm.addControl(self.FriendListPanel)

    #生成好友列表界面
    def genFrindListPanel(self):
        self.FriendListPanel = Panel(cn("好友列表"), (0, 0), self.screen, qqSkin.bgColor)
        self.FriendListPanel.showMenuBar = 1
        self.FriendListPanel.leftMenuName = cn('菜单')
        self.FriendListPanel.rightMenuName = cn('退出')
        self.FriendListPanel.MenuBarHeight = 30
        self.FriendListPanel.MenuBarBgColor = qqSkin.barBgColor
        self.FriendListPanel.MenuBarTextColor = qqSkin.barTextColor

        self.FrindListMenuL = [(cn("发送消息"), self.sendFriendMessage),
                               (cn("查看资料"), self.viewFriendInfo),
                               (cn("刷新列表"), self.refreshFriendList),
                               (cn("帮助关于"), self.helpAndAbout),
                           (cn("退出"), self.exit2)]

        #头像
        self.imgHead = Panel(cn('头像'),(5,5),(32,32))
        #昵称
        self.labelNickName = Label(cn('昵称'), (40,24), qqSkin.textColor, 14)

        self.menuFriendList = Menu(self.FrindListMenuL, (2, 2 + self.LoginPanel.MenuBarHeight), qqSkin.menuBgColor,
                         qqSkin.menuTextColor,
                         qqSkin.menuSelectedTextColor,
                         qqSkin.menuSelectedBgColor, qqSkin.menuBgAroundColor1, qqSkin.menuBgAroundColor2
                         , fontsize=15, menuItemHeight=30, menuMinWidth=50, menuSpeed=40)
        self.menuFriendList.hide()

        self.friendListControl = FriendListControl((5,40),(self.width - 10,self.height - self.FriendListPanel.MenuBarHeight -40-5),color=qqSkin.bgColor)

        self.FriendListPanel.addControl(self.imgHead)
        self.FriendListPanel.addControl(self.labelNickName)
        self.FriendListPanel.addControl(self.friendListControl)
        self.FriendListPanel.addControl(self.menuFriendList)

    #发送好友消息
    def sendFriendMessage(self):
        print('发送好友消息')
        pass
    #查看好友资料
    def viewFriendInfo(self):
        print('查看好友资料')
        pass

    #刷新好友列表
    def refreshFriendList(self):
        pass

    #帮助关于
    def helpAndAbout(self):
        pass

    #生成正在登录界面
    def genLoginingPanel(self):
        self.LoginingPanel = Panel(cn("正在登录"), (0, 0), self.screen, qqSkin.bgColor)

        self.LoginingPanel.showMenuBar = 1
        self.LoginingPanel.rightMenuName = cn('取消')
        self.LoginingPanel.MenuBarHeight = 30
        self.LoginingPanel.MenuBarBgColor = qqSkin.barBgColor
        self.LoginingPanel.MenuBarTextColor = qqSkin.barTextColor

        basex = 0
        if (self.width == 240):
            basex = 0
        else:
            basex = 45
        labelLoginTips = DynamicLabel([cn('正在登录 . '),cn('正在登录 . . '),cn('正在登录 . . . ')], (basex + 70, 120), qqSkin.textColor, 16,nowdymIndex=1)
        self.LoginingPanel.addControl(labelLoginTips)

    def genMainPanel(self):
        self.mainMenu = [(cn("刷新消息"), self.refushMsg),
                         (cn("刷新好友列表"), self.refushFriendList),
                         (cn("刷新群列表"), self.refushGroupList),
                         (cn("退出"), self.exit2)]


    #生成登录界面
    def genLoginPanel(self):

        self.LoginPanel = Panel(cn("登陆界面"), (0, 0), self.screen, qqSkin.bgColor)

        self.loginMenuL = [(cn("登  录"), self.loginEvent),
                           (cn("退  出"), self.exit2)]


        self.LoginPanel.showMenuBar = 1
        self.LoginPanel.leftMenuName = cn('菜单')
        self.LoginPanel.rightMenuName = cn('登录')
        self.LoginPanel.MenuBarHeight = 30
        self.LoginPanel.MenuBarBgColor = qqSkin.barBgColor
        self.LoginPanel.MenuBarTextColor = qqSkin.barTextColor


        self.menuLogin = Menu(self.loginMenuL, (2, 2 + self.LoginPanel.MenuBarHeight), qqSkin.menuBgColor,
                         qqSkin.menuTextColor,
                         qqSkin.menuSelectedTextColor,
                         qqSkin.menuSelectedBgColor, qqSkin.menuBgAroundColor1, qqSkin.menuBgAroundColor2
                         , fontsize=15, menuItemHeight=30, menuMinWidth=50, menuSpeed=40)
        self.menuLogin.hide()
        self.LoginPanel.addControl(self.menuLogin)

        basex = 0
        if (self.width == 240):
            basex = 0
        else:
            basex = 45
        labelUsername = Label(cn('账号：'), (basex + 38, 70), qqSkin.textColor, 16)
        self.LoginPanel.addControl(labelUsername)
        labelPassword = Label(cn('密码：'), (basex + 38, 100), qqSkin.textColor, 16)
        self.LoginPanel.addControl(labelPassword)
        self.textboxUsername = Textbox(cn(''), (basex + 85, 53), (100, 20), qqSkin.textboxTextColor, qqSkin.textboxBgColor,
                                  qqSkin.textboxOutlineColor, qqSkin.selectedOutlineColor, 15)
        self.LoginPanel.addControl(self.textboxUsername)
        self.textboxPassword = PasswordBox(cn(''), '', (basex + 85, 83), (100, 20), qqSkin.textboxTextColor,
                                      qqSkin.textboxBgColor, qqSkin.textboxOutlineColor,
                                      qqSkin.selectedOutlineColor, 15)
        self.LoginPanel.addControl(self.textboxPassword)
        self.ckb_rememberPassword = CheckBox(cn('记住密码'), None, (basex + 82, 113), (82, 20), qqSkin.cbk_TextColor,
                                        qqSkin.bgColor,
                                        qqSkin.bgColor, qqSkin.selectedOutlineColor, 15,
                                        checkedTextColor=qqSkin.cbk_CheckedTextColor,
                                        checkColor=qqSkin.cbk_checkColor,
                                        checkInlineColor=qqSkin.cbk_checkInlineColor)
        self.ckb_receiveGroupMsg = CheckBox(cn('接收群消息'), None, (basex + 82, 143), (95, 20), qqSkin.cbk_TextColor,
                                       qqSkin.bgColor,
                                       qqSkin.bgColor, qqSkin.selectedOutlineColor, 15,
                                       checkedTextColor=qqSkin.cbk_CheckedTextColor,
                                       checkColor=qqSkin.cbk_checkColor,
                                       checkInlineColor=qqSkin.cbk_checkInlineColor)

        self.ckb_rememberPassword.value = 1
        self.ckb_receiveGroupMsg.value = 1
        self.LoginPanel.addControl(self.ckb_rememberPassword)
        self.LoginPanel.addControl(self.ckb_receiveGroupMsg)



    def getMainForm(self):
        return self.MainForm
    def setSplashPanel(self):
        self.RunningForm = self.splash
        self.MainForm.HideAllChildrenExcept(self.SplashPanel)
        self.MainForm.redraw()

    def setFriendListPanel(self):
        self.RunningForm = self.friendlist
        self.MainForm.HideAllChildrenExcept(self.FriendListPanel)
        self.FriendListPanel.setRightMenuEvent(self.exit2)
        self.MainForm.getPaintImg()
        self.MainForm.redraw()

    def setLoginPanel(self):
        self.RunningForm = self.login
        self.MainForm.HideAllChildrenExcept(self.LoginPanel)
        self.LoginPanel.setRightMenuEvent(self.loginEvent)
        self.MainForm.redraw()

    def LoginingreturnEvent(self):
        self.loginCancel = 1
        self.qsdk.logout()
        self.setLoginPanel()
        if(self.redrawAll!=None):
            self.redrawAll()

    def setLoginingPanel(self):
        self.RunningForm = self.logining
        self.MainForm.HideAllChildrenExcept(self.LoginingPanel)
        self.LoginPanel.setRightMenuEvent(self.LoginingreturnEvent)  # 返回键,暂时空置
        loopindex = 0
        while (self.RunningForm == self.logining):
            self.MainForm.getPaintImg()
            self.LoginingPanel.Controls[0].loopIndex()
            if(self.RunningForm == self.logining):
                self.MainForm.redraw()
                loopindex +=1
                time.sleep(0.5)
                if(loopindex >2):
                    break
        if(self.loginCancel == 0):
            self.setFriendListPanel()


class QQUi(object, ):
    def __init__(self):
        self.TitleName = "PYQQ"
        screen = ui.app.layout(ui.EScreen)[0]
        self.width = screen[0]
        self.height = screen[1]

        self.allForm = AllForm()
        self.allForm.redrawAll = self.redraw
        self.MainForm = self.allForm.getMainForm()
        self.MainForm._redraw = self.__redraw
        self.MainForm._blit=self.blit
        self.allForm.setSplashPanel()
        self.MainForm.show()
        self.redraw()
        sleep(1)
        self.allForm.setLoginPanel()
        self.redraw()

    def __redraw(self, size=0):  # 重绘界面
        self.blit(self.MainForm.img)

    def blit(self, img):
        self.MainForm._Form__canvas.blit(img)

    def key(self, event):
        pass

    def show(self):
        self.MainForm.run()
        self._redraw()
    def _redraw(self):
        self.MainForm.img.blit(self.MainForm.getPaintImg())
        self.redraw()

    def redraw(self):  # 重绘界面
        if (self.allForm.RunningForm == self.allForm.splash):
            self.allForm.setSplashPanel()
            self.MainForm.img.blit(self.MainForm.getPaintImg())
        elif (self.allForm.RunningForm == self.allForm.login):
            self.allForm.setLoginPanel()
            self.MainForm.img.blit(self.MainForm.getPaintImg())
        elif (self.allForm.RunningForm == self.allForm.logining):
            self.allForm.setLoginingPanel()
            self.MainForm.img.blit(self.MainForm.getPaintImg())
        elif (self.allForm.RunningForm == self.allForm.friendlist):
            self.allForm.setFriendListPanel()
            self.MainForm.img.blit(self.MainForm.getPaintImg())
        self.__redraw()


qqUi = QQUi()
qqUi.TitleName = cn("PYQQ")
qqUi.show()
e32.Ao_lock().wait()
