# -*- coding: utf-8 -*-
import requests
from myjson import json

class Tops:
    def __init__(self,data):
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
    def __init__(self,data):
        self.toplist = []
        self.newslist=[]
        for i in data['toplist']:
            self.toplist.append(Tops(i))
        for i in data['newslist']:
            self.newslist.append(News(i))
class Slide:
    def __init__(self,data):
        self.title = data['title']
        self.starttime = data['starttime']
        self.endtime = data['endtime']

        self.endtime = data['endtime']

        self.link = data['link']
        self.opentype = data['opentype']
        self.device = data['device']
        self.device = data['image']

class IthomeNet:
    def __init__(self):
        self.urlhead = 'http://api.ithome.com/'
        self.newsListUrl = self.urlhead +'json/newslist/news?r=0'
        self.slideUrl =self.urlhead + 'json/slide/index'
    def get(self,url):
        return requests.get(url).text

    def getNewList(self): #新闻列表
        return NewList(json.loads(self.get(self.newsListUrl)))

    def getSlide(self): #顶部滚动
        return [Slide(i) for i in json.loads(self.get(self.slideUrl))]


if(__name__ == '__main__'):
    ithomenet = IthomeNet()
    t = ithomenet.getSlide()
    print(t)
