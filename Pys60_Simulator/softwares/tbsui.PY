# -*- coding: utf-8 -*-
#贴吧签到UI模块、
#版本：v2.0
#软件作者：Light.紫.星
#塞班S60V3吧吧群:140369358
VER="2.0"
import base64,os
import dialog, appuifw as ui
import tbsnet
import e32
tbsnet= tbsnet.tiebanet
sleep=  e32.ao_sleep
path="c:\\python\\pysoft\\tbs\\"
cn=lambda x:unicode(x,"utf-8","ignore")
en=lambda x:x.encode("utf-8")
def encrypt(x):return base64.encodestring(x)
def decrypt(x):return base64.decodestring(x)
def isphone(s):
    try:
        if(len(str(long(s)))==11) and str(s)[:3] in ['130','131','132','133','134','135','136','137','138','139','150','151','152','153','156','158','159','170','183','182','185','186','188','189']:
            return 1
        return 0
    except:return 0
class set:
    def prepath(s,p):
        t=p.split("\\");head=t[0]
        for i in range(1,len(t)):
            try:head+="\\"+t[i];os.mkdir(head)
            except:pass
    def checkset(s):
        try:
            a=open(path+"zh.png","r")
        except:
            while 1:
                t=ui.query(cn("没有帐号记录请设置百度帐号"),"text")
                if t!=None:break
                ui.note(cn("帐号输入有误！"),"error")
            open(path+"zh.png","w").write(encrypt(en(t)))
        s.un=decrypt(open(path+"zh.png").read())
        try:
            a=open(path+"pa.png","r")
        except:
            while 1:
                t=ui.query(cn("没有密码记录请设置帐号密码"),"code")
                if t!=None:break
                ui.note(cn("密码输入有误！"),"error")
            open(path+"pa.png","w").write(encrypt(en(t)))
        s.psw=decrypt(open(path+"pa.png").read())
    def reset(s):
        while 1:
            t=ui.query(cn("请设置百度帐号"),"text")
            if t!=None:break
            ui.note(cn("帐号输入有误！"),"error")
        open(path+"zh.png","w").write(encrypt(en(t)))
        s.un=decrypt(open(path+"zh.png","r").read())
        while 1:
            t=ui.query(cn("请设置密码"),"code")
            if t!=None:break
            ui.note(cn("密码输入有误！"),"error")
        open(path+"pa.png","w").write(encrypt(en(t)))
        s.psw=decrypt(open(path+"pa.png","r").read())
        ui.note(cn("设置完成！"),"conf")
    def setauto(s,t):
        open(path+"auto.ini","w").write(str(t))
        ui.note(cn("设置完成！"),"conf")
    def addbar(s):
        if(len(s.tblist)==1 and s.tblist[0]==cn("没有添加贴吧！")):s.oldlist=[]
        else:s.oldlist=s.tblist
        def review(list,n):
            s.listbox.set_list(list,n)
        def reload(list):
            ui.app.body=s.listbox=ui.Listbox(list,press)
        def press():
            index=s.listbox.current()
            if(len(s.tblist)==1 and s.tblist[0]==cn("请先刷新列表(需联网)！")):return
            if(s.tblist[index][0]==cn("√")):
                s.tblist[index]=s.tblist[index][2:]
                s.oldlist.remove(s.tblist[index])
            else:
                if(s.tblist[index] in s.oldlist):pass
                else:s.oldlist.append(s.tblist[index])
                s.tblist[index]=cn("√ "+en(s.tblist[index]))
            review(s.tblist,index)
        def all():
            index=s.listbox.current()
            if(len(s.tblist)==1 and s.tblist[0]==cn("请先刷新列表(需联网)！")):
                ui.note(cn("本地无爱贴吧记录！请刷新列表后重试！"))
                return
            else:
                for i in range(len(s.tblist)):
                    if(s.tblist[i][0]==cn("√")):
                        if(s.tblist[i][2:] in s.oldlist):pass
                        else:s.oldlist.append(s.tblist[i][2:])
                    else:
                        if(s.tblist[i] in s.oldlist):pass
                        else:s.oldlist.append(s.tblist[i])
                        s.tblist[i]=cn("√ "+en(s.tblist[i]))
                review(s.tblist,index)
        def clear():
            index=s.listbox.current()
            for i in range(len(s.tblist)):
                if(s.tblist[i][0]==cn("√")):
                    s.oldlist.remove(s.tblist[i][2:])
                    s.tblist[i]=s.tblist[i][2:]
            review(s.tblist,index)
        #def turn():
            #pass
        def f5():
            wait= dialog.Wait(cn("正在刷新列表！"))
            wait.show()
            try:
                s.cookie=open(path+"cookie.ini").read()
                s.tbnet.BDUSS=s.cookie
            except:
                t=s.getcookie()
                if t=="error":
                    wait.close()
                    return
                wait.set_label(cn("正在刷新列表！"))
            if 1:
                s.tblist=[]
                tmp=s.tbnet.getUserLikedForum()
                tmp=tmp["forum_list"]
                for i in range(len(tmp)):
                    s.tblist.append(cn(en(s.tbnet.uto(tmp[i]["name"]))))
                open(path+"allbar.txt","w").write(str(s.tblist))
                ui.note(cn("获取完成！共获取"+str(len(s.tblist))+"个喜欢的贴吧！"))
            else:
                ui.note(cn("获取喜欢的吧失败！请检查帐号密码是否正确！"))
            wait.close()
            for i in range(len(s.tblist)):
                if(s.tblist[i] in s.oldlist):
                    s.tblist[i]=cn("√ "+en(s.tblist[i]))
            reload(s.tblist)
        def done():
            if(ui.query(cn("确认返回？"),"query")):
                if s.oldlist==[]:s.tblist=[cn("没有添加贴吧！")]
                else:s.tblist=s.oldlist
                s.changelist()
        try:
            s.tblist=eval(open(path+"allbar.txt").read())
        except:
            s.tblist=[cn("请先刷新列表(需联网)！")]
        for i in range(len(s.tblist)):
            if(s.tblist[i] in s.oldlist):
                s.tblist[i]=cn("√ "+en(s.tblist[i]))
        reload(s.tblist)
        ui.app.menu=[
            (cn("全部选择"),all),
            (cn("清除全部"),clear),
            #(cn("全部反选"),turn),
            (cn("刷新列表"),f5),
            (cn("完成"),done)
            ]
        ui.app.exit_key_handler=done
    def exit(s):
        if ui.query(cn("确定退出？"),"query"):
            #ui.note(cn("自己结束进程！"))
            ui.app.set_exit()
    def study(s):
        def tmp():
            sleep(0.3)
            if(ui.query(cn("接下来我们将引导您如何使用本软件！"),"query")):pass
            else:return 0
            sleep(0.3)
            if(ui.query(cn("您需添加要一键签到的吧,也可以选择官方一键签到和选择签到来进行其他签到,Now,请添加贴吧！"),"query")):pass
            else:return 0
            sleep(0.3)
            ui.note(cn("请添加需要签到的贴吧！"))
        if(tmp()==0):
            ui.note(cn("用户终止操作！"))
            return 0
        s.changelist(help=1)
    def about(s):
        s.x.color=(0x1111ee)
        s.x.set(cn("\n百度贴吧签到工具v"+VER+" by Light.紫.星\n\n塞班S60V3吧吧群:140369358\n\n软件说明：本版本为全新开发的塞班S60V3百度贴吧签到工具，使用百度贴吧iPhone客户端的接口进行签到，本版本酝酿已久，测试中未出现之前版本中普遍存在的网络问题，本版本网络模块为单独模块，如果你有能力更新或优化本软件，请与本人联系，联系方式:加入塞班S60V3吧吧群，然后私聊Light.紫.星进行讨论交流。本版本具体使用方法在阁下可以查看帮助里的使用说明，如有疑问欢迎加入塞班S60V3吧吧群参与讨论。"))
        s.x.set_pos(0)
class sign(set):
    def __init__(s):
        s.tblist=None
        s.prepath(path)
        s.checkset()
        s.tbnet=tbsnet(en(cn(s.un)),s.psw,isphone(s.un))
        s.main()
    def main(s):
        s.inlist=0
        ui.app.menu=[
            (cn("一键签到"),s.fastsign),
            (cn("辅助签到"),((cn("官方接口"),s.msign),(cn("精确签到"),s.selectsign))),
            (cn("设置"),((cn("添加贴吧"),s.changelist),(cn("设置帐号"),s.reset),(cn("重获cookie"),s.getcookie))),
            (cn("自动签到"),((cn("开启"),lambda:s.setauto(1)),(cn("关闭"),lambda:s.setauto(0)))),
            ((cn("帮助关于")),((cn("软件说明"),s.about),(cn("使用教程"),s.study))),
            (cn("退出程序"),s.exit)]
        ui.app.body=s.x=ui.Text()
        s.x.color=(0)
        s.x.set(cn("\n\n\t贴吧签到 v"+VER+"\n    \t\tby Light.紫.星\n"))
        ui.app.title=cn("贴吧签到")
        ui.app.exit_key_handler=s.exit
        try:
            isauto=open(path+"auto.ini").read()
        except:
            open(path+"auto.ini","w").write("0")
            isauto=open(path
            +"auto.ini").read()
        if(isauto=="0"):pass
        else:s.autosign()
    def autosign(s):
        s.x.set(cn("开始自动签到中……\n"))
        ui.note(cn("您已设置了启动软件后自动签到！"))
        s.fastsign()
        ui.note(cn("全部签到完成！3秒钟后自动退出！"))
        sleep(3)
        #ui.note(cn("自己退出吧、"))
        ui.app.set_exit()
    def fastsign(s):
        s.x.set(cn("正在进行一键签到！\n"))
        sleep(0.2)
        s.x.add(cn("正在获取cookie…\n"))
        sleep(0.1)
        try:
            sleep(0.1)
            s.cookie=open(path+"cookie.ini").read()
            s.tbnet.BDUSS=s.cookie
            s.x.add(cn("已经从本地获取cookie！\n"))
            sleep(0.1)
        except:
            s.x.add(cn("本地无cookie记录，正在联网获取！\n"))
            sleep(0.1)
            t=s.getcookie()
            if t=="error":
                return
            s.x.add(cn("从网络获取cookie成功！\n"))
            sleep(0.1)
        s.x.add(cn("正在获取签到列表…\n"))
        try:
           s.tblist=eval(open(path+"tblist.txt").read())
        except:
            s.study()
        s.tblist=eval(open(path+"tblist.txt").read())
        s.x.color=((0,0,255))
        s.x.add(cn("共获取到"+str(len(s.tblist))+"个需要签到的吧\n"))
        success=0
        s.tbnet.gettbs()
        for i in s.tblist:
            sleep(1.5)
            try:
                tdata=s.tbnet.tsign(en(cn(en(s.tbnet.uto(i)))))
                if(tdata["error_code"]=="160002"):
                    s.x.color=((0,150,0))
                    s.x.add(cn(en(i)+" 吧已经签到过了！\n"))
                    success+=1
                    s.x.color=(0)
                elif(tdata["error_code"]=="0"):
                    s.x.color=((0,140,0))
                    s.x.add(cn(en(i)+" 吧签到成功！\n"))
                    success+=1
                    s.x.color=(0)
                else:
                    try:
                        s.x.color=((255,0,0))
                        s.x.add(i+cn("吧："))
                        s.x.add(s.tbnet.uto(tdata["error_msg"])+u"\n")
                        s.x.color=(0)
                    except:
                        s.x.color=((255,0,0))
                        s.x.add(cn(en(i)+" 吧签到时出现未知错误,可能是cookie问题！\n"))
                        s.x.color=(0)
            except:
                s.x.color=((255,0,0))
                s.x.add(cn(en(i)+" 吧签到时发生未知错误！可能为网络环境问题或cookie问题！\n"))
                s.x.color=(0)
                
        s.x.color=(0)
        s.x.add(cn("签到完成！共签到成功"))
        s.x.color=((250,0,0))
        s.x.add(cn(str(success)))
        s.x.color=(0)
        s.x.add(cn("个吧！"))
    def selectsign(s):
        s.x.set(cn("正在进行精确签到！\n"))
        sleep(0.2)
        while 1:
            tb=ui.query(cn("请输入要签到的贴吧名称"),"text",cn("塞班s60v3"))
            if tb!=None:
                break
            ui.note(cn("请输入正确数据！"))
        s.x.add(cn("正在获取cookie…\n"))
        sleep(0.1)
        try:
            s.cookie=open(path+"cookie.ini").read()
            s.tbnet.BDUSS=s.cookie
            s.x.add(cn("已经从本地获取cookie！\n"))
            sleep(0.1)
        except:
            s.x.add(cn("本地无cookie记录，正在联网获取！\n"))
            sleep(0.1)
            t=s.getcookie()
            if t=="error":
                return
            s.x.add(cn("从网络获取cookie成功！\n"))
            sleep(0.1)
        
        i=tb
        try:
            s.tbnet.gettbs()
            tdata=s.tbnet.tsign(en(i))
            if(tdata["error_code"]=="160002"):
                s.x.color=((0,150,0))
                s.x.add(cn(en(i)+" 吧已经签到过了！\n"))
                s.x.color=(0)
            elif(tdata["error_code"]=="0"):
                s.x.color=((0,140,0))
                s.x.add(cn(en(i)+" 吧签到成功！\n"))
                s.x.color=(0)
            else:
                try:
                    s.x.color=((255,0,0))
                    s.x.add(i+cn("吧："))
                    s.x.add(s.tbnet.uto(tdata["error_msg"])+u"\n")
                    s.x.color=(0)
                except:
                    s.x.color=((255,0,0))
                    s.x.add(cn(en(i)+" 吧签到时出现未知错误,可能是cookie问题！\n"))
                    s.x.color=(0)
        except:
            s.x.color=((255,0,0))
            s.x.add(cn(en(i)+" 吧签到时发生未知错误！可能为网络环境问题或cookie问题！\n"))
            s.x.color=(0)
        s.x.add(cn("精确签到完成！\n"))
    def changelist(s,help=0):
        def review(list,n):
            s.listbox.set_list(list,n)
        def reload(list):
            ui.app.body=s.listbox=ui.Listbox(list,press)
        def runhelp():
            help=0
            sleep(0.3)
            if(ui.query(cn("恭喜您添加完成！是否立即进行签到？"),"query")):
                s.fastsign()
            else:
                sleep(0.3)
                ui.note(cn("引导教程结束！"),"conf")
        def press():
            index=s.listbox.current()
            if(s.tblist[index]==cn("没有添加贴吧！") and len(s.tblist)==1):
                ui.note(cn("没有任何贴吧！"))
            else:
                if(ui.query(cn("是否删除"+en(s.tblist[index])+"吧？"),"query")):
                    s.tblist.remove(s.tblist[index])
                    if(len(s.tblist)==0):
                        s.tblist=[cn("没有添加贴吧！")]
            review(s.tblist,index)
        def clearlist():
            s.tblist=[cn("没有添加贴吧！")]
            reload(s.tblist)
        def addtb(x=0):
            index=s.listbox.current()
            if x==0:
                if(ui.query(cn("是否保存列表？"),"query")):
                    savelist()
                s.addbar()
            elif x==1:
                while 1:
                    tb=ui.query(cn("请输入贴吧名称"),"text",cn("塞班s60v3"))
                    if tb!=None:
                        break
                    ui.note(cn("好歹点一下确定啊！"))
                if(len(s.tblist)==1 and s.tblist[0]==cn("没有添加贴吧！")):
                    s.tblist=[]
                    s.tblist.append(tb)
                elif(tb in s.tblist):
                    ui.note(cn("列表中已存在此贴吧！"),"error")
                else:
                    s.tblist.append(tb)
            review(s.tblist,index)
        def savelist():
            try:
                open(path+"tblist.txt","w").write(str(s.tblist))
                ui.note(cn("保存成功！"),"conf")
            except:
                ui.note(cn("保存成功！"),"error")
            if(help==1):
                runhelp()
                return 0
        def back():
            if(ui.query(cn("是否保存列表？"),"query")):
                savelist()
            else:
                ui.note(cn("列表未保存！"))
            s.main()
            if(help==1):
                runhelp()
                return 0
        if(s.tblist==None):
            try:s.tblist=eval(open(path+"tblist.txt").read())
            except:s.tblist=[cn("没有添加贴吧！")]
        reload(s.tblist)
        ui.app.menu=[
            (cn("添加贴吧"),((cn("从爱贴吧导入"),lambda:addtb(0)),(cn("输入贴吧名称"),lambda:addtb(1)))),
            (cn("删除贴吧"),press),
            (cn("清空列表"),clearlist),
            (cn("保存列表"),savelist),
            (cn("返回主页"),back)
            ]
        ui.app.exit_key_handler=back
    def getcookie(s):
        wait= dialog.Wait(cn("正在获取cookie！"))
        wait.show()
        t=s.tbnet.login()
        if t!="success":
            return "error"
        s.cookie=s.tbnet.BDUSS
        if(ui.query(cn("是否保存cookie？"),"query")):
            open(path+"cookie.ini","w").write(s.cookie)
            ui.note(cn("cookie保存成功！"))
            wait.close()
    def msign(s):
        s.x.set(cn("正在调用官方一键签到接口进行签到！\n"))
        s.x.add(cn("正在获取cookie…\n"))
        sleep(0.2)
        try:
            sleep(0.1)
            s.cookie=open(path+"cookie.ini").read()
            s.tbnet.BDUSS=s.cookie
            s.x.add(cn("已经从本地获取cookie！\n"))
            sleep(0.1)
        except:
            s.x.add(cn("本地无cookie记录，正在联网获取！\n"))
            sleep(0.1)
            t=s.getcookie()
            if t=="error":
                return
            s.x.add(cn("从网络获取cookie成功！\n"))
            sleep(0.1)
        s.x.add(cn("正在获取一键签到列表(获取速度视网络环境而异)…\n"))
        sleep(0.2)
        try:
            foruminfo=s.tbnet.getforumlist()["forum_info"]
        except:
            ui.note(cn("获取不到可官方一键签到的贴吧！请检查帐号设置并确保有符合条件的贴吧！"))
            s.main()
            return
        forum_ids=[]
        havesign=0
        for i in foruminfo:
            if(str(i["is_sign_in"])=="0"):
                forum_ids.append(i["forum_id"])
            else:
                havesign+=1
                s.x.color=((0,150,0))
                s.x.add(s.tbnet.uto(i["forum_name"])+cn("已经签过到\n"))
                sleep(0.1)
                s.x.color=(0)
        s.tbnet.gettbs()
        msig=s.tbnet.msign(",".join(forum_ids))
        if(str(msig["show_dialog"])=="0"):
            s.x.color=((0,0,255))
            s.x.add(cn("官方一键签到完成，共签到了"+str(len(forum_ids))+"个吧！("+str(havesign)+"个吧已经签到过)\n"))
            s.x.color=(0)
        else:
            s.x.color=((255,0,0))
            s.x.add(s.tbnet.uto(msig["error"]["usermsg"]))
            s.x.color=(0)

sign=sign()



#print u"ui loaded ok!"
