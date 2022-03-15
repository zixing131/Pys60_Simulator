#-*- coding:utf-8 -*-
#泡椒聊天拓展函数
#Powered By 52cyy℡
#PJChat_v1.3(Build20110906)

#圆角矩形
def rim(a,b,c,d,e=1):
    if (a,b)<(c,d):
        if e==1:return (a,b+1,a+1,b+1,a+1,b,c-1,b,c-1,b+1,c,b+1,c,d-1,c-1,d-1,c-1,d,a+1,d,a+1,d-1,a,d-1)
        elif e==2:return (a,b+2,a+1,b+1,a+2,b,c-2,b,c-1,b+1,c,b+2,c,d-2,c-1,d-1,c-2,d,a+2,d,a+1,d-1,a,d-2)
        elif e==3:return (a,b+2,a+1,b+1,a+2,b,c-2,b,c-1,b+1,c,b+2,c,d,a,d)
        elif e==4:return (a,b+2,a-1,b+1,a-2,b,c-2,b,c-1,b+1,c,b+2,c,d-2,c+1,d-1,c+2,d,a+2,d,a+1,d-1,a,d-2)

#文本换行
def tWrap(t,w=None,f=("normal",15)):
    import graphics
    import sysinfo
    if w==None:
        w=sysinfo.display_pixels()[0]
    img=graphics.screenshot()
    mt=lambda x,s=f,m=-1:\
    img.measure_text(x,font=s,maxwidth=m)
    t=t.replace("\r\n","\n").replace("\r","\n").split("\n")
    (sub,length)=([],0)
    for i in xrange(len(t)):
        if t[i]=="\n" or mt(t[i])[1]<=w:
            sub.append(t[i])
            continue
        while True:
            st=t[i][:mt(t[i],m=w)[2]-length]
            if mt(st,m=w)[1]<=w:
                sub.append(st)
                t[i]=t[i][len(st):]
                length=0
                if not t[i]:break
            else:length+=1
    del graphics,sysinfo
    return sub

#三角形
def triangle(x,y,type,len):
    if type=="left":
        return (x,y,x+len,y+len,x+len,y-len)
    elif type=="right":
        return (x,y,x-len,y+len,x-len,y-len)
    elif type=="down":
        return (x,y,x-len,y-len,x+len,y-len)
    elif type=="up":
        return (x,y,x-len,y+len,x+len,y+len)

#获取mask图片
def getmaskimg(img,type):
    import graphics
    w,h=img.size
    maskimg=graphics.Image.new(img.size,type)
    color=img.getpixel((0,0))[0]
    for y in range(h):
        line=img.getpixel([(x,y) for x in range(w)])
        for x in range(w):
            if line[x]==color:
                maskimg.point((x,y),0xff00ff)
    del graphics
    return maskimg

#获取显示时间
def getshowtime(times):
    txt = '00:00:00'
    new_time = lambda x, : ('0' * (2 - len(x))) + x 
    if times >= 3600 : 
        txt = ('%s:%s:%s' % (new_time(('%d' % (times / 3600))), new_time(('%d' % ((times % 3600) / 60))), new_time(('%d' % ((times % 3600) % 60)))))
    elif times >= 60 : 
        txt = ('00:%s:%s' % (new_time(('%d' % (times / 60))), new_time(('%d' % (times % 60)))))
    elif times != 0 : 
        txt = ('00:00:%s' % new_time(str(times)))
    return txt

#把Html文件转为Txt
def html2txt(txt):
    import re
    tags=re.compile("<.*?>",re.M)
    txt=txt.replace("%25","%").replace("%28amp;","&").replace("%3D","=").replace("%7C","|")
    txt=txt.replace("<br>","%hhf&").replace("<br/>","%hhf&")
    txt=tags.sub("",txt)
    txt=txt.replace("%hhf&","\n")
    return txt