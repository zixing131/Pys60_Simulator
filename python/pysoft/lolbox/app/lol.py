# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


__doc__ = '\n英雄联盟控 for s60v3\nBy:白色(Bysir)\nQQ:101964529\n尊重作者、请勿更改\n'

import math
import sys
import os
mypath = os.getcwd()
index = mypath.rfind('\\')
mypath=mypath[:index]
mypath4 =  mypath+"\\Pys60_Simulator\\"
mypath5 = mypath+"\\python\\pysoft\\lolbox\\app\\"
mypath6 = mypath+"\\python\\pysoft\\lolbox\\"

index = mypath.rfind('\\')
mypath=mypath[:index]
index = mypath.rfind('\\')
mypath=mypath[:index]
index = mypath.rfind('\\')
mypath=mypath[:index]

mypath3 = mypath + "\\Pys60_Simulator\\"

mypath2 = mypath+"\\python\\pysoft\\lolbox\\"
mypath = mypath+"\\python\\pysoft\\lolbox\\app\\"
#print(mypath3)
if(__name__ =='__main__'):
    sys.path.append(mypath)
    sys.path.append(mypath3)
else:
    sys.path.append(mypath4)
    sys.path.append(mypath5)
    mypath = mypath5
    mypath2 = mypath6

cn = lambda x, : x.decode('utf-8') 
en = lambda x, : x.encode('utf-8')
import e32
import appuifw as appuifw
import sysinfo
import akntextutils
pm_size = sysinfo.display_pixels()
other_size =  not (pm_size[0] in [240, 320])
from graphics import Image as Image
def pass_():
    pass



from Data import *
from lol_event import *
if __name__ == '__main__' : 
    ua = appuifw.app.body
try :
    execfile(mypath + 'set.ini')
except :
    pass
try :
    str(skin)
except :
    skin = 1
try :
    str(move_mobile)
except :
    move_mobile = 0
try :
    str(width)
except :
    width = 400
try :
    str(volume)
except :
    volume = 4
try :
    str(start_m)
except :
    start_m = 1
try :
    cn(sign)
except :
    sign = '❤'
try :
    str(qu)
except :
    qu = 0
try :
    str(acp)
except :
    acp = -1
try :
    str(loading_m)
except :
    loading_m = 1
try :
    str(cd_bg)
except :
    cd_bg = 2
try :
    str(cd_t)
except :
    cd_t = 1
try :
    str(cd_t_find_pos)
except :
    cd_t_find_pos = 0
try :
    str(cd_t_act)
except :
    cd_t_act = 1
try :
    if orientation == 2 : 
        orientation = pm_size[0] == 320
        orientation_, width_ = (2, width)
    else : 
        orientation_, width_ = (orientation, width)
except : 
    orientation = pm_size[0] == 320 and 1 or 0
    orientation_, width_ = (orientation, width)
width += (140 * orientation)
if  not (orientation) : 
    if pm_size[1] < 320 : 
        pm_size = (240, 320)
    pass
elif pm_size[0] < 320 : 
    pm_size = (320, 240)
execfile(mypath + 'skin.ini')
exec skin_list[skin]
try :
    appuifw.app.orientation = ['portrait', 'landscape'][orientation]
except :
    pass


def new(x, l = 0):
    if l : 
        return Image.new(x, 'L')
    else : 
        return Image.new(x)




def rim(a, b = None, c = None, d = None, e = 1):
    try :
        a, b, c, d = a
    except :
        pass
    c -= 1
    d -= 1
    if e == 1 : 
        return (a, (b + 1), (a + 1), (b + 1), (a + 1), b, (c - 1), b, (c - 1), (b + 1), c, (b + 1), c, (d - 1), (c - 1), (d - 1), (c - 1), d, (a + 1), d, (a + 1), (d - 1), a, (d - 1))
    elif e == 2 : 
        return (a, (b + 5), (a + 2), (b + 2), (a + 5), b, (c - 5), b, (c - 2), (b + 2), c, (b + 5), c, (d - 5), (c - 2), (d - 2), (c - 5), d, (a + 5), d, (a + 2), (d - 2), a, (d - 5))




def zz(n, y = 0):
    if n == 3 : 
        x = 3
        y10 = 40
    elif n == 1 : 
        x = 1
        y10 = 55
    elif n == 4 : 
        x = 4
        y10 = 64
    elif n == 2 : 
        x = 2
        y10 = 50
    elif n == 7 : 
        y10 = 40
        x = 3
    elif n == 11 : 
        x = 2
        y10 = 55
    if y : 
        y10 = y
    if n == 7 : 
        y11 = 55
    else : 
        y11 = y10
    color = 0
    img29 = new((y10, y11), 'L')
    if n == 4 : 
        color = (255, 255, 255)
        img29.clear(0)
        img29.polygon((30, 3, 2, 18, 2, 47, 30, 61, 60, 47, 60, 18), color, width = 1, fill = color)
        return img29.resize((40, 40))
    if n != 11 : 
        img29.clear((255, 255, 255))
        img29.polygon((0, 0, x, 0, 0, x), color, width = 1, fill = color)
        img29.polygon((((y10 - x) - 1), 0, (y10 - 1), 0, (y10 - 1), x), color, width = 1, fill = color)
    else : 
        img29.clear(0)
        img29.polygon(rim(2, 2, (y10 - 3), (y10 - 3)), (255, 255, 255), width = 2, fill = (255, 255, 255))
    if n != 7 : 
        img29.polygon((0, ((y10 - x) - 1), 0, (y10 - 1), x, (y10 - 1)), color, width = 1, fill = color)
        img29.polygon(((y10 - 1), ((y10 - x) - 1), (y10 - 1), (y10 - 1), ((y10 - x) - 1), (y10 - 1)), color, width = 1, fill = color)
    if n == 1 or n == 11 : 
        return img29
    img29.point((0, (x + 1)), color, width = 1)
    img29.point(((x + 1), 0), color, width = 1)
    img29.point(((y10 - 1), (x + 1)), color, width = 1)
    img29.point((((y10 - x) - 2), 0), color, width = 1)
    if n != 7 : 
        img29.point((0, ((y10 - x) - 2)), color, width = 1)
        img29.point(((x + 1), (y10 - 1)), color, width = 1)
        img29.point((((y10 - x) - 2), (y10 - 1)), color, width = 1)
        img29.point(((y10 - 1), ((y10 - x) - 2)), color, width = 1)
    return img29


img = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
img2 = new((50, 50))
try :
    img3 = Image.open(mypath + 'start.jpeg')
except :
    img3 = new((200, 200))
import random
k = 0
l = []
l2 = []
lh = range(16)
lh2 = range(16)
for j in xrange(16):
    i = random.choice(lh)
    lh.remove(i)
    l.append(i)
    i2 = random.choice(lh2)
    lh2.remove(i2)
    l2.append(i2)
img2_mask = zz(2)
try :
    img_2 = Image.open((mypath + 'bj_%s_%s.png' % (path_bj, orientation)))
    img_z = new(((240 + (80 * orientation)), (img_2.size[1] * 20)))
    for i in xrange((2 - orientation)):
        img_z.blit(img_2, (0, (( - (261 + (15 * orientation))) * i)))
    img.blit(img_z)
except :
    pass
if orientation : 
    img.text((70, 19), cn('英雄联盟控 for s60v3'), f_color, font = ('title', 17))
    img.text((8, 50), cn('v' + version), f_color, font = ('title', 15))
    img.text((6, 70), cn('正式版'), f_color, font = ('title', 15))
    img.text((6, 225), cn('By:Bysir'), f_color, font = ('title', 15))
    img.text((280, 225), cn('…'), f_color, font = ('title', 15))
else : 
    img.text((20, (30 - (10 * orientation))), cn('英雄联盟控 for s60v3'), f_color, font = ('title', (20 - (3 * orientation))))
    img.text((70, 60), cn(('v%s 正式版' % version)), f_color, font = ('title', 15))
    img.text((160, 311), cn('By:Bysir'), f_color, font = ('title', 16))
    img.text((20, 311), cn('正在召唤…'), f_color, font = ('title', 19))


appuifw.app.body = m = appuifw.Canvas()
appuifw.app.screen = 'full'
e32.ao_sleep(0)
m.blit(img)
def start():
    #print('start')
    global k
    n = l[k]
    n2 = l2[k]
    img2.blit(img3, ((50 * (n / 4)), (50 * (n % 4))))
    if start_m == 0 : 
        x3 = (20 + (50 * (n2 / 4))) + (40 * orientation)
        y3 = ((82 + (50 * (n2 % 4))) - (52 * orientation))
        img.blit(img2, ( - x3,  - y3), mask = img2_mask)
    elif start_m == 1 or start_m == 2 : 
        if start_m == 2 : 
            n2 = k
        xu = math.pi
        ou = (((xu / 8) * n2) - (xu / 2))
        x3 = (95 + (40 * orientation)) + (85 * math.cos(ou))
        y3 = (152 - (47 * orientation)) + (85 * math.sin(ou))
        img.blit(img2, ( - x3,  - y3), mask = img2_mask)
        img.blit(img2, ((-95 - (40 * orientation)), (-152 + (47 * orientation))), mask = img2_mask)
    elif start_m == 3 : 
        if n2 < 8 : 
            x3 = (25 + (40 * orientation))
            y3 = (82 - (52 * orientation)) + (20 * n2)
        else : 
            x3 = (25 + (40 * orientation)) + (20 * (n2 - 8))
            y3 = ((82 + 150) - (52 * orientation))
        img.blit(img2, ( - x3,  - y3), mask = img2_mask)
        if  not (k) : 
            img.text(((120 + (40 * orientation)), (165 - (50 * orientation))), cn('控'), f_color, font = ('title', 80))
            img.text(((122 + (40 * orientation)), (167 - (52 * orientation))), cn('控'), color_likebg, font = ('title', 80))
        pass
    k += 1
    m.blit(img)


try :
    for i in xrange((2 - orientation), (25 - (5 * orientation))):
        img_z.blit(img_2, (0, (( - (261 + (15 * orientation))) * i)))
    img_2 = None
except :
    pass


start()
import re
import string
zm26 = string.ascii_uppercase + string.ascii_lowercase + ',:/().+=![] %*'
del string
start()
import txtfield
start()
import akntextutils
import os
start()
def jc():
    file_list = os.listdir(mypath2+'')
    cnlist = [i for i in file_list if i[-1] == 't' ]
    if len(cnlist) < 100 : 
        appuifw.app.exit_key_handler = pass_
        if  not (appuifw.query(cn('检测到您未正确解压zip文件\n是否由软件自动解压?'), 'query')) : 
            return None
        import zipfile
        import powlite_fm
        try :
            os.makedirs(mypath2+'txt\\')
        except :
            pass
        try :
            os.makedirs(mypath2+'lom\\')
        except :
            pass
        e32.ao_yield()
        zip_list = []
        appuifw.note(cn('请选择资料文件(.zip)'), 'info', 1)
        m.blit(img)
        path = powlite_fm.manager().AskUser('e:\\', ext = ['.zip'])
        if path and path not in zip_list : 
            zip_list.append(path)
        for i in zip_list:
            m.blit(img)
            zip = zipfile.ZipFile(i)
            a = 0
            na = txtfield.New(((120 - (200 / 2)), 143, (120 + (200 / 2)), (143 + 100)), cornertype = txtfield.ECorner2)
            na.textstyle(u'', 140, 16711680, style = u'normal')
            na.bgcolor(6579300)
            na.textstyle(u'', 120, 15132390, style = u'normal')
            na.visible(1)
            na.focus(0)
            e32.ao_yield()
            namelist = zip.namelist()
            l = len(namelist)
            if 'lolbox/app/lol.pyc' in namelist or 'lolbox/app/Data.pyc' in namelist : 
                lx = '更新包'
            elif '无极剑圣.jpeg' in namelist : 
                lx = '资料包'
            elif 'txt/60.输掉比赛的10个原因.txt' in namelist : 
                lx = '攻略包'
            elif 'lom/带妹子1.lom' in namelist : 
                lx = '漫画包'
            else : 
                zip.close()
                e32.ao_yield()
                na.visible(0)
                continue
            for k in zip.namelist():
                m.blit(img)
                j = ((a * 100) / l)
                na.clear()
                na.bgcolor(6579300)
                na.add(cn(('正在解压%s,请稍后…\n已完成 %d' % (lx, j)) + '%'))
                e32.ao_yield()
                if lx == '更新包' : 
                    path_c = 'e:/data/'
                else : 
                    path_c = 'e:/data/lolbox/'
                (open(path_c + k, 'w')).write(zip.read(k))
                a += 1
            zip.close()
            e32.ao_yield()
            na.visible(0)
        m.blit(img)
        appuifw.note(cn('解压成功'), 'conf', 1)



#print('box')

class box :
    __module__ = __name__
    exec skin_list[skin]
    
    def __init__(s):
        global img_z
        #print('init')
        start()
        s.zcd_pos_list_old = s.key_ok = s.key_14 = s.key_15 = s.key_17 = s.key_16 = s.whil = s.hel = s.zjx = s.na = s.diy = s.ne = s.bj = s.y = s.x = s.x_ = s.y_one = s.zb_pos = s.zb = s.jn_pos = s.ex = s.ua = s.zm = s.men = s.wp_pos = s.wp = s.men_2 = s.pos_zh = s.zh = s.jnxxx = s.tx = s.db = s.rune = s.fw = s.fwmn = s.fwmnz = s.y_mn = s.one = s.zbtj = s.tfn = s.tf_pos = s.tfzt = s.zj = s.h_zj = s.h_tf = s.popup_zt = s.zcd_pos = s.zy = s.h_zz = s.zzz = s.mh = s.uppage = s.downpage = s.yxbj_ = s.team = 0
        s.fz_txt = ''
        s.h_list = {cn('页首') : 0, cn('详细信息') : -1, cn('技能') : -1, cn('技巧') : -1, cn('推荐装备') : -1, cn('贴士') : -1}
        s.mh_tp = 1
        s.i = new(pm_size)
        s.i_ = new((pm_size[0], (pm_size[1] / 2)))
        s.tfmn_list = [0 for i in xrange(57)]
        s.new_list = None
        s.zj_dir = {}
        s.tfmnn = [0, 0, 0, 0]
        s.Diy_pos = 0
        start()
        s.img = img
        s.orientation = orientation
        s.sign = sign
        s.cd_bg = cd_bg
        s.tf_list = tf_list
        s.tfgl_list = tfgl_list
        s.weapons_list = weapons_list
        s.weapons = weapons
        s.timer = e32.Ao_timer()
        s.zc = 1
        s.run = 0
        s.pos = [1, 1]
        s.img_tf_all = None
        s.img_tf_all_ = None
        s.list_bj = None
        s.list_team = None
        start()
        jc()
        s.tf = 0
        try :
            execfile(mypath + 'runes_list.save')
            len(s.mnlist)
        except :
            s.mnlist = []
        try :
            execfile(mypath + 'favorite.save')
            len(s.fa_list)
        except :
            s.fa_list = []
        try :
            execfile(mypath + 'new.save')
            len(s.new_list)
            str(s.new_page)
        except :
            s.new_list = None
            s.new_page = 1
        try :
            execfile(mypath + 'name_list.save')
            if len(s.namelist) == 1 : 
                (0 / 0)
        except :
            s.namelist = []
        start()
        s.img_up = None
        s.txt_zb = None
        s.txt_fw = None
        s.txt_zh = None
        s.nlist = [cn(i) for i in weapons_list[0]]
        s.runelist = [cn(i) for i in runes_list[0]]
        s.img_zb = None
        import gzip
        s.gzip = gzip
        gzip = None
        start()
        s.img_t_all = None
        s.icon = Image.open(mypath + 'icon.jpeg')
        s.img_pos = Image.open(mypath + 'pos.jpeg')
        s.img_pos.polygon(s.rim(0, 0, (240 + (80 * orientation)), 45, 1), (75, 75, 75), width = 1)
        import socket
        s.socket = socket
        socket = None
        start()
        s.img_dbzt = new(((240 + (80 * orientation)), 25))
        s.img_jnxx = None
        s.img_zb_j = new((150, 74))
        s.img_zb_j_mask = new((150, 74), 'L')
        s.img_zb_j_mask.clear(0)
        s.img_zb_j_mask.polygon(s.rim(0, 0, 150, 74, 2), (255, 255, 255), width = 1, fill = (255, 255, 255))
        s.img_jn_2 = new((44, 48))
        s.img_zb_2 = new((40, 45))
        s.img_tf_pos = new((40, 55))
        start()
        s.img_runes_all = None
        s.img_pos_ = Image.open(mypath + 'pos_2.jpeg')
        s.img_pos_mask = new(s.img_pos_.size, 'L')
        s.img_pos_mask.load(mypath + 'pos_2_mask.jpeg')
        s.img_pos_mask_ = new(((240 + (80 * orientation)), (320 - (80 * orientation))), 'L')
        s.img_pos_mask_.clear(0)
        s.img_pos_mask_.polygon(s.rim(0, 0, (240 + (80 * orientation)), 45, 1), (255, 255, 255), fill = (255, 255, 255), width = 1)
        start()
        import StringIO
        s.StringIO = StringIO
        StringIO = None
        s.img_jd = None
        start()
        s.img_ztl = Image.open(mypath + 'ztl.jpeg')
        start()
        s.img_sx_2 = new((22, 22))
        s.img_name = new((80, 15))
        s.img_fw = new((40, 40))
        s.img_allzh = None
        s.img_jn = new((44, 44))
        s.img_rw = new((110, 200))
        s.img_rw_mask = new((110, 200), 'L')
        s.img_rw_mask.polygon((0, 197, 0, 199, 2, 199), 0, width = 1, fill = 0)
        s.img_rw_mask.point((0, 196), 0, width = 1, fill = 0)
        s.img_rw_mask.point((3, 199), 0, width = 1, fill = 0)
        s.img_t = new((55, 55))
        s.img_zbxx = new(((240 + (80 * orientation)), 1600))
        start()
        s.img_dbzt_mask = new(((240 + (80 * orientation)), 25), 'L')
        s.img_dbzt_mask.clear((185, 185, 185))
        s.img_zb_mask = zz(3)
        s.img_tf_pos_mask = zz(7)
        s.img_t_mask = zz(1)
        s.img_t_mask_1 = zz(11)
        s.img_fw_mask = zz(4)
        s.img_jn_mask = s.img_zb_mask.resize((44, 44))
        s.img_zb_mask_d = s.img_zb_mask.resize((55, 55))
        s.img_zb_x_mask = s.img_zb_mask.resize((21, 21))
        s.img_zb_d_mask = s.img_zb_mask.resize((45, 45))
        s.img_t_mask_x = s.img_t_mask.resize((30, 30))
        s.img_name_mask = new((80, 15), 'L')
        s.img_name_mask.clear((255, 255, 255))
        for i in xrange(35):
            c = (255 - (14 * i))
            if c < 0 : 
                c = 0
            s.img_name_mask.line(((20 - i), 0, (20 - i), 90), (c, c, c), width = 1)
            s.img_name_mask.line(((60 + i), 0, (60 + i), 90), (c, c, c), width = 1)
        #print(other_size)
        if other_size : 
            s.img_z = new((pm_size[0], 4800))
            s.img_z.clear(color_likebg) 
        else : 
            s.img_z = img_z
            try :
                s.img_z = img_z
            except : 
                #print('init test')
                s.error(8)
            pass
        start()
        s.m = appuifw.Canvas(redraw_callback = s.redraw, event_callback = s.event)
        s.m.blit(s.img)
        appuifw.app.body = s.m
        appuifw.app.exit_key_handler = s.rec
        appuifw.app.menu_key_handler = s.menu
        appuifw.app.body.bind(63586, s.r)

    def rim(s, a, b = None, c = None, d = None, e = 1):
        try :
            a, b, c, d = a
        except :
            pass
        c -= 1
        d -= 1
        if e == 1 : 
            return (a, (b + 1), (a + 1), (b + 1), (a + 1), b, (c - 1), b, (c - 1), (b + 1), c, (b + 1), c, (d - 1), (c - 1), (d - 1), (c - 1), d, (a + 1), d, (a + 1), (d - 1), a, (d - 1))
        elif e == 2 : 
            return (a, (b + 5), (a + 2), (b + 2), (a + 5), b, (c - 5), b, (c - 2), (b + 2), c, (b + 5), c, (d - 5), (c - 2), (d - 2), (c - 5), d, (a + 5), d, (a + 2), (d - 2), a, (d - 5))
        elif e == 3 : 
            return (a, (b + 7), (a + 2), (b + 2), (a + 7), b, (c - 7), b, (c - 2), (b + 2), c, (b + 7), c, (d - 7), (c - 2), (d - 2), (c - 7), d, (a + 7), d, (a + 2), (d - 2), a, (d - 7))




    def redraw(s, rect, k = 0):
        try :
            s.i.clear(color_likebg)
            s.i.blit(s.img, (s.x, s.y))
            if s.db or s.bj : 
                s.i.blit(s.img_dbzt, mask = s.img_dbzt_mask)
            elif s.uppage : 
                s.i.blit(s.img_up, (-40, 0), mask = s.img_up_mask)
            elif s.downpage : 
                s.i.blit(s.img_do, (-40, (-270 + (80 * orientation))), mask = s.img_do_mask)
            if k : 
                if loading_m == 0 : 
                    yn = (k * (2.4 + (0.8 * orientation)))
                    s.i_.blit(s.img_z)
                    s.i.blit(s.i_, (yn, 0))
                    s.i_.blit(s.img_z, (0, (160 - (40 * orientation))))
                    s.i.blit(s.i_, ( - yn, (-160 + (40 * orientation))))
                    s.i.blit(s.icon, (-96 + (40 * orientation) + yn, (-75 + (40 * orientation))))
                    s.i.text(((70 + (40 * orientation) - yn), (155 - (40 * orientation))), cn('英雄联盟控'), f_color, font = ('title', 20))
                    if s.run == 2 : 
                        text = cn('感谢使用')
                    else : 
                        text = cn('载入中…')
                    s.i.text((80 + (40 * orientation) + yn, (185 - (40 * orientation))), text, f_color, font = ('title', 20))
                elif loading_m == 1 : 
                    yn = (k * (1.6 - (0.4 * orientation)))
                    s.i_.blit(s.img_z)
                    s.i.blit(s.i_, (s.x, yn))
                    s.i_.blit(s.img_z, (0, (160 - (40 * orientation))))
                    s.i.blit(s.i_, (0, (-160 + (40 * orientation) - yn)))
                    s.i.blit(s.icon, ((-96 - (40 * orientation)), -75 + (40 * orientation) + yn + (k * 0.6)))
                    s.i.text(((70 + (40 * orientation)), (((155 - (40 * orientation)) - yn) - (k * 0.6))), cn('　　联'), f_color, font = ('title', 20))
                    s.i.text(((70 + (40 * orientation)), (((155 - (40 * orientation)) - yn) - (k * 0.3))), cn('　雄　盟'), f_color, font = ('title', 20))
                    s.i.text(((70 + (40 * orientation)), ((155 - (40 * orientation)) - yn)), cn('英　　　控'), f_color, font = ('title', 20))
                    if s.run == 2 : 
                        text = cn('感谢使用')
                        xn = 80
                    else : 
                        text = cn('载入中')
                        xn = 90
                    s.i.text((xn + (40 * orientation), (185 - (40 * orientation)) + yn), text, f_color, font = ('title', 20))
                pass
            s.m.blit(s.i)
            #print('no except')
        except Exception as e:
            #print(e)
            pass




    def event_():
        pass




    event = event
    def error(s, k = 0, e = ''):
        s.run = 1
        txt = ['出现未知错误,请重启软件', '未找到e:\data\lolbox\app\allt.jpeg文件,请重装软件', '未找到e:\data\lolbox\app\weapons.jpeg文件,请重装软件', '未找到e:\data\lolbox\app\weapons.ini文件,请重装软件', ('未找到关于英雄"%s"的头像图片,请建议作者' % e), ('未找到关于武器"%s"的图片,可能是错误名称,请到e:\data\lolbox\app\weapons.ini改正' % e), '未找到e:\data\lolbox\app\jd.jpeg文件,请重装软件', '未找到e:\data\lolbox\app\sx.jpeg文件,请重装软件', '未找到e:\data\lolbox\app\bj_1.jpeg文件,请重装软件', ('未找到关于"%s"的txt资料文件,请检查文件' % e), ('未找到关于"%s"的资料图片,请检查文件' % e), ('载入推荐装备出错,可能是武器"%s"引起的,请在此英雄的txt资料中更改,e:\data\lolbox\英雄名.txt' % e), ('没有在武器库找到关于"%s"的资料,可能是没有添加(在e:\data\lolbox\app\weapons.ini里添加),或者是武器名错误,请在此英雄的txt资料中更改' % e), '自动解压失败,请按官网(http://lolbox.4vx.cn)里的提示手动解压zip', '未找到e:\data\lolbox\app\summoner.ini文件,请重新安装软件', '未找到e:\data\lolbox\app\summoner.jpeg文件,请重新安装软件', '未找到e:\data\lolbox\app\gifts.jpeg文件,请重新安装软件', '未找到e:\data\lolbox\app\gifts.ini文件,请重新安装软件', '未找到e:\data\lolbox\app\gifts_.jpeg文件,请重新安装软件', '未找到e:\data\lolbox\app\runes.ini文件,请重新安装软件', '未找到e:\data\lolbox\app\runes.jpeg文件,请重新安装软件', '未找到e:\data\lolbox\app\tfgl.ini文件,请重新安装软件'][k] + '\n\n不能解决请联系作者\nQ:1019654929'
        na = txtfield.New(((120 - (200 / 2)), 60, (120 + (200 / 2)), (60 + 200)), cornertype = txtfield.ECorner2)
        na.textstyle(u'', 120, 16711680, style = u'normal')
        na.bgcolor(6579300)
        na.add(cn('程序发生以下错误:\n\n'))
        na.textstyle(u'', 120, 15132390, style = u'normal')
        na.add(cn(txt))
        e32.ao_yield()
        na.visible(1)
        na.focus(1)
        appuifw.app.exit_key_handler = None
        while 1 : 
            e32.ao_sleep(3)




    def zjn(s):
        while 1 : 
            e32.ao_sleep(0.02)
            s.img_jnxx_d.blit(s.img_jnxx, (0, s.va))
            if s.jn_s and  not ( not (0 < s.jn_pos < 6 and s.run) and s.men) : 
                s.img.blit(s.img_jnxx_d, (-2, ( - s.h_jn - 61)))
                s.redraw(())
            else : 
                return None
            if s.va > (s.jn_s * 20) : 
                s.va = -1
                e32.ao_sleep(3.5)
            elif s.va < 1 : 
                e32.ao_sleep(2.5)
            s.va += 1




    def zhc(s):
        if s.zb or s.zbtj or s.zy or  not (0 < s.zb_pos < 7) : 
            return None
        else : 
            pass
        s.run = 1
        na = s.wlist[(s.zb_pos - 1)]
        x7 = (((s.zb_pos - 1) * (40 + (15 * orientation))) + 20)
        y7 = (x7 - 75)
        if y7 < 0 : 
            y7 = 0
        elif y7 > ((90 * 80) * orientation) : 
            y7 = (90 + (80 * orientation))
        e32.ao_yield()
        na = s.get_name(en(na))
        try :
            txt4 = cn(s.txt_zb[na])
        except :
            s.run = 0
            return None
        money = txt4.split(cn('价格:'))[1].split('\n')[0]
        e32.ao_yield()
        ttt = txt4.split('\n')
        tt = [i.split('[')[1].split(']')[0] for i in ttt if i.count(cn('　')) == 1 ]
        s.img_zb_j.blit(s.img_z, (y7, (s.h_zb - 57)))
        s.img_zb_j.polygon(s.rim(0, 0, 150, 74, 2), color_frame, width = 1)
        s.img.blit(s.img_zb_j, ( - y7, ( - s.h_zb + 57)), mask = s.img_zb_j_mask)
        s.img.polygon(((x7 - 5), (s.h_zb + 16), (x7 + 5), (s.h_zb + 16), x7, (s.h_zb + 21)), color_frame, width = 1, fill = color_likebg)
        s.img.line(((x7 - 4), (s.h_zb + 16), (x7 + 5), (s.h_zb + 16)), color_likebg, width = 1)
        e32.ao_yield()
        for i in xrange(len(tt)):
            name = s.get_name(en(tt[i]))
            x_zb = weapons[name]
            s.img_t.blit(s.img_zb, (x_zb, 0))
            s.img.blit(s.img_t.resize((21, 21)), (((( - i * 21) - 2) - y7), ( - s.h_zb + 6)), mask = s.img_zb_x_mask)
            e32.ao_yield()
        s.img.text(((y7 + 2), (s.h_zb - 40)), cn(na), color_highlight_j, font = ('title', 14))
        s.img.text(((y7 + 2), (s.h_zb - 24)), (cn('价格:%s') % money), f_color, font = ('title', 14))
        s.img.text(((y7 + 2), (s.h_zb - 8)), cn('合成需要:'), f_color, font = ('title', 14))
        s.img.text(((y7 + 98), s.h_zb), cn('确定键'), f_color, font = ('title', 14))
        s.img.text(((y7 + 90), (s.h_zb + 15)), cn('查看详情'), f_color, font = ('title', 14))
        s.run = 0
        e32.ao_yield()
        s.redraw(())

    exec ''.join([i for i in 'zllzl=l1ll' if i != 'l' ])
    
    def zcd_t(s):
        #print('zcd_t init ')
        while  not ( not (s.zc and s.men) and cd_bg and cd_t and cd_t_act and s.tx) : 
            #print('zcd_t ing ')
            e32.ao_yield()
            l = range(len(people))
            if cd_t_find_pos and s.zcd_pos_list : 
                po = s.zcd_pos_list[0]
                if po == 0 : 
                    i = random.choice(s.p_list[0 : 2])
                elif po == 1 : 
                    i = random.choice(s.p_list[2 : 4])
                elif po == 6 : 
                    i = random.choice(s.p_list[4 : 6])
                else : 
                    i = random.choice(s.p_list)
                pass
            else : 
                i = random.choice(s.p_list)
            k = random.choice(l)
            s.img_t.blit(s.img_t_all, ((k * 55), 0))
            e32.ao_yield()
            if  not ( not (s.zc and s.men) and cd_bg and cd_t and s.run) : 
                c = 5
                while  not ( not (s.zc and s.men) and cd_bg and c <= 255 and s.run) and cd_t : 
                    e32.ao_sleep(0.03)
                    s.img_t_mask_1.polygon(s.rim(2, 2, 52, 52), (c, c, c), width = 2, fill = (c, c, c))
                    s.img_z_hc.blit(s.img_t, ( - i[0],  - i[1]), mask = s.img_t_mask_1)
                    c += 25
                    e32.ao_yield()
                    if  not ( not ( not (s.zc and s.men) and cd_bg and cd_t and s.run) and s.tx) : 
                        s.pos_zcd(1)
                    else : 
                        break
                s.whil = 0
            s.whil = 0
            e32.ao_sleep(2.5)




    def getxx(s, name):
        s.txt_path = (mypath2+'%s.txt' % cn(name))
        try :
            s.txt_one = s.ztxt(s.txt_path)
        except :
            s.error(9, en(name))
        txtlist = s.txt_one.split('[[')[1].split(']]')[0]
        s.wlist = txtlist.split('\n')[0].split(',')
        try :
            s.zhs = s.txt_one.split(cn('召唤师技能:'))[1].split(' ')[1].split('\n')[0].split(',')
        except :
            s.zhs = [cn('重生'), cn('重生')]
        try :
            s.jdsx = s.txt_one.split(cn('加点顺序:'))[1].split(' ')[1].split('\n')[0].split(',')
        except :
            s.jdsx = ['Q' for i in xrange(16)]




    def get_name(s, o):
        if o in weapons_add_people_rx : 
            o = weapons_add_people_rx[o]
        return o




    def get_pos(s):
        n = 0
        for i in s.pos_list:
            x_, y_, j = i[ : 3]
            xrang = range(x_, x_ + j)
            yrang = range(y_, y_ + j)
            if ((s.zcd_pos[0] + 20) in xrang and s.zcd_pos[1] + 30) in yrang : 
                return [n, ((x_ - 3), (y_ - 3), (x_ + j + 3), (y_ + j + 3))]
            n += 1




    def out(s, k, n = 0):
        s.run = 1
        s.one = 1
        e32.ao_yield()
        appuifw.app.exit_key_handler = s.reu
        if n : 
            s.img = new(s.img_hc.size)
            s.img.blit(s.img_hc)
            s.run = 0
            e32.ao_yield()
            return None
        s.h_list = {cn('页首') : 0, cn('详细信息') : -1, cn('技能') : -1, cn('技巧') : -1, cn('推荐装备') : -1, cn('贴士') : -1}
        s.y5 = s.y
        s.pos_img = 0
        s.wit(0)
        s.y_tf = -1
        e32.ao_sleep(0)
        if  not (s.img_jd) : 
            try :
                s.img_jd = Image.open(mypath + 'jd.jpeg')
            except :
                s.error(6)
            s.img_jd_2 = new((s.img_jd.size[0], (s.img_jd.size[1] / 4)))
            s.img_jd_mask = new(s.img_jd_2.size, 'L')
            try :
                s.img_sx = Image.open(mypath + 'sx.jpeg')
            except :
                s.error(7)
            pass
        if  not (s.img_jnxx) : 
            s.img_jnxx = new(((236 + (80 * s.orientation)), 1600))
            s.img_jnxx_d = new(((236 + (80 * s.orientation)), (232 - (80 * s.orientation))))
        if  not (s.txt_zb) : 
            import weapons_py
            s.txt_zb = weapons_py.txt_zb
        if  not (s.img_zb) : 
            try :
                s.img_zb = Image.open(mypath + 'weapons.jpeg')
            except :
                s.error(2)
            pass
        if  not (s.img_allzh) : 
            try :
                s.img_allzh = Image.open(mypath + 'summoner.jpeg')
            except :
                s.error(15)
            pass
        name = cn(s.name_list[k])
        s.txt_path = (mypath2+'%s.txt' % en(name))
        s.a = 0
        try :
            s.txt_one = s.ztxt(s.txt_path)
        except :
            s.error(9, en(name))
        s.txt_one = s.txt_one.split(cn('背景:'))[0]
        s.jnxx = s.txt_one.split('##')[1]
        txtlist = s.txt_one.split('[[')[1].split(']]')[0]
        s.wlist = txtlist.split('\n')[0].split(',')
        if txtlist.find(cn(':')) != -1 : 
            txtlist2 = txtlist.replace('\n\n', '\n')
            s.xxczlist = '\n'.join(txtlist2.split(cn('\n'))[1 : ])
            ll = 6
        else : 
            s.xxczlist = ''
            ll = 1
        txt1 = (s.txt_one.replace('##' + s.jnxx + '##', cn(('\n' * (14 - (4 * s.orientation)))))).replace('[[' + txtlist + ']]', cn(('\n' * ll)))
        try :
            s.jdsx = s.txt_one.split(cn('加点顺序:'))[1].split(' ')[1].split('\n')[0].split(',')
            txt1 = txt1.replace(','.join(s.jdsx), '\n\n\n\n')
        except :
            pass
        try :
            s.tfmn_listn = int(s.txt_one.split(cn('天赋加点:'))[1].split(' ')[1].split('\n')[0])
            s.tfmn_list = tfgl_list[s.tfmn_listn][ : ]
            i = ''
            for n in xrange(3):
                if n == 1 : 
                    a = 19
                    b = 19
                elif n == 2 : 
                    a = 38
                    b = 19
                else : 
                    a = 0
                    b = 19
                f = 0
                for l in s.tfmn_list[a : a + b]:
                    f += l
                i = i + str(f) + '/'
            i = i[ : -1]
            txt1 = txt1.replace(cn(' ' + str(s.tfmn_listn) + '\n'), cn(' ' + i + '\n'))
        except :
            pass
        try :
            s.zhs = s.txt_one.split(cn('召唤师技能:'))[1].split(' ')[1].split('\n')[0].split(',')
            txt1 = txt1.replace(','.join(s.zhs), '\n\n')
        except :
            pass
        txt = akntextutils.wrap_text_to_array(txt1, 'dese', width)
        txt9 = akntextutils.wrap_text_to_array(s.jnxx, 'dese', width)
        s.jnxx_list = []
        ysa = d = p = 0
        for i in xrange(len(txt9)):
            if txt9[i][2 : 4] == '):' : 
                q = i
                s.jnxx_list.append(txt9[p : q])
                p = q
        s.jnxx_list.append(txt9[q : ])
        s.img = new(((240 + (80 * s.orientation)), ((len(txt) * 20) + 500)))
        s.img.blit(s.img_z)
        try :
            s.img_one = Image.open((mypath2+'%s.jpeg' % name))
        except :
            s.error(10, en(name))
        s.img_rw.blit(s.img_one)
        s.img.blit(s.img_rw, ((-130 - (80 * s.orientation)), 0), mask = s.img_rw_mask)
        for s.img_len in xrange(20):
            if ((((0 in s.img_one.getpixel((((s.img_len * 110) + 1), 199))[0] or s.img_len) * 110) < 0 or s.img_len) * 110) > (s.img_one.size[0] - 1) : 
                break
        if s.pos_img != 0 : 
            t_z = '◄'
        else : 
            t_z = '　'
        if (s.pos_img + 1) != s.img_len : 
            t_y = '►'
        else : 
            t_y = '　'
        s.img.text(((162 + (80 * s.orientation)), 215), cn(t_z + ('%s/%s' % ((s.pos_img + 1), s.img_len)) + t_y), s.f_color, font = ('title', 14))
        for i in txt:
            e32.ao_yield()
            colo = s.f_color
            cx = 0
            fsize = 14
            if  not ((s.a % 7)) : 
                s.wit((s.a / (len(txt) / 100.0)))
            if i[-5 : -1] in s.h_list : 
                if i == cn('推荐装备:') : 
                    s.h_list[i[-5 : -1]] = ((s.a * 20) - 80)
                else : 
                    s.h_list[i[-5 : -1]] = ((s.a * 20) - 20)
                colo = (255, 255, 255)
                xm = 0
                for h in xrange(11):
                    xm += 6
                    s.img.polygon(s.rim(0, (((s.a * 20) - 10) - h), (240 + (80 * s.orientation)), ((s.a * 20) - 9) + h), (xm, xm, xm), width = 1)
                pass
            if i[0 : 4] == cn('使用技巧') or i[0 : 4] == cn('对抗技巧') or i.find(cn('color')) != -1 or i[0 : 4] == cn('加点顺序') or i[0 : 5] == cn('召唤师技能') : 
                colo = s.color_highlight
                i = i.split('color')[0]
            if s.a < 20 and i.find('-') != -1 : 
                if len(i) == 10 : 
                    fsize = 13
                elif len(i) > 10 : 
                    fsize = 12
                try :
                    c = int(i[(i.find('-') - 1)])
                    try :
                        c = int(i[(i.find('-') - 2) : i.find('-')])
                    except :
                        pass
                    i = ''
                    s.img_sx_2.blit(s.img_sx, (0, (d * 22)))
                    s.img.blit(s.img_sx_2.resize((16, 16)), (-1, (( - s.a * 20) + 18)))
                    s.img_jd_2.blit(s.img_jd, (0, (d * s.img_jd_2.size[1])))
                    s.img_jd_mask.clear(0)
                    s.img_jd_mask.polygon(s.rim(0, 0, (((6.5 + (1.5 * s.orientation))) * c), (s.img_jd_2.size[1] - 6), 1), 16777215, width = 1, fill = 16777215)
                    s.img.blit(s.img_jd_2, (-48, (( - s.a * 20) + 14)), mask = s.img_jd_mask)
                    s.img.text((19, ((s.a * 20) - 3)), cn(['攻击', '法术', '生命', '难度'][d]), s.f_color, font = ('title', 14))
                    s.img.text(((50 + (((6.5 + (1.5 * s.orientation))) * c)), ((s.a * 20) - 3)), cn(str(c)), s.f_color, font = ('title', 14))
                    d += 1
                except :
                    pass
                pass
            elif i == cn('推荐装备:') : 
                b = 0
                s.h_zb = ((s.a * 20) - 17)
                s.img.text((1, ((s.a * 20) - 3)), i, 16777215, ('normal', 14))
                i = ''
                for g in s.wlist:
                    try :
                        name = s.get_name(en(g))
                        x_zb = weapons[name]
                        s.img_t.blit(s.img_zb, (x_zb, 0))
                    except :
                        s.img_t.clear(0)
                    s.img.blit(s.img_t.resize((40, 40)), (( - b * (40 + (15 * s.orientation))), (( - s.a * 20) - 10)), mask = s.img_zb_mask)
                    b += 1
                try :
                    e = 0
                    xxlist = [cn('出门：'), cn('前期：'), cn('后期：'), cn('逆风：')]
                    for c in s.xxczlist.split('\n'):
                        b = 2
                        ct, cc = c.split(':')
                        cc = cc.split(',')
                        for g in cc:
                            try :
                                name = s.get_name(en(g.split('(')[0]))
                                x_zb = weapons[name]
                                s.img_t.blit(s.img_zb, (x_zb, 0))
                            except :
                                s.img_t.clear(0)
                            s.img.blit(s.img_t.resize((21, 21)), ((( - b * 23) + 4), ((( - s.a * 20) - 60) - (23 * e))), mask = s.img_zb_x_mask)
                            b += 1
                        s.img.text((1, ((s.a * 20) + 78) + (23 * e)), xxlist[e], s.f_color, font = ('title', 14))
                        if ct : 
                            for i5 in akntextutils.wrap_text_to_array(ct, 'dese', width):
                                s.img.text((1, ((s.a * 20) + 100) + (23 * e)), i5, s.f_color, font = ('title', 14))
                                s.a += 1
                            pass
                        e += 1
                except :
                    pass
                pass
            elif i == cn('加点顺序:') : 
                zn = 0
                for ti in s.jdsx:
                    s.img_jn.clear(0)
                    s.img_jn.blit(s.img_one, (jn[ti], 200))
                    s.img_jn.polygon(s.rim(26, 26, 44, 44), s.color_pos, width = 1, fill = s.color_pos)
                    s.img_jn.text((31, 43), ti, s.f_color_pos, ('normal', 16))
                    s.img.blit(s.img_jn.resize((32, 32)), ((( - (zn % 6) * 38) - 9), ((( - s.a * 20) - 5) - ((zn / 6) * 35))), mask = s.img_jn_mask.resize((32, 32)))
                    zn += 1
                pass
            elif i == cn('天赋加点:') : 
                s.y_tf = (s.a * 20)
                s.img.polygon(s.rim(58, (s.y_tf + 1), 160, (s.y_tf + 19)), s.color_pos, width = 1, fill = s.color_pos)
                s.img.text((60, (s.y_tf + 17)), cn('确定键进入模拟'), s.f_color_pos, ('normal', 14))
            elif i == cn('召唤师技能:') : 
                zn = 0
                if len(s.zhs) > 2 : 
                    s.img.line((120, ((20 * s.a) + 5), 120, ((20 * s.a) + 67)), s.color_line, width = 1)
                    s.img.text((103, ((20 * s.a) + 19)), cn('方 方'), s.f_color, font = ('title', 14))
                    s.img.text((103, ((20 * s.a) + 33)), cn('案 案'), s.f_color, font = ('title', 14))
                    s.img.text((103, ((20 * s.a) + 49)), cn('① ②'), s.f_color, font = ('title', 14))
                for ti in s.zhs:
                    s.img_jn.clear(0)
                    s.img_jn.blit(s.img_allzh, (allzhjn[en(ti)], 0))
                    s.img.blit(s.img_jn, (((( - zn * 45) - 9) - ((zn / 2) * 43)), (( - s.a * 20) - 5)), mask = s.img_jn_mask)
                    s.img.text((((( + zn) * 45) + 9) + ((zn / 2) * 43), ((s.a * 20) + 68)), ti, s.f_color, ('normal', 14))
                    zn += 1
                pass
            elif i == cn('技能:') : 
                s.h_jn = (s.a * 20)
                zn = -4
                for ti in ['b', 'q', 'w', 'e', 'r']:
                    s.img_jn.clear(0)
                    s.img_jn.blit(s.img_one, (jn[ti], 200))
                    s.img.blit(s.img_jn, (zn, ( - s.h_jn - 9)), mask = s.img_jn_mask)
                    zn -= 47 + (19 * s.orientation)
                s.img.text(((82 + (80 * s.orientation)), (s.h_jn - 3)), cn('确定键 全屏浏览单个技能'), (230, 230, 230), ('normal', 13))
                s.img.text(((32 + (40 * s.orientation)), ((s.h_jn + 125) - (42 * s.orientation))), cn('【选中技能　查看详情】'), s.f_color, ('normal', 16))
                s.img.text(((75 + (40 * s.orientation)), ((s.h_jn + 155) - (42 * s.orientation))), cn('英雄联盟控 for 塞班'), s.f_color, ('normal', 16))
                s.img.text(((167 + (40 * s.orientation)), ((s.h_jn + 185) - (42 * s.orientation))), cn('By:Bysir'), s.f_color, ('normal', 16))
                s.img.text(((125 + (40 * s.orientation)), ((s.h_jn + 215) - (42 * s.orientation))), cn('QQ:1019654929'), s.f_color, ('normal', 16))
                s.img.text(((145 + (40 * s.orientation)), ((s.h_jn + 245) - (42 * s.orientation))), cn('欢迎加盟～'), s.f_color, ('normal', 16))
            s.img.text((cx, ((s.a * 20) - 3)), i, colo, ('normal', fsize))
            s.a += 1
        try :
            del s.img_hc
        except :
            pass
        s.img_hc = new(s.img.size)
        s.img_hc.blit(s.img)
        s.zy = s.run = 0
        e32.ao_yield()
        s.redraw(())




    def zcd(s, k = 0, n = None):
        #print(k)
        #print('zcd init 2')
        if  not (s.zc) or s.men : 
            #print('zcd return1')
            
            return None
        if k : 
            if s.img.size[1] != s.img_z_hc.size[1] : 
                s.img = new(s.img_z_hc.size)
            s.img.blit(s.img_z_hc)
            #print('zcd return2')
            return None
        s.run = s.zc = 1
        if cd_bg == 0 : 
            s.listtxt = [['英雄资料', '查看英雄技能资料、出装推荐'], ['查看周免', '查看本周免费英雄'], ['物品资料', '查看所有物品价格、属性'], ['符文资料', '查看符文的价格、属性'], ['召唤师技能', '查看召唤师技能的资料'], ['天赋资料', '查看天赋技能的资料和模拟加点'], ['英雄漫画', '浏览英雄联盟人物漫画'], ['查看新闻', '连接英雄联盟官网查看新闻'], ['查看攻略', '查看英雄联盟攻略文本'], ['神级团队', '神级阵容，赢在起跑线'], ['战绩查询', '联网查看召唤师战斗力、胜负场']]
            s.img = new(((240 + (80 * s.orientation)), ((len(s.listtxt) * 45) + 65)))
            s.img.blit(s.img_z)
            n = 0
            s.list_n = ['英', '免', '物', '符', '技', '天', '漫', '新', '攻', '团', '战']
            for i in s.listtxt:
                s.img.text((38, (47 + (5 * s.orientation)) + (n * 45)), cn(i[0]), s.f_color, font = ('title', 16))
                s.img.text((38, (64 + (5 * s.orientation)) + (n * 45)), cn(i[1]), s.f_color_2, font = ('title', 14))
                s.img.polygon(s.rim(6, (34 + (5 * s.orientation)) + (n * 45), 35, (63 + (5 * s.orientation)) + (n * 45)), (70, 70, 70), width = 1, fill = (70, 70, 70))
                s.img.polygon(s.rim(5, (33 + (5 * s.orientation)) + (n * 45), 34, (62 + (5 * s.orientation)) + (n * 45)), (100, 100, 100), width = 1, fill = (110, 110, 110))
                s.img.text((10, (57 + (5 * s.orientation)) + (n * 45)), cn(s.list_n[n]), (230, 230, 230), font = ('title', 20))
                n += 1
            pass
        elif cd_bg : 
            s.y = 0
            s.img_t_mask_1.polygon(s.rim(2, 2, 52, 52), (255, 255, 255), width = 2, fill = (255, 255, 255))
            if cd_bg == 1 : 
                s.pos_list = [(7, 29, 110, 0, (0, -27)), (123, 29, 110, 0, (0, 27)), (7, 145, 52, 0, (0, 0)), (65, 145, 52, 0, (0, 0)), (123, 145, 52, 0, (0, 0)), (181, 145, 52, 0, (0, 0)), (7, 203, 110, 1, (27, 0)), (123, 203, 52, 0, (0, 0)), (181, 203, 52, 0, (0, 0)), (123, 261, 52, 0, (0, 0)), (181, 261, 52, 0, (0, 0))]
                s.cd_txtlist = [cn('英雄资料'), cn('查看周免'), cn('物品资料'), cn('天赋资料'), cn('符文资料'), cn('英雄漫画'), cn('战绩查询'), cn('召唤技能'), cn('查看新闻'), cn('查看攻略'), cn('神级阵容')]
            elif cd_bg == 2 : 
                s.pos_list = [(7, 29, 110, 0, (0, -27)), (123, 29, 52, 0, (0, 0)), (181, 29, 52, 0, (0, 0)), (123, 87, 52, 0, (0, 0)), (181, 87, 52, 0, (0, 0)), (7, 145, 52, 0, (0, 0)), (65, 145, 52, 0, (0, 0)), (123, 145, 110, 1, (-27, 0)), (7, 203, 110, 1, (27, 0)), (123, 261, 52, 0, (0, 0)), (181, 261, 52, 0, (0, 0))]
                s.cd_txtlist = [cn('英雄资料'), cn('物品资料'), cn('天赋资料'), cn('英雄漫画'), cn('符文资料'), cn('查看攻略'), cn('查看新闻'), cn('查看周免'), cn('战绩查询'), cn('召唤技能'), cn('神级阵容')]
            elif cd_bg == 3 : 
                s.pos_list = [(65, 87, 110, 0, (0, -27)), (7, 29, 52, 0, (0, 0)), (65, 29, 52, 0, (0, 0)), (123, 29, 52, 0, (0, 0)), (181, 29, 52, 0, (0, 0)), (7, 87, 52, 0, (0, 0)), (181, 87, 52, 0, (0, 0)), (7, 145, 52, 0, (0, 0)), (181, 145, 52, 0, (0, 0)), (7, 203, 110, 1, (27, 0)), (123, 203, 110, 1, (-27, 0))]
                s.cd_txtlist = [cn('英雄资料'), cn('召唤技能'), cn('查看攻略'), cn('查看新闻'), cn('神级阵容'), cn('天赋资料'), cn('物品资料'), cn('英雄漫画'), cn('符文资料'), cn('查看周免'), cn('战绩查询')]
            else : 
                s.pos_list = []
                s.cd_txtlist = []
            if orientation : 
                s.pos_list = [(y, x, j, j1, j2) for x, y, j, j1, j2 in s.pos_list]
            [s.cd_txtlist.append('') for i in xrange(15)]
            try :
                p, p = s.zcd_pos
            except :
                s.zcd_pos = [(s.pos_list[0][0] - 15), (s.pos_list[0][1] - 15)]
            s.p_list = []
            for i in s.pos_list:
                if i[2] != 110 : 
                    continue
                if  not (i[3]) : 
                    if i[4][1] < 0 : 
                        s.p_list.append((i[0], (i[1] + 55)))
                        s.p_list.append(((i[0] + 55), (i[1] + 55)))
                    else : 
                        s.p_list.append((i[0], i[1]))
                        s.p_list.append(((i[0] + 55), i[1]))
                    pass
                elif i[4][0] > 0 : 
                    s.p_list.append((i[0], i[1]))
                    s.p_list.append((i[0], (i[1] + 55)))
                else : 
                    s.p_list.append(((i[0] + 55), i[1]))
                    s.p_list.append(((i[0] + 55), (i[1] + 55)))
            x = 49
            y = 7
            for i in range(14):
                if orientation : 
                    s.pos_list.append((y, x, 12))
                else : 
                    s.pos_list.append((x, y, 12))
                x += 13
            s.img = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
            s.img.blit(s.img_z)
            if  not (s.img_t_all) : 
                try :
                    s.img_t_all = Image.open(mypath + 'allt.jpeg')
                except :
                    s.error(1)
                pass
            if orientation : 
                txt = 'lol'
            else : 
                txt = 'lol控'
            s.img.text(((7 - (3 * orientation)), 20), cn(txt), f_color, font = ('title', 14))
            s.img.text(((1007 - (1000 * orientation)), 35), cn('控'), f_color, font = ('title', 14))
            if n == 300 : 
                execfile(mypath + 'color.ini')
            elif n != 200 : 
                for i in range(11):
                    na = random.randint(12, (len(s.pos_color) - 1))
                    s.pos_color[i] = s.pos_color[na]
                if n != 100 and n != None : 
                    for i in range(11):
                        s.pos_color[i] = s.pos_color[n]
                    pass
                pass
            k = 0
            img_p_mask = new((110, 110), 'L')
            img_p = new((110, 110))
            for i in s.pos_list:
                x, y = i[ : 2]
                s.img.rectangle((x, y, x + i[2], y + i[2]), 0, width = 0, fill = s.pos_color[k])
                if i[2] > 100 : 
                    txt = ((x + 5) + i[4][0], (y + 39 + 29) + (i[4][1] * cd_t))
                    if i[3] : 
                        y2 = (31 + y)
                        for ii in s.cd_txtlist[k]:
                            s.img.text(((x + 43) + (i[4][0] * cd_t), y2), ii, f_color_cd, font = ('title', 25))
                            y2 += 25
                        pass
                    else : 
                        s.img.text(txt, s.cd_txtlist[k], f_color_cd, font = ('title', 25))
                    pass
                else : 
                    y2 = (29 + y - 5)
                    for ii in xrange(2):
                        s.img.text(((x + 6), y2), s.cd_txtlist[k][(ii * 2) : (((ii + 1)) * 2)], f_color_cd, font = ('title', 20))
                        y2 += 24
                    pass
                k += 1
            if  not (cd_t) : 
                p_list = []
            else : 
                p_list = s.p_list[ : ]
            l = range(len(people))
            for i in p_list:
                k = random.choice(l)
                l.remove(k)
                s.img_t.blit(s.img_t_all, ((k * 55), 0))
                s.img.blit(s.img_t, ( - i[0],  - i[1]), mask = s.img_t_mask_1)
            if n != 300 : 
                open(mypath + 'color.ini', 'w').write('s.pos_color=' + repr(s.pos_color))
            pass
        s.img_z_hc = new(s.img.size)
        s.img_z_hc.blit(s.img)
        s.run = 0
        #print('pos_zcd ing')
        s.pos_zcd()
        appuifw.app.exit_key_handler = s.exit
        #print('zcd inited')



    def zui(s, k = 0, o = 0, r = 0):
        e32.ao_yield()
        s.run = s.zy = 1
        if k : 
            s.img = new(s.img_zui.size)
            s.img.blit(s.img_zui)
            s.run = 0
            return None
        if s.zm : 
            appuifw.app.menu_key_handler = None
            s.zm = 0
        s.y5 = s.y
        if o == 100 : 
            try :
                f = open('e:\data\lolbox\app\周免.ini', 'r')
                data = f.read()
                f.close()
                data = data.split('\n')[-1]
                s.name_list = data.split(',')
            except :
                s.run = 0
                if  not (s.zm) : 
                    s.men_2 = 1
                appuifw.note(cn('加载失败\n请先去主页刷新周免'), 'error', 1)
                return None
            pass
        elif o == 200 : 
            if  not (len(s.fa_list)) : 
                s.run = 0
                s.men_2 = 1
                appuifw.note(cn('列表为空\n请先添加'), 'error', 1)
                return None
            s.name_list = s.fa_list[ : ]
        elif r == 0 : 
            s.name_list = allpeople[o][ : ]
        y9 = ((((len(s.name_list) / (3 + s.orientation)) + 2)) * 79)
        if y9 < (320 - (80 * s.orientation)) : 
            y9 = (320 - (80 * s.orientation))
        s.wit(0)
        s.img = new(((240 + (80 * s.orientation)), y9))
        s.img.blit(s.img_z)
        qv = 1
        y2 = 7
        x2 = 10
        s.h_yx = 1
        if  not (s.img_t_all) : 
            try :
                s.img_t_all = Image.open(mypath + 'allt.jpeg')
            except :
                s.error(1)
            pass
        for u in s.name_list:
            try :
                u = s.get_name(u)
                s.img_t.blit(s.img_t_all, (people[u], 0))
            except :
                s.img_t.clear(0)
            s.img.blit(s.img_t, ( - x2,  - y2), mask = s.img_t_mask)
            w = s.img.measure_text(cn(u), ('title', 13))
            t = ((w[0][2] - w[0][1]) / 2)
            s.img_name.blit(s.img_z, ((x2 - 13), (y2 + 56)))
            s.img_name.text(((47 - t), 15), cn(u), s.f_color, font = ('title', 13))
            s.img.blit(s.img_name, (( - x2 + 13), ( - y2 - 56)), mask = s.img_name_mask)
            x2 += 75
            qv += 1
            try :
                if  not ((qv % 7)) : 
                    s.wit((qv / (len(s.name_list) / 100.0)))
            except :
                pass
            if (qv % (3 + s.orientation)) == 1 : 
                x2 = 10
                y2 += 79
                s.h_yx += 1
        if  not ((len(s.name_list) % (3 + s.orientation))) : 
            s.h_yx -= 1
        s.img_zui = new(s.img.size)
        s.img_zui.clear(0)
        s.img_zui.blit(s.img)
        s.bjlb(1)
        if r == 0 : 
            s.pos = [1, 1]
            s.y = 0
        else : 
            s.men = s.men_2 = 0
            s.y = s.y5
            e32.ao_sleep(0)
            open(mypath + 'favorite.save', 'w').write('s.fa_list=' + repr(s.fa_list))
            s.bj = 0
        s.pos_yx()
        s.run = 0
        if s.bj : 
            appuifw.app.exit_key_handler = lambda  :  s.zui(r = 1) 
        else : 
            appuifw.app.exit_key_handler = s.rec




    def move_one(s, k = 0, o = 0):
        s.run = 1
        e32.ao_yield()
        s.jn_s = 0
        if s.yxbj_ : 
            for i in xrange(10):
                s.y += (k * 2)
                if s.y < 0 : 
                    s.y = 0
                    break
                elif s.y > (s.h_yxbj - 320) + (80 * orientation) : 
                    s.y = (s.h_yxbj - 320) + (80 * orientation)
                    if s.y < 0 : 
                        s.y = 0
                    break
                e32.ao_sleep(0)
                s.redraw(())
            s.redraw(())
            s.run = 0
            return None
        if s.zb : 
            if k not in [4, -4] : 
                s.run = 0
                return None
            for i in xrange(10):
                if k > 0 : 
                    s.y_one += (31 - (8 * orientation))
                else : 
                    s.y_one -= (31 - (8 * orientation))
                if s.y_one < 0 : 
                    s.y_one = 0
                elif s.y_one > (s.y_zbxx - 324) + (80 * orientation) : 
                    s.y_one = (s.y_zbxx - 324) + (80 * orientation)
                if s.y_one < 0 : 
                    s.y_one = 0
                s.img.blit(s.img_zbxx, (0,  - s.y + s.y_one))
                s.redraw(())
                e32.ao_sleep(0)
            s.run = 0
            s.redraw(())
            return None
        if s.jnxxx : 
            txt9 = s.jnxx_list[s.jn_pos]
            s.y_jnxx = (len(txt9) * 20)
            for i in xrange(10):
                if k > 0 : 
                    s.y_one += (31 - (8 * orientation))
                else : 
                    s.y_one -= (31 - (8 * orientation))
                if s.y_one < 0 : 
                    s.y_one = 0
                elif s.y_one > (s.y_jnxx - 324) + (80 * orientation) : 
                    s.y_one = (s.y_jnxx - 324) + (80 * orientation)
                    if s.y_one < 0 : 
                        s.y_one = 0
                    pass
                s.img.blit(s.img_jnxx, (-2, ( - s.y + s.y_one - 2)))
                s.img.polygon(s.rim(0, s.y, (240 + (80 * orientation) - 1), ((320 - (80 * orientation)) - 1) + s.y), color_frame, width = 2)
                s.redraw(())
                e32.ao_sleep(0)
            s.run = 0
            s.redraw(())
            return None
        if  not ( not (s.y) and k in [4, -4]) : 
            s.pos_img += (k / (16 - (4 * orientation)))
            if  not (-1 < s.pos_img < s.img_len) : 
                s.pos_img -= (k / (16 - (4 * orientation)))
            else : 
                s.img_rw.blit(s.img_one, ((110 * s.pos_img), 0))
                s.img_hc.blit(s.img_rw, ((-130 - (80 * orientation)), 0), mask = s.img_rw_mask)
                s.img_name.blit(s.img_z, ((160 + (80 * orientation)), 200))
                if s.pos_img != 0 : 
                    t_z = '◄'
                else : 
                    t_z = '　'
                if (s.pos_img + 1) != s.img_len : 
                    t_y = '►'
                else : 
                    t_y = '　'
                s.img_name.text((2, 15), cn(t_z + ('%s/%s' % ((s.pos_img + 1), s.img_len)) + t_y), f_color, font = ('title', 14))
                s.img_hc.blit(s.img_name, ((-160 - (80 * orientation)), -200))
                s.out(0, 1)
                s.redraw(())
                s.run = 0
                return None
            pass
        for i in xrange(10):
            if o : 
                s.y += (k * 20)
            elif i > 4 : 
                s.y += (k * 1)
            else : 
                s.y += (k * 3)
            if s.y < 0 : 
                s.y = 0
                break
            elif s.y > ((s.a * 20) - 320) + (80 * orientation) : 
                s.y = ((s.a * 20) - 320) + (80 * orientation)
                break
            if o : 
                break
            e32.ao_sleep(0)
            s.redraw(())
        s.redraw(())
        s.run = 0




    def move_yx(s, k, o = 1):
        s.run = 1
        if s.tx : 
            for i in xrange(10):
                s.y += ((8 - (2 * orientation)) * k)
                if s.y < 0 : 
                    s.y = 0
                elif s.y > (s.y_txt - 320) + (80 * orientation) : 
                    s.y = (s.y_txt - 320) + (80 * orientation)
                if s.y < 0 : 
                    s.y = 0
                s.redraw(())
                e32.ao_sleep(0)
            s.run = 0
            s.redraw(())
            return None
        e32.ao_yield()
        s.pos5 = s.pos[ : ]
        if k == 1 : 
            if s.pos[1] < s.h_yx : 
                s.pos[1] += 1
            elif o == 1 : 
                s.pos[1] = 1
                if len(s.name_list) > 15 : 
                    s.y = 79
                else : 
                    s.y = 0
                pass
            else : 
                s.run = 0
                return None
            pass
        elif k == -1 : 
            if s.pos[1] > 1 : 
                s.pos[1] -= 1
            elif o == 1 : 
                s.pos[1] = s.h_yx
                if len(s.name_list) > 15 : 
                    s.y = (79 * (s.h_yx - 5) + orientation)
                else : 
                    s.y = (79 * (s.h_yx + 1 - 5) + orientation)
                if s.y < 0 : 
                    s.y = 0
                pass
            else : 
                s.run = 0
                return None
            pass
        elif k == 4 : 
            if s.pos[0] < (3 + orientation) : 
                s.pos[0] += 1
            else : 
                s.pos[0] = 1
                s.pos[1] += 1
            if ((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] > len(s.name_list) : 
                s.pos = [1, 1]
                if len(s.name_list) > 15 : 
                    s.y = 79
                else : 
                    s.y = 0
                pass
            pass
        elif k == -4 : 
            if s.pos[0] > 1 : 
                s.pos[0] -= 1
            else : 
                s.pos[0] = (3 + orientation)
                s.pos[1] -= 1
            if (len(s.name_list) % (3 + orientation)) == 0 : 
                x3 = (3 + orientation)
            else : 
                x3 = (len(s.name_list) % (3 + orientation))
            if (((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1) < 0 : 
                s.pos = [x3, s.h_yx]
                if len(s.name_list) > 15 : 
                    s.y = (79 * (s.h_yx - 5) + orientation)
                else : 
                    s.y = (79 * (s.h_yx + 1 - 5) + orientation)
                if s.y < 0 : 
                    s.y = 0
                pass
            pass
        elif k == 100 : 
            s.run = 0
            return (((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)
        try :
            u = s.name_list[(((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)]
        except :
            s.pos[0] = (len(s.name_list) % (3 + orientation))
        s.run = 1
        s.pos_yx(o)




    def pos_Diy(s):
        s.Diy(1)
        s.redraw(())




    def pos_zcd(s, k = 0):
        e32.ao_yield()
        if  not (s.zc) or s.men :
            #print('pos_zcd return')
            return None
        #print('pos_zcd init')
        s.zcd(1)
        #print('pos_zcd ing1') 
        if cd_bg == 0 : 
            s.run = 1
            if s.zcd_pos > (len(s.listtxt) - 1) : 
                s.zcd_pos = 0
                s.y = 0
            elif s.zcd_pos < 0 : 
                s.zcd_pos = (len(s.listtxt) - 1)
                s.y = ((len(s.listtxt) * 45) - 270) + (90 * orientation)
            if (s.zcd_pos * 45) > ((s.y + 250) - (80 * orientation)) : 
                s.y += 45
            elif (s.zcd_pos * 45) < s.y : 
                s.y -= 45
            e32.ao_yield()
            if  not (s.zc) : 
                return None
            s.img.blit(s.img_ztl, (0,  - s.y))
            s.img.text((2, (19 + s.y)), cn('lol控 for 塞班'), (230, 230, 230), font = ('title', 14))
            s.img.text(((220 + (80 * orientation)), (19 + s.y)), cn(s.sign), s.color_like, font = ('title', 14))
            s.img.blit(s.img_ztl, (0, ((-295 + (80 * s.orientation)) - s.y)))
            s.img.text((10, (315 - (80 * s.orientation)) + s.y), cn('菜单'), (230, 230, 230), font = ('title', 14))
            s.img.text(((203 + (80 * s.orientation)), (315 - (80 * s.orientation)) + s.y), cn('退出'), (230, 230, 230), font = ('title', 14))
            s.img.text((((108 + (40 * s.orientation)) - (7 * (len(str((s.zcd_pos + 1))) - 1))), (315 - (80 * s.orientation)) + s.y), cn(('%d/%d' % ((s.zcd_pos + 1), len(s.listtxt)))), (230, 230, 230), font = ('title', 14))
            s.img.blit(s.img_pos, (0, ((-25 - (5 * s.orientation)) - (s.zcd_pos * 45))), mask = s.img_pos_mask_)
            for n in xrange(len(s.listtxt)):
                y12 = ((25 + (5 * s.orientation)) + (n * 45) - s.y)
                if (n and n - 1) != s.zcd_pos and s.zcd_pos != n and y12 < ((320 - (80 * orientation)) - 50) and y12 > 50 : 
                    s.img.line((0, (24 + (5 * s.orientation)) + (n * 45), 320, (24 + (5 * s.orientation)) + (n * 45)), color_line, width = 1)
            i = s.listtxt[s.zcd_pos]
            n = s.zcd_pos
            s.img.text((38, (47 + (5 * s.orientation)) + (n * 45)), cn(i[0]), (230, 230, 230), font = ('title', 16))
            s.img.text((38, (64 + (5 * s.orientation)) + (n * 45)), cn(i[1]), (200, 200, 200), font = ('title', 14))
            s.img.text((10, (57 + (5 * s.orientation)) + (n * 45)), cn(s.list_n[n]), (230, 230, 230), font = ('title', 20))
            if 1 : 
                x7 = (22 + (80 * s.orientation))
                y7 = -5
                s.img.polygon(s.rim((196 + x7), 24 + s.y + y7, (216 + x7), 44 + s.y + y7), (110, 110, 110), width = 1, fill = (110, 110, 110))
                s.img.text(((199 + x7), 41 + s.y + y7), cn(['感', '谢', '使', '用', '白', '色', '的', '软', '件', '•', '•'][s.zcd_pos]), (230, 230, 230), font = ('title', 14))
            s.run = 0
        elif cd_bg : 
            e32.ao_yield()
            if  not (s.zc) : 
                #print('pos_zcd return1') 
                return None
            s.zcd_pos_list = s.get_pos()
            if  not ( not (cd_t_act and cd_t and k) and s.whil) : 
                s.timer.cancel()
                e32.ao_sleep(0)
                try :
                    s.zcd_t()
                    #s.timer.after(2, s.zcd_t)
                except :
                    pass
                pass
            if s.zcd_pos_list != None : 
                e32.ao_yield()
                if  not (s.zc) : 
                    #print('pos_zcd return2') 
                    return None
                s.img.polygon(s.rim(s.zcd_pos_list[1]), s.pos_color[s.zcd_pos_list[0]], width = 3)
            e32.ao_yield()
            if  not (s.zc) : 
                #print('pos_zcd return3') 
                return None
            s.img.blit(s.img_pos_, ( - s.zcd_pos[0],  - s.zcd_pos[1]), mask = s.img_pos_mask)
        
        s.redraw(())




    def pos_popup(s, k = 0):
        if s.run : 
            return None
        s.run = 1
        s.popup_menu(0, 0, 1)
        if k == 1 : 
            appuifw.app.exit_key_handler = s.can_popup
            appuifw.app.menu_key_handler = s.menu
            s.men = 0
        elif k == 2 : 
            appuifw.app.exit_key_handler = s.rec
            appuifw.app.menu_key_handler = s.menu
            s.men = 0
        txtlist = s.popup_list[s.popup_pos]
        if txtlist.find('|') != -1 : 
            cccc, txtlist, p = txtlist.split('|')
            ms = 2
        else : 
            ms = 1
        y = (((s.popup_pos * 20) * ms) + 38)
        if s.y < (y - 300) + (20 * (ms - 1)) + (80 * orientation) : 
            s.y = ((y - 300) + (20 * (ms - 1)) + (80 * orientation) + 2)
        elif s.y > (y - 38) : 
            s.y = (y - 38)
        txtlist = akntextutils.wrap_text_to_array(txtlist, 'dese', width)
        s.img.polygon(s.rim(0, (y - 17), (240 + (80 * orientation)), (y - 17) + ((20 * len(txtlist)) * ms)), 0, width = 0, fill = color_pos)
        if ms == 2 : 
            name, sf = cccc.split(' ')
            na = s.get_name(en(name))
            try :
                s.img_t.blit(s.img_t_all, (people[na], 0))
            except :
                s.img_t.clear(0)
            s.img.blit(s.img_t.resize((34, 34)), (-3, ( - y + 14)), mask = s.img_t_mask.resize((34, 34)))
            if sf == cn('胜利') : 
                c = (99, 200, 16)
            else : 
                c = (210, 60, 60)
            s.img.text((47, y), sf, c, font = ('title', 14))
        for i in xrange(len(txtlist)):
            s.img.text(((7 + ((ms - 1) * 40)), y + (i * 20) + (20 * (ms - 1))), txtlist[i], f_color_pos, font = ('title', 14))
        s.run = 0
        s.redraw(())




    def pos_wp(s, n = 0, k = 0):
        s.run = 1
        if s.zb : 
            if n > 2 : 
                n = 1
            elif n < -2 : 
                n = 0
            else : 
                s.run = 0
                return None
            for i in xrange(10):
                if n : 
                    s.y_one += (31 - (8 * orientation))
                else : 
                    s.y_one -= (31 - (8 * orientation))
                if s.y_one < 0 : 
                    s.y_one = 0
                elif s.y_one > (s.y_zbxx - 324) + (80 * orientation) : 
                    s.y_one = (s.y_zbxx - 324) + (80 * orientation)
                if s.y_one < 0 : 
                    s.y_one = 0
                s.img.blit(s.img_zbxx, (0,  - s.y + s.y_one))
                s.redraw(())
                e32.ao_sleep(0)
            s.run = 0
            return None
        s.wp_pos += n
        if s.wp_pos < 0 : 
            if k : 
                s.wp_pos -= n
                s.run = 0
                return None
            s.wp_pos = (len(s.nlist) - 1)
            s.y = (((s.h_wp - 4) + orientation) * 79)
        elif s.wp_pos > (len(s.nlist) - 1) : 
            if n == 1 : 
                if k : 
                    s.wp_pos -= n
                    s.run = 0
                    return None
                s.wp_pos = 0
                s.y = 0
            elif (s.wp_pos / (3 + orientation)) > (s.h_wp - 1) : 
                if k : 
                    s.wp_pos -= n
                    s.run = 0
                    return None
                else : 
                    s.wp_pos = 0
                    s.y = 0
                pass
            else : 
                s.wp_pos = (len(s.nlist) - 1)
            pass
        x1 = (((s.wp_pos % (3 + orientation))) * 75)
        y1 = ((((s.wp_pos / (3 + orientation))) * 79) + 7)
        if s.y < 0 : 
            s.y = 0
        s.wpzl(1)
        s.run = 1
        s.img.blit(s.img_pos_, (( - x1 - 1), ( - y1 + 7)), mask = s.img_pos_mask)
        if y1 < s.y : 
            for i in xrange(10):
                if k : 
                    s.y -= 79
                    break
                if i > 4 : 
                    s.y -= 3
                else : 
                    s.y -= 12.8
                ba = (((s.y * (4 - orientation)) / eval(str(s.h_wp) + '.0')) + s.y + 1)
                bc = (((4.0 - orientation) / s.h_wp) * (310 - (80 * orientation)))
                if  not (other_size or orientation) : 
                    color2 = color_likebg
                else : 
                    color2 = color_likebg_2
                s.img.line(((232 + (80 * orientation)), 0, (232 + (80 * orientation)), (s.h_wp * 90)), color2, width = 5)
                s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
                s.redraw(())
                e32.ao_yield()
            pass
        elif y1 > ((s.y + 280) - (80 * orientation)) : 
            for i in xrange(10):
                if k : 
                    s.y += 79
                    break
                if i > 4 : 
                    s.y += 3
                else : 
                    s.y += 12.8
                ba = (((s.y * (4 - orientation)) / eval(str(s.h_wp) + '.0')) + s.y + 1)
                bc = (((4.0 - orientation) / s.h_wp) * (310 - (80 * orientation)))
                if  not (other_size or orientation) : 
                    color2 = color_likebg
                else : 
                    color2 = color_likebg_2
                s.img.line(((232 + (80 * orientation)), 0, (232 + (80 * orientation)), (s.h_wp * 90)), color2, width = 5)
                s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
                s.redraw(())
                e32.ao_yield()
            pass
        s.wpzl(1)
        s.img.blit(s.img_pos_, (( - x1 - 1), ( - y1 + 7)), mask = s.img_pos_mask)
        ba = (((s.y * (4 - orientation)) / eval(str(s.h_wp) + '.0')) + s.y + 1)
        bc = (((4.0 - orientation) / s.h_wp) * (310 - (80 * orientation)))
        s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
        s.redraw(())
        s.run = 0




    def pos_fw(s, n = 0, k = 0):
        if s.rune : 
            return None
        s.run = 1
        s.fw_pos += n
        if s.fw_pos < 0 : 
            if k and n in [-1, 1] : 
                s.fw_pos -= n
                s.run = 0
                return None
            if n in [-1, 1] : 
                s.fw_pos = (len(s.runelist) - 1)
                s.y = ((s.fw_pos - (6 - (2 * orientation))) * (45 + (3 * orientation)))
                if s.y < 0 : 
                    s.y = 0
                pass
            else : 
                s.fw_pos = 0
            pass
        elif s.fw_pos > (len(s.runelist) - 1) : 
            if k and n in [-1, 1] : 
                s.fw_pos -= n
                s.run = 0
                return None
            if n in [1, -1] : 
                s.fw_pos = 0
                s.y = (s.fw_pos * (45 + (3 * orientation)))
            else : 
                s.fw_pos = (len(s.runelist) - 1)
            pass
        s.fwzl(1)
        s.run = 1
        y10 = (s.fw_pos * (45 + (3 * orientation)))
        name = s.runelist[s.fw_pos]
        s.img.polygon(s.rim(3, (y10 + 2), (220 + (80 * orientation)), (y10 + 48)), color_pos, width = 1, fill = color_pos)
        name = s.runelist[s.fw_pos]
        s.img_fw.blit(s.img_runes_all, (rune[runes[en(name)]], 0))
        s.img.blit(s.img_fw, (-7, ( - y10 - 5)), mask = s.img_fw_mask)
        s.img.text((53, (y10 + 22)), name, f_color_pos, font = ('title', 14))
        money = (s.txt_fw.split('\n' + name + ':\n')[1]).split('\n')[0]
        if len(money) > 15 : 
            money = money[ : 14] + cn('…')
        s.img.text((53, (y10 + 42)), money, f_color_pos, font = ('title', 14))
        if y10 > ((s.y + 280) - (80 * orientation)) or y10 < (s.y - 20) : 
            for i in xrange(5):
                if k : 
                    s.y += (((45 + (3 * orientation))) * n)
                else : 
                    s.y += (((9 + (0.6 * orientation))) * n)
                if s.y < 0 : 
                    s.y = 0
                if s.y > ((len(s.runelist) - (7 - (2 * orientation))) * (45 + (3 * orientation))) : 
                    s.y = ((len(s.runelist) - (7 - (2 * orientation))) * (45 + (3 * orientation)))
                if k : 
                    break
                ba = (((s.y * (7.0 - (2 * orientation))) / eval(str(len(s.runelist)) + '.0')) + s.y + 1)
                bc = (((7.0 - (2 * orientation)) / len(s.runelist)) * (310 - (80 * orientation)))
                if  not (other_size or orientation) : 
                    color2 = color_likebg
                else : 
                    color2 = color_likebg_2
                s.img.line(((232 + (80 * orientation)), 0, (232 + 80), ((len(s.runelist) * 50) + 100)), color2, width = 5)
                s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
                s.redraw(())
                e32.ao_yield()
            pass
        s.fwzl(1)
        ba = (((s.y * (7.0 - (2 * orientation))) / eval(str(len(s.runelist)) + '.0')) + s.y + 1)
        bc = (((7.0 - (2 * orientation)) / len(s.runelist)) * (310 - (80 * orientation)))
        s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
        s.img.polygon(s.rim(3, (y10 + 2), (220 + (80 * orientation)), (y10 + 48)), color_pos, width = 1, fill = color_pos)
        s.img_fw.clear(0)
        s.img_fw.blit(s.img_runes_all, (rune[runes[en(name)]], 0))
        s.img.blit(s.img_fw, (-7, ( - y10 - 5)), mask = s.img_fw_mask)
        s.img.text((53, (y10 + 22)), name, f_color_pos, font = ('title', 14))
        s.img.text((53, (y10 + 42)), money, f_color_pos, font = ('title', 14))
        s.redraw(())
        s.run = 0




    def pos_zm(s, k = 0):
        if k == 100 : 
            import time
            s.run = 1
            s.zm = 1
            s.img_zm = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
            s.img_zm.clear(0)
            s.img_zm.blit(s.img_z)
            timen = time.localtime()
            ti = cn(str(timen[1]) + '月' + str(timen[2]) + '日')
            s.img_zm.text((0, 20), cn('【查看周免】 ') + ti, f_color, font = ('title', 14))
            s.img_zm.text((0, 40), cn('>>>联网中…'), f_color, font = ('title', 14))
            s.img.blit(s.img_zm, (0,  - s.y))
            s.redraw(())
            appuifw.app.exit_key_handler = pass_
            s.img_zm.blit(s.img_z)
            e32.ao_yield()
            a = 1
            try :
                if  not (s.zm_pos) : 
                    data = s.geturl(url_zm)
                    if data.find('免费英雄更换公告') != -1 : 
                        url_zm_list = {}
                        zm_time = []
                        for i in data.split('免费英雄更换公告')[ : -1]:
                            t = i.split('">')[-1]
                            y = int(t.split('月')[0])
                            r = int(t.split('月')[1].split('日')[0])
                            t = cn(('%s月%02d' % (y, r)))
                            zm_time.append(t)
                            url_zm_list[t] = i.split('<a href="')[-1].split('"')[0].replace('amp;', '')
                        zm_time.sort()
                        zm_time.reverse()
                        ti = zm_time[0]
                        url = 'http://lol.qq.com' + url_zm_list[ti]
                        data = s.geturl(url)
                    else : 
                        data = (0 / 0)
                    pass
                else : 
                    data = s.geturl(url_zm_1)
                    data = data.split('本周免费')[1]
                if  not (s.zm_pos) : 
                    s.zm_list = [h.split(' ')[0] for h in data.split('的免费英雄')[1].split('</p>')[0].split('<br />')[1 : ]]
                    if  not (s.zm_list) : 
                        s.zm_list = [h.split(' ')[0] for h in data.split('的免费英雄')[1].split('</p>')[0].split('<br/>')[1 : ]]
                    s.zm_list = [i.replace('　', '').split('&')[0] for i in s.zm_list]
                    for i in ['流浪法师', '德玛西亚之力', '寒冰射手']:
                        try :
                            s.zm_list.remove(i)
                        except :
                            pass
                    pass
                else : 
                    s.zm_list = re.findall('class="new_tips" title="(.{,22})"><', data)[ : 10]
                s.img_zm.text((0, 20), cn('【查看周免】 ') + ti, f_color, font = ('title', 14))
                s.img_zm.text((0, 40), cn('>>>本周免费英雄: '), f_color, font = ('title', 14))
                s.out_zm()
                f = open('e:\data\lolbox\app\周免.ini', 'w')
                f.write(en(ti) + '\n' + ','.join(s.zm_list))
                f.close()
            except :
                s.img_zm.text((0, 20), cn('【查看周免】 ') + ti, f_color, font = ('title', 14))
                s.img_zm.text((0, 40), cn('>>>获取失败、请稍后再试'), f_color, font = ('title', 14))
                s.img_zm.text((0, 60), cn('提示:请查看帮助按帮助设置软件'), f_color, font = ('title', 14))
            s.img_zm.text(((107 + (40 * orientation)), (315 - (80 * orientation))), cn('刷新'), f_color, font = ('title', 14))
            s.img_zm.text((10, (315 - (80 * orientation))), cn('详细'), f_color, font = ('title', 14))
            s.img_zm.text(((200 + (80 * orientation)), (315 - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
            s.img.blit(s.img_zm, (0,  - s.y))
            s.img_zm_hc = new(s.img.size)
            s.img_zm_hc.blit(s.img)
            s.redraw(())
            appuifw.app.menu_key_handler = lambda  :  s.zui(o = 100) 
            appuifw.app.exit_key_handler = s.rec
            s.run = 0
            s.zm_pos = 0
        else : 
            if k : 
                s.zm_pos =  not (s.zm_pos)
            x2 = (58 + (40 * orientation))
            y2 = (((s.zm_pos * 20) + s.y + 253) - (80 * orientation))
            s.gxzm(1)
            s.img.polygon(s.rim(x2, y2, (x2 + 124), (y2 + 20)), color_pos, width = 1, fill = color_pos)
            s.img.text(((x2 + 9), (y2 + 17)), s.td[s.zm_pos], f_color_pos, font = ('title', 14))
            s.redraw(())




    def pos_menu(s, k):
        s.run = 1
        if s.men_2 : 
            s.menu_pos_2 += k
            if 0 > s.menu_pos_2 : 
                s.menu_pos_2 = (len(s.menu_list) - 1)
            elif s.menu_pos_2 > (len(s.menu_list) - 1) : 
                s.menu_pos_2 = 0
            s.menu_2(1)
            yy = ((302 - (s.menu_len * 20)) - (80 * orientation)) + s.y + (s.menu_pos * 20)
            y2 = ((300 - (80 * orientation)) + s.y - (len(s.menu_list) * 20))
            if yy > y2 : 
                yy = y2
            s.img.polygon(s.rim(78, (yy + 5) + (s.menu_pos_2 * 20), 157, (yy + (s.menu_pos_2 * 20) + 25)), 0, width = 0, fill = color_pos)
            s.img.text((82, (yy + 22) + (s.menu_pos_2 * 20)), cn(str((s.menu_pos_2 + 1)) + '.') + s.menu_list[s.menu_pos_2], f_color_pos, font = ('title', 14))
            s.redraw(())
        else : 
            s.menu_pos += k
            if 0 > s.menu_pos : 
                s.menu_pos = (len(s.menu_list) - 1)
            elif s.menu_pos > (len(s.menu_list) - 1) : 
                s.menu_pos = 0
            s.menu(1)
            ymenu = ((305 - (80 * orientation)) + s.y - (len(s.menu_list) * 20)) + (s.menu_pos * 20)
            if  not (s.zc and cd_bg) : 
                ymenu -= 20
            s.img.polygon(s.rim(10, ymenu, 89, (ymenu + 20)), 0, width = 0, fill = color_pos)
            s.img.text((14, (17 + ymenu)), cn(str((s.menu_pos + 1)) + '.') + s.menu_list[s.menu_pos], f_color_pos, font = ('title', 14))
            s.redraw(())
        s.run = 0




    def pos_yx(s, k = 1):
        s.zui(1)
        s.run = 1
        e32.ao_yield()
        x1, y1 = s.pos
        x1 = ((x1 - 1) * 75)
        y1 = (((y1 - 1) * 79) + 7)
        e32.ao_yield()
        s.img.blit(s.img_pos_, (( - x1 - 1), ( - y1 + 7)), mask = s.img_pos_mask)
        if y1 < s.y : 
            for i in xrange(10):
                if k != 1 : 
                    s.y -= 79
                    break
                if i > 4 : 
                    s.y -= 3
                else : 
                    s.y -= 12.8
                ba = (((s.y * (4 - orientation)) / eval(str(s.h_yx) + '.0')) + s.y + 1)
                bc = (((4.0 - orientation) / s.h_yx) * (310 - (80 * orientation)))
                if  not (other_size or orientation) : 
                    color2 = color_likebg
                else : 
                    color2 = color_likebg_2
                s.img.line(((232 + (80 * orientation)), 0, (232 + (80 * orientation)), (s.h_yx * 90)), color2, width = 5)
                s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
                s.redraw(())
                e32.ao_yield()
            pass
        elif y1 > ((s.y + 280) - (80 * orientation)) : 
            for i in xrange(10):
                if k != 1 : 
                    s.y += 79
                    break
                if i > 4 : 
                    s.y += 3
                else : 
                    s.y += 12.8
                ba = (((s.y * (4 - orientation)) / eval(str(s.h_yx) + '.0')) + s.y + 1)
                bc = (((4.0 - orientation) / s.h_yx) * (310 - (80 * orientation)))
                if  not (other_size or orientation) : 
                    color2 = color_likebg
                else : 
                    color2 = color_likebg_2
                s.img.line(((232 + (80 * orientation)), 0, (232 + (80 * orientation)), (s.h_yx * 90)), color2, width = 5)
                s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
                s.redraw(())
                e32.ao_yield()
            pass
        s.zui(1)
        s.img.blit(s.img_pos_, (( - x1 - 1), ( - y1 + 7)), mask = s.img_pos_mask)
        ba = (((s.y * (4 - orientation)) / eval(str(s.h_yx) + '.0')) + s.y + 1)
        bc = (((4.0 - orientation) / s.h_yx) * (310 - (80 * orientation)))
        s.img.line(((232 + (80 * orientation)), ba, (232 + (80 * orientation)), bc + ba), color_progress, width = 4)
        s.redraw(())
        s.run = 0




    def pos_zb(s, k = 0):
        if k == 1 : 
            return  not ( not ((((s.y + 60) < s.h_zb and s.y + 250) - (80 * orientation)) > s.h_zb and s.zb) and s.yxbj_)
        elif  not (s.zb) : 
            s.jn_pos = 0
            s.run = 1
            s.timer.cancel()
            e32.ao_yield()
            s.out(0, 1)
            s.run = 1
            e32.ao_yield()
            if s.zb_pos != 0 and s.zb_pos != 7 : 
                na = s.wlist[(s.zb_pos - 1)]
                name = s.get_name(en(na))
                try :
                    x_zb = weapons[name]
                    s.img_t.blit(s.img_zb, (x_zb, 0))
                except :
                    s.img_t.clear(0)
                s.img_zb_2.blit(s.img_z, ((((40 + (15 * orientation))) * (s.zb_pos - 1)), (s.h_zb + 24)))
                s.img_zb_2.blit(s.img_t.resize((40, 40)), mask = s.img_zb_mask)
                s.img.blit(s.img_zb_2, ((( - (40 + (15 * orientation))) * (s.zb_pos - 1)), ( - s.h_zb - 24)))
            s.redraw(())
            s.run = 0
            s.timer.after(0.4, s.zhc)




    def pos_tf(s, k = 0):
        if k == 1 : 
            return (((s.y + 20) < s.y_tf and s.y + 300) - (80 * orientation)) > s.y_tf
        if s.one : 
            appuifw.app.exit_key_handler = lambda  :  s.reo(1) 
        elif s.tfzt != 3 : 
            appuifw.app.exit_key_handler = s.rec
            s.tfzt = 1
        else : 
            appuifw.app.exit_key_handler = s.ret
        x3, y3 = tf_list[s.tfn][s.tf_pos]
        wb = (80 * y3 > 3 and orientation)
        if s.y < wb : 
            z = -8
        else : 
            z = 8
        if s.y != wb : 
            for i in xrange(10):
                s.y -= z
                s.redraw(())
            pass
        x1 = ((x3 * 47) - 17) + (40 * orientation)
        y1 = ((y3 * 47) - 12)
        s.tfzl(k = 1)
        s.img_tf_pos.blit(s.img_z, (x1, (y1 - 14)))
        if s.tfn == 1 : 
            a = 19
        elif s.tfn == 2 : 
            a = 38
        else : 
            a = 0
        a += s.tf_pos
        if  not (s.tfzt == 3 and s.tfmn_list[a]) : 
            s.img_fw.blit(s.img_tf_all_, ((a * 40), 0))
        else : 
            s.img_fw.blit(s.img_tf_all, ((a * 40), 0))
        name = s.tf[a]['name']
        s.img_tf_pos.text((8, 54), cn(name)[ : 2], f_color, font = ('title', 13))
        if s.tfzt == 1 : 
            s.img_fw.polygon(s.rim(0, 27, 13, 40), color_pos, width = 1, fill = color_pos)
            s.img_tf_pos.blit(s.img_fw, mask = s.img_zb_mask)
            s.img_tf_pos.text((3, 40), cn(str(len(s.tf[a]['level']))), f_color_pos, font = ('title', 13))
        elif s.pd(a) : 
            s.img_fw.polygon(s.rim(0, 27, 25, 40), color_pos, width = 1, fill = color_pos)
            s.img_tf_pos.blit(s.img_fw, mask = s.img_zb_mask)
            s.img_tf_pos.text((3, 40), cn(('%s/%s' % (s.tfmn_list[a], len(s.tf[a]['level'])))), f_color_pos, font = ('title', 13))
        else : 
            s.img_tf_pos.blit(s.img_fw, mask = s.img_zb_mask)
        s.img.blit(s.img_tf_pos, ( - x1, ( - y1 + 14)), mask = s.img_tf_pos_mask)
        s.redraw(())




    def pos_jn(s, k = 0):
        if k : 
            return  not ( not ( not ((((s.y - 20) < s.h_jn and s.y + 220) - (80 * orientation)) > s.h_jn and s.zb) and s.jnxxx) and s.yxbj_)
        elif  not (s.zb) : 
            s.y_one = s.men = s.men_2 = s.zbtj = 0
            s.jnxxx = 0
            s.zb_pos = 0
            s.jn_s = 0
            e32.ao_sleep(0)
            s.va = 0
            s.timer.cancel()
            s.run = 1
            s.out(0, 1)
            s.run = 1
            e32.ao_yield()
            if s.jn_pos != 0 and s.jn_pos != 6 : 
                s.img_jn.blit(s.img_one, (jn[['b', 'q', 'w', 'e', 'r'][(s.jn_pos - 1)]], 200))
                s.img_jn_2.blit(s.img_z, ((((((47 + (19 * orientation))) * s.jn_pos) - 43) - (19 * orientation)), (s.h_jn + 5)))
                s.img_jn_2.blit(s.img_jn, mask = s.img_jn_mask)
                s.img.blit(s.img_jn_2, (((( - (47 + (19 * orientation))) * s.jn_pos) + 43) + (19 * orientation), ( - s.h_jn - 5)))
                zm = s.y
                for i in xrange(10):
                    if  not (((zm - s.h_jn) + 20)) : 
                        break
                    s.y -= (((zm - s.h_jn) + 20) / 10)
                    s.redraw(())
                    e32.ao_sleep(0)
                txt9 = s.jnxx_list[s.jn_pos]
                v = len(txt9)
                if v > (12 - (5 * orientation)) : 
                    s.jn_s = (v - 12) + (5 * orientation)
                else : 
                    s.jn_s = 0
                if color_jnbg : 
                    s.img_jnxx.clear(color_jnbg)
                else : 
                    s.img_jnxx.blit(s.img_z, (1, (s.h_jn + 60)))
                cj = color_highlight_j
                for i in xrange(v):
                    txt_n = 0
                    t = txt9[i]
                    if en(t[ : 4]) in ['使用心得', '冷却时间', '施法消耗', '施法距离'] : 
                        col = color_highlight
                        txt_n = 5
                    elif t[2 : 4] == '):' : 
                        t = t.split('):')[1]
                    else : 
                        col = f_color
                    x = 1
                    if cj != f_color : 
                        s.img_jnxx.text((1, (20 + (i * 20))), t, cj, ('normal', 14))
                    else : 
                        for ii in t:
                            if ii in '.0123456789' : 
                                bs = 2
                                col = color_highlight_n
                                txt_n = 1
                            elif ii in zm26 : 
                                bs = 2
                                col = f_color
                            else : 
                                bs = 1
                            if txt_n > 0 : 
                                s.img_jnxx.text((x, (20 + (i * 20))), ii, col, ('normal', 14))
                            else : 
                                s.img_jnxx.text((x, (20 + (i * 20))), ii, f_color, ('normal', 14))
                            x += (14 / bs)
                            txt_n -= 1
                        pass
                    cj = f_color
                s.img_jnxx_d.blit(s.img_jnxx)
                s.img.blit(s.img_jnxx_d, (-2, ( - s.h_jn - 61)))
                x7 = (((((47 + (19 * orientation))) * s.jn_pos) - 22) - (18 * orientation))
                s.img.polygon(s.rim(0, (s.h_jn + 59), (239 + (80 * orientation)), ((s.h_jn + 294) - (80 * orientation))), color_frame, width = 2)
                s.img.polygon(((x7 - 5), (s.h_jn + 59), (x7 + 5), (s.h_jn + 59), x7, (s.h_jn + 54)), color_frame, width = 2)
                s.img.line(((x7 - 2), (s.h_jn + 59), (x7 + 2), (s.h_jn + 59)), color_likebg, width = 2)
                if s.jn_s : 
                    try :
                        s.timer.after(1.5, s.zjn)
                    except :
                        pass
                    pass
                pass
            s.redraw(())
            s.run = 0




    def open_txt(s, k = 0):
        if s.run : 
            return None
        s.zc = 0
        s.run = 1
        e32.ao_sleep(0)
        appuifw.app.exit_key_handler = pass_
        try :
            list = os.listdir(mypath2+'txt\\')
            (0 / len(list))
            s.tx = s.zy = 1
        except :
            s.run = 0
            appuifw.note(cn('未在e:\data\lolbox\txt\下找到文本,请到官网下载'), 'error', 1)
            return s.rec()
        if  not (k) : 
            s.y6 = s.y
        list2 = [cn(i.split('.txt')[0]) for i in list]
        pop = s.popup_menu(list2, cn('【查看攻略】'), o = k)
        if pop == None : 
            s.run = 0
            return s.rec()
        s.run = 1
        s.popup_pos_2 = s.popup_pos
        s.wit(0)
        e32.ao_sleep(0)
        txt = s.ztxt(mypath2+'txt\\' + list[pop])
        txtlist = akntextutils.wrap_text_to_array(txt, 'dese', width)
        s.y_txt = ((len(txtlist) * 20) + 20)
        if s.y_txt < (320 - (80 * orientation)) : 
            s.y_txt = (320 - (80 * orientation))
        s.img = new(((240 + (80 * orientation)), s.y_txt))
        for i in range(4):
            if (i * s.img_z.size[1]) < s.img.size[1] : 
                s.img.blit(s.img_z, (0, ( - i * s.img_z.size[1])))
            else : 
                break
        a = 1
        for i in txtlist:
            s.img.text((0, ((a * 20) - 2)), i, f_color, font = ('title', 14))
            a += 1
            if  not ((a % 10)) : 
                s.wit((a / (len(txtlist) / 100.0)))
        appuifw.app.exit_key_handler = lambda  :  s.open_txt(1) 
        s.redraw(())
        s.run = 0




    def open_uc(s, k = 0, o = 0):
        f = open('c://ucurl.txt', 'w')
        if k == 1 : 
            f.write(s.urlj)
        elif k == 0 : 
            f.write('lolbox.4vx.cn')
            if  not (o) : 
                s.rec()
            pass
        elif k == 2 : 
            f.write('https://m.alipay.com/personal/payment.htm')
            if  not (o) : 
                s.rec()
            pass
        elif k == 3 : 
            f.write(url_mh)
        f.close()
        try :
            e32.start_exe('UcWeb60Signed.exe', '')
        except :
            pass
        if k == 3 : 
            s.yxmh(1)




    def open_jn(s):
        s.run = 1
        s.jnxxx = 1
        s.zb_pos = s.one = 0
        s.jn_s = 0
        e32.ao_sleep(0)
        s.va = 0
        s.timer.cancel()
        appuifw.app.exit_key_handler = s.pos_jn
        s.img.blit(s.img_jnxx, (-2, ( - s.y - 2)))
        s.img.polygon(s.rim(0, s.y, (240 + (80 * orientation) - 1), ((320 - (80 * orientation)) - 1) + s.y), color_frame, width = 2)
        s.redraw(())
        s.run = 0




    def open_zb(s, k = 0):
        s.zb = 1
        s.run = 1
        s.one = 0
        if  not (s.txt_zb) : 
            import weapons_py
            s.txt_zb = weapons_py.txt_zb
        if k : 
            na = s.nlist[s.wp_pos]
            appuifw.app.exit_key_handler = s.rew
        else : 
            appuifw.app.exit_key_handler = s.rey
            na = s.wlist[(s.zb_pos - 1)]
        na = s.get_name(en(na))
        try :
            txt4 = cn(s.txt_zb[na])
        except :
            s.error(12, en(na))
        try :
            sj = ('%d' % (int(txt4.split(cn('价格:'))[1].split('\n')[0].split(' ')[0]) / 1.428))
        except :
            sj = '0'
        txt4 = txt4.replace(txt4.split('\n')[0], txt4.split('\n')[0] + cn('\n售价:') + sj)
        s.img_zbxx.blit(s.img_z)
        x_zb = weapons[na]
        s.img_t.blit(s.img_zb, (x_zb, 0))
        s.img_zbxx.blit(s.img_t.resize((45, 45)), (0, 0), mask = s.img_zb_d_mask)
        txt5 = akntextutils.wrap_text_to_array(txt4, 'dese', width)
        s.img_zbxx.text((53, 17), cn(na), color_highlight_j, font = ('title', 15))
        fs = 13
        fj = 14
        x5 = 18
        x6 = 53
        t = 0
        s.y_zbxx = x5 + fj
        for o in txt5:
            if o in [cn('合成:'), cn('被动：'), cn('主动：'), cn('唯一被动：'), cn('唯一主动：'), cn('补充:'), cn('光环：'), cn('唯一光环：')] : 
                color = color_highlight
            else : 
                color = f_color
            if o.find('[') != -1 : 
                x6 = 26
                na = o.split('[')[1].split(']')[0]
                s.y_zbxx += 6
                name = s.get_name(en(na))
                x_zb = weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                g = o.count(cn('　'))
                if g : 
                    jq = cn(s.txt_zb[name]).split(':')[1].split(' ')[0].split('\n')[0]
                    o = o + '[' + jq + ']'
                s.img_zbxx.blit(s.img_t.resize((21, 21)), (((-15 * g) - 3), ( - s.y_zbxx + 18)), mask = s.img_zb_x_mask)
            elif t > 1 : 
                fs = 14
                fj = 17
                x6 = 5
            if t == 2 : 
                s.y_zbxx += 4
            x = 1
            for ii in o:
                if ii in '.0123456789' : 
                    bs = 2
                    col = color_highlight_n
                elif ii in zm26 : 
                    bs = 2
                    col = color
                else : 
                    bs = 1
                    col = color
                s.img_zbxx.text((x6 + x, s.y_zbxx), ii, col, font = ('title', fs))
                x += (fs / bs)
            t += 1
            s.y_zbxx += fj
        s.img.blit(s.img_zbxx, (0,  - s.y))
        s.run = 0
        s.redraw(())




    def open_tf(s):
        if s.tfzt == 3 : 
            appuifw.app.exit_key_handler = s.retfmn
        else : 
            appuifw.app.exit_key_handler = s.pos_tf
        s.tfzt = 2
        s.img.blit(s.img_z)
        if s.tfn == 1 : 
            a = 19
        elif s.tfn == 2 : 
            a = 38
        else : 
            a = 0
        a += s.tf_pos
        s.img_fw.blit(s.img_tf_all, ((a * 40), 0))
        s.img.blit(s.img_fw.resize((45, 45)), (0,  - s.y), mask = s.img_zb_d_mask)
        txt = s.tf[a]
        name = txt['name']
        le = txt['level']
        pos2 = ((tf_list[s.tfn][s.tf_pos][1] - 1) * 4)
        if pos2 : 
            s.img.text((53, (32 + s.y)), cn(('需要在%s系上分配%s点' % (['攻击', '防御', '通用'][s.tfn], pos2))), f_color, font = ('title', 13))
        try :
            ne = txt['need']
            a -= s.tf_pos
            i = ne.keys()[0]
            nneed = ne[i]
            a = a + int(i)
            name2 = s.tf[a]['name']
            s.img.text((53, (46 + s.y)), cn(("需要在'%s'上分配%s点" % (name2, nneed))), f_color, font = ('title', 13))
        except :
            pass
        s.img.text((53, (17 + s.y)), cn(name), f_color, font = ('title', 15))
        n = n1 = 0
        for i in le:
            t = ('lv%s ' % (n1 + 1)) + i
            lee = akntextutils.wrap_text_to_array(cn(t), 'dese', width)
            for i in lee:
                s.img.text((1, (65 + (n * 18)) + s.y), i, f_color, font = ('title', 14))
                n += 1
            n1 += 1
        s.img.text(((200 + (80 * orientation)), ((315 + s.y) - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
        s.redraw(())




    def open_img(s, path):
        if path[-1] == 'm' : 
            t = open(path, 'r').read().encode('hex')
            t = 'ffd8ffe000104a464946' + t[20 : ]
            path = 'd:\\02.jpg'
            open(path, 'w').write(t.decode('hex'))
        try :
            s.img = Image.open(cn(path))
        except :
            s.img = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
            s.img.blit(s.img_z)
            s.img.text((5, 60), cn('打开失败,文件已损坏'), f_color, font = ('title', 15))
        try :
            os.remove('d:\\02.jpg')
        except :
            pass




    def open_fw(s, k = 0):
        s.rune = 1
        s.run = 1
        if k : 
            na = s.runelist[s.fw_pos]
            appuifw.app.exit_key_handler = s.ref
        else : 
            appuifw.app.exit_key_handler = s.rey
            na = s.runelist[(s.fw_pos - 1)]
        txt3 = s.txt_fw.split('\n' + na + ':\n')[1]
        txt4 = txt3.split('\n')[0]
        money = txt3.split('\n')[1]
        s.img_zbxx.blit(s.img_z)
        s.img_fw.clear(0)
        s.img_fw.blit(s.img_runes_all, (rune[runes[en(na)]], 0))
        s.img_zbxx.blit(s.img_fw.resize((45, 45)), (0, 0), mask = s.img_fw_mask.resize((45, 45)))
        txt5 = akntextutils.wrap_text_to_array(txt4, 'dese', (width - 40))
        s.img_zbxx.text((53, 22), na, f_color, font = ('title', 15))
        s.img_zbxx.text((53, 42), cn('价格:') + money, f_color, font = ('title', 15))
        t = 0
        for o in txt5:
            s.img_zbxx.text((0, (65 + (t * 20))), o + cn('(＊1)'), f_color, font = ('title', 14))
            la = re.findall('[+-](\\d{0,2}[.]\\d{0,3})', o)
            o9 = o
            if na.find(cn('精华')) != -1 : 
                leng = 3
            else : 
                leng = 9
            for g in la:
                o9 = o9.replace(g, repr((eval(g) * leng)))
            s.img_zbxx.text((0, (85 + (t * 20))), o9 + cn(('(＊%s)' % leng)), f_color, font = ('title', 14))
            t += 1
        s.img.blit(s.img_zbxx, (0,  - s.y))
        s.run = 0
        s.redraw(())




    def wit(s, k):
        s.y = 0
        s.redraw((), k = (k + 0.01))




    def wit_2(s, k = 1):
        if k : 
            s.na = txtfield.New((225, 5, 235, 15), cornertype = txtfield.ECorner2)
            if k == 1 : 
                s.na.bgcolor(8244000)
            else : 
                s.na.bgcolor(15132390)
            s.na.focus(0)
            s.na.visible(1)
        elif s.na : 
            s.na.visible(0)
            s.na = 0




    def ztxt(s, k, n = 0):
        f = open(k, 'r')
        txt3 = f.read()
        try :
            txt2 = txt3.decode('u16')
        except :
            txt2 = txt3.decode('u8')
        f.close()
        return txt2.replace('\r', '')




    def set(s, k = 0, o = 0):
        global width_, volume, orientation_, start_m, loading_m, sign, move_mobile, qu, acp, cd_bg, cd_t, cd_t_act, cd_t_find_pos, skin
        s.zc = 0
        e32.ao_sleep(0)
        list = [cn('每行字宽度'), cn('更改音效音量'), cn('设置横竖屏'), cn('更改启动动画'), cn('更改载入动画'), cn('更改收藏标志' + '　　　　　' + sign), cn('开启省流(使用前请查看帮助)　' + ['关', '开'][move_mobile]), cn(('退出提示　　　　　　　%s' % ['开', '关'][ not (qu)])), cn('默认接入点'), cn('更换主界面'), cn('色块界面显示头像' + '　　　' + ['否', '是'][cd_t]), cn('动态头像(详情看帮助)' + '　' + ['关', '开'][cd_t_act]), cn('色块头像更换跟随光标' + '　' + ['否', '是'][cd_t_find_pos]), cn('更改皮肤')]
        if  not (o) : 
            t = s.popup_menu(list, cn('【软件设置】  修改后重启软件生效'), o = k)
        else : 
            t = 100
        if  not (o) : 
            s.popup_pos_2 = s.popup_pos
        if t == None : 
            return s.rec(r = 1)
        if t == 0 : 
            list2 = [cn('300'), cn('340'), cn('380'), cn('400'), cn('420'), cn('460'), cn('500')]
            try :
                pos = list2.index(cn(str(width_)))
                list2[pos] = list2[pos] + cn(('　' * (15 - len(list2[pos]))) + '√')
            except :
                pos = 0
            t = s.popup_menu(list2, cn('【宽度设置】'), pos = pos)
            if t == None : 
                return s.set(1)
            width_ = en(list2[t].split(cn('　'))[0])
        elif t == 1 : 
            list2 = [cn(str(i)) for i in xrange(10)]
            list2[volume] = list2[volume] + cn(('　' * (15 - len(list2[volume]))) + '√')
            t = s.popup_menu(list2, cn('【音量设置】'), pos = volume)
            if t == None : 
                return s.set(1)
            volume = t
        elif t == 2 : 
            list2 = [cn('固定竖屏'), cn('固定横屏'), cn('自动检测横竖屏')]
            list2[orientation_] = list2[orientation_] + cn(('　' * (15 - len(list2[orientation_]))) + '√')
            t = s.popup_menu(list2, cn('【横竖屏设置】'), pos = orientation_)
            if t == None : 
                return s.set(1)
            orientation_ = t
        elif t == 3 : 
            list2 = [cn('动画①(正方形)'), cn('动画②(圆形.随机)'), cn('动画③(圆形.顺序)'), cn("动画④('L'形)")]
            list2[start_m] = list2[start_m] + cn(('　' * (15 - len(list2[start_m]))) + '√')
            t = s.popup_menu(list2, cn('【启动动画设置】'), pos = start_m)
            if t == None : 
                return s.set(1)
            start_m = t
        elif t == 4 : 
            list2 = [cn('动画①(拉幕,横)'), cn('动画②(拉幕,竖)')]
            list2[loading_m] = list2[loading_m] + cn(('　' * (15 - len(list2[loading_m]))) + '√')
            t = s.popup_menu(list2, cn('【载入动画设置】'), pos = loading_m)
            if t == None : 
                return s.set(1)
            loading_m = t
        elif t == 5 : 
            t = appuifw.query(cn('输入标志'), 'text', cn(sign))
            if t : 
                sign = en(t)
            pass
        elif t == 6 : 
            move_mobile =  not (move_mobile)
        elif t == 7 : 
            qu =  not (qu)
        elif t == 8 : 
            list2 = {}
            for i in s.socket.access_points():
                list2[i['name']] = i['iapid']
            n = 0
            if acp == -1 : 
                acp = s.socket.access_points()[0]['iapid']
            for i in list2.keys():
                if acp == list2[i] : 
                    break
                n += 1
            if n == len(list2) : 
                n = 0
            list3 = list2.keys()
            list3[n] = list3[n] + cn(('　' * (15 - len(list3[n]))) + '√')
            t = s.popup_menu(list3, cn('【选择接入点】'), pos = n)
            if t == None : 
                return s.set(1)
            acp = list2[list2.keys()[t]]
        elif t == 9 : 
            list2 = [cn('默认'), cn('色块①'), cn('色块②'), cn('色块③')]
            list2[cd_bg] = list2[cd_bg] + cn(('　' * (15 - len(list2[cd_bg]))) + '√')
            t = s.popup_menu(list2, cn('【选择主界面】'), pos = cd_bg)
            if t == None : 
                return s.set(1)
            s.cd_bg = cd_bg = t
        elif t == 10 : 
            cd_t =  not (cd_t)
        elif t == 11 : 
            cd_t_act =  not (cd_t_act)
        elif t == 12 : 
            cd_t_find_pos =  not (cd_t_find_pos)
        elif t == 13 : 
            list2 = [cn(i) for i in skin_name_list]
            list2[skin] = list2[skin] + cn(('　' * (15 - len(list2[skin]))) + '√')
            t = s.popup_menu(list2, cn('【选择皮肤】'), pos = skin)
            if t == None : 
                return s.set(1)
            skin = t
        a = ('width=%s\nvolume=%s\norientation=%s\nstart_m=%s\nloading_m=%s\nsign="%s"\nskin=%s\ncd_bg=%s\ncd_t=%s\ncd_t_find_pos=%s\nqu=%s\nacp=%s\nmove_mobile=%s\ncd_t_act=%s' % (width_, volume, orientation_, start_m, loading_m, sign, skin, cd_bg, cd_t, cd_t_find_pos, qu, acp, move_mobile, cd_t_act))
        f = open(mypath + 'set.ini', 'w')
        f.write(a)
        f.close()
        e32.ao_sleep(0)
        s.set(1)
        




    def updata(s):
        s.run = 1
        s.img_up = new(((240 + (80 * orientation)), 320))
        s.img_up.clear(0)
        s.img_up.blit(s.img_z)
        s.img_up.text((1, 20), cn('【安装资料】'), f_color, font = ('title', 14))
        ltxt = cn(("当前版本 : v%s\n请把下载的更新资料包放在e盘\n根目录下,并命名为'1.zip'\n然后按确定" % version))
        a = 0
        s.img_up.text((200, 317), cn('返回'), f_color, font = ('title', 14))
        s.img_up.text((10, 317), cn('确定'), f_color, font = ('title', 14))
        for i in ltxt.split('\n'):
            s.img_up.text((1, (40 + (20 * a))), i, f_color, font = ('title', 14))
            a += 1
        s.img.blit(s.img_up, (0,  - s.y))
        appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
        appuifw.app.menu_key_handler = s.data
        s.redraw(())




    def fz(s, txt = ''):
        if txt : 
            try :
                import clipboard
                clipboard.Set(txt)
            except :
                pass
            pass




    def help(s):
        if s.run : 
            return None
        s.run = s.hel = 1
        s.y4 = s.y
        s.y = 0
        appuifw.app.exit_key_handler = lambda  :  s.rec() 
        appuifw.app.menu_key_handler = pass_
        ltxt = akntextutils.wrap_text_to_array(cn(("【用户必读】\n ①使用联网功能前请先设置'开启节流'和'默认接入点'(注:开启节流功能需要:1.是移动用户 2.选择移动梦网(cmwap)接入点,不满足要求或开启后不能联网,请关闭)\n ②移动用户加入数据压缩功能,联网更快,更省流量,建议开启,详细请看上条\n ③开启动态头像可能会有闪回主页的情况,若觉得影响使用请关闭\n【功能说明】v%s\n ①查找英雄\物品(１键)\n ②英雄列表页上下翻页(２\８键)\n ③支持多音效功能,不过需要自己添加音效文件(文件名:英雄名***.mp3,***可以是任意字符,为的是不重名)放在e:\data\lolbox\文件夹下\n ④lol官网(推荐)、178网双通道查看周免\n ⑤比赛详情界面按ok键可保存截图\n ⑥推荐出装属性统计(在推荐装备界面按菜单)\n ⑦推荐出装修改；１键修改,２键上移,８键下移\n ⑧浏览英雄漫画(按确定键可全屏缩放)\n ⑨色块界面,在一个色块上按住ok键,移动光标放在另一色块上并送来ok键,可实现色块颜色的复制\n【安装更新包】\n 更新软件用的,主菜单点击'安装资料'查看详情\n【软件设置】\n 宽度:当每行会有一两个字显示不出来时,把它改小点就好。\n【其他】\n 软件的皮肤配色和色块颜色都可以diy,在e:\data\lolbox\app\下的skin.ini和color.ini里,当然diy需要点技巧(文件编码为u8),小心改了不能启动软件哦,所以请先备份。\n\n 注:软件设置重启后生效" % version)), 'dese', width)
        a = 0
        s.img = new(((240 + (80 * orientation)), ((len(ltxt) * 20) + 40)))
        s.img.blit(s.img_z)
        s.img.text((0, 20), cn('【软件帮助】:'), f_color, font = ('title', 14))
        for i in ltxt:
            s.img.text((1, (40 + (20 * a))), i, f_color, font = ('title', 14))
            a += 1
        s.run = 0
        s.redraw(())




    def about(s):
        s.run = 1
        img_ab = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
        img_ab.clear(0)
        img_ab.blit(s.img_z)
        img_ab.text((1, 20), cn('【关于软件】'), f_color, font = ('title', 14))
        ltxt = cn(('软件名：英雄联盟控\n版本：v%s\n更新时间：%s\n作者：Bysir\nQQ：1019654929\n官方网站：http://lolbox.4vx.cn\n——————\n英雄属性修改：小仔\n技能心得编辑：尘曦\n资料更新：Gomorrah丶' % (version, updata_time)))
        a = 0
        img_ab.text((200, 317), cn('返回'), f_color, font = ('title', 14))
        for i in ltxt.split('\n'):
            img_ab.text((1, (40 + (20 * a))), i, f_color, font = ('title', 14))
            a += 1
        s.img.blit(img_ab, (0,  - s.y))
        appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
        s.redraw(())




    def zbmn(s):
        s.run = 1
        s.pos_zb()
        list = s.wlist
        s.zbtj = 1
        t = ''
        for i in list:
            i = s.get_name(en(i))
            t += cn(s.txt_zb[i])
        txt = {}
        jg = 0
        for i in t.split(cn('价格:'))[1 : ]:
            jg += int(i.split(' ')[0].split('\n')[0])
        for i in t.split(cn('+')):
            sa = i.split('\n')[0]
            for h in xrange(len(sa)):
                try :
                    try :
                        int(sa[(h + 1)])
                    except :
                        if sa[(h + 1)] == '.' : 
                            pass
                        else : 
                            (0 / 0)
                        pass
                    if sa[(h + 1)] == '%' : 
                        (0 / 0)
                except :
                    break
            try :
                x = sa[ : (h + 1)]
                if  not (len(sa) > 12) : 
                    try :
                        txt[sa[(h + 1) : ]] += eval(x)
                    except :
                        txt[sa[(h + 1) : ]] = eval(x)
                    pass
            except :
                pass
        txt2 = 0
        y = ((len(txt) * 20) + 8)
        s.img_zbm = new((140, y))
        s.img_zbm.blit(s.img_z, (50, 0))
        s.img_zbm.polygon(s.rim(0, 0, 140, y), color_frame, width = 1)
        for i in txt:
            i = '+' + repr(txt[i]) + i
            w = s.img.measure_text(i, ('title', 14))
            t = ((w[0][2] - w[0][1]) / 2)
            s.img_zbm.text(((70 - t), (20 * txt2)), i, f_color, font = ('title', 14))
            txt2 += 1
        i = cn(('总价:%s' % jg))
        w = s.img.measure_text(i, ('title', 14))
        t = ((w[0][2] - w[0][1]) / 2)
        s.img_zbm.text(((70 - t), (20 * txt2)), i, f_color, font = ('title', 14))
        s.img.blit(s.img_zbm, ((-50 - (40 * orientation)), ( - s.y - ((160 - (40 * orientation)) - (y / 2)))))
        s.redraw(())
        appuifw.app.exit_key_handler = s.rey
        s.run = 0




    def sound(s):
        if s.pos_jn(1) : 
            s.pos_jn()
        else : 
            s.rey()
        import audio
        try :
            s.audio.stop()
        except :
            pass
        s.audio = audio.Sound.open(cn(s.path_sound))
        s.audio.set_volume(volume)
        s.audio.play(1)
        e32.ao_sleep(10)




    def finder(s):
        s.can()
        s.fin = 1
        s.run = 1
        e32.ao_yield()
        x9 = 150
        y9 = 20
        s.img_find = new(((240 + (80 * orientation)), 110))
        s.img_find.blit(s.img_z)
        s.img_find.polygon(s.rim(0, 0, (240 + (80 * orientation)), 110), color_frame, width = 1)
        s.img.blit(s.img_find, (0, (-210 - s.y) + (80 * orientation)))
        s.img.text((12, ((s.y + 233) - (80 * orientation))), cn('查找英雄'), f_color, font = ('title', 16))
        s.img.text((12, ((s.y + 257) - (80 * orientation))), cn('输入英雄名字:'), f_color, font = ('title', 14))
        s.img.text((7, ((s.y + 317) - (80 * orientation))), cn('确定'), f_color, font = ('title', 15))
        s.img.text(((203 + (80 * orientation)), ((s.y + 317) - (80 * orientation))), cn('取消'), f_color, font = ('title', 15))
        try :
            s.get.clear()
            s.get.bgcolor(6579300)
            s.get.focus(1)
            s.get.visible(1)
        except :
            s.get = txtfield.New((((120 + (40 * orientation)) - (x9 / 2)), (270 - (80 * orientation)), (120 + (40 * orientation)) + (x9 / 2), ((270 + y9) - (80 * orientation))), cornertype = txtfield.ECorner1)
            s.get.bgcolor(6579300)
            s.get.focus(1)
            s.get.visible(1)
            s.get.textstyle(u'', 120, 15132390, style = u'normal')
        s.redraw(())
        appuifw.app.menu_key_handler = lambda  :  s.ok(2) 
        appuifw.app.exit_key_handler = s.can_get




    def finder_2(s):
        if s.zb : 
            return None
        s.fin = 1
        s.run = 1
        e32.ao_yield()
        x9 = 150
        y9 = 20
        s.img_find = new(((240 + (80 * orientation)), 110))
        s.img_find.blit(s.img_z)
        s.img_find.polygon(s.rim(0, 0, (240 + (80 * orientation)), 110), color_frame, width = 1)
        s.img.blit(s.img_find, (0, (-210 - s.y) + (80 * orientation)))
        s.img.text((12, ((s.y + 233) - (80 * orientation))), cn('查找物品'), f_color, font = ('title', 16))
        s.img.text((12, ((s.y + 257) - (80 * orientation))), cn('输入物品名字:'), f_color, font = ('title', 14))
        s.img.text((7, ((s.y + 317) - (80 * orientation))), cn('确定'), f_color, font = ('title', 15))
        s.img.text(((203 + (80 * orientation)), ((s.y + 317) - (80 * orientation))), cn('取消'), f_color, font = ('title', 15))
        try :
            s.get.clear()
            s.get.bgcolor(6579300)
            s.get.focus(1)
            s.get.visible(1)
        except :
            s.get = txtfield.New((((120 + (40 * orientation)) - (x9 / 2)), (270 - (80 * orientation)), (120 + (40 * orientation)) + (x9 / 2), ((270 + y9) - (80 * orientation))), cornertype = txtfield.ECorner1)
            s.get.bgcolor(6579300)
            s.get.focus(1)
            s.get.visible(1)
            s.get.textstyle(u'', 120, 15132390, style = u'normal')
        s.redraw(())
        appuifw.app.menu_key_handler = lambda  :  s.ok(4) 
        appuifw.app.exit_key_handler = lambda  :  s.can_get(1) 




    def pd(s, k):
        if s.tfn == 1 : 
            a = 19
            b = 19
        elif s.tfn == 2 : 
            a = 38
            b = 19
        else : 
            a = 0
            b = 19
        e = ((tf_list[s.tfn][(k - a)][1] - 1) * 4)
        f = 0
        for i in s.tfmn_list[a : a + b]:
            f += i
        s.tfmnn[s.tfn] = f
        o = 0
        for i in s.tfmnn[ : 3]:
            o += i
        s.tfmnn[3] = o
        c = f >= e
        if  not (c) : 
            s.tfmn_list[k] = 0
        return s.pdneed(k, c)




    def pdneed(s, k, c = 1):
        if s.tfn == 1 : 
            a = 19
        elif s.tfn == 2 : 
            a = 38
        else : 
            a = 0
        try :
            ne = s.tf[k]['need']
            nne = ne.keys()[0]
            if s.tfzt == 1 : 
                color = (50, 220, 50)
            elif s.tfmn_list[a + int(nne)] == ne[nne] : 
                if  not (c) : 
                    s.tfmn_list[k] = 0
                color = (50, 220, 50)
            else : 
                s.tfmn_list[k] = 0
                c = 0
                color = (255, 0, 20)
            x1, y1 = tf_list[s.tfn][(k - a)]
            x2, y2 = (((x1 * 47) - 1) + (40 * orientation), ((y1 * 47) - 12))
            d = 7
            s.img.rectangle((x2, (y2 - d), (x2 + 9), y2), color, width = 1, fill = color)
            return c
        except :
            return c




    def wpzl(s, k = 0, n = 0, o = 0):
        s.wp = 1
        s.run = 1
        if k : 
            s.img = new(s.img_wp.size)
            s.img.blit(s.img_wp)
            s.run = 0
            return None
        if  not (s.txt_zb) : 
            import weapons_py
            s.txt_zb = weapons_py.txt_zb
        e32.ao_sleep(0)
        s.h_wp = 1
        s.wit(0)
        s.nlist = [cn(i) for i in weapons_list[n]]
        if  not (s.img_zb) : 
            try :
                s.img_zb = Image.open(mypath + 'weapons.jpeg')
            except :
                s.error(2)
            pass
        y9 = (((len(s.nlist) * 79) / 3) + 79)
        if y9 < (320 - (80 * orientation)) : 
            y9 = (320 - (80 * orientation))
        appuifw.app.exit_key_handler = s.rec
        s.img = new(((240 + (80 * orientation)), y9))
        for i in range(4):
            if (i * s.img_z.size[1]) < s.img.size[1] : 
                s.img.blit(s.img_z, (0, ( - i * s.img_z.size[1])))
            else : 
                break
        if o : 
            s.y6 = s.y
        s.men = s.y = s.wp_pos = 0
        y2 = 7
        s.h_wp = 1
        x2 = 10
        qv = 1
        for u in s.nlist:
            try :
                name = s.get_name(en(u))
                x_zb = weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
            except :
                s.img_t.clear(0)
            try :
                if  not ((qv % 10)) : 
                    s.wit((qv / (len(s.nlist) / 100.0)))
            except :
                pass
            w = s.img.measure_text(u, ('title', 13))
            t = ((w[0][2] - w[0][1]) / 2)
            s.img_name.blit(s.img_z, ((x2 - 13), (y2 + 56)))
            s.img_name.text(((47 - t), 15), cn(name), f_color, font = ('title', 13))
            s.img.blit(s.img_name, (( - x2 + 13), ( - y2 - 56)), mask = s.img_name_mask)
            s.img.blit(s.img_t, ( - x2,  - y2), mask = s.img_zb_mask_d)
            x2 += 75
            qv += 1
            if (qv % (3 + orientation)) == 1 : 
                x2 = 10
                y2 += 79
                s.h_wp += 1
        if  not ((len(s.nlist) % (3 + orientation))) : 
            s.h_wp -= 1
        s.img_wp = new(((240 + (80 * orientation)), y9))
        s.img_wp.blit(s.img)
        s.pos_wp()
        s.run = 0
        appuifw.app.exit_key_handler = s.rec




    def tfzl(s, k = 0, o = 0, n = 0, list = [0 for i in xrange(57)]):
        if k : 
            s.img = new(s.img_tf_hc.size)
            s.img.blit(s.img_tf_hc)
            return None
        s.run = 1
        if  not (s.tf) : 
            try :
                execfile(mypath + 'gifts.ini')
            except :
                s.error(17)
            pass
        if s.tfzt != 3 : 
            s.tfzt = 1
        if  not (s.img_tf_all) : 
            try :
                s.img_tf_all = Image.open(mypath + 'gifts.jpeg')
            except :
                s.error(16)
            try :
                s.img_tf_all_ = Image.open(mypath + 'gifts_.jpeg')
            except :
                s.error(18)
            pass
        if o : 
            s.y6 = s.y
            s.y = s.tfn = 0
            s.tfmn_list = list[ : ]
        if  not (n) : 
            s.tf_pos = 0
        if s.tfn == 1 : 
            a = 19
        elif s.tfn == 2 : 
            a = 38
        else : 
            a = 0
        s.img = new(((240 + (80 * orientation)), 320))
        s.img.blit(s.img_z)
        for i in tf_list[s.tfn]:
            x1 = ((17 - (40 * orientation)) - (i[0] * 47))
            y1 = (12 - (i[1] * 47))
            if s.tfzt == 1 : 
                s.img_fw.blit(s.img_tf_all, ((a * 40), 0))
                s.img_fw.polygon(s.rim(0, 27, 13, 40), color_pos, width = 1, fill = color_pos)
                s.img_fw.text((3, 40), cn(str(len(s.tf[a]['level']))), f_color_pos, font = ('title', 13))
                s.img.blit(s.img_fw, (x1, y1), mask = s.img_zb_mask)
                s.pdneed(a)
            elif s.pd(a) : 
                if  not (s.tfmn_list[a]) : 
                    s.img_fw.blit(s.img_tf_all_, ((a * 40), 0))
                else : 
                    s.img_fw.blit(s.img_tf_all, ((a * 40), 0))
                s.img_fw.polygon(s.rim(0, 27, 25, 40), color_pos, width = 1, fill = color_pos)
                s.img_fw.text((3, 40), cn(('%s/%s' % (s.tfmn_list[a], len(s.tf[a]['level'])))), f_color_pos, font = ('title', 13))
                s.img.blit(s.img_fw, (x1, y1), mask = s.img_zb_mask)
            else : 
                if  not (s.tfmn_list[a]) : 
                    s.img_fw.blit(s.img_tf_all_, ((a * 40), 0))
                else : 
                    s.img_fw.blit(s.img_tf_all, ((a * 40), 0))
                s.img.blit(s.img_fw, (x1, y1), mask = s.img_zb_mask)
            a += 1
        if s.tfzt == 3 : 
            for n in xrange(3):
                if n == 1 : 
                    a = 19
                    b = 19
                elif n == 2 : 
                    a = 38
                    b = 19
                else : 
                    a = 0
                    b = 19
                f = 0
                for i in s.tfmn_list[a : a + b]:
                    f += i
                s.tfmnn[n] = f
            o = 0
            for i in s.tfmnn[ : 3]:
                o += i
            s.tfmnn[3] = o
            if s.tfn == 1 : 
                g1, g2, g3 = s.tfmnn[ : 3]
            elif s.tfn == 2 : 
                g3, g1, g2 = s.tfmnn[ : 3]
            else : 
                g2, g3, g1 = s.tfmnn[ : 3]
            s.img.text(((220 + (80 * orientation)), 17), cn('已'), f_color, font = ('title', 12))
            s.img.text(((220 + (80 * orientation)), 30), cn('用'), f_color, font = ('title', 12))
            s.img.text(((220 + (80 * orientation)), 50), cn(str(s.tfmnn[3])), f_color, font = ('title', 12))
            s.img.text((1, 17), cn('加:②'), f_color, font = ('title', 12))
            s.img.text((1, 30), cn('减:⑧'), f_color, font = ('title', 12))
            s.img.text(((50 + (40 * orientation)), 30), cn(str(g1)), f_color, font = ('title', 12))
            s.img.text(((117 + (40 * orientation)), 30), cn(str(g2)), f_color, font = ('title', 12))
            s.img.text(((186 + (40 * orientation)), 30), cn(str(g3)), f_color, font = ('title', 12))
        if s.tfzt != 2 : 
            s.img.text((10, 315), cn('菜单'), f_color, font = ('title', 14))
        s.img.text(((35 + (40 * orientation)), 21), cn(tf_txt[s.tfn]), f_color, font = ('title', 17))
        s.img.text(((72 + (40 * orientation)), 28), cn('④'), f_color, font = ('title', 12))
        s.img.text(((157 + (40 * orientation)), 28), cn('⑥'), f_color, font = ('title', 12))
        s.img.text(((200 + (80 * orientation)), 315), cn('返回'), f_color, font = ('title', 14))
        s.img_tf_hc = new(((240 + (80 * orientation)), 640))
        s.img_tf_hc.blit(s.img)
        s.pos_tf()
        s.run = 0




    def tfmn(s):
        s.tf_pos = 0
        s.men = 0
        s.tfzt = 3
        s.tfzl()




    def fwzl(s, k = 0, n = 0, o = 0):
        s.run = 1
        s.zy = 0
        s.fw = 1
        s.fwmnz = 0
        e32.ao_yield()
        if k : 
            s.img = new(s.img_fwhc.size)
            s.img.blit(s.img_fwhc)
            s.run = 0
            return None
        if  not (s.img_runes_all) : 
            try :
                s.img_runes_all = Image.open(mypath + 'runes.jpeg')
            except :
                s.error(20)
            try :
                s.txt_fw = s.ztxt(mypath + 'runes.ini')
            except :
                s.error(19)
            pass
        s.runelist = [cn(i) for i in runes_list[n]]
        y9 = (((len(s.runelist) + 2)) * 50)
        if y9 < (320 - (80 * orientation)) : 
            y9 = (320 - (80 * orientation))
        if s.fwmn : 
            appuifw.app.exit_key_handler = s.rem
        else : 
            appuifw.app.exit_key_handler = s.rec
        s.img = new(((240 + (80 * orientation)), y9))
        s.img.blit(s.img_z)
        if o : 
            s.y6 = s.y
        s.rune = s.y = s.fw_pos = 0
        y2 = 5
        s.h_fw = 1
        for u in s.runelist:
            s.img_fw.clear(0)
            s.img_fw.blit(s.img_runes_all, (rune[runes[en(u)]], 0))
            s.img.blit(s.img_fw, (-7,  - y2), mask = s.img_fw_mask)
            money = (s.txt_fw.split('\n' + u + ':\n')[1]).split('\n')[0]
            if len(money) > 15 : 
                money = money[ : 14] + cn('…')
            s.img.text((53, (y2 + 17)), u, f_color, font = ('title', 14))
            s.img.text((53, (y2 + 37)), money, f_color, font = ('title', 14))
            y2 += 45 + (3 * orientation)
        s.img_fwhc = new(((240 + (80 * orientation)), (y2 + 78)))
        s.img_fwhc.blit(s.img)
        s.pos_fw()
        s.run = 0




    def fw_mn(s, n = 0):
        s.fwmn = s.fwmnz = 1
        s.fw = 0
        if n : 
            s.img.blit(s.img_mn, (0,  - s.y + (((100 + (80 * orientation))) * s.y_mn)))
            return s.redraw(())
        k = 0
        s.run = 1
        zj = 0
        s.img_mn = new(((240 + (80 * orientation)), 640))
        s.img_mn.blit(s.img_z)
        for i in xrange((4 - len(s.mnlist))):
            s.mnlist.append('')
        txt = {}
        for i in s.mnlist:
            if i : 
                o = (s.txt_fw.split(cn('\n' + i + ':\n'))[1]).split(cn('。。'))[0]
                jg = int(o.split('\n')[-2])
                o = o.split('\n')[0]
                s.img_fw.blit(s.img_runes_all, (rune[runes[i]], 0))
                la = re.findall('[+-](\\d{0,2}[.]\\d{0,3})', o)
                if i.find('精华') != -1 : 
                    leng = 3
                else : 
                    leng = 9
                for g in la:
                    o = o.replace(g, repr((eval(g) * leng)))
                zj += (jg * leng)
                for g in o.split(','):
                    if g.find('+') != -1 : 
                        a1, a2 = g.split('+')
                        a2 = eval(a2.split('%')[0])
                        try :
                            txt[a1 + '+'] += a2
                        except :
                            txt[a1 + '+'] = a2
                        pass
                    elif g.find('-') != -1 : 
                        a1, a2 = g.split('-')
                        a2 = eval(a2.split('%')[0])
                        try :
                            txt[a1 + '-'] += a2
                        except :
                            txt[a1 + '-'] = a2
                        pass
                s.img_mn.text((63, (17 + (k * 65))), cn(i) + ' *' + str(leng), f_color, font = ('title', 14))
                s.img_mn.text((63, (37 + (k * 65))), cn(('价格:%s*%s=%s' % (jg, leng, (jg * leng)))), f_color, font = ('title', 14))
                s.img_mn.text((21, (57 + (k * 65))), o, f_color, font = ('title', 14))
                s.img_mn.blit(s.img_fw, (-20, ( - k * 65)), mask = s.img_fw_mask)
            s.img_mn.text((1, (23 + (k * 65))), cn(txtlist[(k * 2)]), f_color, font = ('title', 14))
            s.img_mn.text((1, (48 + (k * 65))), cn(txtlist[((k * 2) + 1)]), f_color, font = ('title', 14))
            k += 1
            s.img_mn.line((0, ((k * 65) - 5), 320, ((k * 65) - 5)), color_line, width = 1)
        s.img_mn.line((17, 0, 17, 255), color_line, width = 1)
        s.img_mn.text((1, 280), cn(('总价:%s金币' % zj)), f_color, font = ('title', 14))
        txt2 = 0
        for b in txt:
            ok = b.find(cn('暴击')) != -1 or b.find(cn('死亡时间')) != -1 or b.find(cn('经验获得')) != -1 or b.find(cn('速度')) != -1 or b.find(cn('缩减')) != -1 or b.find(cn('吸血')) != -1 or b.find(cn('偷取')) != -1
            s.img_mn.text((1, (310 + (20 * txt2))), b + repr(txt[b]) + ('%' * ok), f_color, font = ('title', 14))
            txt2 += 1
        s.img.blit(s.img_mn, (0,  - s.y + (100 * s.y_mn)))
        appuifw.app.exit_key_handler = s.ref
        s.redraw(())
        f = open(mypath + 'runes_list.save', 'w')
        f.write('s.mnlist=' + repr(s.mnlist))
        f.close()
        s.run = 0




    def zhjn(s, k = 0):
        ly = ['虚弱', '幽灵疾步', '治疗术', '重生', '惩戒', '传送', '屏障', '净化', '清晰术', '引燃', '洞察', '闪现']
        s.run = 1
        if  not (s.img_allzh) : 
            try :
                s.img_allzh = Image.open(mypath + 'summoner.jpeg')
            except :
                s.error(15)
            pass
        if  not (s.txt_zh) : 
            try :
                s.txt_zh = s.ztxt(mypath + 'summoner.ini')
            except :
                s.error(14)
            pass
        s.zh = 1
        if s.pos_zh > (len(ly) - 1) : 
            s.pos_zh = 0
        elif s.pos_zh < 0 : 
            s.pos_zh = (len(ly) - 1)
        s.img.blit(s.img_z)
        try :
            txt = (s.txt_zh.split(cn(ly[s.pos_zh] + ':'))[1]).split(cn('。。'))[0]
        except :
            txt = cn('\n无介绍')
        a = 4
        w = s.img.measure_text(cn(ly[s.pos_zh]), ('title', 15))
        t = ((w[0][2] - w[0][1]) / 2)
        s.img.text(((127 - t) + (38 * orientation), (65 + s.y)), cn(ly[s.pos_zh]), color_highlight, ('normal', 15))
        txt10 = akntextutils.wrap_text_to_array(txt, 'dese', width)
        for i in txt10:
            s.img.text((0, s.y + (a * 17)), i, f_color, ('normal', 14))
            e32.ao_yield()
            a += 1
        a = 0
        for i in xrange(-2, 3):
            s.img_jn.blit(s.img_allzh, (allzhjn[ly[(i + s.pos_zh % len(ly))]], 0))
            s.img.blit(s.img_jn, ((-2 - (((48 + (19 * orientation))) * a)), ((-4 + (i == 0 * 2)) - s.y)), mask = s.img_jn_mask)
            e32.ao_yield()
            a += 1
        e32.ao_yield()
        s.redraw(())
        appuifw.app.exit_key_handler = s.rec
        s.run = 0


    
    def jcgx(s):
        s.run = 1
        s.img_gx = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
        s.img_gx.clear(0)
        s.img_gx.blit(s.img_z)
        s.img_gx.text((0, 20), cn('【检查更新】 '), f_color, font = ('title', 14))
        s.img_gx.text((0, 40), cn('>>>联网中…'), f_color, font = ('title', 14))
        s.img.blit(s.img_gx, (0,  - s.y))
        s.redraw(())
        appuifw.app.exit_key_handler = pass_
        e32.ao_yield()
        data = s.geturl('http://lolbox.4vx.cn/')
        if data.find('英雄') == -1 : 
            sv = '>>>联网失败,请稍后再试'
            s.img_gx.text((0, 60), cn(sv), f_color, font = ('title', 14))
            s.img_gx.text((0, 80), cn('提示:请查看帮助按帮助设置软件'), f_color, font = ('title', 14))
            s.img_gx.text(((200 + (80 * orientation)), (315 - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
            s.img.blit(s.img_gx, (0,  - s.y))
            s.redraw(())
            appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
            return None
        try :
            ol = data.find('更新版本')
            if ol != -1 : 
                data = data[ol : ]
                sv = data.split('更新版本:v')[1].split('<br/>')[0]
            else : 
                sv = data.split('当前版本:v')[1].split('<br/>')[0]
            try :
                ss = '更新时间:' + data.split('更新时间:')[1].split('<br/>')[0]
                sv = sv + '\n' + ss
            except :
                pass
            try :
                nr = '\n更新内容:\n' + data.split('更新内容:<br/>')[1].split('。')[0].replace('<br/>', '\n')
                sv = sv + nr
            except :
                pass
            if sv == version or data.find(version) != -1 : 
                sv = ('已是最新版 v%s\n无需更新' % version)
            else : 
                sv = '发现新版本:v' + sv + '\n\n快去官网下载吧'
        except :
            sv = '未发现新版本'
        a = 0
        svlist = akntextutils.wrap_text_to_array(cn(sv), 'dese', width)
        for i in svlist:
            s.img_gx.text((0, (60 + (a * 20))), i, f_color, font = ('title', 14))
            a += 1
        s.img_gx.text(((200 + (80 * orientation)), (315 - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
        s.img_gx.text((10, (315 - (80 * orientation))), cn('官网'), f_color, font = ('title', 14))
        s.img.blit(s.img_gx, (0,  - s.y))
        s.redraw(())
        appuifw.app.menu_key_handler = lambda  :  s.open_uc(o = 1) 
        appuifw.app.exit_key_handler = lambda  :  s.rec(1) 




    def zjcx(s, k = 0):
        s.run = 1
        e32.ao_sleep(0)
        if  not (k) : 
            s.y6 = s.y
        cxnx = s.popup_menu([cn('战斗力及场数'), cn('最近比赛详情')], cn('【要查询的记录】'))
        if cxnx == None : 
            return s.rec()
        fwq = [cn('艾欧尼亚　　电信一'), cn('祖安　　　　电信二'), cn('诺克萨斯　　电信三'), cn('班德尔城　　电信四'), cn('皮尔特沃夫　电信五'), cn('战争学院　　电信六'), cn('巨神峰　　　电信七'), cn('雷瑟守备　　电信八'), cn('裁决之地　　电信九'), cn('黑色玫瑰　　电信十'), cn('暗影岛　　　电信十一'), cn('钢铁烈阳　　电信十二'), cn('均衡教派　　电信十三'), cn('水晶之痕　　电信十四'), cn('影流　　　　电信十五'), cn('守望之海　　电信十六'), cn('征服之海　　电信十七'), cn('卡拉曼达　　电信十八'), cn('皮城警备　　电信十九'), cn('比尔吉沃特　网通一'), cn('德玛西亚　　网通二'), cn('弗雷尔卓德　网通三'), cn('无畏先锋　　网通四'), cn('恕瑞玛　　　网通五'), cn('扭曲丛林　　网通六'), cn('教育网专区　教育一')]
        po = s.popup_menu(fwq, cn('【选择服务器】'))
        if po == None : 
            return s.rec()
        fw = en(fwq[po].split(cn('　'))[-1])
        if  not (s.namelist.count(cn('重新输入'))) : 
            s.namelist.append(cn('重新输入'))
        while 1 : 
            if len(s.namelist) != 1 : 
                po = s.popup_menu(s.namelist, cn('【选择召唤师名称】'))
                if po == None : 
                    return s.zjcx(1)
                name = s.namelist[po]
                if name == cn('重新输入') : 
                    name = appuifw.query(cn('输入召唤师名称'), 'text')
                pass
            else : 
                name = appuifw.query(cn('输入召唤师名称'), 'text')
                if  not (name) : 
                    return s.zjcx(1)
                pass
            if name : 
                break
        if cxnx : 
            s.zjx = 1
        else : 
            s.zj = 1
        try :
            s.namelist.remove(name)
        except :
            pass
        s.namelist.insert(0, name)
        s.img.blit(s.img_z)
        if len(s.namelist) > 14 : 
            s.namelist = s.namelist[ : 13]
            s.namelist.append(cn('重新输入'))
        s.img.text((5, (20 + s.y)), cn('【战绩查询】'), f_color, font = ('title', 14))
        s.img.text((5, (40 + s.y)), cn('>>>联网中…'), f_color, font = ('title', 14))
        s.redraw(())
        s.run = 1
        e32.ao_sleep(0)
        f = open(mypath + 'name_list.save', 'w')
        f.write('s.namelist=' + repr(s.namelist))
        f.close()
        b = en(name)
        s.img.text((90, (40 + s.y)), cn('3'), f_color, font = ('title', 14))
        if  not ( not (s.img_t_all) and cxnx) : 
            try :
                s.img_t_all = Image.open(mypath + 'allt.jpeg')
            except :
                s.error(1)
            pass
        s.redraw(())
        e32.ao_yield()
        if cxnx : 
            pass
        else : 
            s.geturl('http://lolbox.duowan.com/playerList.php?keyWords=' + b)
        s.img.text((105, (40 + s.y)), cn('2'), f_color, font = ('title', 14))
        s.redraw(())
        s.urlj = 'http://lolbox.duowan.com/matchList.php?serverName=' + fw + '&playerName=' + b
        if  not (cxnx) : 
            data = s.geturl('http://lolbox.duowan.com/playerDetail.php?serverName=' + fw + '&playerName=' + b)
            s.img.text((120, (40 + s.y)), cn('1'), f_color, font = ('title', 14))
        s.redraw(())
        if cxnx : 
            s.run = 0
            return s.zjxx_page(1)
        else : 
            try :
                urlimg = data.split('><img src="')[1].split('"')[0]
                s.geturl(urlimg, 1)
            except :
                pass
            s.img.text((135, (40 + s.y)), cn('0'), f_color, font = ('title', 14))
            s.redraw(())
        s.img.blit(s.img_z)
        try :
            try :
                os.remove('d:\\0.jpeg')
            except :
                pass
            os.rename('d:\\0.html', 'd:\\0.jpeg')
        except :
            pass
        try :
            img_tx = Image.open('d:\\0.jpeg')
        except :
            img_tx = Image.new((65, 65))
            img_tx.clear(0)
        s.img.blit(img_tx, (0,  - s.y))
        try :
            name = b + (data.split('">' + b)[1]).split('</a>')[0]
            zdl = '战斗力:' + data.split('>战斗力</a>')[1].split("'>")[1].split('</span>')[0]
            try :
                z = '被赞' + data.split('">被赞 ')[1].split(' 次</div>')[0] + '次'
            except :
                z = '被赞0次'
            try :
                h = '拉黑' + data.split('">被拉黑 ')[1].split(' 次</div>')[0] + '次'
            except :
                h = '拉黑0次'
            s.img.text((68, (20 + s.y)), cn(name), f_color, font = ('title', 14))
            s.img.text((68, (40 + s.y)), cn(z + '   ' + zdl), f_color, font = ('title', 14))
            s.img.text((68, (60 + s.y)), cn(h), f_color, font = ('title', 14))
            try :
                f = data.split('经典模式')[1].split('</tr>')[0]
                jd = f.split('<td>')[1 : ]
                v = [i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '') for i in jd]
            except :
                v = ['', '', '', '', '']
            try :
                f2 = data.split('人机对战')[1].split('</tr>')[0]
                rj = f2.split('<td>')[1 : ]
                v2 = [i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '') for i in rj]
            except :
                v2 = ['', '', '', '', '']
            try :
                f3 = data.split('大乱斗')[1].split('</tr>')[0]
                dld = f3.split('<td>')[1 : ]
                v3 = [i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '') for i in dld]
            except :
                v3 = ['', '', '', '', '']
            try :
                f4 = data.split('S1+S2排位')[1].split('</tr>')[0]
                pw = f4.split('<td>')[1 : ]
                v4 = [i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '') for i in pw]
            except :
                v4 = ['', '', '', '', '', '']
            try :
                f5 = data.split('5v5单双排')[1].split('</tr>')[0]
                s3 = f5.split('<td>')[1 : ]
                v5 = []
                for i in s3:
                    if i.find('</span>') != -1 : 
                        v5.append(i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').split('>')[1].split('<')[0])
                    else : 
                        v5.append(i.split('</td>')[0].replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', ''))
            except :
                v5 = ['', '', '', '', '', '']
            s.img.text((0, (90 + s.y)), cn('匹配模式:'), f_color, font = ('title', 14))
            a = 1
            txt = cn('总场 胜率 胜场 负场 逃跑')
            s.img.text((40, (90 + (a * 20)) + s.y), txt, f_color, font = ('title', 14))
            s.img.text((0, (110 + (a * 20)) + s.y), cn('传统:'), f_color, font = ('title', 14))
            s.img.text((0, (130 + (a * 20)) + s.y), cn('人机:'), f_color, font = ('title', 14))
            s.img.text((0, (150 + (a * 20)) + s.y), cn('极地:'), f_color, font = ('title', 14))
            we = 43
            for i in xrange(len(v)):
                s.img.text((we, (110 + (a * 20)) + s.y), cn(v[i]), f_color, font = ('title', 14))
                s.img.text((we, (130 + (a * 20)) + s.y), cn(v2[i]), f_color, font = ('title', 14))
                s.img.text((we, (150 + (a * 20)) + s.y), cn(v3[i]), f_color, font = ('title', 14))
                we += 36
            s.img.text((0, (190 + s.y)), cn('排位模式:'), f_color, font = ('title', 14))
            a = 2
            txt = cn('段位 胜点 总  率  胜  负  逃')
            s.img.text((34, (170 + (a * 20)) + s.y), txt, f_color, font = ('title', 14))
            s.img.text((0, (190 + (a * 20)) + s.y), cn('S1S2:'), f_color, font = ('title', 14))
            s.img.text((0, (210 + (a * 20)) + s.y), cn('S3:'), f_color, font = ('title', 14))
            we = 35
            a = 6
            for i in xrange(len(v4)):
                s.img.text((we, (110 + (a * 20)) + s.y), cn(v4[i]), f_color, font = ('title', 14))
                if i == 0 : 
                    s.img.text(((we - 18), (130 + (a * 20)) + s.y), cn(v5[i]), f_color, font = ('title', 14))
                elif i == 1 : 
                    s.img.text(((we + 3), (130 + (a * 20)) + s.y), cn(v5[i]), f_color, font = ('title', 14))
                else : 
                    s.img.text((we, (130 + (a * 20)) + s.y), cn(v5[i]), f_color, font = ('title', 14))
                if i > 1 : 
                    we += 27
                else : 
                    we += 37
            jj = data.split('>时间</th>')[1]
            j = jj.split('title="')[1 : ]
            vv = []
            a = 5.5
            for i in j:
                na = i.split('"')[0]
                ms = i.split('<td>')[1].split('</td>')[0] + '　　'
                sf = i.split('</em></td>')[0].split('">')[-1]
                sj = i.split('<td>')[3].split('</td>')[0]
                i = cn(ms)[ : 3] + cn('　 　 ') + cn(sj)
                vv.append((i, sf))
                try :
                    na = s.get_name(na)
                    s.img_t.blit(s.img_t_all, (people[na], 0))
                except :
                    s.img_t.clear(0)
                s.img.blit(s.img_t.resize((17, 17)), (-2, ((( - a * 20) - 165) - s.y)))
                a += 1
            a = 5.5
            s.img.text((0, (160 + (a * 20)) + s.y), cn('最近比赛:'), f_color, font = ('title', 14))
            for i in vv:
                s.img.text((22, (180 + (a * 20)) + s.y), i[0], f_color, font = ('title', 14))
                if i[1] == '胜利' : 
                    c = (99, 190, 16)
                else : 
                    c = (210, 60, 60)
                s.img.text((71, (180 + (a * 20)) + s.y), cn(i[1]), c, font = ('title', 14))
                a += 1
        except :
            s.img.text((5, (90 + s.y)), cn('>>>获取失败,请重试'), f_color, font = ('title', 14))
            s.img.text((0, (110 + s.y)), cn('提示:请查看帮助按帮助设置软件'), f_color, font = ('title', 14))
            s.img.text((5, (130 + s.y)), cn('并确定服务器和召唤师名称的正确'), f_color, font = ('title', 14))
            s.redraw(())
        s.img.text((5, (437 + s.y)), cn('比赛详情'), f_color, font = ('title', 14))
        s.img.text(((205 + (80 * orientation)), (437 + s.y)), cn('返回'), f_color, font = ('title', 14))
        s.redraw(())
        s.run = 0
        appuifw.app.menu_key_handler = lambda  :  s.zjxx_page(1, 0) 
        appuifw.app.exit_key_handler = s.rec




    def yxmh(s, k = 0):
        if s.run : 
            return None
        s.uppage = s.downpage = 0
        s.run = 1
        try :
            s.mh_list = os.listdir(mypath2+'lom\\')
            list = [cn(i.split('.')[0]) for i in s.mh_list]
            list.append(cn('＊到官网下载更多漫画'))
            (1 / len(s.mh_list))
        except :
            appuifw.note(cn('未在e:\data\lolbox\lom\下找到漫画,请到官网下载'), 'error', 1)
            return s.rec(1)
        if  not (s.img_up) : 
            s.img_up = Image.open(mypath + 'up.jpeg')
            s.img_up_mask = new(s.img_up.size, 'L')
            s.img_up_mask.load(mypath + 'up_mask.jpeg')
            s.img_do = Image.open(mypath + 'do.jpeg')
            s.img_do_mask = new(s.img_up.size, 'L')
            s.img_do_mask.load(mypath + 'do_mask.jpeg')
        t = s.popup_menu(list, cn('【漫画列表】'), o = k)
        if t == None : 
            return s.rec(1)
        s.popup_pos_2 = t
        if t == (len(list) - 1) : 
            return s.open_uc(3)
        s.run = 1
        path = mypath2+'lom\\' + s.mh_list[t]
        s.y = 0
        s.redraw((), k = 0.01)
        s.uppage = s.downpage = 0
        e32.ao_sleep(0)
        appuifw.app.exit_key_handler = lambda  :  s.yxmh(1) 
        s.open_img(path)
        s.mh = 1
        s.run = 0
        if  not (s.mh_tp) : 
            s.mh_tp = 1
            s.event({'scancode' : 167, 'type' : 3})
        else : 
            s.redraw(())




    def ckzm(s):
        import time
        if s.run : 
            return None
        s.zm_pos = s.men = 0
        s.zm = 1
        s.run = 1
        if  not (s.img_t_all) : 
            try :
                s.img_t_all = Image.open(mypath + 'allt.jpeg')
            except :
                s.error(1)
            pass
        appuifw.app.exit_key_handler = s.rec
        e32.ao_yield()
        s.img_zm = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
        s.img_zm.clear(0)
        s.img_zm.blit(s.img_z)
        try :
            f = open('e:\data\lolbox\app\周免.ini', 'r')
            data = f.read()
            f.close()
            n, data = data.split('\n')
            s.img_zm.text((0, 20), cn('【查看周免】 ' + n), f_color, font = ('title', 14))
            s.img_zm.text((0, 40), cn('>>>本周免费英雄:'), f_color, font = ('title', 14))
            s.zm_list = data.split(',')
            s.out_zm()
            s.img_zm.text(((107 + (40 * orientation)), (315 - (80 * orientation))), cn('刷新'), f_color, font = ('title', 14))
            s.img_zm.text((10, (315 - (80 * orientation))), cn('详细'), f_color, font = ('title', 14))
            s.img_zm.text(((200 + (80 * orientation)), (315 - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
            s.img.blit(s.img_zm, (0,  - s.y))
            s.redraw(())
            appuifw.app.menu_key_handler = lambda  :  s.zui(o = 100) 
            appuifw.app.exit_key_handler = s.rec
            s.run = 0
        except :
            s.run = 0
            import time
            timen = time.localtime()
            ti = cn(str(timen[1]) + '月' + str(timen[2]) + '日')
            s.img_zm.text((0, 20), cn('【查看周免】 ') + ti, f_color, font = ('title', 14))
            s.img_zm.text(((107 + (40 * orientation)), (315 - (80 * orientation))), cn('刷新'), f_color, font = ('title', 14))
            s.img_zm.text((10, (315 - (80 * orientation))), cn('详细'), f_color, font = ('title', 14))
            s.img_zm.text(((200 + (80 * orientation)), (315 - (80 * orientation))), cn('返回'), f_color, font = ('title', 14))
            s.img.blit(s.img_zm, (0,  - s.y))
            appuifw.app.menu_key_handler = lambda  :  s.zui(o = 100) 
            appuifw.app.exit_key_handler = s.rec
            s.redraw(())
            return s.gxzm()




    def gxzm(s, k = 0):
        if k : 
            s.img = new(s.img_zm_hc.size)
            s.img.blit(s.img_zm_hc)
            return None
        s.td = [cn('通道1 (lol.com)'), cn('通道2 (178.com)')]
        s.run = 1
        s.zm = 2
        s.img_zm_2 = new((130, 46))
        s.img_zm_2.blit(s.img_z)
        s.img_zm_2.polygon(s.rim(0, 0, 130, 46), color_frame, width = 1)
        s.img_zm_2.text((12, 20), s.td[0], f_color, font = ('title', 14))
        s.img_zm_2.text((12, 40), s.td[1], f_color, font = ('title', 14))
        s.img.blit(s.img_zm_2, ((-55 - (40 * orientation)), ( - s.y - 250) + (80 * orientation)))
        s.img_zm_hc = new(s.img.size)
        s.img_zm_hc.blit(s.img)
        s.pos_zm()
        appuifw.app.menu_key_handler = None
        appuifw.app.exit_key_handler = s.ckzm
        s.run = 0




    def bjlb(s, k = 0):
        s.run = 1
        if  not ( not (s.bj) and k) : 
            s.img_dbzt.blit(s.img_z)
            s.img_dbzt.polygon(s.rim(0, 0, (240 + (80 * orientation)), 25), color_frame, width = 1)
            s.img_dbzt.text((40, 20), cn('点击英雄加入/移除收藏夹'), f_color, font = ('title', 14))
            s.bj = 1
        for i in s.fa_list:
            try :
                n = s.name_list.index(i)
            except :
                continue
            x_fa = ((((n % (3 + orientation))) * 75) + 67)
            y_fa = ((((n / (3 + orientation))) * 79) + 20)
            s.img_zui.text((x_fa, y_fa), cn(sign), color_like, font = ('title', 14))
        if  not (k) : 
            s.pos_yx()
            appuifw.app.exit_key_handler = lambda  :  s.zui(r = 1) 
        s.run = 0




    def zzzz(s):
        s.run = 1
        s.img = new(((240 + (80 * orientation)), 640))
        s.img.blit(s.img_z)
        s.zzz = 1
        s.y4 = s.y
        s.y = 0
        ltxt = akntextutils.wrap_text_to_array(cn('【资助作者】\n 到现在,软件已经成为我心中的完美,可能在游戏上,这软件并不专业,但对于爱好做软件的我来说,它已经很不错了,用了我一年多的心血,不断更新,全当练习,为以后铺路,我也认准了软件专业,请大家祝福我吧,如果以后我有幸为你们做软件,大家记得多多支持。\n 本来想删掉这个功能的,想想还是算了吧,就当是我对大家的诉苦吧\n\n 我的支付宝帐号:15983249561\n 谢谢!! \n\n用uc进入支付宝?'), 'dese', width)
        n = 0
        for i in ltxt:
            s.img.text((1, (20 + (n * 20))), i, f_color, font = ('title', 14))
            n += 1
        s.img.text(((200 + (80 * orientation)), 397), cn('返回'), f_color, font = ('title', 14))
        s.img.text((10, 397), cn('确定'), f_color, font = ('title', 14))
        s.redraw(())
        e32.ao_sleep(0)
        s.na = txtfield.New((120, 0, 220, 20), cornertype = txtfield.ECorner2)
        s.na.textstyle(u'', 120, 15132390, style = u'normal')
        s.na.bgcolor(6579300)
        s.na.align(txtfield.ECenterAlign)
        s.na.add(cn('15983249561'), 1)
        s.na.visible(1)
        s.na.focus(1)
        s.run = 0
        appuifw.app.menu_key_handler = lambda  :  s.open_uc(2, 1) 
        appuifw.app.exit_key_handler = lambda  :  s.rec(1) 




    def out_zm(s):
        if  not (orientation) : 
            a = 1
            for i in s.zm_list:
                s.img_zm.text((0, (60 + (a * 20))), cn(('%02d.%s' % (a, i))), f_color, font = ('title', 14))
                try :
                    i = s.get_name(i)
                    s.img_t.blit(s.img_t_all, (people[i], 0))
                except :
                    s.img_t.clear(0)
                s.img_zm.blit(s.img_t.resize((30, 30)), ((-160 - ( not ((a % 2)) * 35)), (( - a * 20) - 38)), mask = s.img_t_mask_x)
                w = s.img.measure_text(cn(i), ('title', 14))
                t = (w[0][2] - w[0][1])
                s.img_zm.line(((t + 10), ((a * 20) + 52), (157 + ((((a + 1) % 2)) * 35)), ((a * 20) + 52)), color_line, width = 1)
                a += 1
            pass
        else : 
            a = 1
            for i in s.zm_list:
                s.img_zm.text((( not ((a % 2)) * 210), (80 + (((a - 1) / 2) * 32))), cn(('%02d.%s' % (a, i))), f_color, font = ('title', 14))
                try :
                    i = s.get_name(i)
                    s.img_t.blit(s.img_t_all, (people[i], 0))
                except :
                    s.img_t.clear(0)
                s.img_zm.blit(s.img_t.resize((30, 30)), ((-127 - ( not ((a % 2)) * 35)), (( - ((a - 1) / 2) * 32) - 58)), mask = s.img_t_mask_x)
                a += 1
            pass




    def dbyx(s):
        s.db_list = []
        s.can()
        s.db = 1
        s.img_dbzt.blit(s.img_z)
        s.img_dbzt.polygon(s.rim(0, 0, (240 + (80 * orientation)), 25), color_frame, width = 1)
        s.img_dbzt.text((40, 20), cn('请点击两个英雄进行对比'), f_color, font = ('title', 14))
        s.redraw(())




    def getnew(s, k = 0, n = 1):
        s.run = 1
        s.y = 0
        s.img.blit(s.img_z)
        s.img.text((0, 20), cn(('【查看新闻】 第%s页' % n)), f_color, font = ('title', 14))
        s.img.text((0, 40), cn('>>>联网中…'), f_color, font = ('title', 14))
        s.redraw(())
        e32.ao_sleep(0)
        if k : 
            return None
        url_xw_ = url_xw.replace('/list_1.', '/list_' + str(n) + '.')
        data = s.geturl(url_xw_)
        try :
            s.new_list = {}
            if  not (data) : 
                (0 / 0)
            b = data.split('[新闻]')[1 : ]
            for i in b:
                u = 'http://lol.qq.com' + i.split('<a href="')[1].split('"')[0].replace('amp;', '')
                name = cn(i.split('</a>')[1].split('>')[1])
                s.new_list[name] = u
            s.new_page = n
            open(mypath + 'new.save', 'w').write('s.new_list=' + repr(s.new_list) + '\ns.new_page=' + repr(s.new_page))
            s.run = 0
            s.popup_pos_2 = None
            s.new()
        except :
            s.run = 0
            s.img.text((0, 60), cn('>>>联网失败'), f_color, font = ('title', 14))
            s.img.text((0, 80), cn('提示:请查看帮助按帮助设置软件'), f_color, font = ('title', 14))
            s.redraw(())
            appuifw.app.menu_key_handler = None
            appuifw.app.exit_key_handler = s.rec




    def new(s, o = 0):
        if s.run : 
            return None
        s.ne = 1
        s.tx = s.zy = 0
        if s.new_list == None : 
            return s.getnew()
        s.run = 1
        t = s.popup_menu(s.new_list.keys(), cn(('【查看新闻】 第%s页' % s.new_page)), o = o)
        if t == None : 
            return s.rec(1)
        if s.tx : 
            s.run = 0
            return None
        s.getnew(1)
        s.run = 1
        try :
            if s.popup_pos_2 != s.popup_pos : 
                txt = s.geturl(s.new_list.values()[t])
            else : 
                txt = open('d:\\0.html', 'r').read()
        except :
            txt = s.geturl(s.new_list.values()[t])
        txt_ = ''
        for i in txt.split('<p>')[1 : ]:
            c = i.split('</p>')[0].replace('<br />', '\n').replace('<br/>', '\n')
            if c.find('<') != -1 : 
                for a in c.split('<')[1 : ]:
                    c = c.replace(a.split('>')[0], '').replace('<>', '')
                pass
            txt_ += c + '\n'
        txt_list = akntextutils.wrap_text_to_array(cn(txt_), 'dese', width)
        s.tx = s.zy = 1
        s.y_txt = ((len(txt_list) * 20) + 20)
        s.img = new(((240 + (80 * orientation)), s.y_txt))
        for i in range(4):
            if (i * s.img_z.size[1]) < s.img.size[1] : 
                s.img.blit(s.img_z, (0, ( - i * s.img_z.size[1])))
            else : 
                break
        n = 1
        for i in txt_list:
            s.img.text((1, (n * 20)), i, f_color, font = ('title', 14))
            n += 1
        s.run = 0
        s.popup_pos_2 = s.popup_pos
        s.redraw(())
        appuifw.app.exit_key_handler = lambda  :  s.new(1) 




    def dbyx_ok(s):
        s.run = 1
        s.db = 0
        list = s.db_list
        txt = [s.ztxt((mypath2+'%s.txt' % i)) for i in list]
        s.db_list = []
        sm = []
        for n in [cn('生命值　： '), cn('魔法值　： '), cn('攻击力　： '), cn('物理护甲： '), cn('魔法抵抗： '), cn('攻击速度： '), cn('移动速度： '), cn('生命回复： '), cn('魔法回复： '), cn('攻击范围： ')]:
            for i in txt:
                sm.append(i.split(n)[1].split('\n')[0].split('\n')[0].replace(cn('/每级)'), ')'))
        s.img_db = new((240, 320))
        s.img_db.blit(s.img_z)
        a = 1
        for i in list:
            i = s.get_name(i)
            s.img_t.blit(s.img_t_all, (people[i], 0))
            s.img_db.blit(s.img_t, ((-50 - a), -7), mask = s.img_t_mask)
            w = s.img.measure_text(cn(i), ('title', 14))
            t = ((w[0][2] - w[0][1]) / 2)
            s.img_db.text(((84 - t) + a, 80), cn(i), f_color, font = ('title', 14))
            a = 95
        n = 0
        l2 = [cn('生命:'), cn('魔法:'), cn('攻击:'), cn('护甲:'), cn('魔抗:'), cn('攻速:'), cn('移速:'), cn('生回:'), cn('魔回:'), cn('攻距:')]
        for i in sm:
            if  not ((n % 2)) : 
                a = sm[n].split('(')[0]
                b = (sm[(n + 1)]).split('(')[0]
                a = eval(a)
                b = eval(b)
                if a > b : 
                    color = color_highlight_n
                else : 
                    color = f_color
                pass
            else : 
                s.img_db.text((0, (105 + (20 * (n / 2)))), l2[(n / 2)], f_color, font = ('title', 14))
                try :
                    a = sm[(n - 1)].split('(')[0]
                    b = sm[n].split('(')[0]
                    a = eval(a)
                    b = eval(b)
                    if a < b : 
                        color = color_highlight_n
                    else : 
                        color = f_color
                except :
                    pass
                pass
            s.img_db.text(((50 + ((n % 2) * 95)), (105 + (20 * (n / 2)))), i, color, font = ('title', 14))
            n += 1
        if orientation : 
            import graphics
            s.img_db = s.img_db.transpose(graphics.ROTATE_270)
        s.img.blit(s.img_db, (0,  - s.y))
        appuifw.app.exit_key_handler = s.can
        s.redraw(())




    def Diy(s, k = 0):
        s.run = 1
        if k : 
            s.img.blit(s.img_hc)
            s.run = 0
            return None
        na = s.name_list[(((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)]
        s.diy = 1
        s.img = new(((240 + (80 * orientation)), (320 - (80 * orientation))))
        s.img.blit(s.img_z)
        s.img.text((1, 36), cn('正在修改 : ' + na), f_color, font = ('title', 14))
        na = s.get_name(na)
        s.img_t.blit(s.img_t_all, (people[na], 0))
        x = 0
        y = 59
        for i in xrange(4):
            s.img.line((0, y + (i * 60), 320, y + (i * 60)), 0, width = 1)
        s.img.text((1, 77), cn('六神装 : '), f_color, font = ('title', 14))
        s.img.text((1, 137), cn('召唤师技能 : '), f_color, font = ('title', 14))
        s.img.text((1, 197), cn('加点顺序 : '), f_color, font = ('title', 14))
        if  not (s.img_zb) : 
            try :
                s.img_zb = Image.open(mypath + 'weapons.jpeg')
            except :
                s.error(2)
            pass
        s.img.blit(s.img_t, (((-240 - (80 * orientation)) + 57), -2), mask = s.img_t_mask)
        s.getxx(na)
        for i in xrange(6):
            name = s.get_name(en(s.wlist[i]))
            x_zb = weapons[name]
            s.img_t.blit(s.img_zb, (x_zb, 0))
            s.img.blit(s.img_t.resize((30, 30)), ((-5 - (((40 + (15 * orientation))) * i)), -85), mask = s.img_zb_mask.resize((30, 30)))
        s.y_diy = s.y
        s.y = 0
        appuifw.app.exit_key_handler = lambda  :  s.reu() 
        s.img_hc = new(s.img.size)
        s.img_hc.blit(s.img)
        s.run = 0
        s.pos_Diy()




    def yxbj(s):
        s.run = s.yxbj_ = 1
        s.redraw((), 0.001)
        e32.ao_yield()
        if  not (s.list_bj) : 
            execfile(mypath + 'bj.ini')
        s.y6 = s.y
        s.y = 0
        s.men = 0
        s.img.blit(s.img_z)
        y = 40
        name = s.name_list[(((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)]
        try :
            txt = cn(s.list_bj[name])
        except :
            txt = cn('无')
        txtlist = akntextutils.wrap_text_to_array(txt, 'dese', width)
        s.h_yxbj = ((len(txtlist) * 20) + 40)
        s.img.text((1, 20), cn(name + ' :'), f_color, font = ('title', 14))
        for i in txtlist:
            s.img.text((1, y), i, f_color, font = ('title', 14))
            y += 20
        s.redraw(())
        appuifw.app.exit_key_handler = lambda  :  s.reo(1) 
        s.run = 0




    def god_team(s):
        s.run = s.team = 1
        s.redraw((), 0.01)
        e32.ao_yield()
        if  not (s.img_t_all) : 
            try :
                s.img_t_all = Image.open(mypath + 'allt.jpeg')
            except :
                s.error(1)
            pass
        if  not (s.list_team) : 
            execfile(mypath + 'god_team.ini')
        y = 40
        s.img = new(((240 + (80 * orientation)), 2600))
        s.img.blit(s.img_z)
        s.img.text((0, 20), cn('【神团】'), f_color, font = ('title', 14))
        s.img.line((0, (y - 18), 320, (y - 18)), color_line, width = 1)
        for i in s.list_team:
            s.img.text((0, y), cn(i['name']), f_color, font = ('title', 14))
            x = 0
            for ii in i['team']:
                try :
                    ii = s.get_name(ii)
                    s.img_t.blit(s.img_t_all, (people[ii], 0))
                except :
                    s.img_t.clear(0)
                s.img.blit(s.img_t.resize((47, 47)), ( - x, ( - y - 2)), mask = s.img_t_mask.resize((47, 47)))
                x += 48
            try :
                txt = cn(i['txt'])
                txtlist = akntextutils.wrap_text_to_array(txt, 'dese', width)
                for i in txtlist:
                    s.img.text((1, (y + 70)), i, f_color, font = ('title', 14))
                    y += 20
            except :
                pass
            y += 75
            s.img.line((0, (y - 22), 320, (y - 22)), color_line, width = 1)
        s.redraw(())
        s.h_team = y
        appuifw.app.exit_key_handler = s.rec
        s.run = 0




    def zjxx_page(s, k = 0, o = 1):
        if s.run : 
            return None
        e32.ao_sleep(0)
        s.run = 1
        s.y = 0
        s.men = 0
        s.img.blit(s.img_z)
        s.zjx_page = k
        s.img.text((5, (20 + s.y)), cn('【战绩查询】'), f_color, font = ('title', 14))
        if o : 
            s.img.text((5, (40 + s.y)), cn('>>>联网中… 3 2 1'), f_color, font = ('title', 14))
        else : 
            s.img.text((5, (40 + s.y)), cn('>>>联网中…'), f_color, font = ('title', 14))
        s.run = 1
        s.redraw(())
        a = s.geturl(s.urlj + '&page=' + str((k - 1)))
        s.ajax_list = [i.split(';">')[0] for i in a.split('onclick="')[1 : ]]
        s.txtlist = []
        for i in [i.split('</li>')[0] for i in a.split('<li id=')[1 : ]]:
            na = i.split(' alt="')[1].split('"')[0]
            sf = i.split('<p>')[1].split('</p>')[0]
            sf_0 = sf.split('>')[1].split('<')[0]
            sf_1 = sf.split('>')[-1]
            sf = sf_0 + sf_1
            dt = i.split('<p>')[2].split('</p>')[0].replace('   ', ' ')
            id = i.split('(')[1].split(',')[0]
            sf, ms = sf.replace('）', '').split('（')
            s.txtlist.append(cn(na + ' ' + sf + '|' + ms + ' ' + dt + '|' + id))
        s.run = 0
        s.zjxx()




    def zjxx(s, pos = 0):
        if s.run : 
            return None
        s.zjx_t = 0
        s.y = s.x_ = s.x = 0
        s.run = 1
        po = s.popup_menu(s.txtlist, cn(('【选择比赛】 第%s页' % s.zjx_page)), pos = pos)
        if po == None : 
            return s.rec()
        if s.zjx_t : 
            return None
        appuifw.app.exit_key_handler = pass_
        s.zjx_now = s.txtlist[po]
        s.run = 1
        s.zjx_t = 1
        s.y = 0
        s.img.blit(s.img_z)
        s.img.text((5, 20), cn('【比赛查询】'), f_color, font = ('title', 14))
        s.img.text((5, 40), cn('>>>获取比赛中…'), f_color, font = ('title', 14))
        s.redraw(())
        e32.ao_sleep(0)
        if  not (s.zj_dir) : 
            try :
                execfile(mypath + 'zj.save')
            except :
                s.zj_dir = {}
            pass
        if  not (s.img_t_all) : 
            try :
                s.img_t_all = Image.open(mypath + 'allt.jpeg')
            except :
                s.error(1)
            pass
        if  not (s.img_zb) : 
            try :
                s.img_zb = Image.open(mypath + 'weapons.jpeg')
            except :
                s.error(2)
            pass
        list2 = s.ajax_list[po].split('(')[1].split(')')[0].split(',')
        url = ('http://lolbox.duowan.com/ajaxMatchDetail.php?matchId=%s&queueType=%s&serverName=%s&playerName=%s' % (list2[0], list2[1], list2[2], list2[3]))
        name = eval(list2[3])
        wj_gd_ = ['补兵：', '推塔：', '最大连杀：', '最大多杀：', '最大暴击：', '总治疗：', '金钱：', '杀我方野怪：', '杀敌方野怪：', '放眼数：', '排眼数：', '承受伤害：', '给对方英雄造成总伤害：']
        s.run = 1
        s.zjx = 1
        if s.zjx_now not in s.zj_dir : 
            a = s.geturl(url).split('<style>')[1]
            time = a.split('<th class="right prm"')[1].split('</th>')[0].split("<span title='")
            time_0 = time[0].split('>')[-1]
            time_1 = time[1].split('>结束于')[0]
            rwxx = [i.split('</li>')[0].replace('<span>', '').replace('</span>', ' ') for i in a.split('<li>')[1 : ]]
            txt = '\n'.join(rwxx).replace('杀敌：', '\n杀敌：')
            wj_xx = txt.split('\n\n')
            wj_rt = []
            wj_gd = []
            for i in wj_xx:
                sj = []
                for ii in wj_gd_:
                    try :
                        aa = i.split(ii)[1].split(' ')[0].split('\n')[0]
                    except :
                        aa = '无'
                    sj.append(aa)
                wj_gd.append([sj[i2] for i2 in xrange(13)])
                sj = [('%02d' % int(i4)) for i4 in [i.split(i3)[1].split(' ')[0].split('\n')[0] for i3 in ['杀敌：', '死亡：', '助攻：']]]
                wj_rt.append(' '.join(sj))
            wj_name = [i.split('<')[0].replace(' ', '') for i in a.split('<div class="z-skill">')[1 : ]]
            wj_id = [i.split('<')[0] for i in a.split('<strong class="player-name">')[1 : ]]
            wj_cz_0 = [i.split('</td>')[0] for i in a.split('<td class="pic-s"')[1 : ]]
            wj_cz = [[] for i in xrange(10)]
            n = 0
            for i in wj_cz_0:
                for ii in [iii.split(' ')[0] for iii in i.split('title="')[1 : ]]:
                    wj_cz[n].append(ii)
                n += 1
            time = [i.replace('\n', '') for i in (time_0 + time_1).split(' ') if i ][1 : ]
            s.zj_dir[s.zjx_now] = [wj_rt, wj_gd, wj_name, wj_id, wj_cz, time]
            open(mypath + 'zj.save', 'w').write('s.zj_dir=' + repr(s.zj_dir))
        else : 
            wj_rt, wj_gd, wj_name, wj_id, wj_cz, time = s.zj_dir[s.zjx_now]
        list_y = [50, 80, 80, 80, 600, 0]
        list_x = [30, 30, 0]
        for i in xrange(len(wj_id)):
            if i == (len(wj_id) / 2) : 
                list_x.insert(2, 20)
            list_x.insert(2, 60)
        zjxx_x = zjxx_y = 0
        for i in list_y:
            zjxx_x += i
        for i in list_x:
            zjxx_y += i
        s.img = new((zjxx_x, zjxx_y))
        s.img.blit(s.img_z)
        s.img.blit(s.img_z, ( - (240 + (80 * orientation)), 0))
        s.img.blit(s.img_z, ((( - (240 + (80 * orientation))) * 2), 0))
        s.img.blit(s.img_z, ((( - (240 + (80 * orientation))) * 3), 0))
        color = color_line
        y = 0
        for n in xrange(len(list_x)):
            s.img.line((0, y, zjxx_x, y), color, width = 1)
            y += list_x[n]
            if n in xrange((3 + (len(wj_id) / 2)), (3 + len(wj_id))) or n in xrange(2, (2 + (len(wj_id) / 2))) : 
                if n in xrange((3 + (len(wj_id) / 2)), (3 + len(wj_id))) : 
                    n -= 1
                s.img.text((51, (y - 33)), cn(wj_id[(n - 2)]), f_color, font = ('title', 13))
                if name == wj_id[(n - 2)] : 
                    s.img.line((0, (y - 1), zjxx_x, (y - 1)), color, width = 1)
                    s.img.line((0, (y - 59), zjxx_x, (y - 59)), color, width = 1)
                s.img.text((51, (y - 13)), cn(wj_name[(n - 2)]), f_color, font = ('title', 13))
                try :
                    na = s.get_name(wj_name[(n - 2)])
                    s.img_t.blit(s.img_t_all, (people[na], 0))
                except :
                    s.img_t.clear(0)
                s.img.blit(s.img_t.resize((40, 40)), (-5, ( - y + 49)))
                for i in xrange(len(wj_cz[(n - 2)])):
                    try :
                        na = s.get_name(wj_cz[(n - 2)][i].split('（')[0].split('—')[0])
                        x_zb = weapons[na]
                        s.img_t.blit(s.img_zb, (x_zb, 0))
                    except :
                        s.img_t.clear(0)
                    x2 = ((i % 3) * 25)
                    y2 = ((i / 3) * 25)
                    s.img.blit(s.img_t.resize((23, 23)), ((-134 - x2), ( - y + 53 - y2)))
                s.img.text(((62 + list_y[1]) + list_y[2], (y - 33)), cn('杀 死 助'), f_color, font = ('title', 14))
                s.img.text(((62 + list_y[1]) + list_y[2], (y - 13)), cn(wj_rt[(n - 2)]), f_color, font = ('title', 13))
                for i in xrange(len(wj_gd[(n - 2)])):
                    px = ((i / 3) * 100)
                    py = ((i % 3) * 20)
                    s.img.text(((62 + list_y[1]) + list_y[2] + list_y[3] + px, (y - 43) + py), cn(wj_gd_[i] + wj_gd[(n - 2)][i]), f_color, font = ('title', 13))
                pass
        x = 0
        list_y_text = ['', '名称', '出装', '人头', '更多', '']
        for n in xrange(len(list_y)):
            s.img.line((x, 30, x, zjxx_y), color, width = 1)
            x += list_y[n]
            s.img.text((((x - (list_y[n] / 2)) - 16), 53), cn(list_y_text[n]), f_color, font = ('title', 15))
        sf = ['胜利', '失败'][(wj_id.index(name) / 5)]
        if sf == '胜利' : 
            c = (99, 190, 16)
        else : 
            c = (210, 60, 60)
        s.img.text((0, 23), cn('　　' + sf), c, font = ('title', 15))
        s.img.text((0, 23), cn(('　　　　　　%s　%s　%s %s' % (time[0], time[1], time[2], time[3]))), f_color, font = ('title', 15))
        s.run = 0
        s.zjx_t = 1
        appuifw.app.exit_key_handler = lambda  :  s.zjxx(po) 
        s.redraw(())




    def menu(s, k = 0):
        if k : 
            s.img = new(s.img_menu_hc.size)
            s.img.blit(s.img_menu_hc)
            return None
        if s.run or s.whil or s.yxbj_ or s.zb or s.men or s.zm or s.zbtj or s.tfzt == 2 or s.tx : 
            return None
        s.run = 1
        s.men = 1
        if  not (s.men_2) : 
            s.menu_pos = 0
        else : 
            s.men_2 = 0
        s.timer.cancel()
        if s.tfzt == 1 : 
            appuifw.app.exit_key_handler = s.ret
            s.menu_list = [cn('天赋模拟')]
        elif s.ne or s.zjx : 
            appuifw.app.exit_key_handler = lambda  :  s.pos_popup(1) 
            s.menu_list = [cn('第一页'), cn('第二页'), cn('第三页')]
        elif s.diy : 
            appuifw.app.exit_key_handler = s.red
            s.menu_list = [cn('取消修改')]
        elif s.zc : 
            s.y4 = s.y
            appuifw.app.exit_key_handler = s.rec
            s.menu_list = [cn('安装资料'), cn('进入官网'), cn('软件设置'), cn('检查更新'), cn('查看帮助'), cn('关于软件')]
            s.menu_list.insert((6 * s.zz), cn('资助作者'))
        elif s.tfzt == 3 : 
            appuifw.app.exit_key_handler = s.retfmn
            if s.one : 
                s.menu_list = [cn('重新加点')]
            else : 
                s.menu_list = [cn('打野　►'), cn('ADC 　►'), cn('法师　►'), cn('上单　►'), cn('辅助　►'), cn('重新加点')]
            pass
        elif s.fwmnz : 
            appuifw.app.exit_key_handler = s.rem
            s.menu_list = [cn('选择印记'), cn('选择符印'), cn('选择雕纹'), cn('选择精华'), cn('清空符文')]
        elif s.wp : 
            appuifw.app.exit_key_handler = s.rew
            s.menu_list = [cn('消耗品'), cn('攻击　►'), cn('魔法　►'), cn('防御　►'), cn('移动速度'), cn('S3新物品'), cn('全部物品')]
        elif  not (s.fw and s.fwmn) : 
            appuifw.app.exit_key_handler = s.ref
            s.menu_list = [cn('印记'), cn('符印'), cn('雕纹'), cn('精华'), cn('符文模拟')]
        elif s.zy : 
            appuifw.app.exit_key_handler = s.can
            s.menu_list = [cn('分类　►'), cn('收藏　►'), cn('查找英雄'), cn('对比英雄')]
            if s.bj : 
                s.menu_list.pop(3)
            appuifw.app.exit_key_handler = s.can
        elif s.one : 
            s.path_sound = (mypath2+'%s.mp3' % s.name_list[(((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)])
            s.menu_list = [cn('跳转　►')]
            if os.path.isfile(s.path_sound) : 
                s.menu_list.append(cn('音效　►'))
            if s.pos_zb(1) : 
                s.menu_list.append(cn('装备统计'))
            s.menu_list.append(cn('英雄背景'))
            if  not (s.menu_list) : 
                s.run = 0
                s.men = 0
                return None
            if s.pos_jn(1) : 
                appuifw.app.exit_key_handler = s.pos_jn
            else : 
                appuifw.app.exit_key_handler = s.rey
            pass
        else : 
            s.run = 0
            s.men = 0
            return None
        s.img_menu = new((85, ((len(s.menu_list) * 20) + 10)))
        s.img_menu.blit(s.img_z)
        s.img_menu.polygon(s.rim(0, 0, 85, ((len(s.menu_list) * 20) + 10)), color_frame, width = 1)
        o = 0
        a = 1
        for i in s.menu_list:
            s.img_menu.text((7, (22 + o)), cn(('%d.' % a)) + i, f_color, font = ('title', 14))
            a += 1
            o += 20
        ymenu = ((300 - (80 * orientation)) + s.y - (len(s.menu_list) * 20))
        if  not (s.zc and cd_bg) : 
            ymenu -= 20
        s.img.blit(s.img_menu, (-7,  - ymenu))
        s.img_menu_hc = new(s.img.size)
        s.img_menu_hc.blit(s.img)
        s.pos_menu(0)
        s.run = 0




    def menu_2(s, k = 0):
        if k : 
            s.img = new(s.img_menu_2_hc.size)
            s.img.blit(s.img_menu_2_hc)
            return None
        if s.run : 
            return None
        aa = s.menu_list[s.menu_pos]
        if aa[-1] != cn('►') : 
            return None
        s.menu_len = len(s.menu_list)
        s.run = 1
        s.men_2 = 1
        s.menu_pos_2 = 0
        if aa.find(cn('分类')) != -1 : 
            s.menu_list = [cn('本周免费'), cn('法　　师'), cn('战　　士'), cn('后　　期'), cn('坦　　克'), cn('辅　　助'), cn('隐　　身'), cn('无 蓝 条'), cn('全部英雄')]
        if aa.find(cn('音效')) != -1 : 
            list_all = os.listdir(mypath2+'')
            na = s.name_list[(((s.pos[1] - 1) * (3 + orientation)) + s.pos[0] - 1)]
            s.list_sound = [i for i in list_all if i.find('.mp3') != -1 and i.find(na) != -1 ]
            s.menu_list = []
            for i in xrange(len(s.list_sound)):
                s.menu_list.append(cn(('音效_%s' % (i + 1))))
            pass
        elif aa.find(cn('收藏')) != -1 : 
            s.menu_list = [cn('收藏列表'), cn('修改列表')]
        elif aa.find(cn('跳转')) != -1 : 
            s.menu_list = [cn('页首'), cn('详细信息'), cn('技能'), cn('技巧'), cn('推荐装备'), cn('贴士')]
        elif aa.find(cn('魔法')) != -1 : 
            s.menu_list = [cn('法术强度'), cn('法力上限'), cn('法力回复'), cn('技能冷却'), cn('法术吸血'), cn('法术穿透')]
        elif aa.find(cn('攻击')) != -1 : 
            s.menu_list = [cn('攻击力'), cn('攻击速度'), cn('生命偷取'), cn('暴击几率'), cn('护甲穿透')]
        elif aa.find(cn('防御')) != -1 : 
            s.menu_list = [cn('生命上限'), cn('生命回复'), cn('物理护甲'), cn('魔法抵抗')]
        elif aa.find(cn('法师')) != -1 : 
            s.menu_list = [cn('有蓝'), cn('无蓝')]
        elif aa.find(cn('上单')) != -1 : 
            s.menu_list = [cn('半肉'), cn('坦克'), cn('输出为主'), cn('魔法输出')]
        elif aa.find(cn('ADC')) != -1 : 
            s.menu_list = [cn('压制型'), cn('常用技能')]
        elif aa.find(cn('辅助')) != -1 : 
            s.menu_list = [cn('技能远程'), cn('攻守远程'), cn('耐打近战')]
        elif aa.find(cn('打野')) != -1 : 
            s.menu_list = [cn('传统'), cn('AD_1'), cn('AD_2'), cn('AP技能'), cn('打野坦克'), cn('打野新手')]
        s.img_menu_2 = new((85, ((len(s.menu_list) * 20) + 10)))
        s.img_menu_2.blit(s.img_z)
        s.img_menu_2.polygon(s.rim(0, 0, 85, ((len(s.menu_list) * 20) + 10)), color_frame, width = 1)
        o = 0
        a = 1
        for i in s.menu_list:
            s.img_menu_2.text((7, (22 + o)), (cn('%d.') % a) + i, f_color, font = ('title', 14))
            a += 1
            o += 20
        yy = ((302 - (s.menu_len * 20)) - (80 * orientation)) + s.y + (s.menu_pos * 20)
        y2 = ((300 - (80 * orientation)) + s.y - (len(s.menu_list) * 20))
        if yy > y2 : 
            yy = y2
        s.img.blit(s.img_menu_2, (-75,  - yy))
        s.img_menu_2_hc = new(s.img.size)
        s.img_menu_2_hc.blit(s.img)
        s.pos_menu(0)
        s.run = 0




    def geturl(s, url, n = 0):
        global acp
        import httplib
        try :
            if acp == -1 : 
                acp = s.socket.access_points()[0]['iapid']
            sock = s.socket.access_point(acp)
            s.socket.set_default_access_point(sock)
            sock.start()
            if move_mobile : 
                t = '10.0.0.172'
            elif url.find('lol.178.com') != -1 : 
                t = 'lol.178.com'
            elif url.find('lol.qq.com') != -1 : 
                t = 'lol.qq.com'
            elif url.find('lolbox.4vx.cn') != -1 : 
                t = 'lolbox.4vx.cn'
            elif url.find('lolbox.duowan.com') != -1 : 
                t = 'lolbox.duowan.com'
            for h in xrange(2):
                conn = httplib.HTTPConnection(t)
                conn.request('GET', url, headers = {'X-Requested-With' : 'XMLHttpRequest', 'Accept-Encoding' : 'gzip', 'Content-Type' : 'application/x-www-form-urlencoded', 'Accept' : 'text/vnd.wap.wml,text/html,text/plain,image/*,*/*'})
                r = conn.getresponse()
                header_gzip = r.getheader('Content-Encoding') == 'gzip'
                if header_gzip : 
                    s.wit_2(1)
                else : 
                    s.wit_2(2)
                data = r.read()
                conn.close()
                if header_gzip : 
                    gzipper = s.gzip.GzipFile(fileobj = s.StringIO.StringIO(data))
                    data = gzipper.read()
                    gzipper.close()
                s.wit_2(0)
                e32.ao_yield()
                if data.find('charset=gb2312') != -1 : 
                    data = data.decode('gbk').encode('u8')
                open('d:\\0.html', 'w').write(data)
                if header_gzip or len(data) > 2000 : 
                    break
        except :
            return ''
        return data
        




    def r(s):
        if __name__ != '__main__' : 
            s.fz(s.fz_txt)
        else : 
            if s.ua == 0 : 
                appuifw.app.body = ua
            else : 
                appuifw.app.body = s.m
            s.ua =  not (s.ua)
            appuifw.app.body.bind(63586, s.r)




    def rec(s, k = 0, r = 0):
        if  not (s.run and k) : 
            return None
        if s.na : 
            s.na.focus(0)
            s.na.visible(0)
            s.na = 0
        if s.db : 
            s.db = 0
            return s.redraw(())
        s.y = s.y4
        s.zc = 1
        s.hel = s.zy = s.zjx = s.ne = s.h_zz = s.zzz = s.wp_pos = s.wp = s.fw = s.tfzt = s.zh = s.men = s.men_2 = s.zm = s.one = s.zj = s.tfzt = s.h_zj = s.h_tf = s.tx = s.wp = s.wp_pos = s.fw = s.fw_pos = s.zm = s.jn_s = s.mh = s.x = s.x_ = s.team = 0
        appuifw.app.exit_key_handler = s.exit
        appuifw.app.menu_key_handler = s.menu
        if r : 
            s.zcd(n = 300)
        else : 
            s.pos_zcd()
        s.run = 0




    def rew(s):
        if s.run : 
            return None
        s.y_one = 0
        s.run = 1
        s.men = s.men_2 = 0
        s.zb = 0
        s.wpzl(1)
        s.pos_wp()
        s.redraw(())
        appuifw.app.exit_key_handler = s.rec
        s.wp = 1
        s.run = 0




    def ref(s):
        if s.run : 
            return None
        s.run = 1
        s.y_one = 0
        s.men = s.men_2 = 0
        appuifw.app.exit_key_handler = s.rec
        s.rune = 0
        s.fwzl(1)
        s.pos_fw()
        s.redraw(())
        s.fwmn = 0
        s.fw = 1
        s.run = 0




    def rey(s):
        if s.run : 
            return None
        s.zb = s.y_one = s.diy = s.jnxx = s.men = s.men_2 = s.zbtj = 0
        s.pos_zb()
        appuifw.app.exit_key_handler = s.reu




    def reo(s, k = 0):
        if k : 
            s.y = s.y6
        s.one = 1
        s.yxbj_ = 0
        s.out(0, 1)
        s.redraw(())
        s.men = s.tfzt = 0




    def rem(s):
        if s.run : 
            return None
        s.fw_mn(1)
        s.men = 0
        appuifw.app.exit_key_handler = s.ref




    def ret(s):
        s.men = 0
        if s.tfzt == 3 : 
            s.tfzt = 1
            s.tfzl()
        else : 
            s.pos_tf()
        s.tfzt = 1
        appuifw.app.exit_key_handler = s.rec




    def retfmn(s):
        s.men = s.men_2 = 0
        s.tfzt = 3
        s.pos_tf()




    def red(s):
        s.men = s.men_2 = 0
        appuifw.app.exit_key_handler = lambda  :  s.reu() 
        s.pos_Diy()




    def reu(s, k = 0):
        if  not (s.run and k) : 
            return None
        try :
            s.audio.stop()
        except :
            pass
        if s.one : 
            s.y = s.y5
        elif s.diy : 
            s.y = s.y_diy
        else : 
            s.y = s.y6
        s.one = s.diy = s.zj = s.jn_pos = s.zb_pos = s.tfzt = s.h_zj = s.h_tf = s.tx = s.wp = s.wp_pos = s.fw = s.fw_pos = s.men = s.zm = s.jn_s = 0
        s.zy = 1
        s.pos_yx()
        s.redraw(())
        appuifw.app.menu_key_handler = s.menu
        appuifw.app.exit_key_handler = s.rec
        e32.ao_yield()




    def can_popup(s):
        s.popup = None




    def can_get(s, n = 0):
        s.get.focus(0)
        s.get.visible(0)
        appuifw.app.menu_key_handler = s.menu
        if n : 
            s.pos_wp()
        else : 
            s.pos_yx()
        appuifw.app.exit_key_handler = s.rec




    def can(s):
        try :
            s.zip.close()
        except :
            pass
        s.wp = s.wp_pos = s.men_2 = s.men = s.zm = s.zh = 0
        s.zy = 1
        s.pos_yx()
        s.redraw(())
        appuifw.app.menu_key_handler = s.menu
        if s.bj : 
            appuifw.app.exit_key_handler = lambda  :  s.zui(r = 1) 
        else : 
            appuifw.app.exit_key_handler = s.rec
        s.run = 0




    def exit(s):
        if s.run : 
            return None
        if  not (qu) : 
            return s.ok()
        s.y4 = s.y
        s.run = 1
        s.img_exit = new(((240 + (80 * orientation)), 110))
        s.img_exit.blit(s.img_z, (0, (210 + s.y)))
        s.img_exit.polygon(s.rim(0, 0, (240 + (80 * orientation)), 110), color_frame, width = 1)
        s.img.blit(s.img_exit, (0, (-206 - s.y) + (80 * orientation)))
        s.img.text((12, ((s.y + 233) - (80 * orientation))), cn('确定退出?'), f_color, font = ('title', 16))
        s.img.text(((75 + (80 * orientation)), ((s.y + 265) - (80 * orientation))), cn('英雄联盟控 for s60v3'), f_color, font = ('title', 15))
        s.img.text(((192 + (80 * orientation)), ((s.y + 285) - (80 * orientation))), cn(('v%s' % version)), f_color, font = ('title', 15))
        s.img.blit(s.img_ztl, (0, ((-295 + (80 * orientation)) - s.y)))
        s.img.text((10, ((s.y + 315) - (80 * orientation))), cn('确定'), (230, 230, 230), font = ('title', 14))
        s.img.text(((203 + (80 * orientation)), ((s.y + 315) - (80 * orientation))), cn('取消'), (230, 230, 230), font = ('title', 14))
        s.redraw(())
        appuifw.app.menu_key_handler = s.ok
        appuifw.app.exit_key_handler = lambda  :  s.rec(1) 




    def data(s):
        import zipfile
        if  not (os.path.isfile('e:\\1.zip')) : 
            s.img_up.text((1, 160), cn('未检测到安装包'), f_color, font = ('title', 14))
            s.img_up.text((1, 180), cn('请返回并按要求操作'), f_color, font = ('title', 14))
            s.img_up.text((10, 317), cn('——'), f_color, font = ('title', 14))
            s.img.blit(s.img_up, (0,  - s.y))
            s.redraw(())
            appuifw.app.menu_key_handler = None
            s.run = 0
            return None
        try :
            s.zip = zipfile.ZipFile('e:\\1.zip')
            for k in s.zip.namelist():
                if k.find(' up') != -1 : 
                    t = s.zip.read(k)
                    s.upv = k.split(' ')[0]
                    s.vlist = t.split(',')
                    break
            s.img_up.text((1, 160), cn(('检测到安装包 版本:v%s' % s.upv)), f_color, font = ('title', 14))
            s.img_up.text((1, 180), cn('是否立即升级?'), f_color, font = ('title', 14))
            s.run = 1
            s.img.blit(s.img_up, (0,  - s.y))
            s.redraw(())
            appuifw.app.menu_key_handler = lambda  :  s.ok(1) 
        except :
            appuifw.app.menu_key_handler = None
            s.img_up.text((1, 160), cn('安装包错误,请重新下载'), f_color, font = ('title', 14))
            s.img_up.text((10, 317), cn('——'), f_color, font = ('title', 14))
            s.img.blit(s.img_up, (0,  - s.y))
            s.redraw(())




    def ok(s, k = 0):
        if k == 1 : 
            s.run = 1
            try :
                if version not in s.vlist : 
                    s.img_up.text((1, 200), cn('安装失败'), s.f_color, font = ('title', 14))
                    s.img_up.text((1, 220), cn(('此安装包不适合v%s版' % version)), s.f_color, font = ('title', 14))
                    s.img_up.text((1, 240), cn('请在官网下载完整软件'), s.f_color, font = ('title', 14))
                    s.img_up.text((10, 317), cn('——'), s.f_color, font = ('title', 14))
                    s.img.blit(s.img_up, (0,  - s.y))
                    s.redraw(())
                    appuifw.app.menu_key_handler = None
                    appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
                    return None
                s.img_up.text((1, 200), cn('正在安装,请稍后…'), s.f_color, font = ('title', 14))
                appuifw.app.menu_key_handler = None
                s.img.blit(s.img_up, (0,  - s.y))
                s.redraw(())
                e32.ao_yield()
                appuifw.app.exit_key_handler = pass_
                for k in s.zip.namelist():
                    if k.find(' up') == -1 : 
                        if k.find('00.') != -1 : 
                            try :
                                os.makedirs(mypath2+'txt\\')
                            except :
                                pass
                            try :
                                os.makedirs(mypath2+'lom\\')
                            except :
                                pass
                            try :
                                jname = os.listdir(mypath2+'txt\\')[0]
                                if jname.find('00.') != -1 : 
                                    os.remove(mypath2+'txt\\' + jname)
                            except :
                                pass
                            pass
                        (open('e:/data/' + k, 'w')).write(s.zip.read(k))
                        e32.ao_yield()
                appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
                s.zip.close()
                s.img_up.text((1, 220), cn(('安装成功,已更新到v%s' % s.upv)), s.f_color, font = ('title', 14))
                s.img_up.text((1, 240), cn('重启软件后生效'), s.f_color, font = ('title', 14))
                s.img_up.text((10, 317), cn('——'), s.f_color, font = ('title', 14))
                s.img.blit(s.img_up, (0,  - s.y))
                s.redraw(())
            except :
                s.img_up.text((1, 200), cn('安装失败,未知错误'), s.f_color, font = ('title', 14))
                s.img_up.text((1, 220), cn('请到官网下载完整软件'), s.f_color, font = ('title', 14))
                s.img.blit(s.img_up, (0,  - s.y))
                appuifw.app.menu_key_handler = None
                appuifw.app.exit_key_handler = lambda  :  s.rec(1) 
                s.redraw(())
            pass
        elif k == 2 : 
            s.finds = s.get.get()
            if  not (s.finds) : 
                return s.can_get()
            n = 0
            for ii in xrange(len(s.name_list)):
                if cn(s.name_list[ii]).find(s.finds) != -1 : 
                    n = 1
                    break
            if  not (n) : 
                s.run = s.fin = 0
                return s.can_get()
            ii += 1
            x1 = (ii % (3 + s.orientation))
            if  not (x1) : 
                x1 = (3 + s.orientation)
                y1 = (ii / (3 + s.orientation))
            else : 
                y1 = ((ii / (3 + s.orientation)) + 1)
            y2 = (s.y / 79)
            s.pos = [x1, y1]
            if y1 > ((y2 + 4) - s.orientation) : 
                s.y = (79 * (y1 - 5) + s.orientation)
            elif y1 < y2 : 
                s.y = (79 * y1)
            if s.y > (((s.h_yx - 4) + s.orientation) * 79) : 
                s.y = (((s.h_yx - 4) + s.orientation) * 79)
            s.can_get()
        elif k == 3 : 
            s.open_uc(1)
        elif k == 4 : 
            s.finds = s.get.get()
            if  not (s.finds) : 
                return s.can_get(1)
            n = 0
            for ii in xrange(len(s.nlist)):
                if s.nlist[ii].find(s.finds) != -1 : 
                    n = 1
                    break
            if  not (n) : 
                s.run = s.fin = 0
                return s.can_get(1)
            y1 = ii
            y2 = (s.y / 79)
            if (y2 + 4) < y1 : 
                s.y = (79 * ((y1 / 3) - 3))
            elif y2 > y1 : 
                s.y = (79 * (y1 / 3))
            s.wp_pos = y1
            if s.y > (s.h_wp * 79) : 
                s.y = (s.h_wp * 79)
            s.can_get(1)
        else : 
            s.run = 2
            v = 8
            x = 98.01
            for i in xrange(25):
                s.redraw((), x)
                x -= v
                v -= 0.34
                e32.ao_yield()
            e32.ao_sleep(0.05)
            import os
            appuifw.app.set_exit()
            os.abort()




    def popup_menu(s, k, na, n = 0, o = 0, m = 0, pos = None):
        if n : 
            s.img.blit(s.img_popup_hc)
            return None
        if m : 
            s.y6 = s.y
        s.len_txt = len(k)
        if  not (k) : 
            k = [cn('空列表  请立即返回')]
        s.popup_list = k
        if s.ne or s.zjx : 
            appuifw.app.menu_key_handler = s.menu
        else : 
            appuifw.app.menu_key_handler = pass_
        appuifw.app.exit_key_handler = s.can_popup
        ms = (s.popup_list[0].find('|') != -1 + 1)
        y = (((s.len_txt * 20) * ms) + 40)
        if y < s.img.size[1] : 
            y = s.img.size[1]
        s.img = new(((240 + (80 * orientation)), y))
        s.img.blit(s.img_z)
        s.img.text((7, (20 - 2)), na, f_color, font = ('title', 14))
        n = 0
        s.popup = ''
        s.y = s.x = 0
        if o : 
            s.popup_pos = s.popup_pos_2
        else : 
            s.popup_pos = 0
        if pos != None : 
            s.popup_pos = pos
        s.popup_zt = 1
        for i in k:
            if i.find('|') != -1 : 
                ms = 2
                cccc, i, p = i.split('|')
                name, sf = cccc.split(' ')
                na = s.get_name(en(name))
                try :
                    s.img_t.blit(s.img_t_all, (people[na], 0))
                except :
                    s.img_t.clear(0)
                s.img.blit(s.img_t.resize((34, 34)), (-3, (( - n * 40) - 24)), mask = s.img_t_mask.resize((34, 34)))
                if sf == cn('胜利') : 
                    c = (99, 190, 16)
                else : 
                    c = (210, 60, 60)
                s.img.text((47, (((n * 40) - 2) + 40)), sf, c, font = ('title', 14))
            else : 
                ms = 1
            s.img.text(((7 + ((ms - 1) * 40)), ((((n * 20) * ms) - 2) + 20) + (20 * ms)), i, f_color, font = ('title', 14))
            n += 1
        s.img_popup_hc = new(s.img.size)
        s.img_popup_hc.blit(s.img)
        s.run = 0
        s.pos_popup()
        while s.popup == '' : 
            e32.ao_sleep(0)
        s.popup_zt = 0
        if m : 
            s.y = s.y6
        return s.popup




#print('box2')


class MyError :


    __module__ = __name__
    def __init__(s, path = 'e:\\error.txt'):
        s._MyError__flag = 0
        s._MyError__path = path




    def write(s, text):
        if  not (s._MyError__flag) : 
            s._MyError__flag = 1
            fp = open(s._MyError__path, 'w')
            fp.write(text)
            fp.close()
        else : 
            fp = open(s._MyError__path, 'a')
            fp.write(text)
            fp.close()
        appuifw.note(cn('软件出错,错误信息已保存到e:\error.txt,请通知作者。'), 'error', 1)
        appuifw.app.exit_key_handler = None




if __name__ == '__main__' : 
    sys.stderr = MyError()
#print('hello1')
b=box()
#print('box inited')
b.zcd(n = 300)
#print('hello2')
