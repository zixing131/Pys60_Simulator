# -*- coding: utf-8 -*-
"""#游戏作者：Light.紫.星

#QQ:1311817771
　　
#游戏源码未加密，仅供学习交流，切勿用于商业用途，违者自行承担责任
　　
#塞班论坛：bbs.dospy.com"""
zt=u"Sans MT 936_s60",15,1#默认字体
import base64, random
import graphics as ph, appuifw as ui
from BingyiApp import *
cn=lambda x:x.decode("u8")
sleep= e32.ao_sleep
if os.path.isdir("e:\\python\\pygame\\flappybird\\ph"):
    path=u"e:\\python\\pygame\\flappybird"
elif os.path.isdir("c:\\python\\pygame\\flappybird\\ph"):
    path=u"c:\\python\\pygame\\flappybird"
elif os.path.isdir("../../python/pygame/flappybird/ph"):
    path= u"../../python/pygame/flappybird"
else: 
    ui.note(cn("游戏数据损坏，请重新安装游戏！"))
def read(vpath,value):#读取
    try:
        go=open(vpath,"r")
    except:
        go=open(vpath,"w")
        go.write(value)
        go.close()
        go=open(vpath,"r")
    go1=go.read()
    go.close()
    go2=base64.decodestring(go1.encode("u8"))
    if go2==u"None":
        go2=base64.decodestring(value.encode("u8"))
        return int(go2)
    else:
        return int(go2)
def write(wpath,va):#写入
    v2=base64.encodestring(str(va))
    go=open(wpath,"w")
    go.write(v2)
    go.close()
class birdload(object,):
    def __init__(s):
        s.rate=ph.Image.open(path+"\\ph\\rate.png")
        s.ratea=ph.Image.new((65,38),"1")
        s.ratea.load(path+"\\ph\\ratea.png")
        s.img=ph.Image.new((240,320))
        s.logo=ph.Image.open(path+"\\ph\\logo.png")
        s.logoa=ph.Image.new((180,50),"1")
        s.logoa.load(path+"\\ph\\logozhe.png")
        t=read(path+"\\data\\setbj.ini",u"Mw==")
        if t==1:
            s.bjchoice=1
        elif t==2:
            s.bjchoice=2
        else:
            s.bjchoice=random.randint(1,2)
        if s.bjchoice==1:#载入白天
            s.bj=ph.Image.open(path+"\\ph\\day.png")
        elif s.bjchoice==2:#夜间
            s.bj=ph.Image.open(path+"\\ph\\night.png")
        else:
            pass
        t=read(path+"\\data\\setbird.ini",u"NA==")
        if t==1:
            s.birdcolor=3
        elif t==2:
            s.birdcolor=1
        elif t==3:
            s.birdcolor=2
        else:
            s.birdcolor=random.randint(1,3)
        s.birdcolor=random.randint(1,3)#随机选择bird颜色
        if s.birdcolor==1:#红
            s.birda=ph.Image.open(path+"\\ph\\reda.png")
            s.birdb=ph.Image.open(path+"\\ph\\redb.png")
            s.birdc=ph.Image.open(path+"\\ph\\redc.png")
        elif s.birdcolor==2:#黄
            s.birda=ph.Image.open(path+"\\ph\\yellowa.png")
            s.birdb=ph.Image.open(path+"\\ph\\yellowb.png")
            s.birdc=ph.Image.open(path+"\\ph\\yellowc.png")
        elif s.birdcolor==3:#蓝
            s.birda=ph.Image.open(path+"\\ph\\bluea.png")
            s.birdb=ph.Image.open(path+"\\ph\\blueb.png")
            s.birdc=ph.Image.open(path+"\\ph\\bluec.png")
        else:pass
        #生成bird遮罩
        s.maska=ph.Image.new((40,40),"1")
        s.maska.load(path+"\\ph\\maska.png")#上
        s.maskb=ph.Image.new((40,40),"1")
        s.maskb.load(path+"\\ph\\maskb.png")#中
        s.maskc=ph.Image.new((40,40),"1")
        s.maskc.load(path+"\\ph\\maskc.png")#下
        s.quit=ph.Image.open(path+"\\ph\\quit.png")
        s.start=ph.Image.open(path+"\\ph\\start.png")
        s.starta=ph.Image.new((105,59),"1")
        s.starta.load(path+"\\ph\\startzhe.png")
        s.run=ph.Image.open(path+"\\ph\\run.png")
    def main(s):
        s.birdf=1
        s.mark=0
        s.runa=1
        while s.runa:
            s.img.blit(s.bj,(0,0))
            if s.birdf==1:
                s.bird=s.birda
                s.maskf=s.maska
            elif s.birdf==2:
                s.bird=s.birdb
                s.maskf=s.maskb
            elif s.birdf==3:
                s.bird=s.birdc
                s.maskf=s.maskc
            else:pass
            s.mark+=3
            if s.mark>30:
                s.mark=7
            s.img.blit(s.run,(s.mark,-260))
            if s.birdf>2:
                s.birdf=1
            else:
                s.birdf+=1
            s.img.blit(s.start,(-5,-200),mask=s.starta)
            s.img.blit(s.quit,(-130,-200),mask=s.starta)
            s.img.blit(s.logo,(-30,-25),mask=s.logoa)
            s.img.blit(s.rate,(-90,-140),mask=s.ratea)
            s.img.blit(s.bird,(-90,-90),mask=s.maskf)
            app.blit(s.img)
            sleep(0.08)
    def key(s,key):
        if key==5:
            app.main(1)
    def exit(s):
        if app.query2(cn("要退出吗？"),type=0):
            os.abort()
class flappy(object,):
    def __init__(s):
        s.img=ph.Image.new((240,320))
        s.birdb=ph.Image.open(path+"\\ph\\blueb.png")
        s.maskb=ph.Image.new((40,40),"1")
        s.maskb.load(path+"\\ph\\maskb.png")
        s.choose()
        s.jindu(0,30)
        s.gpipu=ph.Image.open(path+"\\ph\\greenta.png")
        s.new=ph.Image.open(path+"\\ph\\new.png")
        gdc=random.randint(1,100)
        if gdc==88:
            app.note2(cn("恭喜你中奖了，给你加十分!"),title=cn("中奖"),type=0)
            s.score=1500
            s.gpipu=ph.Image.open(path+"\\ph\\redta.png")
        else:
            s.gpipu=ph.Image.open(path+"\\ph\\greenta.png")
            s.score=0
        s.sp=read(path+"\\data\\speed.ini",u"Ng==")
        s.long=read(path+"\\data\\long.ini",u"Njk=")
        s.nand=read(path+"\\data\\sety.ini",u"MTA=")
        s.nanf=read(path+"\\data\\setx.ini",u"MzA=")
        s.jindu(30,60)
        #生成bird遮罩
        s.maska=ph.Image.new((40,40),"1")
        s.maska.load(path+"\\ph\\maska.png")#上
        s.maskb=ph.Image.new((40,40),"1")
        s.maskb.load(path+"\\ph\\maskb.png")#中
        s.maskc=ph.Image.new((40,40),"1")
        s.maskc.load(path+"\\ph\\maskc.png")#下
        s.maskd=ph.Image.new((40,40),"1")
        s.jindu(60,120)
        s.maskd.load(path+"\\ph\\maskd.png")#俯冲
        s.run=ph.Image.open(path+"\\ph\\run.png")#前进条
        s.gpipd=ph.Image.open(path+"\\ph\\greentb.png")
        s.maskpu=ph.Image.new((52,321),"1")
        s.maskpu.load(path+"\\ph\\up.png")#上
        s.maskpd=ph.Image.new((52,321),"1")
        s.maskpd.load(path+"\\ph\\down.png")#下
        s.click=ph.Image.open(path+"\\ph\\click.png")
        s.clicka=ph.Image.new((120,100),"1")
        s.clicka.load(path+"\\ph\\clickzhe.png")
        s.logo=ph.Image.open(path+"\\ph\\logo.png")
        s.logoa=ph.Image.new((180,50),"1")
        s.logoa.load(path+"\\ph\\logozhe.png")
        s.ready=ph.Image.open(path+"\\ph\\getready.png")
        s.readya=ph.Image.new((186,51),"1")
        s.readya.load(path+"\\ph\\getreadyzhe.png")
        s.over=ph.Image.open(path+"\\ph\\gameover.png")
        s.overa=ph.Image.new((192,51),"1")
        s.overa.load(path+"\\ph\\gameoverzhe.png")
        s.scorea=ph.Image.open(path+"\\ph\\score.png")
        s.jindu(120,180)
        s.scoreb=ph.Image.new((226,114),"1")
        s.scoreb.load(path+"\\ph\\scorezhe.png")
        s.medala=ph.Image.new((45,45),"1")
        s.medala.load(path+"\\ph\\medal.png")
        s.goal=ph.Image.open(path+"\\ph\\goal.png")
        s.silver=ph.Image.open(path+"\\ph\\silver.png")
        s.tong=ph.Image.open(path+"\\ph\\tong.png")
        s.iron=ph.Image.open(path+"\\ph\\iron.png")
        s.new=ph.Image.open(path+"\\ph\\new.png")
        s.quit=ph.Image.open(path+"\\ph\\quit.png")
        s.start=ph.Image.open(path+"\\ph\\start.png")
        s.starta=ph.Image.new((105,59),"1")
        s.starta.load(path+"\\ph\\startzhe.png")
        s.jindu(180,220)
        #上下鸟
        s.sbs=ph.Image.open(path+"\\ph\\sbs.png")
        s.sbx=ph.Image.open(path+"\\ph\\sbx.png")
        s.sbp=ph.Image.open(path+"\\ph\\sbp.png")
        s.sys=ph.Image.open(path+"\\ph\\sys.png")
        s.syx=ph.Image.open(path+"\\ph\\syx.png")
        s.syp=ph.Image.open(path+"\\ph\\syp.png")
        s.srs=ph.Image.open(path+"\\ph\\srs.png")
        s.srx=ph.Image.open(path+"\\ph\\srx.png")
        s.srp=ph.Image.open(path+"\\ph\\srp.png")
        s.xbp=ph.Image.open(path+"\\ph\\xbp.png")
        s.xyp=ph.Image.open(path+"\\ph\\xyp.png")
        s.xrp=ph.Image.open(path+"\\ph\\xrp.png")
        #bird的up,down遮罩
        s.dz=ph.Image.new((40,40),"1")
        s.dz.load(path+"\\ph\\dz.png")
        s.uu=ph.Image.new((40,40),"1")
        s.uu.load(path+"\\ph\\uu.png")
        s.ud=ph.Image.new((40,40),"1")
        s.ud.load(path+"\\ph\\ud.png")
        s.uz=ph.Image.new((40,40),"1")
        s.uz.load(path+"\\ph\\uz.png")
        s.jindu(220,240)
        s.choice()
    def setbj(s,t):
        write(path+"\\data\\setbj.ini",t)
        app.note2(cn("设置成功！"),type=0)
    def setbird(s,t):
        write(path+"\\data\\setbird.ini",t)
        app.note2(cn("设置成功！"),type=0)
    def setx(s):
        temp=app.query(cn("（越大越快,下次生效,默认为30）"),title=cn("设置小鸟上升速度"),type="text")
        try:
            temp=int(temp)
        except:
            app.note2(cn("请输入数字！"),type=0)
            return
        if temp>180:
            app.note2(cn("这个速度你不可能玩过去的！"),type=0)
        elif temp==0:
            app.note2(cn("如果你想飞不起来的话就这样吧～～"),type=0)
            write(path+"\\data\\setx.ini",temp)
        else:
            app.note2(cn("设置成功！"),type=0)
            write(path+"\\data\\setx.ini",temp)
        del temp
    def sety(s):
        temp=app.query(cn("（越大越快,下次生效,默认为10）"),title=cn("设置小鸟下降速度"),type="number")
        try:
            temp=int(temp)
        except:
            app.note2(cn("请输入数字"),type=0)
            return
        if temp>180:
                app.note2(cn("这个速度你不可能玩过去的！"),type=0)
        elif temp==0:
            app.note2(cn("如果你真想下不去的话就这样吧～～"),type=0)
            write(path+"\\data\\sety.ini",temp)
        else:
            app.note2(cn("设置成功！"),type=0)
            write(path+"\\data\\sety.ini",temp)
        del temp
    def setj(s):
        temp=app.query(cn("越大越快,下次生效,默认为1（设置为负数会有奇怪的事情发生哦！）"),title=cn("设置加速度"),type="text")
        try:
            temp=int(temp)
        except:
            app.note2(cn("请输入数字！"),type=0)
            return
        if temp<0:
            app.note2(cn("接下来会有奇怪的事情发生！"),type=0)
        else:
            app.note2(cn("设置成功！"),type=0)
        write(path+"\\data\\jsd.ini",str(temp))
        del temp
    def seta(s):#游戏速度
        temp=app.query(cn("（越大越快,下次生效,点击取消则为默认的6）"),title=cn("输入游戏速度"),type="text")
        try:
            temp=int(temp)
        except:
            app.note2(cn("请输入数字！"),type=0)
            return
        if temp>80:
            app.note2(cn("这个速度你不可能玩过去的！"),type=0)
        elif temp==0:
            app.note2(cn("如果你真想原地不动的话就这样吧～～"),type=0)
            write(path+"\\data\\speed.ini",temp)
        else:
            app.note2(cn("设置成功！"),type=0)
            write(path+"\\data\\speed.ini",temp)
        del temp
    def setb(s):#管道间隔
        temp=app.query(cn("（下次生效,,点击取消则为默认的69）"),title=cn("输入管道上下间隔"),type="number")
        try:
            temp=int(temp)
        except:
            app.note2(cn("请输入数字！"),type=0)
            return
        if temp>100:
            app.note2(cn("别以为我不知道你想的什么！"),type=0)
        elif temp<50:
            app.note2(cn("据我所知，这样的宽度没人能玩过去！"),type=0)
        else:
            app.note2(cn("设置成功！"),type=0)
            write(path+"\\data\\long.ini",temp)
        del temp
        s.game=0
    def help(s):
        app.query2(cn("本游戏为像素鸟(flappy bird)的塞班py版本，游戏操作很简单，点击5键或OK键使小鸟向上飞，如果你碰到障碍物或者掉到地上，那么游戏结束，本游戏图片资源全部取自安卓版flappy bird。\nEnjoy it!"),title=cn("游戏帮助"),type=0)
    def about(s):
        app.query2(cn("本游戏由塞班论坛 Light.紫.星 开发\n紫星QQ：1311817771\n如有问题，欢迎反馈！\n本版本感谢～あ冰^o^翼げ～的大力支持！\n另外感谢小迷惘°和Smile.醉.嵩的友情测试！\n\n"),title=cn("游戏关于"),type=0)
    def choice(s):
        t=read(path+"\\data\\setbird.ini",u"NA==")
        if t==1:
            birdcolor=3
        elif t==2:
            birdcolor=1
        elif t==3:
            birdcolor=2
        else:
            birdcolor=random.randint(1,3)
        if birdcolor==1:#红
            s.birda=ph.Image.open(path+"\\ph\\reda.png")
            s.birdb=ph.Image.open(path+"\\ph\\redb.png")
            s.birdc=ph.Image.open(path+"\\ph\\redc.png")
            s.birdd=ph.Image.open(path+"\\ph\\redd.png")
            s.birdx=ph.Image.open(path+"\\ph\\srs.png")
            s.birdy=ph.Image.open(path+"\\ph\\srp.png")
            s.birdz=ph.Image.open(path+"\\ph\\srx.png")
            s.birdp=ph.Image.open(path+"\\ph\\xrp.png")
        elif birdcolor==2:#黄
            s.birda=ph.Image.open(path+"\\ph\\yellowa.png")
            s.birdb=ph.Image.open(path+"\\ph\\yellowb.png")
            s.birdc=ph.Image.open(path+"\\ph\\yellowc.png")
            s.birdd=ph.Image.open(path+"\\ph\\yellowd.png")
            s.birdx=ph.Image.open(path+"\\ph\\sys.png")
            s.birdy=ph.Image.open(path+"\\ph\\syp.png")
            s.birdz=ph.Image.open(path+"\\ph\\syx.png")
            s.birdp=ph.Image.open(path+"\\ph\\xyp.png")
        elif birdcolor==3:#蓝
            s.birda=ph.Image.open(path+"\\ph\\bluea.png")
            s.birdb=ph.Image.open(path+"\\ph\\blueb.png")
            s.birdc=ph.Image.open(path+"\\ph\\bluec.png")
            s.birdd=ph.Image.open(path+"\\ph\\blued.png")
            s.birdx=ph.Image.open(path+"\\ph\\sbs.png")
            s.birdy=ph.Image.open(path+"\\ph\\sbp.png")
            s.birdz=ph.Image.open(path+"\\ph\\sbx.png")
            s.birdp=ph.Image.open(path+"\\ph\\xbp.png")
        else:
            pass
    def choose(s):
        t=read(path+"\\data\\setbj.ini",u"Mw==")
        if t==1:
            bjchoice=1
        elif t==2:
            bjchoice=2
        else:
            bjchoice=random.randint(1,2)
        if bjchoice==1:#载入白天
            s.bj=ph.Image.open(path+"\\ph\\day.png")
            s.bj0=ph.Image.open(path+"\\ph\\day.png")
            s.bj0.text((50,260),cn("载入中，请稍等……"),0xf,zt)
        elif bjchoice==2:#夜间
            s.bj=ph.Image.open(path+"\\ph\\night.png")
            s.bj0=ph.Image.open(path+"\\ph\\night.png")
            s.bj0.text((50,260),cn("载入中，请稍等……"),0xf,zt)
        else:pass
    def jindu(s,a,b):#进度条
        for i in range(a,b+2,3):
            s.img.blit(s.bj0,(0,0))
            s.img.blit(s.birdb,(-i,-130),mask=s.maskb)
            s.img.text((110,180),cn(str((int(i/2.39)))+" ％"),0,zt)
            app.blit(s.img)
    def died(s):
        s.game=2
        s.m=260
        s.high=read(path+"\\data\\h.ini","MA==")
        sc=(s.score-210)/138+1
        if sc<0:
            sc=0
        #high=1
        #sc=25
        if sc>s.high:
            app.note2(cn("恭喜您获得最高分:"+str(sc)+"分！"),title=cn("新记录"),type=0)
            write(path+"\\data\\h.ini",str(sc))
            s.pai=s.goal
            s.high=sc
        elif sc<=s.high:
            app.note2(cn("这次你得了"+str(sc)+"分"),cn("游戏结束"),type=0)
            try:
                del s.new
            except:
                pass
        s.y=100
        s.birdf=1
    def drop(s,value):
        s.down-=1
        s.flyt-=1
        s.jsd+=s.setjsd
        s.y+=value+s.jsd#加速度
        if s.flyt>10:
            s.press=2
        elif s.down<0:
            s.birdf=3
        else:
            pass
        if s.birdf==17:
            pass
        else:
            s.birdf+=1
        if s.y>230:
            s.y=0
            s.died()
        elif s.y<-15:
            s.y=0
            if s.birdf>2:
                s.birdf=1
            else:
                s.birdf+=1
        else:
            pass
    def fl(s):
        if s.game==0:
            s.game=1
        elif s.game==2:
            s.game,s.press=0,1
            s.choose()
            s.choice()
            s.score=0
            #抽奖功能
            s.gpipu=ph.Image.open(path+"\\ph\\greenta.png")
            s.new=ph.Image.open(path+"\\ph\\new.png")
            gdc=random.randint(1,100)
            if gdc==88:
                app.note2(cn("恭喜你中奖了，给你加十分!"),title=cn("中奖"),type=0)
                s.score=1500
                s.gpipu=ph.Image.open(path+"\\ph\\redta.png")
            else:
                s.gpipu=ph.Image.open(path+"\\ph\\greenta.png")
                s.score=0
            s.sp=read(path+"\\data\\speed.ini",u"Ng==")
            s.long=read(path+"\\data\\long.ini",u"Njk=")
            s.nand=read(path+"\\data\\sety.ini",u"MTA=")
            s.nanf=read(path+"\\data\\setx.ini",u"MzA=")
            s.setjsd=read(path+"\\data\\jsd.ini","MQ==")
        else:
            pass
        if s.press==1:
            s.press=2
        else:
            s.press=1
    def fly(s,value):
        s.jsd=0
        s.down=10
        s.down-=1
        s.flyt+=1
        if s.flyt>10:
            s.press=2
        elif s.down<0:
            s.birdf=0
        else:
            if s.birdf>13 or s.birdf<5:
                s.birdf=5
            else:
                s.birdf+=1
        s.y-=value
        #s.birdf=1
        if s.y>230:
            s.died()
        elif s.y<-15:
            s.y=0
        else:
            pass
    def pip(s,long):
        s.bpx=s.x-15#birdplacex
        s.bpy=s.y+15#birdplacey
        s.img.blit(s.gpipd,(-s.m,-s.l1+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m,-s.l1-s.long+34),mask=s.maskpu)
        if(abs(s.m-s.bpx)<=40 and abs(s.bpy-s.l1)>s.long-40):
            s.died()
        else:
            pass
        s.img.blit(s.gpipd,(-s.m-140,-s.l2+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m-140,-s.l2-s.long+34),mask=s.maskpu)
        if(abs(s.m+140-s.bpx)<=40 and abs(s.bpy-s.l2)>s.long-40):
            s.died()
        else:
            pass
        s.img.blit(s.gpipd,(-s.m-280,-s.l3+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m-280,-s.l3-s.long+34),mask=s.maskpu)
        if(abs(s.m+280-s.bpx)<=40 and abs(s.bpy-s.l3)>s.long-40):
            s.died()
        else:
            pass
        s.img.blit(s.gpipd,(-s.m-420,-s.l4+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m-420,-s.l4-s.long+34),mask=s.maskpu)
        if(abs(s.m+420-s.bpx)<=40 and abs(s.bpy-s.l4)>s.long-40):
            s.died()
        else:
            pass
        s.img.blit(s.gpipd,(-s.m-560,-s.l1+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m-560,-s.l1-s.long+34),mask=s.maskpu)
        if(abs(s.m+560-s.bpx)<=40 and abs(s.bpy-s.l1)>s.long-40):
            s.died()
        else:
            pass
        s.img.blit(s.gpipd,(-s.m-700,-s.l2+286+s.long),mask=s.maskpd)
        s.img.blit(s.gpipu,(-s.m-700,-s.l2-s.long+34),mask=s.maskpu)
        if(abs(s.m+700-s.bpx)<=40 and abs(s.bpy-s.l2)>s.long-40):
            s.died()
        else:
            pass
    def main(s):
        s.setjsd=read(path+"\\data\\jsd.ini","MQ==")
        s.jsd=2
        s.m,s.high,s.x,s.y,s.game,s.flyt,s.down,s.birdf,s.press,s.game,s.score=260,0,57,100,0,0,0,1,1,0,0#预处理数据
        s.mark,s.down=1,10
        s.menuL=[(cn("难度设置"),((cn("设置上升速度"),lambda:s.setx()),(cn("设置下落速度"),lambda:s.sety()),(cn("设置加速度"),lambda:s.setj()))),(cn("背景设置"),((cn("白天"),lambda:s.setbj(1)),(cn("夜间"),lambda:s.setbj(2)),(cn("随机"),lambda:s.setbj(3)))),(cn("bird颜色"),((cn("蓝色"),lambda:s.setbird(1)),(cn("红色"),lambda:s.setbird(2)),(cn("黄色"),lambda:s.setbird(3)),(cn("随机"),lambda:s.setbird(4)))),(cn("游戏速度"),lambda:s.seta()),(cn("管道间隔"),lambda:s.setb()),(cn("游戏帮助"),lambda:s.help()),(cn("游戏关于"),lambda:s.about()),(cn("退出游戏"),lambda:s.exit())]
        s.l1=random.randint(70,190)#随机的管道位置
        s.l2=random.randint(70,190)
        s.l3=random.randint(70,190)
        s.l4=random.randint(70,190)
        while 1:
            if s.birdf==1:
                s.bird=s.birda
                s.maskf=s.maska
            elif s.birdf==2:
                s.bird=s.birdb
                s.maskf=s.maskb
            elif s.birdf==3:
                s.bird=s.birdc
                s.maskf=s.maskc
            elif s.birdf==4:
                s.bird=s.birdd
                s.maskf=s.maskd
            elif s.birdf==5:
                s.bird=s.birdx
                s.maskf=s.ud
            elif s.birdf==6:
                s.bird=s.birdx
                s.maskf=s.ud
            elif s.birdf==7:
                s.bird=s.birdx
                s.maskf=s.ud
            elif s.birdf==8:
                s.bird=s.birdy
                s.maskf=s.uz
            elif s.birdf==9:
                s.bird=s.birdy
                s.maskf=s.uz
            elif s.birdf==10:
                s.bird=s.birdy
                s.maskf=s.uz
            elif s.birdf==11:
                s.bird=s.birdz
                s.maskf=s.uu
            elif s.birdf==12:
                s.bird=s.birdz
                s.maskf=s.uu
            elif s.birdf==13:
                s.bird=s.birdz
                s.maskf=s.uu
            elif s.birdf==14:
                s.bird=s.birdb
                s.maskf=s.maskb
            elif s.birdf==15:
                s.bird=s.birdb
                s.maskf=s.maskb
            elif s.birdf==16:
                s.bird=s.birdb
                s.maskf=s.maskb
            elif s.birdf==17:
                s.bird=s.birdp
                s.maskf=s.dz
            else:pass
            s.mark+=s.sp
            if s.mark>20:
                s.mark=1
            else:
                pass
            s.img.blit(s.bj,(0,0))
            if s.game==0:
                s.img.blit(s.run,(s.mark,-260))
                s.img.text((7,305),cn("菜单"),0xf,zt)
                s.img.text((200,305),cn("退出"),0xf,zt)
                if s.birdf>2:
                    s.birdf=1
                else:
                    s.birdf+=1
                s.img.blit(s.bird,(-50,-s.y),mask=s.maskf)
                s.img.blit(s.ready,(-25,-30),mask=s.readya)
                s.img.blit(s.click,(-60,-130),mask=s.clicka)
            elif s.game==1:
                s.m-=s.sp
                s.score+=s.sp
                if s.m<-480:
                    s.l3=random.randint(70,190)
                    s.l4=random.randint(70,190)
                    s.m=80
                else:
                    pass
                if s.press==1:
                    s.fly(s.nanf)
                    s.press=2
                else:
                    s.drop(s.nand)
                    s.press=2
                s.pip(s.long)
                s.img.blit(s.run,(s.mark,-260))
                s.img.blit(s.bird,(-50,-s.y),mask=s.maskf)
                stmp=(s.score-210)/138+1
                if stmp<1:
                    stmp=0
                else:
                     pass
                s.img.text((103,30),cn(""+str(stmp)),0xf,zt)
                del stmp
            elif s.game==2:
                stmp=(s.score-210)/138+1
                s.img.blit(s.over,(-25,-50),mask=s.overa)
                s.img.blit(s.scorea,(-7,-100),mask=s.scoreb)
                s.img.text((183,153),cn(""+str(stmp)),0xf,zt)
                s.img.text((183,192),cn(""+str(s.high)),0xf,zt)
                s.img.text((40,250),cn("点击确认键或5键重新开始"),0xf,zt)
                s.img.blit(s.start,(-2,-260),mask=s.starta)
                s.img.blit(s.quit,(-135,-260),mask=s.starta)
                if stmp<s.high and stmp<20:
                    try:
                        del s.pai
                    except:pass
                elif stmp>s.high:
                    s.high=stmp
                    s.pai=s.goal
                elif stmp>20 and stmp<=40:
                    s.pai=s.iron#铁牌
                elif stmp>40 and stmp<=60:
                    s.pai=s.tong#铜牌
                elif stmp>60 and stmp<=80:
                    s.pai=s.silver#银牌
                elif stmp>80:
                    s.pai=s.goal#金牌
                else:
                    pass
                try:
                    s.img.blit(s.pai,(-32,-142),mask=s.medala)
                    s.img.blit(s.new,(-140,-158))
                except:
                    pass
            app.blit(s.img)
            sleep(0.08)
    def key(s,key):
      #上下左右(或2,8,4,6)控制
        if key==5:
            s.fl()
        elif key==0:
            app.menu(s.menuL)
    def exit(s):
        if app.query2(cn("要退出吗"),title=cn("flappy bird"),type=0):
            os.abort()
app=App()
app.TitleName=cn("flappy bird")
#app.keyType=0
app.allClass([birdload,flappy])
app.main()
