# -*- coding: utf-8 -*-
import appuifw
# 导入所需库
import httplib
from urlparse import urlparse
import socket
import json

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

    conn.request(method, parsed_url.path,postdata,headers)
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
        testurl = _BaseUri
        ret = GET(testurl)
        print(ret)
        if(len(ret)>0):
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False

if __name__ == '__main__':
    testconnect()

