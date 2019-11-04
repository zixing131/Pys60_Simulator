# -*- coding: utf-8 -*-
from wsg import *

class App(object,):

    def __init__(self):
        self.wnd = Window(None,0,0,SCRX,SCRY,0x193148)
        self.oldhandler = appuifw.app.exit_key_handler
        self.lock = e32.Ao_lock()

        self.p0 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        m = Calc(cn("wsg模块用法"),(FONT,20))
        self.text = StaticText(self.p0,cn("wsg模块用法"),(SCRX-m[0])/2,10,m[0],m[1],0xBB0000)
        m = Calc(cn("1.Window"),(FONT,16))
        self.link1 = SysLink(self.p0,cn("1.Window"),20,40,2+m[0]+2,2+m[1]+2,self.OnClicked1)
        m = Calc(cn("2.PushButton"),(FONT,16))
        self.link2 = SysLink(self.p0,cn("2.PushButton"),20,70,2+m[0]+2,2+m[1]+2,self.OnClicked2)
        m = Calc(cn("3.CheckButton"),(FONT,16))
        self.link3 = SysLink(self.p0,cn("3.CheckButton"),20,100,2+m[0]+2,2+m[1]+2,self.OnClicked3)
        m = Calc(cn("4.RadioButton"),(FONT,16))
        self.link4 = SysLink(self.p0,cn("4.RadioButton"),20,130,2+m[0]+2,2+m[1]+2,self.OnClicked4)
        m = Calc(cn("5.GroupButton"),(FONT,16))
        self.link5 = SysLink(self.p0,cn("5.GroupButton"),20,160,2+m[0]+2,2+m[1]+2,self.OnClicked5)
        m = Calc(cn("6.SysLink"),(FONT,16))
        self.link6 = SysLink(self.p0,cn("6.SysLink"),20,190,2+m[0]+2,2+m[1]+2,self.OnClicked6)
        m = Calc(cn("7.StaticText"),(FONT,16))
        self.link7 = SysLink(self.p0,cn("7.StaticText"),20,220,2+m[0]+2,2+m[1]+2,self.OnClicked7)
        m = Calc(cn("8.StaticEdit"),(FONT,16))
        self.link8 = SysLink(self.p0,cn("8.StaticEdit"),20,250,2+m[0]+2,2+m[1]+2,self.OnClicked8)
        m = Calc(cn("9.Trackbar"),(FONT,16))
        self.link9 = SysLink(self.p0,cn("9.Trackbar"),20,280,2+m[0]+2,2+m[1]+2,self.OnClicked9)
        
        f = open(path+"Window.txt")
        c = f.read()
        f.close()
        self.p1 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit1 = StaticEdit(self.p1,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p1.hide()
        
        f = open(path+"PushButton.txt")
        c = f.read()
        f.close()
        self.p2 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit2 = StaticEdit(self.p2,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p2.hide()
        
        f = open(path+"CheckButton.txt")
        c = f.read()
        f.close()
        self.p3 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit3 = StaticEdit(self.p3,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p3.hide()
        
        f = open(path+"RadioButton.txt")
        c = f.read()
        f.close()
        self.p4 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit4 = StaticEdit(self.p4,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p4.hide()
        
        f = open(path+"GroupButton.txt")
        c = f.read()
        f.close()
        self.p5 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit5 = StaticEdit(self.p5,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p5.hide()
        
        f = open(path+"SysLink.txt")
        c = f.read()
        f.close()
        self.p6 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit6 = StaticEdit(self.p6,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p6.hide()
        
        f = open(path+"StaticText.txt")
        c = f.read()
        f.close()
        self.p7 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit7 = StaticEdit(self.p7,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p7.hide()
        
        f = open(path+"StaticEdit.txt")
        c = f.read()
        f.close()
        self.p8 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit8 = StaticEdit(self.p8,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p8.hide()
        
        f = open(path+"Trackbar.txt")
        c = f.read()
        f.close()
        self.p9 = Panel(self.wnd,0,0,SCRX,SCRY,0x193148)
        self.edit9 = StaticEdit(self.p9,cn(c),0,0,SCRX,SCRY,0xEEF2FB,16,0)
        self.p9.hide()

    def OnReturn1(self):
        self.p1.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked1(self):
        self.p0.hide()
        self.p1.show()
        appuifw.app.exit_key_handler = self.OnReturn1

    def OnReturn2(self):
        self.p2.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked2(self):
        self.p0.hide()
        self.p2.show()
        appuifw.app.exit_key_handler = self.OnReturn2

    def OnReturn3(self):
        self.p3.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked3(self):
        self.p0.hide()
        self.p3.show()
        appuifw.app.exit_key_handler = self.OnReturn3

    def OnReturn4(self):
        self.p4.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked4(self):
        self.p0.hide()
        self.p4.show()
        appuifw.app.exit_key_handler = self.OnReturn4

    def OnReturn5(self):
        self.p5.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked5(self):
        self.p0.hide()
        self.p5.show()
        appuifw.app.exit_key_handler = self.OnReturn5

    def OnReturn6(self):
        self.p6.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked6(self):
        self.p0.hide()
        self.p6.show()
        appuifw.app.exit_key_handler = self.OnReturn6

    def OnReturn7(self):
        self.p7.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked7(self):
        self.p0.hide()
        self.p7.show()
        appuifw.app.exit_key_handler = self.OnReturn7

    def OnReturn8(self):
        self.p8.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked8(self):
        self.p0.hide()
        self.p8.show()
        appuifw.app.exit_key_handler = self.OnReturn8

    def OnReturn9(self):
        self.p9.hide()
        self.p0.show()
        appuifw.app.exit_key_handler = self.End

    def OnClicked9(self):
        self.p0.hide()
        self.p9.show()
        appuifw.app.exit_key_handler = self.OnReturn9

    def Start(self):
        self.wnd.run()
        appuifw.app.exit_key_handler = self.End
        self.lock.wait()

    def End(self):
        self.wnd.exit()
        appuifw.app.exit_key_handler = self.oldhandler
        self.lock.signal()
        appuifw.app.set_exit()

    def __del__(self):
        pass

app = App()
app.Start()
