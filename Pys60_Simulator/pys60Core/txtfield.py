# -*- coding: utf-8 -*-
try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk 
from appuifw import app as _app 
ECorner1 = 1
ECorner2 = 2
EReadOnly=1
EDisableCursor=1
EDisplayOnly=1
class New():
    def __init__(self,pos,cornertype=0,txtlimit=0,strlimit=0,editorflag=0):
        self.pos = pos
        height =  self.pos[3] - self.pos[1]
        width = self.pos[2] - self.pos[0]
        cv = _app.body and _app.body.cv or None
        self.textbox = tk.Text(cv,width=width,height=height)
        self.textwindow = None
    def textstyle(self,a,b,c,style):
        pass
    def bgcolor(self,color):
        pass
    def add(self,content):
        self.textbox.insert(tk.INSERT,content)
    def select(self,start,end):
        pass
    def focus(self,data):
        if(data==1):
            self.textbox.focus()
        else:
            pass
            #self.textbox.focus_set()
    def visible(self,data):
        #self.textbox.pack(padx=self.pos[0],pady=self.pos[1])
        height =  self.pos[3] - self.pos[1]
        width = self.pos[2] - self.pos[0]
        x=self.pos[0] + width/2
        y=self.pos[1] + height/2
        cv = _app.body and _app.body.cv or None
        if(cv!=None):
           if(data==1):
               try:
                   self.textwindow = _app.body.cv.create_window((x,y),window=self.textbox,height = height, width =width)
               except:
                   cv = _app.body and _app.body.cv or None
                   self.textbox = tk.Text(cv, width=width, height=height)
                   self.textwindow = _app.body.cv.create_window((x, y), window=self.textbox, height=height, width=width)
           elif(data==0):
               if(self.textwindow!=None):
                   _app.body.cv.delete(self.textwindow)
    def get(self,fullget=1):
        ret = self.textbox.get('0.0',tk.END)
        if(fullget==0):ret = ret[0:len(ret)-2]
        cv = _app.body and _app.body.cv or None
        return ret

