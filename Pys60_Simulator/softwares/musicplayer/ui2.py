# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import appuifw as ui
#import keypress
import time
import random
import sysinfo
import graphics
def cn(x):
    return x.decode('u8')




def en(x):
    return x.encode('u8')




class Timecancel :
    __module__ = __name__




def after(t = 0):
    if t < 0.01 : 
        t = 0.01
    Timecancel.t = (t * 100)
    del t
    while True : 
        Timecancel.t = (Timecancel.t - 1)
        if Timecancel.t <= 0 : 
            break
        ui.e32.ao_sleep(0.001)




def cancel():
    Timecancel.t = 0




def split_text(txt, ziti, number = 0):
    try :
        txt = txt.decode('u8')
    except :
        pass
    if number == 0 : 
        return graphics.screenshot().measure_text((u'%s' % txt), ('dense', ziti))[1]
    elif number == 1 : 
        return int(str(graphics.screenshot().measure_text(u'11', ('dense', 16))[0][1])[1 : ])
    else : 
        return [graphics.screenshot().measure_text((u'%s' % txt), ('dense', ziti))[1], int(str(graphics.screenshot().measure_text(u'11', ('dense', 16))[0][1])[1 : ])]




def Mask_color(img, color = 16711935):
    mask = graphics.Image.new(img.size, 'L')
    mask.clear(color)
    return mask




def Mask(img, moshi = '1'):
    width, height = img.size
    mask = graphics.Image.new(img.size, moshi)
    color = img.getpixel((0, 0))[0]
    for y in range(height):
        line = img.getpixel([(x, y) for x in range(width)])
        for x in range(width):
            if line[x] == color : 
                mask.point((x, y), 16711935)
            del x
        del y
        del line
    del width
    del height
    del color
    return mask




class Listbox(object, ) :


    __module__ = __name__
    def __init__(self, path1, path2, color = [(255, 255, 255), (100, 255, 50), (255, 0, 0)], title_tag = 0, menu_tag = 0, cursor_tag = 0):
        if ui.e32.s60_version_info >= (3, 0) : 
            self.ziti = u'Sans MT 936_s60'
        else : 
            self.ziti = u'CombinedChinesePlain12'
        ui.app.screen = 'full'
        self.img = None
        img = graphics.Image.open(cn(path2))
        ui.app.body = canvas = ui.Canvas(event_callback = self.keyft, redraw_callback = self.draw)
        self.x, self.y = canvas.size
        self.blit = canvas.blit
        self.blit(img)
        self.img = graphics.Image.new((self.x, self.y))
        self.gg2 = 0
        self.gg1 = self.x
        self.skin(cn(path1), color, title_tag, menu_tag, cursor_tag)




    def skin(self, path, color, title_tag, menu_tag, cursor_tag):
        self.path = path
        self.color = color
        a = graphics.Image.new((self.x, 25))
        a.clear(title_tag)
        b = graphics.Image.new((self.x, 50))
        b.clear(title_tag)
        app.img1 = []
        self.img1 = [[graphics.Image.open(self.path)], [b, Mask_color(b, 6645093)], [a, Mask_color(a, 6645093)]]
        del a
        del b
        a = graphics.Image.new((self.x, (self.y - 75)))
        a.clear(menu_tag)
        app.img1 = [a, Mask_color(a)]
        a = graphics.Image.new((231, 40))
        a.clear(cursor_tag)
        self.guangbiao = [a, Mask_color(a)]
        del a




    def Listbox(self, list1 = [], list2 = None, bt = '软件标题', gg = [('流动1' * 20), ('流动2' * 20)], run = True):
        app.rolling['界面'] = [random.choice([self.x,  - self.x, 0]), random.choice([self.y,  - self.y, 0])]
        try :
            self.a1 = map(cn, list1)
        except :
            self.a1 = list1
        self.a2 = list2
        self.mode = self.mode1 = self.mode2 = self.gb1 = self.gb2 = self.gb3 = self.b1 = self.b2 = 0
        self.txt = []
        self.gb4 = [0, (self.y / 3)]
        self.gb5 = []
        self.bt = bt
        self.xx = 5
        self.gg = gg
        self.gb_yidong = 0
        self.run = run
        app.yy = split_text(self.gg[self.gg2], 14)
        self.menu_changdu = []
        self.menu_changdu1 = []
        ui.app.exit_key_handler = lambda  : None 
        self.menu()




    def Listbox_new(self, list1, list2 = None, number = None):
        try :
            self.a1 = map(cn, list1)
        except :
            self.a1 = list1
        if list2 != None : 
            self.a2 = list2
        if number == None : 
            self.mode = self.mode1 = self.mode2 = self.gb1 = self.gb2 = self.gb3 = self.b1 = self.b2 = self.gb_yidong = app.liudong = 0
            self.xx = 5
            self.menu_changdu = []
            self.menu_changdu1 = []
        else : 
            self.mode = self.mode1 = self.mode2 = self.gb2 = self.gb3 = app.liudong = 0
            self.xx = 5
            self.menu_changdu = []
            self.menu_changdu1 = []




    def Listbox_set(self, number):
        self.gb1 = number
        self.b2 = 0
        self.b1 = (self.gb1 - self.b2)
        if self.gb1 < 0 : 
            self.gb1 = -1
            self.b1 = 0
            self.b2 = 0
        elif self.gb1 > (len(self.a1) - 1) : 
            self.gb1 = (len(self.a1) - 1)
            self.b2 = 4
            self.b1 = (self.gb1 - self.b2)




    def bind(self, number, hanshu):
        if number == 63586 : 
            app.key['拨号'] = hanshu
        elif number == 8 : 
            app.key['删除'] = hanshu
        elif number == 63495 : 
            app.key['左'] = hanshu
        elif number == 63496 : 
            app.key['右'] = hanshu
        elif number == 49 : 
            app.key['1'] = hanshu
        elif number == 50 : 
            app.key['2'] = hanshu
        elif number == 51 : 
            app.key['3'] = hanshu
        elif number == 52 : 
            app.key['4'] = hanshu
        elif number == 53 : 
            app.key['5'] = hanshu
        elif number == 54 : 
            app.key['6'] = hanshu
        elif number == 55 : 
            app.key['7'] = hanshu
        elif number == 56 : 
            app.key['8'] = hanshu
        elif number == 57 : 
            app.key['9'] = hanshu
        elif number == 42 : 
            app.key['*'] = hanshu
        elif number == 35 : 
            app.key['#'] = hanshu




    def info(self, list):
        try :
            list = map(cn, list)
            list = map(en, list)
        except :
            list = map(en, list)
        if list != app.info : 
            app.info_liudong = 0
        app.info = list
        app.info_color = 255
        app.info_xy = 0




    def up_txt(self, list):
        try :
            list = map(cn, list)
            list = map(en, list)
        except :
            list = map(en, list)
        self.gg = list
        self.gg1 = 75
        self.gg2 = 0




    def up_txt_return(self):
        return (self.gg, self.gg1, self.gg2)




    def title(self, name = None):
        if name != None : 
            self.bt = name




    def close(self):
        self.run = False




    def current(self):
        if self.mode == 0 : 
            return self.gb1




    def Text(self, txt, hong_txt = 0, number = 0):
        if self.txt != [txt, hong_txt] : 
            self.txt = [txt, hong_txt]
            app.txt_changdu = [0, 0, 3, '']
        if number != 0 : 
            self.gb4 = [0, (self.y / 3)]
            self.gb5 = []
            app.txt_changdu = [0, 0]




    def Text_List(self, number = 0):
        self.mode = number
        del number




    def dialog(self, number, name = '正在处理,请稍候…'):
        self.img.rectangle((10, (self.y - 100), (self.x - 10), (self.y - 25)), 2241040, fill = (240, 240, 240))
        self.img.text(((self.x / 6), (self.y - 60)), cn(name), 0, (self.ziti, (app.ziti + 18)))
        self.img.rectangle((20, (self.y - 55), (self.x - 20), (self.y - 40)), 2241040)
        self.img.rectangle((21, (self.y - 54), number, (self.y - 41)), 2241040, fill = 16711762)
        self.blit(self.img)




    def SMS_BEG_START(self, name = '正在扫描文件', name1 = '文件', name2 = '路径', name3 = '数量', color = 0):
        self.mode = -1
        self.img.text((20, 70), cn(name), 0, (self.ziti, (app.ziti + 34)))
        self.img.rectangle((0, 100, self.x, 169), 0, fill = 0)
        self.img.text((5, 122), cn(name1), 16777215, (self.ziti, (app.ziti + 14)))
        self.img.text((5, 144), cn(name2), 16777215, (self.ziti, (app.ziti + 14)))
        self.img.text((5, 166), cn(name3), 16777215, (self.ziti, (app.ziti + 14)))
        self.img.text((20, 200), cn('正在处理，稍候…'), 16777215, (self.ziti, (app.ziti + 24)))
        for i in xrange(8):
            if i == color : 
                col = 0
            else : 
                col = 16777215
            self.img.text(((40 + (i * (app.ziti + 20))), 240), cn('█'), col, (self.ziti, (app.ziti + 20)))
        self.blit(self.img)




    def SMS_BEG_END(self):
        self.mode = 0




    def exit_key_handler(self, hanshu):
        app.exit_key_handler = [hanshu]




    def query(self, txt):
        import akntextutils
        try :
            txt = cn(txt)
        except :
            txt = txt
        app.return_query = None
        app.query = []
        for i in akntextutils.wrap_text_to_array(txt, self.ziti, self.x):
            app.query.append(i)
            del i
        del akntextutils
        while True : 
            if app.return_query != None : 
                return app.return_query
            self.While(1)
            ui.e32.ao_sleep(float(1E-14))




    def note(self, txt, classy = 'note'):
        import akntextutils
        try :
            txt = cn(txt)
        except :
            txt = txt
        list = []
        for i in akntextutils.wrap_text_to_array(txt, self.ziti, self.x):
            list.append(i)
            del i
        if classy == 'note' : 
            app.note = [list, [-50, 50]]
        elif classy == 'info' : 
            app.note = [list, [(self.y / 2), 10]]
        del akntextutils
        del list




    def While(self, number = 0):
        while self.run : 
            if app.note[0] != [] : 
                app.note[1][0] += 10
                if app.note[1][0] >= (self.y / 3) and app.note[1][1] > 0 : 
                    app.note[1][0] = (self.y / 3)
                    app.note[1][1] -= 1
                    if app.note[1][1] <= 0 : 
                        app.note[1][1] = 0
                    pass
                elif app.note[1][0] > self.y : 
                    app.note = [[], [0, 0]]
                pass
            if app.switch['电量'] == True : 
                app.battery[1] += 1
                if app.battery[1] > 100 : 
                    app.battery = [sysinfo.battery(), 0]
                pass
            if app.menu != [] : 
                if self.menu_changdu1 == [] : 
                    self.menu_changdu1 = [[] for t in xrange(len(app.menu))]
                ui.app.menu = []
            if self.a1 != [] : 
                if app.liudong < 30 : 
                    if app.liudong == 0 : 
                        app.xx = split_text(self.a1[self.gb1], (app.ziti + 22))
                    app.liudong += 1
                elif self.gb1 != -1 and app.liudong >= 30 : 
                    if self.xx <  - app.xx + self.x : 
                        app.liudong += 1
                        if app.liudong == 60 : 
                            app.liudong = 0
                            self.xx = 5
                        pass
                    else : 
                        self.xx -= 1
                    pass
                pass
            self.gg1 -= 1
            if self.gg1 < ( - app.yy + 75) : 
                self.gg2 += 1
                self.gg1 = self.x
                if self.gg2 > (len(self.gg) - 1) : 
                    self.gg2 = 0
                app.yy = split_text(self.gg[self.gg2], (app.ziti + 14))
            app.info_color += app.info_xx
            if app.info_color > 253 : 
                app.info_liudong = 0
                app.info_xx = -2
            if app.info_color < 2 : 
                app.info_liudong = 0
                app.info_xx = 2
                app.info_xy += 1
                if app.info_xy > (len(app.info) - 1) : 
                    app.info_xy = 0
                pass
            if split_text(app.info[app.info_xy], (app.ziti + 14)) + app.info_liudong > ((self.x - (self.x / 2)) - 10) : 
                app.info_liudong -= 2
            if self.gb5 != [] : 
                for t in xrange((len(self.gb5) - 1)):
                    if self.gb5[t][0] == self.txt[1] : 
                        self.gb4[1] = ((self.y / 3) - (t * 30))
                        break
                    del t
                if self.gb4[0] > self.gb4[1] : 
                    if ( - (self.gb4[1] - self.gb4[0]) / 30) > 2 : 
                        self.gb4[0] = (self.gb4[1] + 60)
                    self.gb4[0] -= 3
                pass
            if self.gb_yidong < 0 : 
                if self.gb_yidong < -1 : 
                    self.b1 += ( - self.gb_yidong - 1)
                    self.gb_yidong = -1
                self.gb_yidong += 0.25
                self.b1 += 0.25
                if self.b2 != (self.gb1 - self.b1) : 
                    self.b2 = (self.gb1 - self.b1)
                    if self.gb1 == -1 : 
                        self.b2 += 1
                    pass
                pass
            if self.gb_yidong > 0 : 
                if self.gb_yidong > 1 : 
                    self.b1 -= (self.gb_yidong - 1)
                    self.gb_yidong = 1
                self.gb_yidong -= 0.25
                self.b1 -= 0.25
                if self.b2 != (self.gb1 - self.b1) : 
                    self.b2 = (self.gb1 - self.b1)
                    if self.gb1 == -1 : 
                        self.b2 += 1
                    pass
                pass
            for t in app.rolling:
                for tt in xrange(len(app.rolling[t])):
                    if app.rolling[t][tt] != 0 : 
                        app.gb_key = False
                        if app.rolling[t][tt] < 0 : 
                            app.rolling[t][tt] += (self.x / 4)
                            if app.rolling[t][tt] >= 0 : 
                                app.rolling[t][tt] = 0
                                app.gb_key = True
                            pass
                        elif app.rolling[t][tt] > 0 : 
                            app.rolling[t][tt] -= (self.x / 4)
                            if app.rolling[t][tt] <= 0 : 
                                app.rolling[t][tt] = 0
                                app.gb_key = True
                            pass
                        pass
            self.menu()
            if number != 0 : 
                break
            if app.e32 == 0 : 
                ui.e32.ao_yield()
            else : 
                ui.e32.ao_sleep(float(1E-22))




    def menu(self):
        self.img.blit(self.img1[0][0])
        if self.mode == 0 : 
            if self.a1 != [] : 
                for i in xrange(-5, 7):
                    if self.gb1 + i >= 0 and self.gb1 + i <= (len(self.a1) - 1) : 
                        if i != 0 : 
                            self.img.text((25, (85 + (((i - self.b1) + self.gb1) * 40))), self.a1[i + self.gb1], self.color[0], (self.ziti, (app.ziti + 15)))
                        pass
                    self.img.line((0, (98 + (i * 40)), (self.x - 6), (98 + (i * 40))), self.color[1])
                if self.gb1 != -1 : 
                    self.img.blit(self.guangbiao[0], target = (3, (58 + (self.b2 * 40))), mask = self.guangbiao[1])
                    if app.xx < self.x : 
                        self.img.text((5, ((85 + (self.gb1 * 40)) - (self.b1 * 40))), self.a1[self.gb1], self.color[2], (self.ziti, (app.ziti + 20)))
                    else : 
                        self.img.text((self.xx, ((85 + (self.gb1 * 40)) - (self.b1 * 40))), self.a1[self.gb1], self.color[2], (self.ziti, (app.ziti + 22)))
                    pass
                self.img.rectangle(((self.x - 3), 48, self.x, (self.y - 23)), self.color[1], fill = self.color[1])
                self.img.line(((self.x - 4), 48, (self.x - 4), (self.y - 23)), self.color[2])
                x_1 = (float(((((self.y - 50) - 25) * 100) / len(self.a1))) / 100)
                self.img.rectangle(((self.x - 3), 50, self.x, (55 + (((self.gb1 + 1)) * x_1))), fill = self.xx)
            else : 
                self.img.text(((self.x / 5), (self.y / 2)), cn('（无项目）'), self.color[0], (self.ziti, (app.ziti + 30)))

            self.zjm(self.bt)
        elif self.mode == 1 : 
            try :
                if self.txt != [] : 
                    if self.gb5 == [] : 
                        for t in self.txt[0]:
                            try :
                                self.gb5.append([t[0], cn(t[1])])
                            except :
                                self.gb5.append(t)
                            del t
                        pass
                    for t1 in xrange(((((self.y / 3) - self.gb4[1]) / 30) - 3), ((((self.y / 3) - self.gb4[1]) / 30) + 7)):
                        if t1 >= 0 and t1 <= (len(self.gb5) - 1) : 
                            color = [self.color[0], (app.ziti + 16)]
                            if self.gb5[t1][0] == self.txt[1] : 
                                self.gb4[1] = ((self.y / 3) - (t1 * 30))
                                color = [self.color[2], (app.ziti + 18)]
                                if app.txt_changdu[3] != self.gb5[t1][1] : 
                                    app.txt_changdu = [split_text(self.gb5[t1][1], (app.ziti + 18)), 0, 3, self.gb5[t1][1]]
                                pass
                            if color[0] == self.color[2] : 
                                if app.txt_changdu[0] + app.txt_changdu[1] > (self.x - 5) : 
                                    app.txt_changdu[1] -= 2
                                self.img.text(((3 + app.txt_changdu[1]), (80 + (t1 * 30)) + self.gb4[0]), self.gb5[t1][1], color[0], (self.ziti, color[1]))
                            else : 
                                self.img.text((13, (80 + (t1 * 30)) + self.gb4[0]), self.gb5[t1][1], color[0], (self.ziti, color[1]))
                            del t1
                    pass
                else : 
                    self.img.text(((self.x / 5), (self.y / 2)), cn('（无内容）'), self.color[0], (self.ziti, (app.ziti + 30)))
            except :
                pass
            self.zjm(self.bt)
        elif self.mode == 2 : 
            try :
                if app.rolling['界面'] == [0, 0] : 
                    try :
                        if app.music['正在播放'][3] < 0 : 
                            app.music['正在播放'][3] += 1
                        if app.music['正在播放'][3] >= 0 : 
                            if app.music['正在播放'][2] > (((self.x - 85) - app.music['正在播放'][1]) - 10) : 
                                app.music['正在播放'][2] -= 1
                            else : 
                                app.music['正在播放'][3] += 1
                                if app.music['正在播放'][3] > 30 : 
                                    app.music['正在播放'][2] = 0
                                    app.music['正在播放'][3] = -30
                                pass
                            pass
                    except :
                        pass
                    if app.keshihua : 
                        self.img.rectangle((5, 50, (self.x - 5), (self.y / 2)), 0, fill = 0)
                        try :
                            if app._B == [] : 
                                app._B.append([random.randint(5, (self.x - 5)), self.y, 1])
                            for tt in xrange(len(app._B)):
                                if len(app._B) < 8 and random.randint(0, 5) == 0 : 
                                    app._B.append([random.randint(5, (self.x - 5)), self.y, 1])
                                self.img.ellipse(((app._B[tt][0] - app._B[tt][2]), (app._B[tt][1] - app._B[tt][2]), app._B[tt][0] + app._B[tt][2], app._B[tt][1] + app._B[tt][2]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                                app._B[tt][2] += 1
                                app._B[tt][1] -= 20
                                if app._B[tt][1] < 0 : 
                                    del app._B[tt]
                        except :
                            pass
                        if app.music['可视化'] == True : 
                            app._A = [[5, ((self.y / 2) - 50)]] + [[random.randint(10, 20) + (i * 20),  + random.randint(60, ((self.y / 2) - 10))] for i in xrange(11)] + [[(self.x - 5), ((self.y / 2) - 50)]]
                        try :
                            if app._A_color[app._A_color[3]] <= 255 : 
                                ran = random.randint(10, 30)
                                if (app._A_color[app._A_color[3]] - ran) >= 0 : 
                                    app._A_color[app._A_color[3]] -= ran
                                else : 
                                    app._A_color[app._A_color[3]] = random.randint(20, 255)
                                    if app._A_color[3] < 2 : 
                                        app._A_color[3] += 1
                                    else : 
                                        app._A_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0]
                                pass
                            for t in xrange((len(app._A) - 1)):
                                self.img.line((app._A[t][0], app._A[t][1], app._A[(t + 1)][0], app._A[(t + 1)][1]), (app._A_color[0], app._A_color[1], app._A_color[2]), width = 4)
                                self.img.line(((app._A[t][0] - 5), (app._A[t][1] + 6), (app._A[(t + 1)][0] + 6), (app._A[(t + 1)][1] - 9)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                                self.img.line(((app._A[t][0] + 8), (app._A[t][1] - 10), (app._A[(t + 1)][0] - 7), (app._A[(t + 1)][1] + 10)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                        except :
                            pass
                        pass
                    self.img.rectangle((10, ((self.y / 2) + 65), (self.x - 10), ((self.y / 2) + 75)), (self.color[0][1], self.color[1][0], self.color[2][1]))
                    prog = ((self.x - 21) * (float(app.music['进度'][0]) / float(app.music['进度'][2])))
                    self.img.rectangle((11, ((self.y / 2) + 66), (11 + prog), ((self.y / 2) + 74)), fill = 16714052)
                    self.img.text(((11 + prog), ((self.y / 2) + 70)), cn('♫'), self.color[1], (self.ziti, 20))
                    self.img.text((5, ((self.y / 2) + 55)), cn(app.music['进度'][1]), self.color[0], (self.ziti, 18))
                    self.img.text(((self.x - 60), ((self.y / 2) + 55)), cn(app.music['进度'][3]), self.color[0], (self.ziti, 18))
                    if app.music['状态'] : 
                        self.img.polygon((((self.x / 2) - 10), ((self.y / 2) + 85), ((self.x / 2) + 10), ((self.y / 2) + 95), ((self.x / 2) - 10), ((self.y / 2) + 105)), fill = self.color[2])
                    else : 
                        self.img.rectangle((((self.x / 2) - 10), ((self.y / 2) + 85), ((self.x / 2) - 1), ((self.y / 2) + 105)), fill = self.color[2])
                        self.img.rectangle((((self.x / 2) + 1), ((self.y / 2) + 85), ((self.x / 2) + 10), ((self.y / 2) + 105)), fill = self.color[2])
                    self.img.text((((self.x / 2) - 90), ((self.y / 2) + 105)), cn('(4)快退'), self.color[0], (self.ziti, 18))
                    self.img.text((((self.x / 2) + 40), ((self.y / 2) + 105)), cn('(6)快进'), self.color[0], (self.ziti, 18))
                    self.img.text((((self.x / 2) - 40), ((self.y / 2) + 130)), cn('(1)暂停/播放'), self.color[0], (self.ziti, 14))
                    self.img.blit(self.img1[0][0], target = (0, 0), source = (0, 0, 5, self.y))
                    self.img.blit(self.img1[0][0], target = ((self.x - 5), 0), source = ((self.x - 5), 0, self.x, self.y))
                    try :
                        self.img.text(((85 + app.music['正在播放'][2]), ((self.y / 2) + 30)), cn(app.music['正在播放'][0]), self.color[2], (self.ziti, 18))
                    except :
                        pass
                    self.img.blit(self.img1[0][0], target = (0, ((self.y / 2) + 5)), source = (0, (self.y / 2), 85, ((self.y / 2) + 30)))
                    self.img.text((5, ((self.y / 2) + 30)), cn('正在播放:'), self.color[0], (self.ziti, 18))
                    if app.keshihua : 
                        self.img.rectangle((5, 50, (self.x - 5), (self.y / 2)), 22307218, width = 3)
                    if  not (app.keshihua) : 
                        self.img.text((5, ((self.y / 2) - 50)), cn('音乐播放'), self.color[2], (self.ziti, 58))
                        self.img.text(((self.x / 2), (self.y / 2)), cn('v1.04版'), self.color[1], (self.ziti, 30))
                    pass
            except :
                pass
            self.zjm(self.bt)




    def zjm(self, bt = '软件标题', cd = '菜单', tc = '退出'):
        if self.mode1 == 1 : 
            if app.switch['阴影'] : 
                self.img.blit(app.img1[0], target = (0, 50), mask = app.img1[1])
            if self.menu_changdu == [] : 
                t = 0
                for t1 in app.menu:
                    if t1[0][-1] != cn('√') or t1[0][-1] != cn('>') : 
                        t2 = split_text(t1[0] + cn(' √'), (app.ziti + 17), 2)
                    else : 
                        t2 = split_text(t1[0], (app.ziti + 17), 2)
                    if t < t2[0] : 
                        t = t2[0]
                    del t1
                t2[1] = (t2[1] + 10)
                self.menu_changdu = [t, t2]
            else : 
                t = self.menu_changdu[0]
                t2 = self.menu_changdu[1]
            self.img.blit(app.img1[0], target = (0, ((self.y - 40) - (len(app.menu) * t2[1]))), source = (0, 0, (t + 20), ((len(app.menu) * t2[1]) + 10)), mask = app.img1[1])
            for i in xrange(len(app.menu)):
                if app.menu[i][0][-1] == cn('√') : 
                    self.img.text((10, ((self.y - 15) - (len(app.menu) * t2[1])) + (i * t2[1])), app.menu[i][0][ : -1], self.color[0], (self.ziti, (app.ziti + 17)))
                    self.img.text((t, ((self.y - 15) - (len(app.menu) * t2[1])) + (i * t2[1])), cn('√'), self.color[0], (self.ziti, (app.ziti + 17)))
                elif app.menu[i][0][-1] == cn('>') : 
                    self.img.text((10, ((self.y - 15) - (len(app.menu) * t2[1])) + (i * t2[1])), app.menu[i][0][ : -1], self.color[0], (self.ziti, (app.ziti + 17)))
                    self.img.polygon((t, (((self.y - 10) - (len(app.menu) * t2[1])) + (i * t2[1]) - t2[1]), (t + 10), (((self.y - 5) - (len(app.menu) * t2[1])) + (i * t2[1]) - t2[1]), t, ((self.y - (len(app.menu) * t2[1])) + (i * t2[1]) - t2[1])), self.color[0], fill = self.color[0])
                else : 
                    self.img.text((10, ((self.y - 15) - (len(app.menu) * t2[1])) + (i * t2[1])), app.menu[i][0], self.color[0], (self.ziti, (app.ziti + 17)))
            self.img.blit(self.guangbiao[0], source = (0, 0, (t + 20), t2[1]), target = (0, ((self.y - 35) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1])), mask = self.guangbiao[1])
            if app.menu[self.gb2][0][-1] == cn('√') or app.menu[self.gb2][0][-1] == cn('>') : 
                self.img.text((10, ((self.y - 15) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1])), app.menu[self.gb2][0][ : -1], self.color[2], (self.ziti, (app.ziti + 17)))
            else : 
                self.img.text((10, ((self.y - 15) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1])), app.menu[self.gb2][0], self.color[2], (self.ziti, (app.ziti + 17)))
            self.img.rectangle((0, ((self.y - 40) - (len(app.menu) * t2[1])), (t + 20), (self.y - 28)), self.color[2])
            if self.mode2 == 1 : 
                if self.menu_changdu1[self.gb2] == [] : 
                    tt = 0
                    for tt1 in app.menu[self.gb2][1]:
                        tt2 = split_text(tt1[0] + cn(' √'), (app.ziti + 17), 2)
                        if tt < tt2[0] : 
                            tt = tt2[0]
                        del tt1
                    tt2[1] = (tt2[1] + 10)
                    self.menu_changdu1[self.gb2] = [tt, tt2]
                else : 
                    tt = self.menu_changdu1[self.gb2][0]
                    tt2 = self.menu_changdu1[self.gb2][1]
                self.img.blit(app.img1[0], target = (0, ((self.y - 40) - (len(app.menu) * t2[1]))), source = (0, 0, (t + 20), ((len(app.menu) * t2[1]) + 10)), mask = app.img1[1])
                if (t + tt + 40) > (self.x - 3) : 
                    t -= ((t + tt + 40) - (self.x - 3))
                self.img.blit(app.img1[0], target = ((t + 20), (((self.y - 30) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1]))), source = (0, 0, (tt + 20), (((len(app.menu[self.gb2][1]) + 1)) * tt2[1])), mask = app.img1[1])
                for i in xrange(len(app.menu[self.gb2][1])):
                    if app.menu[self.gb2][1][i][0][-1] == cn('√') : 
                        self.img.text(((t + 30), ((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (i * tt2[1])), app.menu[self.gb2][1][i][0][ : -1], self.color[0], (self.ziti, (app.ziti + 17)))
                        self.img.text(((tt + t + 25), ((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (i * tt2[1])), cn('√'), self.color[0], (self.ziti, (app.ziti + 17)))
                    else : 
                        self.img.text(((t + 30), ((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (i * tt2[1])), app.menu[self.gb2][1][i][0], self.color[0], (self.ziti, (app.ziti + 17)))
                    del i
                self.img.blit(self.guangbiao[0], source = (0, 0, (tt + 20), tt2[1]), target = ((t + 20), ((((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (self.gb3 * tt2[1]) - tt2[1]) + 2)), mask = self.guangbiao[1])
                if app.menu[self.gb2][1][self.gb3][0][-1] == cn('√') : 
                    self.img.text(((t + 30), ((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (self.gb3 * tt2[1])), app.menu[self.gb2][1][self.gb3][0][ : -1], self.color[2], (self.ziti, (app.ziti + 17)))
                else : 
                    self.img.text(((t + 30), ((self.y - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])) + (self.gb3 * tt2[1])), app.menu[self.gb2][1][self.gb3][0], self.color[2], (self.ziti, (app.ziti + 17)))
                self.img.rectangle(((t + 20), (((self.y - 30) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1]) - (len(app.menu[self.gb2][1]) * tt2[1])), (t + tt + 40), ((self.y - 10) - (len(app.menu) * t2[1])) + (self.gb2 * t2[1])), self.color[2])
                del tt
                del tt2
            del t
            del t2
            cd = '选择'
            tc = '取消'
        if app.query != [] : 
            t = len(app.query)
            if t < 3 : 
                t = 3
            if app.switch['阴影'] : 
                self.img.blit(app.img1[0], target = (0, 50), mask = app.img1[1])
            self.img.blit(app.img1[0], target = ((3 + app.rolling['提示'][0]), ((self.y - (t * 25)) - 35) + app.rolling['提示'][1]), source = (0, 0, (self.x - 6), ((t * 25) + 10)), mask = app.img1[1])
            self.img.rectangle(((3 + app.rolling['提示'][0]), ((self.y - (t * 25)) - 35) + app.rolling['提示'][1], (self.x - 3) + app.rolling['提示'][0], (self.y - 25) + app.rolling['提示'][1]), self.color[2], width = 2)
            for index in xrange(len(app.query)):
                self.img.text(((10 + app.rolling['提示'][0]), (self.y - (t * 25)) + (index * 20) + app.rolling['提示'][1]), app.query[index], self.color[0], (self.ziti, (app.ziti + 19)))
            self.img.text(((self.x - 45) + app.rolling['提示'][0], (self.y - 40) + app.rolling['提示'][1]), cn('？'), self.color[0], (self.ziti, (app.ziti + 70)))
            cd = '确认'
            tc = '取消'
        self.img.blit(self.img1[0][0], target = (((len(cn(cd)) * (app.ziti + 20)) + 5), (self.y - 25)), source = (((len(cn(cd)) * (app.ziti + 20)) + 5), (self.y - 25), ((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), self.y))
        self.img.blit(self.img1[0][0], target = (50, 0), source = (50, 0, self.x, 50))
        self.img.blit(self.img1[2][0], target = (((len(cn(cd)) * (app.ziti + 20)) + 5), (self.y - 25)), source = (((len(cn(cd)) * (app.ziti + 20)) + 5), 0, ((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), 25), mask = self.img1[2][1])
        self.img.blit(self.img1[1][0], source = (50, 0, self.x, 50), target = (50, 0), mask = self.img1[1][1])
        if self.gb1 == -1 : 
            self.img.rectangle((46, 25, self.x, 45), self.color[2], fill = 15790089)
            self.img.text((self.gg1, 44), cn(self.gg[self.gg2]), 0, (self.ziti, (app.ziti + 16)))
        else : 
            self.img.text((self.gg1, 44), cn(self.gg[self.gg2]), (self.color[1][0], self.color[0][0], self.color[1][0]), (self.ziti, (app.ziti + 15)))
        self.img.blit(self.img1[0][0], source = (0, 0, 50, 50))
        self.img.blit(self.img1[1][0], source = (0, 0, 50, 50), mask = self.img1[1][1])
        self.img.text((10, 42), (cn('%d/%d') % (len(self.gg), (self.gg2 + 1))), self.color[0], (self.ziti, (app.ziti + 16)))
        try :
            self.img.text(((self.x / 4) + app.info_liudong, (self.y - 2)), cn(app.info[app.info_xy]), (app.info_color, app.info_color, app.info_color), (self.ziti, (app.ziti + 14)))
        except :
            self.img.text(((self.x / 4) + app.info_liudong, (self.y - 2)), app.info[app.info_xy], (app.info_color, app.info_color, app.info_color), (self.ziti, (app.ziti + 14)))
        self.img.blit(self.img1[0][0], target = (((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), (self.y - 25)), source = (((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), (self.y - 25), self.x, self.y))
        self.img.blit(self.img1[0][0], target = (0, (self.y - 25)), source = (0, (self.y - 25), ((len(cn(cd)) * (app.ziti + 20)) + 5), self.y))
        self.img.blit(self.img1[2][0], target = (((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), (self.y - 25)), source = (((self.x - (len(cn(tc)) * (app.ziti + 20))) - 5), 0, self.x, 25), mask = self.img1[2][1])
        self.img.blit(self.img1[2][0], target = (0, (self.y - 25)), source = (0, 0, ((len(cn(cd)) * (app.ziti + 20)) + 5), 25), mask = self.img1[2][1])
        if app.switch['电量'] == True : 
            self.img.rectangle(((self.x - 13), 5, (self.x - 3), 20), 16777215, width = 2)
            self.img.rectangle(((self.x - 10), 3, (self.x - 6), 4), 16777215, width = 2)
            self.img.rectangle(((self.x - 11), (20 - ((float(13) * app.battery[0]) / 100)), (self.x - 4), 19), fill = self.color[2])
        if app.switch['时间'] == True : 
            self.img.text(((self.x - 80), 24), cn(time.strftime('%X')), self.color[2], (self.ziti, (app.ziti + 15)))
        self.img.text((60, 24), cn(bt), (self.color[1][0], self.color[0][0], self.color[0][0]), (self.ziti, (app.ziti + 17)))
        self.img.line((46, 23, self.x, 23), 5409177)
        self.img.text((5, 22), cn('公告'), (self.color[0][2], self.color[1][2], self.color[2][2]), (self.ziti, (app.ziti + 17)))
        self.img.text((3, (self.y - 2)), cn(cd), self.color[0], (self.ziti, (app.ziti + 17)))
        self.img.text(((self.x - (len(cn(tc)) * (app.ziti + 20))), (self.y - 2)), cn(tc), self.color[0], (self.ziti, (app.ziti + 17)))
        if app.note[0] != [] : 
            if app.switch['阴影'] : 
                self.img.blit(app.img1[0], target = (0, 50), mask = app.img1[1])
            self.img.blit(app.img1[0], target = (3, app.note[1][0]), source = (3, 0, (self.x - 3), (len(app.note[0]) * 25)), mask = app.img1[1])
            self.img.rectangle((3, app.note[1][0], (self.x - 3), (len(app.note[0]) * 25) + app.note[1][0]), 1193046, width = 2)
            for t in xrange(len(app.note[0])):
                self.img.text((10, ((t * 25) + 23) + app.note[1][0]), app.note[0][t], self.color[0], (self.ziti, (app.ziti + 18)))
            pass


        self.blit(self.img, target = (app.rolling['界面'][0], app.rolling['界面'][1]))




    def exit(self):
        import os
        del self.gb_yidong
        os.abort()




    def draw(self, draw = True):
        pass




    def up(self, number = 0):
        if self.mode1 == 1 : 
            if self.mode2 == 1 : 
                self.gb3 -= 1
                if self.gb3 < 0 : 
                    self.gb3 = (len(app.menu[self.gb2][1]) - 1)
                pass
            else : 
                self.gb2 -= 1
                if self.gb2 < 0 : 
                    self.gb2 = (len(app.menu) - 1)
                pass
            pass
        elif self.mode == 0 : 
            app.liudong = 0
            self.xx = 5
            self.gb1 -= 1
            if self.gb1 != -1 : 
                self.b2 -= 1
                if self.b2 < 0 : 
                    self.gb_yidong += 1
                pass
            if self.gb1 < -1 : 
                self.gb1 = (len(self.a1) - 1)
                if len(self.a1) > 5 : 
                    self.b2 = 4
                    self.b1 = (len(self.a1) - 4)
                    self.gb_yidong = 1
                else : 
                    self.b2 = (len(self.a1) - 1)
                    self.b1 = self.gb_yidong = 0
                pass
            pass
        if number == 0 : 
            self.menu()
        else : 
            self.While(1)




    def down(self, number = 0):
        if self.mode1 == 1 : 
            if self.mode2 == 1 : 
                self.gb3 += 1
                if self.gb3 > (len(app.menu[self.gb2][1]) - 1) : 
                    self.gb3 = 0
                pass
            else : 
                self.gb2 += 1
                if self.gb2 > (len(app.menu) - 1) : 
                    self.gb2 = 0
                pass
            pass
        elif self.mode == 0 : 
            app.liudong = 0
            self.xx = 5
            if self.gb1 != -1 : 
                self.b2 += 1
            self.gb1 += 1
            if self.gb1 > (len(self.a1) - 1) : 
                self.gb1 = self.b2 = 0
                if len(self.a1) > 5 : 
                    self.b1 = self.gb_yidong = -1
                else : 
                    self.b1 = self.gb_yidong = 0
                pass
            elif self.b2 > 4 and self.y == 320 : 
                if len(self.a1) > 5 : 
                    self.gb_yidong -= 1
                else : 
                    self.b1 -= 1
                pass
            elif self.b2 > 2 and self.y == 208 : 
                if len(self.a1) > 5 : 
                    self.gb_yidong -= 1
                else : 
                    self.b1 -= 1
                pass
            pass
        if number == 0 : 
            self.menu()
        else : 
            self.While(1)


    def right(self):
        if self.mode1 == 0 : 
            if self.gb1 == -1 : 
                self.gg2 += 1
                self.gg1 = 75
                if self.gg2 > (len(self.gg) - 1) : 
                    self.gg2 = 0
                pass
            else : 
                try :
                    app.key['右']()
                except :
                    pass
                pass
            pass
        elif self.mode1 == 1 : 
            if self.mode2 == 0 : 
                try :
                    if len(app.menu[self.gb2][1]) >= 1 : 
                        self.mode2 = 1
                except :
                    pass
                pass
            pass




    def left(self):
        if self.mode1 == 0 : 
            if self.gb1 == -1 : 
                self.gg2 -= 1
                self.gg1 = 75
                if self.gg2 < 0 : 
                    self.gg2 = (len(self.gg) - 1)
                pass
            else : 
                try :
                    app.key['左']()
                except :
                    pass
                pass
            pass
        elif self.mode1 == 1 : 
            if self.mode2 == 0 : 
                self.mode1 = 0
                self.gb2 = 0
            else : 
                self.mode2 = 0
                self.gb3 = 0
            pass




    def OK(self):
        if self.mode1 == 1 : 
            if self.mode2 == 0 : 
                try :
                    if len(app.menu[self.gb2][1]) >= 1 : 
                        self.mode2 = 1
                except :
                    try :
                        app.menu[self.gb2][1]()
                    except :
                        pass
                    self.mode1 = 0
                    self.gb2 = 0
                pass
            elif self.mode2 == 1 : 
                try :
                    app.menu[self.gb2][1][self.gb3][1]()
                except :
                    pass
                self.mode1 = 0
                self.gb2 = 0
                self.mode2 = 0
                self.gb3 = 0
            pass
        elif self.mode == 0 : 
            if self.gb1 == -1 : 
                pass
            else : 
                self.a2()
            pass
        self.menu()




    def keyft(self, key):
        tp = key['type']
        ky = key['scancode']
        if(tp==3):
            print (key)
        if app.gb_key == False : 
            pass
        elif app.query != [] : 
            if ky == 165 and tp == 3 : 
                app.query = []
                app.return_query = False
            elif ky == 164 or ky == 167 and tp == 3 : 
                app.query = []
                app.return_query = True
            pass
        elif ky == 16 : 
            if self.mode1 == 1 or self.mode2 == 1 and tp == 1 : 
                self.up()
            elif self.mode == 0 and self.mode1 == 0 and tp == 3 : 
                self.key = 1
                after(0.1)
                while self.key : 
                    self.up(1)
                    ui.e32.ao_yield()
                pass
            elif self.mode == 0 and self.mode1 == 0 and tp == 2 : 
                self.key = 0
                cancel()
                self.up()
            pass
        elif ky == 17 : 
            if self.mode1 == 1 or self.mode2 == 1 and tp == 1 : 
                self.down()
            elif self.mode == 0 and self.mode1 == 0 and tp == 3 : 
                self.key = 1
                after(0.1)
                while self.key : 
                    self.down(1)
                    ui.e32.ao_yield()
                pass
            elif self.mode == 0 and self.mode1 == 0 and tp == 2 : 
                self.key = 0
                cancel()
                self.down()
            pass
        elif ky == 14 and tp == 1 : 
            self.left()
        elif ky == 15 and tp == 1 : 
            self.right()
        elif ky == 48 and tp == 1 : 
            pass
        elif ky == 167 and tp == 3 : 
            self.OK()
        elif ky == 164 and tp == 3 : 
            if self.mode1 == 1 and app.menu != [] : 
                if self.mode2 == 0 : 
                    try :
                        if len(app.menu[self.gb2][1]) >= 1 : 
                            self.mode2 = 1
                    except :
                        try :
                            app.menu[self.gb2][1]()
                        except :
                            pass
                        self.mode1 = 0
                        self.gb2 = 0
                    pass
                elif self.mode2 == 1 : 
                    try :
                        app.menu[self.gb2][1][self.gb3][1]()
                    except :
                        pass
                    self.mode1 = 0
                    self.gb2 = 0
                    self.mode2 = 0
                    self.gb3 = 0
                pass
            elif app.menu != [] : 
                self.mode1 = 1
            self.menu()
        elif ky == 165 : 
            if self.mode1 == 1 or self.mode2 == 1 and tp == 3 : 
                self.gb2 = 0
                self.gb3 = 0
                self.mode1 = 0
                self.mode2 = 0
                self.menu_changdu = []
            else : 
                if self.mode1 == 0 or self.mode2 == 0 and tp == 3 : 
                    try :
                        app.exit_key_handler[0]()
                    except :
                        pass
                    pass
                pass
            pass
        else : 
            if ky == 49 and tp == 1:
                try :
                    app.key['1']()
                except :
                    pass
                pass
            else : 
                if ky == 50 and tp == 1 : 
                    try :
                        app.key['2']()
                    except :
                        pass
                    pass
                else : 
                    if ky == 51 and tp == 1 : 
                        try :
                            app.key['3']()
                        except :
                            pass
                        pass
                    else : 
                        if ky == 52 and tp == 1 : 
                            try :
                                app.key['4']()
                            except :
                                pass
                            pass
                        else : 
                            if ky == 53 and tp == 1 : 
                                try :
                                    app.key['5']()
                                except :
                                    pass
                                pass
                            else : 
                                if ky == 54 and tp == 1 : 
                                    try :
                                        app.key['6']()
                                    except :
                                        pass
                                    pass
                                else : 
                                    if ky == 55 and tp == 1 : 
                                        try :
                                            app.key['7']()
                                        except :
                                            pass
                                        pass
                                    else : 
                                        if ky == 56 and tp == 1 : 
                                            try :
                                                app.key['8']()
                                            except :
                                                pass
                                            pass
                                        else : 
                                            if ky == 57 and tp == 1 : 
                                                try :
                                                    app.key['9']()
                                                except :
                                                    pass
                                                pass
                                            else : 
                                                if ky == 42 and tp == 1 : 
                                                    try :
                                                        app.key['*']()
                                                    except :
                                                        pass
                                                    pass
                                                else : 
                                                    if ky == 127 and tp == 1 : 
                                                        try :
                                                            app.key['#']()
                                                        except :
                                                            pass
                                                        pass
                                                    else : 
                                                        if ky == 196 and tp == 1 : 
                                                            try :
                                                                app.key['拨号']()
                                                            except :
                                                                pass
                                                            pass
                                                        else : 
                                                            if ky == 1 and tp == 1 : 
                                                                try :
                                                                    app.key['删除']()
                                                                except :
                                                                    pass
                                                                pass
                                                            pass






class app :
    __module__ = __name__


app.e32 = 0
app.battery = [100, 0]
app.rolling = {'界面' : [0, 0], '提示' : [0, 0]}
app.gb_key = True
app.key = {}
app.switch = {'电量' : True, '时间' : True, '阴影' : False}
app.exit_key_handler = []
app.query = []
app.note = [[], [0, 0]]
app.return_query = None
app.xx = 0
app.yy = 0
app.liudong = 0
app.info_xx = 2
app.info_color = 0
app.info_xy = 0
app.info_liudong = 0
app.info = ['界面设计:轩宝[py]', '设计时间:2010-05-27']
app.menu = []
app.ziti = 0
app.txt_changdu = [0, 0, 3, '']
app.append = []