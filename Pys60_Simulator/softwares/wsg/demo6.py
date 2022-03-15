import sys
sys.path.append(r"c:\python")
from wsg import *

bool = True
set = False

def OnClicked():
    global bool
    if bool:
        b.SetText(cn("改变"))
        c.SetText(cn("改变"))
        d.SetText(cn("改变"))
        e.SetText(cn("改变"))
        f.SetText(cn("改变"))
        g.SetText(cn("改变"))
        i.SetText(cn("改变"))
    else:
        b.SetText(cn("哈哈"))
        c.SetText(cn("哈哈"))
        d.SetText(cn("哈哈"))
        e.SetText(cn("哈哈"))
        f.SetText(cn("哈哈"))
        g.SetText(cn("哈哈"))
        i.SetText(cn("哈哈"))
    bool = not bool

def OnSet():
    global set
    if set:return
    b.SetColor(0xFF)
    b.SetFont(12)
    c.SetColor(0)
    c.SetFont(12)
    d.SetState(not d.GetState())
    e.SetState(not e.GetState())
    e.SetColor(0xFF0000)
    e.SetFont(12)
    f.SetColor(0xFF0000)
    f.SetFont(12)
    g.SetColor(0xFF0000)
    g.SetFont(12)
    i.SetFontColor(0)
    i.SetBkColor(0xFF0000)
    i.SetFont(30)
    if j.GetValue()<100.0:
        j.SetValue(100.0)
    else:
        j.SetValue(0.0)
    set = True

a = Window()
b = GroupButton(a,cn("组框"),20,20,200,100)
c = PushButton(b,cn("按下"),20,20,80,30,OnClicked)
w = Calc(cn("检查"),(FONT,16))
d = CheckButton(a,cn("检查"),20,130,20+w[0],20,0xFF0000)
w = Calc(cn("互斥"),(FONT,16))
e = RadioButton(b,cn("互斥"),110,20,20+w[0],20,0x00FF00)
w = Calc(cn("控件文字动态改变测试"),(FONT,16))
f = SysLink(b,cn("控件文字动态改变测试"),10,60,w[0]+4,w[1]+4,OnClicked)
w = Calc(cn("静态文本"),(FONT,20))
g = StaticText(a,cn("静态文本"),20,160,w[0],w[1],0,20)
h = PushButton(a,cn("设置"),80,130,60,20,OnSet,0xFF00FF,12)
i = StaticEdit(a,cn("问曰：种种因缘，在生死中不厌，何以故但二因缘说不厌？答曰：是善根备具故，在生死中苦恼薄少；譬人有疮，良药涂之，其痛瘥少。"),20,190,200,80,0xFFFFFF,12,0)
j = Trackbar(a,20,280,200,20+2+16,5.0,0.0,100.0,10.0,True,u"%.2f",Trackbar.FOLLOW,0x808080,16)
a.keyboard(1)
a.run()