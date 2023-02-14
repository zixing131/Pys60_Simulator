# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


class system :
    __module__ = __name__



system.path = r'E:\Users\zixing\Documents\GitHub\Pys60_Simulator\python\pysoft\Pymusic_xb\\'

def openfile(path):
    txt = open(path)
    READ = cn(txt.read())
    txt.close()
    return READ




def writefile(path, txt):
    WRITE = open(path, 'w')
    try :
        WRITE.write(en(txt))
    except :
        WRITE.write(txt)
    WRITE.close()
    return True


from ui2 import *
try :
    import envy
    envy.set_app_system(1)
except :
    pass


def start(number = 0):


    class s :
        __module__ = __name__


    execfile(en(openfile(system.path + 'skin.dat')))
    if number == 1 : 
        canvas = Listbox(s.skin_path, s.logo_path, color = s.color, menu_tag = s.menu_tag, cursor_tag = s.cursor_tag, title_tag = s.title_tag)
    else : 
        canvas.skin(cn(s.skin_path), color = s.color, menu_tag = s.menu_tag, cursor_tag = s.cursor_tag, title_tag = s.title_tag)
    del s
    global canvas


start(1)
import audio
import os
import lrc
import re
vases = '\napp.switch["电量"]=True\napp.switch["时间"]=True\napp.switch["阴影"]=False\nsystem.vol=5\nsystem.moshi=0\nsystem.rolling=True\nsystem.dengguang=False\napp.e32=0\napp.keshihua=True\n'
system.stop = False
system.play = [0, 0]
system.mode = 0
system.dir = None
system.list = []
system.pos = [0, 0]
system.e32 = ui.e32.Ao_timer()
system.time1 = [0, '0:00.0']
app.music = {}
app._A = [[0, 240]]
app._A_color = [255, 255, 255, 0]
app._B = []
app.music['进度'] = [0, '0:00.0', 1, '0:00.0']
app.music['状态'] = True
app.music['可视化'] = False
try :
    execfile(system.path + 'set.db')
except :
    canvas.note('读取设置失败！\n恢复默认设置！', 'note')
    exec vases


def query(txt):
    if system.rolling : 
        app.rolling['提示'] = [0, 110]
    return canvas.query(txt)




def exit():
    if query('退出音乐播放器？') : 
        try :
            writefile(system.path + 'set.db', ('app.switch["电量"]=%s\napp.switch["时间"]=%s\napp.switch["阴影"]=%s\nsystem.vol=%s\nsystem.moshi=%s\nsystem.rolling=%s\nsystem.dengguang=%s\napp.e32=%s\napp.keshihua=%s' % (app.switch['电量'], app.switch['时间'], app.switch['阴影'], system.vol, system.moshi, system.rolling, system.dengguang, app.e32, app.keshihua)))
        except :
            ui.note(cn('设置保存失败'), 'error', 1)
        canvas.exit()




def about():
    canvas.note('—欢迎使用—\n音乐播放器v1.4\n2010-06-14\nby:轩宝\nqq:604054726')




def vol_jia():
    if system.vol < 10 : 
        system.vol += 1
        try :
            txt = re.compile('wma', re.I)
            if txt.findall(system.list[system.lrc][-3 : ]) != [] : 
                system.b.set_volume((system.vol * 11))
            else : 
                system.b.set_volume(system.vol)
        except :
            pass
        pass
    canvas.note('音量 : ' + ('♫' * system.vol), 'info')




def vol_jian():
    if system.vol > 0 : 
        system.vol -= 1
        try :
            txt = re.compile('wma', re.I)
            if txt.findall(system.list[system.lrc][-3 : ]) != [] : 
                system.b.set_volume((system.vol * 10))
            else : 
                system.b.set_volume(system.vol)
        except :
            pass
        pass
    canvas.note('音量 : ' + ('♫' * system.vol), 'info')




def dur(number):
    return [number, str((number / 600)) + ':' + ('%02d' % ((number % 600) / 10)) + '.' + str((number % 600))[-1]]




def pos():
    press(system.lrc, system.pos[2] + system.pos[0])




def position_jian():
    try :
        system.e32.cancel()
    except :
        pass
    try :
        if system.pos[2] == None : 
            if system.b.state() != 2 : 
                stop()
            system.pos[2] = system.b.current_position()
        system.pos[1] -= 1
        system.pos[0] += (system.pos[1] * 1000000)
        time1 = dur((system.pos[2] + system.pos[0] / 100000))
        canvas.note(('模式: 快退 <<\n%s / %s' % (time1[1], system.time1[1])), 'info')
        canvas.While(1)
        system.e32.after(0.3, pos)
    except :
        pass




def position_jia():
    try :
        system.e32.cancel()
    except :
        pass
    try :
        if system.pos[2] == None : 
            if system.b.state() != 2 : 
                stop()
            system.pos[2] = system.b.current_position()
        system.pos[0] += (system.pos[1] * 1000000)
        system.pos[1] += 1
        time1 = dur((system.pos[2] + system.pos[0] / 100000))
        canvas.note(('模式: 快进 >>\n%s / %s' % (time1[1], system.time1[1])), 'info')
        canvas.While(1)
        system.e32.after(0.3, pos)
    except :
        pass




def Play(number, time = None):
    system.lrc = number
    system.b = audio.Sound.open(system.dir + cn(system.list[number]))
    try :
        txt = re.compile('wma', re.I)
        if txt.findall(system.list[system.lrc][-3 : ]) != [] : 
            system.b.set_volume((system.vol * 10))
        else : 
            system.b.set_volume(system.vol)
    except :
        pass
    system.stop = False
    if time != None : 
        system.b.set_position(time)
    system.b.play()
    system.time1 = dur((system.b.duration() / 100000))
    try :
        Lrc()
    except :
        pass
    t = ''
    for i in system.list[number].split('.'):
        if i != system.list[number].split('.')[-1] : 
            t += i
    app.music['正在播放'] = [t, split_text(t, 18), 0, 0]
    app.music['可视化'] = True
    app._A = [[0, 240]]
    app.music['状态'] = False
    system.pos = [0, 0, None]




def stop():
    if system.stop == False : 
        system.b.close()
        system.stop = True
        app.music['可视化'] = False
        app.music['状态'] = True
    else : 
        press(system.play[1], system.play[0])




def Lrc():
    true = False
    list = ['e:\\TTPod\\Lyrics\\' + en(cn(system.list[system.lrc])[ : -4]) + '.lrc', 'e:\\开心听\\歌词\\' + en(cn(system.list[system.lrc])[ : -4]) + '.lrc']
    for t in list:
        try :
            lrc.lrc(t)
            system.time = system.list[system.lrc][ : -4]
            try :
                canvas.Text(lrc.WIN.list, 0, 1)
            except :
                pass
            true = True
            break
        except :
            pass
    if  not (true) : 
        system.time = None
        canvas.info(['找不到歌词文件-1', system.list[system.lrc][ : -4]])
        lrc.WIN.list = []
        try :
            canvas.Text(lrc.WIN.list, 0, 1)
        except :
            pass
        pass




def press(number = None, TIME = None):
    a = canvas.current()
    if number != None : 
        a = number
    if a != None : 
        if TIME != None : 
            Play(a, TIME)
        else : 
            Play(a)
        while True : 
            if system.stop : 
                break
            if system.b.state() != 2 : 
                system.b.close()
                if system.moshi == 0 : 
                    if (a + 1) >= len(system.list) : 
                        a = 0
                    else : 
                        a += 1
                    pass
                elif system.moshi == 1 : 
                    pass
                elif system.moshi == 2 : 
                    a = system.list.index(random.choice(system.list))
                Play(a)
            else : 
                canvas.While(1)
            try :
                if system.time != None : 
                    if system.mode == 0 : 
                        canvas.info([system.time])
                    else : 
                        canvas.info(['歌词界面-轩宝原创'])
                    pass
                system.play = (system.b.current_position(), a)
                time = lrc.Return(system.play[0])
                if time != None : 
                    if system.dengguang : 
                        ui.e32.reset_inactivity()
                    system.time = time
                    try :
                        canvas.Text(lrc.WIN.list, lrc.Return(system.b.current_position(), 1))
                    except :
                        pass
                    pass
                del time
            except :
                pass
            try :
                app.music['进度'] = [system.b.current_position(), dur((system.b.current_position() / 100000))[1], system.b.duration(), system.time1[1]]
            except :
                pass
            if app.e32 == 0 : 
                ui.e32.ao_yield()
            else : 
                ui.e32.ao_sleep(float(1E-22))
        pass




def rolling():
    if system.rolling : 
        system.rolling = False
    else : 
        system.rolling = True
    moshi()




def dengguang():
    if system.dengguang : 
        system.dengguang = False
    else : 
        system.dengguang = True
    moshi()




def switch_time():
    if app.switch['时间'] : 
        app.switch['时间'] = False
    else : 
        app.switch['时间'] = True
    moshi()




def keshihua():
    if app.keshihua : 
        app.keshihua = False
    else : 
        app.keshihua = True
    moshi()




def switch_dl():
    if app.switch['电量'] : 
        app.switch['电量'] = False
    else : 
        app.switch['电量'] = True
    moshi()




def switch_yy():
    if app.switch['阴影'] : 
        app.switch['阴影'] = False
    else : 
        app.switch['阴影'] = True
    moshi()




def skin0():
    canvas.note('正在换皮肤...', 'info')
    canvas.menu()
    ui.e32.ao_sleep(0.1)
    writefile(system.path + 'skin.dat', ('%sskin\\雪夜星空.tb' % system.path))
    start()
    moshi()




def skin1():
    canvas.note('正在换皮肤...', 'info')
    canvas.menu()
    ui.e32.ao_sleep(0.1)
    writefile(system.path + 'skin.dat', ('%sskin\\XP.tb' % system.path))
    start()
    moshi()




def skin2():
    canvas.note('正在换皮肤...', 'info')
    canvas.menu()
    ui.e32.ao_sleep(0.1)
    writefile(system.path + 'skin.dat', ('%sskin\\山河图.tb' % system.path))
    start()
    moshi()




def skin3():
    canvas.note('正在换皮肤...', 'info')
    canvas.menu()
    ui.e32.ao_sleep(0.1)
    writefile(system.path + 'skin.dat', ('%sskin\\海底世界.tb' % system.path))
    start()
    moshi()




def e32_moshi0():
    app.e32 = 0
    moshi()




def e32_moshi1():
    app.e32 = 1
    moshi()




def moshi0():
    system.moshi = 0
    moshi()




def moshi1():
    system.moshi = 1
    moshi()




def moshi2():
    system.moshi = 2
    moshi()




def moshi():
    menu = [(cn('全部循环'), moshi0), (cn('单曲循环'), moshi1), (cn('随机模式'), moshi2), (cn('最快(影响qq窗口闪烁)'), e32_moshi0), (cn('较快(不影响其他程序)'), e32_moshi1), (cn('可视化开关'), keshihua), (cn('平滑切换界面'), rolling), (cn('提示框阴影效果'), switch_yy), (cn('有歌词时灯光常亮'), dengguang), (cn('显示系统时间'), switch_time), (cn('显示手机电量'), switch_dl), (cn('雪夜星空'), skin0), (cn('XP'), skin1), (cn('山河图'), skin2), (cn('海底世界'), skin3)]
    app.menu = []
    txt = openfile(system.path + 'skin.dat')
    for i in menu:
        t = cn('')
        if menu.index(i) == system.moshi : 
            t = cn('√')
        if menu.index(i) == 3 and app.e32 == 0 : 
            t = cn('√')
        elif menu.index(i) == 4 and app.e32 != 0 : 
            t = cn('√')
        elif menu.index(i) == 5 and app.keshihua : 
            t = cn('√')
        elif menu.index(i) == 6 and system.rolling : 
            t = cn('√')
        elif menu.index(i) == 7 and app.switch['阴影'] : 
            t = cn('√')
        elif menu.index(i) == 8 and system.dengguang : 
            t = cn('√')
        elif menu.index(i) == 9 and app.switch['时间'] : 
            t = cn('√')
        elif menu.index(i) == 10 and app.switch['电量'] : 
            t = cn('√')
        elif 10 < menu.index(i) < 15 : 
            tts = re.compile(i[0])
            if tts.findall(txt) != [] : 
                t = cn('√')
            del tts
        i = (i[0] + t, i[1])
        app.menu.append(i)
        del t
        del i
    app.menu = [(cn('选择目录'), scan)] + [(cn('更换皮肤>'), app.menu[11 : 15])] + [(cn('播放模式>'), app.menu[ : 3])] + [(cn('运行模式>'), app.menu[3 : 5])] + [(cn('软件选项>'), app.menu[5 : 11])] + [(cn('关于软件'), about), (cn('退出程序'), exit)]




def mode1():
    system.mode += 1
    if system.mode > 2 : 
        system.mode = 0
    canvas.Text_List(system.mode)
    if system.rolling : 
        app.rolling['界面'][0] = random.choice([-240, -240, 0, -240])
        app.rolling['界面'][1] = random.choice([320, -320, 0, 320, -320])




def mode2():
    system.mode -= 1
    if system.mode < 0 : 
        system.mode = 2
    canvas.Text_List(system.mode)
    if system.rolling : 
        app.rolling['界面'][0] = random.choice([240, 240, 0, 240])
        app.rolling['界面'][1] = random.choice([320, -320, 0, 320, -320])




class self :
    __module__ = __name__




def scan():


    self.list = ['[C:]', '[E:]']
    self.path = []
    def Return():
        if self.path == [] : 
            if query('确认返回？') : 
                main()
                return None
            pass
        else : 
            if self.path[0] == self.path[-1] : 
                self.list = ['[C:]', '[E:]']
                self.path = []
            else : 
                del self.path[-1]
                self.list = []
                for t in os.listdir(self.path[-1]):
                    path = self.path[-1] + '\\' + t
                    try :
                        if os.path.isdir(path) : 
                            self.list.append((str('[%s]') % t))
                    except :
                        pass
                pass
        if system.rolling and self.path != [] : 
            app.rolling['界面'] = [random.choice([240, 0, -240, -240, 240]), random.choice([320, 0, -320, -320, 320])]
        canvas.Listbox_new(self.list, press1)
        canvas.info(['请选择文件夹'])




    def OK1(path):
        if query(('路径:%s' % path)) : 
            a = open(system.path + 'path.dat', 'w')
            a.write(path)
            a.close()
            canvas.note(('保存成功！\n路径:%s' % path))
            del path
            del a
            main()




    def OK():
        try :
            path = self.path[-1] + self.list[canvas.current()][1 : -1]
        except :
            canvas.note('请正确选择路径！')
            return None
        if  not (os.path.isdir(path)) : 
            canvas.note(('请选择文件夹！\n该目录路径为:\n　%s' % self.path[-1]))
            OK1(self.path[-1])
        elif query(('路径:%s' % path)) : 
            a = open(system.path + 'path.dat', 'w')
            a.write(('%s\\' % path))
            a.close()
            canvas.note(('保存成功！\n路径:%s' % path))
            del path
            del a
            main()




    def press1():
        a = canvas.current()
        if a != None : 
            try :
                try :
                    if  not (os.path.isdir(('%s%s\\' % (self.path[-1], self.list[a][1 : -1])))) :
                        canvas.note(('请选择文件夹！\n该目录路径为:\n　%s' % self.path[-1]))
                        OK1(self.path[-1])
                        return None
                    else : 
                        self.path.append(('%s%s\\' % (self.path[-1], self.list[a][1 : -1])))
                except :
                    if  not (os.path.isdir(('%s\\' % self.list[a][1 : -1]))) :
                        canvas.note(('请选择文件夹！\n该目录路径为:\n　%s' % self.path[-1]))
                        OK1(self.path[-1])
                        return None
                    else : 
                        self.path.append(('%s\\' % self.list[a][1 : -1]))
                    pass
                self.list = []
                for t in os.listdir(self.path[-1]):
                    path = self.path[-1] + '\\' + t
                    try :
                        if os.path.isdir(path) or filter(t) != None : 
                            self.list.append((str('[%s]') % t))
                    except :
                        pass
                if system.rolling : 
                    app.rolling['界面'] = [random.choice([240, 0, -240, -240, 240]), random.choice([320, 0, -320, -320, 320])]
                canvas.Listbox_new(self.list, press1)
                canvas.info(['请选择文件夹'])
            except :
                pass
            pass


    canvas.Listbox_new(self.list, press1)
    app.menu = [(cn('确定(选中)'), OK), (cn('返回[上级]'), Return)]
    canvas.info(['请选择文件夹'])
    canvas.bind(63496, canvas.OK)
    canvas.bind(63495, Return)
    canvas.bind(52, Return)
    canvas.bind(54, canvas.OK)
    canvas.bind(57, None)
    canvas.bind(51, None)
    canvas.bind(49, None)
    app.exit_key_handler = [Return]




def filter(x):
    list = ['.wma', '.mp3', '.aac', '.mid', '.amr']
    for t in list:
        txt = re.compile(t, re.I)
        if txt.findall(x[-4 : ]) != [] : 
            return x




def main(number = 0):
    try :
        a = open(system.path + 'path.dat')
        system.dir = a.read().decode('u8')
        a.close()
        del a
        list = map(filter, os.listdir(en(system.dir)))
        system.list = []
        for t in list:
            if t != None : 
                system.list.append(t)
    except :
        system.list = []
    canvas.bind(63496, mode1)
    canvas.bind(63495, mode2)
    canvas.bind(57, vol_jian)
    canvas.bind(51, vol_jia)
    canvas.bind(49, stop)
    canvas.bind(50, canvas.up)
    canvas.bind(56, canvas.down)
    canvas.bind(53, canvas.OK)
    canvas.bind(52, position_jian)
    canvas.bind(54, position_jia)
    moshi()
    app.exit_key_handler = [exit]
    canvas.info(['轩宝作品-必属精品'])
    if number == 1 : 
        canvas.Listbox(system.list, press, '音乐播放v1.4', ['快捷键 : 减小音量(9) 增加音量(3) 暂停(1) 方向键上(2)/下(8)(移动光标) 方向键左(4)/右(6)(界面切换)', '音乐播放器v1.4版 轩宝 qq:604054726 手机:13720861065', '轩宝作品-必属精品-欢迎使用'])
        canvas.While()
    else : 
        canvas.Listbox_new(system.list, press)
        canvas.Text_List(system.mode)


try :
    main(1)
except :
    exec vases
    main(1)