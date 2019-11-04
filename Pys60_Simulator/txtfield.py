# -*- coding: utf-8 -*-
try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk 
from appuifw import app as _app 
ECorner1 = 1

class New():
	def __init__(self,pos,cornertype,txtlimit):
		self.pos = pos
		height =  self.pos[3] - self.pos[1]
		width = self.pos[2] - self.pos[0] 
		self.textbox = tk.Text(_app.body.cv,width=width,height=height)
		
	def textstyle(self,a,b,c,style):
		pass
	def bgcolor(self,color):
		pass
	def add(self,content):
		self.textbox.insert(tk.INSERT,content)
	def select(self,start,end):
		pass
	def focus(self,data):
		pass
	def visible(self,data):  
		#self.textbox.pack(padx=self.pos[0],pady=self.pos[1])
		height =  self.pos[3] - self.pos[1]
		width = self.pos[2] - self.pos[0] 
		x=self.pos[0] + width/2
		y=self.pos[1] + height/2
		self.textwindow = _app.body.cv.create_window((x,y),window=self.textbox,height = height, width =width)
	def get(self):
		ret = self.textbox.get('0.0',tk.END)
		ret = ret[0:len(ret)-2]
		_app.body.cv.delete(self.textwindow)
		return ret
		
	
