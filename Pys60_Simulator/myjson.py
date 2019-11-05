import types
rp = lambda url:url.replace("\/","/")
#ch = lambda str:"".join(map(lambda x:x != "" and unichr(int(x,16)) or "",str.split("\\u")))
false = False
true = True
def ch(str):
    l = str.split("\\u")
    for i in range(len(l)):
        if l[i]:
            try:
                l[i] = unichr(int(l[i],16))
            except:pass
    return "".join(l)
class json(object):
    def ch_dict(self,dict):
        for x in dict.keys():
            if type(dict[x]) == types.StringType:
                if dict[x].find("http://")!=-1:
                    dict[x] = rp(dict[x])
                elif dict[x].find("\\u")!=-1:
                    dict[x] = ch(dict[x])
                else:
                    dict[x] = dict[x]
            elif type(dict[x]) == types.DictionaryType:
                dict[x] = self.ch_dict(dict[x])
            elif type(dict[x]) == types.ListType:
                dict[x] = self.ch_list(dict[x])
            else:
                dict[x] = dict[x]
        return dict
    def ch_list(self,list):
        for x in range(len(list)):
            if type(list[x]) == types.StringType:
                if list[x].find("http://")!=-1:
                    list[x] = rp(list[x])
                elif list[x].find("\\u")!=-1:
                    list[x] = ch(list[x])
                else:pass
            elif type(list[x]) == types.DictType:
                list[x] = self.ch_dict(list[x])
            elif type(list[x]) == types.ListType:
                list[x] = self.ch_list(list[x])
        return list
    def loads(self,str):
        mydict = eval(str)
        if(type(mydict) is dict):
            for x in mydict.keys():
                if type(mydict[x]) == types.StringType:
                    if mydict[x].find("http://")!=-1:
                        mydict[x] = rp(mydict[x])
                    elif mydict[x].find("\\u")!=-1:
                        mydict[x] = ch(mydict[x])
                    else:pass
                elif type(mydict[x]) == types.DictType:
                    mydict[x] = self.ch_dict(mydict[x])
                elif type(mydict[x]) == types.ListType:
                    mydict[x] = self.ch_list(mydict[x])
        return mydict
json=json()
