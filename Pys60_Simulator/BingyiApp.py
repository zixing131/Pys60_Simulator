# -*- coding: utf-8 -*-
__doc__="""
　BingyiApp模块
　　　by : ～あ冰^o^翼げ～(本版为紫星修改自用版)
以下为引入的模块
import appuifw,akntextutils,txtfield
from graphics import*
e32=appuifw.e32

调用方式：
app=App()
一些方法：
app.TitleName=cn('程序名称')
app.allClass(classList)
app.main(index=0,*args)
app.setSystem(type=1)
app.splitLines(content,width=200)

注意：
App:
super=    1→禁止按键  0→正常  2→系统要用的
keyType=    1→传递整个按键事件字典   0→传递简单转化后的数字 


""".decode("u8")

import appuifw,akntextutils,txtfield
from graphics import*
import e32
appuifw.app.screen="full"

def changeScreen(type=0):
  from video import orientation
  orientation(type)
  del orientation,type

def setSystem(type=1):
  import envy
  envy.set_app_system(type)
  del envy,type

class App:
  def __init__(s,path=None,waitTime=0):
    s.screenSize=appuifw.app.layout(appuifw.EScreen)[0]
    s.maxLines=[5,8][s.screenSize[1]>240]
    s.__doc__=__doc__
    s.__canvas=appuifw.Canvas(s.__redraw,s.__events)
    appuifw.app.body=s.__canvas
    try:
      s.blit(Image.open(path))
      e32.ao_sleep(waitTime)
    except:pass
    del path,waitTime
    appuifw.app.exit_key_handler=s.__exit
    s.__imgOld=Image.new(s.screenSize)
    s.__img=s.__imgOld
    s.__mask=Image.new(s.screenSize,"L")
    s.__mask.clear(0x888888)
    s.__imgBlack=Image.new(s.screenSize)
    s.index=0
    s.super=0
    s.selectType=0
    s.keyType=0
    s.keyList=[[16,50,63497],[17,56,63498],[14,52,63495],[15,54,63496],[167,53,63557],[196,63586]]
    s.TitleName="BingyiApp模块".decode("u8")
    s.__lock=e32.Ao_lock()
    s.__timer=e32.Ao_timer()
    
  def main(s,index=0,*args):
    s.index=index
    apply(s.classList[s.index].main,args)
    del index,args

  def allClass(s,classList):
    s.classList=map(lambda x:x(),classList)
    del classList
  
  def splitLines(s,content,width=200):
    return akntextutils.wrap_text_to_array(content,"dense",width)

  def textLen(s,content=u'',font='dense'):
    length=s.__img.measure_text(content,font)[0]
    return length[2],-length[1]

  def getCenter(s,pos,content=u'',font='dense'):
    if type(content)==type(u''):
      list=s.textLen(content,font)
    else:
      list=content
    return (pos[2]/2+pos[0]/2-list[0]/2,pos[3]/2+pos[1]/2+list[1]/2)

  def __exit(s):
    if s.super==2:
      s.choice=None
      s.__lock.signal()
    elif s.super==3:
      s.choice2=None
      s.__lock.signal()
    elif s.super==4:
      s.cursor=[]
      s.__lock.signal()
    elif s.super==0:
      s.classList[s.index].exit()
    elif s.super==5:
      s.choice,s.choiceL=None,[]
      s.__lock.signal()
  
  def __controlEvent(s,event):
    key=event["keycode"]
    scan=event["scancode"]
    type=event["type"]
    #Ok Button
    if key==63557:
      if s.super==2:
        if s.type=="query":
          s.choice=True
        else:
          s.choice=s.field.get()
        s.__lock.signal()
      elif s.super==3:
        s.choice2=True
        s.__lock.signal()
      elif s.super==4:
        s.__pressMenu()
      elif s.super==5:
        s.choice=s.cursorP+s.listP
        if not s.selectType:
          s.__lock.signal()
        else:
          if s.choice in s.choiceL:
            s.choiceL.remove(s.choice)
          else:
            s.choiceL.append(s.choice)
          s.__drawSelectionList()
    #Left Button
    elif scan==164 and type==3:
      if s.super==2:
        if s.type=="query":
          s.choice=True
        else:
          s.choice=s.field.get()
        s.__lock.signal()
      elif s.super==3:
        s.choice2=True
        s.__lock.signal()
      elif s.super==4:
        s.__pressMenu()
      elif s.super==5:
        s.choice=s.cursorP+s.listP
        s.__lock.signal()
    #Up
    elif key==63497:
      if s.super==2:
        if len(s.list)>5 and s.choice>0:
          s.choice-=1
          s.__drawQuery(s.list[s.choice:s.choice+5])
      elif s.super==3:
        if len(s.textL)>s.maxLines and s.choice>0:
          s.choice-=1
          s.__drawQuery2()
      elif s.super==4:
        s.cursor[s.menuI]-=1
        s.__drawMenu2(len(s.allArgs)-1,s.__img)
        s.__redraw()
      elif s.super==5:
        if s.cursorP>0:
          s.cursorP-=1
        else:
          if s.listP>0:
            s.listP-=1
          else:
            s.listP=len(s.selectL)-s.listValue-1
            s.cursorP=s.listValue
        s.__drawSelectionList()
    #Down
    elif key==63498:
      if s.super==2:
        if len(s.list)>5 and s.choice<len(s.list)-5:
          s.choice+=1
          s.__drawQuery(s.list[s.choice:s.choice+5])
      elif s.super==3:
        if len(s.textL)>s.maxLines and s.choice<len(s.textL)-s.maxLines:
          s.choice+=1
          s.__drawQuery2()
      elif s.super==4:
        s.cursor[s.menuI]+=1
        s.__drawMenu2(len(s.allArgs)-1,s.__img)
        s.__redraw()
      elif s.super==5:
        if s.cursorP<s.listValue:
          s.cursorP+=1
        else:
          if s.listP<len(s.selectL)-s.listValue-1:
            s.listP+=1
          else:
            s.listP=0
            s.cursorP=0
        s.__drawSelectionList()
    #Left
    elif key==63495:
      if s.super==4:
        del s.allArgs[-1],s.cursor[-1],s.wallPengL[-1]
        s.menuI-=1
        if s.cursor:
          s.__drawMenu()
        else:
          s.__lock.signal()
      elif s.super==3:
        s.super=1
        for i in xrange(s.maxLines-1):
          if len(s.textL)>s.maxLines and s.choice>0:
            s.choice-=1
            s.__drawQuery2()
        s.super=3
    #Right
    elif key==63496:
      if s.super==4:
        s.__pressMenu()
      elif s.super==3:
        s.super=1
        for i in xrange(s.maxLines-1):
          if len(s.textL)>s.maxLines and s.choice<len(s.textL)-s.maxLines:
            s.choice+=1
            s.__drawQuery2()
        s.super=3
    #数字键，﹡，﹟
    else:
      keyD={42:58,48:59,35:60}
      if key in [42,48,35]:key=keyD[key]

      if s.super==4:
        length=len(s.allArgs[-1][1])
        if length>12:length=12
        if key in range(49,49+length):
          s.cursor[s.menuI]=key-49
          s.__pressMenu()

    del key,scan,type,event

  def __events(s,event):
    if s.super:
      s.__controlEvent(event)
      return
    if s.keyType:
      s.classList[s.index].key(event)
      return
    key=event["keycode"]
    scan=event["scancode"]
    type=event["type"]
    if key==50 or key==63497:
      s.classList[s.index].key(1)
    elif key==56 or key==63498:
      s.classList[s.index].key(2)
    elif key==52 or key==63495:
      s.classList[s.index].key(3)
    elif key==54 or key==63496:
      s.classList[s.index].key(4)
    elif key==53 or key==63557:
      s.classList[s.index].key(5)
    elif scan==164 and type==3:
      s.classList[s.index].key(0)
    elif key==49:
      s.classList[s.index].key(6)
    del key,scan,type,event

  def blit(s,img):
    s.__img=img
    s.__redraw()
    del img

  def __redraw(s,rect=()):
    try:
      s.__canvas.blit(s.__img)
    except:pass    
  
  def menu(s,menuL,pos=None,backColor=0x0,cursorColor=0xaa00,textColor=0xffffff):
    if not pos:pos=[2,s.screenSize[1]-2]
    s.super=4
    s.__imgOld.blit(s.__img)
    #增加距离，以便增加">"
    s.addLength=13
    s.colorL=(backColor,cursorColor,textColor)
    s.menuI=0
    s.wallPengL=[1]
    s.allArgs=[]
    s.cursor=[0]
    s.__argsMenu(menuL,pos)
    s.__drawMenu()

    s.__lock.wait()
    s.super=0
    s.__img.blit(s.__imgOld)
    s.__redraw()
    del s.menuI,s.wallPengL,s.allArgs,s.colorL,s.addLength
    if s.cursor:
      for i in s.cursor:
        menuL=menuL[i][1]
      del s.cursor
      menuL()

  def __argsMenu(s,menuL,pos=None):
    list,listV,lengthL=[],[],[]
    for i in range(len(menuL)):
      if i==s.maxLines+4:break
      if callable(menuL[i][1]):
        listV.append(0)
      else:
        listV.append(menuL[i][1])
      list.append((u'%%%dd. '%len(str(len(menuL))))%(i+1)+menuL[i][0])
      lengthL.append(s.__img.measure_text((u'%%%dd. '%len(str(len(menuL))))%(i+1)+menuL[i][0],("dense",20))[0][2])
    length=max(lengthL)

    #以下，8是前后新增距离，2是两菜单间距
    if s.allArgs:
      if not pos:
        if s.wallPengL[-1]:
          X=s.allArgs[s.menuI][0][0]+s.allArgs[s.menuI][3]+8+2+s.addLength
          #判断是否靠近右侧边界
          if s.screenSize[0]-X-length-8-2-s.addLength<=0:
            s.wallPengL.append(0)
            X=s.screenSize[0]-length-8-2-s.addLength
          else:
            s.wallPengL.append(1)
        else:
          X=s.allArgs[s.menuI][0][0]-length-8-2-s.addLength
          #判断是否靠近左侧边界
          if X<=2:
            s.wallPengL.append(1)
            X=2
          else:
            s.wallPengL.append(0)
        Y=(len(s.allArgs[s.menuI][1])-s.cursor[s.menuI]-len(menuL))*25
        if Y<0:Y=0
        pos=[X,s.allArgs[0][0][1]-Y]
      s.cursor.append(0)
      s.menuI+=1

    s.allArgs.append((pos,list,listV,length))
    del lengthL
  
  def __drawMenu(s):
    s.__imgBlack.blit(s.__imgOld)
    #Redraw Each Menu List
    for j in range(len(s.allArgs)-1):
      s.__drawMenu2(j,s.__imgBlack)
    s.__img.clear(0)
    s.__img.blit(s.__imgBlack,mask=s.__mask)
    s.__img.clear(0)
    s.__img.blit(s.__imgBlack,mask=s.__mask)
    s.__imgBlack.blit(s.__img)
    for i in range(s.allArgs[-1][0][0]+1-7,s.allArgs[-1][0][0]+1,1):
      s.__img.blit(s.__imgBlack)
      s.__drawMenu2(len(s.allArgs)-1,s.__img,X=i)
      s.__redraw()
      e32.ao_yield()
        
  def __drawMenu2(s,j,imgTemp,X=None,Y=None):
      (pos,list,listV,length)=s.allArgs[j]
      if X:pos[0]=X
      if Y:pos[1]=Y
      if s.cursor[j]>=len(list):s.cursor[j]=0
      elif s.cursor[j]<0:s.cursor[j]=len(list)-1
      #Draw Frame
      #print(dir(imgTemp))
      imgTemp.rectangle((pos[0],pos[1]-len(list)*25-8,pos[0]+length+8+s.addLength,pos[1]),fill=s.colorL[0])
      #Draw Cursor
      imgTemp.polygon(s.rim((pos[0]+2,pos[1]-len(list)*25-4+s.cursor[j]*25-1,pos[0]+length+6+s.addLength-1,pos[1]-len(list)*25-2+s.cursor[j]*25+25-1)),fill=s.colorL[1])
      #Draw Menu Text
      for i in range(len(list)):
        imgTemp.text((pos[0]+4,pos[1]-(len(list)-i)*25+25-5),list[i],s.colorL[2],("dense",20))
        if listV[i]:
          imgTemp.text((pos[0]+length+8,pos[1]-(len(list)-i)*25+25-5),u'>',s.colorL[2],("dense",20))
  
  def __pressMenu(s):
    if s.allArgs[s.menuI][2][s.cursor[s.menuI]]:
      s.__argsMenu(s.allArgs[s.menuI][2][s.cursor[s.menuI]])
      s.__drawMenu()
    else:
      s.__lock.signal()
  
  def progressBar(s,title=u'Loading....'):
    s.super=1
    s.__imgOld.blit(s.__img)
    s.__img.clear(0)
    s.__img.blit(s.__imgOld,mask=s.__mask)

    s.__img.polygon(s.rim((0,130,240,160+60)),fill=0xa6f9f8)
    s.__img.polygon(s.rim((0,130,240,160)),fill=0x2ad8ea)
    s.__img.line((1,158,240,158),0xffffff,width=2)
    s.__img.text((120-s.__img.measure_text(title,("dense",20))[0][2]/2.0,155),title,0x0,("dense",20,FONT_BOLD|FONT_ANTIALIAS))
    s.__redraw()
    s.leng=-10
    s.__timer.after(0,s.drawProgressBar)
  
  def __drawProgressBar(s):
    s.leng+=1
    if s.leng==11:s.leng=-10
    s.__img.rectangle((20,177,220,197),fill=0x888888)
    for i in range(0,21,2):
      s.__img.polygon((10+s.leng+i*10,177,20+s.leng+i*10,177,40+s.leng+i*10,197,30+s.leng+i*10,197),fill=0xcaaaaa)
    s.__img.rectangle((1,177,20,197),fill=0xa6f9f8)
    s.__img.rectangle((220,177,240,197),fill=0xa6f9f8)
    s.__redraw()
    s.__timer.after(0,s.drawProgressBar)
  
  def progressBarStop(s,type=1):
    s.__timer.cancel()
    #type作用：是否再次载入上个界面
    if type:
      s.__img.blit(s.__imgOld)
      s.__redraw()
    s.super=0
    
  def query(s,content=u'',title=None,type="query",colour=0x888888):
    if not title:title=s.TitleName
    s.super=2
    s.__imgOld.blit(s.__img)
    s.__img.clear(0)
    s.__img.blit(s.__imgOld,mask=s.__mask)
    s.title,s.content,s.type,s.colour=title,content,type,colour
    s.choice,s.field=0,None
    if s.type=="query":
      s.list=akntextutils.wrap_text_to_array(s.content,"dense",200)
      if len(s.list)<=1:
        list=s.list+(u'',)
      elif len(s.list)>5:
        list=s.list[:5]
      else:
        list=s.list
    else:
      list,s.list=[0]*4,[0]*4
    s.__drawQuery(list)

    s.__lock.wait()
    s.__img.blit(s.__imgOld)
    s.__redraw()
    s.super=0
    del title,s.title,s.list,content,s.content,s.type,type,s.field
    return s.choice

  def __drawQuery(s,list):
    s.__img.polygon(s.rim((13,130,227,160+len(list)*25)),fill=s.colour)
    s.__img.polygon(s.rim((13,130,227,160)),fill=s.colour)
    s.__img.polygon(s.rim((13,160+len(list)*25-2,227,160+len(list)*25+27)),fill=s.colour)
    if len(s.list)>5:
      s.__img.line((224,162,224,280),s.colour,width=3)
      s.__img.line((224,162+s.choice*(280.0-162)/(len(s.list)-5+1),224,162+(s.choice+1)*(280.0-162)/(len(s.list)-5+1)),s.colour+0x777777,width=3)
    s.__img.line((14,158,225,158),s.colour+0x777777,width=2)
    s.__img.line((14,160+len(list)*25-2,225,160+len(list)*25-2),s.colour+0x777777,width=2)
    s.__img.text((120-s.__img.measure_text(s.title,("dense",22))[0][2]/2.0,155),s.title,0x0,("dense",22,FONT_BOLD|FONT_ANTIALIAS))
    s.__img.text((18,160+len(list)*25+25),'确定'.decode("u8"),0xff,("dense",20,FONT_BOLD|FONT_ANTIALIAS))
    s.__img.text((240-18-44,160+len(list)*25+25),'取消'.decode("u8"),0xff,("dense",20,FONT_BOLD|FONT_ANTIALIAS))

    if s.type=="query":
      for i in range(len(list)):
        s.__img.text((20,180+i*25),list[i],0x0,("dense",18,FONT_ANTIALIAS))
    else:
      s.field=txtfield.New((20,170,220,150+len(list)*25),cornertype=txtfield.ECorner1,txtlimit=0)
      s.field.textstyle(u'',140,0xffffff,style=u'normal')
      s.field.bgcolor(s.colour)
      s.field.add(s.content)
      s.field.select(0,len(s.content))
      s.field.focus(1)
      s.field.visible(1)
    s.__redraw()
    del list
  
  def query2(s,content=u'',title=None,maskColor=0x999999,backColor=0x0,textColor=0xffffff,type=1):
    s.__imgBlack.clear(backColor)
    if not title:title=s.TitleName
    s.super=3
    X,Y=5,s.screenSize[1]-60
    s.choice=0
    s.textL=s.splitLines(content,s.screenSize[0]-2*X-10)
    if len(s.textL)<=1:s.textL+=(u'',)
    if len(s.textL)<s.maxLines:
      height=len(s.textL)*25+30
    else:
      height=s.maxLines*25+30
    s.__imgOld.blit(s.__img)

    #for i in range(Y-height+80,Y-height-1,-20):
    step=(height+65)/10.0
    i=Y+65
    while i>Y-height-10:
      s.allArgs=[title,X,height,i,maskColor,textColor]
      s.__drawQuery2()
      i-=step 
    s.__lock.wait() 
    #禁止按键
    s.super=1
    #for i in range(Y-height,321,20):
    while i<Y+65:
      i+=step
      s.allArgs=[title,X,height,i,maskColor,textColor]
      s.__drawQuery2()
    s.super=0
    #是否载入上个界面
    if type:
      s.__img.blit(s.__imgOld)
      s.__redraw()
    #恢复初始的s.mask
    s.__mask.clear(0x888888)
    del s.allArgs,s.choice,s.textL
    return s.choice2

  def __drawQuery2(s):
    textL=s.textL[s.choice:s.choice+s.maxLines]
    title,X,height,i,maskColor,textColor=s.allArgs
    s.__img.blit(s.__imgOld)
    s.__mask.clear(0)
    s.__mask.polygon(s.rim((X,i,s.screenSize[0]-X,i+height+30)),fill=maskColor)
    s.__img.blit(s.__imgBlack,mask=s.__mask)
    s.__img.text((s.screenSize[0]/2-s.__img.measure_text(title,("dense",22))[0][2]/2.0,i+25),title,textColor,("dense",22,FONT_BOLD|FONT_ANTIALIAS))
    s.__img.line((X+2,i+30,s.screenSize[0]-X-2,i+30),maskColor,width=2)
    for j in range(len(textL)):
      s.__img.text((X+5,i+53+j*25),textL[j],textColor,("dense",18))
    s.__img.line((X+2,i+53+j*25+4,s.screenSize[0]-X-2,i+53+j*25+4),maskColor,width=2)
    s.__img.text((X+8,i+53+j*25+28),'确定'.decode("u8"),textColor,("dense",18))
    s.__img.text((s.screenSize[0]-X-3-38,i+53+j*25+28),'取消'.decode("u8"),textColor,("dense",18))
    s.__img.line((s.screenSize[0]-X-4,i+35,s.screenSize[0]-X-4,i+53+j*25),0xffff,width=3)
    if len(s.textL)>s.maxLines:
      s.__img.line((s.screenSize[0]-X-4,i+35,s.screenSize[0]-X-4,i+35+(s.choice+1)*(53+j*25-35)/(len(s.textL)-s.maxLines+1)),0xaaff,width=3)
    s.__redraw()
    e32.ao_yield()
  
  def multiSelectionList(s,selectL,title=None,maskColor=0x999999,backColor=0x0,textColor=0xffffff,selectColor=0xffff00):
    s.selectType=1
    s.selectionList(selectL,title,maskColor,backColor,textColor,selectColor)
    s.selectType=0
    return tuple(s.choiceL)
  
  def selectionList(s,selectL,title=None,maskColor=0x999999,backColor=0x0,textColor=0xffffff,selectColor=0xffa600):
    s.__imgBlack.clear(backColor)
    if not title:title=s.TitleName
    s.selectL=selectL
    s.super=5
    X,Y=5,s.screenSize[1]-60
    s.listP=0
    s.cursorP=0
    s.choice,s.choiceL=None,[]
    s.selectL=[s.splitLines(i,s.screenSize[0]-X-X-8-5-4)[0] for i in s.selectL]
    if len(s.selectL)<s.maxLines:
      height=len(s.selectL)*25+30
      s.listValue=len(s.selectL)-1
    else:
      height=s.maxLines*25+30
      s.listValue=s.maxLines-1

    s.__imgOld.blit(s.__img)
    for i in range(Y,Y-height-1,-15):
      s.allArgs=[title,X,height,i,maskColor,textColor,selectColor]
      s.__drawSelectionList()
    s.__lock.wait()
    s.super=1
    for i in range(Y-height,331,20):
      s.allArgs=[title,X,height,i,maskColor,textColor,selectColor]
      s.__drawSelectionList()
    s.super=0
    s.__img.blit(s.__imgOld)
    s.__redraw()
    #恢复初始的s.mask
    s.__mask.clear(0x888888)
    del s.selectL,s.allArgs,s.listValue,s.listP,s.cursorP
    s.choiceL.sort()
    return s.choice
#    return (s.choice,tuple(s.choiceL))[s.selectType]
  
  def __drawSelectionList(s):
    selectL=s.selectL[s.listP:s.listP+s.maxLines]
    title,X,height,i,maskColor,textColor,selectColor=s.allArgs
    s.__img.blit(s.__imgOld)
    s.__mask.clear(0)
    s.__mask.polygon(s.rim((X,i,s.screenSize[0]-X,i+height+30)),fill=maskColor)
    s.__img.blit(s.__imgBlack,mask=s.__mask)
    s.__img.text((s.screenSize[0]/2-s.__img.measure_text(title,("dense",22))[0][2]/2.0,i+25),title,textColor,("dense",22,FONT_BOLD|FONT_ANTIALIAS))
    s.__img.line((X+2,i+30,s.screenSize[0]-X-2,i+30),maskColor,width=2)
    #Draw Cursor
    s.__img.polygon(s.rim((X+5,i+33+s.cursorP*25,s.screenSize[0]-X-8,i+55+s.cursorP*25)),fill=0xaaaa)
    for j in range(len(selectL)):
      if j+s.listP in s.choiceL:
        s.__img.text((X+8,i+53+j*25),selectL[j],selectColor,("dense",18))
      else:
        s.__img.text((X+8,i+53+j*25),selectL[j],textColor,("dense",18))
    s.__img.line((X+2,i+53+j*25+4,s.screenSize[0]-X-2,i+53+j*25+4),maskColor,width=2)
    s.__img.text((X+8,i+53+j*25+28),'确定'.decode("u8"),textColor,("dense",18))
    s.__img.text((s.screenSize[0]-X-3-38,i+53+j*25+28),'取消'.decode("u8"),textColor,("dense",18))
    s.__img.line((s.screenSize[0]-X-4,i+35,s.screenSize[0]-X-4,i+53+j*25),0xffff,width=3)
    s.__img.line((s.screenSize[0]-X-4,i+35,s.screenSize[0]-X-4,i+35+(s.cursorP+s.listP+1)*(53+j*25-35)/len(s.selectL)),0xaaff,width=3)
    s.__redraw()
    e32.ao_yield()

  def note(s,content,title=None,waitTime=1):
    if not title:title=s.TitleName
    s.super=1
    s.__imgOld.blit(s.__img)
    s.__img.clear(0)
    s.__img.blit(s.__imgOld,mask=s.__mask)

    list=akntextutils.wrap_text_to_array(content,"dense",200)
    if len(list)<=1:list+=(u'',)
    elif len(list)>6:list=list[:6]
    s.__img.polygon(s.rim((13,130,227,160+len(list)*25)),fill=0xa6f9f8)
    s.__img.polygon(s.rim((13,130,227,160)),fill=0x2ad8ea)
    s.__img.line((14,158,225,158),0xffffff,width=2)
    s.__img.text((120-s.__img.measure_text(title,("dense",20))[0][2]/2.0,155),title,0x0,("dense",20,FONT_BOLD|FONT_ANTIALIAS))
    for i in range(len(list)):
      s.__img.text((20,180+i*25),list[i],0x0,("dense",18,FONT_ANTIALIAS))
    s.__redraw()
    e32.ao_sleep(waitTime)
    s.__img.blit(s.__imgOld)
    s.__redraw()
    s.super=0
  
  def note2(s,content,title=None,waitTime=1,maskColor=0x999999,backColor=0x0,textColor=0xffffff,type=1):
    s.__imgBlack.clear(backColor)
    if not title:title=s.TitleName
    s.super=1
    X,Y=5,s.screenSize[1]-40
    textL=s.splitLines(content,s.screenSize[0]-2*X-10)
    if len(textL)<=1:textL+=(u'',)
    elif len(textL)>s.maxLines:textL=textL[:s.maxLines]
    height=len(textL)*25+30
    s.__imgOld.blit(s.__img)
   
    for i in range(Y,Y-height,-15):
      s.__drawNote2(title,X,height,i,textL,maskColor,textColor)
    e32.ao_sleep(waitTime)
    for i in range(Y-height,321,20):
      s.__drawNote2(title,X,height,i,textL,maskColor,textColor)
    s.super=0
    if type:
      s.__img.blit(s.__imgOld)
      s.__redraw()
    #恢复初始的s.mask
    s.__mask.clear(0x888888)
  
  def __drawNote2(s,title,X,height,i,textL,maskColor,textColor):
      s.__img.blit(s.__imgOld)
      s.__mask.clear(0)
      s.__mask.polygon(s.rim((X,i,s.screenSize[0]-X,i+height)),fill=maskColor)
      s.__img.blit(s.__imgBlack,mask=s.__mask)
      s.__img.text((s.screenSize[0]/2-s.__img.measure_text(title,("dense",22))[0][2]/2.0,i+25),title,textColor,("dense",22,FONT_BOLD|FONT_ANTIALIAS))
      s.__img.line((X+2,i+30,s.screenSize[0]-X-2,i+30),maskColor,width=2)
      for j in range(len(textL)):
        s.__img.text((X+5,i+53+j*25),textL[j],textColor,("dense",18))
      s.__redraw()
      e32.ao_yield()
  
  def rim(s,a):
    a,b,c,d=a
    return (a,b+1,a+1,b+1,a+1,b,c-1,b,c-1,b+1,c,b+1,c,d-1,c-1,d-1,c-1,d,a+1,d,a+1,d-1,a,d-1)

  def maskImg(s,path,color=None):
    try:
      imgg=Image.open(path)
    except:
      imgg=path
    if color==None:
      color = imgg.getpixel((0, 0))[0]
    mask = Image.new(s.__imgg.size, "1")
    for y in range(s.__imgg.size[1]):
        line = imgg.getpixel([(x, y) for x in range(imgg.size[0])])
        for x in range(imgg.size[0]):
            if line[x] == color:
                mask.point((x, y),0)
    del color,x,y,line
    return (imgg,mask)
  def imgOpen(s,path):
    imgg=Image.open(path)
    try:
      mask2=Image.open(path.replace(".","M."))
      mask=Image.new(mask2.size,"L")
      mask.blit(mask2)
      del mask2
      return (imgg,mask)
    except:
      return imgg
