# -*- coding: utf-8 -*-
#贴吧网络模块、
#版本：测试版
#软件作者：Light.紫.星
#塞班S60V3吧吧群:140369358
#VER="0.99"
import httplib,urllib,socket,base64,md5,time
import graphics, appuifw as ui, TopWindow
from sysinfo import imei
from sysinfo import display_pixels
unquote=urllib.unquote
cn=lambda x:x.decode('u8')
en=lambda x:x.encode('u8')
import  e32
sleep=  e32.ao_sleep
def showyzm(path):
    global top
    img= graphics.Image.open(path)
    top= TopWindow.TopWindow()
    top.add_image(img, (0,0))
    top.corner_type="corner5"
    top.shadow=2
    top.position=(50,5)
    top.size=(img.size[0],img.size[1])
    top.show()
    while 1:
        try:
            vcode=en(ui.query(cn("请输入验证码"),"text"))
            #print cn(vcode),len(cn(vcode))
            if(len(cn(vcode))!=4):
                ui.note(cn("输入有误！"))
            else:
                del top
                #print cn(vcode)
                return vcode
        except:
            pass
def getip(x):
    x=str(x)
    all=socket.access_points()
    for i in range(len(all)):
        iapid=all[i]["iapid"]
        pname=all[i]["name"]
        socket.set_default_access_point(socket.access_point(iapid))
        try:
            ip=socket.gethostbyname(x)
        except:
            continue
        if ip.find("*")>-1:
            continue
        else:
            break
    #print ip
    return ip
def post(url,pj={"":""}):
    UA="Dalvik/1.2.0 (Linux; U; Android 2.2; sdk Build/FRF91)"
    try:
        host=(lambda(url):((url[:7]=="http://")and(url[7:].find("/")!=-1 and url[7:][:url[7:].find("/")] or url[7:])or(url.find("/")!=-1 and url[:url.find("/")] or url)))(url)
        url=(lambda(x):(url[:7]=="http://" and x or "http://"+x))(url)
        ip=getip(host)
        conn=httplib.HTTPConnection(ip,80)
        try:
            data=urllib.urlencode(pj)
        except:
            data=pj
        header={'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain','User-Agent':UA}
        conn.request("POST",url,data,header)
        dat=conn.getresponse().read().replace("&amp;","&")
        conn.close()
        return dat
    except:
        return "None"

class tiebanet:
    def __init__(s,un,psw,isp):
        s.imei=imei()
        s.pix=display_pixels()
        #以下为测试数据
        s.BDUSS="None"
        s.psw=base64.encodestring(psw.encode('utf8')).replace(u"\n","").replace(u"=","")
        s.un=un
        s.isp=isp
        s.token="fb13bad79b3a1fefc0a5819a0b66eaa3e064a3bdf020f7f453a8ef905fd51aef"
        #s.client_id=s.getsync()
        s.client_id="wappc_1426215240046_404"
        #print s.client_id
    def _md5(s,data=""):
        data=str(data)
        hash=md5.md5()
        hash.update(data)
        hash.digest()
        return hash.hexdigest().upper()
    def sign(s,data=""):
        data=s._md5(data.replace("&","")+"tiebaclient!!!")
        return data
    def prep(s,data):
        tmp=[]
        x=""
        for i in data:
            tmp.append(i)
        tmp.sort()
        for i in range(len(data)):
            x+=unquote(tmp[i]+"="+str(data[tmp[i]]))
        return s.sign(x)
    def uto(s,n):
        try:
            return n.replace("\\\\","\\").decode("unicode-escape")
        except:
            return n
    def getsync(s):
        newimei=s._md5(str(imei)+"0")
        myimei=s._md5(imei)
        syncurl="http://c.tieba.baidu.com/c/s/sync"
        syncprep={
            "msg_status":1,
            "manager_model":0,
            "_active":0,
            "_phone_screen":str(s.pix[0])+"%2A"+str(s.pix[1]),
            "_os_version":"6.1.3",
            "_phone_newimei":newimei,
            "_phone_imei":myimei,
            "cuid":myimei,
            "_timestamp":time.time(),
            "_client_id":0,
            "from":"appstore",
            "net_type":3,
            "ka":"open",
            "_client_version":"5.1.3"
        }
        syncprep["sign"]=s.prep(syncprep)
        data=post(syncurl,syncprep)
        try:
            return eval(data)["client"]["client_id"]
        except:
            return "error"
    def login(s,vmd5=0,vcode="none"):
        loginurl="http://c.tieba.baidu.com/c/s/login"
        newimei=s._md5(str(imei)+"0")
        myimei=s._md5(imei)
        postdata={
            "_client_type":1,
            "_phone_newimei":newimei,
            "cuid":myimei,
            "_timestamp":time.time(),
            "_phone_imei":myimei,
            "_client_id":s.client_id,
            "_client_version":"5.1.3",
            "from":"appstore",
            "un":s.un,
            "isphone":s.isp,
            "token":s.token,
            "passwd":s.psw,
            "net_type":3,
            "ka":"open",
            "m_api":"/c/s/sync",
        }
        #print postdata
        if(vmd5):
            postdata["vcode"]=vcode
            postdata["vcode_md5"]=vmd5
        postdata["sign"]=s.prep(postdata)
        data=post(loginurl,postdata)
        data=eval(data)
        #print data
        if(str(data["error_code"])=="0"):
            #for i in data:
                #print i,s.uto(data[i])
            #print cn("登录成功")
            ui.note(cn("登录成功"))
            s.BDUSS=s.uto(data["user"]["BDUSS"])
            s.id=s.uto(data["user"]["id"])
            s.name=s.uto(data["user"]["name"])
            #print cn(("用户名:%s\n用户ID:%s\ncookie:%s\n")%(en(s.name),en(s.id),en(s.BDUSS)))
            return "success"
        _error_msg=s.uto(data["error_msg"])
        if(_error_msg.find(cn("未知错误"))!=-1):
            if(postdata["vcode_md5"]):
                #print cn("验证码错误")
                ui.note(cn("验证码错误"))
                return cn("验证码错误")
            else:
                #print cn("未知错误")
                ui.note(cn("未知错误"))
                return "未知错误"
        if(_error_msg.find(cn("请输入验证码"))!=-1):
            #print cn("请输入验证码")
            if (str(data["anti"]["need_vcode"])=="1"):
                v_md5=data["anti"]["vcode_md5"]
                v_url=data["anti"]["vcode_pic_url"].replace("\\","")
                path="c:\\python\\pysoft\\tbs\\vpng.jpg"
                open(path,"wb").write(post(v_url))
                vcode=showyzm(path)
                return s.login(v_md5,vcode)
            #return "请输入验证码"
        #print cn(en(_error_msg))
        ui.note(cn(en(_error_msg)))
        return _error_msg

    def gettbs(s):
        newimei=s._md5(str(imei)+"0")
        myimei=s._md5(imei)
        url="http://c.tieba.baidu.com/c/s/tbs"
        postdata={
            "from":"appstore",
            "_client_version":"5.1.3",
            "_client_type":"1",
            "net_type":"3",
            "ka":"open",
            "_phone_imei":myimei,
            "_phone_newimei":newimei,
            "_client_id":s.client_id,
            "cuid":myimei,
            "_timestamp":time.time(),
            "BDUSS":s.BDUSS
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        try:
            s.tbs=eval(data)["tbs"]
            return eval(data)["tbs"]
        except:
            return "error"
    def getforumlist(s):
        newimei=s._md5(str(imei)+"0")
        myimei=s._md5(imei)
        url="http://c.tieba.baidu.com/c/f/forum/getforumlist"
        postdata={
            "BDUSS":s.BDUSS,
            "_client_id":s.client_id,
            "_client_type":"1",
            "_client_version":"5.1.3",
            "_phone_imei":myimei,
            "_phone_newimei":newimei,
            "_timestamp":time.time(),
            "cuid":imei,
            "from":"appstore",
            "ka":"open",
            "net_type":"3",
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        try:
            return eval(data)
        except:
            return "error"
    def msign(s,forumids):
        url="http://c.tieba.baidu.com/c/c/forum/msign"
        newimei=s._md5(str(imei)+"0")
        myimei=s._md5(imei)
        postdata={
            "from":"appstore",
            "_client_version":"5.1.3",
            "_client_type":"1",
            "net_type":"3",
            "ka":"open",
            "_phone_imei":myimei,
            "_phone_newimei":newimei,
            "_client_id":s.client_id,
            "cuid":myimei,
            "_timestamp":time.time(),
            "BDUSS":s.BDUSS,
            "forum_ids":forumids,
            "tbs":s.tbs
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        try:
            return eval(data)
        except:
            return "error"
        #return ["未知错误","你签得太快了，先看看贴子再来签吧",]
    def tsign(s,kw):
        #try:kw=en(kw)
        #except:pass
        url="http://c.tieba.baidu.com/c/c/forum/sign"
        postdata={
            "tbs":s.tbs,
            "kw":kw,
            #"uid":s.id,
            "BDUSS":s.BDUSS
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        data=eval(data)
        if(str(data["error_code"])!="0"):
            #亲，你之前已经签过了
            if(en(s.uto(data["error_msg"]))=="加载数据失败"):
                #print u"ok"
                s.tsign(kw)
        return data
    def getUserLikedForum(s):
        url="http://c.tieba.baidu.com/c/f/forum/like"
        postdata={
            "BDUSS":s.BDUSS
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        try:
            return eval(data)
        except:
            return "error"
    def getmsg(s):
        #获取回复,at,粉丝
        url="http://c.tieba.baidu.com/c/s/msg"
        postdata={
            "BDUSS":s.BDUSS
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        try:
            data=eval(data)
            print data
            return {"fans":data["message"]["fans"],"pletter":data["message"]["pletter"],"replyme":data["message"]["replyme"],"atme":data["message"]["atme"]}
            #{'logid': 295792948, 'server_time': 86983, 'ctime': 0, 'time': 1423793095, 'message': {'count': 27, 'fans': 0, 'pletter': 27, 'bookmark': 0, 'replyme': 0, 'atme': 0}, 'error_code': '0'}
            #return eval(data)
        except:
            return "error"
    def getbar(s,kw,pn=1,rn=35):
        url="http://c.tieba.baidu.com/c/f/frs/page"
        postdata={
            "BDUSS":s.BDUSS,
            "kw":kw,
            "pn":pn,
            "rn":rn
        }
        postdata["sign"]=s.prep(postdata)
        data=post(url,postdata)
        return eval(data)

def autosign(un,psw,isp):
    tbnet=tiebanet(un,psw,isp)
    tbnet.login()
    tbs=tbnet.gettbs()
    #print u"tbs="+tbs
    #print tbnet.tsign("安徽太和一中")#单吧签到
    try:
        foruminfo=tbnet.getforumlist()["forum_info"]
    except:
        foruminfo=""
    #print foruminfo
    ignore_num=len(foruminfo)
    forum_ids=[]
    for i in foruminfo:
        if(str(i["is_sign_in"])=="0"):
            forum_ids.append(i["forum_id"])
        else:
            print tbnet.uto(i["forum_name"]),cn("已经签过到")
    msig=tbnet.msign(",".join(forum_ids))
    print msig
    if(str(msig["show_dialog"])=="0"):
        print cn("一键签到完成")
    else:
        ignore_num=0
        print tbnet.uto(msig["error"]["usermsg"])
        #print tbnet.uto(sign_notice)
    try:
        liketb=tbnet.getUserLikedForum()
        liketb=liketb["forum_list"]
        print len(liketb)
    except:
        print cn("获取喜欢的吧失败！")
        return "获取喜欢的吧失败！"
    if(ignore_num>=len(liketb)):
        return "签到完成！共签到了"+str(ignore_num)+"个吧！"
    fav_ba=[]
    for i in range(ignore_num,len(liketb)):
        t=en(cn(en(tbnet.uto(liketb[i]["name"]))))
        fav_ba.append(t)
        sdata=tbnet.tsign(t)
        #print sdata
        #return 0
        if(str(sdata["error_code"])!="0"):
            print cn(t+"吧:"),tbnet.uto(sdata["error_msg"])
        else:
            print cn(t+"吧签到成功")
            #，第"),sdata["data"]["uinfo"]["user_sign_rank"],cn("个签到！")
        time.sleep(1.5)
#print u"ok"
