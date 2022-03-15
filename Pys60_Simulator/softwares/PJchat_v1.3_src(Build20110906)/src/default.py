#-*- coding:utf-8 -*-
#泡椒聊天启动程序
#Powered By 52cyy℡
#PJChat_v1.3(Build20110906)

import os,sys
path1 = os.getcwd()
index = path1.rfind('\\')
mypath=path1[:index]
index = mypath.rfind('\\')
mypath=mypath[:index]
#mypath2=path1+'\\src\\'
sys.path.append(mypath)
#sys.path.append(mypath2)

import appuifw,graphics,e32

#disk=appuifw.app.full_name()[0]
path=mypath+"\\PJchat_v1.3_src(Build20110906)\\"
try:
    import envy
    envy.set_app_system(1)
except:pass
cn=lambda x:x#.decode("u8")
appuifw.app.screen="full"
appuifw.app.body=body=appuifw.Canvas()
x,y=body.size
if x==240:
    enterimg=graphics.Image.open(path+"Images\\enterimg1.jpg").resize((x,y))
    enterimg.text((x/4,y/1.4),cn("程 序 初 始 化 中 …"),0,("dense",16))
else:
    enterimg=graphics.Image.open(path+"Images\\enterimg2.jpg").resize((x,y))
    enterimg.text((x/2,y/1.4),cn("程 序 初 始 化 中 …"),0,("dense",16))
body.blit(enterimg)
appuifw.app.menu=[]
appuifw.app.exit_key_handler=lambda:None
del enterimg
e32.ao_yield()
#try:
import PJChatMain
Run= PJChatMain.MainPageUI()
Run.StartApp()
Run.lock.wait()
del appuifw,graphics,e32
del PJChatMain
# except Exception,ex:
#     print(ex)
#     appuifw.note("主程序文件运行错误！请卸载本软件后重新安装！".decode("utf8"),"error",1)
#     e32.ao_sleep(2)
#     import os
#     os.abort()