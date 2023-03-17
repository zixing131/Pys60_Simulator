# -*- coding: utf-8 -*-
import sys
import os
import time
import copy
import socket
import cfileman
try:
    if sys.path[1].find('neteaseDebug') == -1:
        sys.path[1:1] = [os.path.abspath("e:\\neteaseDebug")]
    import appuifw2 as appuifw, e32, graphics
    import audio
except:
    pass
import api
import random
import simplejson as json
import re

from util import *

#提取有用歌词的正则表达式
#先寻找一个以 [ + 非数字开头的标签框 如[ar:XX] 即\[\D[^\]]*\]
#然后匹配0或任意数量个\n
re1 = re.compile('\[\D[^\]]*\][\n]*(\[\d.*)',re.DOTALL)

#更新版
re2 = re.compile('\[[\d`\:\.]*\].*',re.MULTILINE)

def int2(x):
    try:
        return int(x)
    except:
        return 0

RE_LYRICLINE = re.compile('\[\D[^\]]*\][\n]*(\[\d.*)',re.DOTALL)
RE_LYRICLINE_PATCH_SQUARE_BRACKETS_TEXT = re.compile('\[(?P<text>[^\]]*[^\]\d\:\.]+[^\]]*)\]',re.DOTALL)
RE_LYRICLINE_BETA = re.compile('\[[\d`\:\.]*\].*',re.MULTILINE)
RE_PATH_FILTER = r"[\/:\*\?\"\<\>!\|]|\\"
RE_LYRICLINE_SPLITTING_TIME = r"\[(\d+:\d+(?:\.\d+)?)\]"
RE_LYRICLINE_SPLITTING_CONTENT = r"\[\d+:\d+(?:\.\d+)?\](?!\[\d+:\d+(?:\.\d+)?\])(.*)"

STR_UTF8_BOM = "\xEF\xBB\xBF"

def procLyric(inLyric, testParam = False):
    #先用正则将没用的部分去掉，并用\n分割，留下纯歌词
    #inLyric = re.sub(RE_LYRICLINE_PATCH_SQUARE_BRACKETS_TEXT, ("(\g<text>)"), inLyric)
    trimLrc_findall = RE_LYRICLINE.findall('[mark]' + inLyric)
    if trimLrc_findall == []:
        return []
    trimLrc = trimLrc_findall[0].split(u'\n')
    lrcList = []
    for lrcLine in trimLrc:
        z = []
        z = z + re.findall(RE_LYRICLINE_SPLITTING_TIME,lrcLine)
        z = z + re.findall(RE_LYRICLINE_SPLITTING_CONTENT, lrcLine)
        if len(z) > 1:
            for i in range(0,len(z)-1):
                t = z[i]
                #处理时间，有00:00.920和00:00.92两种格式
                t1 = t.split(u':')
                t2 = t1[1].split('.')
                minute = int("0" + t1[0])
                sec = int("0" + t2[0])
                if(len(t2) > 1):
                    msc = t2[1]
                    if len(msc) == 2:
                        msc = int("0" + msc) * 10
                    else:
                        msc = int("0" + msc)
                else:
                    msc = 0
                totaltime = ((minute*60000) + (sec*1000) + msc)
                lrcList.append(( totaltime , [z[len(z)-1] , ''] ))
    return lrcList
    
def procTLyric(lrcDict, inTLyric, testParam = False):
    trimTLrc_findall = RE_LYRICLINE.findall('[mark]' + inTLyric)
    if trimTLrc_findall == []:
        return {}
    trimTLrc = trimTLrc_findall[0].split(u'\n')
    for lrcLine in trimTLrc:
        z = []
        z = z + re.findall(RE_LYRICLINE_SPLITTING_TIME,lrcLine)
        z = z + re.findall(RE_LYRICLINE_SPLITTING_CONTENT, lrcLine)
        if len(z) > 1:
            for i in range(0,len(z)-1):
                t = z[i]
                #处理时间，有00:00.920和00:00.92两种格式
                t1 = t.split(u':')
                t2 = t1[1].split('.')
                min = int("0" + t1[0])
                sec = int("0" + t2[0])
                if(len(t2) > 1):
                    msc = t2[1]
                    if len(msc) == 2:
                        msc = int("0" + msc) * 10
                    else:
                        msc = int("0" + msc)
                else:
                    msc = 0
                totaltime = ((min*60000) + (sec*1000) + msc)
                if totaltime in lrcDict:
                    lrcDict[totaltime][1] = z[len(z)-1]
    return lrcDict

def finalProcLyric(lrcDict):
    lrcDictKeySorted = list(lrcDict)
    lrcDictKeySorted.sort()
    lrcDictVarSorted = map(lambda x:lrcDict[x], lrcDictKeySorted)
    lrcList = map(lambda x,y:(x,y) , lrcDictKeySorted, lrcDictVarSorted)
    return lrcList
    
#PlayList的任务是对一个指定的网易云歌曲List(如[0,2,3,4,5])进行播放
class Playlist:
    def __init__(self, playlist, apii, order=0, picsize=73, br=96000, volume=1, debugMode = False):
        #该playlist用的api实例
        self.api = apii
        #0 - 列表循环  1 - 单曲循环  2 - 随机播放
        self.order = order
        self.br = br
        self.volume = volume
        #将来可能要实现历史播放功能
        self.historyList = []
        #更新songList，同时获得其详细信息listDetail，并根据order生成playingList
        #若电台或稍后更新playlist，可设置为[]
        self.updateList(playlist)

        #downCallback: 下载文件时候的callback
        #downCallbackWrapper: 下载文件时候的callback的Wrapper，在主程序中给其赋值一个函数，downCallbackWrapper('提示文字')(chunknum,chunksize,totalsize)为urlretreive的回调方式
        #songCallback: self.player的播放状态发生变化时调用的callback
        self.downCallbackWrapper = lambda a:lambda b,c,d:None
        self.writeCallbackWrapper = lambda a:lambda b,c,d:None
        self.songCallback = lambda a,b,c:None
        #设置界面所需的专辑图片尺寸，默认为73
        self.picSize = picsize
        self.isScroll = False
        logs('End Init Playlist')
        self.playCallback = lambda:None
        self.errCallback = lambda:None
        self.player = False
        self.playlistName = cn('歌单')
        self.debugMode = debugMode
        
        #初始参数设置完成
        
    def setPlaylistName(self, name):
        self.playlistName = name
        
    def updateList(self, newList):
        #songList: 输入时的歌单(歌曲Id的数组)，按照默认排序
        self.songList = newList
        self.initOrder()
        if self.songList != []:#非电台模式下（有歌曲），用api中的方法获取各歌曲信息（需不需要再统一获取下载地址？）
            self.listdetail = self.api.getSongsDetail_(self.songList)
            self.getDownloadUrls(self.br)
        else:
            self.listdetail = []
            self.listdown = []
            #电台怎么办？
        logs('End Update List')
    
    def updateListByDict(self, listDict):
        #输入已经获得的歌曲详情列表Dict来更新
        self.songList = [x['id'] for x in listDict]
        self.initOrder()
        if self.songList != []:
            self.listdetail = listDict
            # self.listdown = [x['url'] for x in self.api.getSongsDetail(self.songList)]
            self.getDownloadUrls(self.br)
        else:
            self.listdetail = []
            self.listdown = []
        logs('End Update List By Dict')
            
    def getDownloadUrls(self, br = 96000):
        self.listdown = self.api.getSongsUrl(self.listdetail, self.br)
        logs('End Get Urls')
            
    def initOrder(self, order = -1):
        self.currPos = 0
        #playingIndex: 在实际播放列表playingList中的索引号
        #songIndex: 在当前输入的列表songList中的索引号（初始置为-1）
        self.playingIndex = 0
        self.songIndex = 0
        #playingList: 播放时依次对应于该播歌曲在songList中的索引组成的数组，由数字组成
        #默认状态下为[0,1,...n-1]
        if order==-1:
            order = self.order
        else:
            self.order = order
        self.playingList = range(len(self.songList))
        if self.order == 2:
            #随机播放状态下，打乱playingList的次序
            random.shuffle(self.playingList)
            
    def updateOrder(self, order = -1):
        if order==-1:
            order = self.order
        else:
            self.order = order
        self.playingList = range(len(self.songList))
        if self.order == 0 or self.order == 1:
            self.playingIndex = self.songIndex
        if self.order == 2:
            self.playingIndex = 0
            random.shuffle(self.playingList)

    def fetchLyric(self, songId):
        logs('Start Fetching Lyric')
        #根据songId获取歌词，生成一个{毫秒数:(歌词, 歌词翻译)}的lrcList
        
        lrcPath ='e:\\netease\\lyric\\%s.txt' % songId
        if os.path.exists(lrcPath):
            file1 = open(lrcPath,'r')
            lyricResult = json.loads(file1.read())
            file1.close()
        else:
            rawLyric = self.api.rawgetSongLyric(songId)
            logs(u'End Get Lyric')
            file2 = open(lrcPath,'wb')
            file2.write(rawLyric)
            file2.close()
            lyricResult = json.loads(rawLyric)
        hasLyric  = False
        hasTLyric  = False
        isScroll = False
        self.hasLyric = ''
        try:
            if 'lrc' in lyricResult and 'lyric' in lyricResult['lrc'] and lyricResult['lrc']['lyric']:
                hasLyric = lyricResult['lrc']['lyric']
            if 'tlyric' in lyricResult and 'lyric' in lyricResult['tlyric'] and lyricResult['tlyric']['lyric']:
                hasTLyric = lyricResult['tlyric']['lyric']
            
            if hasLyric:
                self.hasLyric = hasLyric
                lrcList = procLyric(hasLyric)
                if lrcList == []:
                    #无标签，解析不能，注意，此时和“纯音乐”等情况一样，返回的hasLyric并非一个list而是一个string
                    return (hasLyric, lrcPath, isScroll)
                else:
                    isScroll = True
                    lrcDict = dict(lrcList)
                    if hasTLyric:
                        lrcDict = procTLyric(lrcDict, hasTLyric)
                    lrcList = finalProcLyric(lrcDict)
            else:
                #无歌词，解析不能
                if 'nolyric' in lyricResult and lyricResult['nolyric']:
                    lrcList = '纯音乐，请欣赏'
                else:
                    lrcList = '暂时没有歌词'
            logs(u'End Analyse Lyric')
        except Exception, e:
            printException(Exception, e)
            lrcList = '解析歌词发生错误'
        
        return (lrcList, lrcPath, isScroll)
        
    def getCurrLyric(self):
        #微秒转毫秒
        #如果是非滚动歌词，直接return 错误码-2
        if not self.isScroll:
            return -2
        if self.player.state() == audio.EPlaying:
            currPos = self.player.current_position() / 1000
        else:
            if self.currPos != -1:
                currPos = self.currPos / 1000
            else:
                return -1
        #currLI: 当前的歌词句子的索引i，为[0,1,2,3,...歌词句子数-1]中
        #currLT: 当前的歌词句子应对应的时间（毫秒数）
        currLI = -1
        for i, t in enumerate(self.lrcList):
            if currPos >= t[0]:
                currLI = i
        return currLI
            
    def fetchPic(self, size = -1):
        if size == -1:
            size = self.picSize
        logs('Start Fetching Pic')
        #根据当前播放的歌曲，返回专辑图片的路径，有必要时下载
        album=None
        if('album' in  self.listdetail[self.songIndex]):
            album = self.listdetail[self.songIndex]['album']
        elif('al' in  self.listdetail[self.songIndex]):
            album = self.listdetail[self.songIndex]['al']
        else:
            logs( 'Error Fetching Pic' )
            return
        picPath =u'e:\\netease\\pic\\%s.png' % album['id']
        
        if not os.path.exists(picPath):
            picUrl = album['picUrl'] + '?param=%iy%i' % (size, size)
            logs('Start Downloading Pic at %s to %s' % (picUrl, picPath))
            strList = [ cn('下载专辑图片 ') + cn(album['name']) , cn('目标: ') + cn(picPath.split('\\')[-1]) ]
            strList2 = [ cn('写入文件') ]
            download(picUrl, picPath, self.downCallbackWrapper(strList), self.errCallback, self.writeCallbackWrapper(strList2))
        logs( 'End Fetching Pic' )
        return picPath
        
    def fetchPicImage(self):
        picImage = 1
        try:
            picImage = graphics.Image.open(self.fetchPic())
            return picImage
        except Exception, e:
            printException(Exception, e)
            del picImage
            try:
                if os.path.exists(self.picPath):
                    os.remove(self.picPath)
            except Exception, e:
                printException(Exception, e)
            appuifw.note(cn('出现问题，图片加载错误。请浏览日志文件。'))
            return graphics.Image.open(sys.path[0] + '\\pic\\pic.bmp').resize((self.picSize,self.picSize))
        
    def fetchSong(self):
        #根据当前播放的歌曲，返回音频文件的路径，有必要时下载
        logs('Start Fetching Song')
        songPath ='e:\\netease\\%s_%s.mp3' % (self.listdetail[self.songIndex]['id'], self.br)
        if not os.path.exists(songPath):
            strList = [cn('下载歌曲 ') + cn(self.listdetail[self.songIndex]['name'] ), cn('目标') + cn(songPath.split('\\')[-1])]
            strList2 = [ cn('写入文件') ]
            download(self.listdown[self.songIndex], songPath, self.downCallbackWrapper(strList), self.errCallback, self.writeCallbackWrapper(strList2))
        logs('End Fetching Song')
        return songPath
        
    def saveSong(self):
        try:
            songDict = self.listdetail[self.songIndex]
            prompt = cn('')
            if not os.path.exists(self.songPath):
                self.songPath = self.fetchSong()
            
            if os.path.exists(self.songPath):
                desPath = 'E:\\Music\\%s - %s.mp3' % (cn(songDict['name']), cn(songDict['artists'][0]['name']))
                desPath = cn(desPath)
                orgPath = cn(self.songPath)
                fileman.file_copy(orgPath, desPath, cfileman.EOverWrite)
                prompt += cn('在E:\\Music') + cn('创建了') + cn(os.path.basename(nc(desPath))) + cn('(') + cn(str(self.br / 1000)) + cn('Kbps)')
            else:
                return False
            if self.hasLyric:
                desPath = 'E:\\Music\\%s - %s.lrc' % (cn(songDict['name']), cn(songDict['artists'][0]['name']))
                desPath = nc(cn(desPath))
                f = os.open(desPath , os.O_WRONLY|os.O_CREAT)
                os.write(f, STR_UTF8_BOM)
                os.write(f, nc(cn(self.hasLyric)))
                os.close(f)
                prompt += cn('和') + cn(os.path.basename(desPath))
            resp = appuifw.note(prompt)
            
        except Exception, e:
            printException(Exception, e, cn('SomeErrorsWithsaveSong'))
            try:
                os.close(f)
            except:
                pass
            
            
        
    def play(self, songDict):
        #输入歌曲对应的json数据来执行播放
        lrcList, lrcPath, isScroll = self.fetchLyric(songDict['id'])
        self.currPos = 0
        self.lrcList = lrcList
        self.lrcPath = lrcPath
        self.isScroll = isScroll
        
        try:
            self.picPath = self.fetchPic()
            self.songPath = self.fetchSong()
            self.player = audio.Sound.open(self.songPath)
            self.player.set_volume(self.volume)
            self.player.play(callback=self.songCallback)
            logs(u'Max Volume: '+unicode(self.player.max_volume()))
        except Exception, e:
            printException(Exception, e)
            if self.player:
                self.player.close()
            try:
                if os.path.exists(self.songPath):
                    os.remove(self.songPath)
            except Exception, e:
                printException(Exception, e)
            appuifw.note(cn('出现问题，播放错误。请浏览日志文件。'))
            # appuifw.app.set_exit()

        self.playCallback()
        
    def playDebug(self, songDict):
        #输入歌曲对应的json数据来执行播放
        lrcList, lrcPath, isScroll = self.fetchLyric(songDict['id'])
        self.currPos = 0
        self.lrcList = lrcList
        self.lrcPath = lrcPath
        self.isScroll = isScroll
        
        logs('Current PlayingList')
        logs(str(self.playingList))
        logs('Current SongList')
        logs(cn(u', '.join([cn(x['name']) for x in self.listdetail])))
        logs('playingIndex: ' + str(self.playingIndex))
        logs('songIndex: ' + str(self.songIndex))
        logs('Name: ' + cn(songDict['name']))

        self.playCallback()
        
    def playIndex(self, songIndex):
        #输入歌曲在songList中的Index，调用play来执行播放
        logs('songIndex ' + str(songIndex))
        if self.debugMode:
            self.playDebug(self.listdetail[songIndex])
        else:
            self.play(self.listdetail[songIndex])
        
    def pickupPlay(self, songIndex):
        #在播放列表中挑取一首歌曲播放，目前没有看出和playIndex的区别
        
        self.songIndex = songIndex
        if self.order == 0 or self.order == 1:
            self.playingIndex = self.songIndex
        self.playIndex(self.songIndex)
        
    def firstSong(self):
        self.songIndex = self.playingList[self.playingIndex]
        # if self.order != 2:
            # self.mappedsongIndex=self.songIndex
        self.playIndex(self.songIndex)
        
    def next(self, manual=False):
        #切下一首歌，manual==True时，单曲循环也下一首
        if self.order == 0:
            #顺序播放时，只需在playingIndex操作就行了
            self.playingIndex = (self.playingIndex + 1) % len(self.playingList)
        elif self.order == 1:
            if manual:
                self.playingIndex = (self.playingIndex + 1) % len(self.playingList)
        elif self.order == 2:
            #随机播放，播完playingList的最后一首歌后，将重新生成一个随机的playingList_附加到原playingList后，实现循环
            #可以进一步优化该算法，实现同曲不靠近，例如每次播放按照权重附加一个index到playingList
            if (self.playingIndex + 1) == len(self.playingList):
                self.playingList_  = range(len(self.songList))
                random.shuffle(self.playingList_)
                self.playingList[len(self.playingList):] = self.playingList_
            self.playingIndex = self.playingIndex + 1
        logs('Next PlayingIndex: ' + str(self.playingIndex))
        self.songIndex = self.playingList[self.playingIndex]
        self.playIndex(self.songIndex)
    
    def previous(self): #默认肯定是manual
        if (self.order == 0) or (self.order == 1):
            self.playingIndex = self.playingIndex - 1
            if self.playingIndex < 0:
                self.playingIndex = len(self.playingList) - 1
        elif self.order == 2:
            self.playingIndex = self.playingIndex - 1
            if self.playingIndex < 0:
                self.playingIndex = 0
        logs('Prev PlayingIndex: ' + str(self.playingIndex))
        self.songIndex = self.playingList[self.playingIndex]
        self.playIndex(self.songIndex)
        
    def getCurrentInfo(self):
        if self.songList == []:return None
        return self.listdetail[self.songIndex]
        
    #用于私人FM。 API每次推三首歌，所以弃用playingList，直接用songList和songIndex(0~2)。于是不支持上一首功能（并且按下一首时没有调教曲库的行为）
    def initFM(self, limit = 3):
        self.reloadFM(limit)
        self.updateOrder(0)
        
    def reloadFM(self, limit = 3):
        logs('Reload FM')
        self.updateListByDict(self.api.getFML(limit)['data'])
        self.songIndex = 0
        
    def nextFM(self, manual = False):
        if self.order == 1 and manual:
            pass
        else:
            if self.songIndex == len(self.songList) -1:
                self.reloadFM()
            else:
                self.playingIndex = self.playingIndex + 1
                self.songIndex = self.playingList[self.playingIndex]
        self.playIndex(self.songIndex)
        
    def insertSong(self, songIndex):
        #更换播放顺序后失效
        self.playingList[self.playingIndex+1:self.playingIndex+1] = [songIndex]
        
    def pauseCont(self):
        if self.player.state() == audio.EPlaying:
            self.pause()
        elif self.player.state() == audio.EOpen:
            self.cont()
            
    def pause(self):
        self.currPos = self.player.current_position()
        self.player.stop()
            
    def cont(self):
        self.player.set_position(self.currPos)
        self.player.play(callback=self.songCallback)
            
    def volumeAdjust(self, offset = 1):
        #offset正则加 负则减 音量从1到10
        if self.player:
            self.volume = self.player.current_volume()
            self.volume = self.volume + offset * self.player.max_volume()/10
            self.player.set_volume(self.volume)
            self.volume = self.player.current_volume()
    def volumeAdjustTo(self, num = 1):
        if self.player:
            self.volume = num
            self.player.set_volume(self.volume)
            self.volume = self.player.current_volume()