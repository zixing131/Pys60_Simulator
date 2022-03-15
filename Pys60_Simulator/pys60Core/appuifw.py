# -*- coding: utf-8 -*- 
# import _appuifw
# from _appuifw import *
from key_codes import *
import key_codes
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
except:
    import Tkinter as tk
import tkMessageBox
import pys60Socket



screen = (240, 320)
#screen = (360, 640)
#screen = (320, 240)
from threading import Timer


FFormEditModeOnly = 2
FFormDoubleSpaced = 4
EEventKeyDown=3
EEventKeyUp = 2
EEventKey=1

from PIL import ImageTk
import time
import thread
import os
import graphics
graphics.screen=screen
EScreen = 1
EHLeftVTop = 0
root = tk.Tk()
cv = tk.Canvas(root, width=screen[0], height=screen[1], background='white')
def on_closing():
    abort()
root.protocol("WM_DELETE_WINDOW", on_closing)

def available_fonts():
    return ['dense','normal']

class Form(list):
    def __init__(self,optcont,flags):
        pass
    def bind(self,keycode,nextitem):
        pass
    def __getitem__(self, item):
        return [[1 for i in range(10)] for i in range(10)]

class Listbox():
    def __init__(self,lst,itemevent):
        pass
    def bind(self,keycode,nextitem):
        pass
    def set_list(self,lst,it):
        pass

class Canvas(graphics.Image):
    def __init__(self, redraw_callback=None, event_callback=None, resize_callback=None):
        graphics.Image.__init__(self, screen, None,self)
        self.redraw_callback = redraw_callback
        self.event_callback = event_callback
        self.root = root
        self.root.title('Pys60 Simulator')
        self.root.geometry(str(screen[0]) + 'x' + str(screen[1]))
        self.root.resizable(0, 0)
        self.cv = cv
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind_all(sequence="<KeyPress>", func=self.processKeyPressEvent)
        self.cv.bind_all(sequence="<KeyRelease>", func=self.processKeyUpEvent)
        self.cv.bind_all(sequence="<Button-1>", func=self.mouseLeftButtonEvent) #鼠标左键按下
        self.cv.bind_all(sequence="<ButtonRelease-1>", func=self.mouseLeftButtonReleaseEvent)  #鼠标左键释放


        self.lastimg = None
        self.menu_key_handler = None
        self.size = screen
        self.font = ['font1', 'font2']
        self.lastkeytime = time.time()
        # self.timer = Timer(0,self.redraw,())
        # self.timer.start()
        self.lastkeytime = time.time()
        self.allEvents = []
        self.allTouchEvents = []

    # def rectangle():
    def callEvents(self, evt):
        keycode = evt["keycode"]
        for i in self.allEvents:
            if (keycode == i[0]):
                i[1]()

    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def processKeyPressEvent(self, evt):
        # 打印键盘事件
        flag = time.time() - self.lastkeytime
        self.lastkeytime = time.time()
        keytype = 1
        #if (flag < 0.1):
        #    return
        if(flag<0.1):
            keytype = 2
        #print (keytype)
        if evt.type == "2":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1
            if (mykey == 'q'):
                args = {}
                args["keycode"] = 0
                args["scancode"] = 164
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
            elif (mykey == 'w'):
                args = {}
                args["keycode"] = 0
                args["scancode"] = 165
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                if (app.exit_key_handler): app.exit_key_handler()

            if (key != -1):
                args = {}
                args["keycode"] = 0x30 + key
                args["scancode"] = 1
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'up'):
                args = {}
                args["keycode"] = 63497  # 2
                args["scancode"] = 16
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'down'):
                args = {}
                args["keycode"] = 63498  # 8
                args["scancode"] = 17
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'left'):
                args = {}
                args["keycode"] = 63495  # 4
                args["scancode"] = 14
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'right'):
                args = {}
                args["keycode"] = 63496  # 6
                args["scancode"] = 15
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'space'):
                args = {}
                args["keycode"] = 63557  # 5
                args["scancode"] = 167
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'backspace'):
                args = {}
                args["keycode"] = 8  # backspace
                args["scancode"] = 0
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)

        if evt.type == "4":
            pass
            # print("鼠标： %s" % evt.num)

    def mouseLeftButtonEvent(self,event):
        #print event,event.x,event.y
        for evt in self.allTouchEvents:
            if(evt[0]  == key_codes.EButton1Down):
                if( evt[2][0][0] <= event.x and  evt[2][1][0] >= event.x and evt[2][0][1] <= event.y and  evt[2][1][1] >= event.y):
                    evt[1]((event.x,event.y))

    def mouseLeftButtonReleaseEvent(self,event):
        #print event, event.x, event.y
        for evt in self.allTouchEvents:
            if (evt[0] == key_codes.EButton1Up):
                if( evt[2][0][0] <= event.x and  evt[2][1][0] >= event.x and evt[2][0][1] <= event.y and  evt[2][1][1] >= event.y):
                    evt[1]((event.x, event.y))

    #
    # print(evt.type)
    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def processKeyUpEvent(self, evt):
        # 打印键盘事件
        keytype = 3
        #print (keytype)
        if evt.type == "3":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1
            if (mykey == 'q'):
                args = {}
                args["keycode"] = 0
                args["scancode"] = 164
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
            elif (mykey == 'w'):
                args = {}
                args["keycode"] = 0
                args["scancode"] = 165
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                if (app.exit_key_handler): app.exit_key_handler()
            if (key != -1):
                args = {}
                args["keycode"] = 0x30 + key
                args["scancode"] = 1
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'up'):
                args = {}
                args["keycode"] = 63497
                args["scancode"] = 16
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'down'):
                args = {}
                args["keycode"] = 63498
                args["scancode"] = 17
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'left'):
                args = {}
                args["keycode"] = 63495
                args["scancode"] = 14
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'right'):
                args = {}
                args["keycode"] = 63496
                args["scancode"] = 15
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'space'):
                args = {}
                args["keycode"] = 63557
                args["scancode"] = 167
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)
            if (mykey == 'backspace'):
                args = {}
                args["keycode"] = 8  # backspace
                args["scancode"] = 0
                args["type"] = keytype
                args["modifiers"] = 0
                if (self.event_callback): self.event_callback(args)
                self.callEvents(args)

        if evt.type == "4":
            pass
            # print("鼠标： %s" % evt.num)

    #
    # print(evt.type)
    def blit(self, img, target=(0, 0),scale =False):
        try:
            img = ImageTk.PhotoImage(image=img.image, master=self.cv)
            self.lastimg = img
            self.cv.create_image(target[0] + img.width() / 2, target[1] + img.height() / 2, image=img)
            # self.cv.create_line(10,10,240,320,width=5)
            self.root.update()
        except Exception, e:
            pass
            # print(e)

    def clear(self, color):
        pass

    def bind(self, key, event,point = 0):
        if(key >= 0x101 and key <= 0x10A):
            self.allTouchEvents.append((key, event,point))
        else:
            self.allEvents.append((key, event))

    def update(self):
        self.redraw()

    def redraw(self,t=1):
        try:
            # print(self.redraw_callback)
            if (self.redraw_callback == None):
                return
            else:
                try:
                    self.redraw_callback()
                except:
                    try:
                        self.redraw_callback(())
                    except Exception,ex:
                        print(ex)

            # self.timer = Timer(0,self.redraw,())
            # self.timer.start()
        except Exception, ex:
            print("appuifw 230 ",ex)


class Text(object):
    def __init__(self, redraw_callback=None, event_callback=None, resize_callback=None):
        self.event_callback = event_callback
        self.root = root
        self.root.title('Pys60 Simulator')
        self.root.geometry('240x320')
        self.root.resizable(0, 0)
        self.cv = cv
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind_all(sequence="<KeyPress>", func=self.processKeyboardEvent)
        self.lastimg = None
        self.textbox = tk.Text(self.cv, width=240, height=320, bg='white', fg='black')
        self.textwindow = self.cv.create_window((120, 160), window=self.textbox, height=320, width=240)
        self.showingMenu = 0
        self.font = ['font1', 'font2']
        # root.mainloop()

    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def showMenu(self):
        self.showingMenu = 1
        self.menuBox = tk.Listbox(self.cv)
        for item in app.menu:
            self.menuBox.insert(tk.END, item[0])
        self.menuwindow = self.cv.create_window((120, 160), window=self.menuBox, height=320, width=240)
        while 1:
            self.root.update()

    def processKeyboardEvent(self, evt):
        # 打印键盘事件

        if evt.type == "2":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1
            if (mykey == 'q'):
                args = {}
                args["keycode"] = 0
                args["scancode"] = 164
                args["type"] = 3
                if (self.event_callback): self.event_callback(args)
                if (self.showingMenu == 1):
                    selectIndex = self.menuBox.curselection()[0]
                    if (selectIndex != -1):
                        app.menu[selectIndex][1]()
                        self.showingMenu = 0
                        self.cv.delete(self.menuwindow)
                else:
                    self.showMenu()
            if (mykey == 'w'):
                if (self.showingMenu == 1):
                    self.showingMenu = 0
                    self.cv.delete(self.menuwindow)
                if (app.exit_key_handler): app.exit_key_handler()
            if (key != -1):
                args = {}
                args["keycode"] = 0x30 + key
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'up'):
                args = {}
                args["keycode"] = 63497  # 2
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'down'):
                args = {}
                args["keycode"] = 63498  # 8
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'left'):
                args = {}
                args["keycode"] = 63495  # 4
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'right'):
                args = {}
                args["keycode"] = 63496  # 6
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'space'):
                args = {}
                args["keycode"] = 63557  # 5
                args["scancode"] = 1
                args["type"] = 1
                if (self.event_callback): self.event_callback(args)
                # print("键盘：%s" % evt.keysym)
        # 打印鼠标操作
        if evt.type == "4":
            pass
            # print("鼠标： %s" % evt.num)
        #
        # print(evt.type)

    def set(self, text):
        self.textbox.insert("insert", text)
        while 1:
            self.root.update()


class Application(object):
    def full_name(self):
        # Todo
        return "d:\\"
    def __init__(self, **keys):
        self.running = 1
        self.CC = None
        self.body = None
        self.screen = (0, 0, screen[0], screen[1])
        # thread.start_new_thread(self.refush,())
        self.exit_key_handler=None

    def focus(self):
        pass
    def refush(self):
        while self.running:
            if (self.body != None):
                self.body.update()
                time.sleep(0.1)

    def layout(self, d):
        return [screen]

    def redraw(self,t=1):
        if (self.body):
            self.body.redraw()

    def getscreen(self):
        return self.body.lastimg

    def Yield(self):
        # while 1:
        try:
            if (self.body):
                self.body.update()
        # self.body.redraw()
        except Exception, ex:
            print(ex)
        # time.sleep(0.1)


app = Application()


def abort():
    app.running = 0
    app.body.root.destroy()
    os._exit(0)


os.abort = abort


def note(text, type='info',wait=3):
    if type == "error":
        tkMessageBox.showerror(type.title(), text)
    else:
        tkMessageBox.showinfo(type.title(), text)


def query(text, type='info',defalutvalue=''):
    return True



class popup:
    def __init__(self):
        pass

    def show(self, a, b, c, d, e):
        pass


def InfoPopup():
    return popup()

def popup_menu(name,den):
    return 0

import e32

e32 = e32
graphics.app=app
