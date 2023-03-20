# -*- coding: utf-8 -*-
import time

import appuifw
import graphics
import e32
import os
import neteasemusicapi as api
import qrcode

class ScreenType:
    main=1
    login=2

def cn(x):
    return x.decode('utf8')

img=None
FONT = 'normal'
def get_text_size(text, font=None):
    global img
    if img is None:
        img = graphics.Image.new((240,100))
    wh=img.measure_text(text, (FONT,font))[0]
    print(wh)
    return [wh[2],0-wh[1]]

class MyApp:
    def __init__(self):
        self.screensize = appuifw.app.layout(appuifw.EScreen)[0]
        self.screenwidth, self.screenheight = self.screensize
        self.basePath = 'c:\\python\\pysoft\\pyneteasemusic\\'
        self.isE63 = self.screenwidth == 320
        self.running = 1
        self.canvas = appuifw.Canvas(None,self.handle_redraw)
        appuifw.app.body = self.canvas
        appuifw.app.screen = 'full'
        appuifw.app.exit_key_handler = self.quit
        self.loginkey=''
        self.QrImage = None

        self.api = api.MyApi()
        self.load_resources()
        self.readCookies()
        self.checkLogin()
        self.initialize()
    def readCookies(self):
        self.Cookies = ""
        p = self.basePath+"/cookies.txt"
        if(os.path.exists(p)):
            self.Cookies = open(p,'r').read()

    def SaveCookies(self):
        open(self.basePath+"/cookies.txt",'w').write(self.Cookies)

    def quit(self):
        self.running = 0


    def load_resources(self):
        if self.isE63:
            self.bgimg = graphics.Image.open(self.basePath + "skin\\skin_320x240.png")
            self.iconimg = graphics.Image.open(self.basePath + "skin\\icon_320x240.png")
        else:
            self.bgimg = graphics.Image.open(self.basePath + "skin\\skin_240x320.png")
            self.iconimg = graphics.Image.open(self.basePath + "skin\\icon_240x320.png")

        self.iconimg2 = graphics.Image.new((self.iconimg.size[0] + 10, self.iconimg.size[1] + 10))
        self.iconimg2.blit(self.iconimg, target=(5, 5))
        self.iconimgmask = graphics.Image.new(self.iconimg2.size, "L")
        self.iconimgmask.clear(0x333333)
        self.iconimgmask.rectangle((5, 5, self.iconimg.size[0] + 4, self.iconimg.size[1] + 4), fill=0, outline=0,
                                   width=0)

    def checkLogin(self):
        if(self.Cookies==''):
            self.nowscreen = ScreenType.login
        else:
            self.nowscreen = ScreenType.main

    def drawLoginScreen(self):
        if(self.loginkey==''):
            keyret = self.api.qrKey()
            self.loginkey = keyret['data']['unikey']
            dataret = self.api.qrCreate(self.loginkey)
            qrurl = dataret['data']['qrurl']
            qr = qrcode.QRCode(box_size=4,border=4)
            qr.add_data(qrurl)
            img = qr.make_image()
            self.QrImage = img
        elif(self.QrImage!=None):
            self.baseimg.clear(0x202020)
            center1 = [int(self.screenwidth / 2), int((self.screenheight) / 2 - 20)]
            target1 = [0-int(center1[0] - self.QrImage.size[0] / 2), 0-int(center1[1] - self.QrImage.size[1] / 2)]
            print(target1)
            self.baseimg.blit(self.QrImage,target1)
            self.showLoginText = cn('请使用网易云APP扫码登录')
            wh = get_text_size(self.showLoginText,16)
            self.baseimg.text( (int(center1[0] - wh[0]/2),int(center1[1] + self.QrImage.size[1] / 2+wh[1]+8)) , self.showLoginText, 0xffffff,
                         ("dense", 16, graphics.FONT_BOLD | graphics.FONT_ANTIALIAS))
            self.drawToCanvas()
            while(1):
                checkret = self.api.qrCheck(self.loginkey)
                ccode = checkret['code']
                if(ccode==801):
                    e32.ao_sleep(1)
                elif(ccode == 803 or ccode==802):
                    if(ccode==802):
                        self.showLoginText = cn('请点击授权')
                    else:
                        self.showLoginText = cn('登录成功')
                        self.Cookies = checkret['cookie']
                        self.SaveCookies()
                        self.lastImg = None
                        self.nowscreen = ScreenType.main
                        return
                    self.baseimg.clear(0x202020)
                    self.baseimg.blit(self.QrImage, target1)

                    wh = get_text_size(self.showLoginText, 16)
                    self.baseimg.text((int(center1[0] - wh[0] / 2), int(center1[1] + self.QrImage.size[1] / 2 + wh[1]+8)),
                                      self.showLoginText, 0xffffff,
                                      ("dense", 16, graphics.FONT_BOLD | graphics.FONT_ANTIALIAS))
                    self.drawToCanvas()
                elif(ccode == 804):
                    #码失效了
                    self.loginkey = ''
                    return self.drawLoginScreen()
                e32.ao_sleep(1)
        pass

    def initialize(self):
        self.baseimg = graphics.Image.new(self.screensize)
        splash = graphics.Image.new(self.screensize)
        splash.clear(0xdb2c1f)
        splash1 = graphics.Image.open(self.basePath + "skin\\splash1.png")
        splash2 = graphics.Image.open(self.basePath + "skin\\splash2.png")
        center1 = [int(self.screenwidth / 2), int((self.screenheight * 0.7) / 2)]
        target1 = [int(center1[0] - splash1.size[0] / 2), int(center1[1] - splash1.size[1] / 2)]
        center2 = [int(self.screenwidth / 2), int(self.screenheight * 0.7 + (self.screenheight * 0.3) / 2)]
        target2 = [int(center2[0] - splash2.size[0] / 2), int(center2[1] - splash2.size[1] / 2)]
        splash.blit(splash1, target=target1)
        splash.blit(splash2, target=target2)
        self.canvas.blit(splash)
        del splash
        e32.ao_sleep(1)

    def refresh_screen(self):
        if(self.nowscreen == ScreenType.main):
            self.drawMainScreen()
        elif(self.nowscreen ==ScreenType.login):
            self.drawLoginScreen()
        else:
            pass

    def drawToCanvas(self):
        # 把图形画到canvas(画布)上
        self.canvas.blit(self.baseimg)
        self.lastImg = self.baseimg

    def drawMainScreen(self):
        self.baseimg.clear(0xffffff)
        self.baseimg.blit(self.bgimg)
        if self.isE63:
            self.baseimg.blit(self.iconimg2, target=(11, 28), mask=self.iconimgmask)
        else:
            self.baseimg.blit(self.iconimg2, target=(int(self.screenwidth / 2 - self.iconimg2.size[0] / 2), 66),
                              mask=self.iconimgmask)


    def handle_redraw(self, rect):
        self.drawToCanvas()

    def run(self):
        self.lastImg = None
        while self.running:
            try:
                self.refresh_screen()
                if(self.lastImg!=self.baseimg):
                    self.drawToCanvas()
                e32.ao_yield()
            except:
                pass

if __name__ == "__main__":
    app = MyApp()
    app.run()
