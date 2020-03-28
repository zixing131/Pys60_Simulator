#-*- coding:utf-8 -*-
#泡椒聊天API类
#Powered By 52cyy℡
#PJChat_v1.3(Build20110906)

import appuifw,e32,os
import globalui,graphics
import httplib,urllib,socket
import audio,time
import thread

def cn(x):return x#.decode("utf8")
def en(x):return x#.encode("utf8")
def quote(cntxt):
    return urllib.quote(en(cntxt))
def unquote(entxt):
    return cn(urllib.unquote(entxt))

import os,sys
path1 = os.getcwd()
index = path1.rfind('\\')
mypath=path1[:index]
index = mypath.rfind('\\')
mypath=mypath[:index]
#mypath2=path1+'\\src\\'
sys.path.append(mypath)
#sys.path.append(mypath2)
AppDisk = mypath
class AppSets:
    def __init__(self):
        self.path=mypath+"\\PJchat_v1.3_src(Build20110906)\\"
        self.list=[]
        for name,value in [index.split("=") for index in open(self.path+"Data\\Settings.ini","r").read().splitlines()]:
            self.__dict__[name]=value
            self.list.append(name)
        self.getbbslist()
    def getbbslist(self):
        self.bbslist=[]
        file=open(self.path+"Data\\bbsdata.ini","r")
        data=cn(file.read()).split("&")
        file.close()
        ctnames=data[0].split("|")
        ctids=data[1].split("|")
        self.bbsimg=graphics.Image.open(self.path+"Images\\bbsimgs\\bbslogo.jpg").resize((40,40))
        for i in range(len(ctnames)):
            try:
                img=graphics.Image.open(self.path+"Images\\bbsimgs\\%s.jpg"%en(ctids[i])).resize((40,40))
            except:
                img=self.bbsimg
            self.bbslist.append([ctnames[i],ctids[i],img])
        del file,data,ctnames,ctids,img
    def save(self):
        try:
            open(self.path+"Data\\Settings.ini","w").write("\n".join([name+"="+self.__dict__[name] for name in self.list]))
        except:
            pass
    def bbslistsave(self):
        ctnames=ctids=""
        for i in self.bbslist:
            ctnames+=(i[0]+"|")
            ctids+=(i[1]+"|")
        bbsdata=ctnames[:len(ctnames)-1]+"&"+ctids[:len(ctids)-1]
        try:
            open(self.path+"Data\\bbsdata.ini","w").write(en(bbsdata))
        except:pass

class HTTPs:
    def __init__(self,ap,rid=""):
        self.ap=ap
        self.rid=rid
        self.agent=quote(cn("泡椒聊天v1.3"))
        self.host=self.port=""
        self.geturl=""

    def CONN(self):
        if self.ap==0:#wap
            self.conn=httplib.HTTPConnection("10.0.0.172",80)
            self.geturl="http://%s%s"%(self.host,self.port)
        elif self.ap==1:#net/wifi
            self.conn=httplib.HTTPConnection(self.host)
            self.geturl=self.port
        else:pass

    def POST(self,params):
        try:
            self.CONN()
            #params = urllib.urlencode({"":""})
            headers = {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain'}
            self.conn.request("POST", self.geturl, params, headers)
            data=self.conn.getresponse()
            data=data.read()
            self.conn.close()
            return data
        except:
            return "ERROR"

    def GET(self):
        try:
            self.CONN()
            self.conn.request("GET",self.geturl)
            data=self.conn.getresponse()
            data=data.read()
            self.conn.close()
            return data
        except:
            return "ERROR"

    def getrid(self,id,pw):
        self.host="ct.paojiao.cn"
        self.port="/user.do?method=getuser&rid="
        self.CONN()
        params=urllib.urlencode({"mobile": en(id),"password":en(pw),"returl": en("")})
        data=cn(self.POST(params))
        if data.find(cn("已成功登录泡椒!")) != -1:
            start_pos=data.find(cn("系统将自动返回..."))
            end_pos=data.find(cn('">返回'))
            rid=data[start_pos:end_pos].split("rid=")[1]
            self.rid=rid
            return "OK"
        elif data.find(cn("呃...您填写的密码不正确哦.")) != -1:
            return "ID OR PW ERROR"
        else: return "ERROR"

    def login(self):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=login&type=rid&rid=%s&agent=%s"%(self.rid,self.agent)
        data=cn(self.GET())
        return data

    def gettximg(self,url):
        url=url.replace("http://","")
        self.host=url[:url.find("/")]
        self.port=url[url.find("/"):]
        data=self.GET()
        return data

    def getfriendlist(self):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=getfriendlist&rid=%s"%self.rid
        data=cn(self.GET())
        return data

    def getfriendinfo(self,uid):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=getfriendinfo&userid=%s&rid=%s"%(uid,self.rid)
        data=cn(self.GET())
        return data

    def getnewmessage(self):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=getnewmessage&rid=%s"%self.rid
        data=cn(self.GET())
        return data

    def getmessagecontent(self,msgid):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=getmessagecontent&msgid=%s&rid=%s"%(msgid,self.rid)
        data=cn(self.GET())
        return data

    def getmessagelist(self,type="outbox",limit="10"):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=getmessagelist&type=%s&limit=%s&rid=%s"%(type,limit,self.rid)
        data=cn(self.GET())
        return data

    def sendmessage(self,uid,content):
        content=quote(content)
        self.host="pjchat.sinaapp.com"
        self.port="/?act=sendmessage&to=%s&content=%s&rid=%s"%(uid,content,self.rid)
        data=cn(self.GET())
        return data

    def gettopiclist(self,ctid="76",limit="15"):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=gettopiclist&ctid=%s&limit=%s&rid=%s"%(ctid,limit,self.rid)
        data=cn(self.GET())
        return data

    def gettopicdetail(self,topicid):
        self.host="pjchat.sinaapp.com"
        self.port="/?act=gettopicdetail&topicid=%s&rid=%s"%(topicid,self.rid)
        data=cn(self.GET())
        return data

    def publishtopic(self,ctid,topic,content,type=""):
        topic=quote(topic)
        content=quote(content)
        self.host="pjchat.sinaapp.com"
        self.port="/?act=publishtopic&ctid=%s&topic=%s&content=%s&type=%s&rid=%s"%(ctid,topic,content,type,self.rid)
        data=cn(self.GET())
        return data

    def publishreply(self,topicid,content):
        content=quote(content)
        self.host="pjchat.sinaapp.com"
        self.port="/?act=sendmessage&topicid=%s&content=%s&rid=%s"%(topicid,content,self.rid)
        data=cn(self.GET())
        return data

    def feedback(self,nickname,content):
        nickname=quote(nickname)
        content=quote(content)
        self.host="pjchat.sinaapp.com"
        self.port="/?act=feedback&nickname=%s&content=%s"%(nickname,content)
        data=cn(self.GET())
        return data

    def getannounce(self):
        self.host="pjcyun.sinaapp.com"
        self.port="/announce13.php"
        data=self.GET()
        return data

    def checkver(self):
        self.host="pjcyun.sinaapp.com"
        self.port="/checkver13.php"
        data=self.GET()
        return data

class Analyse_FNDZONE:
    def __init__(self,cndata):
        self.data=cndata
        for name,value in [index.split("=") for index in self.data.split("&")]:
            self.__dict__[name]=value
    def getzonetxt(self):
        def isonline(online):
            if online==u"ON":
                return cn("在线")
            elif online==u"OFF":
                return cn("离线")
        def ischeck(checked):
            if checked==u"Y":
                return cn("已验证")
            elif checked==u"N":
                return cn("未验证")
        def guestlist():
            list=""
            guestnames=self.guestnames.split("|")
            guesttimes=self.guesttimes.split("|")
            for index in range(int(self.guestcount[0])):
                list+=cn("%s(%s)\n")%(guestnames[index],guesttimes[index])
            return list
        self.TXT=cn("%s的空间\n━━━━━━━━━\n")%self.nickname+cn("[ID]：%s(%s)(%s)\n")%(self.id,isonline(self.online),ischeck(self.checked))+cn("[银子]：%s  [金子]：%s\n")%(self.silver,self.gold)+cn("[水草]：%s\n")%self.grass+cn("[池塘等级]：%s级\n[在线等级]：在线%s级\n")%(self.ctrank,self.olrank)+cn("[死党]：%s\n")%self.buddiesnames+cn("[家族]：%s(%s)\n")%(self.familyname,self.familypost)+cn("[入塘时间]：%s(%s天)\n")%(self.jointime,self.joinday)+cn("[所在地]：%s-%s\n")%(self.provience,self.city)+cn("[签名]：%s\n")%self.sign+cn("[最近来访]：\n")+guestlist()+cn("━━━━━━━━━\n泡椒,不只下载才想你…")
        return self.TXT

class Analyse_FNDLIST:
    def __init__(self,cndata):
        self.data=cndata
        msk=graphics.Image.open(AppDisk+":\\system\\Apps\\PJChat\\Images\\tximgs\\msk.png").resize((23,23))
        maskimg=graphics.Image.new((23,23),"L")
        maskimg.blit(msk)
        for name in ["ggon","ggoff","mmon","mmoff"]:
            tempimg=graphics.Image.open(AppDisk+":\\system\\Apps\\PJChat\\Images\\tximgs\\%s.png"%name).resize((23,23))
            self.__dict__[name+"img"]=(tempimg,maskimg)
            del tempimg
        del msk,maskimg
        for name,value in [index.split("=") for index in self.data.split("&")]:
            self.__dict__[name]=value.split("|")

    def getgrouplist(self):
        list1=[]
        for index in range(int(self.groupcount[0])):
            list1.append([0,0])
        for i1 in range(int(self.fndcount[0])):
            for i2 in range(int(self.groupcount[0])):
                if self.group[i1]==self.groupid[i2]:
                    list1[i2][1]+=1
                    if self.online[i1]=="ON":
                        list1[i2][0]+=1
        list2=[]
        #[分组名称,在线情况,分组ID,是否展开,分组详情([])]
        for i3 in range(int(self.groupcount[0])):
            list2.append([\
                self.groupname[i3],\
                cn("[%s/%s]")%(list1[i3][0],list1[i3][1]),\
                self.groupid[i3],\
                "off",\
                []])
        return list2

    def getgroupdetail(self,groupid):
        def gettximg(online,gender):
            if online==u"ON":
                if gender==u"GG":
                    return self.ggonimg
                else:
                    return self.mmonimg
            elif online==u"OFF":
                if gender==u"GG":
                    return self.ggoffimg
                else:
                    return self.mmoffimg
            else:
                return self.ggoffimg
        list=[]
        #[好友昵称,ID,头像]
        for index in range(int(self.fndcount[0])):
            if self.group[index]==groupid:
                tximg=gettximg(self.online[index],self.gender[index])
                list.append([self.nickname[index],self.id[index],tximg])
        return list

class Analyse_MSG:
    def __init__(self,cndata):
        try:
            self.datalist=cndata.split("&&")
        except:
            self.datalist=[cndata]

    def getmsglist(self,type):
        #[来自+用户昵称,短文本,用户ID,长文本,时间,类型,消息ID]
        if type=="outbox":
            txt="[To]"
        else:txt="[From]"
        self.count=0
        list=[]
        for data in self.datalist:
            for name,value in [index.split("=") for index in data.replace("from","nickname").split("&")]:
                self.__dict__[name]=value.split("|")
            self.count+=int(self.msgcount[0])
            for index in range(int(self.msgcount[0])):
                list.append([txt+self.nickname[index],self.shorttext[index],self.authorids[index],self.fulltext[index],self.time[index],self.type[index],self.msgid[index]])
        return list

class Analyse_TOPIC:
    def __init__(self,cndata):
        self.data=cndata
        for name,value in [index.split("=") for index in self.data.split("&")]:
            self.__dict__[name]=value.split("|")
    def gettopiclist(self):
        list=[]
        #[新+头部+标题,作者昵称+[回/阅],帖子ID,作者昵称,ID]
        for index in range(int(self.topiccount[0])):
            if self.news[index]=="1":
                self.news[index]=cn("[新]")
            if self.headers[index] != "":
                self.headers[index]=cn("[%s]")%self.headers[index]
            list.append([self.news[index]+self.headers[index]+self.titles[index],cn("(%s)[%s回/%s阅]")%(self.authors[index],self.visits[index],self.replys[index]),self.topicid[index],self.authors[index],self.authorids[index]])
        return list

class UserInfo:
    def __init__(self):
        self.path=AppDisk+":\\system\\Apps\\PJChat\\"
        self.OL_start=0
        self.OL_gaptime=None
        self.OL_old_starttime=None
        self.OL_new_starttime=None
        self.OL_keep=e32.Ao_timer()
        self.MSG_auto=0
        self.MSG_gaptime=None
        self.MSG_starttime=None
        self.MSG_keep=e32.Ao_timer()
        #self.set_zoneinfo()
        #self.set_tximg()
        #self.set_fndlist()
    def set_tximg(self):
        try:
            self.tximg=graphics.Image.open(self.path+"Images\\tximgs\\mytximg.png").resize((40,40))
        except:
            self.tximg=graphics.Image.open(self.path+"Images\\tximgs\\usertximg.png").resize((40,40))
    def set_zoneinfo(self):
        def isonline(online):
            if online==u"ON":
                return cn("在线")
            elif online==u"OFF":
                return cn("离线")
        def ischeck(checked):
            if checked==u"Y":
                return cn("已验证")
            elif checked==u"N":
                return cn("未验证")
        file=open(self.path+"Tempfile\\myinfo.dat","r")
        data=cn(file.read())
        file.close()
        for name,value in [index.split("=") for index in data.split("&")]:
            self.__dict__[name]=value
        self.myinfo=[\
        cn("[ID]：%s(%s)(%s)")%(self.id,isonline(self.online),ischeck(self.checked)),\
        cn("[银子]：%s　[金子]：%s")%(self.silver,self.gold),\
        cn("[水草(积分)]：%s")%self.grass,\
        cn("[池塘等级]：%s级")%self.ctrank,\
        cn("[在线等级]：在线%s级")%self.olrank,\
        cn("[家族]：开发者工作室"),\
        cn("[入塘时间]：%s(%s天)")%(self.jointime,self.joinday),\
        cn("[所在地]：%s-%s")%(self.provience,self.city)]
        #死党,访客列表
        self.mybestfnds=[]
        self.visitors=[]
        try:
            for i1 in range(int(self.buddiescount)):
                self.mybestfnds.append([self.buddiesnames.split("|")[i1],self.buddiesids.split("|")[i1]])
        except:pass
        try:
            for i2 in range(int(self.guestcount)):
                self.visitors.append([self.guestnames.split("|")[i2],self.guestids.split("|")[i2],cn("(%s)")%self.guesttimes.split("|")[i2]])
        except:pass
    def set_fndlist(self):
        file=open(self.path+"Tempfile\\fndlist.dat","r")
        data=cn(file.read())
        file.close()
        self.fndact=Analyse_FNDLIST(data)
        self.fndlist=self.fndact.getgrouplist()
        self.fndlist_len=len(self.fndlist)
