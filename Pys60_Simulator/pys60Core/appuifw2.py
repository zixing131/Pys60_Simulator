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
#screen = (320, 240)
#screen = (360, 640)
from threading import Timer

FFormEditModeOnly = 2
FFormDoubleSpaced = 4
EEventKeyDown = 3
EEventKeyUp = 2
EEventKey = 1
EEventRedraw = 5
EHCenterVTop = 6

from PIL import ImageTk
import time
import thread
import os
import graphics

graphics.screen = screen
EScreen = 1
EHLeftVTop = 0
root = tk.Tk()
root.title('Pys60 Simulator')
root.geometry(str(screen[0])+'x'+str(screen[1]))
root.resizable(0, 0)

cv = tk.Canvas(root, width=screen[0], height=screen[1], background='white')

def on_closing():
    abort()

root.protocol("WM_DELETE_WINDOW", on_closing)

def available_fonts():
    return ['dense', 'normal']
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
        self.root.geometry(str(screen[0])+'x'+str(screen[1]))
        self.root.resizable(0, 0)
        self.cv = cv
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind_all(sequence="<KeyPress>", func=self.processKeyPressEvent)
        self.cv.bind_all(sequence="<KeyRelease>", func=self.processKeyUpEvent)
        self.cv.bind_all(sequence="<Button-1>", func=self.mouseLeftButtonEvent)
        self.cv.bind_all(sequence="<ButtonRelease-1>", func=self.mouseLeftButtonReleaseEvent)

        self.lastimg = None
        self.menu_key_handler = None
        self.size = screen
        self.font = ['font1', 'font2']
        self.lastkeytime = time.time()
        self.allEvents = []
        self.allTouchEvents = []

    def begin_redraw(self):
        print('begin_redraw')
        pass

    def end_redraw(self):
        print('end_redraw')
        pass

    def callEvents(self, evt):
        keycode = evt["keycode"]
        for i in self.allEvents:
            if (keycode == i[0]):
                i[1]()

    def processKeyPressEvent(self, evt):
        flag = time.time() - self.lastkeytime
        self.lastkeytime = time.time()
        keytype = 1
        if(flag<0.1):
            keytype = 2

        if evt.type == "2":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1
            key_mapping = {
                'q': (0, 164),
                'w': (0, 165),
                'up': (63497, 16),
                'down': (63498, 17),
                'left': (63495, 14),
                'right': (63496, 15),
               'space': (63557, 167),
                'backspace': (8, 0)
            }

            if mykey in key_mapping:
                args = {
                    "keycode": key_mapping[mykey][0],
                    "scancode": key_mapping[mykey][1],
                    "type": keytype,
                    "modifiers": 0
                }
                self.callEvents(args)

            if key != -1:
                args = {
                    "keycode": 0x30 + key,
                    "scancode": 1,
                    "type": keytype,
                    "modifiers": 0
                }
                self.callEvents(args)

    def check_event_and_execute(self, event, button_event):
        for evt in self.allTouchEvents:
            if evt[0] == button_event:
                x1, y1 = evt[2][0]
                x2, y2 = evt[2][1]
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    evt[1]((event.x, event.y))

    def mouseLeftButtonEvent(self, event):
        self.check_event_and_execute(event, key_codes.EButton1Down)

    def mouseLeftButtonReleaseEvent(self, event):
        self.check_event_and_execute(event, key_codes.EButton1Up)

    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def processKeyUpEvent(self, evt):
        keytype = 3
        print(evt)
        if evt.type == "3":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1

            key_map = {
                'q': (0, 164),
                'w': (0, 165),
                'up': (63497, 16),
                'down': (63498, 17),
                'left': (63495, 14),
                'right': (63496, 15),
                'space': (63557, 167),
                'backspace': (8, 0)
            }

            if mykey in key_map:
                args = {
                    "keycode": key_map[mykey][0],
                    "scancode": key_map[mykey][1],
                    "type": keytype,
                    "modifiers": 0
                }
                if self.event_callback:
                    self.event_callback(args)
                if mykey == 'w' and app.exit_key_handler:
                    app.exit_key_handler()
                self.callEvents(args)

            if key != -1:
                args = {
                    "keycode": 0x30 + key,
                    "scancode": 1,
                    "type": keytype,
                    "modifiers": 0
                }
                if self.event_callback:
                    self.event_callback(args)
                self.callEvents(args)

        if evt.type == "4":
            pass
            # print("鼠标： %s" % evt.num)

    def blit(self,img,source=None,target=None,scale=False,mask=None):
        graphics.Image.blit(self,img,source,target,scale,mask)
    def clear(self, color):
        graphics.Image.clear(self, color)

    def bind(self, key, event, point=0):
        if 0x101 <= key <= 0x10A:
            self.allTouchEvents.append((key, event, point))
        else:
            self.allEvents.append((key, event))

    def blitSelf(self):
        try:
            img = ImageTk.PhotoImage(image=self.image, master=self.cv)
            self.lastimg = img
            self.cv.create_image(0 + img.width() / 2, 0 + img.height() / 2, image=img)
            self.root.update()
        except Exception as e:
            print(e)
    def update(self):
        self.redraw()

    def redraw(self, t=1):
        if self.redraw_callback is None:
            return
        try:
            self.redraw_callback()
        except:
            try:
                self.redraw_callback(())
            except Exception as ex:
                print(ex)


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

    def showMenu(self):
        self.showingMenu = 1
        self.menuBox = tk.Listbox(self.cv)
        for item in app.menu:
            self.menuBox.insert(tk.END, item[0])
        self.menuwindow = self.cv.create_window((120, 160), window=self.menuBox, height=320, width=240)
        while 1:
            self.root.update()

    def processKeyboardEvent(self, evt):
        if evt.type == "2":
            mykey = evt.keysym.lower()
            key = -1
            try:
                key = int(mykey)
            except:
                key = -1
            if (mykey == 'q'):
                args = {"keycode": 0, "scancode": 164, "type": 3}
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
                args = {"keycode": 0x30 + key, "scancode": 0x30 + key, "type": 1}
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'up'):
                args = {"keycode": 63497, "scancode": key_codes.EScancodeUpArrow, "type": 1}
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'down'):
                args = {"keycode": 63498, "scancode": key_codes.EScancodeDownArrow, "type": 1}
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'left'):
                args = {"keycode": 63495, "scancode":  key_codes.EScancodeLeftArrow, "type": 1}
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'right'):
                args = {"keycode": 63496, "scancode": key_codes.EScancodeRightArrow, "type": 1}
                if (self.event_callback): self.event_callback(args)
            if (mykey == 'space'):
                args = {"keycode": 63557, "scancode": key_codes.EScancodeSelect, "type": 1}
                if (self.event_callback): self.event_callback(args)

    def set(self, text):
        self.textbox.insert("insert", text)
        while 1:
            self.root.update()


class Text_display():
    def __init__(self, text, skinned):
        self.text = text
        self.skinned = skinned
Listbox2 = Listbox

class Application(object):
    def full_name(self):
        # Todo
        return "d:\\"

    def set_exit(self):
        pass

    def set_tabs(self,N,c):
        pass

    def activate_tab(self,N):
        pass

    def __init__(self, **keys):
        self.running = 1
        self.CC = None
        self.body = None
        self.screen = (screen[0], screen[1])
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
            if(root):
                root.update()
        # self.body.redraw()
        except Exception as ex:
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

class text:
    @staticmethod
    def measure_text(text, font):
        return graphics.getTextFontWidth(text,font)
import e32

e32 = e32
graphics.app=app
