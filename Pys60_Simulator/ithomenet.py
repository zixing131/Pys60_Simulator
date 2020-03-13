# -*- coding: utf-8 -*-
# import requests
import urllib
import hashlib
import os
import graphics as ph
import simplejson as json

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

    def get(self, url):
        return urllib.urlopen(url).read()

    def getNewList(self):  # 新闻列表
        t=self.get(self.newsListUrl)
        #t = open("e:\\1塞班QQ\\ithome\\data\\newlist.txt", "rb").read()

        return NewList(json.loads(t))

    def getSlide(self):  # 顶部滚动
        t=self.get(self.slideUrl)
        #t = open("e:\\1塞班QQ\\ithome\\data\\slide.txt", "rb").read()
        return [Slide(i) for i in json.loads(t)]

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

    def getPic(self, picurl, size):
        key = self.Url2FileName(picurl)
        t = self.getLocalPic(key)
        if (t != None):
            return t
        imgpath = cachePath + key + ".jpg"
        # imgpath = cachePath + "02365e66cb2e9ef6e27a1f0c24af90a3.jpg"
        # return imgpath
        if (os.path.exists(imgpath)):
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
        self.imglist[key] = t
        del t
        return self.imglist[key]


if (__name__ == '__main__'):
    ithomenet = IthomeNet()
    t = ithomenet.getNewList()
    print(t)
