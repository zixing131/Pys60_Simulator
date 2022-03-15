# -*- coding: utf-8 -*-

from os import path as path
from os import listdir as listdir
import iniparser
import appuifw
__version__ = 1.4
def ru(s):
    return s.decode('utf-8')




def lang_find(program_path):
    lang_list = []
    itlist = listdir(program_path + 'Lang\\')
    for item in itlist:
        if path.isfile(program_path + 'Lang\\' + item) and item[-3 : ].lower() == 'lng' : 
            lang_list.append(unicode(item[ : -4].lower()))
    if len(lang_list) == 0 : 
        appuifw.note(u'language file is not found')
    return lang_list




def lang_define(program_path):
    parser = iniparser.TIniParser()
    try :
        parser.open(program_path + 'config.ini')
        parser.readgroup('MISC')
        firststart = parser.readint('firststart', 10, 1)
        if firststart == 1 : 
            parser.close()
            return False
        else : 
            lang = parser.readstr('language')
            parser.close()
    except :
        appuifw.note(u'language file is not set')
        lang = '中文'
    return lang




def lang_selectnow(langs):
    ind = appuifw.popup_menu(langs, '选择你的语言:'.decode('utf8'))
    return ind




def lang_readfromfile(program_path, lang, app_version):
    parser = iniparser.TIniParser()
    dtext = parser.getdictfromfile(program_path + 'Lang\\' + lang + '.lng')
    return dtext




def lang_load(program_path, app_version):
    lang_list = lang_find(program_path)
    lang = lang_define(program_path)
    if lang == False : 
        ind = lang_selectnow(lang_list)
        if ind is None : 
            ind = 0
        lang = lang_list[ind]
    elif  not (lang in lang_list) : 
        appuifw.note(u'language file is missing')
    dtext = lang_readfromfile(program_path, lang, app_version)
    return (lang_list, lang, dtext)






def key_getkeycode(self, ind):
    return self.data[ind][2]




def mod_getkeycode(self, ind):
    return self.data[ind][3]




def timeout_tick(self):
    if self.counter is not None : 
        if (clock() - self.counter) > self.timeout : 
            self.counter = None
            self.mods_unbind()
            self.hotkeys_set()
        pass




def hotkeys_unbind_old(self):
    for t in xrange(len(self.olddata)):
        k = self.olddata[t][2]
        m = self.olddata[t][3]
        if k is not None : 
            self.canvas.bind(k, lambda  : None )
            self.canvas.bind(k, None)
        if m is not None : 
            self.canvas.bind(m, lambda  : None )
            self.canvas.bind(m, None)




def hotkeys_set(self):
    xclude = []
    self.modspair = []
    for t in xrange(len(self.data)):
        k = self.data[t][2]
        m = self.data[t][3]
        if k is not None and m is None : 
            self.canvas.bind(k, self.data[t][1])
        if m is not None and k is not None and t not in xclude : 
            indx = [x for x in xrange(len(self.data)) if m == self.data[x][3] and self.data[x][2] is not None ]
            self.modspair.append((m, indx))
            xclude.extend(indx)
        else : 
            pass
    self.mods_bind(self.modspair)




def mods_bind(self, modspair):
    if modspair : 
        for mp in modspair:
            self.canvas.bind(mp[0], partial(self.enable_modifier, mp[1]))
        pass




def mods_unbind(self):
    for t in xrange(len(self.data)):
        m = self.data[t][3]
        if m is not None : 
            self.canvas.bind(m, lambda  : None )
            self.canvas.bind(m, None)




def enable_modifier(self, indexes):
    if indexes : 
        if self.gettimeout() is not None : 
            self.counter = clock()


        self.hotkeys_clear()
        def modifier_funct(fun):
            try :
                if callable(self.offmod_callback) : 
                    self.offmod_callback()
                fun()
                self.mods_unbind()
                self.hotkeys_set()
            except :
                traceback.print_exc(sys.stderr)


        for t in indexes:
            k = self.data[t][2]
            m = self.data[t][3]
            if k is not None and m is not None : 
                self.canvas.bind(k, partial(modifier_funct, self.data[t][1]))
        if callable(self.onmod_callback) : 
            self.onmod_callback(self.keycodetostr(m), self.timeout)
        pass




def hotkeys_clear(self):
    for t in xrange(len(self.data)):
        k = self.data[t][2]
        m = self.data[t][3]
        if k is not None : 
            self.canvas.bind(k, lambda  : None )
            self.canvas.bind(k, None)
        if m is not None : 
            self.canvas.bind(m, lambda  : None )
            self.canvas.bind(m, None)




def hotkeys_on(self):
    for t in xrange(len(self.data)):
        k = self.data[t][2]
        m = self.data[t][3]
        if k is not None and m is None : 
            self.canvas.bind(k, self.data[t][1])
        self.mods_bind(self.modspair)




def hotkeys_off(self):
    for t in xrange(2, len(self.data)):
        k = self.data[t][2]
        m = self.data[t][3]
        if k is not None and m is None : 
            self.canvas.bind(k, lambda  : None )
            self.canvas.bind(k, None)
        if m is not None : 
            self.canvas.bind(m, lambda  : None )
            self.canvas.bind(m, None)




def getkeycodedata(self):
    return ([x[2] for x in self.data], [x[3] for x in self.data])




def setkeycodedata(self, kdata):
    for t in xrange(len(self.data)):
        self.data[t][2] = kdata[0][t]
        self.data[t][3] = kdata[1][t]
    self.hotkeys_set()






def partial(func, *args, **keywords):


    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args + fargs, **newkeywords)


    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

