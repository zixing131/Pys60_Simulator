#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 19:48
# @Author  : zixing
# @QQun    : 140369358
# @File    : qqcontrols.py
# @Software: PyCharm

import graphics as ph
import appuifw as ui
import txtfield
cn = lambda x: x.decode("u8")
class Events:
    def __init__(self):
        self.KEY_UP = 0
        self.KEY_REPEAT = 1
        self.KEY_DOWN = 2

        self.ARROW_LEFT = 14
        self.ARROW_RIGHT = 15
        self.ARROW_UP = 16
        self.ARROW_DOWN = 17

events = Events()
tempImg = ph.Image.new((1, 1))
screen = ui.app.layout(ui.EScreen)[0]

class Control(object):
    def __init__(self,pos,color,fontsize):
        self.pos = pos
        self.color= color
        self.fontsize = fontsize
        self.Controls = []
        self.PaintImg = None
        self.isShow = 1
        self.Parent = None
        self.canGetFocus = 1
        self.width = screen[0]
        self.height = screen[1]
        #是否有焦点
        self.focus = 0
    def textLen(self, content=u'', font=('dense',15)):
        length = tempImg.measure_text(content, font)[0]
        return length[2]

    def maxLenOfText(self, content=u'',maxwidth = -1, font=('dense', 15)):
        length = tempImg.measure_text(content, font,maxwidth=maxwidth)
        return length[2]

    def addControl(self, control):
        control.Parent = self
        self.Controls.append(control)

    def pressOk(self):
        pass

    def pressLeft(self):
        pass

    def WndProc(self,message, wparam, lparam):
        pass

    def Paint(self,baseImg):
        if (self.isShow == 0):
            return
        #self.PaintImg = ph.Image.new()
    def show(self):
        self.isShow = 1
    def hide(self):
        self.isShow=0

    def HideAllChildren(self):
        for i in self.Controls:
            i.hide()

    def HideAllChildrenExcept(self,exp):
        exp.show()
        for i in self.Controls:
            if(i!=exp):
                i.hide()

    def getPaintImg(self):
        return self.PaintImg

class Button(Control):
    def __init__(self,text="",event = None,pos=(0,0),size=(0,0),color=0x0,bgcolor = 0x0,outlinecolor=0x0,selectedOutLineColor = 0x0,fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
        self.canGetFocus = 1
        self.size = size
        self.outlinecolor=outlinecolor
        self.bgcolor=bgcolor
        self.event=event
        self.selectedOutLineColor=selectedOutLineColor
    def Paint(self,baseImg):
        if (self.isShow == 0):
            return
        if (self.focus == 0):
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                              outline=self.outlinecolor, fill=self.bgcolor, width=1)
        else:
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                              outline=self.selectedOutLineColor, fill=self.bgcolor, width=2)
        baseImg.text((self.pos[0] + 2, self.pos[1] + self.size[1] - 1), self.text, self.color,
                     ('dense', self.fontsize))
    def pressOk(self):
        if(self.isShow==1 and self.focus==1):
            if( self.event!=None):
                self.event()

class CheckBox(Button):
    def __init__(self,text="",event = None,pos=(0,0),size=(0,0),color=0x0,bgcolor = 0x0,outlinecolor=0x0,selectedOutLineColor = 0x0,fontsize=15,checkedTextColor = 0x0,checkColor=0x0,checkInlineColor=0x0):
        Button.__init__(self,text,event, pos,size, color,bgcolor,outlinecolor,selectedOutLineColor, fontsize)
        self.value = 0
        self.canGetFocus = 1
        self.checkedTextColor = checkedTextColor
        self.checkColor=checkColor
        self.checkInlineColor=checkInlineColor

    def Paint(self,baseImg):
        if (self.isShow == 0):
            return
        if (self.focus == 0):
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                              outline=self.outlinecolor, fill=self.bgcolor, width=1)
        else:
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                              outline=self.selectedOutLineColor, fill=self.bgcolor, width=2)

        gap = int((self.size[1] - 10)/2)
        x = self.pos[0] + gap
        y = self.pos[1] + gap
        baseImg.rectangle((x , y, x + 10, y+ 10),
                              outline=self.checkColor, fill=0xffffff, width=1)
        textcolor = self.color
        if (self.value == 1):
            textcolor = self.checkedTextColor
            baseImg.rectangle((x+2 , y+2, x + 8, y+ 8),
                                          outline=0xffffff, fill=self.checkColor, width=1)
        baseImg.text((self.pos[0] + 2 + 15, self.pos[1] + self.size[1] - 1), self.text, textcolor,
                     ('dense', self.fontsize))


    def getValue(self):
        return self.value

    def pressOk(self):
        if(self.isShow==1 and self.focus==1):
            if( self.event!=None):
                self.event()
            if(self.value == 1):
                self.value = 0
            else:
                self.value = 1


class Label(Control):

    def __init__(self,text="",pos=(0,0),color=0x0,fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
        self.canGetFocus = 0

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        baseImg.text(self.pos,self.text,self.color,('dense',self.fontsize))

class Textbox(Control):

    def __init__(self, text="", pos=(0, 0),size = (0,0), color=0x0,bgcolor = 0x0,outlinecolor=0x0,selectedOutLineColor = 0x0, fontsize=15,limit = 16):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
        self.TextEditing = 0 #是否正在编辑文本
        self.size = size
        self.bgcolor=bgcolor
        self.selectedOutLineColor=selectedOutLineColor
        self.outlinecolor=outlinecolor
        self.field = txtfield.New(
            (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
            cornertype=txtfield.ECorner1, txtlimit=limit)
        self.field.textstyle(u'', 140, 0x0, style=u'normal')
        self.field.bgcolor(self.bgcolor)
        self.field.add(self.text)
        self.field.select(0, len(self.text))
        self.field.focus(0)
        self.field.visible(0)

    def pressOk(self):
        if(self.TextEditing == 1):
            self.TextEditing = 0
            self.field.focus(0)
            self.field.visible(0)
            if(isinstance(self,PasswordBox)):
                self.password = self.field.get()
            else:
                self.text = self.field.get()
        elif(self.TextEditing == 0):
            self.TextEditing = 1
            self.field.focus(1)
            self.field.visible(1)


    def Paint(self, baseImg):
        if(self.isShow==0):
            return
        if(self.focus==0):
            baseImg.rectangle((self.pos[0],self.pos[1],self.pos[0]+self.size[0],self.pos[1]+self.size[1]),outline=self.outlinecolor,fill=self.bgcolor,width=1)
        else:
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                              outline=self.selectedOutLineColor, fill=self.bgcolor, width=2)

        drawLength = self.maxLenOfText(self.text,self.size[0],('dense',self.fontsize))
        drawText =self.text [:drawLength]
        baseImg.text((self.pos[0] + 2, self.pos[1] + self.size[1] - 1), drawText, self.color,
                         ('dense', self.fontsize))


class PasswordBox(Textbox):

    def __init__(self, text='',password='', pos=(0, 0),size = (0,0), color=0x0,bgcolor = 0x0,outlinecolor=0x0,selectedOutLineColor = 0x0, fontsize=15,limit=16):
        Textbox.__init__(self,text, pos,size, color,bgcolor,outlinecolor, selectedOutLineColor,fontsize,limit)
        self.password = password
    def Paint(self,baseImg):
        if(self.password!=''):
            self.text = cn('*'*len(self.password))
        Textbox.Paint(self,baseImg)
    def pressOk(self):
        Textbox.pressOk(self)

class Menu(Control):

    #Menu的pos是从左下角开始的
    def __init__(self, menuList=[], pos=(0, 0), color=0x0,textColor = 0x0,selectedTextColor = 0x0,selectedBgColor = 0x0 ,menuBgAroundColor1=0x0,menuBgAroundColor2=0x0, fontsize=15,menuItemHeight = 30,menuMinWidth = 50,menuSpeed = 40):
        Control.__init__(self,pos, color, fontsize)
        self.menuList = menuList
        self.menuItemHeight = menuItemHeight
        self.menuMinWidth=menuMinWidth
        self.menuSpeed=menuSpeed
        self.textColor=textColor
        self.selectedTextColor=selectedTextColor
        self.selectedBgColor=selectedBgColor
        self.menuBgAroundColor1=menuBgAroundColor1
        self.menuBgAroundColor2=menuBgAroundColor2
        self.MenuIndex = 0
        self.genMenuList()

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        self._drawMenu(baseImg)

    def MenuDown(self):
        self.MenuIndex += 1
        if(self.MenuIndex > len(self.listName)-1):
            self.MenuIndex = 0

    def MenuUp(self):
        self.MenuIndex -=1
        if(self.MenuIndex<0):
            self.MenuIndex = len(self.listName)-1

    def _drawMenu(self, baseImg):
        # self.imgOld.blit(self.img)

        imgTemp = ph.Image.new((self.RealMenuWidth, self.RealMenuHeight))
        imgTemp.clear(self.menuBgAroundColor1)
        imgTemp.rectangle((1,1,self.RealMenuWidth-1, self.RealMenuHeight-1),self.menuBgAroundColor2,self.menuBgAroundColor2)
        imgTemp.rectangle((2, 2, self.RealMenuWidth - 2, self.RealMenuHeight -2), self.color,
                          self.color)

        for i in range(len(self.listName)):
            color = self.textColor
            if (i == self.MenuIndex):
                color = self.selectedTextColor
                imgTemp.rectangle((3,i * self.menuItemHeight + 3,self.RealMenuWidth - 3,i * self.menuItemHeight + self.menuItemHeight+3),self.selectedBgColor,self.selectedBgColor)
            imgTemp.text((5, i * self.menuItemHeight + self.menuItemHeight / 2 + 11), self.listName[i], color, ('dense',self.fontsize))
        T=(0-self.pos[0],0-(self.height - self.pos[1] - self.RealMenuHeight))
        baseImg.blit(imgTemp, T)
        del imgTemp

    def genMenuList(self):
        self.listName = []
        self.listEvent = []
        index = 1
        for i in self.menuList:
            self.listName.append(cn(str(index) + '. ') + i[0])
            self.listEvent.append(i[1])
            index += 1
        self.RealMenuWidth = self.getMenuWidth()
        self.RealMenuHeight = len(self.listName) * self.menuItemHeight

    def getMenuWidth(self):
        l = self.menuMinWidth
        for i in self.listName:
            t = self.textLen(i, ('dense',self.fontsize+2)) +10
            if (l < t):
                l = t
            if (l > self.width):
                return self.width
        return l

    def pressLeft(self):
        if(self.isShow == 1):
            self.isShow = 0
            self.Parent.leftMenuName = self.ParentLeftMenuName
            self.Parent.rightMenuName = self.ParentRightMenuName
            self.listEvent[self.MenuIndex]()
            self.MenuIndex = 0
            ui.app.exit_key_handler = self.lastExitHandle
        else:
            self.isShow = 1
            if(type(self.Parent) is Panel):
                self.ParentLeftMenuName =  self.Parent.leftMenuName
                self.ParentRightMenuName =  self.Parent.rightMenuName
                self.Parent.leftMenuName = cn('选择')
                self.Parent.rightMenuName = cn('返回')
                self.lastExitHandle = ui.app.exit_key_handler
                ui.app.exit_key_handler = self.returnMenu
    def returnMenu(self):
        if (self.isShow == 1):
            self.isShow = 0
            self.MenuIndex = 0
            ui.app.exit_key_handler = self.lastExitHandle
            if (type(self.Parent) is Panel):
                self.Parent.leftMenuName = self.ParentLeftMenuName
                self.Parent.rightMenuName = self.ParentRightMenuName
                if (type(self.Parent.Parent) is Form):
                    self.Parent.Parent.reblit()

    def pressOk(self):
        if (self.isShow == 1):
            self.isShow = 0
            self.Parent.leftMenuName = self.ParentLeftMenuName
            self.Parent.rightMenuName = self.ParentRightMenuName
            self.listEvent[self.MenuIndex]()
            self.MenuIndex = 0
            ui.app.exit_key_handler = self.lastExitHandle


    #def appuifw.app.exit_key_handler = self.OnReturn6

class Panel(Control):
    def __init__(self,text='', pos=(0, 0),size=(240,320), color=0x0, fontsize=15,bgImage=''):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
        self.bgImage=bgImage
        self.size = size
        self.canGetFocus = 0
        self.showMenuBar = 0
        self.leftMenuName = cn('')
        self.rightMenuName = cn('')
        self.MenuBarHeight = 30
        self.MenuBarBgColor=0x0
        self.MenuBarTextColor = 0x0

    def setRightMenuEvent(self,event):
        ui.app.exit_key_handler = event

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), fill=self.color,width=0)
        if(self.bgImage!=''):
            baseImg.blit(ph.Image.open(self.bgImage))
        if(self.showMenuBar):
            baseImg.rectangle(( 0,self.height - self.MenuBarHeight ,self.width,self.height),self.MenuBarBgColor,self.MenuBarBgColor)
            baseImg.text((int(self.fontsize/2), self.height - int(self.fontsize/2) ), self.leftMenuName, self.MenuBarTextColor,
                         ('dense', self.fontsize))
            p = self.textLen(self.rightMenuName, ('dense', self.fontsize))
            baseImg.text((self.width - p - int(self.fontsize / 2), self.height - int(self.fontsize / 2)), self.rightMenuName,
                         self.MenuBarTextColor,
                         ('dense', self.fontsize))
        for i in self.Controls:
            i.Paint(baseImg)

    def show(self):
        self.isShow = 1
    def hide(self):
        self.isShow = 0

    def pressLeft(self):
        for i in self.Controls:
            i.pressLeft()

class Form(Control):

    def __init__(self, text="", pos=(0, 0),size=(240,320), color=0x0, fontsize=15):
        Control.__init__(self,pos, color, fontsize)
        self.text = text
        self.size = size
        self.canGetFocus = 0
        self.baseImg = ph.Image.new(self.size)
        self._redraw =None
        self._blit=None
        self._Form__canvas = ui.Canvas(redraw_callback=self.redraw, event_callback=self.event)
        ui.app.screen = 'full'
        ui.app.body = self._Form__canvas
        self._Form__index = -1 #当前选中的项目
        self.center = [] #模拟鼠标对应的控件中心点
        self.img = ph.Image.new(size)
        self.oldImg = ph.Image.new(size)


    def redraw(self,rd=None):
        if(self._redraw!=None):
            self._redraw(rd)
    def event(self,key=None):
        type = key['type']
        code = key['scancode']
        if type == 3:
            self.WndProc(events.KEY_DOWN, code, 0)
        elif type == 1:
            self.WndProc(events.KEY_REPEAT, code, 0)
        else:
            self.WndProc(events.KEY_UP, code, 0)

    def WalkCildren(self,parent,ret):
        if(len(parent.Controls) == 0 ):
            return
        for i in parent.Controls:
            if (i.isShow == 1 and i.canGetFocus):
                ret.append(i)
                self.WalkCildren(i,ret)
            if(i.isShow == 1 and i.canGetFocus == 0):
                self.WalkCildren(i, ret)


    def getVisiableChildrens(self):
        ret = []
        self.WalkCildren(self,ret)
        return ret

    def setChildrenFocus(self,child,controls):
        child.focus = 1
        for i in controls:
            if(i != child):
                i.focus = 0


    def indexUp(self):
        visiableChildrens = self.getVisiableChildrens()
        if(len(visiableChildrens) == 0):
            return
        for child in visiableChildrens:
            if ( isinstance(child,Menu) and child.isShow == 1):
                child.MenuUp()
                return
            if ( isinstance(child,Textbox) and child.TextEditing == 1):
                return
        self._Form__index -= 1
        if (self._Form__index < 0):
            self._Form__index = len(visiableChildrens) - 1
        self.setChildrenFocus(visiableChildrens[self._Form__index],visiableChildrens)

    def indexDown(self):
        visiableChildrens = self.getVisiableChildrens()
        if (len(visiableChildrens) == 0):
            return
        for child in visiableChildrens:
            if (isinstance(child, Menu) and child.isShow == 1):
                child.MenuDown()
                return
            if (isinstance(child,Textbox) and child.TextEditing == 1):
                return
        self._Form__index += 1
        if (self._Form__index > len(visiableChildrens) - 1):
            self._Form__index = 0
        self.setChildrenFocus(visiableChildrens[self._Form__index],visiableChildrens)

    def pressOk(self):
        visiableChildrens = self.getVisiableChildrens()
        if (len(visiableChildrens) == 0):
            return
        for child in visiableChildrens:
            if ( isinstance(child,Menu) and child.isShow == 1):
                child.pressOk()
                return
        for child in visiableChildrens:
            if (child.focus):
                child.pressOk()


    def keyup(self,message, wparam, lparam):
        if wparam == events.ARROW_LEFT:
            self.indexUp()
        elif(wparam == events.ARROW_UP):
            self.indexUp()
        elif (wparam == events.ARROW_DOWN):
            self.indexDown()
        elif (wparam == events.ARROW_RIGHT):
            self.indexDown()
        if(wparam == 167):#ok键
            self.pressOk()
        if(wparam == 164): #左键
            self.pressLeft()

    def reblit(self):
        if(self._blit!=None):
            self._blit(self.getPaintImg())

    def keydown(self,message, wparam, lparam):
        return
        if wparam == events.ARROW_LEFT:
            self.indexUp()
        elif(wparam == events.ARROW_UP):
            self.indexUp()
        elif (wparam == events.ARROW_DOWN):
            self.indexDown()
        elif (wparam == events.ARROW_RIGHT):
            self.indexDown()

    def keyrepeat(self,message, wparam, lparam):
        return
        if wparam == events.ARROW_LEFT:
            self.indexUp()
        elif (wparam == events.ARROW_UP):
            self.indexUp()
        elif (wparam == events.ARROW_DOWN):
            self.indexDown()
        elif (wparam == events.ARROW_RIGHT):
            self.indexDown()

    def WndProc(self,message, wparam, lparam):
        if(message == events.KEY_UP):
            self.keyup(message, wparam, lparam)
            self.reblit()
        elif(message == events.KEY_REPEAT):
            self.keyrepeat(message, wparam, lparam)
            self.reblit()
        elif (message == events.KEY_DOWN):
            self.keydown(message, wparam, lparam)
            self.reblit()

    def pressLeft(self):
        for i in self.Controls:
            if(i.isShow):
                i.pressLeft()

    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def run(self):
        pass

    def getPaintImg(self):
        self.baseImg.clear(self.color)
        for i in self.Controls:
            i.Paint(self.baseImg)
        self.img.blit(self.baseImg)
        return self.baseImg

    def InitializeComponent(self):
        pass


