# -*- coding: utf-8 -*-
# import requests
import urllib, e32
import hashlib
import httplib
import os
import graphics as ph
import simplejson as json
import thread

import mypath
mypath = mypath.getmypath("\\python\\pysoft\\ithome\\")

cachePath = mypath + "cache\\"


class Tops:
    def __init__(self, data):
        self.live = data.has_key('live') and data['live'] or 0
        self.client = data['client']
        self.device = data['device']

        self.topplat = data['topplat']
        self.title = data['title']
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
    def __init__(self, data=None):
        if(data == None):
            return
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
        self.istop = 0

    def convert(self,top):
        self.newsid = top.newsid
        self.title = top.title
        self.postdate = top.postdate
        self.orderdate = top.orderdate
        self.description =  top.description
        self.image = top.image
        self.hitcount = top.hitcount
        self.commentcount = top.commentcount

        self.cid = top.cid
        self.sid = top.sid
        self.url = top.url
        self.istop = 1


class NewList:
    def __init__(self, data):
        self.toplist = []
        self.newslist = []
        for i in data['toplist']:
            self.toplist.append(Tops(i))
        for i in data['newslist']:
            self.newslist.append(News(i))

class NewsContent:
    def __init__(self ,data):
        self.success = data['success']
        self.newssource = data['newssource']
        self.newsauthor = data['newsauthor']
        self.keyword = data['keyword']
        self.btheme = data['btheme']
        self.detail = data['detail']

        self.z = data['z']



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
        self.host="api.ithome.com"
        self.newsListUrl = '/json/newslist/news?r=0'
        self.slideUrl = '/json/slide/index'
        self.newsContentUrl ='/json/newscontent/'
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
        self.newsLoadingImg = None
        self.slideLoadingImg = None
        self.asyncLoad = None
        self.imgcount = 0
        self.nowimgindex = 0
        self.loadingPrecent = 0
        self.nowUrl = ['',(200,200)]

    def get(self, url):
        conn = httplib.HTTPConnection(self.host)
        conn.request('GET', url)
        t=conn.getresponse().read()
        conn.close()
        return t

    def asyncLoadChange(self,precent):
        pass
        #self.loadingPrecent = precent

    def getImageAsync(self):
        if(self.newslist==[]):
            return
        for i in self.newslist.newslist:
            imgurl = i.image
            # print imgurl
            self.savePic(imgurl, (self.newImgWidth, self.newImgHeight))
            self.nowimgindex += 1
            p = (float(90)/float(self.imgcount)) * self.nowimgindex + 10
            self.asyncLoadChange(p)
            self.nowUrl = [imgurl, (self.newImgWidth, self.newImgHeight)]


    def getSlideImageAsync(self):
        if (self.slidelist == []):
            return
        for i in self.slidelist:
            imgurl = i.image
            self.savePic(imgurl, (self.SlideWidth, self.SlideHeight))
            self.nowimgindex += 1
            p = (float(90) / float(self.imgcount)) * self.nowimgindex + 10
            self.asyncLoadChange(p)
            self.nowUrl = [imgurl,(self.SlideWidth, self.SlideHeight)]


    def getNewList(self): 
        t = self.get(self.newsListUrl)
        # t = open("e:\\1塞班QQ\\ithome\\data\\newlist.txt", "rb").read()
        t = NewList(json.loads(t))
        # thread.start_new_thread(self.getImageAsync,(t,))

        for i in range(len(t.toplist)):
            tt = News()
            tt.convert(t.toplist[i])
            t.newslist.insert(i,tt)
        self.newslist = t
        return t

    def getNewsContent(self,newsid):
        t = self.get(self.newsContentUrl+str(newsid))
        t = NewsContent(json.loads(t))
        return t

    def getSlide(self):  
        t = self.get(self.slideUrl)
        # t = open("e:\\1塞班QQ\\ithome\\data\\slide.txt", "rb").read()
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

    def loadImg(self): 
        self.loadingPrecent = 10
        self.imgcount = len(self.newslist.newslist) + len(self.slidelist)
        #self.getImageAsync()
        thread.start_new_thread(self.getImageAsync,())
        #self.th1.after(0, self.getImageAsync)
        #self.getSlideImageAsync()
        thread.start_new_thread(self.getSlideImageAsync,())
        #self.th2.after(0, self.getSlideImageAsync)
        self.loadingPrecent = 100

    def savePic(self, picurl, size): 
        key = self.Url2FileName(picurl)
        t = self.getLocalPic(key)
        if (t != None):
            return
        imgpath = cachePath + key + ".jpg"
        # imgpath = cachePath + "02365e66cb2e9ef6e27a1f0c24af90a3.jpg"
        # return imgpath
        try: 
            img = self.get(picurl) 
            open(imgpath, 'wb').write(img) 
            return
        except:
            return

    def resizePic(self,picurl,size):
        if (self.errorImg == None):
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
                f = open(imgpath, 'rb')
                data = f.read(2)
                f.close()
                if (data == '' or data == None or data.encode('hex').lower() != 'ffd8'):
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

        except:
            self.errorImg.resize(size)
            self.imglist[key] = self.errorImg
            return self.errorImg

    def getLocalPicByUrl(self,picurl,typ): #1 ： newsLoadingImg ， 2：slideLoadingImg
        if(self.newsLoadingImg==None):
            self.newsLoadingImg = ph.Image.open(mypath + "image_loading.jpg").resize((self.newImgWidth, self.newImgHeight))
        if (self.slideLoadingImg == None):
            self.slideLoadingImg = ph.Image.open(mypath + "image_loading2.jpg").resize(
                (self.SlideWidth, self.SlideHeight))
        key = self.Url2FileName(picurl)
        t = self.getLocalPic(key)
        if (t != None):
            return t
        else:
            imgpath = cachePath + key + ".jpg"
            if (os.path.exists(imgpath)):
                try:
                    t1 = ph.Image.open(imgpath)
                    size = (self.newImgWidth, self.newImgHeight)
                    if(typ==2):
                        size = (self.SlideWidth, self.SlideHeight)
                    t = t1.resize(size)
                    del t1
                    self.imglist[key] = t
                    del t
                    return self.imglist[key]
                except:
                    pass
        if(typ == 1):
            return self.newsLoadingImg
        elif(typ==2):
            return self.slideLoadingImg

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
            img = self.get(picurl)
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
    #ithomenet.loadImg()
    print(t)
