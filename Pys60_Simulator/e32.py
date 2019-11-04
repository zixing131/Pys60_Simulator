# -*- coding: utf-8 -*- 
from time import sleep 
import threading

from threading import Timer
from threading import Condition

from appuifw import app as _app 
_UpdateEvent, _EVT_UPDATE = None,None

class Ao_lock:
    def __init__(self):
		#self.condition = threading.Condition()
		self.iswait = 0
    def wait(self): 
		self.iswait = 1
		while self.iswait:
			_app.Yield()
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
        ao_yield()
        self.timer = Timer(0, func,())
        self.timer.start()
        ao_yield()
    
def ao_yield():
    _app.Yield()

def drive_list():
    return [""]

def ao_sleep(interval, cb=None): 
    ao_yield()
    sleep(interval)

def in_emulator():
    return True
