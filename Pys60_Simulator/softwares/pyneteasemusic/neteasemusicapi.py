# -*- coding: utf-8 -*-
import appuifw
# 导入所需库
import httplib
from urlparse import urlparse
import socket
import time
import simplejson as json
import qrcode

def getTs():
    return str(int(time.time()*1000))

_BaseUri = 'http://music.zixing.fun:3000'

def send_request(url, method, postdata=None, headers={}):
    parsed_url = urlparse(url)
    if parsed_url.scheme == "https":
        conn = httplib.HTTPSConnection(parsed_url.hostname,  parsed_url.port or 443)
    else:
        conn = httplib.HTTPConnection(parsed_url.hostname, parsed_url.port or 80)

    headers = {}
    if method == "POST" and postdata is not None:
        #headers["Content-Type"] = "application/json"
        headers["Content-Length"] = len(postdata)

    conn.request(method, url,postdata,headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def GET(url):
    return send_request(url,"GET")

def POST(url,postdata):
    headers = {}
    headers["Content-Type"] = "application/json"
    return send_request(url,"POST",postdata,headers)

def testconnect():
    try:
        aps = socket.access_points()
        testurl = _BaseUri+'/ping'
        ret = GET(testurl)
        print(ret)
        if(len(ret)>0):
            return True
        else:
            return False
    except Exception:
        #print(ex)
        return False

class MyApi:
    def __init__(self,baseurl = ''):
        if(baseurl==''):
            self.BaseUrl = _BaseUri
        else:
            self.BaseUrl = baseurl

    def getUrl(self,uri):
        return self.BaseUrl+uri

    def qrKey(self):
        url = self.getUrl("/login/qr/key?timestamp="+getTs())
        ret = GET(url)
        jsonret = json.loads(ret)
        return jsonret

    def qrCreate(self,key):
        url = self.getUrl("/login/qr/create?key="+key+"&timestamp="+getTs())
        ret = GET(url)
        jsonret = json.loads(ret)
        return jsonret

    def qrCheck(self,key):
        url = self.getUrl("/login/qr/check?key="+key+"&timestamp="+getTs())
        ret = GET(url)
        jsonret = json.loads(ret)
        return jsonret
    def p(self):
        pass

def testQrLogin():
    myapi = MyApi()
    keyret = myapi.qrKey()
    key = keyret['data']['unikey']
    dataret = myapi.qrCreate(key)
    qrurl = dataret['data']['qrurl']
    qr = qrcode.QRCode(box_size=1,border=2)
    qr.add_data(qrurl)
    img = qr.make_image()
    img.save('1.jpg')
    while(1):
        #等待扫码 {u'message': u'\u7b49\u5f85\u626b\u7801', u'code': 801L, u'cookie': u''}
        #授权中 {u'cookie': u'', u'message': u'\u6388\u6743\u4e2d', u'code': 802L, u'nickname': u'Light_\u7d2b\u661f', u'avatarUrl': u'https://p1.music.126.net/iMTbuUzrousRWFgkQTFQCg==/18612532836719726.jpg'}
        #授权登陆成功 {u'message': u'\u6388\u6743\u767b\u9646\u6210\u529f', u'code': 803L, u'cookie': u'xxx'}
        #二维码不存在或已过期{u'message': u'\u4e8c\u7ef4\u7801\u4e0d\u5b58\u5728\u6216\u5df2\u8fc7\u671f', u'code': 800L, u'cookie': u''}
        checkret = myapi.qrCheck(key)
        print(checkret)
        print(checkret['message'])
        time.sleep(1)

if __name__ == '__main__':
    testQrLogin()
