# -*- coding: utf-8 -*-

from os import path as path
import codecs
__version__ = 1.4
def ru(s):
    return s.decode('utf-8')




class TIniParser(object, ) :


    __module__ = __name__
    def __init__(self):
        self.fobj = None
        self.curpos = 0




    def open(self, filepath, mode = 'r'):
        if path.isfile(filepath) : 
            self.fobj = codecs.open(filepath, mode, 'utf-8')
            return True
        else : 
            return False




    def create(self, filepath, mode = 'wb'):
        self.fobj = open(filepath, mode)
        if self.fobj is not None : 
            return True




    def close(self):
        if self.fobj is not None : 
            self.fobj.close()
            self.fobj = None




    def readgroup(self, group):
        self.fobj.seek(0)
        self.curpos = 0
        line = None
        group = '[' + group.lower().strip() + ']'
        while line != '' : 
            line = self.fobj.readline()
            line = line.lower().strip()
            if line[0] != '[' : 
                continue
            elif line == group : 
                self.curpos = self.fobj.tell()
                return True
        return False




    def resetgroup(self):
        self.fobj.seek(0)
        self.curpos = 0




    def getkeys(self, group):
        if self.readgroup(group) : 
            line = None
            self.fobj.seek(self.curpos)
            self.keys = []
            while line != '' : 
                line = self.fobj.readline()
                if line is not None and line.strip() != '' and line.strip()[0] != ';' : 
                    ind = line.find('=')
                    if ind > 0 : 
                        k = line[ : ind].strip().lower()
                        self.keys.append(k)
                    if line.strip()[0] == '[' : 
                        return self.keys
                    pass
            return self.keys




    def getgroups(self):
        self.fobj.seek(0)
        self.curpos = 0
        line = None
        group = []
        while line != '' : 
            line = self.fobj.readline()
            line = line.lower().strip()
            if line is not None and line.strip() != '' : 
                if line[0] != '[' : 
                    continue
                elif line[-1] == ']' : 
                    group.append(line[1 : -1])
                pass
        self.fobj.seek(0)
        self.curpos = 0
        if len(group) == 0 : 
            return None
        return group




    def getdictfromfile(self, filepath, codec = None):
        if path.isfile(filepath) : 
            fobj = codecs.open(filepath, 'r', 'utf-8')
        else : 
            return None
        dic = {}
        lines = fobj.readlines()
        for line in lines:
            striped = line.strip()
            if striped != '' and striped[0] != ';' : 
                ind = line.find('=')
                if ind > 0 : 
                    k = line[ : ind].strip().lower()
                    value = (line[(ind + 1) : ]).strip()
                    dic[k] = value
                pass
        return dic




    def getdict(self, group, codec = None):
        if self.readgroup(group) : 
            line = None
            dic = {}
            self.fobj.seek(self.curpos)
            while line != '' : 
                line = self.fobj.readline()
                if line is not None and line.strip() != '' and line.strip()[0] != ';' : 
                    ind = line.find('=')
                    if ind > 0 : 
                        k = line[ : ind].strip().lower()
                        value = (line[(ind + 1) : ]).strip()
                        if codec is None : 
                            dic[k] = value
                        else : 
                            dic[k] = value.decode(codec)
                        pass
                    if line.strip()[0] == '[' : 
                        return dic
                    pass
            return dic




    def readkey(self, wkey, mode = 'ASCII'):
        line = None
        self.fobj.seek(self.curpos)
        while line != '' : 
            line = self.fobj.readline()
            if line is not None and line.strip() != '' and line.strip()[0] != ';' : 
                ind = line.find('=')
                if ind > 0 : 
                    key = line[ : ind].strip()
                    value = (line[(ind + 1) : ]).strip()
                    if key.lower() == wkey.strip().lower() : 
                        return value
                    pass
                if line.strip()[0] == '[' : 
                    return None
                pass
        return None




    def checknone(self, st):
        if st == 'None' : 
            return None
        return st




    def readstr(self, key, dflt = '', dlmt = None):
        line = self.readkey(key)
        if line is not None : 
            if dlmt is not None : 
                result = []
                strar = line.split(dlmt)
                for t in strar:
                    result.append(self.checknone(t))
                pass
            else : 
                result = self.checknone(line)
            pass
        else : 
            result = dflt
        return result




    def readstrm(self, key, mode = 'ASCII', dflt = '', dlmt = None):
        line = self.readkey(key, mode)
        if line is not None : 
            if dlmt is not None : 
                result = []
                strar = line.split(dlmt)
                for t in strar:
                    result.append(self.checknone(t))
                pass
            else : 
                result = self.checknone(line)
            pass
        else : 
            result = dflt
        return result




    def readint(self, key, nsys = 10, dflt = 0, dlmt = None):
        line = self.readkey(key)
        if line is not None : 
            try :
                if dlmt is not None : 
                    result = []
                    strar = line.split(dlmt)
                    for t in strar:
                        if t != 'None' : 
                            result.append(int(t, nsys))
                        else : 
                            result.append(None)
                    pass
                elif line != 'None' : 
                    result = int(line, nsys)
                else : 
                    result = None
            except :
                result = dflt
            pass
        else : 
            result = dflt
        return result




    def readbool(self, key, dflt = False, dlmt = None):
        line = self.readkey(key)
        if line is not None : 
            if dlmt is not None : 
                result = []
                strar = line.split(dlmt)
                for t in strar:
                    if t.lower() == 'true' : 
                        t = True
                        result.append(t)
                    elif t.lower() == 'false' : 
                        t = False
                        result.append(t)
                    elif t == 'None' : 
                        t = None
                        result.append(t)
                pass
            elif line.lower() == 'true' : 
                result = True
            elif t.lower() == 'false' : 
                result = False
            elif t == 'None' : 
                result = None
            pass
        else : 
            result = dflt
        return result




    def writegroup(self, group):
        self.fobj.write(('[' + group + ']\r\n').encode('utf-8'))




    def writestr(self, key, val, dlmt = None):
        if type(val) == 'list' or type(val) == type(()) : 
            if dlmt is None : 
                dlmt = ','
            strng = ''
            for t in xrange(len(val)):
                if t == (len(val) - 1) : 
                    dlmt = '\r\n'
                strng += val[t] + dlmt
            self.fobj.write((key + ' = ' + strng).encode('utf-8'))
        else : 
            self.fobj.write((key + ' = ' + val + '\r\n').encode('utf-8'))




    def writeint(self, key, val, dlmt = None):
        if type(val) == type([]) or type(val) == type(()) : 
            if dlmt is None : 
                dlmt = ','
            strng = ''
            for t in xrange(len(val)):
                if t == (len(val) - 1) : 
                    dlmt = '\r\n'
                strng += str(val[t]) + dlmt
            self.fobj.write((key + ' = ' + strng).encode('utf-8'))
        else : 
            self.fobj.write((key + ' = ' + str(val) + '\r\n').encode('utf-8'))




    def writebool(self, key, val, dlmt = None):
        if type(val) == 'list' : 
            if dlmt is None : 
                dlmt = ','
            strng = ''
            for t in xrange(len(val)):
                if t == (len(val) - 1) : 
                    dlmt = '\r\n'
                if val[t] is True : 
                    v = 'True'
                elif val[t] is False : 
                    v = 'False'
                else : 
                    return False
                strng += v + dlmt
            self.fobj.write((key + ' = ' + strng).encode('utf-8'))
        else : 
            if val is True : 
                v = 'True'
            elif val is False : 
                v = 'False'
            else : 
                return False
            self.fobj.write((key + ' = ' + v + '\r\n').encode('utf-8'))




    def writecomment(self, text):
        self.fobj.write((u';' + text + u'\r\n').encode('utf-8'))



