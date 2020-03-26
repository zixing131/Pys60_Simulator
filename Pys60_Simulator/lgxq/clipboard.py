# -*- coding: utf-8 -*-

__doc__ = 'Power Clipboard tool for Pys60 by Atrant'
__name__ = 'Power Clipboard tool for Pys60 by Atrant'
from os import makedirs as makedirs
symbian = [144, 145, 146, 147, 148, 149, 129, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 209, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207]
symbia2 = [192, 193, 194, 195, 196, 197, 168, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 220, 219, 218, 221, 222, 223, 224, 225, 226, 227, 228, 229, 184, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 252, 251, 250, 253, 254, 255]
normal = [1040, 1041, 1042, 1043, 1044, 1045, 1025, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1105, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103]
def __tosymbian(string):
    res = ''
    i = 0
    while i < len(string) : 
        char = string[i]
        i += 1
        tmp = ord(char)
        if char == '\n' or tmp == 8233 : 
            res += chr(14) + chr(32) + chr(41)
            continue
        index = -1
        for k in range(len(symbia2)):
            if symbia2[k] == tmp or normal[k] == tmp : 
                index = k
                break
        if index == -1 : 
            try :
                res += char
            except :
                res += char.encode('utf-8')
            pass
        else : 
            res += unichr(symbian[index])
    return res




def __tonormal(string):
    res = ''
    for i in range(len(string)):
        char = string[i]
        tmp = ord(char)
        index = -1
        for k in range(len(symbian)):
            if symbian[k] == tmp : 
                index = k
                break
        if index == -1 : 
            res += char
        else : 
            res += unichr(normal[index])
    return res




def Get():


    def Read32(f):
        tmp = f.read(4)
        result = (ord(tmp[3]) * 16777216) + (ord(tmp[2]) * 65536) + (ord(tmp[1]) * 256) + ord(tmp[0])
        return result


    try :
        f = open(u'D:\\system\\Data\\Clpboard.cbd', 'rb')
        f.seek(20)
        length = Read32(f)
        text = ''
        i = 0
        while i < length : 
            char = f.read(1)
            if char == chr(18) or char == chr(3) : 
                continue
            elif char == chr(14) : 
                tmp = f.read(2)
                if tmp == chr(32) + chr(41) : 
                    char = '\n'
                else : 
                    f.seek(-2, 1)
                    continue
                pass
            elif char == chr(64) : 
                tmp = f.read(2)
                if tmp == chr(169) + chr(169) : 
                    char = '\n\n'
                    length += 1
                else : 
                    f.seek(-2, 1)
                    continue
                pass
            elif char == chr(169) : 
                char = '\n'
                length += 1
            text += char
            i += 1
        return __tonormal(text)
    except :
        return False




def print_exception():
    import sys
    import traceback
    type, value, tb = sys.exc_info()
    sys.last_type = type
    sys.last_value = value
    sys.last_traceback = tb
    tblist = traceback.extract_tb(tb)
    del tblist[: 1]
    list = traceback.format_list(tblist)
    if list : 
        list.insert(0, u'Tra' + 'ce:\n')
    list[len(list) :] = traceback.format_exception_only(type, value)
    tblist = tb = None
    import appuifw
    appuifw.app.body.add(unicode(str(list).replace('\\n', '\n')))




def Set(text):
    try :
        try :
            text = text.decode('utf-8')
        except :
            pass
        import struct
        header = chr(55) + (chr(0) * 2) + (chr(16) * 2) + chr(58) + chr(0) + chr(16) + (chr(0) * 4) + chr(106) + chr(252) + chr(123) + chr(3)
        encstr = chr(18)
        txt = __tosymbian(text)
        strtxt = ''
        for i in range(len(txt)):
            char = txt[i]
            if char == '\n' : 
                strtxt += chr(14) + chr(32) + chr(41)
                continue
            tmp = ord(char)
            if tmp > 255 : 
                tmp = ord(u' ')
            strtxt += struct.pack('B', tmp)
        strlength = struct.pack('I', len(strtxt.replace(chr(14) + chr(32) + chr(41), ' ')))
        contentend = chr(0) + chr(2) + chr(29) + chr(58) + chr(0) + chr(16) + chr(20) + (chr(0) * 3)
        totallength = ((4 + len(header)) + len(strlength) + len(encstr) + len(text) + len(contentend) - 9)
        totallength = struct.pack('I', 0)
        try :
            makedirs(u'D:\\system\\Data\\')
        except :
            pass
        f = open(u'D:\\system\\Data\\Clpboard.cbd', 'wb')
        f.write(header + totallength + strlength + encstr)
        f.write(strtxt)
        f.write(contentend)
        f.close()
        f = open(u'D:\\system\\Data\\Clpboard.cbd', 'a+b')
        pos = f.tell()
        f.seek(16)
        f.write(struct.pack('I', (pos - 9)))
        f.close()
    except :
        return False
    return True


