# -*- coding: utf-8 -*-

import sys
import os
import re
import base64
import binascii
import md5
if sys.path[1].find('neteaseDebug') == -1:
    sys.path[1:1] = [os.path.abspath("e:\\neteaseDebug")]
import simplejson as json
usePc=0
try:
    import pyaes as AES
    usePc=1
except:
    import aes as AES
import random

import copy
import StringIO
import httplib
import urllib
import socket

baseUrl='http://music.wmm521.cn:3000/'

try:
    import appuifw2 as appuifw
    import appuifw as appuifw_
    import e32
    import audio
    
except:
    pass
    
import time
from util import *
infoPopup = appuifw_.InfoPopup()
progress = 0
writeprogress = 0
def downProg(n,s,t):
    global progress
    pc = n*s*100/t
    if pc > 100:
        pc=100
    if pc != progress:
        infoPopup.show(cn('↓  ') + u'%s %%' % pc,(0,0), 1000,0, appuifw_.EHCenterVTop)
    progress = pc
    e32.ao_yield()
    
def writeProg(n,s,t):
    global writeprogress
    pc = n*s*100/t
    if pc > 100:pc=100
    if pc != writeprogress:
        infoPopup.show(cn('○  ') + u'%s %%' % pc,(0,0), 1000,0, appuifw_.EHCenterVTop)
    writeprogress = pc
    e32.ao_yield()

def cookie2Dict(str1):return dict([(x.replace(' ','').split('=') + [''])[0:2] for x in re.split(',|;', str1)])
def dict2Cookie(dict1):return ';'.join([a + '=' + b for a,b in dict1.items()])
def aesEncrypt(text, secKey):
    t = type(text)
    if(type(text)==type(u"")):
        text = text.encode('u8')
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    # encryptor = AES.new(secKey, 2, '0102030405060708')
    # ciphertext = encryptor.encrypt(text)
    # ciphertext = base64.b64encode(ciphertext)
    # return ciphertext.decode()
    if(usePc):
        encrypter = AES.Encrypter(AES.AESModeOfOperationCBC(secKey, '0102030405060708'))
        ciphertext = encrypter.feed(text)
        ciphertext += encrypter.feed()
        ciphertext = base64.encodestring(ciphertext).replace('\n', '')
        return ciphertext.decode()
    else:
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.encodestring(ciphertext).replace('\n','')
        return ciphertext.decode()

def modpow(base, exponent, mod):
    ans = 1
    index = 0
    while(1 << index <= exponent):
        if(exponent & (1 << index)):
            ans = (ans * base) % mod
        index += 1
        base = (base * base) % mod
    return ans

def rsaEncrypt(text, pubKey, modulus):
    textRvs=""
    for x in text:
        textRvs = x + textRvs
    text = textRvs.encode()
    rs = modpow(long(binascii.hexlify(text), 16), long(pubKey, 16), long(modulus, 16))
    return ('%x' % rs).zfill(256)



def createSecretKey(size):
    return ''.join( [ hex(random.randint(1,255))[2:] for x in range(16) ] )[0:16]

def getParams(paramsData):
    modulus = 'E0B509F6259DF8642DBC35662901477DF22677EC152B5FF68ACE615BB7B725152B3AB17A876AEA8A5AA76D2E417629EC4EE341F56135FCCF695280104E0312ECBDA92557C93870114AF6C9D05C4F7F0C3685B7A46BEE255932575CCE10B424D813CFE4875D3E82047B97DDEF52741D546B8E289DC6935B3ECE0462DB0A22B8E7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(paramsData)
    secKey = createSecretKey(16)
    #secKey = "7874369994448f96"
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data
    
#代码来自http://github.com/yanunon/NeteaseCloudMusic
#根据音乐的dfsId在本地算出音乐的url
def encDfsId(dfsId):
    magic = str('3go8&$8*3*3h0k(2)2')
    song_id = str(dfsId)
    song_id_ = ''
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id_ += chr(ord(sid) ^ ord(magic[i % magic_len]))
    m_ = md5.new()
    m_.update(song_id_)
    m = m_.digest()

    result = m.encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

def encMp3Url(dfsId):
    encdfsid = encDfsId(dfsId)
    mp3Url = "http://p%s.music.126.net/%s/%s.mp3" % (random.randint(1,4), encdfsid, dfsId)
    return mp3Url
    
def getUrlBySongDict(song, br, mode1=False):
    bpsKeyList = ['b', 'l', 'm', 'h']
    bpsKey = 0
    if br > 96000:bpsKey = 1
    if br > 128000:bpsKey = 2
    if br > 160000:bpsKey = 3
    
    url = ''
    
    if br <= 128000:
        url = song.get('mp3Url').replace('http://m', 'http://p')
    
    if not(url):
        if not(mode1):
            def getDfsIdWrapped(bpsKey1):
                dfsDict = song.get('%sMusic' % bpsKeyList[bpsKey1])
                dfsId = 0
                if dfsDict:
                    dfsId = dfsDict.get('dfsId')
                return dfsId
                
            dfsId = getDfsIdWrapped(bpsKey)
            if dfsId == 0:
                dfsId = getDfsIdWrapped(bpsKey-1)
            if dfsId == 0:
                dfsId = getDfsIdWrapped(bpsKey-2)
            if dfsId == 0:
                dfsId = getDfsIdWrapped(bpsKey-3)
            if dfsId != 0:
                url = encMp3Url(dfsId)
            logs('Use Old Api: url = ' + url)
        else:
            url = 'http://p2.music.126.net/rsoHYJSo3I4Dfw10iaKUrg==/5751545324986254.mp3?mark=Failed'

    return url
    
class NEApi:
    def __init__(self, username, password, phone = False, relogin = False, mode1=True):
        self.uid=0
        self.cookie = INIT_COOKIE
        self.updateCookie(self.loadCookie())
        data = json.loads(self.loadUserdata())
        self.updateUid(data)
        self.netFailedCallback = lambda:None
        self.loginSucceed = False
        self.httpResponseCallback = downProg
        self.useNewApi = mode1
        if not(self.checkLogin()) or relogin:
            logs('ReLogin')
            loginCount = 0
            while True:
                if loginCount >= 5:
                    raise Exception, 'Login Failed. Unknown Error2'
                    break
                loginCount +=1
                try:
                    self.login(username, password, phone)
                except Exception, e:
                    printException(Exception, e, cn('在登录时出现了一些问题。用户名或密码错误吗？'))
                    break
                if self.checkLogin():
                    break
    def ProcessCookie(self,ck):
        cks = ck.split('Domain=.music.163.com, ')
        t = ''
        for c in cks:
            t = c.find('MUSIC_U')
            if (t > -1):
                c2 = c[t:].split(';')[0]
                return c2 + ';'
        return ''

    def updateCookie(self, str1):
        str1 = self.ProcessCookie(str1)
        self.cookie = INIT_COOKIE + str1
        #reFind = re.findall(r'(?<=NETEASE\_WDA\_UID=).*(?=#\|)',str1)
        #if reFind:
        #    self.uid=reFind[0]
        #else:
        #    self.uid=0
    
    def rawHttpReq(self, url, method='GET', params='', query='', header=None):
    #发HTTP请求，并返回cookie内容和正文
        if header == None:
            header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.30 Safari/537.36',
                    'Cookie': self.cookie,
                      'Referer': 'http://music.163.com/',
                      'Content-Type':"application/x-www-form-urlencoded"
                      }
        urlhost = url.split('/')[2]
        httpLogs(cn('<Request URI> ') + cn(url))
        httpLogs(cn('<Request Body> ') + cn(params))
        try:
            conn1 = httplib.HTTPConnection(urlhost, 80, 3)
            conn1.request(method, url, params, header)
            resp1=conn1.getresponse()
            totalSize = getIOLength(resp1)
            responseData = StringIO.StringIO()
            callbackWhenRead(resp1, responseData, self.httpResponseCallback, 512, totalSize)
            responseData.seek(0)
            
            result = (resp1.getheader('set-cookie'), responseData.read())
            httpLogs(cn('<Response Cookie> \n') + cn(result[0]))
            httpLogs(cn('<Response Body> \n   Length: ') + unicode(len(result[1])))
            httpLogs(cn('<Response Body> \n  : ') + result[1].decode('u8'))
            conn1.close()
            return result
        except Exception, e:
            printException(Exception,e)
            logs_('SomeProblemsWithHttpRequest')
            self.netFailedCallback()
        
        
        
    def encHttpReq(self, url, params={'':''}):
    #针对网易云网页版新API发加密的POST
        httpLogs(cn('<Encryped Data> ') + cn(urllib.urlencode(params)))
        encParams = getParams(params)
        data=urllib.urlencode(encParams)
        ret=self.rawHttpReq(url, "POST",data )
        return ret
    
    def loadCookie(self):
    #从默认位置载入COOKIE
        if not os.path.exists('e:\\netease\\data\\cookie.txt'):
            file0 = open('e:\\netease\\data\\cookie.txt','wb')
            file0.write('')
            file0.close()
        file1=open('e:\\netease\\data\\cookie.txt','r')
        readCookie = file1.read()
        file1.close()
        return readCookie
        
    def writeCookie(self):
        file1=open('e:\\netease\\data\\cookie.txt','wb')
        file1.write(self.cookie)
        file1.close()
        return None

    def loadUserdata(self):
        if not os.path.exists('e:\\netease\\data\\userdata.txt'):
            file0 = open('e:\\netease\\data\\userdata.txt', 'w')
            file0.write('{}')
            file0.close()
        file1 = open('e:\\netease\\data\\userdata.txt', 'r')
        data = file1.read()
        file1.close()
        return data

    def writeUserdata(self,data):
        file1=open('e:\\netease\\data\\userdata.txt','w')
        file1.write(json.dumps(data))
        file1.close()
        return None

    def checkLogin(self):
        #通过检查个人推荐页的结果是否为200来判定是否登录成功，<并且通过UID检测判断是否同一账号>
        #2022-11-28更新，直接获取用户状态，account不为空是登录成功
        try:
            if json.loads(self.encHttpReq(HOST+'/weapi/w/nuser/account/get', {'':''})[1]).get('account') != None:
                self.loginSucceed = True
                return True
                
            else:
                return False
        except Exception, e:
            printException(Exception, e, cn('在检测登录时出现了一些问题。'))
            return False
    
    def login(self, username, password, phone = False):

        loginSuc = False
        m = md5.new()
        m.update(password.encode())
        pwEnc=m.hexdigest()

        loginDict = {
            'username': username,
            'password': pwEnc,
            'rememberLogin': 'true'
        }
        loginUrl = HOST + '/weapi/login/'
        if phone :
            loginDict = {
                'phone': username,
                'password': pwEnc,
                'rememberLogin': 'true'
            }
            loginUrl = loginUrl + 'cellphone'
        loginCount = 0
        while loginSuc == False:
            if loginCount >= 5:
                raise Exception, 'Login Failed. Unknown Error'
                break
            loginCount += 1
            (loginCookie,loginReads) = self.encHttpReq(loginUrl, loginDict)
            
            loginReads = json.loads(loginReads)
            
            if str(loginReads['code'])=='415':
                captValid = False
                captCount = 0
                while captValid == False :
                    if captCount >= 5:
                        raise Exception, 'Login Failed. IP Frequent and Many Wrong Captcha'
                        break
                    download(HOST + '/captcha?id=' + loginReads['captchaId'], 'E:\\netease\\data\\captcha.png',ck=self.cookie)
                    inputCapt = appuifw.query(cn('请输入E:\\netease\\data\\captcha.png中的验证码：'), 
                     'text')
                    captReads = self.encHttpReq(HOST + '/weapi/image/captcha/verify/hf', {'id': loginReads['captchaId'] , 'captcha': inputCapt})[1]
                    captReads = json.loads(captReads)
                    if str(captReads['result'])=='True':captValid = True
                    captCount += 1
            elif str(loginReads['code'])=='200':
                loginSuc = True
            else:
                raise Exception, 'Login Failed. Wrong Username or Password?'
        self.updateUid(loginReads)
        self.updateCookie(INIT_COOKIE + loginCookie)
        self.writeCookie()
        self.writeUserdata(loginReads)
        return None
    def updateUid(self,data):
        if('account' in data and 'id' in data['account']):
            self.uid = data['account']['id']
        else:
            self.uid = 0

    def dailySign(self):
        try:
            signUrl = HOST + '/weapi/point/dailyTask'
            signResult = json.loads(self.encHttpReq(signUrl, {'type': 0 })[1])
            return signResult
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithdailySign'))
        
    
    def getUserPLs(self, uid = 0, offset=0, limit=1000):
        try:
            if not uid:
                uid = self.uid
            uplUrl = HOST + '/api/user/playlist/?offset=%s&limit=%s&uid=%s' % (offset, limit, uid)
            return json.loads(self.rawHttpReq(uplUrl)[1])
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetUserPLs'))
        
    def getRecomPL(self):
        try:
            recUrl = HOST + '/weapi/v1/discovery/recommend/songs?csrf_token='
            recomResult = self.encHttpReq(recUrl, {'': ''})[1]
            recomResult_ = json.loads(recomResult)['recommend']
            return recomResult_
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetRecomPL'))

    # def getFML(self):
        # recUrl = HOST + '/api/radio/get'
        # return json.loads(self.rawHttpReq(recUrl)[1])
    def getFML(self, limit = 3):
        try:
            recReq = {'limit': limit}
            # recReq = {}
            recUrl = HOST + '/api/radio/get'
            return json.loads(self.encHttpReq(recUrl, recReq)[1])
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetFML'))
        
    def fmLike(self, songId, like=True, time=0, alg='itembased'):
        try:
            likeUrl = HOST + '/api/radio/like?alg=%s&trackId=%s&like=%s&time=%s' % (alg, songId, like, time)
            likeResult = json.loads(self.rawHttpReq(likeUrl)[1])
            if likeResult['code'] == 200:
                return likeResult
            else:return -1
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithfmLike'))
        
    def fmTrash(self, songId, time=0, alg='RT'):
        try:
            trashUrl = HOST + '/api/radio/trash?alg=%s&songId=%s&time=%s' % (alg, songId, time)
            trashResult = json.loads(self.rawHttpReq(trashUrl)[1])
            if trashResult['code'] == 200:
                return trashResult
            else:return -1
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithfmTrash'))
        
    def getPlaylist(self, plId, useDownload = True, forceRefresh = True):
        global progress,writeprogress
        
        
        try:
            plPath = u'e:\\netease\\cache\\playlist\\playlist_%s.txt'%plId
            plUrl = HOST + '/api/v6/playlist/detail?id=%s' % (plId)
            if not useDownload:return json.loads(self.rawHttpReq(plUrl)[1])['playlist']
            
            if forceRefresh or not(os.path.exists(plPath)):
                download(plUrl, plPath, downProg, lambda:None, writeProg,ck=self.cookie)
            infoPopup.hide()
            file1 = open(plPath, 'r')
            content = json.loads(file1.read())['playlist']
            file1.close()
            return content
            
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetPlaylist'))
            
    def like(self, songId, like=True, time=25, alg='itembased'):
        try:
            likeUrl = HOST + '/api/radio/like?alg=%s&trackId=%s&like=%s&time=%s' % (alg, songId, ['false','true'][like], time)
            return json.loads(self.rawHttpReq(likeUrl)[1])
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithlike'))
           
    def favorPlaylist(self, playlistId):
        try:
            favorUrl = HOST + "/weapi/playlist/subscribe?csrf_token="
            csrf = cookie2Dict(self.cookie)['__csrf']
            logs('csrf : ' + csrf)
            favorUrl += csrf
            favorReq = {'id':playlistId, 'csrf_token':csrf}
            # favorReq = {'id':playlistId}
            return json.loads(self.encHttpReq(favorUrl, favorReq)[1])['code']
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithfavorPlaylist'))
       
     
    '''     
        获取歌曲ID列表中每首歌曲的Url（raw仅获取原始json, 未处理）
        两种模式：
        1. 用新API enhance/player/url 获取歌曲url信息（长网址）
             缺点：没法获取到版权/下架歌曲信息 需要发加密post
        2. 用旧API /api/song/detail 提取歌曲url信息(h,m,..)
             若没有url信息，则反查歌曲专辑，会得到歌曲的dfsId，用加密算法得到url （短网址）
        借鉴cunyu loadfield的代码思路
        缺点：将来可能会失效 并且服务器需要从m换成p
        ！！（16.8.31）现在对于高音质来说很大几率无效！！
        ！！！
        目前 选择第二条
        这个函数返回的是一个数组 其上有各mp3的url
    '''

    def getSongsUrl_mode1(self, songIds=[], br  = 96000):
        songsDetailRes = json.loads(self.rawgetSongsUrl(songIds, br))['data']
        songsDetailRes_ = copy.copy(songsDetailRes)
        for x in songsDetailRes:
            i = songIds.index(int(x['id']))
            #待写
            songsDetailRes_[i] = x
        return songsDetailRes_
        
    def getSongsUrl(self, songDict, br=96000):
    #songDict实际上是Dict构成的List
        mode1 = self.useNewApi
        try:
            
            urlList = ['http://p2.music.126.net/rsoHYJSo3I4Dfw10iaKUrg==/5751545324986254.mp3?mark=Failed' for i in range(len(songDict))]
            listToUseOldApi = []
            if mode1:
                logs('useNewApi' )
                newApiResult = self.getSongsUrl_mode1([x['id'] for x in songDict], br)
                for i, j in enumerate(newApiResult):
                    # logs('%s s newapiurl = %s'%(i,j.get('url')))
                    urlList[i] = j.get('url')
                    if not(j.get('url')):
                        #下架
                        logs('Song %s Undercart!' % i)
                        listToUseOldApi.append(i)
            else:
                listToUseOldApi = range(len(songDict))
            
            logs('listToUseOldApi: ' + str(listToUseOldApi))
            if listToUseOldApi != []:
                for i,j in enumerate(listToUseOldApi):
                    if False and songDict[j].get('mp3Url') and songDict[j].get('lMusic'):
                        #can be searched
                        #old api dead. no hope for getting url by mp3url or dfsid
                        url = getUrlBySongDict(songDict[j], br)
                        
                    else:
                        logs('%s cannot be searched! use album'%(j))
                        url = self.getUrlByAlbum(songDict[j]['id'], songDict[j]['album']['id'], br)
                    if url != '': urlList[j] = url.replace(u'http://m', u'http://p')
                    # logs('%s s oldapiurl = %s'%(j,urlList[j]))
                    
            return urlList
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetSongsUrl'))
        
    def getUrlByAlbum(self, songId, albumId, br):
        albumDict = json.loads(self.rawgetAlbum(albumId))
        url = ''
        if albumDict.get('code') != 200: return url
        for song in albumDict['album']['songs']:
            if song['id'] == songId:
                url = getUrlBySongDict(song, br)
        return url
    #可以获取详细信息（获取歌曲ID列表中每首歌曲的详细信息，有可能出现查不到Url的情况）
    def getSongsDetail(self, songIds=[]):
        try:
            songsDetailRes = json.loads(self.rawgetSongsDetail(songIds))['songs']
            songsDetailRes_ = copy.copy(songsDetailRes)
            for x in songsDetailRes:
                try:
                    i = songIds.index(x['id'])
                except:
                    pass
                try:
                    i = songIds.index(str(x['id']))
                except:
                    pass
                songsDetailRes_[i] = x
            return songsDetailRes_
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetSongsDetail'))
        
    # def getSongsDetail_(self, songIds=[]):
        # return [self.getSongDetail_(x) for x in songIds]
        
    def getSongDetail_(self, songId):
        songsDetailUrl = HOST  + '/api/song/detail?ids=[%s]'%songId
        (urlCookie, urlReads) = self.rawHttpReq(songsDetailUrl)
        return json.loads(urlReads)['songs'][0]
        
    def getSongUrl(self, songId, br  = 96000):
        return self.getSongDetail(songId, br)['url']
        
    def getSongLyric(self, songId):
        try:
            hasLyric  = False
            hasTLyric  = False
            lyricUrl = HOST + '/api/song/lyric?id=%s&lv=-1&kv=-1&tv=-1' % (songId)
            rawResult = self.rawHttpReq(lyricUrl)[1]
            lyricResult = json.loads(rawResult)
            if 'lrc' in lyricResult and 'lyric' in lyricResult['lrc'] and lyricResult['lrc']['lyric']:
                hasLyric = lyricResult['lrc']['lyric']
            if 'tlyric' in lyricResult and 'lyric' in lyricResult['tlyric'] and lyricResult['tlyric']['lyric']:
                hasTLyric = lyricResult['tlyric']['lyric']
            return (lyricResult, hasLyric, hasTLyric)
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetSongLyric'))
        
    def getComments(self, songId, commentThreadId = '_', offset=0, total=False, limit=10):
        try:
            #此处commentThreadId赋值为R_AL_3_XXX之类的可以获取其他种类的评论(歌手/专辑/歌单)
            if commentThreadId == '_':
                commentThreadId = 'R_SO_4_%s' % songId
            commUrl = HOST + '/weapi/v1/resource/comments/%s' % commentThreadId
            commReq = {
            'offset' : offset,
            'total' : total,
            'limit' : limit
            }
            (commCookie, commResult) = self.encHttpReq(commUrl, commReq)
            commResult = json.loads(commResult)
            hotCommList = commResult.get('hotComments')
            ordCommList = commResult.get('comments')
            totalNum = commResult.get('total')
            haveMore = commResult.get('more')
            return (hotCommList, ordCommList, totalNum, haveMore)
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithgetComments'))
        
    def favorComment(self, commentId, threadId, favor = True):
        try:
            #必须提供threadId，否则按默认的歌曲来
            favorReq = {
            'commentId' : commentId,
            'threadId' : threadId,
            'like' : favor
            }
            favorUrl = HOST + '/weapi/v1/comment/%slike' % ('un','')[favor]
            favorResult = json.loads(self.encHttpReq(favorUrl, favorReq)[1])
            message = u''
            favorSuc = False
            if 'message' in favorResult:
                message = favorResult['message']
            else:
                message = str(favorResult.get('code'))
                if favorResult.get('code') == 200:
                    favorSuc = True
            return (favorSuc, message)
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithfavorComment'))
            
    #add: 添加
    
    #502返回码：歌曲已经存在
    #成功：{"trackIds":"[715785]","code":200,"count":31,"cloudCount":0}
    
    #del: 删除
    #成功：{"code":200,"count":30,"cloudCount":0}
    #失败：好像仍是返回200？
    def manipulatePlaylist(self, plId, songIDList, operation):
        try:
            #必须提供threadId，否则按默认的歌曲来
            manReq = {
            'op' : operation,
            'pid' : plId,
            'trackIds' : u'[%s]' % (u','.join([unicode(x) for x in songIDList])),
            'tracks' : '[object Object]'
            }
            manUrl = HOST + '/weapi/playlist/manipulate/tracks'
            manResult = json.loads(self.encHttpReq(manUrl, manReq)[1])
            if manResult['code'] == 200:
                return -1
                #-1表示成功
            else:
                return manResult['code']
                #否则返回错误码
            
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithmanipulatePlaylist'))
            
    def createPlaylist(self, name, songIDList = []):
        try:
            #必须提供threadId，否则按默认的歌曲来
            createReq = {
            'name' : name,
            }
            createUrl = HOST + '/weapi/playlist/create'
            createResult = json.loads(self.encHttpReq(createUrl, createReq)[1])
            if createResult['code'] == 200:
                if songIDList:
                    manRes = self.manipulatePlaylist(createResult['id'],songIDList, 'add')
                    if manRes != -1: raise Exception, manRes
                return -1
            else:
                raise Exception, createResult['code']
                
            
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithmanipulatePlaylist'))
            return e
            
    #1 单曲
    #10 专辑
    #100 歌手
    #1000 歌单
    #1002 用户
    def search(self, keyword, type, limit=10, offset=0):
    #待改进API，旧的API只能显示10条
        try:
            #必须提供threadId，否则按默认的歌曲来
            searchReq = {
            's' : keyword,
            'type' : type,
            'limit' : limit,
            'offset' : offset
            }
            searchURL = HOST + '/api/search/get'
            searchResult = json.loads(self.rawHttpReq(searchURL, 'POST', urllib.urlencode(searchReq))[1])['result']
            
            return searchResult
            
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithsearch'))
        
    
   # ---
    def rawgetUserPLs(self, uid = 0, offset=0, limit=10):
        if uid ==  0:
            uid = self.uid
        uplUrl = HOST + '/api/user/playlist/?offset=%s&limit=%s&uid=%s' % (offset, limit, uid)
        return self.rawHttpReq(uplUrl)[1]
        
    def rawgetRecomPL(self):
        recUrl = HOST + '/weapi/v1/discovery/recommend/songs?csrf_token='
        return self.encHttpReq(recUrl, {'': ''})[1]

    def rawgetFML(self):
        recUrl = HOST + '/api/radio/get'
        return self.rawHttpReq(recUrl)[1]
       
    def rawfmLike(self, songId, like=True, time=0, alg='itembased'):
        likeUrl = HOST + '/api/radio/like?alg=%s&trackId=%s&like=%s&time=%s' % (alg, songId, like, time)
        likeResult = self.rawHttpReq(likeUrl)[1]
        return likeResult

        
    def rawfmTrash(self, songId, time=0, alg='RT'):
        trashUrl = HOST + '/api/radio/trash?alg=%s&songId=%s&time=%s' % (alg, songId, time)
        trashResult = self.rawHttpReq(trashUrl)[1]
        return trashResult
        
    def rawgetPlaylist(self, plId):
        plUrl = HOST + '/api/playlist/detail?id=%s' % (plId)
        return self.rawHttpReq(plUrl)[1]
    
    
    #rawgetSongsDetail: 获取歌曲ID列表中每首歌曲的详细信息，有可能出现查不到Url的情况
    
    def rawgetSongsDetail(self, songIds=[]):
        songsDetailUrl = HOST  + '/api/song/detail?ids=[%s]' % ','.join([str(songid) for songid in songIds])
        (urlCookie, urlReads) = self.rawHttpReq(songsDetailUrl)
        # (urlCookie, urlReads) = self.encHttpReq(HOST  + '/weapi/song/enhance/player/url?csrf_token=', mp3UrlReq)
        return urlReads
        
    #rawgetSongsUrl:
    #获取歌曲ID列表中每首歌曲的Url（raw仅获取原始json未处理）
    #是采取上述的模式1 现在暂时用不到
    def rawgetSongsUrl(self, songIds=[], br=96000):
        mp3UrlReq = {
            'ids' : songIds,
            'br' : br
        }
        (urlCookie, urlReads) = self.encHttpReq(HOST  + '/weapi/song/enhance/player/url?csrf_token=', mp3UrlReq)
        return urlReads
        
    #weapi v2版的 songdetail api，暂时用不上
    def newrawgetSongDetail(self, songId, br  = 96000):
        mp3UrlReq = {
        'ids' : [songId],
        }
        (urlCookie, urlReads) = self.encHttpReq(HOST  + '/weapi/v1/song/detail', mp3UrlReq)
        # (urlCookie, urlReads) = self.rawHttpReq(HOST  + '/api/v2/song/detail', 'POST',  mp3UrlReq)
        # return json.loads(urlReads)['data'][0]
        return urlReads
        
    def rawgetSongLyric(self, songId):
        hasLyric  = False
        hasTLyric  = False
        lyricUrl = HOST + '/api/song/lyric?id=%s&lv=-1&kv=-1&tv=-1' % (songId)
        RAWRESULT = self.rawHttpReq(lyricUrl)[1]
        # if 'lrc' in lyricResult and lyricResult['lrc']['lyric'] is not None:
            # hasLyric = True
        # if 'tlyric' in lyricResult and lyricResult['tlyric']['lyric'] is not None:
            # hasTLyric = True
        return RAWRESULT
    def rawgetComments(self, songId, commentThreadId = '_', offset=0, total=False, limit=10):
        if commentThreadId == '_':
            commentThreadId = 'R_SO_4_%s' % songId
        commUrl = HOST + '/weapi/v1/resource/comments/%s' % commentThreadId
        commReq = {
        'offset' : offset,
        'total' : total,
        'limit' : limit
        }
        (commCookie, commReads) = self.encHttpReq(commUrl, commReq)
        return commReads
    def rawgetAlbum(self, albumId):
        albumUrl = HOST + '/api/album/%s?id=%s' % (albumId, albumId)
        return self.rawHttpReq(albumUrl)[1]

if __name__ == '__main__':
    newapi = NEApi('','',True,True)

