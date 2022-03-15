# -*- coding: utf-8 -*-

import struct
import zlib
import appuifw
import sys
import os
import e32
import sre
import time
__version__ = 1.4
reload(sys)
sys.setdefaultencoding('u8')
def ru(x):
    return x.decode('u8')




class PNGFile :


    __module__ = __name__
    def __init__(s, path = None):
        png = '\x89PNG\r\n\x1a\n'
        if path : 
            s.data, s.path = (file(path).read(), path)
            assert s.data[ : 8] == png
        else : 
            s.data, s.path = (png, None)




    def Read(s, type, pos = 0):
        loc = s.Loc(type, pos)
        return s.data[(loc + 4) : (loc + 4) + struct.unpack('>i', s.data[(loc - 4) : loc])[0]]




    def Repeats(s, type):
        return len(sre.findall(type, s.data))




    def Path(s):
        return s.path




    def Info(s):
        return struct.unpack('>iibbbbb', s.Read('IHDR'))




    def Loc(s, type, pos = 0):
        return pos + s.data[pos : ].find(type)




    def DelChunk(s, type):
        loc = s.Loc(type)
        s.data = s.data[ : (loc - 4)] + s.data[(loc + 9) + struct.unpack('>i', s.data[(loc - 4) : loc])[0] : ]




    def Save(s, path):
        s.path = path
        file(path, 'w').write(s.data)




    def AddChunk(s, type, data, loc = None):
        if loc == None : 
            s.data += struct.pack('>i', len(data)) + type + data + struct.pack('>i', zlib.crc32(type + data))
        else : 
            s.data = s.data[ : loc] + struct.pack('>i', len(data)) + type + data + struct.pack('>i', zlib.crc32(type + data)) + s.data[loc : ]






def rgbToBytes(color):
    return ''.join([chr(i) for i in color])




def bytesToInt(color):
    return eval('0x' + ''.join([('%02x' % ord(i)) for i in color]))




def editFile(f, color, callback, dtext):
    color = rgbToBytes(color)
    if color == None : 
        return None
    k = appuifw.query(dtext['translev'], 'number', 50)
    if k == None or k > 100 : 
        return None
    k = int(((255.0 / 100.0) * float((100 - k))))
    path = f.Path()
    count = time.clock()
    e32.ao_yield()
    info, nidat, idat, loc, pos = (f.Info(), [], '', 0, [])
    for i in xrange(f.Repeats('IDAT')):
        pos.append(f.Loc('IDAT', loc))
        loc = (pos[-1] + 4)
    for i in pos:
        idat += f.Read('IDAT', i)
    try :
        idat = zlib.decompress(idat)
    except :
        None
    if info[3] in (6, 2) : 
        s = 0
        if info[3] == 2 : 
            incr = ((info[0] * 3) + 1)
        else : 
            incr = ((info[0] * 4) + 1)
        t = len(nidat)
        nidat += range(info[1])
        cc = 0
        for i in xrange(info[1]):
            nidat[t + i] = idat[s : s + incr]
            s += incr
            cc += 1
            callback(((cc * 15) / info[1]))
        cc = 0
        if info[3] == 2 : 
            idat = nidat[ : ]
            for i in xrange(len(nidat)):
                tp = nidat[i][0]
                nidat[i] = nidat[i][1 : ]
                strng = ""
                for e in xrange(2, len(nidat[i]), 3):
                    strng += nidat[ : ][i][(e - 2) : (e + 1)] + '\xff'
                idat[i] = strng
                nidat[i] = tp + nidat[i]
                cc += 1
                callback((((cc * 15) / len(nidat)) + 15))
            nidat = idat[ : ]
        for i in xrange(len(nidat)):
            tp = nidat[i][0]
            nidat[i] = nidat[i][1 : ]
            tt = list(nidat[i])
            for e in xrange(3, len(nidat[i]), 4):
                nidat[i] = tt
                if color is None : 
                    nidat[i][e] = chr(k)
                elif ''.join(map(str, nidat[i][(e - 3) : e])) == color : 
                    nidat[i][e] = chr(k)
                nidat[i] = ''.join(nidat[i])
            nidat[i] = tp + nidat[i]
            callback((((i * 70) / len(nidat)) + 30))
            e32.ao_yield()
        pass
    elif info[3] == 3 : 
        s = 0
        plte, nplte = (f.Read('PLTE'), [])
        for i in xrange(3, len(plte), 3):
            nplte.append(plte[(i - 3) : i])
        for i in xrange(info[1]):
            nidat.append(nplte[ord(idat[s : s + info[0]])])
            s += info[0]
        idat = []
        for i in xrange(len(nidat)):
            if isinstance(color, list) : 
                if nidat[i] in color : 
                    idat.append(nidat[i] + chr(k))
                else : 
                    idat.append(nidat[i] + '\xff')
                pass
            elif color == None : 
                idat.append(nidat[i] + chr(k))
            elif i == color : 
                idat.append(nidat[i] + chr(k))
            else : 
                idat.append(nidat[i] + '\xff')
            e32.ao_yield()
        nidat = idat[ : ]
    newf = PNGFile()
    newf.AddChunk('IHDR', struct.pack('>iibbbbb', info[0], info[1], 8, 6, 0, 0, 0))
    newf.AddChunk('IDAT', zlib.compress(''.join(nidat)))
    newf.AddChunk('IEND', '')
    newf.Save(path)
    del newf
    appuifw.note(dtext['done'], 'conf', 1)




def file_transparent(path, color, callback, dtext):
    if path == None : 
        return None
    try :
        f = PNGFile(path)
    except :
        appuifw.note(u('File opening error!'), 'error', 1)
        return None
    info = f.Info()
    if info[3] not in (2, 3, 6) : 
        appuifw.note(u('Unsupported type of colour interpreting!'), 'error', 1)
        return None
    editFile(f, color, callback, dtext)

