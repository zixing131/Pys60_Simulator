#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 19:48
# @Author  : zixing
# @QQun    : 140369358
# @File    : qqcontrols.py
# @Software: PyCharm

import graphics as ph

class Control:
    def __init__(self,pos,color,fontsize):
        self.pos = pos
        self.color= color
        self.fontsize = fontsize
        self.Controls = []
        self.PaintImg = None

    def addControl(self, control):
        self.Controls.append((control))

    def Paint(self,baseImg):
        pass
        #self.PaintImg = ph.Image.new()

    def getPaintImg(self):
        return self.PaintImg

class Label(Control):

    def __init__(self,text="",pos=(0,0),color=0x0,fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.text = text

    def Paint(self, baseImg):
        baseImg.text(self.pos,self.text,self.color,('dense',self.fontsize))

class Textbox(Control):

    def __init__(self, text="", pos=(0, 0), color=0x0, fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.text = text

    def Paint(self, baseImg):
        pass

class PasswordBox(Control):

    def __init__(self, text="", pos=(0, 0), color=0x0, fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
    def Paint(self,baseImg):
        pass

class Menu(Control):

    def __init__(self, menuList=[], pos=(0, 0), color=0x0, fontsize=15,menuItemHeight = 30,menuMinWidth = 0,menuSpeed = 40):
        Control.__init__(self,pos, color, fontsize)
        self.menuList = menuList
        self.menuItemHeight = menuItemHeight
        self.menuMinWidth=menuMinWidth
        self.menuSpeed=menuSpeed

    def Paint(self, baseImg):
        pass

class Panel(Control):
    def __init__(self, pos=(0, 0),size=(240,320), color=0x0, fontsize=15,bgImage=''):
        Control.__init__(self, pos, color, fontsize)
        self.bgImage=bgImage

    def Paint(self, baseImg):
        baseImg.blit(ph.Image.open(self.bgImage))

class Form(Control):

    def __init__(self, text="", pos=(0, 0),size=(240,320), color=0x0, fontsize=15):
        Control.__init__(self,pos, color, fontsize)
        self.text = text
        self.size = size
        self.baseImg = ph.Image.new(self.size)


    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def getPaintImg(self):
        self.baseImg.clear(self.color)
        for i in self.Controls:
            i.Paint(self.baseImg)
        return self.baseImg

    def InitializeComponent():
        pass


