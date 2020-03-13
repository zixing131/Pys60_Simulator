# -*- coding: utf-8 -*-

#百度贴吧客户端登录界面（重写）by紫星
"""使用说明：假设本模块名称为dl.py，import dl后直接dl.main()即可调用登录界面
print dl.id可以打印出用户名
print dl.psw打印用户密码
dl.pnum变量为1时用手机号登录，为0时用户名登录（默认为0）
dl.rempsw变量为1时记住密码，为0时不记住密码（默认为1）
"""

cn=lambda x:x.decode("u8")
#引入模块
from sysinfo import display_pixels
import graphics as ph
import appuifw as ui
import appuifw2 as ui2
import e32
import txtfield as td
lock = e32.Ao_lock()
sleep=ui.e32.ao_sleep
zt=u"Sans MT 936_s60",15,1#默认字体

ui.app.screen="full"#定义屏幕全屏

class tbUi(object,):
    def __init__(self):
        pass

    def _redraw(self):  # 定义重绘函数
        can.blit(img)

    def redraw(self):
        img.clear(dl.bgcr)
        ima.clear(dl.inputcr)
        imb.clear(dl.oncr)
        imc.clear(dl.oncr)
        imd.clear(dl.oncr)
        """for i in range(25):
            imi=ph.Image.new((dl.w,1))
            imi.clear((i*10,i*10,i*10))
            img.blit(imi,target=(0,i))
        #画顶部边框
        """
        #下面是贴图到img
        if(dl.ping==1):
            img.blit(tietu,(-88,-25),mask=maska)#贴吧LOGO
            img.blit(ima,(-55,-112))#帐号输入框
            img.blit(ima,(-55,-153))#密码输入框
            if(dl.pnum==0):
                img.blit(gof,(-59,-199))#不用手机号登录
            elif(dl.pnum==1):
                img.blit(gon,(-59,-199))#用手机号登录
            if(dl.rempsw==0):
                img.blit(gof,(-59,-240))#不记密码
            elif(dl.rempsw==1):
                img.blit(gon,(-59,-240))#记住密码
            if(s_p==0 or s_p==1):
                img.blit(imd,(-55,-(113+41*s_p)))
                img.blit(imd,(-202,-(113+41*s_p)))
                img.blit(imb,(-55,-(112+41*s_p)))
                img.blit(imb,(-55,-(135+41*s_p)))#选择框
            else:
                img.blit(imd,(-55,-(113+41*s_p)))
                img.blit(imd,(-160,-(113+41*s_p)))
                img.blit(imc,(-55,-(112+41*s_p)))
                img.blit(imc,(-55,-(133+41*s_p)))#选择框
            img.text((62,132),id,0xf,zt)#帐号遮盖
            if(psw==cn("请输入密码")):
                img.text((62,173),psw,0xf,zt)#密码遮盖
            else:img.text((62,173),cn("********"),0xf,zt)
            #img.text((40,20), cn("百度贴吧客户端 v1.0"),0xf,zt)
            img.text((15,132), cn("帐号:"),0xf,zt)
            img.text((15,173), cn("密码:"),0xf,zt)
            img.text((10,310), cn("登录"),0xf,zt)
            img.text((195,310), cn("返回"),0xf,zt)
            img.text((80,214), cn("手机号登录"),0xf,zt)
            img.text((80,255), cn("记住密码"),0xf,zt)
        elif(dl.ping==2):
            img.blit(tietu,(-30,-55),mask=maska)#贴吧LOGO
            img.blit(ima,(-150,-60))#帐号输入框
            img.blit(ima,(-150,-100))#密码输入框
            if(dl.pnum==0):
                img.blit(gof,(-154,-144))#不用手机号登录
            elif(dl.pnum==1):
                img.blit(gon,(-154,-144))#用手机号登录
            if(dl.rempsw==0):
                img.blit(gof,(-154,-184))#不记密码
            elif(dl.rempsw==1):
                img.blit(gon,(-154,-184))#记住密码
            if(s_p==0 or s_p==1):
                img.blit(imd,(-150,-(60+40*s_p)))
                img.blit(imd,(-300,-(60+40*s_p)))
                img.blit(imb,(-150,-(60+40*s_p)))
                img.blit(imb,(-150,-(82+40*s_p)))#选择框
            else:
                img.blit(imd,(-150,-(60+40*s_p)))
                img.blit(imd,(-255,-(60+40*s_p)))
                img.blit(imc,(-150,-(60+40*s_p)))
                img.blit(imc,(-150,-(80+40*s_p)))#选择框
            img.text((158,80),id,0xf,zt)#帐号遮盖
            if(psw==cn("请输入密码")):
                img.text((158,120),psw,0xf,zt)#密码遮盖
            else:img.text((158,120),cn("********"),0xf,zt)
            #img.text((200,300), cn("百度贴吧客户端 v1.0"),0xf,zt)
            img.text((110,80), cn("帐号:"),0xf,zt)
            img.text((110,120), cn("密码:"),0xf,zt)
            img.text((10,230), cn("登录"),0xf,zt)
            img.text((280,230), cn("返回"),0xf,zt)
            img.text((175,158), cn("手机号登录"),0xf,zt)
            img.text((175,198), cn("记住密码"),0xf,zt)
        self._redraw()

    def move_u(self):  # 按键上
        global x, y, s_p, id, psw
        if (dl.kjzt != 0): dl.kjzt = 0
        if y < 90:
            x = 170
            y = 190
            s_p = 3
        else:
            x -= 41
            y -= 41
            s_p -= 1
        if (id != cn("请输入帐号")):
            id = kj1.get()
        elif (psw != cn("请输入密码")):
            psw = kj2.get()
        kj1.visible(0)
        kj1.focus(0)
        kj2.visible(0)
        kj2.focus(0)

    def move_d(self):  # 按键下
        global x, y, s_p, id, psw
        if (dl.kjzt != 0): dl.kjzt = 0
        if y > 160:
            x = 50
            y = 50
            s_p = 0
        else:
            x += 41
            y += 41
            s_p += 1
        if (id != cn("请输入帐号")):
            id = kj1.get()
        elif (psw != cn("请输入密码")):
            psw = kj2.get()
        kj1.visible(0)
        kj1.focus(0)
        kj2.visible(0)
        kj2.focus(0)
        self.redraw()

    def enter(self):  # 按键确认
        global id, psw
        if (s_p == 0):
            if (dl.kjzt == 0):
                dl.kjzt = 1
            else:
                dl.kjzt = 0
            if (dl.kjzt == 0):
                id = kj1.get()
                kj1.visible(0)
                kj1.focus(0)
                kj2.visible(0)
                kj2.focus(0)
            elif (dl.kjzt == 1):
                id = kj1.get()
                kj1.visible(1)
                kj1.focus(1)
            elif (dl.kjzt == 2):
                psw = kj2.get()
                kj2.visible(1)
                kj2.focus(1)
        elif (s_p == 1):
            if (dl.kjzt == 0):
                dl.kjzt = 2
            else:
                dl.kjzt = 0
            if (dl.kjzt == 0):
                id = kj1.get()
                kj1.visible(0)
                kj1.focus(0)
                kj2.visible(0)
                kj2.focus(0)
            elif (dl.kjzt == 1):
                id = kj1.get()
                kj1.visible(1)
                kj1.focus(1)
            elif (dl.kjzt == 2):
                psw = kj2.get()
                kj2.visible(1)
                kj2.focus(1)
        elif s_p == 2:
            if (dl.pnum == 0):
                dl.pnum = 1
            elif (dl.pnum == 1):
                dl.pnum = 0
        elif s_p == 3:
            if (dl.rempsw == 0):
                dl.rempsw = 1
            elif (dl.rempsw == 1):
                dl.rempsw = 0
        self.redraw()

    def fan(self):  # 定义返回键动作
        ui.note(cn("在这里定义返回键东西"))
        self.redraw()

    def denglu(self):  # 定义登录键动作
        ui.note(cn("在这里定义登录键键东西"))
        self.redraw()

    def main(self):
        global id, psw

        can.bind(63498, lambda: self.move_d())
        can.bind(63497, lambda: self.move_u())
        can.bind(63557, lambda: self.enter())
        can.bind(63554, lambda: self.denglu())
        can.bind(63555, lambda: self.fan())
        self.redraw()


class dl:pass
dl.version="V1.0"
dl.w=display_pixels()[0]#屏宽
dl.h=display_pixels()[1]#屏高
dl.bgcr=(100,200,200)#背景颜色
dl.inputcr=(145,125,238)#输入框颜色
dl.oncr=(255,100,100)#选择框颜色
dl.kjcr=0x995599#控件颜色
dl.pnum=0#手机号登录状态
dl.rempsw=1#记住密码状态
dl.kjzt=0#控件状态
dl.dong=1#移动状态
dl.ping=0
#判断横竖屏
if(display_pixels()==(240,320)):
    dl.ping=1#竖屏
elif(display_pixels()==(320,240)):
    dl.ping=2#横屏

#dl.ping=2#测试横竖屏

if(dl.ping==1):
    img=ph.Image.new((240,320))
    dl.kjwz1=(57,113,203,137)#控件1位置
    dl.kjwz2=(57,154,203,178)#控件2位置
else:
    img=ph.Image.new((320,240))
    dl.kjwz1=(152,61,301,84)#控件1位置
    dl.kjwz2=(152,101,301,124)#控件2位置
ima=ph.Image.new((150,25))#输入框架
imb=ph.Image.new((150,3))#选择框横着1
imc=ph.Image.new((107,3))#选择框横着2
imd=ph.Image.new((3,25))#选择框竖着1
imd=ph.Image.new((3,23))#选择框竖着2
tietu=ph.Image.open(u"..\\python\\pysoft\\tieba\\tie.png")#贴吧LOGO图标
maska=ph.Image.new((72,72),"1")
maska.load("..\\python\\pysoft\\tieba\\zhe.png")#遮罩
gon=ph.Image.open(u"..\\python\\pysoft\\tieba\\gon.png")
gof=ph.Image.open(u"..\\python\\pysoft\\tieba\\gof.png")

kj1=td.New(dl.kjwz1,cornertype=td.ECorner2,strlimit=1)#新建文本控件1
kj2=td.New(dl.kjwz2,cornertype=td.ECorner2,txtlimit=16)#新建文本控件2
kj1.bgcolor(dl.kjcr)#控件1颜色
kj2.bgcolor(dl.kjcr)#控件2颜色
kj1.textstyle(u"Sans MT 936_s60",15*10,0xf,u'normal')#控件2字体
kj2.textstyle(u"Sans MT 936_s60",15*10,0xf,u'normal')#控件2字体
kj1.visible(0)
kj2.visible(0)#可视为假

x,y,s_p=50,69,0
id=cn("请输入帐号")
psw=cn("请输入密码")

tbui= tbUi()


ui.app.body=can=ui.Canvas(event_callback=None, redraw_callback=tbui.redraw)

tbui.main()

ui.app.exit_key_handler = lock.signal
lock.wait()
