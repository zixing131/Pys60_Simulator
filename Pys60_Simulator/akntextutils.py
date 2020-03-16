# -*- coding: utf-8 -*-
import tkFont
def wrap_text_to_array(content,dense,width):
	font = None
	size = 15
	font = tkFont.Font(family=dense, size=size)
	w = font.measure(content)
	if(w<width):
		return [content]
	result=[]
	t = ''
	for i in content:
		if(i=='\n'):
			result.append(t)
			t='' 
			continue
		t=t+i
		w = font.measure(t) 
		if(w>=width):
			result.append(t)
			t='' 
	if(t != ''):
		result.append(t) 
	return result
