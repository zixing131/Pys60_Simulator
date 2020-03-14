# -*- coding: utf-8 -*-
# import requests
import urllib, e32
import hashlib
import os
import graphics as ph
import simplejson as json
import thread

mypath = u"..\\python\\pysoft\\ithome\\"
if (os.name != 'nt'):
    mypath = u"e:\\python\\pysoft\\ithome\\"
cachePath = mypath + "cache\\"


class Tops:
    def __init__(self, data):
        self.live = data.has_key('live') and data['live'] or 0
        self.client = data['client']
        self.device = data['device']

        self.topplat = data['topplat']
        self.newsid = data['newsid']
        self.postdate = data['postdate']
        self.orderdate = data['orderdate']
        self.description = data['description']
        self.image = data['image']
        self.hitcount = data['hitcount']
        self.commentcount = data['commentcount']
        self.cid = data['cid']
        self.sid = data['sid']
        self.url = data['url']


class News:
    def __init__(self, data):
        self.newsid = data['newsid']
        self.title = data['title']
        self.postdate = data['postdate']
        self.orderdate = data['orderdate']
        self.description = data['description']
        self.image = data['image']
        self.hitcount = data['hitcount']
        self.commentcount = data['commentcount']

        self.cid = data['cid']
        self.sid = data['sid']
        self.url = data['url']


class NewList:
    def __init__(self, data):
        self.toplist = []
        self.newslist = []
        for i in data['toplist']:
            self.toplist.append(Tops(i))
        for i in data['newslist']:
            self.newslist.append(News(i))


class Slide:
    def __init__(self, data):
        self.title = data['title']
        self.starttime = data['starttime']
        self.endtime = data['endtime']

        self.endtime = data['endtime']

        self.link = data['link']
        self.opentype = data['opentype']
        self.device = data['device']
        self.image = data['image']


class IthomeNet:
    def __init__(self):
        self.imglist = {}
        self.urlhead = 'http://api.ithome.com/'
        self.newsListUrl = self.urlhead + 'json/newslist/news?r=0'
        self.slideUrl = self.urlhead + 'json/slide/index'
        self.newsCornor = 2
        self.newImgHeight = 0
        self.newImgWidth = 0
        self.SlideHeight = 0
        self.SlideWidth = 0
        self.newslist = []
        self.slidelist = []
        self.th1 = e32.Ao_timer()
        self.th2 = e32.Ao_timer()
        self.errorImg = None
        self.asyncLoad = None
        self.imgcount = 0
        self.nowimgindex = 0

    def get(self, url):
        return urllib.urlopen(url).read()

    def asyncLoadChange(self,precent):
        if(self.asyncLoad):
            #print precent
            self.asyncLoad(precent)

    def getImageAsync(self):
        if(self.newslist==[]):
            return
        for i in self.newslist.newslist:
            imgurl = i.image
            # print imgurl
            self.getPic(imgurl, (self.newImgWidth, self.newImgHeight))
            self.nowimgindex += 1
            p = (float(90)/float(self.imgcount)) * self.nowimgindex + 10
            self.asyncLoadChange(p)


    def getSlideImageAsync(self):
        if (self.slidelist == []):
            return
        for i in self.slidelist:
            imgurl = i.image
            self.getPic(imgurl, (self.SlideWidth, self.SlideHeight))
            self.nowimgindex += 1
            p = (float(90) / float(self.imgcount)) * self.nowimgindex + 10
            self.asyncLoadChange(p)


    def getNewList(self):  # 鏂伴椈鍒楄〃
        t = self.get(self.newsListUrl)
        # t = open("e:\\1濉炵彮QQ\\ithome\\data\\newlist.txt", "rb").read()
        t = NewList(json.loads(t))
        # thread.start_new_thread(self.getImageAsync,(t,))
        self.newslist = t
        return t

    def getSlide(self):  # 椤堕儴婊氬姩
        t = self.get(self.slideUrl)
        # t = open("e:\\1濉炵彮QQ\\ithome\\data\\slide.txt", "rb").read()
        t = [Slide(i) for i in json.loads(t)]
        self.slidelist = t
        return t

    def getMd5(self, data):
        hash = hashlib.md5()
        hash.update(data)
        return hash.hexdigest()

    def Url2FileName(self, url):
        return self.getMd5(url)

    def getLocalPic(self, key):
        if (self.imglist.has_key(key)):
            return self.imglist[key]
        return None

    def loadImg(self,AsyncLoad):
        self.asyncLoad = AsyncLoad
        self.imgcount = len(self.newslist.newslist) + len(self.slidelist)
        self.th1.after(0, self.getImageAsync)
        self.th2.after(0, self.getSlideImageAsync)

    def getPic(self, picurl, size):
        if(self.errorImg == None):
            self.errorImg = ph.Image.open(mypath + "error_image.jpg").resize((self.newImgWidth, self.newImgHeight))
        key = self.Url2FileName(picurl)
        t = self.getLocalPic(key)
        if (t != None):
            return t
        imgpath = cachePath + key + ".jpg"
        # imgpath = cachePath + "02365e66cb2e9ef6e27a1f0c24af90a3.jpg"
        # return imgpath
        try:
            if (os.path.exists(imgpath)):
                f = open(imgpath,'rb')
                data = f.read(2)
                f.close()
                if(data=='' or data==None or data.encode('hex').lower()!='ffd8'):
                    req = urllib.urlopen(picurl)
                    img = req.read()
                    open(imgpath, 'wb').write(img)
                    t1 = ph.Image.open(imgpath)
                    t = t1.resize(size)
                    del t1
                    t.save(imgpath)
                    self.imglist[key] = t
                    del t
                    return self.imglist[key]
                t1 = ph.Image.open(imgpath)
                t = t1.resize(size)
                del t1
                self.imglist[key] = t
                del t
                return self.imglist[key]
            req = urllib.urlopen(picurl)
            img = req.read()
            open(imgpath, 'wb').write(img)
            t1 = ph.Image.open(imgpath)
            t = t1.resize(size)
            del t1
            t.save(imgpath)
            self.imglist[key] = t
            del t
            return self.imglist[key]
        except:
            self.errorImg.resize(size)
            self.imglist[key] = self.errorImg
            return self.errorImg


if (__name__ == '__main__'):
    ithomenet = IthomeNet()
    t = ithomenet.getSlide()
    ithomenet.loadImg()
    print(t)
