# -*- coding: utf-8 -*-
import datetime,random

def imei():
	return '1'*15
def display_pixels():
	return (240,320)
def battery():
	now = datetime.datetime.now()
	return int(now.minute   * 100 / 60)#random.randint(0,100)
