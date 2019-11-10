import sys
sys.path.append(r"c:\python")
from wsg import *

class App1(object,):

    def __init__(self):
        self.wnd = Window()
        self.button1 = PushButton(self.wnd,cn("Move"),20,20,100,20,self.OnClicked,0,12)
        self.button2 = CheckButton(self.wnd,cn("检查"),20,60,16+4+16*2,20)
        self.button2.SetState(True)
        self.button3 = RadioButton(self.wnd,cn("互斥"),20,100,16+4+16*2,20)
        self.button4 = GroupButton(self.wnd,cn("组框"),20,140,100,40,12)
        self.button5 = PushButton(self.button4,cn("嵌套"),10,16,60,20,self.HelloWorld,0,12)
        self.link = SysLink(self.wnd,cn("链接"),20,200,2+16*2+2,2+16+2,self.HelloWorld)
        self.text = StaticText(self.wnd,cn("文字"),20,230,100,16)
        self.edit = StaticEdit(self.wnd,cn("静态编辑控件"),20,250,100,20,0xFFFFFF,10,0)
        self.trackbar = Trackbar(self.wnd,20,280,100,20+2+12,5,0,100,40,True,u"%d",Trackbar.FOLLOW,0x808080,12)
        self.ismoved = False
        self.oldhandler = appuifw.app.exit_key_handler
        self.lock = e32.Ao_lock()

    def HelloWorld(self):
        appuifw.note(cn("Hello World!"))

    def OnClicked(self): 
        if not self.ismoved:
            self.button1.Move(10,10,SCRX-20,30)
            self.button2.Move(10,50,SCRX-20,30)
            self.button3.Move(10,90,SCRX-20,30)
            self.button4.Move(10,130,SCRX-20,50)
            self.button5.Move(10,16,SCRX-40,20)
            self.link.Move(10,190,SCRX-20,30)
            self.text.Move(10,220,SCRX-20,16)
            self.edit.Move(10,240,SCRX-20,30)
            self.trackbar.Move(10,280,SCRX-20,40)
            self.ismoved = True
        else:
            appuifw.note(cn("已移动过！"))

    def Start(self):
        self.wnd.keyboard(1)
        self.wnd.run()
        appuifw.app.exit_key_handler = self.End
        self.lock.wait()

    def End(self):
        self.wnd.exit()
        appuifw.app.exit_key_handler = self.oldhandler
        self.lock.signal()

    def __del__(self):
        pass

app = App1()
app.Start()