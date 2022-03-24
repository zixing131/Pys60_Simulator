# -*- coding: utf-8 -*-
import os
from time import sleep 
import threading
import shutil
from threading import Timer
from threading import Condition

from appuifw import app as _app 
_UpdateEvent, _EVT_UPDATE = None,None
s60_version_info = (3, 0)
class Ao_lock:
    def __init__(self):
		#self.condition = threading.Condition()
		self.iswait = 0
    def wait(self): 
		self.iswait = 1
		while self.iswait:
			_app.Yield()
			sleep(0.2)
		#self.condition.acquire()
		#self.condition.wait(5)
		#self.condition.release()
    def signal(self):  
		self.iswait = 0
		#self.condition.acquire()
		#self.condition.notify()
		#self.condition.release()
class Ao_timer:
    def __init__(self):
        self.iscancel = 0
        self.timer = None
    def cancel(self):
        ao_yield()
        if(self.timer):
            self.timer.cancel()
    def after(self,delay,func):
        self.timer = Timer(delay,func,())
        self.timer.start()
        ao_yield()
    
def ao_yield():
    _app.Yield()

def drive_list():
    print(os.getcwd())
    return ['c:','d:','e:','z:',os.getcwd()]

def ao_sleep(interval, cb=None): 
    ao_yield()
    sleep(interval)
pys60_version_info=(1,4,5,0,0)
def in_emulator():
    return True
def file_copy(old,new):
    shutil.copy(old, new)