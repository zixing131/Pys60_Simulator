# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import sysinfo
DATA_PATH = 'C:\\DATA\\2048_profile'
W, H = sysinfo.display_pixels()
portrait = W < H and 1 or 0
def cn(string):
    try:
        return string.decode('utf-8')
    except:
        return string


TWIP = 5
TILE = 55
FIELD = 220
STEP = (H / 10)
LX = portrait and 10 or 50
TY = portrait and 55 or 15
RX = LX + FIELD
BY = TY + FIELD
loc = [[[0, 0] for i in range(4)] for i in range(4)]
for i in range(len(loc)):
    for j in range(len(loc)):
        loc[i][j] = ((i * TILE) + LX, (j * TILE) + TY)
MAX_UNDO_STEPS = 20
UndoOptionList = (1, 3, 5, 10, 20, 50, 99)
UndoBarScale = (3, 9, 17, 29, 44, 60, 82)
DevelopOptionList = [cn('滑动步长(简单)'), cn('滑动步长(高级)'), cn('输入命令')]
score_num_loc = (LX, (TY - 12))
undo_x, undo_y = ((RX - 56), score_num_loc[1])
hs_x, hs_y = (LX, 50)
date_x, date_y = ((W / 2), 50)
dat = [([0] * 4) for i in range(4)]
SlideRange = [25, 15, 5]
ScrollRange = [50, 40, 30, 20, 10]
sumscore = 0
snlg_flag = 0
undo_option_flag = 4
max_undo_chances = UndoOptionList[undo_option_flag]
undo_chances = max_undo_chances
sumscore_flag = 0
four = 2
numlist = [2 for i in xrange((9 - four))] + [4 for i in xrange(four)]
dat_bak = []
sumscore_bak = []
read_values = []
hs = []
Xcode = '0000'
is_move = 0
UI_flag = 8
screen_loc = (2 * H)
won = 0
end = 0
MapPointer = 0
BgPointer = 0
SelectedItem = 0