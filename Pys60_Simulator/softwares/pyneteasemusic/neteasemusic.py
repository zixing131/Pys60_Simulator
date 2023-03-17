# -*- coding: utf-8 -*-
import appuifw
import graphics
import e32
import os


class MyApp:
    def __init__(self):
        self.screenwidth, self.screenheight = appuifw.screen
        self.basePath = 'c:\\python\\pysoft\\pyneteasemusic\\'
        self.isE63 = self.screenwidth == 320
        self.running = 1
        self.canvas = appuifw.Canvas()
        appuifw.app.body = self.canvas
        appuifw.app.screen = 'full'
        appuifw.app.exit_key_handler = self.quit
        self.canvas.bind(appuifw.EEventRedraw, self.handle_redraw)
        self.load_resources()
        self.initialize()

    def quit(self):
        self.running = 0

    def cn(self, x):
        return x.decode('utf8')

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

    def initialize(self):
        self.baseimg = graphics.Image.new(appuifw.screen)
        splash = graphics.Image.new(appuifw.screen)
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
        self.baseimg.clear(0xffffff)
        self.baseimg.blit(self.bgimg)
        if self.isE63:
            self.baseimg.blit(self.iconimg2, target=(11, 28), mask=self.iconimgmask)
        else:
            self.baseimg.blit(self.iconimg2, target=(int(self.screenwidth / 2 - self.iconimg2.size[0] / 2), 66),
                              mask=self.iconimgmask)
        # 把图形画到canvas(画布)上
        self.canvas.blit(self.baseimg)
        # 线程(不是必须)，但最好有延时
        e32.ao_yield()

    def handle_redraw(self, rect):
        self.refresh_screen()

    def run(self):
        while self.running:
            self.refresh_screen()
            e32.ao_sleep(0.1)


if __name__ == "__main__":
    app = MyApp()
    app.run()
