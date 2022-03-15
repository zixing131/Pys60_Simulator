# -*- coding: utf-8 -*- 
"""#游戏作者：Light.紫.星
#QQ:1311817771
#游戏源码未加密，仅供学习交流，切勿用于商业用途，违者自行承担责任
#塞班论坛：bbs.dospy.com#本版本更新说明：更新全图形界面，更新提示，加大字体
#更新说明：优化代码，加入后退一步和动画效果"""
zt2=u"Sans MT 936_s60",15,1#文字字体
zt=u"Sans MT 936_s60",25,1#默认字体
VER="1.4"
import appuifw as ui
import e32
import graphics as ph,os,random,e32dbm,math,time
from BingyiApp import *
cn=lambda x:x.decode("u8")
sleep= e32.ao_sleep
try:
    os.makedirs("c:\\python")
except:
    pass
try:
    os.makedirs("c:\\python\\pygame")
except:
    pass
try:
    os.makedirs("c:\\python\\pygame\\2048")
except:
    pass
path="c:\\python\\pygame\\2048"
def log(x,y):
    return int(math.log(y)/math.log(x))
def read():
    try:
        db= e32dbm.open(path + "\\data", "r")
        tdb=db.items()
        db.close()
        return int(cn(tdb[0][1]))
    except:
        return 0
def write(v):
    db= e32dbm.open(path + "\\data", "c")
    db["score"]=str(v)
    db.close()
try:
    highs=read()
except:
    write(0)
highs=read()
class g2048:#游戏主体
    def __init__(s):
        s.menuL=[(cn("再来一局"),lambda:s.RUNB()),(cn("最高记录"),lambda:s.best()),(cn("帮助关于"),lambda:s.about()),(cn("退出游戏"),lambda:s.exit2())]
        s.high=highs
        s.bjcolor=[(205,192,180),15656154,15589576,15905145,16094563,16153695,16145979,15585138,15584353,15583312,15582527,15581742,15581850,15581999,15582500,15582800,15582999,(187,173,160)]#背景颜色
        s.img=ph.Image.new((240,320))
        s.bj=ph.Image.new((240,320))
        s.tou=ph.Image.new((240,20))
        s.kuai=ph.Image.new((59,74))
        s.bj.clear(s.bjcolor[0])
        s.kuai.clear(s.bjcolor[0])
        s.tou.clear(s.bjcolor[-1])
        s.bj.blit(s.tou,(0,0))
        for i in range(1,4):
            s.bj.line((0,20+i*75,240,20+i*75),(s.bjcolor[-1]),1)
            s.bj.line((i*60,0,i*60,320),(s.bjcolor[-1]),1)
        s.bj.text((50,17),cn("当前得分:"),0xf,zt2)
        nhour=int(time.strftime("%H"))
        t=nhour
        if t>=1 and t<=2:
            zf="夜深了，睡觉吧！"
        elif t>=3and t<=5:
            zf="半夜了，早点睡吧！"
        elif t>=6and t<=8:
            zf="早上玩游戏，精神一下！ "
        elif t>=9and t<=10:
            zf="上午好，加油哦！"
        elif t>=11and t<=12:
            zf="中午该吃午饭了！"
        elif t>=13and t<=16:
            zf="下午玩游戏，放松一下！"
        elif t>=17and t<=19:
            zf="傍晚该吃晚饭了！"
        elif t>=20and t<=21:
            zf="已经晚上了，玩盘游戏，忘记一天的烦恼！"
        elif t==0 or (t<=23 and t>=22):
            zf="现在很晚了，建议早点休息！"
        else:
            zf="你好啊，欢迎来玩【2048】！"
        jy=["紫星祝您游戏愉快！","适当游戏益脑，过度游戏伤身！",zf]
        a=random.randint(0,4)
        if a==0 or a==1:
            s.zxjy=jy[a]
        else:
            s.zxjy=zf
        s.first=1
    def RUNB(s):
        s.RUN=1
    def ai(s,fv,ci=0):
        he=0
        if fv==2:#上
            t=1
            while(t<=3):
                for i in range(4):
                    if s.game[i][t-1]==1 and t==1:
                        s.game[i][t-1]=s.game[i][t]
                        if s.game[i][t]!=1:
                            he+=1
                        s.game[i][t]=1
                    if s.game[i][t-1]==1 and t==2:
                        if s.game[i][t-2]==1:
                            s.game[i][t-2]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        else:
                            s.game[i][t-1]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                    if s.game[i][t-1]==1 and t==3:
                        if s.game[i][t-2]==1 and s.game[i][t-3]==1:
                            s.game[i][t-3]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        elif s.game[i][t-2]==1:
                            s.game[i][t-2]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        else:
                            s.game[i][t-1]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                t+=1
            if ci==1:
                return
            t=0
            while(t<=2):
                for i in range(4):
                    if s.game[i][t]==s.game[i][t+1] and s.game[i][t]!=1:
                        s.game[i][t]=s.game[i][t]*2
                        s.score+=s.game[i][t]
                        if s.game[i][t]!=1:
                            he+=1
                        s.game[i][t+1]=1
                t+=1
            s.ai(2,1)
        if fv==4:#左
            t=1
            while(t<=3):
                for i in range(4):
                    if s.game[t-1][i]==1 and t==1:
                        s.game[t-1][i]=s.game[t][i]
                        if s.game[t][i]!=1:
                            he+=1
                        s.game[t][i]=1
                    if s.game[t-1][i]==1 and t==2:
                        if s.game[t-2][i]==1:
                            s.game[t-2][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        else:
                            s.game[t-1][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                    if s.game[t-1][i]==1 and t==3:
                        if s.game[t-2][i]==1 and s.game[t-3][i]==1:
                            s.game[t-3][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        elif s.game[t-2][i]==1:
                            s.game[t-2][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        else:
                            s.game[t-1][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                t+=1
            if ci==1:
                return
            t=0
            while(t<=2):
                for i in range(4):
                    if s.game[t][i]==s.game[t+1][i] and s.game[t][i]!=1:
                        s.game[t][i]=s.game[t][i]*2
                        s.score+=s.game[t][i]
                        if s.game[t][i]!=1:
                            he+=1
                        s.game[t+1][i]=1
                t+=1
            s.ai(4,1)
        if fv==6:#右
            t=2
            while(t>=0):
                for i in range(4):
                    if s.game[t+1][i]==1 and t==2:
                        s.game[t+1][i]=s.game[t][i]
                        if s.game[t][i]!=1:
                            he+=1
                        s.game[t][i]=1
                    if s.game[t+1][i]==1 and t==1:
                        if s.game[t+2][i]==1:
                            s.game[t+2][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        else:
                            s.game[t+1][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                    if s.game[t+1][i]==1 and t==0:
                        if s.game[t+2][i]==1 and s.game[t+3][i]==1:
                            s.game[t+3][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        elif s.game[t+2][i]==1:
                            s.game[t+2][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                        else:
                            s.game[t+1][i]=s.game[t][i]
                            if s.game[t][i]!=1:
                                he+=1
                            s.game[t][i]=1
                t-=1
            if ci==1:
                return
            t=3
            while(t>=1):
                for i in range(4):
                    if s.game[t][i]==s.game[t-1][i] and s.game[t][i]!=1:
                        s.game[t][i]=s.game[t][i]*2
                        s.score+=s.game[t][i]
                        if s.game[t][i]!=1:
                            he+=1
                        s.game[t-1][i]=1
                t-=1
            s.ai(6,1)
        if fv==8:#下
            t=2
            while(t>=0):
                for i in range(4):
                    if s.game[i][t+1]==1 and t==2:
                        s.game[i][t+1]=s.game[i][t]
                        if s.game[i][t]!=1:
                            he+=1
                        s.game[i][t]=1
                    if s.game[i][t+1]==1 and t==1:
                        if s.game[i][t+2]==1:
                            s.game[i][t+2]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        else:
                            s.game[i][t+1]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                    if s.game[i][t+1]==1 and t==0:
                        if s.game[i][t+2]==1 and s.game[i][t+3]==1:
                            s.game[i][t+3]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        elif s.game[i][t+2]==1:
                            s.game[i][t+2]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                        else:
                            s.game[i][t+1]=s.game[i][t]
                            if s.game[i][t]!=1:
                                he+=1
                            s.game[i][t]=1
                t-=1
            if ci==1:
                return
            t=3
            while(t>=1):
                for i in range(4):
                    if s.game[i][t]==s.game[i][t-1] and s.game[i][t]!=1:
                        s.game[i][t]=s.game[i][t]*2
                        s.score+=s.game[i][t]
                        if s.game[i][t]!=1:
                            he+=1
                        s.game[i][t-1]=1
                t-=1
            s.ai(8,1)
        if he>0:
            s.get()
        else:
            pass
        s.die()
    def die(s):
        if s.sh==1:
            app.note2(cn("本局游戏已经结束，请重新开局！"),waitTime=2)
            return
        temp=0
        t=0
        for x in range(4):
            for y in range(4):
                if s.game[x][y]==2048 and s.da==0:
                    app.note2(cn("达成2048阶段奖励，获得2048分！"))
                    s.score+=2048
                    s.da=1
                if s.game[x][y]==1:
                    t+=1
                    temp=0
        if (s.game[1][1]!=s.game[1][0] and s.game[1][1]!=s.game[0][1] and s.game[1][1]!=s.game[2][1] and s.game[1][1]!=s.game[1][2]) and (s.game[2][2]!=s.game[2][1] and s.game[2][2]!=s.game[1][2] and s.game[2][2]!=s.game[3][2] and s.game[2][2]!=s.game[2][3]) and (s.game[0][0]!=s.game[1][0] and s.game[0][0]!=s.game[0][1] and s.game[3][0]!=s.game[2][0] and s.game[3][0]!=s.game[3][1]) and (s.game[0][3]!=s.game[1][3] and s.game[0][3]!=s.game[0][2] and s.game[3][3]!=s.game[3][2] and s.game[3][3]!=s.game[2][3]) and (s.game[2][1]!=s.game[2][0] and s.game[2][1]!=s.game[3][1] and s.game[1][2]!=s.game[0][2] and s.game[1][2]!=s.game[1][3]) and (s.game[1][0]!=s.game[2][0] and s.game[0][1]!=s.game[0][2] and s.game[1][3]!=s.game[2][3] and s.game[3][1]!=s.game[3][2]) and t==0:
            temp=1
        else:
            temp=0
        if temp==1:
            if int(s.score)<=int(s.high):
                app.query2(cn("您本次得分:"+str(s.score)+"。\n历史最高分为:"+str(s.high)+"。\n很遗憾您没能打破最高分！"),cn("游戏结束"))
            else:
                write(s.score)
                s.high=read()
                app.query2(cn("恭喜你获得最高分！\n当前最高分为:"+str(s.score)),cn("游戏结束"))
            s.sh=1
            return 1
        else:
            return 0
    def get(s):
        tx=[]
        for x in range(4):
            for y in range(4):
                if s.game[x][y]==1:
                    tx.append((x,y))
        try:
            a=random.randint(0,len(tx)-1)
            a=tx[a]
            c=random.randint(1,2)
        except:
            return
        if c==1:
            s.game[a[0]][a[1]]=2
        if c==2:
            s.game[a[0]][a[1]]=4
    def main(s):
        s.game=[[1 for a in range(4)]for b in range(4)]
        #s.game[0][0]=2048
        s.RUN=0
        s.sh=0
        s.da=0
        s.score=0
        s.get()
        s.get()
        #测试数据
        #for x in range(4):
            #for y in range(1,4):
                #s.game[x][y]=2**(y+x)
        while 1 : 
            if s.RUN == 1 : 
                s.game = [[1 for a in range(4)] for b in range(4)]
                s.azt, s.air, s.autor, s.z, s.sh, s.da, s.score = (0, 0, 0, 0, 0, 0, 0)
                s.get()
                s.get()
                s.RUN = 0
            s.img.blit(s.bj, (0, 0))
            for x in range(4):
                for y in range(4):
                    color = log(2, s.game[x][y])
                    try :
                        s.kuai.clear(s.bjcolor[color])
                    except :
                        s.kuai.clear(s.bjcolor[-1])  
                    s.bj.blit(s.kuai, ((( - x * 60) - 1), (-21 - (y * 75))))
                    if s.game[x][y] != 1 : 
                        num = int(s.game[x][y])
                        s.bj.text(((x * 60) + ((58 - (len(str(num)) * 11)) / 2), (56 + (y * 75))), cn(str(num)), 15, zt)
            s.img.text((115, 17), cn(str(s.score)), 15, zt2)
            app.blit(s.img)
            sleep(0.07)
            if s.first == 1 : 
                app.note2(cn(s.zxjy), cn('紫星寄语'), waitTime = 1.5, type = 0)
                s.first = 0
    def key(s,key):
        if key==0:
            app.menu(s.menuL)
        if key==1:
            s.ai(2)
        if key==3:
            s.ai(4)
        if key==4:
            s.ai(6)
        if key==2:
            s.ai(8)
    def exit(s):
        if app.query2(cn("要退出吗？")):
            os.abort()
    def about(s):
        app.query2(cn("游戏关于：\n\t本游戏由Light.紫.星开发。\n\t紫星QQ：1311817771。\n\t如有问题，欢迎反馈！\n游戏说明：\n\t移动数字，将相同数字融合相加，你要做的就是合成更大的数字，挑战最高分！"),cn("2048正式版v"+str(VER)))
    def best(s):
        try:
            highs=read()
        except:
            write(0)
        highs=read()
        app.query2(cn("游戏最高分："+str(highs)),cn("最高分"))
    def exit2(s):
      os.abort()
app=App()
app.TitleName=cn("Fight 2048")
app.keyType=0
app.allClass([g2048,])
#app.query2(cn("游戏关于：\n\t本游戏由Light.紫.星开发。\n\t紫星QQ：1311817771。\n\t如有问题，欢迎反馈！\n游戏说明：\n\t移动数字，将相同数字融合相加，你要做的就是合成更大的数字，挑战最高分！"),cn("2048正式版v"+str(VER)))
app.main()
