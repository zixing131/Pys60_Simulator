# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import appuifw
import graphics
TOP = 16
BOTTOM = 32
LEFT = 4
RIGHT = 8
HCENTER = 1
VCENTER = 2
PI_1_2 = 1.5707963267949
PI = 3.14159265358979
PI_3_2 = 4.71238898038469
PI_2_1 = 6.28318530717961
functions = ['drawImage', 'drawRect', 'FillRect', 'drawRoundRect', 'FillRoundRect', 'drawString']
def drawImage(self, img, x = 0, y = 0, anchor = (LEFT | TOP)):
    if anchor == (LEFT | TOP) : 
        self.blit(img, target = (x, y))
    elif anchor == (LEFT | HCENTER) : 
        self.blit(img, target = (x, (y - (img.size[1] / 2))))
    elif anchor == (LEFT | BOTTOM) : 
        self.blit(img, target = (x, (y - img.size[1])))
    elif anchor == (HCENTER | TOP) : 
        self.blit(img, target = ((x - (img.size[0] / 2)), y))
    elif anchor == (HCENTER | VCENTER) : 
        self.blit(img, target = ((x - (img.size[0] / 2)), (y - (img.size[1] / 2))))
    elif anchor == (HCENTER | BOTTOM) : 
        self.blit(img, target = ((x - (img.size[0] / 2)), (y - img.size[1])))
    elif anchor == (RIGHT | TOP) : 
        self.blit(img, target = ((x - img.size[0]), y))
    elif anchor == (RIGHT | VCENTER) : 
        self.blit(img, target = ((x - img.size[0]), (y - (img.size[1] / 2))))
    elif anchor == (RIGHT | BOTTOM) : 
        self.blit(img, target = ((x - img.size[0]), (y - img.size[1])))




def drawRect(self, left, top, w, h, col = 0, wid = 1):
    self.rectangle((left, top, left + w, top + h), fill=col, width = wid)




def FillRect(self, left, top, w, h, col = 0):
    self.rectangle((left, top, left + w, top + h), col, col)




def drawRoundRect(self, left, top, w, h, xr, yr, col = 0, wid = 1):
    if xr > (w / 2) : 
        xr = (w / 2)
    if yr > (h / 2) : 
        yr = (h / 2)
    self.line((left + xr, top, (left + w - xr), top), col, width = wid)
    self.line((left + xr, (top + h - 1), (left + w - xr), (top + h - 1)), col, width = wid)
    self.line((left, top + yr, left, (top + h - yr)), col, width = wid)
    self.line(((left + w - 1), top + yr, (left + w - 1), (top + h - yr)), col, width = wid)
    self.arc((left, top, left + (2 * xr), top + (2 * yr)), PI_1_2, PI, col, width = wid)
    self.arc(((left + w - (2 * xr)), top, left + w, top + (2 * yr)), 0, PI_1_2, col, width = wid)
    self.arc((left, (top + h - (2 * yr)), left + (2 * xr), top + h), PI, PI_3_2, col, width = wid)
    self.arc(((left + w - (2 * xr)), (top + h - (2 * yr)), left + w, top + h), PI_3_2, PI_2_1, col, width = wid)




def FillRoundRect(self, left, top, w, h, xr, yr, col = 0):
    if xr > (w / 2) : 
        xr = (w / 2)
    if yr > (h / 2) : 
        yr = (h / 2)
    self.rectangle((left + xr, top + yr, (left + w - xr), (top + h - yr)), col, col)
    self.rectangle((left + xr, top, (left + w - xr), top + yr), col, col)
    self.rectangle((left + xr, (top + h - yr), (left + w - xr), top + h), col, col)
    self.rectangle((left, top + yr, left + xr, (top + h - yr)), col, col)
    self.rectangle(((left + w - xr), top + yr, left + w, (top + h - yr)), col, col)
    self.pieslice((left, top, left + (2 * xr), top + (2 * yr)), PI_1_2, PI, col, col)
    self.pieslice(((left + w - (2 * xr)), top, left + w, top + (2 * yr)), 0, PI_1_2, col, col)
    self.pieslice((left, (top + h - (2 * yr)), left + (2 * xr), top + h), PI, PI_3_2, col, col)
    self.pieslice(((left + w - (2 * xr)), (top + h - (2 * yr)), left + w, top + h), PI_3_2, PI_2_1, col, col)




def drawString(self, font, col, x, y, str, anchor = (LEFT | TOP)):
    tup = self.measure_text(str, font)[0]
    if anchor == (LEFT | TOP) : 
        self.text((x, (y + tup[3] - tup[1])), str, col, font)
    elif anchor == (LEFT | VCENTER) : 
        self.text((x, y + ((tup[3] - tup[1]) / 2)), str, col, font)
    elif anchor == (LEFT | BOTTOM) : 
        self.text((x, y), str, col, font)
    elif anchor == (HCENTER | TOP) : 
        self.text(((x - ((tup[2] - tup[0]) / 2)), (y + tup[3] - tup[1])), str, col, font)
    elif anchor == (HCENTER | VCENTER) : 
        self.text(((x - ((tup[2] - tup[0]) / 2)), y + ((tup[3] - tup[1]) / 2)), str, col, font)
    elif anchor == (HCENTER | BOTTOM) : 
        self.text(((x - ((tup[2] - tup[0]) / 2)), y), str, col, font)
    elif anchor == (RIGHT | TOP) : 
        self.text(((x - (tup[2] - tup[0])), (y + tup[3] - tup[1])), str, col, font)
    elif anchor == (RIGHT | VCENTER) : 
        self.text(((x - (tup[2] - tup[0])), y + ((tup[3] - tup[1]) / 2)), str, col, font)
    elif anchor == (RIGHT | BOTTOM) : 
        self.text(((x - (tup[2] - tup[0])), y), str, col, font)


for i in functions:
    setattr(graphics.Image, i, eval(i))
