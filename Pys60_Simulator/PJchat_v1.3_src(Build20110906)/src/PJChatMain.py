#-*- coding:utf-8 -*-
#泡椒聊天主程序
#Powered By 52cyy℡
#PJChat_v1.3(Build20110906)

from pjc_APIs_class import *
from pjc_extend_functions import *

sets=AppSets()
user=UserInfo()

class MainPageUI(object):
    def StartApp(self):
        self.SetAppData()
        self.E.ao_yield()
        self.pre_page="loginpage"
        self.page="loginpage"
        self.LoginPage()
        self.E.ao_yield()
        if sets.ap_id=="-1":
            self.page="setap"
            self.MaskPG()
            self.SetAccessPointPG()
        else:
            self.SetDefaultAP()

    def __init__(self): 
        self.UI,self.GBUI,self.E,self.G,self.TM,self.SK=appuifw,globalui,e32,graphics,time,socket
        self.path = mypath + "\\PJchat_v1.3_src(Build20110906)\\"
        self.img=self.maskimg=None
        self.UI.app.screen="full"
        self.c=self.UI.Canvas(redraw_callback=self.Img_Redraw,resize_callback=self.Img_Resize,event_callback=self.Key_Event)
        self.UI.app.body=self.c
        self.blit=self.c.blit
        self.x,self.y=self.c.size
        self.img=self.newimg()
        self.lock=self.E.Ao_lock()
        self.zt=u"Sans MT 936_s60"
        self.UI.app.menu=[]
        self.UI.app.exit_key_handler=lambda:None
        self.tab=1

    def SetAppData(self):
        #登录界面变量
        self.ID=cn(sets.loginid)
        self.PW=cn(sets.loginpw)
        self.PW2=u"*" * len(self.PW)
        self.loginpage1=self.G.Image.open(self.path+"Images\\loginpage1.jpg")
        self.loginpage2=self.G.Image.open(self.path+"Images\\loginpage2.jpg")
        self.loginpage_index=0
        #菜单变量
        self.menu_list=[["1.切换窗口",["1.空间","2.好友","3.池塘","4.信箱","5.挂机"],0],["2.注销登录",[],0],["3.软件设置",["1.挂机","2.消息音","3.接入点"],1],["4.更多功能",["1.公告 [#]","2.更新 [*]","3.反馈 [0]","4.帮助 [8]","5.捐赠"],1],["5.退出软件",[],1]]
        self.menu_bgcl=0xdcf0fa
        self.menu1_index=0
        self.menu2_index=0
        self.menu2="off"
        #文本界面变量
        self.textpg_gdt=0
        self.textpg_run=0#判断是否在滚动
        self.textpg_txt=self.textpg_title=self.textpg_zjname=""
        #列表界面变量
        self.listpg_index=0
        self.listpg_pos=0
        self.listpg_list=[]
        self.listpg_title=""
        self.listpg_zjname=""
        #Mini文本界面变量
        self.minitextpg_gdt=0
        self.minitextpg_txt=self.minitextpg_title=self.minitextpg_zjname=""
        #Mini列表界面变量
        self.minilistpg_index=0
        self.minilistpg_list=[]
        self.minilistpg_title=""
        #设置接入点数据变量
        self.setap_index=self.setaptype_index=0
        self.access_point_dict=self.SK.access_points()
        self.access_point_list=[cn("未设置")]
        for i in self.access_point_dict:
            self.access_point_list.append(i["name"])
        self.aptypelist=[cn("1.wap[例:cmwap,uniwap等]"),cn("2.net/wifi[例:cmnet,uninet,无线网]")]
        #聊天页面变量
        self.chat_uid=""
        self.chat_name=""
        self.chat_content=""
        #反馈页面变量
        self.fd_index=0
        self.fd_name=self.fd_content=""
        #主界面数据
        self.tab=0
        self.tabtext=[[cn("空间"),cn("我的空间")],[cn("好友"),cn("好友列表")],[cn("池塘"),cn("泡椒池塘")],[cn("信箱"),cn("我的信箱")],[cn("挂机"),cn("在线挂机")]]
        self.zone_index=0
        self.fnd_index=0#好友
        self.fndlist_index=0#列表
        self.fnd_all_index=0#总
        self.fnd_all_pos=0
        self.fnd_choice="group"
        self.bbs_pos=self.bbs_index=0
        self.msgbox_index=0
        self.msgbox_menu=[cn("新消息"),cn("收件箱"),cn("发件箱"),cn("手动刷新"),cn("刷新设置")]
        self.olmenu_index=0
        self.olmenu=[[cn("开始"),0],[cn("停止"),1],[cn("设置"),1]]
        #读取缓存文本
        (self.helptxt_shu,self.helptxt_heng)=self.ReadTXT("help")
        (self.changelogtxt_shu,self.changelogtxt_heng)=self.ReadTXT("changelog")
        (self.announcetxt_shu,self.announcetxt_heng)=self.ReadTXT("announce")

    def Play_Sound(self):
        sound=audio.Sound.open(self.path+"Data\\newmsg.mp3")
        try:
            sound.play()
            self.E.ao_sleep(3)
            sound.stop()
        except:pass
        sound.close()
        del sound

    def SetDefaultAP(self):
        try:
            ap=self.SK.access_point(int(sets.ap_id))
            self.SK.set_default_access_point(ap)
            self.http=HTTPs(int(sets.ap_type),sets.rid)
            return
        except:
            self.UI.note(cn("请重新设置接入点"),"info",1)
            return

    def newimg(self,imgsize=None):
        if imgsize:
            return self.G.Image.new(imgsize)
        else:
            return self.G.Image.new((self.x,self.y))

    def get_text_len(self,txt,font=16):
        return self.img.measure_text(txt,(self.zt,font))[1]

    def showtext(self,txt,limit_len,font=16):
        if self.img.measure_text(txt,(self.zt,font))[1]<=limit_len:
            return txt
        else:
            temptxt=""
            for i in txt:
                temptxt+=i
                if self.img.measure_text(temptxt+cn("…"),(self.zt,font))[1]>limit_len:
                    return temptxt[:len(temptxt)-1]+cn("…")

    def getshowtab(self,tab):
        a=tab-1;b=tab;c=tab+1
        if a<0:
            a=len(self.tabtext)-1
        if c>len(self.tabtext)-1:
            c=0
        return [[a,0,0xffffff,(62,43)],[b,1,0x323232,(self.x/2-8,43)],[c,0,0xffffff,(self.x-47,43)]]

    def LoginPage(self):
        #竖屏
        if self.x==240:
            #绘制登录界面图片
            self.img.blit(self.loginpage1)
            #选择框
            self.img.polygon(rim(98,182+33*self.loginpage_index,230,204+33*self.loginpage_index,2),0x50b4e6,width=2)
            #绘制账号密码
            self.img.text((125,202),self.ID,0x323232,(self.zt,16))
            self.img.text((125,237),self.PW2,0x323232,(self.zt,16))
        #横屏
        elif self.x==320:
            self.img.blit(self.loginpage2)
            self.img.polygon(rim(150,133+30*self.loginpage_index,306,155+30*self.loginpage_index,2),0x50b4e6,width=2)
            self.img.text((180,153),self.ID,0x323232,(self.zt,16))
            self.img.text((180,186),self.PW2,0x323232,(self.zt,16))
        self.img.text((self.x-95,100),cn("泡椒聊天v1.3"),0x323232,(self.zt,16))
        #菜单,登录
        self.img.text((3,self.y-2),cn("菜单"),0x323232,(self.zt,18))
        self.img.text((self.x-40,self.y-2),cn("登录"),0x323232,(self.zt,18))
        self.blit(self.img)

    def TabPG(self):
        for i in xrange(48):
            self.img.line((0,i,self.x,i),(50+i,150+i,200+i))
        #绘制用户头像
        self.img.blit(user.tximg,target=(4,4),mask=getmaskimg(user.tximg,"L"))
        #头像框
        self.img.rectangle((3,3,45,45),0xb6e5f7,width=2)
        #标题框
        self.img.rectangle((0,48,self.x,51),fill=0xdcf0fa)
        self.img.polygon(rim(100,22,self.x-55,48,3),fill=0xdcf0fa)
        for i in xrange(8):
            self.img.line((0,51+i,self.x,51+i),(180+i*5.7,225+i*2,250))
        self.Gettime()
        #时间,用户昵称
        self.img.text((self.x-40,18),self.presenttime,0x323232,(self.zt,16))
        self.img.text((48,20),self.showtext(user.nickname,self.x-90,15),0x323232,(self.zt,15))
        #顶部菜单
        for i in self.getshowtab(self.tab):
            self.img.text(i[3],self.tabtext[i[0]][i[1]],i[2],(self.zt,15))
        #顶部向左,右三角形
        self.img.polygon(triangle(48,35,"left",6),fill=0xffffff)
        self.img.polygon(triangle(self.x-3,35,"right",6),fill=0xffffff)

    def MainPG(self):
        if self.page != "main":
            pass
        else:
            if self.tab==0:
                self.ZonePG()
            elif self.tab==1:
                self.FndlistPG()
            elif self.tab==2:
                self.BBSPG()
            elif self.tab==3:
                self.MsgboxPG()
            elif self.tab==4:
                self.OnlinePG()

    def ZonePG(self):
        self.zoneimg=self.newimg((self.x,2*self.y))
        self.zoneimg.clear(0xdcf0fa)
        #基本资料框
        self.zoneimg.text((5,75),cn("[基本资料]"),0x565656,(self.zt,16))
        self.zoneimg.line((2,78,self.x-3,78),0xb6e5f7)
        self.zoneimg.line((2,79,self.x-3,79),0xffffff)
        for i in user.myinfo:
            self.zoneimg.text((5,102+22*user.myinfo.index(i)),i,0x323232,(self.zt,16))
        #空间列表
        if user.buddiescount=="":
            user.buddiescount="0"
        if user.guestcount=="":
            user.guestcount="0"
        zonemenu=[cn("[我的签名]：%s")%self.showtext(user.sign,self.x-100),cn("[我的死党]：(%s个)-(点击展开)")%user.buddiescount,cn("[最近来访]：(%s个)-(点击展开)")%user.guestcount,cn("[点击刷新空间资料]")]
        for i in zonemenu:
            self.zoneimg.line((2,260+30*zonemenu.index(i),self.x-3,260+30*zonemenu.index(i)),0xb6e5f7)
            self.zoneimg.line((2,261+30*zonemenu.index(i),self.x-2,261+30*zonemenu.index(i)),0xffffff)
            self.zoneimg.text((5,284+30*zonemenu.index(i)),i,0x565656,(self.zt,16))
        del zonemenu
        #基本资料选择框
        if self.zone_index==0:
            self.zoneimg.polygon(rim(2,80,self.x-3,258,2),0x50b4e6,width=1.5)
            self.img.blit(self.zoneimg)
        #列表选择框
        else:
            self.zoneimg.polygon(rim(2,232+self.zone_index*30,self.x-3,258+self.zone_index*30,2),0x50b4e6)
            if self.x==240:
                self.img.blit(self.zoneimg,target=(0,-85))
            elif self.x==320:
                self.img.blit(self.zoneimg,target=(0,-165))
        self.TabPG()
        self.ctrlpanel(cn("菜单"),cn("切换"),1)

    def FndlistPG(self):
        self.fndlistimg=self.newimg()
        self.fndlistimg.clear(0xdcf0fa)
        self.fnd_limit={240:7,320:5}
        tpos=(self.fnd_all_pos-self.fnd_all_index)*32
        ypos=80
        #选择框
        self.fndlistimg.polygon(rim(2,tpos+58+self.fnd_all_index*32,self.x-9,tpos+87+self.fnd_all_index*32,2),fill=0x50b4e6)
        #好友列表
        for i1 in user.fndlist:
            #分组名字
            self.fndlistimg.text((17,tpos+ypos),i1[0],0x565656,(self.zt,16))
            #在线详情eg.(5/23)
            self.fndlistimg.text((self.x-12-self.get_text_len(i1[1]),tpos+ypos),i1[1],0x565656,(self.zt,16))
            #分隔线
            self.fndlistimg.line((3,tpos+ypos+8,self.x-9,tpos+ypos+8),0xb6e5f7)
            self.fndlistimg.line((3,tpos+ypos+9,self.x-9,tpos+ypos+9),0xffffff)
            #分组未展开
            if i1[3]=="off":
                self.fndlistimg.polygon(triangle(12,tpos+ypos-8,"right",6),fill=0x565656)
            #展开分组
            elif i1[3]=="open":
                self.fndlistimg.polygon(triangle(10,tpos+ypos-5,"down",6),fill=0x565656)
                for i2 in i1[4]:
                    #好友头像
                    self.fndlistimg.blit(i2[2][0],target=(6,tpos+ypos+13),mask=i2[2][1])
                    #头像与昵称分割线
                    self.fndlistimg.line((33,tpos+ypos+13,33,tpos+ypos+37),0xb6e5f7)
                    #好友昵称
                    self.fndlistimg.text((38,tpos+ypos+32),self.showtext(i2[0],self.x-50,15),0x323232,(self.zt,15))
                    #分割线
                    self.fndlistimg.line((3,tpos+ypos+40,self.x-9,tpos+ypos+40),0xb6e5f7)
                    self.fndlistimg.line((3,tpos+ypos+41,self.x-9,tpos+ypos+41),0xffffff)
                    ypos+=32
            ypos+=32
        self.img.blit(self.fndlistimg)
        #滚动条
        if user.fndlist_len<=self.fnd_limit[self.x]:
            self.img.polygon(rim(self.x-6,59,self.x-2,self.y-26,2),0,width=1,fill=0xb6e5f7)
        else:
            #滚动条背景
            self.img.polygon(rim(self.x-7,58,self.x-1,self.y-25,2),fill=0x50b4e6)
            #滚动条
            tpos/=32
            self.img.polygon(rim(self.x-6,59-(self.y-85)/float(user.fndlist_len)*tpos,self.x-2,59+(self.y-85)/float(user.fndlist_len)*self.fnd_limit[self.x]-(self.y-85)/float(user.fndlist_len)*tpos,2),0,width=1,fill=0xb6e5f7)
        self.TabPG()
        self.ctrlpanel(cn("菜单"),cn("切换"),1)

    def BBSPG(self):
        self.bbsimg=self.newimg()
        self.bbsimg.clear(0xdcf0fa)
        self.bbs_limit={240:5,320:3}
        tpos=(self.bbs_pos-self.bbs_index)*48
        #画选择框
        self.bbsimg.polygon(rim(2,tpos+58+self.bbs_index*48,self.x-9,tpos+103+self.bbs_index*48,2),fill=0x50b4e6)
        #画列表
        for i in range(len(sets.bbslist)):
            self.bbsimg.blit(sets.bbslist[i][2],target=(5,tpos+61+i*48))
            self.bbsimg.text((50,tpos+80+i*48),sets.bbslist[i][0],0x323232,(self.zt,18))
            self.bbsimg.text((50,tpos+98+i*48),cn("[池塘ID：%s]")%sets.bbslist[i][1],0x323232,(self.zt,15))
            self.bbsimg.line((2,tpos+104+i*48,self.x-9,tpos+104+i*48),0xb6e5f7)
            self.bbsimg.line((2,tpos+105+i*48,self.x-9,tpos+105+i*48),0xffffff)
        #把列表填充到img上
        self.img.blit(self.bbsimg)        
        #滚动条
        if len(sets.bbslist)<=self.bbs_limit[self.x]:
            self.img.polygon(rim(self.x-6,59,self.x-2,self.y-26,2),0,width=1,fill=0xb6e5f7)
        else:
            #滚动条背景
            self.img.polygon(rim(self.x-7,58,self.x-1,self.y-25,2),fill=0x50b4e6)
            #滚动条
            tpos/=48
            self.img.polygon(rim(self.x-6,59-(self.y-85)/float(len(sets.bbslist))*tpos,self.x-2,59+(self.y-85)/float(len(sets.bbslist))*self.bbs_limit[self.x]-(self.y-85)/float(len(sets.bbslist))*tpos,2),0,width=1,fill=0xb6e5f7)
        self.TabPG()
        self.ctrlpanel(cn("菜单"),cn("切换"),1)
    
    def MsgboxPG(self):
        self.msgboximg=self.newimg()
        self.msgboximg.clear(0xdcf0fa)
        #新消息提示
        self.msgboximg.text((3,78),cn("您有[%s]条新消息！")%sets.new_msg,0x323232,(self.zt,16))
        #刷新剩余时间
        if user.MSG_auto:
            try:
                self.msgboximg.text((self.x-100,78),cn("[%s]后刷新")%getshowtime(int(user.MSG_gaptime+user.MSG_starttime-self.TM.clock())),0xff0000,(self.zt,14))
            except:pass
        else:
            self.msgboximg.text((self.x-100,78),cn("自动刷新已关闭"),0xff0000,(self.zt,14))
        self.msgboximg.line((0,82,self.x,82),0xb6e5f7)
        self.msgboximg.line((0,83,self.x,83),0xffffff)
        #信箱菜单
        if self.x==240:#横屏
            for i in range(3):
                self.msgboximg.polygon(rim(30,91+i*50,self.x-31,131+i*50),0x3296c8)
                self.msgboximg.text((85,120+i*50),self.msgbox_menu[i],0x323232,(self.zt,20))
            #信箱选择框
            if self.msgbox_index<3:
                self.msgboximg.polygon(rim(30,91+self.msgbox_index*50,self.x-31,131+self.msgbox_index*50),0xffffff,width=1,fill=0x50b4e6)
                self.msgboximg.text((85,120+self.msgbox_index*50),self.msgbox_menu[self.msgbox_index],0xffffff,(self.zt,20))
        elif self.x==320:#竖屏
            for i in range(3):
                self.msgboximg.polygon(rim(10+i*102,100,106+i*102,140),0x3296c8)
                self.msgboximg.text((28+i*102,130),self.msgbox_menu[i],0x323232,(self.zt,20))
            #信箱选择框
            if self.msgbox_index<3:
                self.msgboximg.polygon(rim(10+self.msgbox_index*102,100,106+self.msgbox_index*102,140),0xffffff,width=1,fill=0x50b4e6)
                self.msgboximg.text((28+self.msgbox_index*102,130),self.msgbox_menu[self.msgbox_index],0xffffff,(self.zt,20))
        #底部菜单
        self.msgboximg.line((0,self.y-81,self.x,self.y-81),0xb6e5f7)
        self.msgboximg.line((0,self.y-80,self.x,self.y-80),0xffffff)
        for i in range(2):
            self.msgboximg.polygon(rim(20+i*(self.x/2-10),self.y-72,self.x/2-10+i*(self.x/2-10),self.y-32),0x3296c8)
            if self.x==240:
                self.msgboximg.text((25+i*(self.x/2-10),self.y-41),self.msgbox_menu[i+3],0x323232,(self.zt,20))
            elif self.x==320:
                self.msgboximg.text((45+i*(self.x/2-10),self.y-41),self.msgbox_menu[i+3],0x323232,(self.zt,20))
        #底部菜单选择框
        if self.msgbox_index>=3:
            self.msgboximg.polygon(rim(20+(self.msgbox_index-3)*(self.x/2-10),self.y-72,self.x/2-10+(self.msgbox_index-3)*(self.x/2-10),self.y-32),0xffffff,width=1,fill=0x50b4e6)
            if self.x==240:
                self.msgboximg.text((25+(self.msgbox_index-3)*(self.x/2-10),self.y-41),self.msgbox_menu[self.msgbox_index],0xffffff,(self.zt,20))
            elif self.x==320:
                self.msgboximg.text((45+(self.msgbox_index-3)*(self.x/2-10),self.y-41),self.msgbox_menu[self.msgbox_index],0xffffff,(self.zt,20))
        self.img.blit(self.msgboximg)
        self.TabPG()
        self.ctrlpanel(cn("菜单"),cn("切换"),1)

    def OnlinePG(self):
        self.onlineimg=self.newimg()
        self.onlineimg.clear(0xdcf0fa)
        #在线信息
        if user.OL_start:
            self.onlineimg.text((3,78),cn("[正在挂机]：%s")%getshowtime(int(self.TM.clock()-user.OL_old_starttime)),0x323232,(self.zt,16))
            refreshtime=int(user.OL_gaptime+user.OL_new_starttime-self.TM.clock())
            if self.x==240:
                self.onlineimg.text((3,200),cn("[刷新剩余时间]：%s")%getshowtime(refreshtime),0xff0000,(self.zt,16))
            elif self.x==320:
                self.onlineimg.text((175,78),cn("[刷新剩余]：%s")%getshowtime(refreshtime),0xff0000,(self.zt,16))
        else:
            self.onlineimg.text((3,78),cn("您还没有开始挂机…"),0x323232,(self.zt,16))
        self.onlineimg.line((0,82,self.x,82),0xb6e5f7)
        self.onlineimg.line((0,83,self.x,83),0xffffff)
        self.onlineimg.text((3,104),cn("[在线等级]：%s级")%user.olrank,0x323232,(self.zt,16))
        self.onlineimg.text((3,128),cn("[在线总时长]：%s")%user.onlinetime,0x323232,(self.zt,16))
        self.onlineimg.text((3,152),cn("[升级剩余时间]：%s")%user.upgradetime,0x323232,(self.zt,16))
        self.onlineimg.text((3,176),cn("[在线等级排名]：%s")%user.onlinerank,0x323232,(self.zt,16))
        self.onlineimg.line((0,self.y-61,self.x,self.y-61),0xb6e5f7)
        self.onlineimg.line((0,self.y-60,self.x,self.y-60),0xffffff)
        #底部菜单
        for i in range(3):
            self.onlineimg.polygon(rim(7+i*(self.x/3.1),self.y-56,(i+1)*(self.x/3.1),self.y-28,2),0x3296c8)
            self.onlineimg.text((self.x/9.2+i*(self.x/3.1),self.y-34),self.olmenu[i][0],0x323232,(self.zt,16))
        self.onlineimg.polygon(rim(7+self.olmenu_index*(self.x/3.1),self.y-56,(self.olmenu_index+1)*(self.x/3.1),self.y-28,2),0xffffff,width=1,fill=0x50b4e6)
        self.onlineimg.text((self.x/9.2+self.olmenu_index*(self.x/3.1),self.y-34),self.olmenu[self.olmenu_index][0],0xffffff,(self.zt,16))
        self.img.blit(self.onlineimg)
        self.TabPG()
        self.ctrlpanel(cn("菜单"),cn("切换"),1)

    def MenuPG(self):
        if self.pre_page=="loginpage":
            if self.menu1_index<2:
                self.menu1_index=2
        if self.menu2=="off":
            #一级菜单范围框
            self.img.polygon(rim(30,self.y-31-30*len(self.menu_list),self.x-30,self.y-27,2),0,width=1,fill=self.menu_bgcl)
            #一级菜单选择框
            self.img.polygon(rim(32,self.y-28-30*len(self.menu_list)+self.menu1_index*30,self.x-32,self.y-1-len(self.menu_list)*30+self.menu1_index*30,2),fill=0x50b4e6)
            #一级菜单列表
            for i1 in self.menu_list:
                if i1[2]==0:
                    self.img.text((45,self.y-5-len(self.menu_list)*30+self.menu_list.index(i1)*30),cn(i1[0]),0x969696,(self.zt,18))
                elif i1[2]==1:
                    self.img.text((45,self.y-5-len(self.menu_list)*30+self.menu_list.index(i1)*30),cn(i1[0]),0x323232,(self.zt,18))
                self.img.line((32,self.y-30-self.menu_list.index(i1)*30,self.x-32,self.y-30-self.menu_list.index(i1)*30),0xb6e5f7)
                self.img.line((32,self.y-29-self.menu_list.index(i1)*30,self.x-32,self.y-29-self.menu_list.index(i1)*30),0xffffff)
                #画三角形
                if i1[1] != []:
                    if i1[2]==0:
                        self.img.polygon(triangle(self.x-45,self.y-15-30*len(self.menu_list)+self.menu_list.index(i1)*30,"right",6),fill=0x969696)
                    elif i1[2]==1:
                        self.img.polygon(triangle(self.x-45,self.y-15-30*len(self.menu_list)+self.menu_list.index(i1)*30,"right",6),fill=0x323232)
        elif self.menu2=="on":
            #二级菜单范围框
            templist=self.menu_list[self.menu1_index][1]
            self.img.polygon(rim(self.x-135,self.y-26-30*len(self.menu_list),self.x-35,self.y-22-30*len(self.menu_list)+25*len(templist),2),0,width=1,fill=self.menu_bgcl)
            #二级菜单选择框
            self.img.polygon(rim(self.x-133,self.y-23-30*len(self.menu_list)+self.menu2_index*25,self.x-37,self.y-1-30*len(self.menu_list)+self.menu2_index*25,2),fill=0x50b4e6)
            #二级菜单列表
            for i2 in templist:
                self.img.text((self.x-125,self.y-2-len(self.menu_list)*30+templist.index(i2)*25),cn(i2),0x323232,(self.zt,18))
                self.img.line((self.x-133,self.y-150+templist.index(i2)*25,self.x-37,self.y-150+templist.index(i2)*25),0xb6e5f7)
                self.img.line((self.x-133,self.y-149+templist.index(i2)*25,self.x-37,self.y-149+templist.index(i2)*25),0xffffff)
        self.ctrlpanel(cn("选择"),cn("取消"),1)

    def tWrapTXT(self,txt):
        txt_shu=[]
        txt_heng=[]
        for i in tWrap(txt,int(240*0.9)):
            txt_shu.append(i)
        for i in tWrap(txt,int(320*0.9)):
            txt_heng.append(i)
        return (txt_shu,txt_heng)

    def ReadTXT(self,txt_file):
        file=open(self.path+"Data\\%s.txt"%txt_file,"r")
        temptxt=cn(file.read())
        file.close()
        return self.tWrapTXT(temptxt)

    def HelpPG(self):
        if self.x==240:
            self.textpg_txt=self.helptxt_shu
        elif self.x==320:
            self.textpg_txt=self.helptxt_heng
        self.textpg_title=cn("帮助-关于")
        self.textpg_zjname=cn("")
        self.TextPG()

    def ChangelogPG(self):
        if self.x==240:
            self.textpg_txt=self.changelogtxt_shu
        elif self.x==320:
            self.textpg_txt=self.changelogtxt_heng
        self.textpg_title=cn("更新日记")
        self.textpg_zjname=cn("检查更新")
        self.TextPG()

    def AnnouncePG(self):
        if self.x==240:
            self.textpg_txt=self.announcetxt_shu
        elif self.x==320:
            self.textpg_txt=self.announcetxt_heng
        self.textpg_title=cn("最新公告")
        self.textpg_zjname=cn("刷新")
        self.TextPG()

    def TextPG_up(self):
        if self.textpg_run==0:
            self.textpg_run=1
            for x in xrange(0,5):
                self.textpg_gdt-=0.8
                if self.textpg_gdt<0:
                    self.textpg_gdt=0
                    self.TextPG()
                    self.textpg_run=0
                    break
                self.TextPG()
                self.E.ao_yield()
            self.textpg_run=0
        else:pass

    def TextPG_down(self):
        if self.textpg_run==0:
            self.textpg_run=1
            for x in xrange(0,5):
                self.textpg_gdt+=0.8
                if self.textpg_gdt>float(len(self.textpg_txt)-(self.y-50)/20):
                    self.textpg_gdt=float(len(self.textpg_txt)-(self.y-50)/20)
                    self.TextPG()
                    self.textpg_run=0
                    break
                self.TextPG()
                self.E.ao_yield()
            self.textpg_run=0
        else:pass

    def TextPG(self):
        self.img.clear(0xffffff)
        #文本长度大于屏幕
        if len(self.textpg_txt)*20>275:
            for i in xrange(len(self.textpg_txt)):
                self.img.text((3,(50-self.textpg_gdt*20)+i*20),self.textpg_txt[i],0x323232,(self.zt,16))
            #滚动条背景
            self.img.polygon(rim(self.x-7,26,self.x-1,self.y-26,2),fill=0x50b4e6)
            #滚动条长度
            self.gdtlen=(self.y-60)*(self.y-60)/(len(self.textpg_txt)*20.0)
            self.gdtimg=self.newimg((5,self.gdtlen))
            self.gdtimg.rectangle((0,0,5,self.gdtlen),0,width=1,fill=0xb6e5f7)
            #滚动条位置
            self.img.blit(self.gdtimg,(-(self.x-6),-(27+(self.y-26-self.gdtlen-26)/(float(len(self.textpg_txt)-(self.y-50)/20))*self.textpg_gdt)))
        #文本长度小于屏幕
        else:
            for i in xrange(len(self.textpg_txt)):
                self.img.text((3,50+i*20),self.textpg_txt[i],0x323232,(self.zt,16))
            #滚动条
            self.img.rectangle((self.x-7,27,self.x-1,self.y-26),0,width=1,fill=0xb6e5f7)
        self.ctrlpanel(self.textpg_zjname,cn("返回"),0,self.textpg_title)

    def ListPG(self):
        self.img.clear(0xdcf0fa)
        self.listpg_limit={240:6,320:4}
        tpos=self.listpg_pos-self.listpg_index
        #选择框
        self.img.polygon(rim(2,27+(self.listpg_index+tpos)*45,self.x-9,69+(self.listpg_index+tpos)*45,2),fill=0x50b4e6)
        for i in range(len(self.listpg_list)):
            #第一行
            self.img.text((5,46+(i+tpos)*45),self.showtext(self.listpg_list[i][0],self.x-12,16),0x323232,(self.zt,16))
            self.img.line((5,49+(i+tpos)*45,self.x-12,49+(i+tpos)*45),0xb6e5f7)
            #第二行
            self.img.text((5,67+(i+tpos)*45),self.showtext(self.listpg_list[i][1],self.x-12,14),0x323232,(self.zt,14))
            #分隔线
            self.img.line((2,70+(i+tpos)*45,self.x-9,70+(i+tpos)*45),0xb6e5f7)
            self.img.line((2,71+(i+tpos)*45,self.x-9,71+(i+tpos)*45),0xffffff)
        #滚动条
        if len(self.listpg_list)<=self.listpg_limit[self.x]:
            self.img.polygon(rim(self.x-6,26,self.x-2,self.y-26,2),0,width=1,fill=0xb6e5f7)
        else:
            #滚动条背景
            self.img.polygon(rim(self.x-7,25,self.x-1,self.y-25,2),fill=0x50b4e6)
            #滚动条
            self.img.polygon(rim(self.x-6,26-(self.y-52)/float(len(self.listpg_list))*tpos,self.x-2,26+(self.y-52)/float(len(self.listpg_list))*self.listpg_limit[self.x]-(self.y-52)/float(len(self.listpg_list))*tpos,2),0,width=1,fill=0xb6e5f7)
        self.ctrlpanel(self.listpg_zjname,cn("返回"),0,self.listpg_title)

    def MiniTextPG(self):
        #透明蒙板
        self.img.blit(self.maskimg)
        if len(self.minitextpg_txt)<=5:
            minitextbox_len=len(self.minitextpg_txt)
        else:
            minitextbox_len=5
        #范围框
        self.img.polygon(rim(3,self.y-27-minitextbox_len*25-40,self.x-4,self.y-27,2),fill=0xdcf0fa)
        #划线
        self.img.line((5,self.y-27-25*minitextbox_len-11,self.x-5,self.y-27-25*minitextbox_len-11),0xb6e5f7)
        self.img.line((5,self.y-27-25*minitextbox_len-10,self.x-5,self.y-27-25*minitextbox_len-10),0xffffff)
        #标题
        self.img.text((12,self.y-27-25*minitextbox_len-15),self.showtext(self.minitextpg_title,self.x-35,18),0x323232,(self.zt,18,self.G.FONT_BOLD))
        #滚动条
        if len(self.minitextpg_txt)<=5:
            self.img.polygon(rim(self.x-11,self.y-27-25*minitextbox_len-8,self.x-7,self.y-30,2),0,width=1,fill=0xb6e5f7)
        else:
            #滚动条背景
            self.img.polygon(rim(self.x-12,self.y-27-25*minitextbox_len-8,self.x-6,self.y-30,2),fill=0x50b4e6)
            #滚动条开始坐标
            gdtstart=self.y-35-25*minitextbox_len+self.minitextpg_gdt*(165/len(self.minitextpg_txt))
            #滚动条结束坐标
            gdtend=self.y-30-(165/len(self.minitextpg_txt))*(len(self.minitextpg_txt)-5)+self.minitextpg_gdt*(165/len(self.minitextpg_txt))
            #画滚动条
            self.img.polygon(rim(self.x-11,gdtstart,self.x-7,gdtend,2),0,width=1,fill=0xb6e5f7)
        #文本
        for i in range(minitextbox_len):
            self.img.text((11,self.y-12-25*minitextbox_len+i*25),self.minitextpg_txt[i+self.minitextpg_gdt],0x323232,(self.zt,16))
        self.ctrlpanel(self.minitextpg_zjname,cn("返回"),1)

    def MiniListPG(self):
        #透明蒙板
        self.img.blit(self.maskimg)
        #列表框范围
        self.img.polygon(rim(3,self.y-27-len(self.minilistpg_list)*28-31,self.x-4,self.y-27,2),fill=0xdcf0fa)
        #列表选择框
        self.img.polygon(rim(6,self.y-27-len(self.minilistpg_list)*28+self.minilistpg_index*28+2,self.x-7,self.y-27-len(self.minilistpg_list)*28+(self.minilistpg_index+1)*28-2,2),fill=0x50b4e6)
        #列表标题
        self.img.text((12,self.y-27-len(self.minilistpg_list)*28-8),self.minilistpg_title,0x323232,(self.zt,18,self.G.FONT_BOLD))
        #绘制列表[昵称,ID,时间]
        for i in self.minilistpg_list:
            if len(i)==2:
                self.img.text((10,self.y-27-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28+23),self.showtext(i[0],self.x-20),0x323232,(self.zt,16))
            elif len(i)==3:
                self.img.text((10,self.y-27-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28+23),self.showtext(i[0],self.x-20-self.get_text_len(i[2])),0x323232,(self.zt,16))
                self.img.text((self.x-10-self.get_text_len(i[2]),self.y-27-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28+23),i[2],0x323232,(self.zt,16))
            self.img.line((5,self.y-27-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28,self.x-5,self.y-27-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28),0xb6e5f7)
            self.img.line((5,self.y-26-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28,self.x-5,self.y-26-len(self.minilistpg_list)*28+self.minilistpg_list.index(i)*28),0xffffff)
        self.ctrlpanel(cn("选择"),cn("返回"),1)

    def InfoBoxPG(self,title,showtxt,zjname="",yjname=""):
        #消息框
        self.img.polygon(rim(3,self.y-90,self.x-4,self.y-27,2),fill=0xdcf0fa)
        self.img.line((5,self.y-65,self.x-5,self.y-65),0xb6e5f7)
        self.img.line((5,self.y-64,self.x-5,self.y-64),0xffffff)
        #标题
        self.img.text((10,self.y-68),cn("[%s]")%title,0x323232,(self.zt,18,self.G.FONT_BOLD))
        #消息内容
        self.img.text((10,self.y-38),showtxt,0x323232,(self.zt,16))
        self.ctrlpanel(zjname,yjname,1)

    #设置接入点界面
    def SetAccessPointPG(self):
        #透明蒙板
        self.img.blit(self.maskimg)
        #接入点框范围
        self.img.polygon(rim(3,self.y-58-len(self.access_point_list)*28,self.x-4,self.y-27,2),fill=0xdcf0fa)
        #接入点选择框
        self.img.polygon(rim(6,self.y-27-len(self.access_point_list)*28+self.setap_index*28+2,self.x-7,self.y-27-len(self.access_point_list)*28+(self.setap_index+1)*28-2,2),fill=0x50b4e6)
        #接入点标题
        self.img.text((self.x/4,self.y-27-len(self.access_point_list)*28-8),cn("设置联网接入点："),0x323232,(self.zt,15,self.G.FONT_BOLD))
        #接入点列表
        for i in self.access_point_list:
            self.img.text((12,self.y-27-len(self.access_point_list)*28+self.access_point_list.index(i)*28+23),i,0x323232,(self.zt,16))
            self.img.line((5,self.y-27-len(self.access_point_list)*28+self.access_point_list.index(i)*28,self.x-5,self.y-27-len(self.access_point_list)*28+self.access_point_list.index(i)*28),0xb6e5f7)
            self.img.line((5,self.y-26-len(self.access_point_list)*28+self.access_point_list.index(i)*28,self.x-5,self.y-26-len(self.access_point_list)*28+self.access_point_list.index(i)*28),0xffffff)
        #当前接入点打"√"
        self.img.text((self.x-30,self.y-27-len(self.access_point_list)*28+int(sets.ap_pos)*28+23),cn("√"),0x323232,(self.zt,16))
        self.ctrlpanel(cn("选择"),cn("返回"),1)

    #设置接入点类型界面
    def SetAPtypePG(self):
        #透明蒙板
        self.img.blit(self.maskimg)
        #接入点类型框范围
        self.img.polygon(rim(3,self.y-27-2*28-31,self.x-4,self.y-27,2),fill=0xdcf0fa)
        #接入点类型选择框
        self.img.polygon(rim(6,self.y-27-2*28+self.setaptype_index*28+2,self.x-7,self.y-27-2*28+(self.setaptype_index+1)*28-2,2),fill=0x50b4e6)
        #接入点类型标题
        self.img.text((self.x/4,self.y-27-2*28-8),cn("设置接入点类型："),0x323232,(self.zt,15,self.G.FONT_BOLD))
        #接入点类型列表
        for i in self.aptypelist:
            self.img.text((12,self.y-27-2*28+self.aptypelist.index(i)*28+23),i,0x323232,(self.zt,16))
            self.img.line((5,self.y-27-2*28+self.aptypelist.index(i)*28,self.x-5,self.y-27-2*28+self.aptypelist.index(i)*28),0xb6e5f7)
            self.img.line((5,self.y-27-2*28+self.aptypelist.index(i)*28+1,self.x-5,self.y-27-2*28+self.aptypelist.index(i)*28+1),0xffffff)
        self.ctrlpanel(cn("选择"),cn("返回"),1)

    def FeedBackPG(self):
        self.img.clear(0xffffff)
        self.img.text((5,50),cn("我们期待您的建议！"),0x323232,(self.zt,18))
        self.img.text((5,80),cn("昵称(选填):"),0x323232,(self.zt,18))
        self.img.polygon(rim(5,85,self.x-6,112,2),fill=0xb6e5f7)
        self.img.text((5,140),cn("反馈内容(必填):"),0x323232,(self.zt,18))
        self.img.polygon(rim(5,145,self.x-6,172,2),fill=0xb6e5f7)
        self.img.text((8,106),self.showtext(self.fd_name,self.x-20),0x323232,(self.zt,16))
        self.img.text((8,166),self.showtext(self.fd_content,self.x-20),0x323232,(self.zt,16))
        self.img.polygon(rim(5,85+self.fd_index*60,self.x-6,112+self.fd_index*60),0,width=1)
        self.img.text((5,self.y-26),cn("Powered By 52cyy℡ ©2011"),0x323232,(self.zt,18))
        self.ctrlpanel(cn("发送"),cn("返回"),0,cn("用户反馈"))

    def FndZonePG(self):
        if self.x==240:
            self.textpg_txt=self.fndzone_shu
        elif self.x==320:
            self.textpg_txt=self.fndzone_heng
        self.textpg_title=cn("好友资料")
        self.textpg_zjname=cn("聊天")
        self.TextPG()

    def ChatPG(self):
        self.img.clear(0xffffff)
        #显示昵称
        self.img.polygon(rim(3,28,self.x-4,55,2),0,width=1,fill=0xb6e5f7)
        self.img.text((5,50),self.showtext(self.chat_name,self.x-6),0x323232,(self.zt,16))
        #聊天记录
        self.img.polygon(rim(3,59,self.x-4,self.y-77,2),0,width=1,fill=0xb6e5f7)
        self.img.line((6,84,self.x-6,84),0x323232)
        self.img.line((6,85,self.x-6,85),0xffffff)
        self.img.text((5,80),cn("[聊天记录]-(暂不支持)"),0x323232,(self.zt,14))
        self.img.text((self.x/3+15,self.y/2),cn("(暂无)"),0x323232,(self.zt,18))
        #消息内容
        self.img.text((3,self.y-58),cn("请输入内容[按OK键编辑]："),0x323232,(self.zt,14))
        self.img.polygon(rim(3,self.y-55,self.x-4,self.y-28,2),0,width=1,fill=0xb6e5f7)
        self.img.text((5,self.y-34),self.showtext(self.chat_content,self.x-6),0x323232,(self.zt,16))
        self.ctrlpanel(cn("发送"),cn("返回"),0,cn("与好友聊天中…")) 

    def MaskPG(self):
        self.maskimg=self.G.screenshot()
        tempimg=self.newimg()
        tempimg.clear(0)
        maskimg=self.G.Image.new(tempimg.size,"L")
        maskimg.clear(0x00ff00)
        self.maskimg.blit(tempimg,mask=maskimg)
        self.img.blit(self.maskimg)
        del tempimg,maskimg
        
    def Gettime(self):
        shi,fen=self.TM.localtime()[3],self.TM.localtime()[4]
        self.shi=str(shi)
        if shi<10:
            self.shi=u"0"+cn(str(shi))
        self.fen=str(fen)
        if fen<10:
            self.fen=u"0"+cn(str(fen))
        self.presenttime=cn("%s:%s")%(self.shi,self.fen)

    def ctrlpanel(self,zjname,yjname,type=0,title=""):
        for i in xrange(25):
            self.img.line((0,self.y-i,self.x,self.y-i),(50+i,150+i,200+i))
        self.img.line((0,self.y-23,self.x,self.y-23),0xb6e5f7)
        self.img.text((3,self.y-2),zjname,0xffffff,(self.zt,18))
        self.img.text((self.x-40,self.y-2),yjname,0xffffff,(self.zt,18))
        if type==0:#绘制标题面板
            for i in xrange(25):
                self.img.line((0,i,self.x,i),(75-i,175-i,225-i))
            self.img.text((5,20),title,0xffffff,(self.zt,16))
            self.Gettime()
            self.img.text((self.x-45,21),self.presenttime,0xffffff,(self.zt,18))
        self.blit(self.img)
        if self.page=="main" and self.tab==3 and user.MSG_auto:
            self.E.ao_sleep(1,lambda:self.MainPG())
        elif self.page=="main" and self.tab==4 and user.OL_start:
            self.E.ao_sleep(1,lambda:self.MainPG())

    def ExitAct(self):
        self.lock.signal()
        try:sets.save()
        except:pass
        os.abort()

    def OnlineAct(self,type="start"):
        if type=="start":
            if user.OL_start:
                self.UI.note(cn("挂机已开始！"),"info",1)
                return
            self.E.ao_yield()
            choice=self.UI.popup_menu([cn("10分钟"),cn("20分钟"),cn("30分钟")],cn("刷新间隔"))
            if choice==None:
                return
            user.OL_gaptime=[600,1200,1800][choice]
            user.OL_start=1
        elif type=="stop":
            self.E.ao_yield()
            if not(user.OL_start):
                self.UI.note(cn("挂机未开始！"),"info",1)
                return
            if self.UI.query(cn("正在挂机，确定要停止？"),"query",1):
                user.OL_start=0
                user.OL_gaptime=None
                user.OL_old_starttime=user.OL_new_starttime=None
                user.OL_keep.cancel()
                self.UI.note(cn("挂机已停止！"),"info",1)
            return
        thread.start_new_thread(self.GetMsgAct,("newmsg",))
        user.OL_keep.after(user.OL_gaptime,lambda:self.OnlineAct("keep"))
        if not(user.OL_old_starttime):
            user.OL_old_starttime=self.TM.clock()
        user.OL_new_starttime=self.TM.clock()

    def MsgRefreshMenuAct(self):
        self.E.ao_yield()
        choice=self.UI.popup_menu([cn("[获取新消息]"),cn("[刷新收件箱(10条)]"),cn("[刷新发件箱(10条)]")],cn("手动刷新消息"))
        if choice==None:
            return
        elif choice==0:
            self.UI.note(cn("正在获取新消息…"),"info",1)
            thread.start_new_thread(self.GetMsgAct,("newmsg",))
        elif choice==1:
            self.UI.note(cn("正在刷新收件箱…"),"info",1)
            thread.start_new_thread(self.GetMsgAct,("inbox",))
        elif choice==2:
            self.UI.note(cn("正在刷新发件箱…"),"info",1)
            thread.start_new_thread(self.GetMsgAct,("outbox",))

    def MsgSetMenuAct(self,type):
        if type=="set":
            self.E.ao_yield()
            choice=self.UI.popup_menu([cn("[关闭自动刷新]"),cn("[1分钟]"),cn("[5分钟]"),cn("[10分钟]"),cn("[15分钟]"),cn("[20分钟]"),cn("[30分钟]")],cn("消息自动刷新设置"))
            if choice==None:
                return
            elif choice==0:
                user.MSG_auto=0
                try:
                    user.MSG_keep.cancel()
                except:pass
                self.UI.note(cn("自动刷新消息已关闭！"),"info",1)
                return
            user.MSG_gaptime=[0,60,300,600,900,1200,1800][choice]
            user.MSG_auto=1
            try:
                user.MSG_keep.cancel()
            except:pass
        thread.start_new_thread(self.GetMsgAct,("newmsg",))
        user.MSG_keep.after(user.MSG_gaptime,lambda:self.MsgSetMenuAct("keep"))
        user.MSG_starttime=self.TM.clock()

    def GetMsgAct(self,type):
        self.SetDefaultAP()
        if type=="newmsg":
            try:
                result=self.http.getnewmessage()
            except:
                result="ERROR"
            if result in ("ERROR","E:630"):
                return
            if sets.new_msg=="0":
                file=open(self.path+"Tempfile\\newmsg.dat","w")
                file.write(en(result))
                file.close()
            else:
                file1=open(self.path+"Tempfile\\newmsg.dat","r")
                result=cn(file1.read())+"&&"+result
                file1.close()
                file2=open(self.path+"Tempfile\\newmsg.dat","w")
                file2.write(en(result))
                file2.close()
            Act=Analyse_MSG(result)
            Act.getmsglist("newmsg")
            sets.new_msg=str(Act.count)
            sets.save()
            del Act
            if sets.msg_voice=="on":
                self.Play_Sound()
            else:
                self.UI.note(cn("您有新的消息，请注意查收！"),"info",1)
        else:
            try:
                result=self.http.getmessagelist(type)
            except:
                result="ERROR"
            if result=="ERROR":
                self.UI.note(cn("获取消息失败，请稍候重试！"),"info",1)
                return
            file=open(self.path+"Tempfile\\%s.dat"%type,"w")
            file.write(en(result))
            file.close()
            if type=="inbox":
                self.UI.note(cn("收件箱已刷新，请查看！"),"info",1)
            elif type=="outbox":
                self.UI.note(cn("发件箱已刷新，请查看！"),"info",1)

    def OpenMsgBoxAct(self,type):
        file=open(self.path+"Tempfile\\%s.dat"%type,"r")
        cndata=cn(file.read())
        file.close()
        msgdic={"newmsg":cn("新消息"),"inbox":cn("收件箱"),"outbox":cn("发件箱")}
        Act=Analyse_MSG(cndata)
        self.listpg_list=Act.getmsglist(type)
        self.listpg_title=cn("%s(%s)")%(msgdic[type],str(len(self.listpg_list)))
        self.listpg_zjname=cn("查看")
        del cndata,Act,msgdic
        self.pre_page="main"
        self.page="msg_list"
        self.ListPG()

    def OpenBrowserAct(self,url):
        try:
            import openurl
        except:
            self.GBUI.global_msg_query(cn("您的PY平台缺少openurl模块，暂无法调用浏览器，请下载安装此模块或手动访问：\n%s")%url,cn("错误提示"))
            return
        try:
            openurl.open_ucweb(url)
        except:
            openurl.open_browser(url)
        del openurl

    def CheckUpdataAct(self):
        self.page="lianwang"
        self.MaskPG()
        self.InfoBoxPG(cn("检查更新"),cn("正在联网检查更新…请稍候！"))
        self.E.ao_yield()
        try:
            result=self.http.checkver()
            dat=result.split("&&")
            ver=float(dat[0])
            time=dat[1]
            self.downaddress=dat[2]
            text=dat[3]
        except:
            result="ERROR"
        if result=="ERROR":
            self.page="changelog"
            self.ChangelogPG()
            self.UI.note(cn("检查更新失败，请稍候重试！"))
            return
        if ver > 1.30:
            self.page="new_ver_minitext"
            self.minitextpg_title=cn("[发现新版本]")
            self.minitextpg_zjname=cn("下载")
            self.minitextpg_txt=tWrap(cn("[更新时间]：%s\n[新版特性]：\n%s")%(time,unquote(text)),int(self.x*0.85))
            self.MiniTextPG()
        else:
            self.page="changelog"
            self.ChangelogPG()
            self.UI.note(cn("当前版本是最新的啦！"),"info",1)

    def GetAnnounceAct(self):
        self.page="lianwang"
        self.MaskPG()
        self.InfoBoxPG(cn("获取公告"),cn("正在获取最新公告…请稍候！"))
        self.E.ao_yield()
        try:
            result=self.http.getannounce()
            result=cn("泡椒聊天-公告页面：\n——————————\n%s\n——————————\n[请按左键获取最新公告]")%unquote(result)
        except:
            result="ERROR"
        if result=="ERROR":
            self.page="announce"
            self.AnnouncePG()
            self.UI.note(cn("获取公告失败，请稍候重试！"))
            return
        file=open(self.path+"Data\\announce.txt","w")
        file.write(en(result))
        file.close()
        (self.announcetxt_shu,self.announcetxt_heng)=self.tWrapTXT(result)
        self.page="announce"
        self.AnnouncePG()

    def SendFBAct(self,name,content):
        self.SetDefaultAP()
        try:
            result=self.http.feedback(name,content)
        except:
            result="ERROR"
        if result=="OK!":
            self.UI.note(cn("您的反馈已成功发送！"),"info",1)
        else:
            self.UI.note(cn("您的反馈发送失败，请稍后重试！"),"info",1)

    def RefreshZoneAct(self):
        self.SetDefaultAP()
        try:
            result=self.http.login()
        except:
            result="ERROR"
        if result=="ERROR":
            self.UI.note(cn("刷新空间资料失败，请稍候重试！"),"info",1)
        else:
            file=open(self.path+"Tempfile\\myinfo.dat","w")
            file.write(en(result))
            file.close()
            user.set_zoneinfo()
            self.UI.note(cn("空间资料已刷新！"),"info",1)

    def GetMsgContentAct(self,msgid):
        try:
            result=self.http.getmessagecontent(msgid)
            msgdetail=[]
            for i in result.split("&"):
                i=i.split("=")
                if (i[0]=="authorid" or i[0]=="content"):
                    msgdetail.append(i[1])
            return msgdetail
        except: 
            return"ERROR"

    def SendMsgAct(self,uid,content):
        self.SetDefaultAP()
        try:
            result=self.http.sendmessage(uid,content)
        except:
            result="ERROR"
        if result=="OK!":
            self.UI.note(cn("消息已发送！"),"info",1)
        else:
            self.UI.note(cn("发送失败，请稍候重试！"),"info",1)

    def LoginingPG(self,step,note):
        #登录框范围
        self.img.polygon(rim(3,self.y-90,self.x-4,self.y-27,2),fill=0xdcf0fa)
        #分割线
        self.img.line((5,self.y-65,self.x-5,self.y-65),0xb6e5f7)
        self.img.line((5,self.y-64,self.x-5,self.y-64),0xffffff)
        #提示信息
        self.img.text((10,self.y-68),note,0x323232,(self.zt,16))
        #进度条
        self.img.polygon(rim(10,self.y-54,self.x-11,self.y-37,2),0x50b4e6)
        self.img.polygon(rim(11,self.y-53,11+(self.x-23)*step/5,self.y-38,2),fill=0x50b4e6)
        self.ctrlpanel("",cn("取消"),1)

    def LoginAct(self):
        if (self.ID=="" or self.PW==""):
            self.UI.note(cn("请同时输入帐号和密码！"),"info",1)
            return
        if sets.ap_id=="-1":
            self.UI.note(cn("请新设置接入点！"),"info",1)
            return
        self.MaskPG()
        self.page="lianwang"
        self.LoginingPG(1,cn("正在验证帐号、密码…"))
        self.E.ao_yield()
        try:
            self.E.ao_sleep(2)
            result=self.http.getrid(en(self.ID),en(self.PW))
        except:
            result="ERROR"
        if result=="ID OR PW ERROR":
            self.page="login_failed"
            self.InfoBoxPG(cn("登录失败"),cn("您输入的帐号或密码错误！"),yjname=cn("返回"))
            return
        elif result=="ERROR":
            self.page="login_failed"
            self.InfoBoxPG(cn("登录失败"),cn("接入点设置错误，请重新设置！"),yjname=cn("返回"))
            return
        sets.loginid=self.ID
        sets.loginpw=self.PW
        sets.rid=self.http.rid
        sets.save()
        self.E.ao_yield()
        self.LoginingPG(2,cn("正在获取个人资料…"))
        try:
            self.E.ao_sleep(2)
            result=self.http.login()
        except:
            result="ERROR"
        if result=="ERROR":
            self.page="login_failed"
            self.InfoBoxPG(cn("登录失败"),cn("获取个人资料失败，请稍后重试！"),yjname=cn("返回"))
            return
        else:
            file=open(self.path+"Tempfile\\myinfo.dat","w")
            file.write(en(result))
            file.close()
            user.set_zoneinfo()
        self.E.ao_yield()
        self.LoginingPG(3,cn("正在下载用户头像…"))
        try:
            data=self.http.gettximg(user.face)
            file=open(self.path+"Images\\tximgs\\mytximg.png","wb")
            file.write(data)
            file.close()
            user.set_tximg()
        except:
            user.set_tximg()
        self.E.ao_yield()
        self.LoginingPG(4,cn("正在刷新好友列表…"))
        try:
            self.E.ao_sleep(2)
            result="OK"
            result=self.http.getfriendlist()
        except:
            result="ERROR"
        if result=="ERROR":
            self.page="login_failed"
            self.InfoBoxPG(cn("登录失败"),cn("获取好友列表失败，请稍后重试！"),yjname=cn("返回"))
            return
        else:
            file=open(self.path+"Tempfile\\fndlist.dat","w")
            file.write(en(result))
            file.close()
            user.set_fndlist()
        self.LoginingPG(5,cn("登录成功，跳转中…"))
        self.E.ao_sleep(1)
        self.menu_list[0][2]=self.menu_list[1][2]=1
        self.tab=1
        self.pre_page="main"
        self.page="main"
        self.MainPG()
        user.MSG_auto=1
        user.MSG_gaptime=300
        self.E.ao_sleep(1,lambda:self.MsgSetMenuAct("keep"))
        if sets.online_auto=="on":
            user.OL_start=1
            user.OL_gaptime=1200
            self.E.ao_sleep(2,lambda:self.OnlineAct("keep"))

    def LogoutAct(self):
        try:
            user.OL_keep.cancel()
        except:pass
        try:
            user.MSG_keep.cancel()
        except:pass
        self.page="lianwang"
        self.InfoBoxPG(cn("注销"),cn("正在注销，请稍候…"))
        self.E.ao_sleep(1)
        self.menu_list[0][2]=self.menu_list[1][2]=0
        self.pre_page="loginpage"
        self.page="loginpage"
        self.LoginPage()

    def FndMenuAct(self,name,id):
        self.E.ao_yield()
        self.chat_uid=id
        self.chat_name=name
        self.chat_content=""
        choice=self.UI.popup_menu([cn("[发送消息]"),cn("[查看资料]")],name)
        if choice==None:
            return        
        elif choice==0:
            self.pre_page="main"
            self.page="chat"
            self.ChatPG()
        elif choice==1:
            self.E.ao_yield()
            self.MaskPG()
            self.page="lianwang"
            self.InfoBoxPG(cn("联网中…"),cn("正在获取好友资料，请稍候！"),yjname=cn("取消"))
            self.E.ao_yield()
            try:
                result=self.http.getfriendinfo(id)
                (self.fndzone_shu,self.fndzone_heng)=self.tWrapTXT(Analyse_FNDZONE(result).getzonetxt())
                self.pre_page="main"
                self.page="fndzone"
                self.FndZonePG()
            except:
                self.page="main"
                self.MainPG()
                self.UI.note(cn("获取好友资料失败，请稍候重试！"),"info",1)

    def BBSMenuAct(self):
        self.E.ao_yield()
        choice=self.UI.popup_menu([cn("[查看帖子]"),cn("[发表帖子]"),cn("[添加池塘]"),cn("[删除池塘(C)]"),cn("[修改池塘信息]")],sets.bbslist[self.bbs_index][0])
        if choice==None:
            return
        elif choice==0:
            self.E.ao_yield()
            self.MaskPG()
            self.page="lianwang"
            self.InfoBoxPG(cn("联网中…"),cn("正在获取池塘帖子，请稍候！"),yjname=cn("取消"))
            self.E.ao_yield()
            try:
                result=self.http.gettopiclist(sets.bbslist[self.bbs_index][1])
            except:
                result="ERROR"
            if result=="ERROR":
                self.UI.note(cn("获取帖子失败，请稍候重试！"),"info",1)
                self.page="main"
                self.MainPG()
                return
            elif result=="E:654":
                self.UI.note(cn("该池塘设置错误，请重新设置！"),"error",1)
                self.page="main"
                self.MainPG()
                return
            try:
                Act=Analyse_TOPIC(result)
                self.listpg_list=Act.gettopiclist()
                self.listpg_title=sets.bbslist[self.bbs_index][0]+cn("(%s贴)")%Act.topiccount[0]
                self.listpg_zjname=cn("选项")
                del result,Act
                self.pre_page="main"
                self.page="topic_list"
                self.ListPG()
            except:
                self.UI.note(cn("打开帖子未知错误！"),"error",1)
                self.page="main"
                self.MainPG()
                return
        elif choice==1:
            url="http://ct.paojiao.cn/topic.do?method=savetopic&id=%s&rid=%s"%(sets.bbslist[self.bbs_index][1],sets.rid)
            self.OpenBrowserAct(url)
        elif choice==2:
            self.E.ao_yield()
            ctname=self.UI.query(cn("请输入池塘名称："),"text")
            if ctname==None:return
            ctid=self.UI.query(cn("请输入池塘ID："),"number")
            if ctid==None:return
            ctid=str(ctid)
            if self.GBUI.global_msg_query(cn("池塘名称：%s\n池塘ID：%s")%(ctname,ctid),cn("添加新池塘确认:")):
                sets.bbslist.append([ctname,ctid,sets.bbsimg])
                sets.bbslistsave()
                self.MainPG()
                self.UI.note(cn("新池塘已添加！"),"conf",1)
        elif choice==3:
            if self.bbs_index<12:
                self.UI.note(cn("默认池塘不能删除！"),"info",1)
            else:
                if self.UI.query(cn("确认删除[%s]")%sets.bbslist[self.bbs_index][0],"query",1):
                    sets.bbslist.remove(sets.bbslist[self.bbs_index])
                    sets.bbslistsave()
                    self.bbs_index-=1
                    self.MainPG()
                    self.UI.note(cn("该池塘已删除！"),"conf",1)
        elif choice==4:
            if self.bbs_index<12:
                self.UI.note(cn("默认池塘不能修改！"),"info",1)
            else:
                ctname=self.UI.query(cn("请输入池塘新名称："),"text",sets.bbslist[self.bbs_index][0])
                if ctname==None:return
                ctid=self.UI.query(cn("请输入池塘新ID："),"number",int(sets.bbslist[self.bbs_index][1]))
                if ctid==None:return
                ctid=str(ctid)
                if self.GBUI.global_msg_query(cn("原池塘名称：%s\n原池塘ID：%s\n修改后池塘名称：%s\n修改后池塘ID：%s")%(sets.bbslist[self.bbs_index][0],sets.bbslist[self.bbs_index][1],ctname,ctid),cn("池塘修改确认：")):
                    sets.bbslist[self.bbs_index][0]=ctname
                    sets.bbslist[self.bbs_index][1]=ctid
                    sets.bbslistsave()
                    self.MainPG()
                    self.UI.note(cn("原池塘已修改！"),"conf",1)

    def TopicMenuAct(self):
        self.E.ao_yield()
        choice=self.UI.popup_menu([cn("[帖子详情]"),cn("[发表新贴]"),cn("[与楼主聊天]")],sets.bbslist[self.bbs_index][0])
        if choice==None:
            return
        elif choice==0:
            self.E.ao_yield()
            self.minitextpg_title=cn("[帖子详情]")
            self.minitextpg_zjname=cn("查看该贴")
            self.minitextpg_txt=tWrap(cn("标题：%s\n作者：%s")%(self.listpg_list[self.listpg_index][0],self.listpg_list[self.listpg_index][1]),int(self.x*0.85))
            self.MaskPG()
            self.pre_page="topic_list"
            self.page="topic_minitext"
            self.MiniTextPG()
        elif choice==1:
            url="http://ct.paojiao.cn/topic.do?method=savetopic&id=%s&rid=%s"%(sets.bbslist[self.bbs_index][1],sets.rid)
            self.OpenBrowserAct(url)
        elif choice==2:
            self.chat_name=self.listpg_list[self.listpg_index][3]
            self.chat_uid=self.listpg_list[self.listpg_index][4]
            self.pre_page="topic_list"
            self.page="chat"
            self.ChatPG()

    def Img_Resize(self,size):
        if self.img != None:
            (self.x,self.y)=self.c.size
            self.img=self.G.Image.new((self.x,self.y))
            if self.page=="main":
                self.MainPG()
            elif self.page=="loginpage":
                self.LoginPage()
            elif self.page=="help":
                self.HelpPG()
            elif self.page=="changelog":
                self.ChangelogPG()
            elif self.page=="announce":
                self.AnnouncePG()
            elif self.page=="fndzone":
                self.FndZonePG()
            elif self.page=="feedback":
                self.FeedBackPG()
            elif self.page=="chat":
                self.ChatPG()
            elif self.page in ("msg_list","topic_list"):
                self.ListPG()
            else:
                if self.page=="setaptype":
                    self.page="setap"
                self.right_key_press()

    def Img_Redraw(self,rect=None):
        if self.img != None:
            self.blit(self.img)

    def menu_press(self):
        if self.menu2=="off":
            if self.menu_list[self.menu1_index][1] != []:
                self.menu2="on"
                self.MenuPG()
            elif self.menu1_index==1:
                self.page="logout"
                self.img.blit(self.maskimg)
                self.InfoBoxPG(cn("注销"),cn("当前已登录,您确定要注销？"),cn("确定"),cn("取消"))
            elif self.menu1_index==4:
                self.page="exit"
                self.img.blit(self.maskimg)
                self.InfoBoxPG(cn("退出"),cn("您确定要退出[泡椒聊天]？"),cn("确定"),cn("取消"))
            else:pass
        elif self.menu2=="on":
            if self.menu1_index==0:
                self.tab=self.menu2_index
                self.right_key_press()
            elif self.menu1_index==2:
                if self.menu2_index==0:
                    self.E.ao_yield()
                    choice=self.UI.popup_menu([cn("[开启]"),cn("[关闭]")],cn("登录后自动挂机[%s]")%sets.online_auto)
                    if choice==None:
                        return
                    if choice==0:
                        sets.online_auto="on"
                        sets.save()
                        self.UI.note(cn("登录后自动挂机已开启！"),"info",1)
                    elif choice==1:
                        sets.online_auto="off"
                        sets.save()
                        self.UI.note(cn("登录后自动挂机已关闭！"),"info",1)
                elif self.menu2_index==1:
                    self.E.ao_yield()
                    choice=self.UI.popup_menu([cn("[开启]"),cn("[关闭]")],cn("新消息语音提醒[%s]")%sets.msg_voice)
                    if choice==None:
                        return
                    if choice==0:
                        sets.msg_voice="on"
                        sets.save()
                        self.UI.note(cn("新消息语音提醒已开启！"),"info",1)
                    elif choice==1:
                        sets.msg_voice="off"
                        sets.save()
                        self.UI.note(cn("新消息语音提醒已关闭！"),"info",1)
                elif self.menu2_index==2:
                    self.page="setap"
                    self.SetAccessPointPG()
            elif self.menu1_index==3:
                if self.menu2_index==0:
                    self.textpg_gdt=0
                    self.page="announce"
                    self.AnnouncePG()
                elif self.menu2_index==1:
                    self.textpg_gdt=0
                    self.page="changelog"
                    self.ChangelogPG()
                elif self.menu2_index==2:
                    self.page="feedback"
                    self.FeedBackPG()
                elif self.menu2_index==3:
                    self.textpg_gdt=0
                    self.page="help"
                    self.HelpPG()
                else:
                    self.OpenBrowserAct("http://pjcyun.sinaapp.com/jz.php")
        else:pass

    def mainpg_press(self):
        if self.tab==0:
            if self.zone_index==1:
                self.MaskPG()
                self.pre_page="main"
                self.page="sign_minitext"
                self.minitextpg_zjname=""
                self.minitextpg_title=cn("[我的签名]")
                self.minitextpg_txt=tWrap(user.sign,int(self.x*0.85))
                self.MiniTextPG()
            elif self.zone_index==2:
                if user.buddiescount=="0":
                    self.UI.note(cn("您暂无死党！"),"info",1)
                    return
                self.MaskPG()
                self.pre_page="main"
                self.page="sd_minilist"
                self.minilistpg_title=cn("[我的死党]：(%s个)")%user.buddiescount
                self.minilistpg_list=user.mybestfnds
                self.MiniListPG()
            elif self.zone_index==3:
                if user.guestcount=="0":
                    self.UI.note(cn("您暂无访客！"),"info",1)
                    return
                self.MaskPG()
                self.pre_page="main"
                self.page="fk_minilist"
                self.minilistpg_title=cn("[最近来访]：(%s个)")%user.guestcount
                self.minilistpg_list=user.visitors
                self.MiniListPG()
            elif self.zone_index==4:
                self.UI.note(cn("正在刷新空间资料…"),"info",1)
                thread.start_new_thread(self.RefreshZoneAct,())
            pass
        elif self.tab==1:
            if self.fnd_choice=="group":
                if user.fndlist[self.fndlist_index][3]=="off":
                    user.fndlist[self.fndlist_index][3]="open"
                    if user.fndlist[self.fndlist_index][4]==[]:
                        user.fndlist[self.fndlist_index][4]=user.fndact.getgroupdetail(user.fndlist[self.fndlist_index][2])
                    user.fndlist_len+=len(user.fndlist[self.fndlist_index][4])
                else:#"open"
                    user.fndlist[self.fndlist_index][3]="off"
                    user.fndlist_len-=len(user.fndlist[self.fndlist_index][4])
                self.FndlistPG()
            elif self.fnd_choice=="fnd":
                self.FndMenuAct(user.fndlist[self.fndlist_index][4][self.fnd_index][0],user.fndlist[self.fndlist_index][4][self.fnd_index][1])
        elif self.tab==2:
            self.BBSMenuAct()
        elif self.tab==3:
            if self.msgbox_index==0:
                if sets.new_msg != "0":
                    try:
                        self.OpenMsgBoxAct("newmsg")
                        sets.new_msg="0"
                    except:
                        self.UI.note(cn("打开新消息错误！"),"error",1)
                        sets.new_msg="0"
                else:
                    self.UI.note(cn("暂无新消息！"),"info",1)
            elif self.msgbox_index==1:
                try:
                    self.OpenMsgBoxAct("inbox")
                except:
                    self.UI.note(cn("正在刷新收件箱…"),"info",1)
                    thread.start_new_thread(self.GetMsgAct,("inbox",))
            elif self.msgbox_index==2:
                try:
                    self.OpenMsgBoxAct("outbox")
                except:
                    self.UI.note(cn("正在刷新发件箱…"),"info",1)
                    thread.start_new_thread(self.GetMsgAct,("outbox",))
            elif self.msgbox_index==3:
                self.MsgRefreshMenuAct()
            elif self.msgbox_index==4:
                self.MsgSetMenuAct("set")
                self.MainPG()
        elif self.tab==4:
            if self.olmenu_index==0:
                self.OnlineAct("start")
                self.MainPG()
            elif self.olmenu_index==1:
                self.OnlineAct("stop")
            else:
                self.E.ao_yield()
                choice=self.UI.popup_menu([cn("[开启]"),cn("[关闭]")],cn("登录后自动挂机[%s]")%sets.online_auto)
                if choice==None:
                    return
                if choice==0:
                    sets.online_auto="on"
                    sets.save()
                    self.UI.note(cn("登录后自动挂机已开启！"),"info",1)
                elif choice==1:
                    sets.online_auto="off"
                    sets.save()
                    self.UI.note(cn("登录后自动挂机已关闭！"),"info",1)

    def up_key_press(self):
        if self.page=="loginpage":
            self.loginpage_index-=1
            if self.loginpage_index<0:
                self.loginpage_index=2
            self.LoginPage()
        elif self.page=="main":
            if self.tab==0:
                self.zone_index-=1
                if self.zone_index<0:
                    self.zone_index=4
            elif self.tab==1:
                temp=self.fndlist_index-1
                if temp<0:
                    temp=len(user.fndlist)-1
                if self.fnd_choice=="group":
                    if user.fndlist[temp][3]=="off":
                        self.fndlist_index=temp
                    else:#"open"
                        if user.fndlist[temp][4]==[]:
                            self.fndlist_index=temp
                        else:
                            self.fnd_choice="fnd"
                            self.fndlist_index=temp
                            self.fnd_index=len(user.fndlist[temp][4])-1
                else:#"fnd"
                    self.fnd_index-=1
                    if self.fnd_index<0:
                        self.fnd_index=0
                        self.fnd_choice="group"
                self.fnd_all_index-=1
                self.fnd_all_pos-=1
                if self.fnd_all_pos<0:
                    self.fnd_all_pos=0
                if self.fnd_all_index<0:
                    self.fnd_all_index=user.fndlist_len-1
                    if user.fndlist_len>self.fnd_limit[self.x]:
                        self.fnd_all_pos=self.fnd_limit[self.x]-1
                    else:
                        self.fnd_all_pos=self.fnd_all_index
            elif self.tab==2:
                self.bbs_index-=1
                self.bbs_pos-=1
                if self.bbs_pos<0:
                    self.bbs_pos=0
                if self.bbs_index<0:
                    self.bbs_index=len(sets.bbslist)-1
                    if len(sets.bbslist)>self.bbs_limit[self.x]:
                        self.bbs_pos=self.bbs_limit[self.x]-1
                    else:
                        self.bbs_pos=self.bbs_index
            elif self.tab==3:
                self.msgbox_index-=1
                if self.msgbox_index<0:
                    self.msgbox_index=4
            elif self.tab==4:
                self.olmenu_index-=1
                if self.olmenu_index<0:
                    self.olmenu_index=2
            self.MainPG()
        elif self.page=="menu":
            if self.menu2=="off":
                self.menu1_index-=1
                if self.pre_page=="loginpage":
                    if self.menu1_index<2:
                        self.menu1_index=len(self.menu_list)-1
                elif self.pre_page=="main":
                    if self.menu1_index<0:
                        self.menu1_index=len(self.menu_list)-1
            elif self.menu2=="on":
                self.menu2_index-=1
                if self.menu2_index<0:
                    self.menu2_index=len(self.menu_list[self.menu1_index][1])-1
            self.MenuPG()
        elif self.page=="setap":
            self.setap_index-=1
            if self.setap_index<0:
                self.setap_index=len(self.access_point_list)-1
            self.SetAccessPointPG()
        elif self.page=="setaptype":
            self.setaptype_index-=1
            if self.setaptype_index<0:
                self.setaptype_index=1
            self.SetAPtypePG()
        elif self.page=="feedback":
            if self.fd_index==0:
                self.fd_index=1
            elif self.fd_index==1:
                self.fd_index=0
            self.FeedBackPG()
        elif self.page in ("sign_minitext","msg_minitext","topic_minitext","new_ver_minitext"):
            if len(self.minitextpg_txt)>5:
                self.minitextpg_gdt-=1
                if self.minitextpg_gdt<0:
                    self.minitextpg_gdt=0
                self.MiniTextPG()
            else:pass
        elif self.page in ("sd_minilist","fk_minilist"):
            self.minilistpg_index-=1
            if self.minilistpg_index<0:
                self.minilistpg_index=len(self.minilistpg_list)-1
            self.MiniListPG()
        elif self.page in ("msg_list","topic_list"):
            self.listpg_index-=1
            self.listpg_pos-=1
            if self.listpg_pos<0:
                self.listpg_pos=0
            if self.listpg_index<0:
                self.listpg_index=len(self.listpg_list)-1
                if len(self.listpg_list)>self.listpg_limit[self.x]:
                    self.listpg_pos=self.listpg_limit[self.x]-1
                else:
                    self.listpg_pos=self.listpg_index
            self.ListPG()
        elif self.page in ("help","changelog","announce","fndzone"):
            self.TextPG_up()
        else:pass

    def down_key_press(self):
        if self.page=="loginpage":
            self.loginpage_index+=1
            if self.loginpage_index>2:
                self.loginpage_index=0
            self.LoginPage()
        elif self.page=="main":
            if self.tab==0:
                self.zone_index+=1
                if self.zone_index>4:
                    self.zone_index=0
            elif self.tab==1:
                if user.fndlist[self.fndlist_index][3]=="off":
                    self.fndlist_index+=1
                else:#"open"
                    if self.fnd_choice=="group":
                        if user.fndlist[self.fndlist_index][4]==[]:
                            self.fndlist_index+=1
                        else:
                            self.fnd_choice="fnd"
                            self.fnd_index=0
                    else:#"fnd"
                        self.fnd_index+=1
                        if self.fnd_index>len(user.fndlist[self.fndlist_index][4])-1:
                            self.fnd_index=0
                            self.fndlist_index+=1
                            self.fnd_choice="group"
                if self.fndlist_index>len(user.fndlist)-1:
                    self.fndlist_index=0
                self.fnd_all_index+=1
                self.fnd_all_pos+=1
                if self.fnd_all_pos>self.fnd_limit[self.x]-1:
                    self.fnd_all_pos=self.fnd_limit[self.x]-1
                if self.fnd_all_index>user.fndlist_len-1:
                    self.fnd_all_index=0
                    self.fnd_all_pos=0
            elif self.tab==2:
                self.bbs_index+=1
                self.bbs_pos+=1
                if self.bbs_pos>self.bbs_limit[self.x]-1:
                    self.bbs_pos=self.bbs_limit[self.x]-1
                if self.bbs_index>len(sets.bbslist)-1:
                    self.bbs_index=0
                    self.bbs_pos=0
            elif self.tab==3:
                self.msgbox_index+=1
                if self.msgbox_index>4:
                    self.msgbox_index=0
            elif self.tab==4:
                self.olmenu_index+=1
                if self.olmenu_index>2:
                    self.olmenu_index=0
            self.MainPG()
        elif self.page=="menu":
            if self.menu2=="off":
                self.menu1_index+=1
                if self.menu1_index>len(self.menu_list)-1:
                    self.menu1_index=0
            elif self.menu2=="on":
                self.menu2_index+=1
                if self.menu2_index>len(self.menu_list[self.menu1_index][1])-1:
                    self.menu2_index=0
            self.MenuPG()
        elif self.page=="setap":
            self.setap_index+=1
            if self.setap_index>len(self.access_point_list)-1:
                self.setap_index=0
            self.SetAccessPointPG()
        elif self.page=="setaptype":
            self.setaptype_index+=1
            if self.setaptype_index>1:
                self.setaptype_index=0
            self.SetAPtypePG()
        elif self.page=="feedback":
            if self.fd_index==0:
                self.fd_index=1
            elif self.fd_index==1:
                self.fd_index=0
            self.FeedBackPG()
        elif self.page in ("sign_minitext","msg_minitext","topic_minitext","new_ver_minitext"):
            if len(self.minitextpg_txt)>5:
                self.minitextpg_gdt+=1
                if self.minitextpg_gdt>len(self.minitextpg_txt)-5:
                    self.minitextpg_gdt=len(self.minitextpg_txt)-5
                self.MiniTextPG()
            else:pass
        elif self.page in ("sd_minilist","fk_minilist"):
            self.minilistpg_index+=1
            if self.minilistpg_index>len(self.minilistpg_list)-1:
                self.minilistpg_index=0
            self.MiniListPG()
        elif self.page in ("msg_list","topic_list"):
            self.listpg_index+=1
            self.listpg_pos+=1
            if self.listpg_pos>self.listpg_limit[self.x]-1:
                self.listpg_pos=self.listpg_limit[self.x]-1
            if self.listpg_index>len(self.listpg_list)-1:
                self.listpg_index=0
                self.listpg_pos=0
            self.ListPG()
        elif self.page in ("help","changelog","announce","fndzone"):
            self.TextPG_down()
        else:pass

    def right_key_press(self):
        if self.page=="loginpage":
            self.LoginAct()
        elif self.page=="main":
            self.tab+=1
            if self.tab>4:self.tab=0
            self.MainPG()
        elif self.page=="setap":
            if sets.ap_id=="-1":
                self.UI.note(cn("必须先设置接入点！"),"info",1)
                return
            self.setap_index=0
            self.page=""
            self.right_key_press()
        elif self.page=="setaptype":
            self.page="setap"
            self.setaptype_index=0
            self.SetAccessPointPG()
        elif self.page=="lianwang":
            pass
        else:
            self.menu2="off"
            self.menu1_index=0
            self.menu2_index=0
            self.fd_index=0
            self.fd_name=""
            self.fd_content=""
            self.textpg_gdt=0
            self.textpg_run=0
            if self.pre_page=="loginpage":
                self.pre_page="loginpage"
                self.page="loginpage"
                self.LoginPage()
            elif self.pre_page=="main":
                self.listpg_index=0
                self.listpg_pos=0
                self.minitextpg_gdt=0
                self.minilistpg_index=0
                self.pre_page="main"
                self.page="main"
                self.MainPG()
            elif self.pre_page=="msg_list":
                self.minitextpg_gdt=0
                self.pre_page="main"
                self.page="msg_list"
                self.ListPG()
            elif self.pre_page=="fndzone":
                self.pre_page="main"
                self.page="fndzone"
                self.FndZonePG()
            elif self.pre_page=="topic_list":
                self.minitextpg_gdt=0
                self.pre_page="main"
                self.page="topic_list"
                self.ListPG()

    def Key_Event(self,key):
        tp=key["type"]
        ky=key["scancode"]
        #按下右键
        if ky==165 and tp==3:
            self.right_key_press()

        #按下左键、确定键
        elif (ky==164 or ky==167) and tp==3:
            #登录界面
            if self.page=="loginpage":
                if ky==164:#按下左键
                    self.pre_page="loginpage"
                    self.page="menu"
                    self.MaskPG()
                    self.MenuPG()
                elif ky==167:#按确定键
                    if self.loginpage_index==0:
                        self.E.ao_yield()
                        id=self.UI.query(cn("请输入帐号："),"text",self.ID)
                        if id:
                            self.ID=id
                            self.LoginPage()
                    elif self.loginpage_index==1:
                        self.E.ao_yield()
                        pw=self.UI.query(cn("请输入密码："),"code",self.PW)
                        if pw:
                            self.PW=pw
                            self.PW2=u"*" * len(self.PW)
                            self.LoginPage()
                    elif self.loginpage_index==2:
                        self.pre_page="loginpage"
                        self.page="setap"
                        self.MaskPG()
                        self.SetAccessPointPG()
            #主界面
            elif self.page=="main":
                if ky==164:#按下左键
                    self.pre_page="main"
                    self.page="menu"
                    self.MaskPG()
                    self.MenuPG()
                elif ky==167:#按确定键
                    self.mainpg_press()
            elif self.page=="menu":
                self.menu_press()
            elif self.page=="setap":
                if self.setap_index==0:
                    self.UI.note(cn("请选择接入点！"),"info",1)
                else:
                    self.page="setaptype"
                    self.SetAPtypePG()
            elif self.page=="setaptype":
                self.SK.set_default_access_point(None)
                a=self.access_point_dict[self.setap_index-1]["iapid"]
                ap=self.SK.access_point(a)
                self.SK.set_default_access_point(ap)
                self.pointname=self.access_point_dict[self.setap_index-1]["name"]
                sets.ap_id=str(a)
                sets.ap_pos=str(self.setap_index)
                sets.ap_type=str(self.setaptype_index)
                sets.save()
                self.http=HTTPs(int(sets.ap_type),sets.rid)
                self.page="setap"
                self.right_key_press()
                self.UI.note(cn("已设置接入点：\n[%s]")%self.pointname,"conf",1)
            elif self.page in ("sd_minilist","fk_minilist"):
                self.FndMenuAct(self.minilistpg_list[self.minilistpg_index][0],self.minilistpg_list[self.minilistpg_index][1])
            elif self.page=="changelog" and ky==164:
                self.CheckUpdataAct()
            elif self.page=="announce" and ky==164:
                self.GetAnnounceAct()
            elif self.page=="feedback":
                if ky==164:
                    if self.fd_content=="":
                        self.UI.note(cn("请输入反馈内容！"),"info",1)
                    else :
                        if self.fd_name=="":
                            nickname=cn("泡椒聊天v1.3用户")
                        else:
                            nickname=self.fd_name.replace("%","%25").replace("&","%26").replace("=","%3D").replace("|","%7C")
                        content=self.fd_content.replace("%","%25").replace("&","%26").replace("=","%3D").replace("|","%7C")
                        if self.GBUI.global_msg_query(cn("昵称：%s\n内容：%s")%(nickname,content),cn("确认发送")):
                            thread.start_new_thread(self.SendFBAct,(nickname,content))
                            self.fd_content=""
                            self.FeedBackPG()
                            self.UI.note(cn("正在发送您的反馈…"),"info",1)
                elif ky==167:
                    if self.fd_index==0:
                        self.E.ao_yield()
                        txt=self.UI.query(cn("请输入昵称："),"text",self.fd_name)
                        if txt:
                            self.fd_name=txt
                            self.FeedBackPG()
                    if self.fd_index==1:
                        self.E.ao_yield()
                        txt=self.UI.query(cn("请输入反馈内容："),"text",self.fd_content)
                        if txt:
                            self.fd_content=txt
                            self.FeedBackPG()
            elif self.page=="chat":
                if ky==164:
                    if self.chat_content=="":
                        self.UI.note(cn("请输入消息内容！"),"info",1)
                    else:
                        self.chat_content=self.chat_content.replace("%","%25").replace("&","%26").replace("=","%3D").replace("|","%7C")+cn("(通过泡椒聊天软件发送!)")
                        thread.start_new_thread(self.SendMsgAct,(self.chat_uid,self.chat_content))
                        self.chat_content=""
                        self.ChatPG()
                        self.UI.note(cn("正在发送消息…"),"info",1)
                elif ky==167:
                    self.E.ao_yield()
                    txt=self.UI.query(cn("请输入内容："),"text",self.chat_content)
                    if txt:
                        self.chat_content=txt
                        self.ChatPG()
            elif self.page=="fndzone":
                self.pre_page="fndzone"
                self.page="chat"
                self.ChatPG()
            elif self.page=="msg_list":
                #发件箱
                if self.msgbox_index==2:
                    self.minitextpg_zjname=""
                else:#收件箱、新消息
                    if self.listpg_list[self.listpg_index][2]=="":
                        self.page="lianwang"
                        self.MaskPG()
                        self.InfoBoxPG(cn("联网中…"),cn("正在获取该消息内容…"))
                        self.E.ao_yield()
                        try:
                            data=self.http.getmessagecontent(self.listpg_list[self.listpg_index][6])
                            data=data.split("&")
                            self.listpg_list[self.listpg_index][2]=data[1].split("=")[1]
                            self.listpg_list[self.listpg_index][3]=data[3].split("=")[1]
                        except:
                            self.page="msg_list"
                            self.ListPG()
                            self.UI.note(cn("获取该消息内容失败！"),"error",1)
                            return
                    self.minitextpg_zjname=cn("回复")
                if self.listpg_list[self.listpg_index][3]=="":#长文本为空
                    htxt=html2txt(self.listpg_list[self.listpg_index][1])+"\n"+self.listpg_list[self.listpg_index][4]
                else:
                    htxt=html2txt(self.listpg_list[self.listpg_index][3])+"\n"+self.listpg_list[self.listpg_index][4]
                self.minitextpg_txt=tWrap(htxt,int(self.x*0.85))
                self.minitextpg_title=self.listpg_list[self.listpg_index][0]
                self.MaskPG()
                self.pre_page="msg_list"
                self.page="msg_minitext"
                self.MiniTextPG()
            elif self.page=="msg_minitext":
                if ky==167:
                    return
                if self.msgbox_index==2:
                    return
                if self.listpg_list[self.listpg_index][5]=="user":
                    self.chat_name=self.listpg_list[self.listpg_index][0][7:]
                    self.chat_uid=self.listpg_list[self.listpg_index][2]
                    self.pre_page="msg_list"
                    self.page="chat"
                    self.ChatPG()
                else:
                    self.UI.note(cn("系统消息不能回复！"),"info",1)
            elif self.page=="topic_list":
                if ky==164:
                    self.TopicMenuAct()
                else:
                    self.minitextpg_title=cn("[帖子详情]")
                    self.minitextpg_zjname=cn("查看该贴")
                    self.minitextpg_txt=tWrap(cn("标题：%s\n作者：%s")%(self.listpg_list[self.listpg_index][0],self.listpg_list[self.listpg_index][1]),int(self.x*0.85))
                    self.MaskPG()
                    self.pre_page="topic_list"
                    self.page="topic_minitext"
                    self.MiniTextPG()
            elif self.page=="topic_minitext":
                if key==167:
                    return
                else:
                    url="http://ct.paojiao.cn/topic.do?method=topicdetail&topicid=%s&rid=%s"%(self.listpg_list[self.listpg_index][2],sets.rid)
                    self.OpenBrowserAct(url)
            elif self.page=="new_ver_minitext":
                self.OpenBrowserAct(self.downaddress)
            elif self.page=="logout":
                self.LogoutAct()
            elif self.page=="exit":
                self.ExitAct()

        #按上导航键
        elif ky==16 and tp==1:
            self.up_key_press()

        #按下导航键
        elif ky==17 and tp==1:
            self.down_key_press()

        #按右导航键
        elif ky==15 and tp==1:
            if self.page=="main":
                self.tab+=1
                if self.tab>4:self.tab=0
                self.MainPG()
            elif self.page=="menu":
                if self.menu_list[self.menu1_index][1] != []:
                    self.menu2="on"
                    self.MenuPG()
                else:pass
            else:pass

        #按左导航键
        elif ky==14 and tp==1:
            if self.page=="main":
                self.tab-=1
                if self.tab<0:self.tab=4
                self.MainPG()
            elif self.page=="menu":
                if self.menu2=="on":
                    self.menu2="off"
                    self.menu2_index=0
                    self.MenuPG()
                else:
                    self.right_key_press()
            else:pass

        #主界面按下#键查看公告
        elif ky==127 and tp==1:
            if self.page in ("main","loginpage"):
                self.page="announce"
                self.AnnouncePG()

        #主界面按下*键检查更新
        elif ky==42 and tp==1:
            if self.page in ("main","loginpage"):
                self.page="changelog"
                self.ChangelogPG()

        #主界面按下0键反馈
        elif ky==48 and tp==1:
            if self.page in ("main","loginpage"):
                self.page="feedback"
                self.FeedBackPG()

        #主界面按下8键帮助
        elif ky==56 and tp==1:
            if self.page in ("main","loginpage"):
                self.page="help"
                self.HelpPG()
        #删除键
        elif ky==1 and tp==1:
            if self.page=="main" and self.tab==2:
                if self.bbs_index<12:
                    self.UI.note(cn("默认池塘不能删除！"),"info",1)
                else:
                    if self.UI.query(cn("确认删除[%s]？")%sets.bbslist[self.bbs_index][0],"query",1):
                        sets.bbslist.remove(sets.bbslist[self.bbs_index])
                        sets.bbslistsave()
                        self.bbs_index-=1
                        self.MainPG()
                        self.UI.note(cn("该池塘已删除！"),"conf",1)

if __name__=="__main__":
    Run=MainPageUI()
    Run.StartApp()
    Run.lock.wait()