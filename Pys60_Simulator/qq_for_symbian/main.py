# -*- coding: utf-8 -*-
import os
import sys
path = os.getcwd()
index = path.rfind('\\')
path=path[:index]
sys.path.append(path)
import appuifw as ui
from zui import *

class Demo(object, ):
    __module__ = __name__

    def __init__(self):
        self.wnd = Window()
        self.label_username = Label(self.wnd, cn('账号：'), 38, 71)
        self.label_password = Label(self.wnd, cn('密码：'), 38, 100)
        #self.link.SetColor(1921983)
        self.txt_username = Textbox(self.wnd,cn('请输入账号'),78,69,120,24,limit=10)
        self.txt_password = Textbox(self.wnd, cn('请输入密码'), 78, 97, 120, 24,limit=16)
        self.ismoved = False
        self.oldhandler = ui.app.exit_key_handler
        self.lock = e32.Ao_lock()

    def HelloWorld(self):
        ui.note(cn('Hello World!'))

    def OnClicked(self):
        ui.note(cn('Hello World!'))

    def Start(self):
        self.wnd.run()
        ui.app.exit_key_handler = self.End
        self.lock.wait()

    def End(self):
        self.wnd.exit()
        ui.app.exit_key_handler = self.oldhandler
        self.lock.signal()

    def __del__(self):
        pass

if __name__ == '__main__':
    app = Demo()
    app.Start()
