# -*- coding: utf-8 -*-
from struct import pack as pack
from struct import unpack as unpack
from graphics import Image as Image
from os import mkdir as mkdir
from os import remove as remove
__version__ = 1.4
class MbmInfo :


    __module__ = __name__
    def __init__(s, path = None):
        if path == None : 
            print ' usage:\nimport info\ninf=info.mbminfo("path to mbm file")\ninf.GetInfo()\ninf.GetInfo(key1)\ninf.GetInfo(key1,key2)\nmbm info structure:\nkey1  key2  value\n"uid"\n  "uid1"\n  "uid2"\n  "uid3"\n  "crc"\n"trlr"   ---\n"numimg" ---\nimagenumber    (int) = in range(0,"numimg")  # 1 2 3 ect.\n  "datasize"\n  "reserv1"\n  "width"\n  "height"\n  "reserv2"\n  "reserv3"\n  "bpp"\n  "bpp1"\n  "bpp2"\n  "bpp3"\n',
            print
        else : 
            s.struct = {}
            f = open(path)
            s.struct['uid'] = {}
            s.struct['uid']['uid1'] = unpack('L', f.read(4))[0]
            s.struct['uid']['uid2'] = unpack('L', f.read(4))[0]
            s.struct['uid']['uid3'] = unpack('L', f.read(4))[0]
            s.struct['uid']['crc'] = unpack('L', f.read(4))[0]
            s.struct['trlr'] = unpack('L', f.read(4))[0]
            f.seek(s.struct['trlr'])
            s.struct['numimg'] = unpack('L', f.read(4))[0]
            for i in range(s.struct['numimg']):
                s.struct[i] = {}
                s.struct[i]['start'] = unpack('L', f.read(4))[0]
            for i in range(s.struct['numimg']):
                f.seek(s.struct[i]['start'])
                s.struct[i]['datasize'], s.struct[i]['reserv1'], s.struct[i]['width'], s.struct[i]['height'], s.struct[i]['reserv2'], s.struct[i]['reserv3'], s.struct[i]['bpp'], s.struct[i]['bpp1'], s.struct[i]['bpp2'], s.struct[i]['bpp3'] = unpack('LLLLLLLLLL', f.read(40))
            f.close()




    def GetInfo(s, key1 = None, key2 = None):
        if key1 == None and key2 == None : 
            return s.struct
        if key1 != None and key2 == None : 
            return s.struct[key1]
        if key1 == None and key2 != None : 
            return 0






class MbmPack :


    __module__ = __name__
    def __init__(s, out = 'C://image.mbm', in_dir = 'C:\\', files = []):
        s.out_file = out
        s.files = files
        s.in_dir = in_dir




    def RLE12102(s, f, img, x, y):


        def c(aa, id = None):
            r, g, b =aa
            if id == None : 
                r, g, b = ((r >> 4), (g >> 4), (b >> 4))
                return (r, g, b)
            else : 
                a1 = eval(('0x%s%s' % (hex(g)[-1], hex(b)[-1])))
                a2 = eval(('0x%s%s' % (hex(id)[-1], hex(r)[-1])))
                return chr(a1) + chr(a2)


        if (x % 4) != 0 : 
            xx = x + (x % 2)
        else : 
            xx = x
        for yy in range(y):
            s = [(ii, yy) for ii in range(xx)]
            s = img.getpixel(s)
            ss = []
            for ii in range(xx):
                if ii <= x : 
                    ii = s[ii]
                else : 
                    ii = (255, 255, 255)
                if ss == [] : 
                    ss = [c(ii)]
                elif c(ii) == ss[0] : 
                    if len(ss) < 16 : 
                        ss.append(c(ii))
                    else : 
                        f.write(c(ss[0], (len(ss) - 1)))
                        ss = [c(ii)]
                    pass
                else : 
                    f.write(c(ss[0], (len(ss) - 1)))
                    ss = [c(ii)]
            f.write(c(ss[0], (len(ss) - 1)))




    def RLE8000(s, f, img, x, y):


        def c(aa):
            r, g, b = aa
            return chr(((2 * r) + (5 * g) + b / 8))


        if (x % 4) != 0 : 
            xx = x + (4 - (x % 4))
        else : 
            xx = x
        for yy in range(y):
            s = [(ii, yy) for ii in range(xx)]
            s = img.getpixel(s)
            for ii in range(xx):
                if ii <= x : 
                    ii = s[ii]
                else : 
                    ii = (255, 255, 255)
                f.write(c(ii))




    def RLE24100(s, f, img, x, y):
        if (x % 4) != 0 : 
            xx = x + (4 - (x % 4))
        else : 
            xx = x
        for yy in range(y):
            s = [(ii, yy) for ii in range(xx)]
            s = img.getpixel(s)
            ss = []
            for ii in range(xx):
                if ii <= x : 
                    ii = s[ii]
                else : 
                    ii = (255, 255, 255)
                f.write(chr(ii[2]) + chr(ii[1]) + chr(ii[0]))




    def RLE8001(s, f, img, x, y):


        def c(aa):
            r, g, b = aa
            return chr(((2 * r) + (5 * g) + b / 8))


        if (x % 4) != 0 : 
            xx = x + (4 - (x % 4))
        else : 
            xx = x
        for yy in range(y):
            s = [(ii, yy) for ii in range(xx)]
            s = img.getpixel(s)
            ss = []
            for ii in range(xx):
                if ii <= x : 
                    ii = s[ii]
                else : 
                    ii = (255, 255, 255)
                if ss == [] : 
                    ss = [ii]
                elif ii == ss[0] : 
                    if len(ss) < 127 : 
                        ss.append(ii)
                    else : 
                        f.write(chr((len(ss) - 1)) + c(ss[0]))
                        ss = [ii]
                    pass
                else : 
                    f.write(chr((len(ss) - 1)) + c(ss[0]))
                    ss = [ii]
            f.write(chr((len(ss) - 1)) + c(ss[0]))




    def RLE16103(s, f, img, x, y):


        def c(aa):
            r, g, b = aa
            rgb = chr(((((g / 4) & 7) << 5) | (((b / 8) & 31) & 255))) + chr(((((r / 8) & 31) << 3) | ((((g / 4) >> 3) & 7) & 255)))
            return rgb


        if (x % 4) != 0 : 
            xx = x + (x % 2)
        else : 
            xx = x
        for yy in range(y):
            s = [(ii, yy) for ii in range(xx)]
            s = img.getpixel(s)
            ss = []
            for ii in range(xx):
                if ii <= x : 
                    ii = s[ii]
                else : 
                    ii = (255, 255, 255)
                if ss == [] : 
                    print s[ii],
                    print
                    ss = s[ii]
                elif ii == ss[0] : 
                    if len(ss) < 127 : 
                        ss.append(ii)
                    else : 
                        f.write(chr((len(ss) - 1)) + c(ss[0]))
                        ss = [ii]
                    pass
                else : 
                    f.write(chr((len(ss) - 1)) + c(ss[0]))
                    ss = [ii]
            f.write(chr((len(ss) - 1)) + c(ss[0]))




    def RLE16100(s, f, img, x, y):


        def c(aa):
            r, g, b = aa
            rgb = chr(((((g / 4) & 7) << 5) | (((b / 8) & 31) & 255))) + chr(((((r / 8) & 31) << 3) | ((((g / 4) >> 3) & 7) & 255)))
            return rgb


        for i in range(y):
            if (x % 4) != 0 : 
                x += (x % 2)
            s = [(ii, i) for ii in range(x)]
            s = img.getpixel(s)
            for ii in s:
                f.write(c(ii))




    def PACK(s, callback):
        offset = pack('i', len(s.files))
        f = open(s.out_file, 'w')
        f.write(pack('LLLLL', 268435511, 268435522, 0, 1194943545, 0))
        total = len(s.files)
        tt = 0
        for files in s.files:
            START = f.tell()
            offset += pack('i', START)
            NAME, RLE = files.split(':')
            img = Image.open(s.in_dir + NAME)
            x, y = img.size
            f.write(eval((" pack('LiLLLLLLLL',0,40,%s,%s,0,0,%s)" % (x, y, RLE))))
            if RLE == '8,0,0,0' : 
                s.RLE8000(f, img, x, y)
            if RLE == '8,0,0,1' : 
                s.RLE8001(f, img, x, y)
            if RLE == '12,1,0,2' : 
                s.RLE12102(f, img, x, y)
            if RLE == '16,1,0,0' : 
                s.RLE16100(f, img, x, y)
            if RLE == '16,1,0,3' : 
                s.RLE16103(f, img, x, y)
            if RLE == '24,1,0,0' : 
                s.RLE24100(f, img, x, y)
            END = f.tell()
            f.seek(START)
            f.write(pack('L', (END - START)))
            f.seek(END)
            tt += 1
            callback(((tt * 100) / total))
        f.seek(16)
        f.write(pack('L', END))
        f.seek(END)
        f.write(offset)
        f.close()






def RLE(id = None):
    alg = ['8,0,0,0', '8,0,0,1', '12,1,0,2', '16,1,0,0', '16,1,0,3', '24,1,0,0']
    if id == None : 
        for i in alg:
            print i,
            print
        pass
    else : 
        return alg




def Unmake(mbmfile, outdir):


    rlelist = [(24, 1, 0, 0), (16, 1, 0, 0), (16, 1, 0, 3), (8, 0, 0, 0), (8, 0, 0, 1), (12, 1, 0, 2)]
    def readL(f, pos = None):
        if pos != None : 
            f.seek(pos)
        return unpack('i', f.read(4))[0]


    f = open(mbmfile)
    uids = f.read(20)
    trailer = readL(f, 16)
    num = readL(f, trailer)
    offset = [readL(f) for i in range(num)]
    result = []
    for i in range(num):
        start = offset[i]
        dl = readL(f, start)
        f.seek((start + 24))
        RLE = unpack('iiii', f.read(16))
        if RLE not in rlelist : 
            RLE = (12, 1, 0, 2)
        name = str(('00000000%s.png' % i))[-8 : ]
        f.seek(start)
        mbmf = open('d:\\temp.mbm', 'w')
        mbmf.write(('%s%s' % (uids, f.read(dl))))
        dl = mbmf.tell()
        mbmf.seek(16)
        mbmf.write(pack('i', dl))
        mbmf.seek(dl)
        mbmf.write(pack('ii', 16777216, 335544320))
        mbmf.close()
        img = Image.open('d:\\temp.mbm')
        img.save(outdir + name)
        result.append(outdir + name)
    remove('d:\\temp.mbm')
    return result

