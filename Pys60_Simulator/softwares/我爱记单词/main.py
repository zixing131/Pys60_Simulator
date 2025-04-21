# -*- coding: utf-8 -*-

from images import *
import e32, time, random, key_codes as kc

def paint_all():
    canvas.blit(readyimg)


def redraw(rect):
    paint_all()


def execute(event):
    global UI_flag
    if UI_flag == 0:
        if event['keycode'] == kc.EKeyLeftArrow:
            pass
        elif event['keycode'] == kc.EKeyUpArrow:
            moveSelection(-1)
        elif event['keycode'] == kc.EKeyRightArrow:
            pass
        elif event['keycode'] == kc.EKeyDownArrow:
            moveSelection(1)
        elif event['keycode'] == kc.EKeySelect:
            selectDic()
            UI_flag = 1
    elif UI_flag == 1:
        mainProc(event)


def mainProc(event):
    global TapState
    global clock_0
    global clock_1
    global hf_word
    if event['keycode'] == kc.EKeyLeftArrow:
        moveSpace(-1)
    elif event['keycode'] == kc.EKeyUpArrow:
        movePage(-1)
    elif event['keycode'] == kc.EKeyRightArrow:
        moveSpace(1)
    elif event['keycode'] == kc.EKeyDownArrow:
        movePage(1)
    elif event['keycode'] == kc.EKeySelect or event['keycode'] == kc.EKeyEnter:
        if isRight == 0:
            if not busy:
                checkWord()
        else:
            nextWord()
        return
    elif event['keycode'] == kc.EKeySpace:
        nextWord()
    elif event['keycode'] == kc.EKeyBackspace:
        if hf_word[Blanks[XPlace]] == '_':
            moveSpace(-1)
        else:
            hf_word = rp(hf_word, Blanks[XPlace], '_')
    elif event['keycode'] in KeyMap:
        if KEY_TYPE == 0:
            fillWord(KeyMap[event['keycode']])
            moveSpace(1)
        elif KEY_TYPE == 1:
            if TapState == 0:
                TapState = 1
                clock_0 = time.clock()
                fillWord(KeyMap[event['keycode']][0])
            else:
                clock_1 = time.clock()
                if clock_1 - clock_0 < TapDelay:
                    clock_0 = clock_1
                    fillWord(KeyMap[event['keycode']][TapState])
                    TapState = TapState < len(KeyMap[event['keycode']]) - 1 and TapState + 1 or 0
                else:
                    TapState = 1
                    clock_0 = time.clock()
                    fillWord(KeyMap[event['keycode']][0])
    draw_all()
    paint_all()


def showDicList(focus_line=0):
    readyimg.blit(getBg(title_string='我爱记单词'))
    line = 0
    for item in DicList:
        if DicList_pos[1] + line * (MAINFONT_SIZE + LINE_DIST) < H - TITLE_HEIGHT:
            if line == focus_line:
                readyimg.blit(cursorimg, target=(Selection_pos[0], Selection_pos[1] + line * (MAINFONT_SIZE + LINE_DIST)), mask=cursor_mask)
            readyimg.text((DicList_pos[0], DicList_pos[1] + line * (MAINFONT_SIZE + LINE_DIST)), cn(item), SHADOW, font=MAINFONT)
            line += 1

    paint_all()


def moveSelection(drct):
    global Selection
    Selection += drct
    if Selection >= DicAmount:
        Selection = 0
    elif Selection < 0:
        Selection = DicAmount - 1
    showDicList(focus_line=Selection)


def selectDic():
    global RecentList
    global Title
    Title = DicList[Selection]
    try:
        RecentList = file2List(RES_PATH + '\\' + DicList[Selection] + '.txt')
    except:
        RecentList = file2List(RES_PATH + '\\' + DicList[Selection].decode('u8').encode('gbk') + '.txt')
    preLoadWord()
    showPlayingPanel()
    ap.app.menu = Menu1


def showPlayingPanel():
    global Blanks
    global Blks
    global Fragmentary
    global XLine
    global XLines
    global XPlace
    global haveWrong
    global hf_word
    global isRight
    global phonetic_symbol
    global straight_matter_all
    global straight_matter_part
    global word
    global word_class
    XLine = 0
    isRight = 0
    haveWrong = 0
    word = n_word
    phonetic_symbol = n_phonetic_symbol
    word_class = n_word_class
    straight_matter_all = n_smatter
    straight_matter_part = n_smatter[:n_smatter.find(': ')] + cn('\n(...)')
    if n_smatter.find(': ') == -1:
        Fragmentary = 1
        straight_matter_all = straight_matter_all + cn('\n (该释义可能不够全面)\n答案:') + word + cn('.')
    (hf_word, Blanks, Blks) = getHalfWord(word, lvl=Level)
    XPlace = 0
    XLines = initSMatterImg(straight_matter_part)
    chooseButtom(buttomimg1)
    draw_all()
    paint_all()
    preLoadWord()


def draw_all():
    readyimg.blit(getBg(background=playing_bg, title_string=Title, extra_string=Extra_string))
    drawMwbg()
    drawUnderline(hf_word, Blanks)
    drawWord(hf_word)
    drawWordClass(word_class)
    drawSpacePointer(Blanks[XPlace], hf_word)
    drawPhoneticSymbol(phonetic_symbol)
    drawSMatter(line=XLine)


def preLoadWord(backward=0):
    global n_phonetic_symbol
    global n_smatter
    global n_word
    global n_word_class
    if backward == 0:
        history.append(int(getRandomLine(RecentList)[:-1]))
    elif len(history) <= 2:
        ap.note(cn('已经是第一个单词！'))
    else:
        history.pop(-1)
        history.pop(-1)
    rline = WordLines[history[-1]].decode(USERCODE)
    n_word = rline[:rline.find('\t')].lower()
    tmp1 = rline.find('/')
    tmp2 = rline.find('/', tmp1 + 1)
    n_phonetic_symbol = rline[tmp1:tmp2 + 1]
    tmp1 = rline.find(' ', tmp2) + 1
    if rline[tmp1] == '(':
        tmp2 = rline.find(')', tmp1)
        if tmp2 != -1:
            tmp1 = rline.find(' ', tmp2) + 1
    tmp2 = rline.find(' ', tmp1)
    if rline[tmp2 - 1] == ',':
        tmp2 = rline.find(' ', tmp2 + 1)
    n_word_class = rline[tmp1:tmp2] + cn('. ')
    n_smatter = rline[tmp2 + 1:]
    n_smatter = n_smatter.replace('*', '\n')
    n_smatter = n_smatter.replace('\\n', '\n')
    tmp1 = n_smatter.find('  ')
    while tmp1 != -1:
        if n_smatter[tmp1 + 2].isdigit():
            if n_smatter[tmp1 + 3] == ' ' or n_smatter[tmp1 + 3].isdigit() and n_smatter[tmp1 + 4] == ' ':
                n_smatter = n_smatter[:tmp1 + 2] + '\n' + n_smatter[tmp1 + 2:]
        tmp1 = n_smatter.find('  ', tmp1 + 2)


def moveSpace(drct):
    global TapState
    global XPlace
    XPlace += drct
    if XPlace < 0:
        XPlace = Blks - 1
    elif XPlace > Blks - 1:
        XPlace = 0
    if KEY_TYPE == 1:
        TapState = 0


def movePage(drct):
    global XLine
    XLine += drct
    if XLine > XLines - 4:
        XLine -= 1
    elif XLine < 0:
        XLine = 0


def fillWord(letter):
    global hf_word
    hf_word = rp(hf_word, Blanks[XPlace], letter)


def checkWord():
    global FinishTimes
    global OneShots
    global XLines
    global haveWrong
    global isRight
    if word == hf_word:
        isRight = 1
        FinishTimes += 1
        if haveWrong == 0:
            OneShots += 1
        screen_bak.blit(readyimg)
        drawTick(screen_bak)
        screen_bak.text((W / 2, H - TITLE_HEIGHT), cn('正在加载。。'), 4286945, font=('normal', 18, 1))
        screen_mask.clear(0)
        for i in xrange(1, 11, 1):
            screen_mask.rectangle((W / 2, 0, W / 2 + W / 20 * i, H), fill=16777215)
            readyimg.blit(screen_bak, mask=screen_mask)
            paint_all()
            e32.ao_sleep(0.01)

        XLines = initSMatterImg(straight_matter_all)
        chooseButtom(buttomimg2)
        draw_all()
        paint_all()
    else:
        haveWrong = 1
        screen_bak.blit(readyimg)
        for i in range(4):
            drawCross(img=screen_bak, part=i)
            readyimg.blit(screen_bak)
            paint_all()
            e32.ao_sleep(0.03)

        e32.ao_sleep(0.03)
        draw_all()
        paint_all()


def nextWord():
    showPlayingPanel()


def lastWord():
    preLoadWord(backward=1)
    showPlayingPanel()


def seeAllMeaning():
    global Blanks
    global Blks
    global XLines
    global XPlace
    global haveWrong
    global hf_word
    XLines = initSMatterImg(straight_matter_all)
    hf_word = u''
    for letter in word:
        hf_word = hf_word + '_'

    Blanks = range(len(word))
    Blks = len(Blanks)
    XPlace = 0
    draw_all()
    paint_all()
    haveWrong = 1


def changeLevel():
    global Extra_string
    global Level
    Level = ap.popup_menu(LevelOptionList)
    Extra_string = Extra_string_list[Level]
    nextWord()


def loadDicLib():
    try:
        Dic = open(RES_PATH + '\\Dic.dat', 'r')
    except:
        ap.note(cn('无法打开Dic.dat文件！'), 'error')
    else:
        ls = Dic.readlines()
        Dic.close()
        return ls


def getDicList(p):
    ls = []
    for item in os.listdir(p):
        item = item.decode('gbk').encode('u8')
        if not os.path.isdir(p + '\\' + item):
            if item.lower().endswith('.txt'):
                ls.append(item[:-4])

    return (ls, len(ls))


def file2List(p):
    f = open(p, 'r')
    ls = f.readlines()
    f.close()
    return ls


def getRandomLine(ls):
    return ls[random.randrange(len(ls))]


def getMultiRand(seq, num):
    l = []
    while len(l) < num:
        x = random.choice(seq)
        if not x in l:
            l.append(x)

    return l


def getHalfWord(wrd, lvl=1):
    lw = len(wrd)
    blks = 1
    hfwrd = wrd[:]
    if lvl == 0:
        if lw < 6:
            blks = 1
        elif lw < 9:
            blks = 2
        elif lw < 12:
            blks = 3
        else:
            blks = 4
    elif lvl == 1:
        if lw < 3:
            blks = 1
        elif lw < 6:
            blks = 2
        elif lw < 9:
            blks = 3
        elif lw < 12:
            blks = 4
        else:
            blks = 5
    elif lvl == 2:
        if lw < 5:
            blks = lw - 1
        elif lw < 8:
            blks = lw - 2
        elif lw < 11:
            blks = lw - 3
        else:
            blks = lw - 4
    elif lvl == 3:
        blks = lw
    ls = getMultiRand(range(lw), blks)
    ls.sort()
    for l in ls:
        hfwrd = rp(hfwrd, l, '_')

    return (hfwrd, ls, blks)


def help():
    global UI_flag
    UI_flag = 2
    ap.app.menu = []
    drawHelp()


def backNexit():
    global Title
    global UI_flag
    if UI_flag == 0:
        if FinishTimes == 0:
            if ap.query(cn('是否退出？'), 'query'):
                ap.app.set_exit()
        elif ap.query(cn('本次共拼写%d个单词,其中一招命中%d个(%d%%)。\n\n是否退出？' % (FinishTimes, OneShots, 100 * OneShots / float(FinishTimes))), 'query'):
            ap.app.set_exit()
    elif UI_flag == 1:
        UI_flag = 0
        Title = ' '
        ap.app.menu = Menu0
        chooseButtom(buttomimg0)
        showDicList(focus_line=Selection)
    elif UI_flag == 2:
        UI_flag = 0
        ap.app.menu = Menu0
        showDicList(focus_line=Selection)


import appuifw as ap
canvas = ap.Canvas(redraw_callback=redraw, event_callback=execute)
ap.app.body = canvas
ap.app.screen = 'full'
ap.app.exit_key_handler = backNexit
info = ap.InfoPopup()
Menu0 = [(cn('关于'), help), (cn('退出'), backNexit)]
Menu1 = [(cn('下一个词'), nextWord), (cn('上一个词'), lastWord), (cn('查看全部释义'), seeAllMeaning), (cn('切换难度'), changeLevel)]
LevelOptionList = [cn('简单（%s）' % Extra_string_list[0]), cn('中等（%s）' % Extra_string_list[1]), cn('困难（%s）' % Extra_string_list[2]), cn('变态（%s）' % Extra_string_list[3])]
drawSplashScreen()
paint_all()
e32.ao_sleep(0.1)
chooseButtom(buttomimg0)
drawWatermark(DEFAULT_BG)
makePieceimg()
for i in range(0, W + pw, pw):
    for j in range(0, H + ph, ph):
        playing_bg.blit(pieceimg, target=(i, j))

WordLines = loadDicLib()
(DicList, DicAmount) = getDicList(RES_PATH)
showDicList()
ap.app.menu = Menu0

while(1):
    e32.ao_sleep(0.1)
