# coding: utf-8
import os
import sys
import time
import traceback
import StringIO
import httplib
import cfileman
try:
    import appuifw2 as appuifw
except:
    pass

HOST = 'http://music.163.com'
INIT_COOKIE = 'os=pc;appver=2.9.8;'
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
E = 2.7183
Pi = 3.1416
Terminator = ''

#写日志
def tw(str1 , str2 = 'e:\\netease\\a.txt', str3 = 'wb'):
    file1=open(str2, str3)
    file1.write(str(str1))
    file1.close()
    return None


class Out:
    def __init__(self, cmdwrite):
        self.cmdwrite = cmdwrite
    def write(self, str1):
        str1=cn(str1)
        try:
            # self.cmdwrite.write(str1 + Terminator)
            pass
        except:
            self.cmdwrite.write(str1.encode('gbk') + Terminator.encode('gbk'))
        logwrite = open('e:\\neteaseDebug\\log.txt','a')
        logwrite.write((str1+Terminator).encode('utf-8'))
        logwrite.close()
    def write_(self, str1):
        str1=cn(str1)
        #self.cmdwrite.write(str1 + Terminator)
        logwrite = open('e:\\neteaseDebug\\log.txt','a')
        logwrite.write((str1+Terminator).encode('utf-8'))
        logwrite.close()
class OutErr:
    def __init__(self, errwrite):
        self.errwrite = errwrite
    def write(self, str1):
        str1=cn(str1)
        try:
            # self.errwrite.write(str1 + Terminator)
            pass
        except:
            self.errwrite.write(str1.encode('gbk') + Terminator.encode('gbk'))
        logwrite = open('e:\\neteaseDebug\\log.txt','a')
        logwrite.write((u'@ '+str1+Terminator).encode('utf-8'))
        logwrite.close()

def logs(str1):
    print u'%s - %s' % (time.clock(), cn(str1))
def logs_(str1):
    sys.stdout.write_('%s - %s' % (time.clock(), str1))
    
def httpLogs(str1):
    str1 = cn(str1)
    logwrite = open('e:\\neteaseDebug\\http.txt','a')
    logwrite.write((str1+'\n').encode('utf-8'))
    logwrite.close()
    pass
    
UTILINITED  = False
    
def utilInit():
    global out, outerr, cmdwrite, errwrite, UTILINITED, fileman
    dirList = [u'e:\\netease\\', u'e:\\netease\\cache', u'e:\\netease\\cache\\playlist', u'e:\\netease\\lyric\\', u'e:\\netease\\pic\\', u'e:\\netease\\data\\', u'e:\\neteaseDebug\\', u'e:\\NetEaseMusic\\']
    fileman = cfileman.FileMan()

    for x in dirList:
        if not os.path.isdir(x):
            os.makedirs(x)
        fileman.set_att(x, cfileman.EAttHidden)

    fileman.set_att(u'e:\\NetEaseMusic\\', 0, cfileman.EAttHidden)
        
    
    logwrite = open('e:\\neteaseDebug\\log.txt','w')
    logwrite.write('---Start Logging---\n')
    logwrite.close()
    logwrite = open('e:\\neteaseDebug\\http.txt','w')
    logwrite.write('---Start Network Capturing---\n')
    logwrite.close()
    cmdwrite = sys.stdout
    errwrite = sys.stderr
    out=Out(cmdwrite)
    outerr=OutErr(errwrite)
    sys.stdout = out
    sys.stderr = outerr
    UTILINITED = True
    logs('Util Init')
    
def printException(Exception, e, str1=''):
    logs(u'@ Error :')
    errStr = cn(str(Exception) + u': ' + str(e))
    logs(errStr)
    traceback.print_exc()
    if str1:
        displayLongText(u'Error Encountered: \n' + errStr + u'\n' + str1)
        appuifw.note(u'View E:\\neteaseDebug\\log.txt For More Details.')
        # aolock.signal()
        # appuifw.app.set_exit()
    
def download(objUrl, objPath, callBack = None, errBack = lambda:None, writeCallBack = None,ck=None):
    succeed = False
    retryCount = 0
    # while((not succeed) and retryCount < 4):
    if True:
        try:
            # try:
                # if os.path.exists(objPath):
                    # os.remove(objPath)
            # except Exception, e:
                # logs(repr(Exception) + ': ' + repr(e))
                # traceback.print_exc()
            httpLogs(cn('<Download> ') + cn(objUrl) + cn(' To: ') + cn(objPath))
            httpDownload(objUrl, objPath, callBack, writeCallBack,ck=ck)
            logs(u'Download Succeed')
            succeed = True
        except Exception, e:
            errBack()
            httpLogs(cn('<Download Failure> ') + cn(str(e)))
            logs(u'Error * %s' % (retryCount + 1))
            logs(repr(Exception) + ': ' + repr(e))
            traceback.print_exc()
            # appuifw.note(cn('出现常见网络错误，文件可能不完整！'))
            # try:
                # if os.path.exists(objPath):
                    # os.remove(objPath)
            # except Exception, e:
                # printException(Exception, e)
            retryCount = retryCount + 1
    # if not succeed:
        # try:
            # if os.path.exists(objPath):
                # os.remove(objPath)
        # except Exception, e:
            # printException(Exception, e)
        # appuifw.note(cn('出现网络问题，下载持续出现错误。请检查网络，并重新启动程序。'))
        # appuifw.app.set_exit()
        
def httpDownload(objUrl, objPath, callBack = None, writeCallBack = None, bs = 8*1024, writebs = 512 * 1024,ck=None):
    try:
        urlhost = objUrl.split('/')[2]
        conn1 = httplib.HTTPConnection(urlhost,80,3)
        hd={}
        if(ck!=None):
            hd={
                'Cookie':ck
            }
        conn1.request('GET',objUrl,'', hd)
        responseIO=conn1.getresponse()
        logs('Downloading From ' + objUrl)
        if responseIO.status == 302 or bool(responseIO.getheader('Location')):
            conn1.close()
            objUrl2 = responseIO.getheader('Location')
            urlhost = objUrl2.split('/')[2]
            logs('Redirecting to ' + objUrl2)
            conn1 = httplib.HTTPConnection(urlhost,80,3)
            conn1.request('GET',objUrl2,'',{})
            responseIO=conn1.getresponse()
        
        responseData = StringIO.StringIO()
        totalSize = getIOLength(responseIO)
        httpLogs(cn('<FileSize> ') + unicode(totalSize))
        fileIO = open(objPath, 'wb')
        # if totalSize < 4*1024*1024:
        if totalSize < 1:
            callbackWhenRead(responseIO, responseData, callBack, bs, totalSize)
            logs('Load Completed.')
            responseData.seek(0)
            logs('Start Write Progress.')
            callbackWhenRead(responseData, fileIO, writeCallBack, writebs, totalSize)
            logs('Write Completed.')
        else:
            logs('Big File, Enable Instant ReadWrite')
            callbackWhenRead(responseIO, fileIO, callBack, bs * 16, totalSize)
            logs('ReadWrite Completed')
            
        
        fileIO.close()
        responseData.close()
        conn1.close()
        
        del responseData
        del fileIO
        del responseIO
        del conn1
    except Exception, e:
        printException(Exception, e)
        try:
            conn1.close()
            responseData.close()
            fileIO.close()
        except:
            pass
        try:
            del conn1
            del responseIO
            del responseData
            del fileIO
        except:
            pass
        raise Exception, e
        
def getIOLength(readIO):
    try:
        logs('.length = ' + str(readIO.length))
    except:
        pass
        
    try:
        logs('.len = ' + str(readIO.len))
    except:
        pass
    
    try:
        if readIO.len == None:
            totalSize = 1
        else:
            totalSize = long(readIO.len)
    except:
        logs('contentlength = ' + str(readIO.getheader("Content-Length")))
        if readIO.getheader("Content-Length") == None:
            totalSize = 1
        else:
            totalSize = long(readIO.getheader("Content-Length"))
    return totalSize
        
def callbackWhenRead(readIO, writeIO, callBack, bs, totalSize):
    receivedBlock = 0
    
        
    if callBack: callBack(0, bs, totalSize)
    block = readIO.read(bs)
    receivedBlock = 1
    if callBack: callBack(receivedBlock, bs, totalSize)

    while block:
        receivedBlock += 1
        writeIO.write(block)
        block = readIO.read(bs)
        # logs('callback %s %s %s' % (receivedBlock, bs, totalSize))
        if callBack: callBack(receivedBlock, bs, totalSize)
        
def readableTime(msec, showMsec = False, noChar = False):
    hr = long(msec / 3600000L)
    msec = long(msec % 3600000L)
    min = long(msec / 60000)
    msec = long(msec % 60000)
    sec = long(msec / 1000)
    msec = long(msec % 1000)
    str1 = ''
    if noChar:
        unit = [':',':','.','']
        if not showMsec:unit[2] = ''
    else:
        unit = ['h','m','s','ms']
    if hr > 0: str1 = str1 + '%i%s' % (hr,unit[0])
    if min > 0: str1 = str1 + '%.2i%s' % (min,unit[1])
    if sec > 0: str1 = str1 + '%.2i%s' % (sec,unit[2])
    if showMsec: str1 = str1 + '%.3i%s' % (msec,unit[3])
    if str1 == '': str1 = '0'
    return str1
    
def readableTime2(msec):
    hr = long(msec / 3600000L)
    msec = long(msec % 3600000L)
    min = long(msec / 60000)
    msec = long(msec % 60000)
    sec = long(msec / 1000)
    msec = long(msec % 1000)
    str1 = ''
    unit = [':',':','.','']
    str1 = str1 + '%.2i%s' % (min,unit[1])
    str1 = str1 + '%.2i' % (sec)
    if str1 == '': str1 = '00:00'
    return str1
    
timeUnit = ['年', '月', '日', '时', '分', '秒']
timeUnit2 = ['年', '个月', '天', '小时', '分钟', '秒']
def fuzzyTime(tgSec, timeType = 2, AbsTimeDepth = 2):
    currTime_ = time.localtime()
    tgetTime_ = time.localtime(tgSec)
    currTime = currTime_[0:6]
    tgetTime = tgetTime_[0:6]
    #找到第一个不同的时间单位
    if currTime!=tgetTime:
        firstDiff = map(lambda x:currTime[x]==tgetTime[x], range(6) ).index(False)
    else:
        return cn('几乎同时')
    #0: 相对时间 1: 绝对时间 2: 相距2月以上则绝对时间，否则相对时间
    if timeType == 2:
        if (firstDiff == 0 or (firstDiff == 1 and abs(currTime[1] - tgetTime[1]) > 1)):
            timeType = 1
            AbsTimeDepth = 3 - firstDiff
        else:
            timeType = 0
        
    if timeType == 1:
        #timeString = str(currTime[firstDiff])+cn(timeUnit[firstDiff])
        timeString = ''.join(map(lambda x:str(tgetTime[x])+cn(timeUnit[x]), range(firstDiff, firstDiff+AbsTimeDepth)))
    else:
        timeString = str(abs(currTime[firstDiff] - tgetTime[firstDiff])) + cn(timeUnit2[firstDiff])+(cn('前'),cn('后'))[currTime[firstDiff] < tgetTime[firstDiff]]
    return timeString
    
WIDTHS = [
    (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
    (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
    (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
    (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
    (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
    (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
    (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]
def get_char_width_o(char):
        """
        查表(WIDTHS)获取单个字符的宽度
        """
        char = ord(char)
        if char == 0xe or char == 0xf:
            return 0

        for num, wid in WIDTHS:
            if char <= num:
                return wid
        return 1
def get_char_width(char):
        """
        查表(WIDTHS)获取单个字符的宽度
        """
        char = ord(char)
        if char == 0xe or char == 0xf:
            return 0
        widMapped=[0.,0.8,2.0]
        for num, wid in WIDTHS:
            if char <= num:
                return widMapped[wid]
        return 1

def getStringWidth(str1):
    if len(str1) == 0: return 0
    return reduce(lambda x,y:float(x)+get_char_width_o(y), u'0'+str1)

def getStringWidth_(str1):
    if len(str1) == 0: return 0
    return reduce(lambda x,y:float(x)+get_char_width(y), u'0'+str1)
    
def fillUnicodeByWidth(str1, width, filler=u' ', leftFill = True):
    str1Width = int(getStringWidth(str1))
    str1Filler = filler * int(width - str1Width)
    if leftFill:
        return str1Filler + str1
    else:
        return str1 + str1Filler
        
def displayLongText(str1):
    textArray = [str1[x:x+30] for x in range(0,len(str1),30)]
    for (x, y) in enumerate(textArray):
        appuifw.query(y + u' (' + str(x+1) + u'/' + str(len(textArray)) + u')' , 'query')
    
def splitUnicodeByWidth(str1, width):
    totalWidth = 0.
    cursorPosition = 0
    finalList = []
    for i in range(0, len(str1)):
        thisWidth = get_char_width(str1[i])
        if (totalWidth + thisWidth)>width:
            finalList[len(finalList):] = [str1[cursorPosition:i]]
            totalWidth = thisWidth
            cursorPosition = i
        else:
            totalWidth += thisWidth
    finalList[len(finalList):] = [str1[cursorPosition:]]
    return finalList
#转码用
def cn(str1):
    if isinstance(str1, unicode):
        return str1
    else:
        str1 = str(str1).decode('utf-8')
        return str1
        
def nc(str1):return unicode(str1).encode('utf-8')
def cnList(list1, toTuple=False):
    cnedList = [cn(x) for x in list1]
    if toTuple:cnedList = tuple(cnedList)
    return cnedList
    
#删除一个文件夹内所有文件（文件夹排除）
def cleanDir(Dir):
    if not os.path.isdir(Dir): return None
    for f in os.listdir(Dir):
        filePath = os.path.join(Dir,f)
        if os.path.isfile(filePath):
            try:
                os.remove(filePath)
            except:
                logs('remove error on %s' % filePath)
    return True
def clearCache_():
    dirs = ['e:\\neteaseDebug', 'e:\\netease', 'e:\\netease\\lyric', 'e:\\netease\\pic', 'e:\\netease\\cache\\playlist']
    for d in dirs:
        cleanDir(d)
        
    files = ['e:\\netease\\data\\cookie.txt', 'e:\\netease\\data\\captcha.png']
    for f in files:
        if os.path.isfile(f):
            try:
                os.remove(f)
            except:
                logs('remove error on %s' % f)
    appuifw.note(cn('清除完成'))
utilInit()