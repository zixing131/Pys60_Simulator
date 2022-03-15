#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 19:48
# @Author  : zixing
# @QQun    : 140369358
# @File    : qqcontrols.py
# @Software: PyCharm
import mypath
mypath = mypath.getmypath("\\python\\pysoft\\pyqq\\")
cachePath = mypath + "cache\\"
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


    def getChildrenType(self,WalkControls,Type):
        if(WalkControls.Controls!=None and len(WalkControls.Controls)>0):
            #有子控件，遍历子控件
            for i in WalkControls.Controls:
                if (i.isShow == 1):
                    if (isinstance(i, Type)):
                        return i
                    elif(isinstance(i, Control)):
                        tt = self.getChildrenType(i,Type)
                        if(tt!=None):
                            return tt
        else:
            return None

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


class DynamicLabel(Control):

    def __init__(self,text=[''],pos=(0,0),color=0x0,fontsize=15,nowdymIndex = 1):
        Control.__init__(self, pos, color, fontsize)
        self.text = text
        self.nowdymIndex = nowdymIndex
        self.canGetFocus = 0
    def loopIndex(self):
        if(self.nowdymIndex>len(self.text)-1):
            self.nowdymIndex=0
        else:
            self.nowdymIndex+=1

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        baseImg.text(self.pos,self.text[self.nowdymIndex%len(self.text)],self.color,('dense',self.fontsize))


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
            if(self.Parent.isShow):
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
        return True
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

#网易云专用，宫格歌单列表
class MusicListControl(Control):
    def __init__(self, pos=(0, 0), size=(240, 320), color=0x0, fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.size = size
        #图标的大小
        self.miniconSize = (50,50)
        self.NowX = 0
        self.NowY = 0
        self.MaxX = int(self.size[0] / (self.miniconSize[0] + 20))
        self.MaxY = int(self.size[1] / (self.miniconSize[1] + 20 + 20))
        self.Data = []

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        #画背景
        ListImg = ph.Image.new(self.size)
        ListImg.clear(self.color)

        nowXp = 0
        nowYp = 0
        #X轴的间隙
        xGap = int((self.size[0] - (self.miniconSize[0] * self.MaxX)) / (self.MaxX+1))
        #Y轴的间隙
        YGap = int((self.size[1] - (self.miniconSize[1] * self.MaxY)) / (self.MaxY + 1))

        for i in range(len(self.Data)):
            nowblock= self.Data[i]
            name = nowblock.name
            copywriter =  nowblock.copywriter
            picUrl =  nowblock.picUrl
            x = i% self.MaxX
            y = int(i / self.MaxX)

            nowXp = (x+1) * xGap + x*self.miniconSize[0]
            nowYp = (y+1) * YGap + y*self.miniconSize[1]
            print(i,x,y,nowXp,nowYp,xGap,YGap,self.MaxX,self.MaxY)
            ListImg.rectangle((nowXp ,nowYp ,nowXp + self.miniconSize[0],nowYp+ self.miniconSize[1]), fill=0x0,width=0)



        baseImg.blit(ListImg,target=self.pos)
    def show(self):
        self.isShow = 1
    def hide(self):
        self.isShow = 0

    def pressLeft(self):
        for i in self.Controls:
            handle = i.pressLeft()
            if (handle == True):
                return handle

    def indexDown(self):
        pass

    def indexUp(self):
        pass
    def pressOk(self):
        pass

#qq专用，好友列表
class FriendListControl(Control):
    def __init__(self,pos=(0, 0),size=(240,320),color=0x0, fontsize=15):
        Control.__init__(self, pos, color, fontsize)
        self.size = size
        #基大分组坐标
        self.nowBaseX = 0
        #大分组下标
        self.nowindexX = 0
        #基小分组坐标
        self.nowBaseY = 0
        #分组内的下标
        self.nowindexY = -1

        self.nowAllBaseX = 0
        self.nowALlIndexX = 0

        self.frindList = {}
        #分组的名称列表
        self.Biglist = []
        self.allList = []
        #小图标的每行高度
        self.miniconHeight = 18
        #大图标每行的高度
        self.maxiconHeight = 36


    def setFriendList(self,l):
        self.allList = []
        self.Biglist = []
        self.frindList = l
        for i in l:
            #名称，是否已经打开
            self.Biglist.append([i,0])
            #名称，是否为标题，是否已经打开,uin,icon
            self.allList.append(([i,1,0,0,'']))
            for j in l[i]['mems']:
                name = j['name']
                uin = j['uin']
                self.allList.append(([name, 0, 0,uin,mypath+'qqicon.jpg']))


    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        #画背景
        baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), fill=self.color,width=0)
        #画选择背景
        #baseImg.rectangle((self.pos[0] + 1 , self.pos[1]+self.nowindexX*self.miniconHeight, self.pos[0] + self.size[0] - 1 , self.pos[1] +(self.nowindexX+1)*self.miniconHeight),
        #                  fill=0xA5D5F3, width=0)
        # 分组没有打开的时候
        #maxrows = int(self.size[1] / self.miniconHeight) + 1  # 最大可能的行数
        maxrows = len(self.allList)
        nowx = self.pos[1]

        lastIsOpening = 0
        for i in range(self.nowAllBaseX,maxrows):
            #如果超过绘制区域，跳出循环
            if(nowx>self.pos[1] + self.size[1]):
                break
            #当前绘制的项目
            nowItem = self.allList[i]
            nowtitle = cn(nowItem[0])
            isTitleItem = nowItem[1]
            isOpening =  nowItem[2]
            nowUin = nowItem[3]
            nowIcon = nowItem[4]

            nowheight =  self.miniconHeight
            if (isTitleItem == 0 and self.nowALlIndexX == i):
                nowheight = self.maxiconHeight

            #绘制选中的项目的背景
            if(self.nowALlIndexX == i):
                #绘制选中背景
                baseImg.rectangle((self.pos[0],
                                   nowx,
                                   self.pos[0] + self.size[0],
                                   nowx + nowheight
                                   ),
                                  fill=0xA5D5F3, width=0)

            if(isTitleItem == 1):
                lastIsOpening = isOpening
                if (isOpening == 0):
                    baseImg.polygon((
                        self.pos[0] + 7,
                        nowx+ 3,
                        self.pos[0] + 7,
                        nowx + 15,
                        self.pos[0] + 13,
                        nowx + 9,
                    ),
                        fill=0x33bbff, width=0)
                else:
                    baseImg.polygon((
                        self.pos[0] + 1,
                        nowx + 6,
                        self.pos[0] + 13,
                        nowx + 6,
                        self.pos[0] + 7,
                        nowx + 12,
                    ),
                        fill=0x33bbff, width=0)
                txtcolor = 0xA5D5F3
                if (self.nowALlIndexX == i):
                    txtcolor = 0x0
                baseImg.text((self.pos[0] + 16, nowx + self.fontsize),
                             nowtitle,
                             txtcolor,
                             ('dense', self.fontsize))

            elif(isTitleItem == 0):
                if(lastIsOpening == 1):
                    img = ph.Image.open(nowIcon)
                    if (self.nowALlIndexX == i):
                        img = img.resize((32, 32))
                    else:
                        img = img.resize((16, 16))
                    img.save('qqheadimgicon.jpg')
                    baseImg.blit(ph.Image.open( 'qqheadimgicon.jpg'), target=(self.pos[0] + 16,nowx))
                    txtcolor = 0xA5D5F3
                    baseT=16
                    if (self.nowALlIndexX == i):
                        txtcolor = 0x0
                        baseT = 32
                    baseImg.text((self.pos[0] + 16 + baseT +5, nowx + self.fontsize),
                                 nowtitle,
                                 txtcolor,
                                 ('dense', self.fontsize))
                else:
                    nowheight = 0

            nowx = nowx +  nowheight



        '''
        nowx = 0 
        for i in range(self.nowBaseX,maxrows):
            nwobig  =self.Biglist[i]
            nowtitle = cn(nwobig[0])
            nowOpening = nwobig[1]
            baseImg.rectangle((self.pos[0] ,
                               self.pos[1] + (nowx+1) * self.miniconHeight,
                               self.pos[0] + self.size[0] ,
                               self.pos[1]  + (nowx + 1) * self.miniconHeight
                               ),
                              fill=0xA5D5F3, width=0)
            if(nowOpening == 0):
                baseImg.polygon((
                        self.pos[0] + 7,
                        self.pos[1] + nowx * self.miniconHeight + 3,
                        self.pos[0] + 7,
                        self.pos[1] + nowx * self.miniconHeight + 15,
                        self.pos[0] + 13,
                        self.pos[1] + nowx * self.miniconHeight + 9,
                                   ),
                                  fill=0x33bbff, width=0)
            else:
                baseImg.polygon((
                    self.pos[0] + 1,
                    self.pos[1] + nowx * self.miniconHeight + 6,
                    self.pos[0] + 13,
                    self.pos[1] + nowx * self.miniconHeight + 6,
                    self.pos[0] + 7,
                    self.pos[1] + nowx * self.miniconHeight + 12,
                ),
                    fill=0x33bbff, width=0)

            txtcolor = 0xA5D5F3
            if(self.nowindexX == i):
                txtcolor = 0x0
            baseImg.text((self.pos[0]+16, self.pos[1] + (nowx+1) * self.miniconHeight),
                         nowtitle,
                         txtcolor,
                         ('dense', self.fontsize))
            nowx += 1
        '''

    def show(self):
        self.isShow = 1
    def hide(self):
        self.isShow = 0

    def pressLeft(self):
        for i in self.Controls:
            handle = i.pressLeft()
            if(handle == True):
                return handle

    def indexDown(self):
        nowItem = self.allList[self.nowALlIndexX]
        nowtitle = cn(nowItem[0])
        isTitleItem = nowItem[1]
        isOpening = nowItem[2]
        nowUin = nowItem[3]
        nowIcon = nowItem[4]
        if(isTitleItem==1 and isOpening == 0):
            while(self.nowALlIndexX<len(self.allList)-1):
                if(self.allList[self.nowALlIndexX + 1][1] == 0):
                    self.nowALlIndexX += 1
                    continue
                else:
                    self.nowALlIndexX += 1
                    break
            if(self.nowALlIndexX == len(self.allList) -1 ):
                self.nowALlIndexX = 0
        else:
            if(self.nowALlIndexX+1>len(self.allList)-1):
                self.nowALlIndexX = 0
            else:
                self.nowALlIndexX+=1

        nowItem = self.allList[self.nowALlIndexX]
        isTitleItem = 0
        if(nowItem[1]==0):
            isTitleItem = 1
        t =  self.nowALlIndexX - (int(self.size[1] / self.miniconHeight)) - isTitleItem
        if(t<0):
            t=0
        self.nowAllBaseX = t


    def indexUp(self):
        nowItem = self.allList[self.nowALlIndexX]
        nowtitle = cn(nowItem[0])
        isTitleItem = nowItem[1]
        isOpening = nowItem[2]
        nowUin = nowItem[3]
        nowIcon = nowItem[4]

        lastIsOpening = -1
        i = self.nowALlIndexX-1
        while(i>=0):
            if(self.allList[i][1] == 1):
                lastIsOpening = self.allList[i][2]
                break
            i-=1
        if(lastIsOpening == -1):
            i = len(self.allList)-1
            while (i > 0):
                if (self.allList[i][1] == 1):
                    lastIsOpening = self.allList[i][2]
                    break
                i-=1


        if (isTitleItem ==1 and lastIsOpening == 0):
            while (self.nowALlIndexX >= 0):
                if (self.allList[self.nowALlIndexX - 1][1] == 0):
                    self.nowALlIndexX -= 1
                    continue
                else:
                    self.nowALlIndexX -= 1
                    break
            if (self.nowALlIndexX == -1):
                self.nowALlIndexX = len(self.allList) - 1
                while 1:
                    if(self.allList[self.nowALlIndexX-1][1]==1):
                        self.nowALlIndexX -= 1
                        break
                    else:
                        self.nowALlIndexX -= 1
                        continue

        else:
            if (self.nowALlIndexX - 1 < 0):
                self.nowALlIndexX = len(self.allList)-1
            else:
                self.nowALlIndexX -= 1

        nowItem = self.allList[self.nowALlIndexX]
        isTitleItem = nowItem[1]

    def pressOk(self):
        #是标题
        if(self.allList[self.nowALlIndexX][1] == 1):
            if(self.allList[self.nowALlIndexX][2] == 1):
                self.allList[self.nowALlIndexX][2] = 0
            else:
                self.allList[self.nowALlIndexX][2] = 1

        else:
            #打开发送消息的界面
            pass


class Panel(Control):

    # def Crea_Maschera(self,imgg):
    #     width, height = imgg.size
    #     mask = ph.Image.new(imgg.size, '1')
    #     transparent_color = imgg.getpixel((0, 0))[0]
    #     for y in range(height):
    #         line = imgg.getpixel([(x, y) for x in range(width)])
    #         for x in range(width):
    #             if line[x] == transparent_color:
    #                 pass
    #             else:
    #                 mask.point((x, y), 0xff00ff)
    #     return mask

    def __init__(self,text='', pos=(0, 0),size=(240,320), color=0x0, fontsize=15,bgImage='',useMask = 0):
        Control.__init__(self, pos, color, fontsize)
        #图片是否居中显示
        self.isCenterImg = 0
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
        self.resizeSize = 0
        self.useMask = useMask
        self.firstRun = 1

    def setRightMenuEvent(self,event):
        ui.app.exit_key_handler = event

    def Crea_Maschera(self,imgg):
        width, height = imgg.size
        mask = ph.Image.new(imgg.size, '1')
        transparent_color = imgg.getpixel((0, 0))[0]
        for y in range(height):
            line = imgg.getpixel([(x, y) for x in range(width)])
            for x in range(width):
                if line[x] == transparent_color:
                    mask.point((x, y),0x0)
        return mask

    def Paint(self, baseImg):
        if (self.isShow == 0):
            return
        if (self.useMask == 0):
            baseImg.rectangle((self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), fill=self.color,width=0)
        if(self.bgImage!=''):
            bgimg = ph.Image.open(self.bgImage)
            if(self.resizeSize!=0):
                bgimg.resize(self.resizeSize)
            if(self.useMask==1):
                if(self.firstRun ==1):
                    self.Mask = self.Crea_Maschera(bgimg)
                    self.firstRun = 0
            if(self.isCenterImg == 0):
                if(self.useMask==1):
                    baseImg.blit(bgimg, target=self.pos,mask = self.Mask)
                else:
                    baseImg.blit(bgimg,target=self.pos)
            else:
                left = int((self.size[0] - bgimg.size[0])/2)
                top = int((self.size[1] - bgimg.size[1])/2)
                if (self.useMask == 1):
                    baseImg.blit(bgimg, target=(left, top), mask=self.Mask)
                else:
                    baseImg.blit(bgimg, target=(left, top))

        if(self.showMenuBar):
            baseImg.rectangle(( 0,self.height - self.MenuBarHeight ,self.width,self.height),self.MenuBarBgColor,self.MenuBarBgColor)
            baseImg.text((int(self.fontsize/2), self.height - int(self.fontsize/2) ), self.leftMenuName, self.MenuBarTextColor,
                         ('dense', self.fontsize))
            p = self.textLen(self.rightMenuName, ('dense', self.fontsize))
            baseImg.text((self.width - p - int(self.fontsize / 2), self.height - int(self.fontsize / 2)), self.rightMenuName,
                         self.MenuBarTextColor,
                         ('dense', self.fontsize))

        childMenu = self.getChildrenType(self,Menu)
        if(childMenu!=None):
            for i in self.Controls:
                if(i!=childMenu):
                    i.Paint(baseImg)
            childMenu.Paint(baseImg)
        else:
            for i in self.Controls:
                i.Paint(baseImg)

    def show(self):
        self.isShow = 1
    def hide(self):
        self.isShow = 0

    def pressLeft(self):
        for i in self.Controls:
            handle = i.pressLeft()
            if(handle==True):
                return handle

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
        childMenu = self.getChildrenType(self,Menu)
        if (childMenu != None):
            childMenu.MenuUp()
            return
        for child in visiableChildrens:
            if ( isinstance(child,Textbox) and child.TextEditing == 1):
                return
            if (isinstance(child, FriendListControl) and child.isShow == 1):
                child.indexUp()

        self._Form__index -= 1
        if (self._Form__index < 0):
            self._Form__index = len(visiableChildrens) - 1
        self.setChildrenFocus(visiableChildrens[self._Form__index],visiableChildrens)

    def indexDown(self):
        visiableChildrens = self.getVisiableChildrens()
        if (len(visiableChildrens) == 0):
            return

        childMenu =  self.getChildrenType(self,Menu)
        if(childMenu!=None):
            childMenu.MenuDown()
            return

        for child in visiableChildrens:
            if (isinstance(child,Textbox) and child.TextEditing == 1):
                return
            if (isinstance(child, FriendListControl) and child.isShow == 1):
                child.indexDown()

        self._Form__index += 1
        if (self._Form__index > len(visiableChildrens) - 1):
            self._Form__index = 0
        self.setChildrenFocus(visiableChildrens[self._Form__index],visiableChildrens)

    def pressOk(self):
        visiableChildrens = self.getVisiableChildrens()
        if (len(visiableChildrens) == 0):
            return

        childMenu =  self.getChildrenType(self,Menu)
        if (childMenu != None):
            childMenu.pressOk()
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
                handle = i.pressLeft()
                if(handle==True):
                    return handle

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


