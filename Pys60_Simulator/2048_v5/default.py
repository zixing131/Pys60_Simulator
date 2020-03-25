#-*- encoding:utf-8 -*-
"""#游戏作者：Light.紫.星
#QQ:1311817771
#五版触屏移植：小迷惘°
#QQ:758212944
#游戏源码未加密，仅供学习交流，切勿用于商业用途，违者自行承担责任
#塞班论坛：bbs.dospy.com"""

import os,sys
path = os.getcwd()
index = path.rfind('\\')
mypath=path[:index]
mypath2=path+"\\2048_v5\\"
sys.path.append(mypath)
sys.path.append(mypath2)

zt=u"Sans MT 936_s60",15,1#默认字体
VER="1.2.5"
import appuifw as ui
import graphics as ph,os,random,e32dbm,math
from BingyiApp import *
cn=lambda x:x.decode("u8")
sleep=ui.e32.ao_sleep
ui.app.directional_pad=False
pan=os.getcwd()[0]
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
        db=e32dbm.open(path+"\\data","r")
        tdb=db.items()
        db.close()
        return int(cn(tdb[0][1]))
    except:
        return 0
def write(v):
    db=e32dbm.open(path+"\\data","c")
    db["score"]=str(v)
    db.close()
try:
    highs=read()
except:
    write(0)
highs=read()
class g2048:#游戏主体
    def __init__(s):
        s.high=highs
        s.bjcolor=[(205,192,180),15656154,15589576,15905145,16094563,16153695,16145979,15585138,15584353,15583312,15582527,15581742,16682527,16682800,16682999,(187,173,160)]#背景颜色
        s.img=ph.Image.new((360,640))
        s.bj=ph.Image.new((360,640))
        s.tou=ph.Image.new((340,50))
        s.mtou=ph.Image.new((160,45))
        s.kuai=ph.Image.new((84,84))
        try:
            s.tu=ph.Image.open("2048.gif")
        except:
            ui.note(cn("文件丢失！请重新安装"))
            os.abort()
        s.tu.resize((170,170))
        s.bj.clear(s.bjcolor[0])
        s.kuai.clear(s.bjcolor[0])
        s.tou.clear(s.bjcolor[-1])
        s.mtou.clear(s.bjcolor[-1])
        s.bj.blit(s.tou,target=(10,20))
        s.bj.blit(s.mtou,target=(190,80))
        s.bj.blit(s.mtou,target=(190,170))
        s.bj.blit(s.tu,target=(10,80))
        
        for i in xrange(0,5):
            s.bj.line((10,270+i*85,350,270+i*85),(s.bjcolor[-1]),1)
            s.bj.line((i*85+10,270,i*85+10,610),(s.bjcolor[-1]),1)
        s.bj.text((25,70),cn("R"),0,("dense",40,1))
        s.bj.text((310,70),cn("X"),0,("dense",40,1))
    def ai(s,fv,ci=0):
        he=0
        if fv==2:#上
            t=1
            while(t<=3):
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
                for i in xrange(4):
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
    def die(s):
        t=0
        for x in xrange(4):
            for y in xrange(4):
                if s.game[x][y]==2048 and s.da==0:
                    ui.note(cn("达成2048阶段奖励，获得2048分！"))
                    s.score+=2048
                    s.da=1
                    return 2
                if s.game[x][y]==1:
                    t+=1
        if t>0:
            return 0
        if (s.game[1][1]!=s.game[1][0] and s.game[1][1]!=s.game[0][1] and s.game[1][1]!=s.game[2][1] and s.game[1][1]!=s.game[1][2]) and (s.game[2][2]!=s.game[2][1] and s.game[2][2]!=s.game[1][2] and s.game[2][2]!=s.game[3][2] and s.game[2][2]!=s.game[2][3]) and (s.game[0][0]!=s.game[1][0] and s.game[0][0]!=s.game[0][1] and s.game[3][0]!=s.game[2][0] and s.game[3][0]!=s.game[3][1]) and (s.game[0][3]!=s.game[1][3] and s.game[0][3]!=s.game[0][2] and s.game[3][3]!=s.game[3][2] and s.game[3][3]!=s.game[2][3]) and (s.game[2][1]!=s.game[2][0] and s.game[2][1]!=s.game[3][1] and s.game[1][2]!=s.game[0][2] and s.game[1][2]!=s.game[1][3]) and (s.game[1][0]!=s.game[2][0] and s.game[0][1]!=s.game[0][2] and s.game[1][3]!=s.game[2][3] and s.game[3][1]!=s.game[3][2]):
            if s.score>s.high:
                write(s.score)
            return 1
    def get(s):
        tx=[]
        for x in xrange(4):
            for y in xrange(4):
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
        s.game=[[1 for a in xrange(4)]for b in xrange(4)]
        s.da=0
        s.score=0
        s.get()
        s.get()
        #测试数据
        #for x in xrange(4):
            #for y in xrange(1,4):
                #s.game[x][y]=2**(y+x)
        while 1:
            for x in xrange(4):
                for y in xrange(4):
                    color=log(2,s.game[x][y])
                    s.kuai.clear(s.bjcolor[color])
                    #print (-x*85-11,-271-y*85)
                    s.bj.blit(s.kuai,(-x*85-11,-271-y*85))
                    if s.game[x][y]!=1:
                        s.bj.text(((x*85+20,330+y*85)),cn(str(s.game[x][y])),0xf,("dense",30,1))
            s.img.blit(s.bj,(0,0))
            s.img.text((200,120),cn("最佳成绩："),0xf,("dense",30,1))
            s.img.text((200,210),cn("当前分数："),0xf,("dense",30,1))
            s.img.text((250,250),cn(str(s.score)),0xf,("dense",20,2))
            s.img.text((250,160),cn(str(s.high)),0xf,("dense",20,2))
            s.img.text((70,635),cn("© Light.紫.星 & 小迷惘°"),0xf,("dense",20,1))
            app.blit(s.img)
            tem=s.die()
            if tem==0:
                pass
            elif tem==1:
                if int(s.score)<=int(s.high):
                    ui.query(cn("游戏结束"),"query",cn("您本次得分:"+str(s.score)+"。历史最高分为:"+str(s.high)+"。很遗憾您没能打破最高分！"))
                else:
                    s.high=str(s.score)
                    ui.query(cn("游戏结束"),"query",cn("恭喜你获得最高分！当前最高分为:"+str(s.score)))
                break
            sleep(0.08)
    def key(s,key):
        if key==1:
            s.ai(2)
        elif key==3:
            s.ai(4)
        elif key==4:
            s.ai(6)
        elif key==2:
            s.ai(8)
        elif key==0:
            s.exit()
        elif key==5:
            s.main()
        
    def exit(s):
        if ui.query(cn("要退出吗？"),"query"):
            os.abort()

app=App()
app.TitleName=cn("2048")
app.keyType=0
app.allClass([g2048,])
app.main()
