# -*- coding: utf-8 -*- 
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import e32
cn = lambda x, : x.decode('utf-8') 
en = lambda x, : x.encode('utf-8') 
def new(x, l = 0):
    from graphics import Image as Image
    if l : 
        return Image.new(x, 'L')
    else : 
        return Image.new(x)




def event(s, ev):
    es = ev['scancode']
    et = ev['type']
    e32.ao_yield()
    if et == 2 : 
        s.key = 0
    if s.run or s.zbtj or es in [164, 165] : 
        return None
    if et == 2 : 
        s.key = 0
        if es == 14 : 
            s.key_14 = 0
        elif es == 15 : 
            s.key_15 = 0
        elif es == 16 : 
            s.key_16 = 0
        elif es == 17 : 
            s.key_17 = 0
        elif es == 48 : 
            s.run = 0
            s.whil = 0
        e32.ao_yield()
        if  not (s.zc and s.men) and s.cd_bg and es == 167 : 
            if s.zcd_pos_list != s.zcd_pos_list_old : 
                if  not ( not (s.zcd_pos_list_old) or s.zcd_pos_list) or s.zcd_pos_list_old[0] > 10 : 
                    s.zcd_pos_list_old = 0
                    return None
                s.pos_color[s.zcd_pos_list_old[0]] = s.pos_color[s.zcd_pos_list[0]]
                s.zcd_pos_list_old = 0
                return s.zcd(n = 200)
            if  not (s.zcd_pos_list) or s.whil : 
                return None
            s.timer.cancel()
            e32.ao_sleep(0)
            s.zcd_pos_list_old = 0
            fir = s.zcd_pos_list[0]
            if fir < 11 : 
                fir = {cn('英雄资料') : 0, cn('查看周免') : 1, cn('物品资料') : 2, cn('天赋资料') : 3, cn('符文资料') : 4, cn('英雄漫画') : 5, cn('战绩查询') : 6, cn('召唤技能') : 7, cn('查看新闻') : 8, cn('查看攻略') : 9, cn('神级阵容') : 10}[s.cd_txtlist[fir]]
            s.run = s.whil = 0
            if fir < 11 : 
                s.y4 = s.y
                s.zc = s.y = 0
            e32.ao_yield()
            if fir == 1 : 
                s.ckzm()
            elif fir == 0 : 
                s.zui()
            elif fir == 2 : 
                s.wpzl(o = 1)
            elif fir == 4 : 
                s.fwzl(o = 1)
            elif fir == 7 : 
                s.zhjn()
            elif fir == 3 : 
                s.tfzl(o = 1)
            elif fir == 9 : 
                s.open_txt()
            elif fir == 6 : 
                s.zjcx()
            elif fir == 8 : 
                s.new()
            elif fir == 5 : 
                s.yxmh()
            elif fir == 10 : 
                s.god_team()
            elif fir == 11 : 
                s.zcd(n = 100)
            elif fir > 11 : 
                s.zcd(n = fir)
            pass
        return None
    elif et == 3 : 
        if  not (s.zc and s.men) and s.cd_bg and es == 167 : 
            try :
                s.zcd_pos_list_old = s.zcd_pos_list[ : ]
            except :
                s.zcd_pos_list_old = 0
            return None
        s.key = 1
        if s.men_2 or s.men : 
            if es == 16 : 
                s.pos_menu(-1)
                e32.ao_sleep(0.3)
                while s.key : 
                    e32.ao_sleep(0.01)
                    s.pos_menu(-1)
                pass
            elif es == 17 : 
                s.pos_menu(1)
                e32.ao_sleep(0.3)
                while s.key : 
                    e32.ao_sleep(0.01)
                    s.pos_menu(1)
                pass
            elif es == 14 : 
                s.men = 0
                s.menu(1)
                s.menu()
            elif es == 15 : 
                s.menu_2()
            elif es == 167 or 48 < es < (len(s.menu_list) + 49) : 
                menu_d = {cn('进入官网') : 2, cn('关于软件') : 3, cn('查看帮助') : 4, cn('检查更新') : 5, cn('安装资料') : 6, cn('消耗品') : 8, cn('攻击力') : 9, cn('法术强度') : 10, cn('物理护甲') : 11, cn('魔法抵抗') : 12, cn('生命上限') : 13, cn('法力上限') : 14, cn('法力回复') : 15, cn('生命回复') : 16, cn('攻击速度') : 17, cn('技能冷却') : 19, cn('暴击几率') : 18, cn('生命偷取') : 20, cn('法术吸血') : 21, cn('法术穿透') : 22, cn('护甲穿透') : 23, cn('对比英雄') : 24, cn('战绩查询') : 25, cn('查找英雄') : 26, cn('查看攻略') : 27, cn('有蓝') : 28, cn('无蓝') : 29, cn('半肉') : 30, cn('坦克') : 31, cn('输出为主') : 32, cn('魔法输出') : 33, cn('压制型') : 34, cn('常用技能') : 35, cn('技能远程') : 36, cn('攻守远程') : 37, cn('耐打近战') : 38, cn('传统') : 39, cn('AD_1') : 40, cn('AD_2') : 41, cn('AP技能') : 42, cn('打野坦克') : 43, cn('打野新手') : 44, cn('查看周免') : 1, cn('物品资料') : 7, cn('消耗品') : 8, cn('全部物品') : 45, cn('移动速度') : 46, cn('召唤技能') : 47, cn('S3新物品') : 49, cn('查看符文') : 48, cn('选择印记') : 50, cn('选择符印') : 51, cn('选择雕纹') : 52, cn('选择精华') : 53, cn('印记') : 50, cn('符印') : 51, cn('雕纹') : 52, cn('精华') : 53, cn('清空符文') : 54, cn('符文模拟') : 55, cn('.....') : 56, cn('装备统计') : 57, cn('天赋资料') : 58, cn('天赋模拟') : 59, cn('重新加点') : 60, cn('软件设置') : 61, cn('资助作者') : 62, cn('法　　师') : 63, cn('战　　士') : 64, cn('后　　期') : 65, cn('坦　　克') : 66, cn('辅　　助') : 67, cn('无 蓝 条') : 68, cn('隐　　身') : 69, cn('全部英雄') : 70, cn('本周免费') : 71, cn('修改列表') : 72, cn('收藏列表') : 73, cn('第一页') : 74, cn('第二页') : 75, cn('第三页') : 76, cn('音效_1') : 77, cn('音效_2') : 78, cn('音效_3') : 79, cn('音效_4') : 80, cn('音效_5') : 81, cn('修改英雄') : 82, cn('英雄背景') : 83}
                if es == 167 : 
                    if s.men_2 : 
                        tt = s.menu_list[s.menu_pos_2]
                    else : 
                        tt = s.menu_list[s.menu_pos]
                    pass
                else : 
                    tt = s.menu_list[(es - 49)]
                s.popup = -1
                e32.ao_sleep(0)
                if s.men_2 : 
                    s.men_2 = 0
                    s.key = 0
                    if s.one and tt in s.h_list : 
                        s.out(0, 1)
                        s.run = 1
                        s.y_one = ((s.h_list[tt] - s.y) / 10)
                        for i in xrange(10):
                            s.y += s.y_one
                            s.redraw(())
                        s.men = 0
                        s.run = 0
                        return None
                    pass
                elif es != 167 : 
                    s.menu_pos = (es - 49)
                    s.pos_menu(0)
                s.men = 0
                if tt.find(cn('►')) != -1 : 
                    s.key = 0
                    return s.menu_2()
                fir = menu_d[tt]
                if fir == 1 : 
                    s.ckzm()
                elif fir == 2 : 
                    s.open_uc()
                elif fir == 3 : 
                    s.about()
                elif fir == 4 : 
                    s.help()
                elif fir == 5 : 
                    s.jcgx()
                elif fir == 6 : 
                    s.updata()
                elif fir == 7 : 
                    s.wpzl(o = 1)
                elif fir == 8 : 
                    s.wpzl(n = 1)
                elif fir == 9 : 
                    s.wpzl(n = 7)
                elif fir == 10 : 
                    s.wpzl(n = 9)
                elif fir == 11 : 
                    s.wpzl(n = 4)
                elif fir == 12 : 
                    s.wpzl(n = 6)
                elif fir == 13 : 
                    s.wpzl(n = 11)
                elif fir == 14 : 
                    s.wpzl(n = 10)
                elif fir == 15 : 
                    s.wpzl(n = 2)
                elif fir == 16 : 
                    s.wpzl(n = 3)
                elif fir == 17 : 
                    s.wpzl(n = 8)
                elif fir == 18 : 
                    s.wpzl(n = 14)
                elif fir == 19 : 
                    s.wpzl(n = 12)
                elif fir == 20 : 
                    s.wpzl(n = 13)
                elif fir == 21 : 
                    s.wpzl(n = 16)
                elif fir == 22 : 
                    s.wpzl(n = 17)
                elif fir == 23 : 
                    s.wpzl(n = 18)
                elif fir == 24 : 
                    s.dbyx()
                elif fir == 25 : 
                    s.zjcx()
                elif fir == 26 : 
                    s.finder()
                elif fir == 27 : 
                    s.open_txt()
                elif fir == 45 : 
                    s.wpzl()
                elif fir == 46 : 
                    s.wpzl(n = 5)
                elif fir == 47 : 
                    s.zhjn()
                elif fir == 48 : 
                    s.fwzl(o = 1)
                elif fir == 49 : 
                    s.wpzl(n = 15)
                elif fir == 50 : 
                    s.fwzl()
                elif fir == 51 : 
                    s.fwzl(n = 1)
                elif fir == 52 : 
                    s.fwzl(n = 2)
                elif fir == 53 : 
                    s.fwzl(n = 3)
                elif fir == 54 : 
                    s.mnlist = []
                    s.fw_mn()
                elif fir == 55 : 
                    s.fw_mn()
                elif fir == 56 : 
                    s.sound()
                elif fir == 57 : 
                    s.zbmn()
                elif fir == 58 : 
                    s.tfzl(o = 1)
                elif fir == 59 : 
                    s.tfmn()
                elif fir == 60 : 
                    s.tfmn_list = [0 for i in xrange(56)]
                    s.tfn = s.tf_pos = 0
                    s.tfzl()
                elif fir == 61 : 
                    s.set()
                elif fir == 62 : 
                    s.zzzz()
                elif fir == 63 : 
                    s.zui(o = 3)
                elif fir == 64 : 
                    s.zui(o = 1)
                elif fir == 65 : 
                    s.zui(o = 4)
                elif fir == 66 : 
                    s.zui(o = 7)
                elif fir == 67 : 
                    s.zui(o = 2)
                elif fir == 68 : 
                    s.zui(o = 5)
                elif fir == 69 : 
                    s.zui(o = 6)
                elif fir == 70 : 
                    s.zui()
                elif fir == 71 : 
                    s.zui(o = 100)
                elif fir == 72 : 
                    s.bjlb()
                elif fir == 73 : 
                    s.zui(o = 200)
                elif fir == 74 : 
                    if s.ne : 
                        s.getnew(n = 1)
                    else : 
                        s.zjxx_page(1, 0)
                    pass
                elif fir == 75 : 
                    if s.ne : 
                        s.getnew(n = 2)
                    else : 
                        s.zjxx_page(2, 0)
                    pass
                elif fir == 76 : 
                    if s.ne : 
                        s.getnew(n = 3)
                    else : 
                        s.zjxx_page(3, 0)
                    pass
                elif 77 <= fir <= 81 : 
                    s.path_sound = ('e:\\data\\lolbox\\%s' % s.list_sound[(fir - 77)])
                    s.sound()
                elif fir == 82 : 
                    s.Diy()
                elif fir == 83 : 
                    s.yxbj()
                elif (fir - 27) > 0 : 
                    s.tfmn_list = s.tfgl_list[(fir - 28)][ : ]
                    s.tfn = 0
                    s.tfzl()
                pass
            else : 
                pass
            pass
        elif s.popup_zt : 
            o = s.popup_pos
            s.run = 0
            if es == 17 : 
                s.popup_pos += 1
                if  not (s.popup_pos < s.len_txt) : 
                    s.popup_pos = 0
                s.pos_popup()
                e32.ao_sleep(0.3)
                while s.key : 
                    s.popup_pos += 1
                    if  not (s.popup_pos < s.len_txt) : 
                        s.popup_pos -= 1
                        break
                    s.pos_popup()
                    e32.ao_sleep(0.03)
                pass
            elif es == 16 : 
                s.popup_pos -= 1
                if  not (-1 < s.popup_pos) : 
                    s.popup_pos = (s.len_txt - 1)
                s.pos_popup()
                e32.ao_sleep(0.3)
                while s.key : 
                    s.popup_pos -= 1
                    if  not (-1 < s.popup_pos) : 
                        s.popup_pos += 1
                        break
                    s.pos_popup()
                    e32.ao_sleep(0.03)
                pass
            elif es == 14 : 
                for i in xrange((7 - (2 * s.orientation))):
                    s.popup_pos -= 2
                    if  not (-1 < s.popup_pos) : 
                        s.popup_pos = 0
                    s.pos_popup()
                pass
            elif es == 15 : 
                for i in xrange((7 - (2 * s.orientation))):
                    s.popup_pos += 2
                    if  not (s.popup_pos < s.len_txt) : 
                        s.popup_pos = (s.len_txt - 1)
                    s.pos_popup()
                pass
            elif es == 167 : 
                s.popup = s.popup_pos
            pass
        elif s.team : 
            if es == 15 : 
                s.run = 1
                for i in xrange(10):
                    s.y += (32 - (8 * s.orientation))
                    if s.y > (s.h_team - 320) + (80 * s.orientation) : 
                        s.y = (s.h_team - 320) + (80 * s.orientation)
                        break
                    s.redraw(())
                    e32.ao_sleep(0)
                s.redraw(())
                s.run = 0
                e32.ao_sleep(0.25)
                s.run = 1
                while s.key : 
                    for i in xrange(10):
                        s.y += (32 - (8 * s.orientation))
                        if s.y > (s.h_team - 320) + (80 * s.orientation) : 
                            s.y = (s.h_team - 320) + (80 * s.orientation)
                            break
                        s.redraw(())
                        e32.ao_sleep(0)
                    s.redraw(())
                    e32.ao_sleep(0.02)
                pass
            elif es == 14 : 
                s.run = 1
                for i in xrange(10):
                    s.y -= (32 - (8 * s.orientation))
                    if s.y < 0 : 
                        s.y = 0
                        break
                    s.redraw(())
                    e32.ao_sleep(0)
                s.redraw(())
                s.run = 0
                e32.ao_sleep(0.25)
                s.run = 1
                while s.key : 
                    for i in xrange(10):
                        s.y -= (32 - (8 * s.orientation))
                        if s.y < 0 : 
                            s.y = 0
                            break
                        s.redraw(())
                        e32.ao_sleep(0)
                    s.redraw(())
                    e32.ao_sleep(0.02)
                pass
            elif es == 17 : 
                s.run = 1
                for i in xrange(10):
                    s.y += 8
                    if s.y > (s.h_team - 320) + (80 * s.orientation) : 
                        s.y = (s.h_team - 320) + (80 * s.orientation)
                        break
                    s.redraw(())
                    e32.ao_sleep(0)
                s.redraw(())
                s.run = 0
                e32.ao_sleep(0.25)
                s.run = 1
                while s.key : 
                    for i in xrange(10):
                        s.y += 8
                        if s.y > (s.h_team - 320) + (80 * s.orientation) : 
                            s.y = (s.h_team - 320) + (80 * s.orientation)
                            break
                        s.redraw(())
                        e32.ao_sleep(0)
                    s.redraw(())
                    e32.ao_sleep(0.02)
                pass
            elif es == 16 : 
                s.run = 1
                for i in xrange(10):
                    s.y -= 8
                    if s.y < 0 : 
                        s.y = 0
                        break
                    s.redraw(())
                    e32.ao_sleep(0)
                s.redraw(())
                s.run = 0
                e32.ao_sleep(0.25)
                s.run = 1
                while s.key : 
                    for i in xrange(10):
                        s.y -= 8
                        if s.y < 0 : 
                            s.y = 0
                            break
                        s.redraw(())
                        e32.ao_sleep(0)
                    s.redraw(())
                    e32.ao_sleep(0.02)
                pass
            s.run = 0
        elif s.diy : 
            pass
        elif s.hel : 
            if es == 16 : 
                s.key_16 = 1
                while s.key_16 : 
                    s.y -= 3
                    if s.y < 0 : 
                        s.y = 0
                    e32.ao_yield()
                    s.redraw(())
                s.redraw(())
            elif es == 17 : 
                s.key_17 = 1
                while s.key_17 : 
                    s.y += 3
                    if s.y > (s.img.size[1] - 320) + (80 * s.orientation) : 
                        s.y = (s.img.size[1] - 320) + (80 * s.orientation)
                        if s.y < 0 : 
                            s.y = 0
                        pass
                    e32.ao_yield()
                    s.redraw(())
                s.redraw(())
            pass
        elif s.mh or s.zjx : 
            if es == 15 : 
                s.key_15 = 1
                while s.key_15 : 
                    if s.mh : 
                        s.x += 3
                        if s.x > ((s.img.size[0] - 240) - (80 * s.orientation)) : 
                            s.x = ((s.img.size[0] - 240) - (80 * s.orientation))
                            s.redraw(())
                            break
                        pass
                    else : 
                        s.x_ += 3
                        if s.x_ > ((s.img.size[0] - 240) - (80 * s.orientation)) : 
                            s.x_ = ((s.img.size[0] - 240) - (80 * s.orientation))
                            s.x = s.x_
                            s.redraw(())
                            break
                        if 270 < (s.x_ + 240) + (80 * s.orientation) < 310 : 
                            s.x = ((290 - 240) - (80 * s.orientation))
                        else : 
                            s.x = s.x_
                    s.redraw(())
                    e32.ao_yield()
                pass
            elif es == 14 : 
                s.key_14 = 1
                while s.key_14 : 
                    if s.mh : 
                        s.x -= 3
                        if s.x < 0 : 
                            s.x = 0
                            s.redraw(())
                            break
                        pass
                    else : 
                        s.x_ -= 3
                        if s.x_ < 0 : 
                            s.x_ = 0
                            s.x = s.x_
                            s.redraw(())
                            break
                        if 270 < (s.x_ + 240) + (80 * s.orientation) < 310 : 
                            s.x = ((290 - 240) - (80 * s.orientation))
                        else : 
                            s.x = s.x_
                    s.redraw(())
                    e32.ao_yield()
                pass
            elif es == 16 : 
                s.key_16 = 1
                s.downpage = 0
                while s.key_16 : 
                    s.y -= 3
                    if s.y < 0 : 
                        s.y = 0
                        if  not (s.uppage) : 
                            if s.mh and s.popup_pos_2 : 
                                s.uppage = 1
                                s.redraw(())
                            break
                        else : 
                            s.run = 1
                            s.y = s.x = 0
                            s.redraw((), 0.01)
                            e32.ao_yield()
                            s.uppage = s.downpage = 0
                            s.popup_pos_2 -= 1
                            path = 'e:\\data\\lolbox\\lom\\' + s.mh_list[s.popup_pos_2]
                            s.open_img(path)
                            if  not (s.mh_tp) : 
                                s.mh_tp = 1
                                s.run = 0
                                s.event({'scancode' : 167, 'type' : 3})
                            s.key_16 = 0
                            s.run = 0
                        pass
                    s.redraw(())
                    e32.ao_yield()
                pass
            elif es == 17 : 
                s.key_17 = 1
                s.uppage = 0
                while s.key_17 : 
                    s.y += 3
                    if s.y > (s.img.size[1] - 320) + (80 * s.orientation) : 
                        s.y = (s.img.size[1] - 320) + (80 * s.orientation)
                        if s.y < 0 : 
                            s.y = 0
                        if  not (s.downpage) : 
                            if s.mh and s.popup_pos_2 != (len(s.mh_list) - 1) : 
                                s.downpage = 1
                                s.redraw(())
                            break
                        else : 
                            s.run = 1
                            s.y = s.x = 0
                            s.redraw((), 0.01)
                            e32.ao_yield()
                            s.popup_pos_2 += 1
                            s.uppage = s.downpage = 0
                            path = 'e:\\data\\lolbox\\lom\\' + s.mh_list[s.popup_pos_2]
                            s.open_img(path)
                            if  not (s.mh_tp) : 
                                s.mh_tp = 1
                                s.run = 0
                                s.event({'scancode' : 167, 'type' : 3})
                            s.key_17 = 0
                            s.run = 0
                        pass
                    s.redraw(())
                    e32.ao_yield()
                pass
            elif es == 52 and s.mh : 
                if  not (s.popup_pos_2) : 
                    s.key = 0
                    return None
                s.run = 1
                s.y = s.x = 0
                s.redraw((), 0.01)
                e32.ao_yield()
                s.uppage = s.downpage = 0
                s.popup_pos_2 -= 1
                path = 'e:\\data\\lolbox\\lom\\' + s.mh_list[s.popup_pos_2]
                s.open_img(path)
                s.run = 0
                if  not (s.mh_tp) : 
                    s.mh_tp = 1
                    s.event({'scancode' : 167, 'type' : 3})
                else : 
                    s.redraw(())
                pass
            elif es == 54 and s.mh : 
                if s.popup_pos_2 == (len(s.mh_list) - 1) : 
                    s.key = 0
                    return None
                s.run = 1
                s.y = s.x = 0
                s.redraw((), 0.01)
                e32.ao_yield()
                s.uppage = s.downpage = 0
                s.popup_pos_2 += 1
                path = 'e:\\data\\lolbox\\lom\\' + s.mh_list[s.popup_pos_2]
                s.open_img(path)
                s.run = 0
                if  not (s.mh_tp) : 
                    s.mh_tp = 1
                    s.event({'scancode' : 167, 'type' : 3})
                else : 
                    s.redraw(())
                pass
            elif es == 1 and s.zjx : 
                try :
                    del s.zj_dir[s.zjx_now]
                    open('e:\\data\\lolbox\\app\\zj.save', 'w').write('s.zj_dir=' + repr(s.zj_dir))
                except :
                    pass
                pass
            elif es == 167 : 
                if s.mh : 
                    s.y = s.x = 0
                    s.uppage = s.downpage = 0
                    s.run = 1
                    if s.mh_tp : 
                        s.redraw((), k = 0.01)
                        e32.ao_yield()
                        w2, h2 = s.img.size
                        s.mh_tp = 0
                        s.img_mh = new((w2, h2))
                        s.img_mh.blit(s.img)
                        s.img = s.img.resize(((240 + (80 * s.orientation)), ((((240.0 + (80 * s.orientation))) * h2) / w2)))
                    else : 
                        s.mh_tp = 1
                        s.img = new(s.img_mh.size)
                        s.img.blit(s.img_mh)
                    pass
                else : 
                    s.img.save(cn('c:\lol控_战绩截图.jpeg'))
                    appuifw.note(cn('战绩截图已成功保存到c盘'), 'conf', 1)
                s.redraw(())
                s.run = 0
            pass
        elif s.zzz : 
            s.run = 1
            if es == 17 : 
                if  not (s.h_zz) : 
                    s.h_zz = 1
                    for i in xrange(10):
                        s.y += 8 + (8 * s.orientation)
                        s.redraw(())
                        e32.ao_yield()
                    pass
                pass
            elif es == 16 : 
                if s.h_zz : 
                    s.h_zz = 0
                    for i in xrange(10):
                        s.y -= 8 + (8 * s.orientation)
                        s.redraw(())
                        e32.ao_yield()
                    pass
                pass
            s.run = 0
        elif s.zj : 
            s.run = 1
            if es == 17 : 
                if  not (s.h_zj) : 
                    s.h_zj = 1
                    for i in xrange(10):
                        s.y += 12 + (8 * s.orientation)
                        s.redraw(())
                        e32.ao_yield()
                    pass
                pass
            elif es == 16 : 
                if s.h_zj : 
                    s.h_zj = 0
                    for i in xrange(10):
                        s.y -= 12 + (8 * s.orientation)
                        s.redraw(())
                        e32.ao_yield()
                    pass
                pass
            s.run = 0
        elif s.zh : 
            if es == 15 : 
                s.pos_zh += 1
                s.zhjn()
                e32.ao_sleep(0.3)
                while s.key : 
                    s.pos_zh += 1
                    s.zhjn()
                    e32.ao_sleep(0)
                pass
            elif es == 14 : 
                s.pos_zh -= 1
                s.zhjn()
                e32.ao_sleep(0.3)
                while s.key : 
                    s.pos_zh -= 1
                    s.zhjn()
                    e32.ao_sleep(0)
                pass
            pass
        elif s.zc : 
            if  not (s.cd_bg) : 
                if es == 17 : 
                    s.key_17 = 1
                    s.zcd_pos += 1
                    s.pos_zcd()
                    s.whil = 1
                    e32.ao_sleep(0.3)
                    while s.key_17 : 
                        s.zcd_pos += 1
                        e32.ao_sleep(0.01)
                        s.pos_zcd()
                    s.whil = 0
                elif es == 16 : 
                    s.key_16 = 1
                    s.zcd_pos -= 1
                    s.pos_zcd()
                    e32.ao_sleep(0.3)
                    s.whil = 1
                    while s.key_16 : 
                        s.zcd_pos -= 1
                        e32.ao_sleep(0.01)
                        s.pos_zcd()
                    s.whil = 0
                pass
            else : 
                if es == 15 : 
                    s.key_15 = 1
                elif es == 14 : 
                    s.key_14 = 1
                elif es == 16 : 
                    s.key_16 = 1
                elif es == 17 : 
                    s.key_17 = 1
                if s.whil : 
                    s.run = 0
                    return None
                s.whil = 1
                e32.ao_sleep(0)
                while s.whil and s.key_15 or s.key_14 or s.key_16 or s.key_17 : 
                    if s.key_15 : 
                        s.zcd_pos[0] += 4
                    if s.key_14 : 
                        s.zcd_pos[0] -= 4
                    if s.key_17 : 
                        s.zcd_pos[1] += 4
                    if s.key_16 : 
                        s.zcd_pos[1] -= 4
                    if s.zcd_pos[1] > (291 - (80 * s.orientation)) : 
                        s.zcd_pos[1] = (291 - (80 * s.orientation))
                    elif s.zcd_pos[1] < -17 : 
                        s.zcd_pos[1] = -17
                    if s.zcd_pos[0] > (219 + (80 * s.orientation)) : 
                        s.zcd_pos[0] = (219 + (80 * s.orientation))
                    elif s.zcd_pos[0] < -20 : 
                        s.zcd_pos[0] = -20
                        s.pos_zcd()
                        break
                    e32.ao_yield()
                    s.pos_zcd()
                s.whil = 0
                e32.ao_sleep(0)
            if  not (s.cd_bg) and es == 167 or 48 < es < 58 : 
                s.y4 = s.y
                s.zc = s.y = 0
                e32.ao_sleep(0)
                kb = {'查看周免' : 1, '英雄资料' : 2, '物品资料' : 3, '符文资料' : 4, '召唤师技能' : 5, '天赋资料' : 6, '关于软件' : 11, '软件帮助' : 10, '进入官网' : 9, '检查更新' : 8, '安装更新包' : 7, '查看攻略' : 12, '战绩查询' : 13, '查看新闻' : 14, '英雄漫画' : 15, '神级团队' : 16}
                if es == 167 : 
                    fir = kb[s.listtxt[s.zcd_pos][0]]
                else : 
                    fir = kb[s.listtxt[(es - 49)][0]]
                if fir == 1 : 
                    s.ckzm()
                elif fir == 2 : 
                    s.zui()
                elif fir == 3 : 
                    s.wpzl(o = 1)
                elif fir == 4 : 
                    s.fwzl(o = 1)
                elif fir == 5 : 
                    s.zhjn()
                elif fir == 6 : 
                    s.tfzl(o = 1)
                elif fir == 7 : 
                    s.updata()
                elif fir == 8 : 
                    s.jcgx()
                elif fir == 9 : 
                    s.open_uc()
                elif fir == 10 : 
                    s.help()
                elif fir == 11 : 
                    s.about()
                elif fir == 12 : 
                    s.open_txt()
                elif fir == 13 : 
                    s.zjcx()
                elif fir == 14 : 
                    s.new()
                elif fir == 15 : 
                    s.yxmh()
                elif fir == 16 : 
                    s.god_team()
                pass
            else : 
                pass
            pass
        elif s.tfzt : 
            if s.tfzt == 2 : 
                return None
            if es == 14 : 
                if s.tf_pos == 0 : 
                    return None
                s.tf_pos -= 1
                s.pos_tf()
                e32.ao_sleep(0.3)
                while s.key : 
                    if s.tf_pos == 0 : 
                        return None
                    s.tf_pos -= 1
                    s.pos_tf()
                    e32.ao_sleep(0.05)
                pass
            elif es == 16 : 
                x3, y3 = s.tf_list[s.tfn][s.tf_pos]
                for i in xrange(1, 4):
                    if (x3, (y3 - i)) in s.tf_list[s.tfn] : 
                        s.tf_pos = s.tf_list[s.tfn].index((x3, (y3 - i)))
                        s.pos_tf()
                        break
                e32.ao_sleep(0.3)
                while s.key : 
                    x3, y3 = s.tf_list[s.tfn][s.tf_pos]
                    for i in xrange(1, 4):
                        if (x3, (y3 - i)) in s.tf_list[s.tfn] : 
                            s.tf_pos = s.tf_list[s.tfn].index((x3, (y3 - i)))
                            s.pos_tf()
                            break
                    e32.ao_sleep(0.05)
                pass
            elif es == 15 : 
                if s.tf_pos == (len(s.tf_list[s.tfn]) - 1) : 
                    return None
                s.tf_pos += 1
                s.pos_tf()
                e32.ao_sleep(0.3)
                while s.key : 
                    if s.tf_pos == (len(s.tf_list[s.tfn]) - 1) : 
                        return None
                    s.tf_pos += 1
                    s.pos_tf()
                    e32.ao_sleep(0.05)
                pass
            elif es == 17 : 
                x3, y3 = s.tf_list[s.tfn][s.tf_pos]
                for i in xrange(1, 4):
                    if (x3, y3 + i) in s.tf_list[s.tfn] : 
                        s.tf_pos = s.tf_list[s.tfn].index((x3, y3 + i))
                        s.pos_tf()
                        break
                e32.ao_sleep(0.3)
                while s.key : 
                    x3, y3 = s.tf_list[s.tfn][s.tf_pos]
                    for i in xrange(1, 4):
                        if (x3, y3 + i) in s.tf_list[s.tfn] : 
                            s.tf_pos = s.tf_list[s.tfn].index((x3, y3 + i))
                            s.pos_tf()
                            break
                    e32.ao_sleep(0.05)
                pass
            elif es == 52 : 
                s.tfn -= 1
                if s.tfn == -1 : 
                    s.tfn = 2
                s.tfzl()
            elif es == 54 : 
                s.tfn += 1
                if s.tfn == 3 : 
                    s.tfn = 0
                s.tfzl()
            if s.tfn == 1 : 
                a = 19
            elif s.tfn == 2 : 
                a = 38
            else : 
                a = 0
            a += s.tf_pos
            s.key = 0
            if es == 56 and s.tfzt == 3 : 
                mk = s.tfmn_list[a]
                if mk == 0 : 
                    return None
                s.tfmn_list[a] = (mk - 1)
                s.tfzl(n = 1)
            if es == 50 and s.tfzt == 3 : 
                if  not (s.pd(a)) or s.tfmnn[3] == 30 : 
                    return None
                mk = s.tfmn_list[a]
                if mk == len(s.tf[a]['level']) : 
                    return None
                s.tfmn_list[a] = (mk + 1)
                s.tfzl(n = 1)
            elif es == 167 : 
                s.open_tf()
            pass
        elif s.zm : 
            if s.zm == 1 : 
                if es == 167 : 
                    s.gxzm()
                pass
            elif es == 167 : 
                s.pos_zm(100)
            elif es == 16 : 
                s.pos_zm(-1)
            elif es == 17 : 
                s.pos_zm(1)
            return None
        elif s.wp : 
            if es == 14 : 
                s.pos_wp(-1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_wp(-1, 1)
                pass
            elif es == 15 : 
                s.pos_wp(1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_wp(1, 1)
                pass
            elif es == 16 : 
                s.pos_wp((-3 - s.orientation))
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_wp((-3 - s.orientation), 1)
                pass
            elif es == 17 : 
                s.pos_wp((3 + s.orientation))
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_wp((3 + s.orientation), 1)
                pass
            elif es == 167 : 
                if  not (s.zb) : 
                    s.open_zb(1)
                pass
            elif es == 49 : 
                s.finder_2()
            pass
        elif  not (s.fw and s.fwmnz) : 
            if es == 16 : 
                s.pos_fw(-1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_fw(-1, 1)
                pass
            elif es == 17 : 
                s.pos_fw(1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_fw(1, 1)
                pass
            elif es == 14 : 
                s.pos_fw(-7)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_fw(-7, 1)
                pass
            elif es == 15 : 
                s.pos_fw(7)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_sleep(0)
                    s.pos_fw(7, 1)
                pass
            elif es == 167 : 
                if  not (s.rune) : 
                    if s.fwmn : 
                        na = s.runelist[s.fw_pos]
                        s.mnlist[['印记', '符印', '雕纹', '精华'].index(en(na[-2 : ]))] = en(na)
                        s.fw_mn()
                    else : 
                        s.open_fw(1)
                    pass
                pass
            pass
        elif s.zy : 
            if es == 16 : 
                s.move_yx(-1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_yield()
                    s.move_yx(-1, 4)
                pass
            elif es == 17 : 
                s.move_yx(1)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_yield()
                    s.move_yx(1, 4)
                pass
            elif es == 14 : 
                s.move_yx(-4)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_yield()
                    s.move_yx(-4, 4)
                pass
            elif es == 15 : 
                s.move_yx(4)
                e32.ao_sleep(0.25)
                while  not (s.key and s.run) : 
                    s.run = 1
                    e32.ao_yield()
                    s.move_yx(4, 4)
                pass
            if s.tx : 
                return None
            if es == 49 : 
                s.finder()
            elif es == 50 : 
                for i in xrange((4 - s.orientation)):
                    if s.y > 10 : 
                        s.y -= 79
                    s.move_yx(-1, 4)
                pass
            elif  not (es == 56 and s.tx) : 
                for i in xrange((4 - s.orientation)):
                    if s.y < (79 * (s.h_yx - 5) + s.orientation) : 
                        s.y += 79
                    s.move_yx(1, 4)
                pass
            else : 
                if es == 167 : 
                    if s.db : 
                        s.db_list.append(s.name_list[s.move_yx(100)])
                        s.img_dbzt.blit(s.img_z)
                        s.img_dbzt.polygon(s.rim(0, 0, (240 + (80 * s.orientation)), 25), s.color_frame, width = 1)
                        s.img_dbzt.text((10, 20), cn('请再点击一个,已选中:') + cn(s.name_list[s.move_yx(100)]), s.f_color, font = ('title', 14))
                        if len(s.db_list) == 2 : 
                            s.dbyx_ok()
                        else : 
                            s.pos_yx()
                        pass
                    elif s.bj : 
                        n = s.move_yx(100)
                        name = s.name_list[n]
                        if name in s.fa_list : 
                            color = s.color_likebg
                            s.fa_list.remove(name)
                        else : 
                            color = s.color_like
                            s.fa_list.append(name)
                        x_fa = ((((n % (3 + s.orientation))) * 75) + 67)
                        y_fa = ((((n / (3 + s.orientation))) * 79) + 20)
                        s.img_zui.text((x_fa, y_fa), cn(s.sign), color, font = ('title', 14))
                        s.pos_yx()
                    else : 
                        s.out(s.move_yx(100))
                    pass
                pass
            pass
        elif s.fwmnz : 
            if es == 16 : 
                s.y_mn = 0
            elif es == 17 : 
                s.y_mn = 1
            s.fw_mn(1)
        elif es == 16 : 
            if s.pos_zb(1) and s.zb_pos > 0 : 
                s.zb_pos -= 1
                s.pos_zb()
            elif s.pos_jn(1) and s.jn_pos > 0 : 
                s.jn_pos -= 1
                s.pos_jn()
            else : 
                s.move_one(-4)
            e32.ao_sleep(0.25)
            while  not (s.key and s.run) : 
                s.run = 1
                e32.ao_sleep(0.02)
                if s.pos_zb(1) and s.zb_pos > 0 : 
                    s.zb_pos -= 1
                    s.pos_zb()
                elif s.pos_jn(1) and s.jn_pos > 0 : 
                    s.jn_pos -= 1
                    s.pos_jn()
                else : 
                    s.move_one(-4, 1)
            pass
        elif es == 17 : 
            if s.pos_zb(1) and s.zb_pos < 7 : 
                s.zb_pos += 1
                s.pos_zb()
            elif s.pos_jn(1) and s.jn_pos < 6 : 
                s.jn_pos += 1
                s.pos_jn()
            else : 
                s.move_one(4)
            e32.ao_sleep(0.25)
            while  not (s.key and s.run) : 
                s.run = 1
                e32.ao_sleep(0.02)
                if s.pos_zb(1) and s.zb_pos < 7 : 
                    s.zb_pos += 1
                    s.pos_zb()
                elif s.pos_jn(1) and s.jn_pos < 6 : 
                    s.jn_pos += 1
                    s.pos_jn()
                else : 
                    s.move_one(4, 1)
            pass
        elif es == 14 : 
            s.move_one((-16 + (4 * s.orientation)))
            e32.ao_sleep(0.25)
            while  not (s.key and s.run) : 
                s.run = 1
                e32.ao_sleep(0.02)
                s.move_one((-16 + (4 * s.orientation)), 1)
            pass
        elif es == 15 : 
            s.move_one((16 - (4 * s.orientation)))
            e32.ao_sleep(0.25)
            while  not (s.key and s.run) : 
                s.run = 1
                e32.ao_sleep(0.02)
                s.move_one((16 - (4 * s.orientation)), 1)
            pass
        elif  not (es == 167 and s.zb) : 
            if s.pos_zb(1) and 0 < s.zb_pos < 7 : 
                s.zb = 1
                s.open_zb()
            elif s.pos_jn(1) and 0 < s.jn_pos < 6 : 
                s.open_jn()
            elif s.pos_tf(1) : 
                s.tfzt = 3
                s.tfzl(o = 1, list = s.tfgl_list[s.tfmn_listn])
            pass
        elif  not (0 < s.zb_pos < 7 and s.pos_zb(1) and s.tx) : 
            s.run = 1
            s.key = 0
            e32.ao_yield()
            na = s.txt_one.split('[[')[1].split(']]')[0].split('\n')[0]
            if es == 50 : 
                if s.zb_pos == 1 : 
                    s.run = 0
                    return None
                a = s.wlist.pop((s.zb_pos - 2))
                s.wlist.insert((s.zb_pos - 1), a)
                s.zb_pos -= 1
                name = s.get_name(en(s.wlist[(s.zb_pos - 1)]))
                x_zb = s.weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                s.img_hc.blit(s.img_t.resize((40, 40)), ((( - (40 + (15 * s.orientation))) * (s.zb_pos - 1)), ( - s.h_zb - 27)), mask = s.img_zb_mask)
                name = s.get_name(en(s.wlist[s.zb_pos]))
                x_zb = s.weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                s.img_hc.blit(s.img_t.resize((40, 40)), ((( - (40 + (15 * s.orientation))) * s.zb_pos), ( - s.h_zb - 27)), mask = s.img_zb_mask)
                s.pos_zb()
                txt2 = s.txt_one.replace('[[' + na, '[[' + ','.join(s.wlist))
                f = open(s.txt_path, 'w')
                f.write(txt2.encode('u16'))
                f.close()
            elif es == 56 : 
                if s.zb_pos == 6 : 
                    s.run = 0
                    return None
                a = s.wlist.pop(s.zb_pos)
                s.wlist.insert((s.zb_pos - 1), a)
                s.zb_pos += 1
                name = s.get_name(en(s.wlist[(s.zb_pos - 1)]))
                x_zb = s.weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                s.img_hc.blit(s.img_t.resize((40, 40)), ((( - (40 + (15 * s.orientation))) * (s.zb_pos - 1)), ( - s.h_zb - 27)), mask = s.img_zb_mask)
                name = s.get_name(en(s.wlist[(s.zb_pos - 2)]))
                x_zb = s.weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                s.img_hc.blit(s.img_t.resize((40, 40)), ((( - (40 + (15 * s.orientation))) * (s.zb_pos - 2)), ( - s.h_zb - 27)), mask = s.img_zb_mask)
                s.pos_zb()
                txt2 = s.txt_one.replace('[[' + na, '[[' + ','.join(s.wlist))
                f = open(s.txt_path, 'w')
                f.write(txt2.encode('u16'))
                f.close()
            elif es == 49 : 
                list = [cn(i) for i in s.weapons_list[0]]
                index = s.popup_menu(list, cn('【选择装备】'), m = 1)
                if index == None : 
                    s.run = 0
                    return s.pos_zb()
                s.wlist[(s.zb_pos - 1)] = list[index]
                name = s.get_name(en(s.wlist[(s.zb_pos - 1)]))
                x_zb = s.weapons[name]
                s.img_t.blit(s.img_zb, (x_zb, 0))
                s.img_hc.blit(s.img_t.resize((40, 40)), ((( - (40 + (15 * s.orientation))) * (s.zb_pos - 1)), ( - s.h_zb - 27)), mask = s.img_zb_mask)
                s.pos_zb()
                txt2 = s.txt_one.replace('[[' + na, '[[' + ','.join(s.wlist))
                f = open(s.txt_path, 'w')
                f.write(txt2.encode('u16'))
                f.close()
            s.run = 0
        s.key = 0

