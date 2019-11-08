# -*- coding: utf-8 -*-
import os
import sys
path = os.getcwd()
index = path.rfind('\\')
path=path[:index]
index = path.rfind('\\')
path=path[:index]
sys.path.append(path+"\\Pys60_Simulator\\")
mypath = path+"\\python\\pygame\\Sokoban\\"

class Sokoban:
  def __init__(s):
    import appuifw,sysinfo,e32dbm,os
    from graphics import Image
    s.appuifw,s.e32,s.Image,s.e32dbm=appuifw,appuifw.e32,Image,e32dbm
    s.appuifw.app.screen="full"
    s.canvas=s.appuifw.Canvas(s.redraw0,s.events)
    s.screen_size=sysinfo.display_pixels()
    s.path=mypath
    s.back()
    s.start()
    del appuifw,Image,sysinfo,e32dbm,os

  def back(s):
    s.img_back=s.Image.new(s.screen_size)
    s.img_back.clear(0xffff)
    for i in range(30):
      s.img_back.rectangle((0,i,240,30-i),(255-i*5,i*4,255-i*2))
    s.length2=s.img_back.measure_text('推 箱 子  V2.00'.decode("u8"),(u'',22))[0]
    s.img_back.text((120-s.length2[2]/2,15-s.length2[1]/2),'推 箱 子  V2.00'.decode("u8"),(255,255,0),("dense",22))
    s.img_back.rectangle((1,1+40,239,239+40),0xff0000,width=3)
    s.img_floor_1=s.Image.open(s.path_pic("floor_1"))
    s.img_floor_2=s.Image.open(s.path_pic("floor_2"))
    for i in range(9):
      for j in range(9):
        if i %2==0:
          if j%2==0:
            s.img_back.blit(s.img_floor_1,target=(i*25+7,j*25+7+40))
          else:
            s.img_back.blit(s.img_floor_2,target=(i*25+7,j*25+7+40))
        else:
          if j%2==1:
            s.img_back.blit(s.img_floor_1,target=(i*25+7,j*25+7+40))
          else:
            s.img_back.blit(s.img_floor_2,target=(i*25+7,j*25+7+40))
          pass
        pass
      pass
    del i,j,s.img_floor_1,s.img_floor_2
  
  def start(s):
    s.map_db=s.e32dbm.open((s.path+"record\\map").decode("u8"),"r")
    s.img_main=s.Image.new(s.screen_size)
    s.img=s.Image.new(s.screen_size)
    s.img_box_1=s.Image.open(s.path_pic("box_1"))
    s.img_box_2=s.Image.open(s.path_pic("box_2"))
    s.img_ren=s.Image.open(s.path_pic("ren_down")).resize((25,25))
    s.img_rock=s.Image.open(s.path_pic("rock"))
    s.img_flag=s.Image.open(s.path_pic("flag"))  
  
  def exit(s):
    if s.play==0:text='返回主界面？'.decode("u8")
    else:text='返回？'.decode("u8")
    if s.appuifw.query(text,'query'):
      s.run=0
    del text
  
  def main(s,level,key_list=[]):
    s.play=0
    s.appuifw.app.exit_key_handler=s.exit
    s.game(level)
    s.appuifw.app.body=s.canvas

    s.run=1
    if key_list!=[]:
      s.play=1
      try:_time=float(open(s.path+"record\\time.db").read())
      except:_time=0.2
      s.appuifw.note("开 始 播 放".decode("u8"))
      for i in key_list:
        if i==1:s.move_up()
        elif i==2:s.move_down()
        elif i==3:s.move_left()
        elif i==4:s.move_right()
        if s.run==0:break
        s.e32.ao_sleep(_time)
      if s.run==1:s.appuifw.note("播放完毕！".decode("u8"),"conf")
      del _time

    del level

    while s.run:
      s.e32.ao_yield()
    return

  def game(s,level):
    s.map=eval(s.map_db[str(level)])
    s.level=level
    s.move_history=[]
    s.key_history=[]
    s.map_pic()
    s.redraw()
    open(s.path+"record\\sokoban.db","w").write("%s"%level)
  
  def judge_win(s):
    if s.play==1:return
    _judge=0
    for i in s.map:
      for j in i:
        if j==1 or j==2:_judge+=1;break
        pass
      pass
    if _judge==0:
      key_history=s.key_history
      if s.level<64:
        s.appuifw.note("恭喜你过关了！\n正在进入下一关！".decode("u8") ,"conf")
        s.game(s.level+1)
        s.judge_zui(s.level-1,key_history)
      else:
        s.appuifw.note("恭喜你通关了！".decode("u8") ,"conf")
        s.judge_zui(s.level,key_history)
        s.run=0
      del key_history
    del _judge,i,j
  
  def judge_zui(s,level,key_history):
    try:db=s.e32dbm.open((s.path+"record\\key").decode("u8"),"w")
    except:db=s.e32dbm.open((s.path+"record\\key").decode("u8"),"n")
    try:
      if len(eval(db[str(level)]))<len(key_history):return
    except:pass
    db[str(level)]=repr(key_history)
    db.close()
    
  def map_pic(s):
    s.move_history.append(eval(repr(s.map)))
    s.img.blit(s.img_back)
    s.img.text((20,300),("关卡：%s"%s.level).decode("u8"),0,("dense",20))
    s.img.text((140,300),("步数：%s"%len(s.key_history)).decode("u8"),0,("dense",20))
    for i in range(len(s.map)):
      for j in range(len(s.map[i])):
        _pos=s.map[i][j]
        if _pos==0:pass
        elif _pos==6:
          s.img.blit(s.img_rock,target=(j*25+7,i*25+7+40))
        elif _pos==1:
          s.img.blit(s.img_flag,target=(j*25+7,i*25+7+40))
        elif _pos==2:
          s.img.blit(s.img_box_1,target=(j*25+7,i*25+7+40))
        elif _pos==3:
          s.img.blit(s.img_box_2,target=(j*25+7,i*25+7+40))
        elif _pos==4 or _pos==5:
          s.img.blit(s.img_ren,target=(j*25+7,i*25+7+40))
          s.ren_pos=[j,i]
        pass
      pass
    del i,j,_pos
    
  def move_all(s,ss,hh,type):
    s.key_history.append(type)
    s.map[ss][hh]=s.map[ss][hh]-4
    s.map_pic()
    s.redraw()
    del ss,hh,type
    s.judge_win()

  def move_down(s):
    hh,ss=s.ren_pos
    if ss<8 and s.map[ss+1][hh]!=6:
      if s.map[ss+1][hh]==2 or s.map[ss+1][hh]==3:
        if ss+2<=8 and ( s.map[ss+2][hh]==0 or s.map[ss+2][hh]==1 ):
          s.map[ss+1][hh]=s.map[ss+1][hh]+2
          s.map[ss+2][hh]=s.map[ss+2][hh]+2
          s.move_all(ss,hh,2)
        pass
      else:
        s.map[ss+1][hh]=s.map[ss+1][hh]+4
        s.move_all(ss,hh,2)
      pass
    del ss,hh
  
  def move_up(s):
    hh,ss=s.ren_pos
    if ss>0 and s.map[ss-1][hh]!=6:
      if s.map[ss-1][hh]==2 or s.map[ss-1][hh]==3:
        if ss-2>=0 and ( s.map[ss-2][hh]==0 or s.map[ss-2][hh]==1 ):
          s.map[ss-1][hh]=s.map[ss-1][hh]+2
          s.map[ss-2][hh]=s.map[ss-2][hh]+2
          s.move_all(ss,hh,1)
        pass
      else:
        s.map[ss-1][hh]=s.map[ss-1][hh]+4
        s.move_all(ss,hh,1)
      pass
    del ss,hh
    
  def move_right(s):
    hh,ss=s.ren_pos
    if hh<8 and s.map[ss][hh+1]!=6:
      if s.map[ss][hh+1]==2 or s.map[ss][hh+1]==3:
        if hh+2<=8 and ( s.map[ss][hh+2]==0 or s.map[ss][hh+2]==1 ):
          s.map[ss][hh+1]=s.map[ss][hh+1]+2
          s.map[ss][hh+2]=s.map[ss][hh+2]+2
          s.move_all(ss,hh,4)
        pass
      else:
        s.map[ss][hh+1]=s.map[ss][hh+1]+4
        s.move_all(ss,hh,4)
      pass
    del ss,hh

  def move_left(s):
    hh,ss=s.ren_pos
    if hh>0 and s.map[ss][hh-1]!=6:
      if s.map[ss][hh-1]==2 or s.map[ss][hh-1]==3:
        if hh-2>=0 and ( s.map[ss][hh-2]==0 or s.map[ss][hh-2]==1 ):
          s.map[ss][hh-1]=s.map[ss][hh-1]+2
          s.map[ss][hh-2]=s.map[ss][hh-2]+2
          s.move_all(ss,hh,3)
        pass
      else:
        s.map[ss][hh-1]=s.map[ss][hh-1]+4
        s.move_all(ss,hh,3)
      pass
    del ss,hh
    
  def move_back(s):
    if len(s.move_history)>1:
      s.map=s.move_history[:][-2]
      del s.move_history[-2:]
      del s.key_history[-1]
      s.map_pic();s.redraw()
      
  def redraw(s):
    s.img_main.blit(s.img)
    s.redraw0(())
  
  def redraw0(s,rect):
    s.canvas.blit(s.img_main)

  def events(s,event):
    s.scan=event["scancode"]
    s.key=event["keycode"]
    s.type=event["type"]
    if s.play==1:return
    if s.key==56 or s.key==63498:
      s.move_down()
    elif s.key==50 or s.key==63497:
      s.move_up()
    elif s.key==52 or s.key==63495:
      s.move_left()
    elif s.key==54 or s.key==63496:
      s.move_right()
    elif s.key==8:
      s.move_back()
    elif s.key==63586:
      s.game(s.level)
    
      
  def path_pic(s,_pic_name):
    return (s.path+"picture\\"+_pic_name+".jpg").decode("u8")



class main:
  def __init__(s):
    import appuifw,sysinfo,akntextutils,os,e32dbm,os,envy
    from graphics import Image
    s.appuifw,s.e32,s.Image,s.akntextutils,s.os,s.e32dbm=appuifw,appuifw.e32,Image,akntextutils,os,e32dbm
    envy.set_app_system(1)
    s.appuifw.app.screen="full"
    s.screen_size=sysinfo.display_pixels()
    s.path=mypath
    s.sokoban=Sokoban()
    s.canvas=s.appuifw.Canvas(s.redraw0,s.events)
    s.appuifw.app.body=s.canvas
    s.appuifw.app.exit_key_handler=s.exit
    del appuifw,Image,sysinfo,akntextutils,os,envy
    
    s.start()

  def start(s):
    s.img_back_main=s.Image.open((s.path+"picture\\Sokoban.jpg").decode("u8"))
    s.img_main=s.Image.new(s.screen_size)
    s.img=s.Image.new(s.screen_size)
    s.img_back=s.Image.new(s.screen_size)
    s.menu0=["开 始 游 戏","继 续 游 戏","关 卡 选 择","更 多 内 容","退 出 游 戏"]
    s.menu1=["最 佳 记 录","设 置 延 时","更 新 内 容","使 用 说 明","软 件 关 于"]
    
    s.level_show=0
    s.menu_show=0
    s.text_show=0
    s.back()
    s.cursor_pic()

  def back(s,_cursor=0):
    s.cursor=_cursor
    del _cursor
    if s.menu_show==0:
      s.menu=s.menu0
    else:s.menu=s.menu1
    s.img_back.blit(s.img_back_main)
    s.length=s.img_back.measure_text(s.menu[0].decode("u8"),("dense",20))[0]
    for i in range(len(s.menu)):
      s.img_back.polygon(s.rim((120-s.length[2]/2-16,135+i*35,120+s.length[2]/2+16,165+i*35)),fill=0xffa600)
      s.img_back.text((120-s.length[2]/2,160+i*35),s.menu[i].decode("u8"),0x201e1b,("dense",20))


  def cursor_pic(s):
    s.img.blit(s.img_back)
    if s.menu_show!=2:
      s.img.polygon(s.rim((120-s.length[2]/2-16,135+s.cursor*35,120+s.length[2]/2+16,165+s.cursor*35)),fill=0xffc700)
      s.img.text((120-s.length[2]/2,160+s.cursor*35),s.menu[s.cursor].decode("u8"),0xff,("dense",20))
    else:
      level_show_old=s.level_show
      s.level_show=s.cursor/16
      if level_show_old!=s.level_show:
        s.key_list_pic();s.cursor_pic();s.redraw()
      
      if s.cursor<16*s.level_show+8:g,h=s.cursor+1-16*s.level_show,60
      else:g,h=s.cursor-7-16*s.level_show,180
      s.img.polygon(s.rim((h-s.length2[2]/2-4,g*35,h+s.length2[2]/2+4,30+g*35)),fill=0xffc700)
      s.img.text((h-s.length2[2]/2,25+g*35),("第%s关:%s步"%(s.cursor+1,len(s.key_list[s.cursor]))).decode("u8"),0xff,("dense",18))

  def exit(s):
    if s.text_show==1:
      s.text_show=0
      s.back(s.cursor)
      s.cursor_pic()
      s.redraw()
      return
    if s.menu_show==1:
      s.menu_show=0
      s.back(3)
      s.cursor_pic()
      s.redraw()
    elif s.menu_show==2:
      s.menu_show=1
      s.back(0)
      s.cursor_pic()
      s.redraw()
      
  def redraw(s):
    s.img_main.blit(s.img)
    s.redraw0(())
  
  def events(s,event):
    s.scan=event["scancode"]
    s.key=event["keycode"]
    s.type=event["type"]
    if s.text_show==1:return
    if s.menu_show!=2:
      limit=len(s.menu)-1
    else:
      limit=63
    if s.key==56 or s.key==63498:
      if s.cursor<limit:s.cursor+=1
      else:s.cursor=0
      s.cursor_pic();s.redraw()
    elif s.key==50 or s.key==63497:
      if s.cursor>0:s.cursor-=1
      else:s.cursor=limit
      s.cursor_pic();s.redraw()
    elif s.key==52 or s.key==63495:
      if s.menu_show==2:
        if s.cursor==0:s.cursor=63
        elif s.cursor<8:s.cursor+=55
        else:s.cursor-=8
        s.cursor_pic();s.redraw()
    elif s.key==54 or s.key==63496:
      if s.menu_show==2:
        if s.cursor==63:s.cursor=0
        elif s.cursor>55:s.cursor-=55
        else:s.cursor+=8
        s.cursor_pic();s.redraw()
    elif s.key==53 or s.key==63557:
      s.certain()
  
  def certain(s):
    if s.menu_show==0:
      if s.cursor==0:
        s.game(1)

      elif s.cursor==1:
        try:
          level=int(open(s.path+"record\\sokoban.db").read())
          s.game(level)
        except:
          s.game(1)
        pass

      elif s.cursor==2:
        level=s.appuifw.query("第？关卡（1～64）".decode("u8"),"number",1)
        if level!=None:
          if level==0 or level>64:s.appuifw.note(("没有第%s关！！\n（1～64）"%level).decode("u8"))
          else:s.game(level)
        
      elif s.cursor==3:
        s.menu_show=1
        s.back()
        s.cursor_pic()
        s.redraw()

      elif s.cursor==4:
        import os;os.abort()

    elif s.menu_show==1:
      if s.cursor==0:
        s.best_record()
      elif s.cursor==1:
        while 1:
          time=s.appuifw.query("播放延时（0.04～5秒）".decode("u8"),"float",0.2)
          if time==None:break
          elif time>=0.04 and time<=5:
            open(s.path+"record\\time.db","w").write("%s"%time)
            s.appuifw.note("设置成功！".decode("u8"),"conf")
            break
          else: 
            s.appuifw.note("请重新设置\n（0.04～5秒）".decode("u8"),"conf")
          
      elif s.cursor==2:
        db=s.e32dbm.open((s.path+"record\\text").decode("u8"),"r")
        text=db["update"].decode("u8")
        s.text_pic("更 新".decode("u8"),text)
        db.close();del db,text
      elif s.cursor==3:
        db=s.e32dbm.open((s.path+"record\\text").decode("u8"),"r")
        text=db["help"].decode("u8")
        s.text_pic("帮 助".decode("u8"),text)
        db.close();del db,text
      elif s.cursor==4:
        db=s.e32dbm.open((s.path+"record\\text").decode("u8"),"r")
        text=db["about"].decode("u8")
        s.text_pic("关 于".decode("u8"),text)
        db.close();del db,text
        
    else:
        s.play_record()
        
  def play_record(s):
      if s.key_list[s.cursor]==[]:
        s.appuifw.note('没有过关，不能播放！'.decode("u8"))
      else:
        s.sokoban.main(s.cursor+1,s.key_list[s.cursor])
        s.appuifw.app.body=s.canvas
        s.appuifw.app.exit_key_handler=s.exit
        s.cursor_pic()
        s.redraw()
  
  def best_record(s):
    s.cursor=0
    path=s.path+"record\\key"
    if s.os.path.isfile(path+".e32dbm"):
      s.key_list=[]
      db=s.e32dbm.open(path.decode("u8"),"r")
      for i in range(1,65):
        try:
          s.key_list.append(eval(db[str(i)]))
        except:
          s.key_list.append([])
        pass
      db.close()
      del db
    else:
      s.key_list=[[] for i in range(1,65)]
    s.key_list_pic()
    s.cursor_pic()
    s.redraw()

  def key_list_pic(s):
    s.menu_show=2
    s.img_back.clear(0xffff)
    for i in range(30):
      s.img_back.rectangle((0,i,240,30-i),(255-i*5,i*4,255-i*2))
    s.length2=s.img_back.measure_text('最 佳 记 录→播放'.decode("u8"),(u'',22))[0]
    s.img_back.text((120-s.length2[2]/2,15-s.length2[1]/2),'最 佳 记 录→播放'.decode("u8"),(255,255,0),("dense",22))
    s.length2=s.img_back.measure_text("第55关:555步".decode("u8"),("dense",18))[0]
    for i in range(s.level_show*16+1,s.level_show*16+17):
      if i<s.level_show*16+9:g,h=i-s.level_show*16,60
      else:g,h=i-8-s.level_show*16,180
      s.img_back.polygon(s.rim((h-s.length2[2]/2-4,g*35,h+s.length2[2]/2+4,30+g*35)),fill=0xffa600)
      s.img_back.text((h-s.length2[2]/2,25+g*35),("第%s关:%s步"%(i,len(s.key_list[i-1]))).decode("u8"),0x201e1b,("dense",18))
  
  def text_pic(s,title,text):
    s.text_show=1
    s.img.clear(0xffff)
    for i in range(30):
      s.img.rectangle((0,i,240,30-i),(255-i*5,i*4,255-i*2))
    length=s.img.measure_text('推 箱 子 → '.decode("u8")+title,(u'',22))[0]
    s.img.text((120-length[2]/2,15-length[1]/2),'推 箱 子 → '.decode("u8")+title,(255,255,0),("dense",22))
    text=s.akntextutils.wrap_text_to_array(text, 'dense', 230)
    for i in range(len(text)):
      s.img.text((8,50+i*25),text[i],0,("dense",18))
    s.redraw()
  
  def redraw0(s,rect):
    s.canvas.blit(s.img_main)


  def game(s,level):
    s.sokoban.main(level)
    s.appuifw.app.body=s.canvas
    s.appuifw.app.exit_key_handler=s.exit
    s.cursor_pic()
    s.redraw()

  def rim(s,a):
    a,b,c,d=a
    return (a,b+1,a+1,b+1,a+1,b,c-1,b,c-1,b+1,c,b+1,c,d-1,c-1,d-1,c-1,d,a+1,d,a+1,d-1,a,d-1)


main().redraw()



exec(u'import e32\ne32.Ao_lock().wait()', {}, {})