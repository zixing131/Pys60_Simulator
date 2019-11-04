# -*- coding: utf-8 -*- 
#import _appuifw
#from _appuifw import *
try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk 
import tkMessageBox 
from PIL import ImageTk
import time
import thread
import os

EScreen = 1

root = tk.Tk()
cv = tk.Canvas(root, width = 240, height = 320,background='white') 
class Canvas():
    def __init__(self,redraw_callback=None,event_callback=None, resize_callback=None):
        self.event_callback=event_callback
        self.root = root
        self.root.title('Pys60 Simulator')
        self.root.geometry('240x320')
        self.root.resizable(0,0)
        self.cv = cv
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind_all(sequence="<KeyPress>", func=self.processKeyboardEvent)
        self.lastimg = None
        self.menu_key_handler = None
        #root.mainloop()
    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def processKeyboardEvent(self, evt):
        #打印键盘事件
		if evt.type == "2":
			mykey = evt.keysym.lower()
			key = -1
			try:
				key = int(mykey)
			except:
				key = -1
			if(mykey == 'q'):
				args = {}
				args["keycode"] = 0
				args["scancode"] = 164
				args["type"] = 3
				self.event_callback(args) 
			if(mykey == 'w'): 
				if(app.exit_key_handler):app.exit_key_handler() 
			if(key!=-1):
				args = {}
				args["keycode"] = 0x30 + key  
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'up'):
				args = {}
				args["keycode"] = 63497 #2
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'down'):
				args = {}
				args["keycode"] = 63498 #8
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'left'):
				args = {}
				args["keycode"] = 63495 #4
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'right'):
				args = {}
				args["keycode"] = 63496 #6
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'space'):
				args = {}
				args["keycode"] = 63557 #5
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			#print("键盘：%s" % evt.keysym)
		#打印鼠标操作
		if evt.type == "4":
			pass
			#print("鼠标： %s" % evt.num)
		#
		#print(evt.type) 
    def blit(self,img):
        img = ImageTk.PhotoImage(img.image,master = self.cv) 
        self.lastimg = img
        self.cv.create_image(img.width()/2,img.height()/2,image = img) 
        #self.cv.create_line(10,10,240,320,width=5)  
        
        self.root.update()
    def bind(self,key,event):
        pass
    def update(self):
        if(self.lastimg):
           self.cv.create_image(self.lastimg.width()/2,self.lastimg.height()/2,image = self.lastimg)  
        self.root.update()
class Text(object):
    def __init__(self,redraw_callback=None,event_callback=None, resize_callback=None):
        self.event_callback=event_callback
        self.root = tk.Tk()
        self.root.title('Pys60 Simulator')
        self.root.geometry('240x320')
        self.root.resizable(0,0)
        self.cv = tk.Canvas(self.root, width = 240, height = 320,background='white') 
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind_all(sequence="<KeyPress>", func=self.processKeyboardEvent)
        self.lastimg = None
        self.textbox=tk.Text(self.cv,width=240,height=320,bg = 'white',fg = 'black')
        self.textwindow = self.cv.create_window((120,160),window=self.textbox,height = 320, width =240)
        self.showingMenu=0
        #root.mainloop()
    # 处理键盘事件，ke为控件传递过来的键盘事件对象
    def showMenu(self):
		self.showingMenu = 1 
		self.menuBox = tk.Listbox(self.cv)
		for item in app.menu:
			self.menuBox.insert(tk.END,item[0])
		self.menuwindow = self.cv.create_window((120,160),window=self.menuBox,height = 320, width =240)
		while 1:
			self.root.update()
		
    def processKeyboardEvent(self, evt):
        #打印键盘事件
		if evt.type == "2":
			mykey = evt.keysym.lower()
			key = -1
			try:
				key = int(mykey)
			except:
				key = -1
			if(mykey == 'q'):
				args = {}
				args["keycode"] = 0
				args["scancode"] = 164
				args["type"] = 3
				if(self.event_callback):self.event_callback(args) 
				if(self.showingMenu == 1):					
					selectIndex = self.menuBox.curselection()[0] 
					if(selectIndex!=-1):
						app.menu[selectIndex][1]()
						self.showingMenu = 0
						self.cv.delete(self.menuwindow)
				else:
					self.showMenu()
			if(mykey == 'w'): 
				if(self.showingMenu==1):
					self.showingMenu = 0 
					self.cv.delete(self.menuwindow )
				if(app.exit_key_handler):app.exit_key_handler() 
			if(key!=-1):
				args = {}
				args["keycode"] = 0x30 + key  
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'up'):
				args = {}
				args["keycode"] = 63497 #2
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'down'):
				args = {}
				args["keycode"] = 63498 #8
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'left'):
				args = {}
				args["keycode"] = 63495 #4
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'right'):
				args = {}
				args["keycode"] = 63496 #6
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			if(mykey == 'space'):
				args = {}
				args["keycode"] = 63557 #5
				args["scancode"] = 1
				args["type"] = 1
				if(self.event_callback):self.event_callback(args) 
			#print("键盘：%s" % evt.keysym)
		#打印鼠标操作
		if evt.type == "4":
			pass
			#print("鼠标： %s" % evt.num)
		#
		#print(evt.type)
    
    def set(self,text):
        self.textbox.insert("insert", text)
        while 1:
           self.root.update()

class Application(object):
	
    def __init__(self, **keys):
		self.exit_key_handler = None
		self.body=None
    def layout(self,d):
        return  [(240,320)]
    def Yield(self):
        #while 1:
        if(self.body):self.body.update()
        #time.sleep(0.1)
        
app = Application()
def abort():
	app.body.root.destroy()
	os._exit(0)
os.abort = abort
def note(text, type = 'info'):
    if type == "error":
        tkMessageBox.showerror(type.title(),text)
    else:
        tkMessageBox.showinfo(type.title(),text) 
def query(text, type = 'info'):
    return ''
import e32
e32=e32
