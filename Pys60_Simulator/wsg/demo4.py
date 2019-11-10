import sys
sys.path.append(r"c:\python")
from wsg import *

def main():
    import time
    t = time.clock()
    ab = lambda:appuifw.note(cn("Hello World!"))
    import re
    fp = open(r"c:\python\lexun.txt")
    content = fp.read()
    ht = re.findall(r'<a href="(.+?)">(.+?)</a>|(<br/>)|(</div></div>)',content)
    fp.close()
    a = Window()
    x,y,w = 0,0,0
    for i in range(len(ht)):
        if ht[i][2] or ht[i][3]:
            y+=20
            x = 0
            continue
        w = Calc(cn(ht[i][1]),(FONT,16))[0]+4
        if x+w>SCRX:
            y+=20
            x = 0
            SysLink(a,cn(ht[i][1]),x,y,w,20,ab)
            x+=w
        else:
            SysLink(a,cn(ht[i][1]),x,y,w,20,ab)
            x+=w
        if y>=SCRY:
            break
    a.keyboard(1)
    a.run()
    appuifw.note(cn("耗时%s秒"%(time.clock()-t)))

main()