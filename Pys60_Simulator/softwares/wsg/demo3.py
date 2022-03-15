import sys
sys.path.append(r"c:\python")
from wsg import *

ab = lambda:appuifw.note(cn("Hello World!"))

def main():
    a = Window()
    PushButton(a,cn("弹出"),20,20,80,30,ab)
    b = GroupButton(a,cn("组框"),20,60,100,70)
    PushButton(b,cn("嵌套"),10,20,80,30,ab)
    CheckButton(a,cn("检查"),20,150,52,20)
    RadioButton(a,cn("互斥"),20,180,52,20).SetState(1)
    SysLink(a,cn("超链"),20,210,36,20,ab)
    StaticText(a,cn("静态文本"),20,240,68,20,0xFF0000)
    StaticEdit(a,cn("类Windows XP的GUI框架(实际并未模拟消息循环)，目前封了PushButton,CheckButton,RadioButton,GroupButton,SysLink,StaticText(单行),StaticEdit,但还不支持动态添加控件。此为静态编辑控件(暂时还不能编辑...)，操作:焦点移动到此控件，按下OK键即进入滚动状态(当然以可以滚动为前提)，再次按下OK键则离开滚动状态。"),80,135,120,100)
    Trackbar(a,20,280,200,34,5,0,100,30,True,u"%.2f",Trackbar.FOLLOW,0x808080,12)
    a.run()
    
main()