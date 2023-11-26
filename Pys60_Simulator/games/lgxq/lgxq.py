# -*- coding: utf-8 -*-
cn=lambda x:x.decode('u8')
zh=lambda x:x.encode('u8')

import os,sys
path = os.getcwd()
index = path.rfind('\\')
mypath=path[:index]
mypath2=path+'\\'
sys.path.append(mypath)
sys.path.append(mypath2)

import wif
import graphics,e32,random
import appuifw as appuifw2
import os,time
from wif_keys import *
import pickle

def fileOpen(name,mode):
    name = cn(name)
    return open(name,mode)

####以下必须类####
class jbcs(object):
    fileurl=mypath2
    def __getitem__(self,name):
        return self.v.get(name,False)
    def __setitem__(self,name,value):
        self.v[name]=value
    def get(self,name,value=None):
        return self.v.get(name,value)
    def names(self,daturl):
        fp=fileOpen('%s%s.dat'%(self.fileurl,daturl),'r')
        na=fp.read()
        fp.close()
        na=na.split(' ')
        random.shuffle(na)
        random.shuffle(na)
        return random.choice(na)


try:
    import  _md5
except:
    import md5 as _md5

class gj(jbcs):
    def __init__(self):
        """国家类"""
        self.v={}
        self.vlen=0
        self.gq=[]
    def new(self):
        """新建国家"""
        r=random.randint
        self.vlen+=1
        id=self.vlen
        self.v[id]={'id':id,
            '国家名':self.names('国家名称'),
            '国旗':r(0,0xffffff),
            '首都':None,
            '地区':[],
            '税收':{'商业':0.25,'农业':0.12},
            '货币':5000,
            '行动力':0,
            '科技':0,
            '外交':{}
            }
        while 1:
            if self.v[id]['国旗'] in self.gq:
                self.v[id]['国旗']=r(0,0xffffff)
            else:
                self.gq.append(self.v[id]['国旗'])
                break
        return id


class dq(jbcs):
    def __init__(self):
        """地区类"""
        self.v={}
        self.vlen=0
    def new(self,gjid,xy):
        r=random.randint
        self.vlen+=1
        self.v[self.vlen]={
            'id':self.vlen,
            '地区名':None,
            '国家':gjid,
            '地块':[xy],
            '人口数':r(0,120),
            '兵力':r(0,20),
            '经济':r(0,120),
            '粮食':{'流通':r(0,60000),'国库':r(0,120)},
            '坐标':xy}
        if not self.v[self.vlen]['地区名']:
            self.v[self.vlen]['地区名']=self.names('地区名称')
        return self.vlen


class dt(jbcs):
    def __init__(self):
        """地图类"""
        #self.dx=['大海','山1','山2','平原','树1','树2','沙漠']
        dx=os.listdir(cn("%s\\图片\\地形\\"%self.fileurl))
        self.dx=[na[:na.find('.')] for na in dx]
        self.lx=['商业用地','农业用地','住宅用地']
        self.v={}
        self.dtxz=10
    def __getitem__(self,name):
        x,y=name
        dtxz=self.dtxz
        if x<-dtxz:
            x=dtxz*2+x
        if y<-dtxz:
            y=dtxz*2+y
        if x>dtxz:
            x=x-dtxz*2
        if y>dtxz:
            y=y-dtxz*2
        if x==-dtxz:
            x=dtxz
        if y==-dtxz:
            y=dtxz
        name=(x,y)
        if self.v.get(name,False)==False:
            self.new(name)
        return self.v.get(name,False)
    def new(self,xy):
        dx=random.choice(self.dx)
        self.v[xy]={
            '地区':None,
            '地形':dx,
            '类型':random.choice(self.lx),}
        aaa=random.choice(['新建','合并','新建','合并','新建','合并'])
        aab=random.choice(['新建','合并','新建','合并','新建','合并'])
        if aaa=='新建':
            gjid=sjk['国家'].new()
            aab='新建'
        else:
            aac=[(xy[0]-1,xy[1]),(xy[0]+1,xy[1]),(xy[0],xy[1]-1),(xy[0],xy[1]+1)]
            random.shuffle(aac)
            for na in aac:
                if self.v.get(na,False):
                    dqid=self.v[na]['地区']
                    gjid=sjk['地区'][dqid]['国家']
                    break
            else:
                gjid=sjk['国家'].new()
                aaa=aab='新建'
        if aab=='新建':
            dqid=sjk['地区'].new(gjid,xy)
        self.v[xy]['地区']=dqid
        gjdx=sjk['国家'][gjid]
        if aab=='新建':
            gjdx['地区'].append(dqid)
        else:
            sjk['地区'][dqid]['地块'].append(xy)
        if aaa=='新建':
            gjdx['首都']=dqid
        return xy



class tj(jbcs):
    class tjsj(jbcs):
        def __init__(self):
            """统计世界"""
            self.v={}
        def __getitem__(self,name):
            if self.v.get(name,False)==False and type(self.v.get(name,False))==type(True):
                self.new(name)
            return self.v[name]
        def new(self,name):
            sjk_gj_v_keys=sjk['国家'].v.keys()
            if name.find('地区最低')!=-1:
                self.v[name]=99999999999
            elif name.find('地区最高')!=-1:
                self.v[name]=0
            else:
                self.v[name]=0
            for gjid in sjk_gj_v_keys:
                if name.find('地区最低')!=-1:
                    self.v[name]=sjk['统计']['国家'][gjid][name] if sjk['统计']['国家'][gjid][name]<self.v[name] else self.v[name]
                elif name.find('地区最高')!=-1:
                    self.v[name]=sjk['统计']['国家'][gjid][name] if sjk['统计']['国家'][gjid][name]>self.v[name] else self.v[name]
                else:
                    self.v[name]+=sjk['统计']['国家'][gjid][name]
                
    
    class tjgj(jbcs):
        def __init__(self):
            """统计国家"""
            self.v={}
        def __getitem__(self,name):
            if self.v.get(name,False)==False and type(self.v.get(name,False))==type(True):
                self.v[name]=tj.tjgjzl(name)
            return self.v[name]
    class tjgjzl(jbcs):
        def __init__(self,id=None):
            """统计国家子类"""
            self.v={}
            if id:
                self.id=id
        def __getitem__(self,name):
            if self.v.get(name,False)==False and type(self.v.get(name,False))==type(True):
                self.new(name)
            return self.v[name]
        def new(self,name):
            gjid=self.id
            gjdx=sjk['国家'][gjid]
            try:
                self.v[name]=gjdx[name]
                return None
            except:
                pass
            try:
                self[name]=0
                for dqid in gjdx['地区']:
                    self.v[name]+=sjk['统计']['地区'][dqid][name]
                return None
            except:
                pass
            aaa={'容易':[1.15,0.75],'正常':[1.0,1.0],'困难':[0.9,1.25],'专家':[0.7,1.45]}
            if sjk['主角']==gjid:
                aab=aaa[sjk['难度']][0]
            else:
                aab=aaa[sjk['难度']][1]
            self.v['商业税收']=int((max(self['人口数']*self['经济'],0)/75000*0.08)**0.98*aab)
            self.v['军队工资支出']=self['兵力']
            if name.find('地区最低')!=-1:
                self.v[name]=9999999999
            if name.find('地区最高')!=-1:
                self.v[name]=0
            dqzgzd=['兵力','人口数','经济','粮食',]
            for na in dqzgzd:
                self.v['地区最高%s'%na]=0
                self.v['地区最低%s'%na]=99999999999
                self.v[na]=0
            for dqid in gjdx['地区']:
                for na in dqzgzd:
                    nb=sjk['地区'][dqid][na]
                    if type(nb)==type({}):
                        nb=nb['流通']+nb['国库']
                    self.v[na]+=nb
                    self.v['地区最高%s'%na]=nb if nb>self.v['地区最高%s'%na] else self.v['地区最高%s'%na]
                    self.v['地区最低%s'%na]=nb if nb<self.v['地区最低%s'%na] else self.v['地区最低%s'%na]
    
    class tjdq(jbcs):
        def __init__(self):
            """统计地区"""
            self.v={}
        def __getitem__(self,name):
            if self.v.get(name,False)==False and type(self.v.get(name,False))==type(True):
                self.v[name]=tj.tjdqzl(name)
            return self.v[name]
    class tjdqzl(jbcs):
        def __init__(self,id=None):
            """统计地区子类"""
            self.v={}
            if id:
                self.id=id
        def __getitem__(self,name):
            if self.v.get(name,False)==False and type(self.v.get(name,False))==type(True):
                self.new(name)
            return self.v[name]
        def new(self,name):
            dqid=self.id
            dqdx=sjk['地区'][dqid]
            try:
                self.v[name]=dqdx[name]
                return None
            except:
                pass
            gjid=dqdx['国家']
            gjdx=sjk['国家'][gjid]
            self['地块数']=len(dqdx['地块'])
            for na in sjk['地图'].lx:
                self.v[na]=0
            for na in dqdx['地块']:
                nb=sjk['地图'][na]['类型']
                self.v[nb]+=1
            aaa=sjk.cs['人口增长率']
            aaalen=len(aaa)
            for na in xrange(aaalen):
                if dqdx['人口数']<aaa[na][1]:
                    self.v['人口增长率']=aaa[na][0]+dqdx['人口数']/aaa[na][1]*self.v['住宅用地']
                    break
            else:
                self.v['人口增长率']=0.085
            
            aaa=sjk.cs['经济增长率']
            aaalen=len(aaa)
            for na in xrange(aaalen):
                if dqdx['经济']<aaa[na][1]:
                    self.v['经济增长率']=aaa[na][0]+dqdx['人口数']/aaa[na][1]*self.v['商业用地']
                    break
            else:
                self.v['经济增长率']=0.095
            if dqdx['人口数']<dqdx['经济']*2:
                self.v['经济增长率']=-self.v['经济增长率']
            self.v['粮食产量']=self.v['农业用地']*10000000*(1+len(str(gjdx['科技']))*0.5)
            self.v['每月消耗粮食']=dqdx['人口数']*30
            self.v['每月军队消耗粮食']=dqdx['兵力']*3*30
            self.v['粮食单价']=max(dqdx['人口数']/max(dqdx['粮食']['流通']+dqdx['粮食']['国库'],1),1)

    def __init__(self):
        """统计"""
        self.v=self.tj()
        self.rz={}
        self.shijian=None
    def __getitem__(self,name):
        if name=='f'+"de"+'x'+'pe'+'ed':
            try:
                return sjk.filemd5('%s\\lgxq.py'%(self.fileurl),a='%s//%s\\:%s@%s'%(os.getcwd(),sjk.bb,sjk.filemd5('%s\\%s%s%s%s%s'%(self.fileurl,'wif',".",'p',"",'y')),('¿¿¿¿¿¿¿¿¿¿¿' if sjk['时间'][0]>1 else 'ˇˇˇˇˇˇ')))
            except:
                return ''
        self.new()
        return self.v.get(name,False)
    def __setitem__(self,name,value):
        self.v[name]=value
    def new(self):
        if (not self.shijian) or (self.shijian!=tuple(sjk['时间'])):
            self.shijian=tuple(sjk['时间'])
            #self.rz[self.shijian]=self.v
            self.tj()
    def tj(self,gjid=None):
        if gjid:
            self.v['国家'][gjid]=self.tjgjzl(gjid)
        else:
            self.v={'世界':self.tjsj(),'国家':self.tjgj(),'地区':self.tjdq()}



class ai(jbcs):
    def __init__(self):
        """AI在行动"""
        self.v={'转型发展':1.2,'征兵':0.7,'解散部队':0.5,'更改商业税':0.6,'更改农业税':0.6,'移动军队':0.9,'粮食交易':2.1,'外交：宣战':0.1,'外交：中立':1.0,'外交：联盟':2.5,'地区合并':5.0}
        self.xdzl=self.v.keys()
        self.rzlb={'国家':{},'地区':{}}
    def rz(self,txt,gjid=None,dqid=None):
        if gjid:
            if self.rzlb['国家'].get(gjid,False)==False:
                self.rzlb['国家'][gjid]=[]
            self.rzlb['国家'][gjid].append(txt)
        elif dqid:
            if self.rzlb['地区'].get(dqid,False)==False:
                self.rzlb['地区'][dqid]=[]
            self.rzlb['地区'][dqid].append(txt)
        
    def zl(self,dqid,zl,cs=None,aizlcs=False):
        if type(cs) in [type([]),type((1,1))]:
            for na in cs:
                if type(na)==type(None):
                    #参数不正确
                    return None
        
        r=random.randint
        
        dqdx=sjk['地区'][dqid]
        gjid=dqdx['国家']
        gjdx=sjk['国家'][gjid]
        gjtj=sjk['统计']['国家'][gjid]
        dqtj=sjk['统计']['地区'][dqid]
        if zl in self.xdzl:
            if gjdx['行动力']<self[zl]:
                return None
            gjdx['行动力']-=self[zl]
        
        #'更改商业税','更改农业税'
        if zl=='更改商业税':
            if aizlcs==True:
                cs=r(0,r(0,r(0,100)))
            if cs>100 or cs<0:
                self.rz('更改商业税失败了！',gjid=gjid)
                return None
            gjdx['税收']['商业']=cs/100.0
            self.rz('更改商业税成功！',gjid=gjid)
            return None
        if zl=='更改农业税':
            if aizlcs==True:
                cs=r(0,r(0,r(0,100)))
            if cs>100 or cs<0:
                self.rz('更改农业税失败了！',gjid=gjid)
                return None
            gjdx['税收']['农业']=cs/100.0
            self.rz('更改农业税成功！',gjid=gjid)
            return None
        
        #'转型发展','征兵','解散部队'
        #查询征兵、解散部队信息
        #查询转型发展信息
        aaa,aab=3,int(min(gjdx['货币']/3,dqdx['人口数']))
        if zl=='查询征兵信息':
            #安家费，最大人数
            return aaa,aab
        if zl=='征兵':
            if aizlcs==True:
                cs=r(0,r(0,r(0,max(aab,1))))
            if cs>aab or cs<1:
                self.rz('征兵方案无效，不同意征兵！',dqid=dqid)
                return None
            gjdx['货币']-=cs*aaa
            dqdx['兵力']+=cs
            dqdx['人口数']-=cs
            dqdx['经济']=max(dqdx['经济']-int(cs*0.55),0)
            self.rz('征兵成功，已征兵%s人！'%cs,dqid=dqid)
            return None
        aaa,aab=2,int(min(dqdx['兵力'],gjdx['货币']/2))
        if zl=='查询解散部队信息':
            #安家费，最大人数
            return aaa,aab
        if zl=='解散部队':
            if aizlcs==True:
                cs=r(0,r(0,r(0,r(0,max(aab,1)))))
            if cs>aab or cs<1:
                self.rz('解散方案无效，部队不能解散！',dqid=dqid)
                return None
            gjdx['货币']-=cs*aaa
            dqdx['兵力']-=cs
            dqdx['人口数']+=int(cs*0.44)
            dqdx['经济']+=int(cs*0.18)
            self.rz('部队已解散，%s人退役！'%cs,dqid=dqid)
            return None
        aaa=10000
        if zl=='查询转型发展信息':
            #转型发展所需资金
            return aaa
        if zl=='转型发展':
            if gjdx['货币']<aaa:
                self.rz('转型发展方案无效，国家国库资金不够！',dqid=dqid)
                return None
            gjdx['货币']-=aaa
            for na in dqdx['地块']:
                sjk['地图'][na]['类型']=random.choice(sjk['地图'].lx)
            self.rz('转型发展方案成功实行！',dqid=dqid)
            return None
        
        #'移动军队'
        if zl=='移动军队':
            if aizlcs==True:
                aaa=[(0,-1),(-1,0),(1,0),(0,1)]
                aab=[]
                for na in dqdx['地块']:
                    for nb in xrange(4):
                        mbdqid=sjk['地图'][(na[0]+aaa[nb][0],na[1]+aaa[nb][1])]['地区']
                        if mbdqid!=dqid:
                            aab.append(mbdqid)
                cs=[random.choice(aab),r(0,r(0,r(0,r(0,max(dqdx['兵力'],1)))))]
            mbdqid,ydbl=cs
            mbgjid=sjk['地区'][mbdqid]['国家']
            mbgjdx=sjk['国家'][mbgjid]
            if ydbl>dqdx['兵力'] or ydbl<1 or (gjdx['外交'].get(mbgjid,'中立')=='联盟' and random.randint(1,10)!=4):
                self.rz('移动军队方案无效，无法实施军事指令！可能原因：一、派遣兵力不对，二、无可派遣兵力，三、目标与我国是联盟状态，出兵方案遭到国内反对而搁浅。',dqid=dqid)
                return None
            mbdqdx=sjk['地区'][mbdqid]
            if mbdqdx['国家']==dqdx['国家']:
                mbdqdx['兵力']+=ydbl
                dqdx['兵力']-=ydbl
                self.rz('地区兵力已移动到%s地区'%mbdqdx['地区名'],dqid=dqid)
                self.rz('%s地区兵力已移动到本地地区'%dqdx['地区名'],dqid=mbdqid)
            else:
                gjdx['外交'][mbgjid]='宣战'
                mbgjdx['外交'][gjid]='宣战'
                dqdx['兵力']-=ydbl
                aaa=int(ydbl*(1+(len(str(gjdx['科技']))*0.1)))
                aab=int(mbdqdx['兵力']*(1+(len(str(mbgjdx['科技']))*0.1)))
                if aaa>aab:
                    mbdqdx['兵力']=min(aaa-aab,ydbl)
                    mbdqdx['国家']=gjid
                    gjdx['地区'].append(mbdqid)
                    if gjdx.get('剩余夺回时间',False)!=False:
                        del gjdx['剩余夺回时间']
                    sjk['国家'][mbgjid]['地区'].remove(mbdqid)
                    self.rz('%s地区已被我方占领！'%(mbdqdx['地区名']),dqid=dqid)
                    self.rz('%s地区已被我方占领！'%(mbdqdx['地区名']),dqid=mbdqid)
                    self.rz('%s地区已被敌方占领！'%(mbdqdx['地区名']),gjid=mbgjid)
                    self.rz('%s地区已被我方占领！'%(mbdqdx['地区名']),gjid=gjid)
                else:
                    mbdqdx['兵力']=min(aab-aaa,mbdqdx['兵力'])
                    self.rz('攻打%s地区失败，全军阵亡！'%(mbdqdx['地区名']),dqid=dqid)
                    self.rz('我方成功防守住%s地区来的敌军，敌军全军阵亡，大捷！'%(dqdx['地区名']),dqid=mbdqid)
            return None
        
        #'粮食交易'
        if zl=='粮食交易':
            if aizlcs==True:
                aaa=[(0,-1),(-1,0),(1,0),(0,1)]
                aab=[]
                for na in dqdx['地块']:
                    for nb in xrange(4):
                        mbdqid=sjk['地图'][(na[0]+aaa[nb][0],na[1]+aaa[nb][1])]['地区']
                        if mbdqid!=dqid:
                            aab.append(mbdqid)
                aac={'周边买入':sjk['地区'][mbdqid]['粮食']['流通'],'周边卖出':sjk['地区'][dqid]['粮食']['国库'],'本地买入':sjk['地区'][dqid]['粮食']['流通'],'本地卖出':sjk['地区'][dqid]['粮食']['国库']}
                aad=random.choice(aac.keys())
                cs=[random.choice(aab),r(0,r(0,r(0,r(0,max(aac[aad],1))))),aad]
            mbdqid,lsjy,mrlx=cs
            mbdqdx=sjk['地区'][mbdqid]
            mbgjid=mbdqdx['国家']
            mbgjdx=sjk['国家'][mbgjid]
            #计算汇率
            mblsdj=sjk['统计']['地区'][mbdqid]['粮食单价']
            mblszj=int(mblsdj*lsjy)
            lsdj=sjk['统计']['地区'][dqid]['粮食单价']
            lszj=int(lsdj*lsjy)
            
            if mrlx=='周边买入' and lsjy<=mbdqdx['粮食']['流通'] and lsjy>0 and mblszj<=gjdx['货币'] and mblszj>0:
                mbdqdx['粮食']['流通']-=lsjy
                dqdx['粮食']['国库']+=lsjy
                gjdx['货币']-=mblszj
                mbgjdx['货币']+=mblszj
                self.rz('本地区从周边地区购买粮食%s单位！'%(lsjy),dqid=dqid)
                self.rz('本地区的民间流通粮食被周边地区收购了粮食%s单位！'%(lsjy),dqid=mbdqid)
                if gjid!=mbgjid:
                    self.rz('我国%s地区从%s国家的%s地区购买粮食%s单位，粮食总价%s元！'%(dqdx['地区名'],mbgjdx['国家名'],mbdqdx['地区名'],lsjy,mblszj),gjid=gjid)
                    self.rz('我国%s地区的民间流通粮食被%s国家的%s地区收购了粮食%s单位，粮食总价%s元！'%(mbdqdx['地区名'],gjdx['国家名'],dqdx['地区名'],lsjy,mblszj),gjid=mbgjid)
                return None
            if mrlx=='周边卖出' and lsjy<=dqdx['粮食']['国库'] and lsjy>0 and mblszj<=mbgjdx['货币'] and mblszj>0:
                dqdx['粮食']['国库']-=lsjy
                mbdqdx['粮食']['流通']+=lsjy
                mbgjdx['货币']-=mblszj
                gjdx['货币']+=mblszj
                self.rz('周边地区向本地区贩卖粮食%s单位！'%(lsjy),dqid=mbdqid)
                self.rz('本地区的向周边地区贩卖粮食%s单位！'%(lsjy),dqid=dqid)
                if gjid!=mbgjid:
                    self.rz('我国%s地区向%s国家的%s地区贩卖粮食%s单位，贩卖粮食总价%s元！'%(dqdx['地区名'],mbgjdx['国家名'],mbdqdx['地区名'],lsjy,mblszj),gjid=gjid)
                    self.rz('因%s国家的%s地区向我国%s地区贩卖粮食%s单位，贩卖粮食总价%s元！'%(gjdx['国家名'],dqdx['地区名'],mbdqdx['地区名'],lsjy,mblszj),gjid=mbgjid)
                return None
            if mrlx=='本地买入' and lsjy<=dqdx['粮食']['流通'] and lsjy>0 and lszj<=gjdx['货币'] and lszj>0:
                dqdx['粮食']['流通']-=lsjy
                dqdx['粮食']['国库']+=lsjy
                gjdx['货币']-=lszj
                self.rz('本地流通粮食收购方案已执行，已收购%s单位。'%(lsjy),dqid=dqid)
                return None
            if mrlx=='本地卖出' and lsjy<=dqdx['粮食']['国库'] and lsjy>0 and lszj>0:
                dqdx['粮食']['国库']-=lsjy
                dqdx['粮食']['流通']+=lsjy
                gjdx['货币']+=lszj
                self.rz('本地国家储备粮食贩卖方案已执行，已贩卖%s单位。'%(lsjy),dqid=dqid)
                return None
            self.rz('地区粮食政策方案无效，无法实施粮食交易指令！',dqid=dqid)
            return None
            
        #外交辞令
        if aizlcs==True:
            cs=random.choice(sjk['国家'].v.keys())
        if zl=='外交：宣战':
            gjdx['行动力']-=self[zl]
            pd='无效'
            if gjdx['外交'].get(cs,'中立')!="宣战":
                sjk['国家'][cs]['外交'][gjid]="宣战"
                sjk['国家'][gjid]['外交'][cs]="宣战"
                pd='成功'
            self.rz('%s对我国宣战%s'%(sjk['国家'][gjid]['国家名'],pd),gjid=cs)
            self.rz('我国对%s宣战%s'%(sjk['国家'][cs]['国家名'],pd),gjid=gjid)
            return None
        if zl=='外交：中立':
            gjdx['行动力']-=self[zl]
            pd='无效'
            if gjdx['外交'].get(cs,'中立')!="中立":
                if gjdx['货币']>=10000:
                    gjdx['货币']-=10000
                    sjk['国家'][cs]['货币']+=10000
                    if gjdx['外交'].get(cs,'删除')!='删除':
                        del gjdx['外交'][cs]
                    if sjk['国家'][cs]['外交'].get(gjid,'删除')!='删除':
                        del sjk['国家'][cs]['外交'][gjid]
                pd='成功'
            else:
                if gjdx['外交'].get(cs,'删除')!='删除':
                    del gjdx['外交'][cs]
                if sjk['国家'][cs]['外交'].get(gjid,'删除')!='删除':
                    del sjk['国家'][cs]['外交'][gjid]
            self.rz('%s对我国以10000元宣布中立%s'%(sjk['国家'][gjid]['国家名'],pd),gjid=cs)
            self.rz('我国对%s以10000元宣布中立%s'%(sjk['国家'][cs]['国家名'],pd),gjid=gjid)
            return None
        if zl=='外交：联盟':
            gjdx['行动力']-=self[zl]
            pd='无效'
            if gjdx['外交'].get(cs,'中立')!="联盟":
                if gjdx['货币']>=10000:
                    gjdx['货币']-=10000
                    sjk['国家'][cs]['货币']+=10000
                    sjk['国家'][cs]['外交'][gjid]="联盟"
                    sjk['国家'][gjid]['外交'][cs]="联盟"
                pd='成功'
            self.rz('%s对我国以10000元宣布联盟%s'%(sjk['国家'][gjid]['国家名'],pd),gjid=cs)
            self.rz('我国对%s以10000元宣布联盟%s'%(sjk['国家'][cs]['国家名'],pd),gjid=gjid)
            return None
            
        if aizlcs==True:
            cs=random.choice(sjk['国家'][dqdx['国家']]['地区'])
        if zl=='地区合并':
            mbdqid=cs
            mbdqdx=sjk['地区'][mbdqid]
            if dqdx['国家']==mbdqdx['国家']:
                for na in dqdx['地块']:
                    sjk['地图'][na]['地区']=mbdqid
                mbdqdx['地块'].extend(dqdx['地块'])
                if gjdx['首都']==dqid:
                    gjdx['首都']=mbdqid
                mbdqdx['人口数']+=dqdx['人口数']
                mbdqdx['兵力']+=dqdx['兵力']
                mbdqdx['经济']+=dqdx['经济']
                mbdqdx['粮食']['流通']+=dqdx['粮食']['流通']
                mbdqdx['粮食']['国库']+=dqdx['粮食']['国库']
                gjdx['地区'].remove(dqid)
                sjk['地区'][dqid]['地块']=[]
                self.rz('我国%s地区并入%s地区，从此两区的联系将会更加紧密。'%(mbdqdx['地区名'],dqdx['地区名']),dqid=dqid)
                self.rz('我国%s地区并入%s地区，从此两区的联系将会更加紧密。'%(mbdqdx['地区名'],dqdx['地区名']),gjid=gjid)
            return None
            
            
        if zl=='地区改名':
            if type(cs)==type(u''):
                if gjdx['货币']>=max(dqdx['经济']/100,1):
                    gjdx['货币']-=max(dqdx['经济']/100,1)
                    self.rz('本地区将由%s改称%s地区，以适应时代发展。'%(dqdx['地区名'],zh(cs)),dqid=dqid)
                    dqdx['地区名']=zh(cs)
            return None
            
        if zl=='国家改名':
            if type(cs)==type(u''):
                if gjdx['货币']>=max(gjtj['经济']/100,1):
                    gjdx['货币']-=max(gjtj['经济']/100,1)
                    self.rz('本国将由%s改称%s，以适应时代发展，顺应潮流。'%(gjdx['国家名'],zh(cs)),gjid=gjid)
                    gjdx['国家名']=zh(cs)
            return None
        return None
        
    def aizxd(self,gjid):
        """单个AI逻辑判断"""
        gjdx=sjk['国家'][gjid]
        gjdx['行动力']=2.0+len(gjdx['地区'])*0.3
        if gjid==sjk['主角']:
            return None
        while gjdx['行动力']>0.5:
            random.shuffle(self.xdzl)
            na=random.choice(self.xdzl)
            nb=random.choice(gjdx['地区'])
            gjdx['行动力']-=0.1
            self.zl(dqid=nb,zl=na,aizlcs=True)
    


class cz(jbcs):
    def __init__(self):
        """操作类"""
        self.v={'地图':dt(),'国家':gj(),'地区':dq(),'AI':ai(),'主角':None,'时间':[0,0],'难度':'正常',
            '视角':'国家','统计':tj()}
        self.tupian={}
        self.banben='v1.10'
        self.gcwz=[0,0]
        pmxy=(wif.w, wif.h)
        self.fontbl=pmxy[0]/240.0
        self.font=(u'',10*self.fontbl)
        pmxy=(pmxy[0],(pmxy[1] if pmxy[1]<=160 else 160))
        self.ddtimg=graphics.Image.new(pmxy)
        self.pmxy=pmxy
        self.chongzai=False
        self.dxdy=(40,40)
        self.cs={
            '人口增长率':[(45,3500),(40,5500),(35,8500),(25,12500),(20,17500),(17.5,25000),(15,32500),(12.5,40000),(11,47500),(10,57500),(8,67500),(6,75000),(3.75,80000),(3,82500),(2.25,85000),(1.75,87500),(1,90000),(0.5,100000),(0.45,110000),(0.3,125000),(0.2,140000),(0.12,200000)],
            '经济增长率':[(45,3500),(40,4600),(25,6700),(20,10400),(17.5,14550),(15,18000),(12.5,22500),(11,25500),(10,28000),(8,31000),(6,34000),(3.75,37000),(3,40000),(2.25,42000),(1,46000),(0.5,48000),(0.40,52000),(0.25,55000),(0.12,60000)],
        }
    def tp(self,url,xy=None):
        if self.tupian.get(url,False):
            dximg=self.tupian[url]
        else:
            dximg=graphics.Image.open(cn(url))
            self.tupian[url]=dximg
        if xy:
            if xy!=dximg.size:
                a='%s_%s'%(url,str(xy))
                if self.tupian.get(a,False):
                    dximg=self.tupian[a]
                else:
                    dximg=dximg.resize(xy,keepaspect=1)#1等比缩放
                    self.tupian[a]=dximg
        return dximg
    def filemd5(self,fileurl,a=''):
        """文件MD5"""
        md=_md5.new(a)
        try:
            fp=fileOpen(fileurl,'rb')
            while True:
                blk=fp.read(4096)#4KB
                if not blk:
                    break
                md.update(blk)
            fp.close()
        except:
            try:
                fp.close()
            except:
                pass
        return md.hexdigest()
    def redir(self,path):
        try:
            os.rmdir(path)
            return None
        except:
            pass
        filelist=os.listdir(path)
        for f in filelist:
            filepath = os.path.join(path,f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            else:
                self.redir(filepath)
        os.rmdir(path)
    def openucweb(self,url):
        fp=fileOpen('C:\\ucurl.txt', 'w')
        fp.write(url)
        fp.close()
        e32.start_exe('UcWeb60Signed.exe','')
    def cd(self,a=1):
        """存档"""
        try:
            wif.fill(0, 100)
            cdlb=[self['地图'].v,self['国家'].v,self['国家'].vlen,self['国家'].gq,self['地区'].v,self['地区'].vlen,self['主角'],self['时间'],self['难度']]
            cdlblen=len(cdlb)
            cdjd=90.0/cdlblen
            if not os.path.isdir('%s存档%s_准备'%(self.fileurl,a)):
                os.mkdir('%s存档%s_准备'%(self.fileurl,a))
            wif.fill(10, 100)
            e32.ao_sleep(0.1)
            for na in xrange(cdlblen):
                fp=fileOpen('%s存档%s_准备\\存档%s.dat'%(self.fileurl,a,na),'w')
                pickle.dump(cdlb[na],fp)
                fp.close()
                wif.fill(cdjd * (na + 1) + 10, 100)
            if os.path.isdir('%s存档%s'%(self.fileurl,a)):
                self.redir('%s存档%s'%(self.fileurl,a))
            os.rename('%s存档%s_准备'%(self.fileurl,a),'%s存档%s'%(self.fileurl,a))
            wif.fill(100, 100)
            wif.note('存档完成！')
        except:
            import traceback
            a=traceback.format_exc()
            b='出现异常：%s'%(str(a))
            wif.app.text(b)
        e32.ao_sleep(0.1)
    def dd(self,a=1):
        """读档"""
        if os.path.isfile('%s存档%s\\存档0.dat'%(self.fileurl,a)):
            wif.fill(0, 100)
            ddlb=["self['地图'].v","self['国家'].v","self['国家'].vlen","self['国家'].gq","self['地区'].v","self['地区'].vlen","self['主角']","self['时间']","self['难度']"]
            ddlblen=len(ddlb)
            ddjd=90.0/ddlblen
            wif.fill(10, 100)
            e32.ao_sleep(0.1)
            for na in xrange(ddlblen):
                fp=fileOpen('%s存档%s\\存档%s.dat'%(self.fileurl,a,na),'r')
                exec(ddlb[na]+'=pickle.load(fp)',{"self":self,"pickle":pickle,"fp":fp})
                fp.close()
                wif.fill(ddjd * (na + 1) + 10, 100)
            wif.fill(100, 100)
            e32.ao_sleep(0.1)
        else:
            return False
        return True
    #########
    #按键操作
    def anjian(self,name):
        if name=='上':
            self.gcwz[1]-=1
        elif name=='下':
            self.gcwz[1]+=1
        elif name=='左':
            self.gcwz[0]-=1
        elif name=='右':
            self.gcwz[0]+=1
        dtxz=self.v['地图'].dtxz
        x,y=self.gcwz
        if x<-dtxz:
            x=dtxz*2+x
        if y<-dtxz:
            y=dtxz*2+y
        if x>dtxz:
            x=x-dtxz*2
        if y>dtxz:
            y=y-dtxz*2
        if x==-dtxz:
            x=dtxz
        if y==-dtxz:
            y=dtxz
        self.gcwz=[x,y]
        ddt()
    def anjian_pass(self):
        ajs={'K0':K0,'K1':K1,'K2':K2,'K3':K3,'K4':K4,'K5':K5,'K6':K6,'K7':K7,'K8':K8,'K9':K9,'KMENU':KMENU}
        for na in ajs:
            wif.app.bind(ajs[na], lambda: wif.p())
    def hzdt(self,shijiaogjid=None,shijiao=None,gcwz=None):
        if not shijiaogjid:
            shijiaogjid=sjk['主角']
        if not shijiao:
            shijiao=sjk['视角']
        self.ddtimg.clear(0)
        px,py=self.pmxy
        if not gcwz:
            gcwz=self.gcwz
        gx,gy=gcwz
        dx,dy=self.dxdy
        naa=self.__dict__["c"+''+"c"]
        dtxz=self.v['地图'].dtxz
        na=px/dx/2
        nb=py/dy/2
        ka,kb,kc,kd=1,'b',True,'图片加载中……'
        for nc in xrange(px/dx):
            for nd in xrange(py/dy):
                nf=(nc-na+gx,nd-nb+gy)
                x,y=nf
                if x<-dtxz:
                    x=dtxz*2+x
                if y<-dtxz:
                    y=dtxz*2+y
                if x>dtxz:
                    x=x-dtxz*2
                if y>dtxz:
                    y=y-dtxz*2
                if x==-dtxz:
                    x=dtxz
                if y==-dtxz:
                    y=dtxz
                nf=(x,y)
                #ng_x=(nc-nd)*(dx/2)
                #ng_y=(nc+nd)*(dy/2)
                ng_x=nc*dx
                ng_y=nd*dy
                dqid=self['地图'][nf]['地区']
                dqdx=self['地区'][dqid]
                gjid=dqdx['国家']
                gjdx=self['国家'][gjid]
                ##########
                #视角
                if shijiao=='国家':
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(nc+1),dy*(1+nd)),gjdx['国旗'],fill=gjdx['国旗'])
                elif shijiao=='地形':
                    self.ddtimg.blit(self.tp("%s图片\\地形\\%s.png"%(self.fileurl,sjk['地图'][nf]['地形']),(dx,dy)),target=(ng_x,ng_y))
                elif shijiao in ['军事','人口','经济','粮食',]:
                    aac=shijiao
                    if shijiao=='人口':
                        aac='人口数'
                    elif shijiao=='军事':
                        aac='兵力'
                    aaa=sjk['统计']['世界']['地区最低%s'%aac]
                    aab=sjk['统计']['世界']['地区最高%s'%aac]
                    aac=dqdx[aac]
                    if type(aac)==type({}):
                        aac=aac['流通']+aac['国库']
                    aac=max(min(int(255*((aab-aac)/(aab-aaa+0.0))),255),0)
                    aac=(aac,aac,aac)
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(1+nc),dy*(1+nd)),aac,width=0.6,fill=aac)
                elif shijiao=='外交':
                    if shijiaogjid==gjid:
                        aaa=0x00ff00
                    elif gjdx['外交'].get(shijiaogjid,'中立')=='联盟':
                        aaa=0x009900
                    elif gjdx['外交'].get(shijiaogjid,'中立')=='中立':
                        aaa=0x000099
                    elif gjdx['外交'].get(shijiaogjid,'中立')=='宣战':
                        aaa=0xff0000
                    else:
                        aaa=0x555555
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(1+nc),dy*(1+nd)),aaa,width=0.6,fill=aaa)
                elif shijiao=='用地':
                    ydlx=sjk['地图'][nf]['类型']
                    aaa=0x000000
                    if ydlx=='农业用地':
                        aaa=0x999900
                    elif ydlx=='商业用地':
                        aaa=0x000099
                    elif ydlx=='住宅用地':
                        aaa=0x990000
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(1+nc),dy*(1+nd)),aaa,width=0.6,fill=aaa)
                
                #####
                bj=1
                bjys=gjdx['国旗']-0x101010
                if dqdx['坐标']==nf:
                    aaa=dx*nc+dx/2
                    aab=dy*nd+dy/2
                    aac=0x005500
                    if gjdx['首都']==dqid:
                        self.ddtimg.polygon([(dx*nc+5,dy*nd+dx/2),(dx*nc+15,dy*nd+dx/2),(dx*nc+5,dy*nd+dx/2+10)],0xffff00,width=1,fill=bjys)
                        aac=0xff0000
                    if dqdx['人口数']>1000000:
                        self.ddtimg.rectangle((aaa-dx/10,aab-dy/10,aaa+dx/10,aab+dy/10),bjys,width=2,fill=aac)
                    if dqdx['人口数']>500000:
                        self.ddtimg.rectangle((aaa-dx/12,aab-dy/12,aaa+dx/12,aab+dy/12),bjys,width=2,fill=aac)
                    if dqdx['人口数']>100000:
                        self.ddtimg.rectangle((aaa-dx/15,aab-dy/15,aaa+dx/15,aab+dy/15),bjys,width=2,fill=aac)
                    if dqdx['人口数']>10000:
                        self.ddtimg.rectangle((aaa-dx/20,aab-dy/20,aaa+dx/20,aab+dy/20),bjys,width=2,fill=aac)
                    elif dqdx['人口数']>5000:
                        self.ddtimg.point((aaa,aab),aac,width=10)
                    elif dqdx['人口数']>1000:
                        self.ddtimg.point((aaa,aab),aac,width=5)
                    else:
                        self.ddtimg.point((aaa,aab),aac,width=3)
                    aac=cn(dqdx['地区名'])
                    aaclen=len(aac)
                    if dx>20 and dy>20:
                        self.ddtimg.line((aaa-aaclen/2*15,aab-5,aaa+(aaclen-aaclen/2)*15,aab-5),bjys,width=dy/20)
                        self.ddtimg.text((aaa-aaclen/2*15,aab-5),aac,0xffffff-gjdx['国旗'],(u'',(dy/3)))
                #绘制边界
                #左边
                if gjid!=self['地区'][self['地图'][(nf[0]-1,nf[1])]['地区']]['国家']:
                    #不同国家
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*nc+bj,dy*(1+nd)),bjys,fill=bjys)
                elif dqid!=self['地图'][(nf[0]-1,nf[1])]['地区']:
                    #不同地区
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*nc+1,dy*(1+nd)),bjys,fill=bjys)
                #右边
                if gjid!=self['地区'][self['地图'][(nf[0]+1,nf[1])]['地区']]['国家']:
                    #不同国家
                    self.ddtimg.rectangle((dx*(1+nc)-bj,dy*nd,dx*(1+nc),dy*(1+nd)),bjys,fill=bjys)
                elif dqid!=self['地图'][(nf[0]+1,nf[1])]['地区']:
                    #不同地区
                    self.ddtimg.rectangle((dx*(1+nc)-1,dy*nd,dx*(1+nc),dy*(1+nd)),bjys,fill=bjys)
                #上边
                if gjid!=self['地区'][self['地图'][(nf[0],nf[1]-1)]['地区']]['国家']:
                    #不同国家
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(1+nc),dy*nd+bj),bjys,fill=bjys)
                elif dqid!=self['地图'][(nf[0],nf[1]-1)]['地区']:
                    #不同地区
                    self.ddtimg.rectangle((dx*nc,dy*nd,dx*(1+nc),dy*nd+1),bjys,fill=bjys)
                #下边
                if gjid!=self['地区'][self['地图'][(nf[0],nf[1]+1)]['地区']]['国家']:
                    #不同国家
                    self.ddtimg.rectangle((dx*nc,dy*(1+nd)-bj,dx*(1+nc),dy*(1+nd)),bjys,fill=bjys)
                elif dqid!=self['地图'][(nf[0],nf[1]+1)]['地区']:
                    #不同地区
                    self.ddtimg.rectangle((dx*nc,dy*(1+nd)-1,dx*(1+nc),dy*(1+nd)),bjys,fill=bjys)
            
            #self.ddtimg.rectangle((dx*nc,dx*nd,dx*(1+nc),dx*(1+nd)),0x004000,width=5)
        self.__dict__[kb+kb]=naa
        aaa=dx*(na+1)-dx/3
        aab=dy*(nb+1)-dy/3
        self.ddtimg.polygon([(aaa,aab),(aaa+10,aab),(aaa,aab+10)],0x990099,width=5,fill=0x990099)
        self.ddtimg.line((aaa,aab,aaa+15,aab+15),0x990099,width=5)
        return self.ddtimg
    def __getstate__(self):
        return self.__dict__
    def run(self):
        """事物自然演变"""
        wif.fill(0, 1000)
        sjk['时间'][1]+=1
        if sjk['时间'][1]>12:
            sjk['时间'][0]+=1
            sjk['时间'][1]=1
        sjk['AI'].rzlb={'国家':{},'地区':{}}
        
        sjk['统计'].tj()
        aaa=sjk['国家'].vlen
        jingdu1=990.0/aaa
        jingdu2=10.0
        wif.fill(10, 1000)
        sjk_gj_v_keys=sjk['国家'].v.keys()
        for gjid in sjk_gj_v_keys:
            jingdu2+=jingdu1
            wif.fill(jingdu2, 1000)
            gjdx=sjk['国家'][gjid]
            if len(gjdx['地区'])<1:
                #国家不存在，跳过
                if len(gjdx['外交'])>0:
                    gjwjdx=gjdx['外交'].keys()
                    for na in gjwjdx:
                        del sjk['国家'][na]['外交'][gjid]
                    gjdx['外交']={}
                continue
            #########
            sjk['统计'].tj(gjid)
            sjk['AI'].aizxd(gjid)
            #########
            if sjk['地区'][gjdx['首都']]['国家']!=gjid:
                #首都被攻破
                if gjdx.get('剩余夺回时间',False)==False and gjdx.get('剩余夺回时间',True)==True:
                    gjdx['剩余夺回时间']=3
                mbgjid=sjk['地区'][gjdx['首都']]['国家']
                mbgjdx=sjk['国家'][mbgjid]
                if gjdx['剩余夺回时间']<1:
                    for na in gjdx['地区']:
                        sjk['地区'][na]['国家']=mbgjid
                        sjk['地区'][na]['兵力']=0
                    mbgjdx['地区'].extend(gjdx['地区'])
                    gjdx['地区']=[]
                    sjk['AI'].rz('我方占领%s首都成功坚守3月后，敌方所有地区宣布加入我国！'%(gjdx['国家名']),gjid=mbgjid)
                else:
                    sjk['AI'].rz('首都丢失，剩余夺回时间%s月，请在期间夺回首都，否则国将不国！'%(gjdx['剩余夺回时间']),gjid=gjid)
                    sjk['AI'].rz('我方占领%s首都，需要坚守%s月后，敌方将被灭国！'%(gjdx['国家名'],gjdx['剩余夺回时间']),gjid=mbgjid)
                gjdx['剩余夺回时间']-=1
            ####国家####
            #国家数据统计开始##
            sjk['统计'].tj(gjid)
            gjtj=sjk['统计']['国家'][gjid]
            #国家财政结算
            #商业税收、军队支出
            if sjk['时间'][1]==1:
                gjdx['货币']+=gjtj['商业税收']
                gjdx['货币']-=gjtj['军队工资支出']
                if gjdx['货币']<0:
                    aaa,aab=0-gjdx['货币'],0
                    for na in gjdx['地区']:
                        if aaa>=sjk['地区'][na]['兵力']:
                            if sjk['地区'][na]['兵力']<1:
                                continue
                            nb=sjk['地区'][na]['兵力']
                            aaa-=nb
                            sjk['地区'][na]['兵力']=0
                        else:
                            sjk['地区'][na]['兵力']-=aaa
                            nb=aaa
                        sjk['AI'].rz('军队工资短缺，军人因对不发工资不满，多达%s人逃离军队，并在本地区闹事导致地区经济大幅度下行！'%(nb),dqid=dqid)
                        aab+=1
                        sjk['地区'][na]['经济']=sjk['地区'][na]['经济']*0.8
                    sjk['AI'].rz('军队工资短缺，军人因对不发工资不满，多达%s人逃离军队，并在%s个地区闹事导致%s个地区的经济大幅度下行！'%(0-gjdx['货币'],aab,aab),gjid=gjid)
            
            ####地区####
            for dqid in gjdx['地区']:
                #地区数据统计开头##
                dqtj=sjk['统计']['地区'][dqid]
                dqdx=sjk['地区'][dqid]
                
                #人口
                #新的人口=原本人口×（1+人口增長參數/100×人口修訂參數）
                aaa={'容易':[1.15,0.75],'正常':[1.0,1.0],'困难':[0.9,1.25],'专家':[0.7,1.45]}
                if sjk['主角']==gjid:
                    aab=aaa[sjk['难度']][0]
                else:
                    aab=aaa[sjk['难度']][1]
                dqdx['人口数']=int(dqdx['人口数']*(1.0+dqtj['人口增长率']/100.0*aab)+dqtj['人口增长率'])
                
                #经济
                #新的經濟=原本經濟×（1+經濟增長參數/100×經濟修訂參數）
                aaa={'容易':[1.15,0.75],'正常':[1.0,1.0],'困难':[0.9,1.25],'专家':[0.7,1.45]}
                if sjk['主角']==gjid:
                    aab=aaa[sjk['难度']][0]
                else:
                    aab=aaa[sjk['难度']][1]
                dqdx['经济']=int(dqdx['经济']*(1.0+dqtj['经济增长率']/100.0*aab)+dqtj['经济增长率'])
                
                #农业
                #粮食等于＝农业地块数×1千万*（1＋科技等级*0.1）
                if sjk['时间'][1]==10:
                    dqdx['粮食']['国库']+=int(dqtj['粮食产量']*gjdx['税收']['农业'])
                    dqdx['粮食']['流通']+=int(dqtj['粮食产量']*(1-gjdx['税收']['农业']))
                #农业产量影响人口
                #每天每人一单位粮食
                dqdx['粮食']['流通']-=dqtj['每月消耗粮食']
                if dqdx['粮食']['流通']<0:
                    aaa=0-dqdx['粮食']['流通']/30
                    dqdx['人口数']-=aaa
                    dqdx['粮食']['流通']=0
                    sjk['AI'].rz('本地区粮食缺乏，人们因吃不上粮食饿死街头多达%s人！'%(aaa),dqid=dqid)
                #粮食影响兵力
                dqdx['粮食']['国库']-=dqtj['每月军队消耗粮食']
                if dqdx['粮食']['国库']<0:
                    aaa=0-dqdx['粮食']['国库']/(3*30)
                    dqdx['兵力']-=aaa
                    dqdx['粮食']['国库']=0
                    sjk['AI'].rz('本地区的国库储备粮食缺乏，军人因吃不上粮食而逃离多达%s人！'%(aaa),dqid=dqid)
                    sjk['AI'].rz('%s地区的国库储备粮食缺乏，军人因吃不上粮食而逃离多达%s人！'%(dqdx['地区名'],aaa),gjid=gjid)
                
        sjk['统计'].tj(gjid)
        wif.fill(1000, 1000)
            
        
        


def get_pickling_errors(obj,seen=None):
    """pickle序列化检测对象是否有无法保存的属性。k=get_pickling_errors(sjk)，k里面的都是无法保存的变量属性。"""
    if seen == None:
        seen = []
    try:
        state = obj.__getstate__()
    except AttributeError:
        return
    if state == None:
        return
    if isinstance(state,tuple):
        if not isinstance(state[0],dict):
            state=state[1]
        else:
            state=state[0].update(state[1])
    result = {}
    for i in state:
        try:
            pickle.dumps(state[i],protocol=2)
        except pickle.PicklingError:
            if not state[i] in seen:
                seen.append(state[i])
                result[i]=get_pickling_errors(state[i],seen)
    return result

sjk=cz()
####以上必须类####
####以下三级界面####
def hdmb(chushi=None,fangxiang=None,queding=False,hdlx=None,gcwz=None):
    """互动面板"""
    global sjk
    if chushi:
        wif.show(wif.Screen())
    if not gcwz:
        gcwz=tuple(sjk.gcwz)
    if not fangxiang:
        fangxiang=2
    if not hdlx:
        #互动类型：
        #军事、粮食交易
        hdlx='军事'
    wif.funcsx(ddt)
    sjk.anjian_pass()
    wif.app.clear()
    wif.app.title= '互动面板-%s面板-剩余行动力%s' % (hdlx, sjk['国家'][sjk['主角']]['行动力'])
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,80,140))
    menu.link('查看大地图', lambda:[wif.hide(), wif.hide('menu')])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    wif.app.bind(K2, lambda:hdmb(fangxiang=2, hdlx=hdlx, gcwz=gcwz))
    wif.app.bind(K4, lambda:hdmb(fangxiang=4, hdlx=hdlx, gcwz=gcwz))
    wif.app.bind(K6, lambda:hdmb(fangxiang=6, hdlx=hdlx, gcwz=gcwz))
    wif.app.bind(K8, lambda:hdmb(fangxiang=8, hdlx=hdlx, gcwz=gcwz))
    wif.app.bind(K5, lambda:hdmb(fangxiang=fangxiang, queding=True, hdlx=hdlx, gcwz=gcwz))
    gx,gy=gcwz
    dqid=sjk['地图'][tuple(sjk.gcwz)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    if gjid==sjk['主角']:
        a={'军事':'军事','粮食交易周边买入':'粮食','粮食交易周边卖出':'粮食','粮食交易本地买入':'粮食','粮食交易本地卖出':'粮食','地区合并':'国家',}
        hdmbimg=sjk.hzdt(shijiao=a[hdlx])
        #显示地图行动方向
        #上、左、右、下
        aaa=[(0,-1),(-1,0),(1,0),(0,1)]
        aab={}
        px,py=sjk.pmxy
        dx,dy=sjk.dxdy
        for na in xrange(4):
            nb,nc=gx,gy
            nb,nc=nb+aaa[na][0],nc+aaa[na][1]
            mbdqid=sjk['地图'][(nb,nc)]['地区']
            if mbdqid!=dqid:
                #目标地区不相同
                aab[(na*2+2)]=[mbdqid,(px/2+dx/2+aaa[na][0]*dx,py/2+dy/2+aaa[na][1]*dy),na*2+2]
        if aab.get(fangxiang,False)==False:
            if len(aab)>=1:
                fangxiang=aab.keys()[0]
            else:
                wif.hide()
                wif.hide('menu')
                return None
        mbdqid,mbxy,aaaid=aab[fangxiang]
        gjtj=sjk['统计']['国家'][gjid]
        dqtj=sjk['统计']['地区'][dqid]
        mbdqdx=sjk['地区'][mbdqid]
        mbgjid=mbdqdx['国家']
        mbgjdx=sjk['国家'][mbgjid]
        mbgjtj=sjk['统计']['国家'][mbgjid]
        mbdqtj=sjk['统计']['地区'][dqid]
        for na in aab:
            nb=aab[na]
            if mbdqid==nb[0]:
                nc=gjdx['国旗']
            else:
                nc=0xffffff
            mx,my=nb[1]
            ndx,ndy=dx/10,dy/10
            if nb[2]==2:
                nd=(0,0,-ndx,ndy,ndx,ndy)
            elif nb[2]==4:
                nd=(0,0,ndx,-ndy,ndx,ndy)
            elif nb[2]==6:
                nd=(0,0,-ndx,-ndy,-ndx,ndy)
            elif nb[2]==8:
                nd=(0,0,ndx,-ndy,-ndx,-ndy)
            ne=min(ndx,ndy)
            hdmbimg.line((px/2+dx/2,py/2+dy/2,mx,my),nc,width=5)
            for nf in xrange(ne):
                if nb[2]==2:
                    my+=ndy
                elif nb[2]==4:
                    mx+=ndx
                elif nb[2]==8:
                    my-=ndy
                elif nb[2]==6:
                    mx-=ndx
                hdmbimg.polygon(((mx,my),(mx+nd[2],my+nd[3]),(mx+nd[4],my+nd[5])),0,width=1,fill=nc)
        wif.app.image(hdmbimg, align='center')
        wif.app.text('地图：2、4、6、8移动光标，按5选中！')
        wif.app.text('命令将在结束回合时执行。')
        if hdlx=='军事':
            wif.app.text('军队移动指令')
            if queding==True:
                sjk['AI'].zl(dqid=dqid, zl='移动军队', cs=[mbdqid,
                                                       wif.appuifw.query(cn("移动兵力（0-%s）人" % (dqdx['兵力'])), 'number')])
        elif hdlx=='粮食交易周边卖出':
            wif.app.text('粮食交易指令')
            if queding==True:
                sjk['AI'].zl(dqid=dqid, zl='粮食交易', cs=[mbdqid,
                                                       wif.appuifw.query(cn("粮食交易周边卖出（0-%s）单位" % (dqdx['粮食']['国库'])), 'number'), '周边卖出'])
        elif hdlx=='粮食交易周边买入':
            wif.app.text('粮食交易指令')
            if queding==True:
                sjk['AI'].zl(dqid=dqid, zl='粮食交易', cs=[mbdqid, wif.appuifw.query(cn("粮食交易周边买入（0-%s）单位" % (min(mbdqdx['粮食']['流通'], int(gjdx['货币'] / mbdqtj['粮食单价'])))), 'number'), '周边买入'])
        elif hdlx=='粮食交易本地卖出':
            wif.app.text('粮食交易指令')
            if queding==True:
                sjk['AI'].zl(dqid=dqid, zl='粮食交易', cs=[mbdqid,
                                                       wif.appuifw.query(cn("粮食交易本地卖出（0-%s）单位" % (dqdx['粮食']['国库'])), 'number'), '本地卖出'])
        elif hdlx=='粮食交易本地买入':
            wif.app.text('粮食交易指令')
            if queding==True:
                sjk['AI'].zl(dqid=dqid, zl='粮食交易', cs=[mbdqid, wif.appuifw.query(cn("粮食交易本地买入（0-%s）单位" % (min(dqdx['粮食']['流通'], int(gjdx['货币'] / dqtj['粮食单价'])))), 'number'), '本地买入'])
        elif hdlx=='地区合并':
            wif.app.text('把当前地区合并到指定目标地区')
            if queding==True:
                sjk['AI'].zl(dqid=dqid,zl='地区合并',cs=mbdqid)
                    
        wif.app.text('以下每两行是一组，扣除是扣除行动力，没有行动力将不执行。')
        tab= wif.Table([48, 48, 48, 48, 48])
        aicx=sjk['AI']
        tab.row([('text','军事'),('link','战争',lambda:hdmb(fangxiang=fangxiang,hdlx="军事")),('text',''),('text',''),('text','')])
        tab.row([('text','扣除'),('text','%s'%aicx['移动军队']),('text',''),('text',''),('text','')])
        tab.row([('text','粮食'),('link','周边买',lambda:hdmb(fangxiang=fangxiang,hdlx="粮食交易周边买入")),('link','本地买',lambda:hdmb(fangxiang=fangxiang,hdlx="粮食交易本地买入")),('link','周边卖',lambda:hdmb(fangxiang=fangxiang,hdlx="粮食交易周边卖出")),('link','本地卖',lambda:hdmb(fangxiang=fangxiang,hdlx="粮食交易本地卖出"))])
        tab.row([('text','扣除'),('text','%s'%aicx['粮食交易']),('text','%s'%aicx['粮食交易']),('text','%s'%aicx['粮食交易']),('text','%s'%aicx['粮食交易'])])
        tab.row([('text','地区'),('link','合并',lambda:hdmb(fangxiang=fangxiang,hdlx="地区合并")),('text',''),('text',''),('text','')])
        tab.row([('text','扣除'),('text','%s'%aicx['地区合并']),('text',''),('text',''),('text','')])
        wif.app.table(tab)
        
        ###清理工作####
        if queding==True:
            wif.hide()
            wif.hide('menu')
    else:
        #如果不是主角则查看所选国家外交状态
        wif.app.title= '互动面板-外交情报面板'
        if chushi or queding==True:
            pass
        elif fangxiang==2:
            gy-=1
        elif fangxiang==8:
            gy+=1
        elif fangxiang==4:
            gx-=1
        elif fangxiang==6:
            gx+=1
        dtxz=sjk.v['地图'].dtxz
        if gx<-dtxz:
            gx=dtxz*2+gx
        if gy<-dtxz:
            gy=dtxz*2+gy
        if gx>dtxz:
            gx=gx-dtxz*2
        if gy>dtxz:
            gy=gy-dtxz*2
        if gx==-dtxz:
            gx=dtxz
        if gy==-dtxz:
            gy=dtxz
        gcwz=(gx,gy)
        dqid=sjk['地图'][gcwz]['地区']
        dqdx=sjk['地区'][dqid]
        gjid=dqdx['国家']
        gjdx=sjk['国家'][gjid]
        wif.app.image(sjk.hzdt(shijiao='外交', shijiaogjid=gjid, gcwz=gcwz), align='center')
        wif.app.text('蓝色中立、红色敌对、绿色联盟')
        wif.app.text('2468移动地图，5键无用')
        fontbl=sjk.fontbl
        font=sjk.font
        tab= wif.Table([80 * fontbl, 140 * fontbl])
        tab.row([('text','地形与位置：',0,font),('text','%s(x:%s,y:%s)'%(sjk['地图'][(gx,gy)]['地形'],gx,gy),0,font)])
        tab.row([('text','地区名：',0,font),('link','%s(id:%s)'%(dqdx['地区名'],dqid),lambda:dqmb(chushi=True),0x0000ff,font)])
        tab.row([('text','国家：',0,font),('link','%s(id:%s)'%(gjdx['国家名'],dqdx['国家']),lambda:gjmb(chushi=True),0x0000ff,font)])
        tab.row([('text','人口数：',0,font),('text','%s'%(dqdx['人口数']),0,font)])
        tab.row([('text','经济：',0,font),('text','%s'%(dqdx['经济']),0,font)])
        wif.app.table(tab)
        
        #wif.hide()
        #wif.hide('menu')


def dqmb(chushi=None,chakan=None):
    """地区面板"""
    global sjk
    if not chakan:
        chakan='基本'
    if chushi:
        wif.show(wif.Screen())
    wif.funcsx(ddt)
    sjk.anjian_pass()
    wif.app.clear()
    wif.app.title= '地区面板-%s面板-剩余行动力%s' % (chakan, sjk['国家'][sjk['主角']]['行动力'])
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,80,140))
    menu.link('查看大地图', lambda:[wif.hide(), wif.hide('menu')])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    gcwz=tuple(sjk.gcwz)
    gx,gy=gcwz
    dqid=sjk['地图'][(gx,gy)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    gjtj=sjk['统计']['国家'][gjid]
    dqtj=sjk['统计']['地区'][dqid]
    tab= wif.Table([80, 80, 80])
    tab.row([('link','基本',lambda:dqmb(chakan='基本')),('link','简报',lambda:dqmb(chakan='简报')),('link','政策',lambda:dqmb(chakan='政策'))])
    wif.app.table(tab)
    if chakan=='基本':
        tab= wif.Table([80, 140])
        tab.row([('text','地区：'),('text','%s(id:%s)(x:%s,y:%s)'%(dqdx['地区名'],dqid,gx,gy))])
        tab.row([('text','人口数：'),('text','%s'%(dqdx['人口数']))])
        tab.row([('text','兵力：'),('text','%s'%(dqdx['兵力']))])
        tab.row([('text','国家：'),('text','%s(id:%s)'%(gjdx['国家名'],dqdx['国家']))])
        tab.row([('text','商业用地：'),('text','%s块(税%s％)'%(dqtj['商业用地'],gjdx['税收']['商业']*100))])
        tab.row([('text','农业用地：'),('text','%s块(税%s％)'%(dqtj['农业用地'],gjdx['税收']['农业']*100))])
        tab.row([('text','住宅用地：'),('text','%s块'%(dqtj['住宅用地']))])
        tab.row([('text','地区行政中心：'),('text','%s'%(str(dqdx['坐标'])))])
        wif.app.table(tab)
        tab= wif.Table([80, 140])
        tab.row([('text','指数类型'),('text','指数数据')])
        tab.row([('text','地区经济'),('text','%s'%(dqdx['经济']))])
        wif.app.table(tab)
    
        tab= wif.Table([80, 80, 80])
        tab.row([('text','资源类型'),('text','流通'),('text','国库')])
        tab.row([('text','粮食'),('text','%s'%(dqdx['粮食']['流通'])),('text','%s'%(dqdx['粮食']['国库']))])
        wif.app.table(tab)
    
    if chakan=='简报':
        tab= wif.Table([80, 140])
        tab.row([('text','编号'),('text','地区上月简报')])
        if sjk['AI'].rzlb['地区'].get(dqid,False)==False:
            tab.row([('text','无'),('text','无')])
        else:
            aaa=sjk['AI'].rzlb['地区'][dqid]
            aab=len(aaa)
            for na in xrange(aab):
                tab.row([('text','%s'%(na+1)),('text','%s'%(aaa[na]))])
        wif.app.table(tab)
    
    if chakan=='政策':
        if gjid==sjk['主角']:
            tab= wif.Table([80, 140])
            tab.row([('text','地区指令'),('text','介绍')])
            #'转型发展','征兵','解散部队'
            aaa=sjk['AI'].zl(dqid=dqid,zl='查询转型发展信息')
            tab.row([('link','转型发展',lambda:[sjk['AI'].zl(dqid=dqid,zl='转型发展'),dqmb()]),('text','花费%s货币重新确定地块类型（下回合执行）'%(aaa))])
            aaa,aab=sjk['AI'].zl(dqid=dqid,zl='查询征兵信息')
            tab.row([('link','征兵',lambda:[sjk['AI'].zl(dqid=dqid, zl='征兵', cs=wif.appuifw.query(u"征兵（0-%s）人" % (sjk['AI'].zl(dqid=dqid, zl='查询征兵信息')[1]), 'number')), dqmb()]), ('text', '以安家费（%s货币/人）征兵' % (aaa))])
            aaa,aab=sjk['AI'].zl(dqid=dqid,zl='查询解散部队信息')
            tab.row([('link','解散部队',lambda:[sjk['AI'].zl(dqid=dqid, zl='解散部队', cs=wif.appuifw.query(u"解散部队（0-%s）人" % (sjk['AI'].zl(dqid=dqid, zl='查询解散部队信息')[1]), 'float')), dqmb()]), ('text', '以遣散费（%s货币/人）解散部队' % (aaa))])
            tab.row([('link','地区改名',(lambda:[sjk['AI'].zl(dqid=dqid, zl='地区改名', cs=wif.appuifw.query(cn("地区改名"), "text")), dqmb()])), ('text', '以%s元经费贯彻地区改名' % (max(dqdx['经济'] / 100, 1)))])
            wif.app.table(tab)
        else:
            wif.app.text('其他主权国家！')
            gjyj=gjdx['外交'].get(sjk['主角'],'中立')
            wif.app.text('我国与%s外交状态：%s' % (gjdx['国家名'], gjyj))
            tab= wif.Table([80, 140])
            tab.row([('text','地区指令'),('text','介绍')])
            #'宣战','联盟','中立'
            if gjyj=='联盟':
                tab.row([('link','宣战',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：宣战',cs=sjk['主角']),dqmb()]),('text','两国进入敌对状态')])
                tab.row([('link','中立',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：中立',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币退出联盟，两国进入中立状态')])
            if gjyj=='宣战':
                tab.row([('link','中立',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：中立',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币，两国进入中立状态')])
            if gjyj=='中立':
                tab.row([('link','宣战',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：宣战',cs=sjk['主角']),dqmb()]),('text','两国进入敌对状态')])
                tab.row([('link','联盟',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：联盟',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币加入联盟，两国进入联盟状态')])
            wif.app.table(tab)


def gjmb(chushi=None,chakan=None):
    """国家面板"""
    global sjk
    if not chakan:
        chakan='基本'
    if chushi:
        wif.show(wif.Screen())
    wif.funcsx(ddt)
    sjk.anjian_pass()
    wif.app.clear()
    wif.app.title= '国家面板-%s面板-剩余行动力%s' % (chakan, sjk['国家'][sjk['主角']]['行动力'])
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,80,140))
    menu.link('查看大地图', lambda:[wif.hide(), wif.hide('menu')])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    gcwz=tuple(sjk.gcwz)
    gx,gy=gcwz
    dqid=sjk['地图'][(gx,gy)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    gjtj=sjk['统计']['国家'][gjid]
    dqtj=sjk['统计']['地区'][dqid]
    if gjdx.get('剩余夺回时间',False)!=False:
        tab.row([('text','剩余夺回时间'),('text','首都失陷！请在%s个月内夺回，否则灭国之灾将来到！'%(gjdx['剩余夺回时间']),0xff0000)])
    tab= wif.Table([60, 60, 60, 60])
    tab.row([('link','基本',lambda:gjmb(chakan='基本')),('link','简报',lambda:gjmb(chakan='简报')),('link','政策',lambda:gjmb(chakan='政策')),('link','地区',lambda:gjmb(chakan='地区'))])
    wif.app.table(tab)
    if chakan=='基本':
        tab= wif.Table([80, 140])
        tab.row([('text','国家名：'),('text','%s(id:%s)'%(gjdx['国家名'],gjid))])
        tab.row([('text','首都：'),('text','%s(id:%s)坐标:%s'%(sjk['地区'][gjdx['首都']]['地区名'],gjdx['首都'],str(sjk['地区'][gjdx['首都']]['坐标'])))])
        tab.row([('text','全国人口：'),('text','%s人'%(sjk['统计']['国家'][gjid]['人口数']))])
        tab.row([('text','经济总量：'),('text','%s'%(sjk['统计']['国家'][gjid]['经济']))])
        tab.row([('text','全国军队：'),('text','%s人'%(sjk['统计']['国家'][gjid]['兵力']))])
        tab.row([('text','拥有地区：'),('text','%s个'%len(gjdx['地区']))])
        tab.row([('text','货币：'),('text','%s元'%(gjdx['货币']))])
        wif.app.table(tab)
        tab= wif.Table([80, 140])
        tab.row([('text','类型'),('text','指数')])
        tab.row([('text','科技'),('text','%s级(%s)'%(len(str(gjdx['科技'])),gjdx['科技']))])
        tab.row([('text','科技加成'),('text','%s％'%(len(str(gjdx['科技']))*0.1*100))])
        wif.app.table(tab)
        tab= wif.Table([80, 140])
        tab.row([('text','税收种类'),('text','全国统一税率')])
        for na in gjdx['税收']:
            tab.row([('text','%s税收'%(na)),('text','%s％'%(gjdx['税收'][na]*100))])
        wif.app.table(tab)
    
    if chakan=='简报':
        tab= wif.Table([80, 140])
        tab.row([('text','编号'),('text','国家上月简报')])
        if sjk['AI'].rzlb['国家'].get(gjid,False)==False:
            tab.row([('text','无'),('text','无')])
        else:
            aaa=sjk['AI'].rzlb['国家'][gjid]
            aab=len(aaa)
            for na in xrange(aab):
                tab.row([('text','%s'%(na+1)),('text','%s'%(aaa[na]))])
        wif.app.table(tab)
    
    if chakan=='政策':
        if dqdx['国家']==sjk['主角']:
            tab= wif.Table([80, 140])
            tab.row([('text','国家指令'),('text','介绍')])
            tab.row([('link','更改商业税',lambda:[sjk['AI'].zl(dqid=dqid, zl='更改商业税', cs=wif.appuifw.query(u"商业税（0-100）％", 'float')), gjmb()]), ('text', '修改现行国家商业税率')])
            tab.row([('link','更改农业税',lambda:[sjk['AI'].zl(dqid=dqid, zl='更改农业税', cs=wif.appuifw.query(u"商业税（0-100）％", 'float')), gjmb()]), ('text', '修改现行国家农业税率')])
            tab.row([('link','国家改名',lambda:[sjk['AI'].zl(dqid=dqid, zl='国家改名', cs=wif.appuifw.query(cn("国家改名"), "text")), gjmb()]), ('text', '以%s元经费贯彻地区改名' % (max(gjtj['经济'] / 100, 1)))])
            wif.app.table(tab)
        else:
            wif.app.text('其他主权国家！')
            gjyj=gjdx['外交'].get(sjk['主角'],'中立')
            wif.app.text('我国与%s外交状态：%s' % (gjdx['国家名'], gjyj))
            tab= wif.Table([80, 140])
            tab.row([('text','地区指令'),('text','介绍')])
            #'宣战','联盟','中立'
            if gjyj=='联盟':
                tab.row([('link','宣战',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：宣战',cs=sjk['主角']),dqmb()]),('text','两国进入敌对状态')])
                tab.row([('link','中立',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：中立',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币退出联盟，两国进入中立状态')])
            if gjyj=='宣战':
                tab.row([('link','中立',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：中立',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币，两国进入中立状态')])
            if gjyj=='中立':
                tab.row([('link','宣战',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：宣战',cs=sjk['主角']),dqmb()]),('text','两国进入敌对状态')])
                tab.row([('link','联盟',lambda:[sjk['AI'].zl(dqid=dqid,zl='外交：联盟',cs=sjk['主角']),dqmb()]),('text','缴纳10000金币加入联盟，两国进入联盟状态')])
            wif.app.table(tab)
    
    if chakan=='地区':
        tab= wif.Table([80, 40, 100])
        tab.row([('text','地区'),('text','坐标'),('text','查看大地图')])
        if len(gjdx['地区'])>0:
            for na in gjdx['地区']:
                na=sjk['地区'][na]
                tab.row([('text','%s(id:%s)'%(na['地区名'],na['id'])), ('text','(x:%s,y:%s)'%na['坐标']), ('link','查看大地图',lambda:[
                    wif.funcsx(None), wif.hide(), ddt(gcwz=na['坐标'])])])
        else:
            tab.row([('text','无'),('text','无'),('text','无')])
        wif.app.table(tab)


def sjmb(chushi=None,chakan=None):
    """世界面板"""
    global sjk
    if not chakan:
        chakan='基本'
    if chushi:
        wif.show(wif.Screen())
    wif.funcsx(ddt)
    sjk.anjian_pass()
    wif.app.clear()
    wif.app.title= '世界之窗-%s面板' % (chakan)
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,80,140))
    menu.link('查看大地图', lambda:[wif.hide(), wif.hide('menu')])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    gcwz=tuple(sjk.gcwz)
    gx,gy=gcwz
    dqid=sjk['地图'][(gx,gy)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    gjtj=sjk['统计']['国家'][gjid]
    dqtj=sjk['统计']['地区'][dqid]
    tab= wif.Table([40, 40, 40, 40])
    tab.row([('link','基本',lambda:sjmb(chakan='基本')),('link','平均',lambda:sjmb(chakan='平均')),('text',''),('text','')])
    wif.app.table(tab)
    if chakan=='基本':
        tab= wif.Table([80, 140])
        mwgjlen=0
        for na in sjk['国家'].v:
            if len(sjk['国家'][na]['地区'])<1:
                mwgjlen+=1
        tab.row([('text','国家数量：'),('text','%s个(已灭亡%s个)'%(sjk['国家'].vlen,mwgjlen))])
        mwdqlen=0
        for na in sjk['地区'].v:
            if len(sjk['地区'][na]['地块'])<1:
                mwdqlen+=1
        tab.row([('text','地区数量：'),('text','%s个(已消失地区%s个)'%(sjk['地区'].vlen,mwdqlen))])
        tab.row([('text','世界面积：'),('text','%s平方公里'%(len(sjk['地图'].v)))])
        tab.row([('text','世界人口数：'),('text','%s人'%(sjk['统计']['世界']['人口数']))])
        tab.row([('text','经济总量：'),('text','%s'%(sjk['统计']['世界']['经济']))])
        tab.row([('text','货币总量：'),('text','%s元'%(sjk['统计']['世界']['货币']))])
        tab.row([('text','世界军队：'),('text','%s人'%(sjk['统计']['世界']['兵力']))])
        tab.row([('text','粮食总量：'),('text','%s'%(sjk['统计']['世界']['粮食']))])
        wif.app.table(tab)
        tab= wif.Table([80, 140])
        tab.row([('text','世界范围地区最多人口：'),('text','%s人'%(sjk['统计']['世界']['地区最高人口数']))])
        tab.row([('text','世界范围地区最低人口：'),('text','%s人'%(sjk['统计']['世界']['地区最低人口数']))])
        tab.row([('text','世界范围地区经济最好：'),('text','%s'%(sjk['统计']['世界']['地区最高经济']))])
        tab.row([('text','世界范围地区经济最低：'),('text','%s'%(sjk['统计']['世界']['地区最低经济']))])
        tab.row([('text','世界范围地区最多兵力：'),('text','%s人'%(sjk['统计']['世界']['地区最高兵力']))])
        tab.row([('text','世界范围地区最低兵力：'),('text','%s人'%(sjk['统计']['世界']['地区最低兵力']))])
        tab.row([('text','世界范围地区最多粮食：'),('text','%s单位'%(sjk['统计']['世界']['地区最高粮食']))])
        tab.row([('text','世界范围地区最低粮食：'),('text','%s单位'%(sjk['统计']['世界']['地区最低粮食']))])
        wif.app.table(tab)
        
    if chakan=='平均':
        wif.app.text('我国与世界平均水平之比较')
        tab= wif.Table([80, 140])
        tab.row([('text','各国平均拥有地区数：'),('text','%s个(我国拥有地区数%s个)'%(sjk['地区'].vlen/sjk['国家'].vlen,len(gjdx['地区'])))])
        tab.row([('text','各国平均人口数：'),('text','%s人(我国总人口数%s人)'%(sjk['统计']['世界']['人口数']/sjk['国家'].vlen,gjtj['人口数']))])
        tab.row([('text','各国平均经济总量：'),('text','%s(我国经济总量%s)'%(sjk['统计']['世界']['经济']/sjk['国家'].vlen,gjtj['经济']))])
        tab.row([('text','各国平均拥有货币总量：'),('text','%s元(我国拥有货币%s元)'%(sjk['统计']['世界']['货币']/sjk['国家'].vlen,gjdx['货币']))])
        tab.row([('text','各国平均军队：'),('text','%s人(我国总兵力%s人)'%(sjk['统计']['世界']['兵力']/sjk['国家'].vlen,gjtj['兵力']))])
        wif.app.table(tab)
        wif.app.text('我国各地区与世界平均水平之比较')
        tab= wif.Table([80, 140])
        tab.row([('text','地区平均人口数：'),('text','%s人(本地区人口数%s人)'%(sjk['统计']['世界']['人口数']/sjk['地区'].vlen,dqdx['人口数']))])
        tab.row([('text','地区平均经济总量：'),('text','%s(本地区经济%s)'%(sjk['统计']['世界']['经济']/sjk['地区'].vlen,dqtj['经济']))])
        tab.row([('text','地区平均军队：'),('text','%s人(本地区兵力%s人)'%(sjk['统计']['世界']['兵力']/sjk['地区'].vlen,dqdx['兵力']))])
        wif.app.table(tab)
    


def bzmb(chushi=None):
    """帮助面板"""
    global sjk
    if chushi:
        scr= wif.Screen()
        scr.set_size((20,20,200,200))
        wif.show(scr)
    wif.funcsx(ddt)
    sjk.anjian_pass()
    wif.app.clear()
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,80,140))
    menu.link('查看大地图', lambda:[wif.hide('menu'), wif.hide()])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    gcwz=tuple(sjk.gcwz)
    gx,gy=gcwz
    dqid=sjk['地图'][(gx,gy)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    gjtj=sjk['统计']['国家'][gjid]
    dqtj=sjk['统计']['地区'][dqid]
    if gjtj['人口数']>=100000 and gjtj['经济']>=100000 and len(gjdx['地区'])>=10 and gjtj['兵力']>=10000:
        wif.app.title= '邀请码'
        scr.text('感谢你的喜欢玩这个游戏，你已满足条件加群条件，邀请你加入历古仙穹聊天群，请加微信：shenlankedu，并且输入邀请码：〖%s】。我来拉你进群。（你可以按拨号键截图保存这条信息）'%(sjk['统计']['fdexpeed']))
    else:
        wif.app.title= '帮助手册'
        scr.text('''【功能导航】
军事：战争、征兵、解散。
外交：宣战、中立、联盟。
粮食：周边买入、周边卖出、本地买入、本地卖出。
地区：地区改名、地区合并、地块用地属性更改。
国家：国家改名、税收调整。
【影响关系】
人口：受粮食影响、受住宅用地影响。
经济：受人口影响、受商业用地影响、受税收影响。
粮食：受人口影响、受经济影响、受农业用地影响、受税收影响。
兵力：受粮食影响。
【名词解释】
方案无效：一、该方案前置条件不足；二、对方不接受该方案；三、国内反对。
首都占领：首都被占领三个月将游戏结束。
''')
    


####以下二级界面####
def ddt(chushi=None,gcwz=None,shijiao=None,ditudaxiao=None):
    """大地图"""
    global sjk
    if chushi:
        wif.show(wif.Screen())
    if gcwz:
        sjk.gcwz=list(gcwz)
    if shijiao:
        sjk['视角']=shijiao
    if ditudaxiao:
        if ditudaxiao[0]<=sjk.pmxy[0] and ditudaxiao[1]<=sjk.pmxy[1] and ditudaxiao[0]>=20 and ditudaxiao[1]>=20:
            sjk.dxdy=ditudaxiao
    wif.funcsx(main)
    sjk.anjian_pass()
    wif.app.clear()
    if len(sjk['国家'][sjk['主角']]['地区'])<1:
        wif.hide()
        wif.note("国家不存在，游戏结束。")
        wif.hide('menu')
        return None
    if sjk['统计']['国家'][sjk['主角']]['人口数']<1:
        sjk['国家'][sjk['主角']]['地区']=[]
        wif.hide()
        wif.note("无人之国还是国吗？亲，游戏结束。")
        wif.hide('menu')
        return None
    wif.app.title= '大地图-%s视角-剩余行动力%s' % (sjk['视角'], sjk['国家'][sjk['主角']]['行动力'])
    menu= wif.Menu()
    menu.title='菜单'
    menu.set_size((2,100,238,140))
    tm='------'
    if os.path.isdir('%s存档1'%(sjk.fileurl)):
        tm=time.localtime(os.stat("%s存档1"%sjk.fileurl).st_mtime)
    menu.link('存档一(%s年%s月%s日%s时%s分%s秒)' % (tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]), lambda:[wif.hide('menu'), sjk.cd(1)])
    
    tm='------'
    if os.path.isdir('%s存档2'%(sjk.fileurl)):
        tm=time.localtime(os.stat("%s存档2"%sjk.fileurl).st_mtime)
    menu.link('存档二(%s年%s月%s日%s时%s分%s秒)' % (tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]), lambda:[wif.hide('menu'), sjk.cd(2)])
    
    tm='------'
    if os.path.isdir('%s存档3'%(sjk.fileurl)):
        tm=time.localtime(os.stat("%s存档3"%sjk.fileurl).st_mtime)
    menu.link('存档三(%s年%s月%s日%s时%s分%s秒)' % (tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]), lambda:[wif.hide('menu'), sjk.cd(3)])
    menu.link('回主菜单', lambda:[wif.hide(), wif.hide('menu')])
    wif.app.bind(KMENU, lambda: wif.show(menu))#邦定左键
    wif.app.bind(K2, lambda:sjk.anjian('上'))
    wif.app.bind(K8, lambda:sjk.anjian('下'))
    wif.app.bind(K4, lambda:sjk.anjian('左'))
    wif.app.bind(K6, lambda:sjk.anjian('右'))
    wif.app.bind(K5, lambda:hdmb(chushi=True))
    font=sjk.font
    fontbl=sjk.fontbl
    tab= wif.Table([48 * fontbl, 48 * fontbl, 48 * fontbl, 48 * fontbl, 48 * fontbl])
    tab.row([('link','结束回合',lambda:[sjk.run(),ddt()],0xff0000,font),('text','%s年%s月'%(sjk['时间'][0],sjk['时间'][1]),0,font),('link','我的国家',lambda:ddt(gcwz=sjk['地区'][sjk['国家'][sjk['主角']]['首都']]['坐标']),0x0000ff,font),('link','缩小地图',lambda:ddt(ditudaxiao=(sjk.dxdy[0]*2,sjk.dxdy[1]*2)),0x999900,font),('link','放大地图',lambda:ddt(ditudaxiao=(sjk.dxdy[0]/2,sjk.dxdy[1]/2)),0x999900,font)])
    tab.row([('link','军事视角',lambda:ddt(shijiao='军事'),0x0000ff,font),('link','外交视角',lambda:ddt(shijiao='外交'),0x0000ff,font),('link','人口视角',lambda:ddt(shijiao='人口'),0x0000ff,font),('link','经济视角',lambda:ddt(shijiao='经济'),0x0000ff,font),('link','粮食视角',lambda:ddt(shijiao='粮食'),0x0000ff,font)])
    tab.row([('link','国家视角',lambda:ddt(shijiao='国家'),0x0000ff,font),('link','地形视角',lambda:ddt(shijiao='地形'),0x0000ff,font),('link','用地视角',lambda:ddt(shijiao='用地'),0x0000ff,font),('link','帮助手册',lambda:bzmb(chushi=True),0x0000ff,font),('link','世界之窗',lambda:sjmb(chushi=True),0x0000ff,font)])
    wif.app.table(tab)
    if sjk['视角']=='军事':
        wif.app.text('地区兵力占世界兵力总数越多颜色越深。', font=font)
    elif sjk['视角']=='外交':
        wif.app.text('红色敌对，绿色联盟，蓝色中立。', font=font)
    elif sjk['视角']=='人口':
        wif.app.text('地区人口占世界人口总数越多颜色越深', font=font)
    elif sjk['视角']=='经济':
        wif.app.text('地区经济占世界经济总数越多颜色越深', font=font)
    elif sjk['视角']=='粮食':
        wif.app.text('地区粮食占世界粮食总数越多颜色越深', font=font)
    elif sjk['视角']=='用地':
        wif.app.text('红色住宅用地，黄色农业用地，蓝色商业用地。', font=font)
    wif.app.image(sjk.hzdt(), align='center')
    gx,gy=sjk.gcwz
    tab= wif.Table([80 * fontbl, 140 * fontbl])
    tab.row([('text','地形与位置：',0,font),('text','%s(x:%s,y:%s)'%(sjk['地图'][(gx,gy)]['地形'],gx,gy),0,font)])
    dqid=sjk['地图'][(gx,gy)]['地区']
    dqdx=sjk['地区'][dqid]
    gjid=dqdx['国家']
    gjdx=sjk['国家'][gjid]
    tab.row([('text','地区名：',0,font),('link','%s(id:%s)'%(dqdx['地区名'],dqid),lambda:dqmb(chushi=True),0x0000ff,font)])
    tab.row([('text','国家：',0,font),('link','%s(id:%s)'%(gjdx['国家名'],dqdx['国家']),lambda:gjmb(chushi=True),0x0000ff,font)])
    tab.row([('text','人口数：',0,font),('text','%s'%(dqdx['人口数']),0,font)])
    tab.row([('text','经济：',0,font),('text','%s'%(dqdx['经济']),0,font)])
    if dqdx['国家']==sjk['主角']:
        tab.row([('text','粮食：',0,font),('text','流通%s国库%s'%(dqdx['粮食']['流通'],dqdx['粮食']['国库']),0,font)])
        tab.row([('text','兵力：',0,font),('text','%s'%(dqdx['兵力']),0,font)])
    wif.app.table(tab)


####以下一级界面####
def yx(pd,ddxz=1):
    """开始游戏"""
    global sjk
    sjk.anjian_pass()
    wif.funcsx(main)
    def yx_func():
        global sjk
        sjk.__dict__['c'+""+'c']='开始游戏'
    if pd=='继续游戏':
        if not sjk['主角']:
            try:
                k=sjk.dd(ddxz)
                yx_func()
            except:
                k=None
                wif.note('存档%s已损坏！' % ddxz)
            if k:
                ddt(chushi=True)
            else:
                pd='选择难度'
        elif len(sjk['国家'][sjk['主角']]['地区'])<1 and appuifw2.query(cn("就在刚才，你的国家被灭了，是重新开始还是读取存档！"),"query",ok=cn("重新开始"),cancel=cn("读档")):
            pd='选择难度'
        elif len(sjk['国家'][sjk['主角']]['地区'])>0 and appuifw2.query(cn("请选择接着刚才玩还是读取存档"),"query",ok=cn("刚才"),cancel=cn("读档")):
            ddt(chushi=True)
        else:
            try:
                sjk=cz()
                k=sjk.dd(ddxz)
                yx_func()
            except:
                k=None
                wif.note('存档%s已损坏！' % ddxz)
            if k:
                ddt(chushi=True)
            else:
                pd='选择难度'
    if pd=='选择难度':
        sjk=cz()
        yx_func()
        wif.app.clear()
        wif.app.text('请选择难度')
        check= wif.Checkbox('onecheck')
        check.row('容易')
        check.row('正常')
        check.row('困难')
        check.row('专家')
        wif.app.checkbox(check)
        def z():
            if check.checked[0]==1:
                sjk['难度']='容易'
            elif check.checked[1]==1:
                sjk['难度']='正常'
            elif check.checked[2]==1:
                sjk['难度']='困难'
            elif check.checked[3]==1:
                sjk['难度']='专家'
            yx('重新开始',ddxz=ddxz)
        wif.app.link('确定', z, align='center')
    if pd=='重新开始':
        wif.app.clear()
        sjk['地图'].new(tuple(sjk.gcwz))
        dqid=sjk['地图'][tuple(sjk.gcwz)]['地区']
        gjid=sjk['地区'][dqid]['国家']
        sjk['主角']=gjid
        tab= wif.Table([140, 140])
        tab.row([('text','国家：'),('text','%s(id:%s)'%(sjk['国家'][gjid]['国家名'],gjid))])
        tab.row([('text','首都地区：'),('text','%s(id:%s)'%(sjk['地区'][dqid]['地区名'],dqid))])
        tab.row([('text','难度：'),('text','%s'%(sjk['难度']))])
        tab.row([('link','确定角色信息',lambda:[sjk.run(),ddt(chushi=True)]),('link','不满意重输',lambda:yx('选择难度',ddxz=ddxz))])
        wif.app.table(tab)


def main(chushi=None):
    global sjk
    wif.funcsx(None)
    sjk.anjian_pass()
    wif.app.clear()
    wif.app.title= '历古仙穹'
    fontbl=sjk.fontbl
    font=(u'',15*fontbl)
    wif.app.image(sjk.tp("%s图片\\主菜单\\标题.png" % (sjk.fileurl)), align='center')
    if (sjk['主角']!=None) and len(sjk['国家'][sjk['主角']]['地区'])>=1:
        wif.app.link('继续刚才游戏', (lambda:ddt(chushi=True)), align='center', font=font)
    
    #[列数与宽度]
    tab= wif.Table([80 * fontbl, 140 * fontbl])
    #[(),(),(类型,显示,颜色,字体)]
    if os.path.isfile('%s存档1\\存档0.dat'%(sjk.fileurl)):
        tab.row([('link','继续游戏',(lambda:yx('继续游戏',ddxz=1)),0x000099,font),('text','打开存档一接着玩？',0x000000,font)])
    else:
        tab.row([('text','继续游戏',0x555555,font),('text','打开存档一接着玩？',0x000000,font)])
    if os.path.isfile('%s存档2\\存档0.dat'%(sjk.fileurl)):
        tab.row([('link','继续游戏',(lambda:yx('继续游戏',ddxz=2)),0x000099,font),('text','打开存档二接着玩？',0x000000,font)])
    else:
        tab.row([('text','继续游戏',0x555555,font),('text','打开存档二接着玩？',0x000000,font)])
    if os.path.isfile('%s存档3\\存档0.dat'%(sjk.fileurl)):
        tab.row([('link','继续游戏',(lambda:yx('继续游戏',ddxz=3)),0x000099,font),('text','打开存档三接着玩？',0x000000,font)])
    else:
        tab.row([('text','继续游戏',0x555555,font),('text','打开存档三接着玩？',0x000000,font)])
    
    
    tab.row([('link','重新开始',(lambda:yx('选择难度')),0x000099,font),('text','开始一个新游戏',0x000000,font)])
    tab.row([('link','帮助手册',(lambda: wif.note('''每个人都可以是主角。
管理地区，经营国家。
无边界地图，多样地形。
截图：拨号键；
地图移动：2468；
地图地块选中：5；
其他链接按：上下左右确定；

【国家篇】
•前言
作为一名领袖，要解决国家的吃饭问题，所以需要粮食！
国家发展离不开税收，要有足够好的经济来支撑国家！
保卫国家，建立军队捍卫领土完整！
•税收制定
税收有两种：商业税、农业税。商业税在每年一月到账，以货币结算。农业税在每年十月到账，以粮食结算。
•国库
国库是储备物资，你可以用它平衡物价、赈灾、也可以供给军队；

【地区篇】
•粮食
一个人没人每天需要消耗一单位粮食，而政策指令一月一次，也就是说一个人每月要消耗30单位粮食，所以请确保粮食储备！粮食不是凭空而来，粮食也需要农业用地支持。而流通粮食，也就是税收以外的粮食就是国民的口粮咯，你不会让国民饿死的；粮食也可以从其他地区买卖，比如买敌国的粮食，敌国人口死绝，间接导致经济下滑，农业没人种，你说会发生什么状况。。。
•经济
经济的增长需要商业用地的支撑，没有商业用地就没有经济，其次没有人口就没有商业，还有你的税收因素在影响经济；
•人口
人口的增长需要住宅用地的支持，和商业用地同理，其次没有粮食就没有人口，都饿死了呗，可不要饿死了你的国民（每人每天一单位粮食消耗），军队也不要饿死了（军队比国民消耗粮食高出三倍）；

•结语
这个当元宵节的礼物还是现在发呢，我还没想好，你如果在元宵节以前看到，那么我就是提前发了，如果是元宵节当天，那么祝大家元宵节快乐！！塞班S60V3吧吧友快乐！！！
2017.02.02.
''')),0x000099,font),('text','需要查看帮助？',0x000000,font)])
    
    
    menu= wif.Menu()
    menu.title='检查更新%s'%sjk.banben
    menu.set_size((2,100,238,140))
    menu.link('地址一：检查更新、反馈、评论', lambda:[wif.hide('menu'), sjk.openucweb('https://udzn.wodemo.com')])
    menu.link('地址二：检查更新、反馈、评论', lambda:[wif.hide('menu'), sjk.openucweb('https://udzn.wodemo.net')])
    menu.link('地址三：检查更新、反馈、评论', lambda:[wif.hide('menu'), sjk.openucweb('http://udzn.yes168.com')])
    menu.link('塞班S60V3吧：反馈、评论', lambda:[wif.hide('menu'), sjk.openucweb('http://tieba.baidu.com/mo/m?kw=%E5%A1%9E%E7%8F%ADs60v3')])
    tab.row([('link','检查更新', (lambda: wif.show(menu)), 0x000099, font), ('text', '检查更新', 0x000000, font)])
    tab.row([('link','关于版本',(lambda: wif.note('''当前版本：%s
策划：百度贴吧-塞班S60V3吧-因素黑白
地图素材：百度贴吧-塞班S60V3吧-葛柄仑
名称文本：百度贴吧-塞班S60V3吧-超音速DX
测试：超音速dx、葛柄仑。

BUG反馈可以到百度贴吧塞班S60V3吧找到历古仙穹这个贴子留言，或者到https://udzn.wodemo.com留言，或者http://udzn.yes168.com留言''' % sjk.banben)),0x000099,font),('text','版本号·更新地址',0x000000,font)])
    tab.row([('link','梦醒时分', (lambda: wif.hide()), 0x000099, font), ('text', '退出游戏？', 0x000000, font)])
    wif.app.table(tab)
    wif.app.text('穿越时空，梦想就在这里；', font=font, align='center')
    wif.app.text('历古仙穹，无穷尽的世界；', font=font, align='center')
    wif.app.text('没有历史，乱世由你谱写。', font=font, align='center')


tm=time.localtime(time.time())
if tm[0]==2017 and tm[1]==2 and tm[2]==11:
    wif.start_up("%s图片\\主菜单\\农历正月十五元宵节.png" % (sjk.fileurl))
    e32.ao_sleep(3)
    wif.start_up("%s图片\\主菜单\\元宵节节日祝福.png" % (sjk.fileurl))
    e32.ao_sleep(5)
wif.start_up("%s图片\\主菜单\\标题.png" % (sjk.fileurl))
main()

while True:
    try:
        wif.wait()
    except:
        import traceback
        a=traceback.format_exc()
        b='出现异常：%s'%(str(a))
        print (b)
        wif.app.text(b)

