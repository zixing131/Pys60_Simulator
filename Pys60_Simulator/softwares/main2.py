# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


from Pys60_Simulator.pys60Core.getdate import *
from Pys60_Simulator.games.init_game import *
from Pys60_Simulator.pys60Core.images import *
import os
import random
import envy, appuifw as ap, e32, key_codes as kc

mypath=u"..\\..\\python\\pygame\\2048_maps\\"

def drawTime(string, locx, locy, img = readyimg):
    img.blit(DgtList[int(string[0])], target = (locx, locy), mask = Dgt_maskList[int(string[0])])
    img.blit(DgtList[int(string[1])], target = ((locx + 8), locy), mask = Dgt_maskList[int(string[1])])
    img.blit(sym_colon, target = ((locx + 16), locy), mask = sym_colon_mask)
    img.blit(DgtList[int(string[2])], target = ((locx + 24), locy), mask = Dgt_maskList[int(string[2])])
    img.blit(DgtList[int(string[3])], target = ((locx + 32), locy), mask = Dgt_maskList[int(string[3])])




def drawDate(string, locx, locy, img = hslimg):
    img.blit(DgtList[int(string[0])], target = (locx, locy), mask = Dgt_maskList[int(string[0])])
    img.blit(DgtList[int(string[1])], target = ((locx + 8), locy), mask = Dgt_maskList[int(string[1])])
    img.blit(sym_staff, target = ((locx + 16), locy), mask = sym_staff_mask)
    img.blit(DgtList[int(string[2])], target = ((locx + 24), locy), mask = Dgt_maskList[int(string[2])])
    img.blit(DgtList[int(string[3])], target = ((locx + 32), locy), mask = Dgt_maskList[int(string[3])])
    img.blit(sym_staff, target = ((locx + 40), locy), mask = sym_staff_mask)
    img.blit(DgtList[int(string[4])], target = ((locx + 48), locy), mask = Dgt_maskList[int(string[4])])
    img.blit(DgtList[int(string[5])], target = ((locx + 56), locy), mask = Dgt_maskList[int(string[5])])
    drawTime(string[-4 : ], (locx + 72), locy, img = hslimg)




def drawNum(num, img = readyimg, loc = score_num_loc):
    n, m = numImg(num)
    img.blit(n, target = loc, mask = m)
    img.blit(sym_back1, target = (undo_x, undo_y), mask = sym_back1_mask)
    img.blit(sym_back2, target = ((undo_x + 8), undo_y), mask = sym_back2_mask)
    if undo_chances > 9 : 
        img.blit(DgtList[(undo_chances / 10)], target = ((undo_x + 16), undo_y), mask = Dgt_maskList[(undo_chances / 10)])
    img.blit(DgtList[(undo_chances % 10)], target = ((undo_x + 24), undo_y), mask = Dgt_maskList[(undo_chances % 10)])
    img.blit(sym_staff, target = ((undo_x + 32), undo_y), mask = sym_staff_mask)
    img.blit(DgtList[(max_undo_chances / 10)], target = ((undo_x + 40), undo_y), mask = Dgt_maskList[(max_undo_chances / 10)])
    img.blit(DgtList[(max_undo_chances % 10)], target = ((undo_x + 48), undo_y), mask = Dgt_maskList[(max_undo_chances % 10)])




def drawBars(img = readyimg):
    img.blit(barslot[0], target = bar_loc[0], mask = barProgressMask(UndoBarScale[undo_option_flag]))
    img.blit(barslot[1], target = bar_loc[1], mask = barProgressMask((four * 10)))




def drawBarNotes(img = readyimg):
    img.blit(numImg(UndoOptionList[undo_option_flag])[0], target = (barnote1_x, barnote1_y), mask = numImg(UndoOptionList[undo_option_flag])[1])
    img.blit(DgtList[four], target = (barnote2_x, barnote2_y), mask = Dgt_maskList[four])
    img.blit(sym_staff, target = ((barnote2_x + 8), barnote2_y), mask = sym_staff_mask)
    img.blit(dgt_9, target = ((barnote2_x + 16), barnote2_y), mask = dgt_9_mask)




def drawBg(img = readyimg):
    img.blit(bg)




def drawBg2(img = readyimg):
    img.blit(bg2)




def paint_all():
    canvas.blit(readyimg)




def redraw(rect):
    paint_all()




def updateMenuImage():
    mnbg.blit(mnbg_back)
    for i in (0, 1, 2):
        if saveExist(i) : 
            mnbg.blit(greenlamb, target = led_loc[0][i], mask = led_mask)
    screen_back.blit(mnbg)
    if SelectedItem < 2 : 
        screen_back.blit(mouse, target = mouse_loc[SelectedItem][snlg_flag], mask = mouse_mask)
    else : 
        screen_back.blit(selection, target = selection_loc[SelectedItem], mask = selection_mask)
    screen_back.blit(barslot[0], target = bar_loc[0], mask = barProgressMask(UndoBarScale[undo_option_flag]))
    screen_back.blit(barslot[1], target = bar_loc[1], mask = barProgressMask((four * 10)))
    drawBarNotes(screen_back)
    longimg.blit(screen_back, target = (0, H))




def longimgBackup():
    longimg.blit(readyimg, target = (0, screen_loc))




def longimgRead():
    readyimg.blit(longimg, source = (0, screen_loc))




def longimgInit():
    longimg.blit(hpbg)
    updateMenuImage()
    longimg.blit(hslimg, target = (0, (3 * H)))




def makedir(path):
    try :
        os.makedirs(path)
    except :
        pass




def saveExist(slot):
    if  not (os.path.exists(DATA_PATH)) : 
        return 0
    else : 
        ls = os.listdir(DATA_PATH)
        inls = [0, 0, 0]
        for l in ls:
            if l == 'sav1.dat' : 
                inls[0] = 1
            elif l == 'sav2.dat' : 
                inls[1] = 1
            elif l == 'sav3.dat' : 
                inls[2] = 1
        return inls[slot]




def saveGame(slot):
    dat_buffer = ''
    for i in range(4):
        for j in range(4):
            if dat[i][j] : 
                dat_buffer = dat_buffer + str(dat[i][j].value) + ','
            else : 
                dat_buffer = dat_buffer + '0,'
    dat_buffer = dat_buffer + str(sumscore) + ',' + str(undo_chances) + ',' + str(undo_option_flag) + ',' + str(four)
    if  not (os.path.exists(DATA_PATH)) : 
        makedir(DATA_PATH)
    if slot == 0 : 
        f = open(DATA_PATH + '\\sav1.dat', 'w')
    elif slot == 1 : 
        f = open(DATA_PATH + '\\sav2.dat', 'w')
    elif slot == 2 : 
        f = open(DATA_PATH + '\\sav3.dat', 'w')
    f.write(dat_buffer)
    f.close()
    info.show(cn('保存成功。'), (W, H), 2000, 0, ap.EHRightVTop)




def loadGame(slot):
    won = 0
    dat_bak = []
    sumscore_bak = []
    if os.path.exists(DATA_PATH) : 
        if slot == 0 : 
            f = open(DATA_PATH + '\\sav1.dat', 'r')
        elif slot == 1 : 
            f = open(DATA_PATH + '\\sav2.dat', 'r')
        elif slot == 2 : 
            f = open(DATA_PATH + '\\sav3.dat', 'r')
        fs = f.readline()
        f.close()
        fs_split = fs.split(',')
        if len(fs_split) == 20 : 
            read_values = [([0] * 4) for i in range(4)]
            for i in range(4):
                for j in range(4):
                    read_values[i][j] = int(fs_split[(i * 4) + j])
            sumscore = int(fs_split[16])
            undo_chances = int(fs_split[17])
            undo_option_flag = int(fs_split[18])
            max_undo_chances = UndoOptionList[undo_option_flag]
            four = int(fs_split[19])
            numlist = [2 for i in xrange((9 - four))] + [4 for i in xrange(four)]
            if  not (canmove()) : 
                end = 1
            return 1
        else : 
            ap.note(cn('存档可能有错误！'), 'error')
        pass
    else : 
        info.show(cn('找不到存档。'), (W, H), 2000, 0, ap.EHRightVTop)
        makedir(DATA_PATH)
    global won, dat_bak, sumscore_bak, read_values, sumscore, undo_chances, undo_option_flag, max_undo_chances, four, numlist, end




def readHighscoresFromDisk():
    if os.path.exists(DATA_PATH + '\\hsl.dat') : 
        f = open(DATA_PATH + '\\hsl.dat', 'r')
        for i in xrange(10):
            fs = f.readline().replace('\n', '')
            if fs == '' : 
                hs.append([0, '0000000000'])
            else : 
                hs.append([int(fs[ : -10]), fs[-10 : ]])
        f.close()
    else : 
        hs = [[0, '0000000000'] for i in range(10)]
        saveHighscoresToDisk()
    global hs




def saveHighscoresToDisk():
    try :
        if  not (os.path.exists(DATA_PATH)) : 
            os.makedirs(DATA_PATH)
        f = open(DATA_PATH + '\\hsl.dat', 'w')
    except :
        f = open('d:\\error.log', 'w')
        f.write('Cannot open hsl.dat')
        f.close()
    else :
        for i in xrange(-1, -11, -1):
            f.write(str(hs[i][0]) + hs[i][1] + '\n')
        f.close()




def deleteSav(slot):
    if ap.query(cn('删除存档？'), 'query') : 
        try :
            if slot == 0 : 
                os.remove(DATA_PATH + '\\sav1.dat')
            elif slot == 1 : 
                os.remove(DATA_PATH + '\\sav2.dat')
            elif slot == 2 : 
                os.remove(DATA_PATH + '\\sav3.dat')
        except :
            pass
        mnbg.blit(mnbg_back)
        updateMenuImage()
        longimgRead()
        paint_all()




def rematch():
    updateHighscoreList()
    saveHighscoresToDisk()
    hs = []
    readHighscoresFromDisk()
    is_move = 0
    won = 0
    end = 0
    sumscore = 0
    dat = [([0] * 4) for i in range(4)]
    hs.sort()
    hs.insert(0, [sumscore, today()])
    sumscore_flag = 0
    dat_bak = []
    sumscore_bak = []
    Xcode = '0000'
    max_undo_chances = UndoOptionList[undo_option_flag]
    undo_chances = max_undo_chances
    for t in ts:
        t.visible = 0
    longimgInit()
    drawBg2()
    drawNum(sumscore)
    t01.appear()
    t02.appear()
    t01.draw()
    t02.draw()
    backupLoading()
    paint_all()
    backupRecentData()
    e32.ao_sleep(0.05)
    global hs, is_move, won, end, sumscore, dat, sumscore_flag, dat_bak, sumscore_bak, Xcode, max_undo_chances, undo_chances




def startGame():
    changeBackground()
    changeTileType()
    selectMenuBg(bg)
    longimgInit()
    readHighscoresFromDisk()
    hs.sort()
    hs.insert(0, [sumscore, today()])
    drawBg2()
    drawNum(sumscore)
    t01.appear()
    t02.appear()
    t01.draw()
    t02.draw()
    paint_all()
    backupRecentData()
    UI_flag = 0
    global UI_flag




def execute(event):
    if  not (UI_flag) : 
        if event['keycode'] == kc.EKeyLeftArrow or event['keycode'] == kc.EKey4 : 
            slide(-1, 0)
        elif event['keycode'] == kc.EKeyUpArrow or event['keycode'] == kc.EKey2 : 
            slide(0, -1)
        elif event['keycode'] == kc.EKeyRightArrow or event['keycode'] == kc.EKey6 : 
            slide(1, 0)
        elif event['keycode'] == kc.EKeyDownArrow or event['keycode'] == kc.EKey8 : 
            slide(0, 1)
        elif event['keycode'] == kc.EKey7 : 
            undo()
            end = 0
        elif event['scancode'] == kc.EScancodeLeftSoftkey : 
            scroll(-1)
            UI_flag = 2
        elif event['keycode'] == kc.EKey0 : 
            UI_flag = 8
            showLoading()
            changeTileType()
            backupLoading()
            closeLoading()
            UI_flag = 0
        elif event['keycode'] == kc.EKey1 : 
            updateHighscoreList()
            scroll(1)
            UI_flag = 1
        elif event['keycode'] == kc.EKey5 : 
            showLoading()
            changeBackground()
            selectMenuBg(bg)
            updateMenuImage()
            backupLoading()
            closeLoading()
        elif event['keycode'] == kc.EKeyStar : 
            if ap.query(cn('是否重新开始？'), 'query') : 
                showLoading()
                rematch()
                closeLoading()
            pass
        if  not ( not (canmove()) and end) : 
            end = 1
            info.show(cn('=====游戏结束====='), ((LX + 8), TY), 1800, 0, ap.EHLeftVTop)
        if won : 
            UI_flag = 7
            showWin()
        pass
    elif UI_flag == 1 : 
        if event['keycode'] == kc.EKeyBackspace : 
            if ap.query(cn('清除全部得分记录？'), 'query') : 
                clearHighscoreList()
                longimgRead()
                paint_all()
            pass
        pass
    elif UI_flag == 2 : 
        doMenuEvent(event)
    elif UI_flag == 3 : 
        pass
    elif UI_flag == 4 : 
        pass
    elif UI_flag == 5 : 
        pass
    elif UI_flag == 6 : 
        pass
    elif UI_flag == 7 : 
        if event['type'] == 1 : 
            longimgRead()
            paint_all()
            UI_flag = 0
            won = 0
        pass
    global end, UI_flag, won




def slide(dx, dy):
    if dx == -1 : 
        for i in xrange(3):
            for x in xrange(1, (4 - i)):
                for y in xrange(4):
                    move((dx, dy), (x, y))
        pass
    elif dx == 1 : 
        for i in xrange(3):
            for x in xrange(2, (i - 1), -1):
                for y in xrange(4):
                    move((dx, dy), (x, y))
        pass
    elif dy == -1 : 
        for i in xrange(3):
            for y in xrange(1, (4 - i)):
                for x in xrange(4):
                    move((dx, dy), (x, y))
        pass
    elif dy == 1 : 
        for i in xrange(3):
            for y in xrange(2, (i - 1), -1):
                for x in xrange(4):
                    move((dx, dy), (x, y))
        pass
    for i in SlideRange:
        drawBg2()
        for t in ts:
            if t.steps : 
                if dx == -1 : 
                    t.x -= (t.steps * i)
                elif dx == 1 : 
                    t.x += (t.steps * i)
                elif dy == -1 : 
                    t.y -= (t.steps * i)
                elif dy == 1 : 
                    t.y += (t.steps * i)
                pass
            if t.visible : 
                t.draw()
        drawNum(sumscore)
        paint_all()
        e32.ao_sleep(0.01)
    drawBg2()
    for t in ts:
        if t.value_update : 
            sumscore += t.value
            t.value += t.value
            t.value_update = 0
            if t.value > 2000 : 
                won = 1
            pass
        if t.visible_update : 
            t.visible = 0
            t.visible_update = 0
        if t.visible : 
            t.x, t.y = loc[t.blx][t.bly]
            t.draw()
        if t.merged : 
            t.merged = 0
        t.steps = 0
    drawNum(sumscore)
    paint_all()
    if is_move : 
        for t in ts:
            if  not (t.visible) : 
                t.appear()
                t.draw()
                break
        paint_all()
        is_move = 0
        backupRecentData()
    global won, is_move




def move(a, b):
    dx, dy = a
    x, y = b
    if dat[x][y] : 
        orit = dat[x][y]
        if dx == -1 : 
            if dat[(x - 1)][y] : 
                if dat[(x - 1)][y].value == orit.value : 
                    if  not ( not (dat[(x - 1)][y].merged) and orit.merged) : 
                        (dat[(x - 1)][y]).visible_update = 1
                        dat[(x - 1)][y] = orit
                        dat[x][y] = 0
                        orit.value_update = 1
                        orit.blx -= 1
                        orit.steps += 1
                        orit.merged = 1
                        is_move = 11
                    pass
                pass
            else : 
                orit.blx -= 1
                orit.steps += 1
                dat[(x - 1)][y] = orit
                dat[x][y] = 0
                is_move = 1
            pass
        elif dx == 1 : 
            if dat[(x + 1)][y] : 
                if (dat[(x + 1)][y]).value == orit.value : 
                    if  not ( not ((dat[(x + 1)][y]).merged) and orit.merged) : 
                        (dat[(x + 1)][y]).visible_update = 1
                        dat[(x + 1)][y] = orit
                        dat[x][y] = 0
                        orit.value_update = 1
                        orit.blx += 1
                        orit.steps += 1
                        orit.merged = 1
                        is_move = 11
                    pass
                pass
            else : 
                orit.blx += 1
                orit.steps += 1
                dat[(x + 1)][y] = orit
                dat[x][y] = 0
                is_move = 1
            pass
        elif dy == -1 : 
            if dat[x][(y - 1)] : 
                if dat[x][(y - 1)].value == orit.value : 
                    if  not ( not (dat[x][(y - 1)].merged) and orit.merged) : 
                        (dat[x][(y - 1)]).visible_update = 1
                        dat[x][(y - 1)] = orit
                        dat[x][y] = 0
                        orit.value_update = 1
                        orit.bly -= 1
                        orit.steps += 1
                        orit.merged = 1
                        is_move = 11
                    pass
                pass
            else : 
                orit.bly -= 1
                orit.steps += 1
                dat[x][(y - 1)] = orit
                dat[x][y] = 0
                is_move = 1
            pass
        elif dy == 1 : 
            if dat[x][(y + 1)] : 
                if (dat[x][(y + 1)]).value == orit.value : 
                    if  not ( not ((dat[x][(y + 1)]).merged) and orit.merged) : 
                        (dat[x][(y + 1)]).visible_update = 1
                        dat[x][(y + 1)] = orit
                        dat[x][y] = 0
                        orit.value_update = 1
                        orit.bly += 1
                        orit.steps += 1
                        orit.merged = 1
                        is_move = 11
                    pass
                pass
            else : 
                orit.bly += 1
                orit.steps += 1
                dat[x][(y + 1)] = orit
                dat[x][y] = 0
                is_move = 1
            pass
        pass
    global is_move




def backupRecentData():
    dat_temp = [([0] * 4) for i in range(4)]
    for i in xrange(4):
        for j in xrange(4):
            if dat[i][j] : 
                dat_temp[i][j] = dat[i][j].value
    dat_bak.append(dat_temp)
    sumscore_bak.append(sumscore)
    if len(dat_bak) > MAX_UNDO_STEPS : 
        dat_bak.pop(0)
        sumscore_bak.pop(0)




def canmove():
    can = 0
    for d in dat:
        if  not (d) : 
            can = 1
            break
    if can : 
        return 1
    else : 
        for i in range(4):
            for j in range(3):
                if dat[i][j] : 
                    if dat[i][(j + 1)] : 
                        if dat[i][j].value == (dat[i][(j + 1)]).value : 
                            can = 1
                            break
                        pass
                    else : 
                        can = 1
                        break
                    pass
                else : 
                    can = 1
                    break
        pass
    if can : 
        return 1
    else : 
        for i in range(3):
            for j in range(4):
                if dat[i][j] : 
                    if dat[(i + 1)][j] : 
                        if dat[i][j].value == (dat[(i + 1)][j]).value : 
                            can = 1
                            break
                        pass
                    else : 
                        can = 1
                        break
                    pass
                else : 
                    can = 1
                    break
        pass
    if can : 
        return 1
    else : 
        return 0




def undo():
    if len(dat_bak) > 1 and undo_chances : 
        dat_bak.pop(-1)
        sumscore_bak.pop(-1)
        values = dat_bak[-1]
        sumscore = sumscore_bak[-1]
        drawBg2()
        ind = 0
        tmp = []
        for i in range(4):
            for j in range(4):
                if values[i][j] : 
                    dat[i][j] = ts[ind]
                    ts[ind].visible = 1
                    ts[ind].value = values[i][j]
                    ts[ind].blx = i
                    ts[ind].bly = j
                    ts[ind].x, ts[ind].y = loc[i][j]
                    ts[ind].draw()
                else : 
                    dat[i][j] = 0
                    ts[ind].visible = 0
                ind += 1
        undo_chances -= 1
        drawNum(sumscore)
        paint_all()
    global sumscore




def backupLoading():
    ld_back.blit(readyimg, source = ((0, ld_y), (ld_back.size[0], ld_back.size[1] + ld_y)))




def showLoading():
    for i in (-45, -30, -15, 0):
        readyimg.blit(ld, target = (i, ld_y), mask = ld_mask)
        paint_all()
        e32.ao_sleep(0.01)




def closeLoading():
    for i in (0, -15, -30, -45, -65):
        e32.ao_sleep(0.01)
        readyimg.blit(ld_back, target = (0, ld_y))
        readyimg.blit(ld, target = (i, ld_y), mask = ld_mask)
        paint_all()




def changeTileType():
    drawBg2()
    drawNum(sumscore)
    if os.path.exists(MAP_PATH) : 
        maps = os.listdir(MAP_PATH)
        for m in maps:
            if  not (m.split('.')[-1].lower() in ('png', 'jpg', 'jpeg')) : 
                maps.remove(m)
        if len(maps) == 0 : 
            ap.note(cn('找不到图片！'), 'error')
        else : 
            MapPointer = (MapPointer < (len(maps) - 1) and MapPointer + 1) or 0
            selectedmap = gr.Image.open(cn(MAP_PATH + '\\' + maps[MapPointer]))
            for j in xrange(4):
                for i in xrange(4):
                    (tiles[(2 ** ((j * 4) + i + 1))]).blit(selectedmap, source = (((TILE * i), (TILE * j)), ((TILE * i) + TILE, (TILE * j) + TILE)))
                    (tile_masks[(2 ** ((j * 4) + i + 1))]).blit(selectedmap, source = (((TILE * (i + 4)), (TILE * j)), ((TILE * (i + 4)) + TILE, (TILE * j) + TILE)))
            pass
        pass
    else : 
        ap.note(cn('找不到图片！'), 'error')
        makedir(MAP_PATH)
    for t in ts:
        if t.visible : 
            t.draw()
    backupLoading()
    paint_all()
    global MapPointer




def changeBackground():
    if os.path.exists(BG_PATH) : 
        bgs = os.listdir(BG_PATH)
        for b in bgs:
            if  not ( not ( not (b.endswith('.png')) and b.endswith('.jpg')) and b.endswith('.jpeg')) : 
                bgs.remove(b)
        if len(bgs) == 0 : 
            makedir(BG_PATH)
            setBg()
            setBg2()
            drawBg2()
            drawNum(sumscore)
            for t in ts:
                if t.visible : 
                    t.draw()
            paint_all()
        else : 
            BgPointer = (BgPointer < (len(bgs) - 1) and BgPointer + 1) or 0
            selectBg(cn(BG_PATH + '\\' + bgs[BgPointer]))
            drawBg2()
            drawNum(sumscore)
            for t in ts:
                if t.visible : 
                    t.draw()
            paint_all()
            ld_back.blit(bg2, source = ((0, ld_y), (ld_back.size[0], ld_back.size[1] + ld_y)))
        pass
    else : 
        makedir(BG_PATH)
        setBg()
        setBg2()
        drawBg2()
        drawNum(sumscore)
        for t in ts:
            if t.visible : 
                t.draw()
        paint_all()
    global BgPointer




def scroll(drt):
    longimgBackup()
    screen_loc = screen_loc + (H * drt)
    longimgRead()
    paint_all()
    global screen_loc




def doMenuEvent(event):
    if event['keycode'] == kc.EKeyLeftArrow : 
        selectOption(-1)
    elif event['keycode'] == kc.EKeyUpArrow : 
        SelectedItem -= 1
        if SelectedItem < 0 : 
            SelectedItem = 4
        selectOption(0)
    elif event['keycode'] == kc.EKeyRightArrow : 
        selectOption(1)
    elif event['keycode'] == kc.EKeyDownArrow : 
        SelectedItem = ((SelectedItem + 1) <= 4 and SelectedItem + 1) or 0
        selectOption(0)
    elif event['keycode'] == kc.EKeySelect : 
        if SelectedItem == 0 : 
            if saveExist(snlg_flag) : 
                if ap.query(cn('是否覆盖？'), 'query') : 
                    readyimg.blit(redlamb, target = led_loc[0][snlg_flag], mask = led_mask)
                    readyimg.blit(mouse, target = mouse_loc[0][snlg_flag], mask = mouse_mask)
                    paint_all()
                    saveGame(snlg_flag)
                    updateMenuImage()
                pass
            else : 
                readyimg.blit(redlamb, target = led_loc[0][snlg_flag], mask = led_mask)
                readyimg.blit(mouse, target = mouse_loc[0][snlg_flag], mask = mouse_mask)
                paint_all()
                saveGame(snlg_flag)
                updateMenuImage()
            pass
        elif SelectedItem == 1 : 
            if saveExist(snlg_flag) : 
                if ap.query(cn('载入游戏？'), 'query') : 
                    if loadGame(snlg_flag) : 
                        readyimg.blit(mnbg)
                        readyimg.blit(redlamb, target = led_loc[1][snlg_flag], mask = led_mask)
                        readyimg.blit(mouse, target = mouse_loc[1][snlg_flag], mask = mouse_mask)
                        drawBars()
                        drawBarNotes()
                        paint_all()
                        updateMenuImage()
                        e32.ao_sleep(0.4)
                        scroll(1)
                        UI_flag = 0
                        drawBg2()
                        for i in range(4):
                            for j in range(4):
                                ind = (4 * i) + j
                                if read_values[i][j] : 
                                    dat[i][j] = ts[ind]
                                    ts[ind].visible = 1
                                    ts[ind].value = read_values[i][j]
                                    ts[ind].blx = i
                                    ts[ind].bly = j
                                    ts[ind].x, ts[ind].y = loc[i][j]
                                    ts[ind].draw()
                                else : 
                                    dat[i][j] = 0
                                    ts[ind].visible = 0
                        drawNum(sumscore)
                        paint_all()
                        backupRecentData()
                        info.show(cn('载入成功。'), (W, H), 1200, 0, ap.EHRightVTop)
                    pass
                pass
            else : 
                info.show(cn('存档不存在。'), (W, H), 2000, 0, ap.EHRightVTop)
            pass
        elif SelectedItem == 4 : 
            scroll(-1)
            UI_flag = 3
        pass
    elif event['keycode'] == kc.EKeyBackspace : 
        deleteSav(snlg_flag)
    elif event['keycode'] == kc.EKey2 : 
        xcodeCheck(2)
    elif event['keycode'] == kc.EKey0 : 
        xcodeCheck(0)
    elif event['keycode'] == kc.EKey4 : 
        xcodeCheck(4)
    elif event['keycode'] == kc.EKey8 : 
        xcodeCheck(8)
    global SelectedItem, UI_flag




def selectOption(direction):
    readyimg.blit(mnbg)
    if SelectedItem == 0 : 
        if direction == -1 : 
            snlg_flag = ((snlg_flag - 1) >= 0 and snlg_flag - 1) or 0
        elif direction == 1 : 
            snlg_flag = ((snlg_flag + 1) <= 2 and snlg_flag + 1) or 2
        readyimg.blit(mouse, target = mouse_loc[0][snlg_flag], mask = mouse_mask)
    if SelectedItem == 1 : 
        if direction == -1 : 
            snlg_flag = ((snlg_flag - 1) >= 0 and snlg_flag - 1) or 0
        elif direction == 1 : 
            snlg_flag = ((snlg_flag + 1) <= 2 and snlg_flag + 1) or 2
        readyimg.blit(mouse, target = mouse_loc[1][snlg_flag], mask = mouse_mask)
    if SelectedItem == 2 : 
        if direction == -1 : 
            undo_option_flag = ((undo_option_flag - 1) >= 0 and undo_option_flag - 1) or 0
        elif direction == 1 : 
            undo_option_flag = (((undo_option_flag + 1) < len(UndoOptionList) and undo_option_flag + 1) or len(UndoOptionList) - 1)
        readyimg.blit(selection, target = selection_loc[SelectedItem], mask = selection_mask)
    elif SelectedItem == 3 : 
        if direction == -1 : 
            four = ((four - 1) >= 0 and four - 1) or 0
        elif direction == 1 : 
            four = ((four + 1) < 10 and four + 1) or 9
        numlist = [2 for i in xrange((9 - four))] + [4 for i in xrange(four)]
        readyimg.blit(selection, target = selection_loc[SelectedItem], mask = selection_mask)
    elif SelectedItem == 4 : 
        readyimg.blit(selection, target = selection_loc[SelectedItem], mask = selection_mask)
    drawBars()
    drawBarNotes()
    paint_all()
    global snlg_flag, undo_option_flag, four, numlist




def updateHighscoreList():
    hs[sumscore_flag] = [sumscore, today()]
    while sumscore_flag < (len(hs) - 1) and hs[(sumscore_flag + 1)][0] < sumscore : 
        hs[sumscore_flag], hs[(sumscore_flag + 1)] = (hs[(sumscore_flag + 1)], hs[sumscore_flag])
        sumscore_flag += 1
    while hs[(sumscore_flag - 1)][0] > sumscore and sumscore_flag > 0 : 
        hs[sumscore_flag], hs[(sumscore_flag - 1)] = (hs[(sumscore_flag - 1)], hs[sumscore_flag])
        sumscore_flag -= 1
    hslimg.blit(hsl_back)
    for i in range(len(hs)):
        if hs[i][0] != 0 : 
            if i == sumscore_flag : 
                hslimg.blit(sym_score, target = ((hs_x - 3), hs_y + ((10 - i) * 14)), mask = sym_score_mask)
                drawDate(today(), date_x, date_y + ((10 - i) * 14))
            else : 
                drawDate(hs[i][1], date_x, date_y + ((10 - i) * 14))
            pass
        if i < 5 : 
            hslimg.blit(DgtList[(i + 1)], target = ((hs_x + 8), hs_y + (i * 14)), mask = Dgt_maskList[(i + 1)])
        n, m = numImg(hs[i][0])
        hslimg.blit(n, target = ((hs_x + 24), hs_y + ((10 - i) * 14)), mask = m)
    longimg.blit(hslimg, target = (0, (3 * H)))




def clearHighscoreList():
    sumscore_flag = 0
    hs = [[0, '0000000000'] for i in range(10)]
    hs.insert(0, [sumscore, today()])
    saveHighscoresToDisk()
    updateHighscoreList()
    global sumscore_flag, hs




def showWin():
    longimgBackup()
    readyimg.blit(wimg1, mask = wimg_mask1)
    for t in ts:
        if t.visible and t.value > 2000 : 
            t.draw()
    paint_all()




def showDevelopOption():
    UI_flag = 8
    devslt = ap.selection_list(DevelopOptionList)
    if devslt == 0 : 
        arg0 = ap.query(cn('第一步长：'), 'number', 25)
        if arg0 != None : 
            arg1 = ap.query(cn('第二步长：'), 'number', 15)
            if arg1 != None : 
                arg2 = ap.query(cn('第三步长：'), 'number', 5)
                if arg2 != None : 
                    SlideRange = [arg0, arg1, arg2]
                    info.show(cn('设置成功'), (W, H), 1000, 0, ap.EHRightVTop)
                pass
            pass
        pass
    elif devslt == 1 : 
        arg0 = ap.query(cn('步长:(至少一个数字，多者以英文逗号隔开)'), 'text', cn('25,15,5'))
        if arg0 != None : 
            ss = arg0.split(',')
            SlideRange = []
            try :
                for s in ss:
                    SlideRange.append(int(s))
                info.show(cn('设置成功'), (W, H), 1000, 0, ap.EHRightVTop)
            except :
                ap.note(cn('格式错误!'), 'error')
                SlideRange = [25, 15, 5]
            pass
        pass
    elif devslt == 2 : 
        arg = ap.query(cn('输入代码:'), 'text')
        if arg != None : 
            try :
                exec arg
                info.show(cn('成功执行!'), (W, H), 1000, 0, ap.EHRightVTop)
            except :
                ap.note(cn('代码错误!'), 'error')
            pass
        pass
    UI_flag = 2
    global UI_flag, SlideRange




def xcodeCheck(xinput):
    Xcode += str(xinput)
    if Xcode.endswith('2048') : 
        showDevelopOption()
        Xcode = '0000'
    else : 
        Xcode = Xcode[-4 : ]
    global Xcode




class Tile :


    __module__ = __name__
    def __init__(self, idx):
        self.value = 2
        self.index = idx
        self.steps = 0
        self.merged = 0
        self.blx = 0
        self.bly = 0
        self.x = 0
        self.y = 0
        self.visible = 0
        self.visible_update = 0
        self.value_update = 0
        self.image = 0




    def draw(self, img = readyimg):
        if self.value < 70000 : 
            img.blit(tiles[self.value], mask = tile_masks[self.value], target = (self.x, self.y))
        else : 
            img.rectangle((self.x, self.y, self.x + TILE, self.y + TILE), 16777215, fill = 0)
            img.text(((self.x + 4), (self.y + 46)), cn(str(self.value)), 16777215, font = (u'', 14))




    def appear(self):
        self.blx = random.randrange(4)
        self.bly = random.randrange(4)
        while dat[self.blx][self.bly] : 
            self.blx = random.randrange(4)
            self.bly = random.randrange(4)
        dat[self.blx][self.bly] = self
        dat[self.blx][self.bly].value = random.choice(numlist)
        self.x, self.y = loc[self.blx][self.bly]
        self.visible = 1






def backNexit():
    if  not (UI_flag) : 
        if ap.query(cn('是否退出游戏？'), 'query') : 
            updateHighscoreList()
            saveHighscoresToDisk()
            ap.app.set_exit()
        pass
    elif UI_flag == 1 : 
        scroll(-1)
        UI_flag = 0
    elif UI_flag == 2 : 
        scroll(1)
        UI_flag = 0
    elif UI_flag == 3 : 
        scroll(1)
        UI_flag = 2
    elif UI_flag == 7 : 
        longimgRead()
        paint_all()
        UI_flag = 0
        won = 0
    global UI_flag, won


canvas = ap.Canvas(redraw_callback = redraw, event_callback = execute)
showLoading()
info = ap.InfoPopup()
t01 = Tile(1)
t02 = Tile(2)
t03 = Tile(3)
t04 = Tile(4)
t05 = Tile(5)
t06 = Tile(6)
t07 = Tile(7)
t08 = Tile(8)
t09 = Tile(9)
t10 = Tile(10)
t11 = Tile(11)
t12 = Tile(12)
t13 = Tile(13)
t14 = Tile(14)
t15 = Tile(15)
t16 = Tile(16)
ts = (t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16)
envy.set_app_system(1)
ap.app.body = canvas
ap.app.screen = 'full'
ap.app.exit_key_handler = backNexit
startGame()
closeLoading()
while 1:
    ap.app.Yield()
