# -*- coding: utf-8 -*-
import appuifw
import key_codes
from time import clock as clock
import sys
import traceback
__version__ = 1.4
class CKeyConfig(object, ) :


    __module__ = __name__
    def __init__(self, app, canv, itemlist, dtext):
        self.dtext = dtext
        self.timeout = 1.0
        self.keylist = [self.dtext['none'], u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'*', u'#', u'Yes', u'No', u'Pen', u'C']
        self.keys_reset(itemlist)
        self.lst = [(self.dtext['function'], self.data[0][0]), (self.dtext['key'], self.keycodetostr(self.data[0][2])), (self.dtext['modifier'], self.keycodetostr(self.data[0][3])), (self.dtext['modtimeout'], unicode(int((self.timeout * 1000))))]
        self.body = appuifw.Listbox(self.lst, self.itemevent)
        self.app = app
        self.canvas = canv
        self.curfunctind = 0
        self.counter = None
        self.onmod_callback = None
        self.offmod_callback = None
        self.body.bind(key_codes.EKeyRightArrow, self.nextitem)
        self.body.bind(key_codes.EKeyLeftArrow, self.previtem)




    def itemevent(self):
        it = self.body.current()
        if it == 0 : 
            ind = appuifw.popup_menu(self.functname, self.dtext['function'])
            if ind is None : 
                return None
            else : 
                self.set_function(ind)
            pass
        elif it == 1 : 
            ind = appuifw.popup_menu(self.keylist + [self.dtext['enterkeycode']], self.dtext['key'])
            if ind is None : 
                return None
            elif ind == 17 : 
                self.enter_keycode(0)
            else : 
                self.set_key(self.curfunctind, self.strtokeycode(self.keylist[ind]))
            pass
        elif it == 2 : 
            ind = appuifw.popup_menu(self.keylist + [self.dtext['enterkeycode']], self.dtext['modifier'])
            if ind is None : 
                return None
            elif ind == 17 : 
                self.enter_keycode(1)
            else : 
                self.set_mod(self.curfunctind, self.strtokeycode(self.keylist[ind]))
            pass
        elif it == 3 : 
            to = appuifw.query(self.dtext['modtimeout'], 'number', self.gettimeout())
            if to is None : 
                return None
            else : 
                self.settimeout(to)
            pass




    def nextitem(self):
        it = self.body.current()
        if it == 0 : 
            ind = (self.curfunctind + 1)
            if ind > (len(self.data) - 1) : 
                ind = 0
            self.set_function(ind)
        elif it == 1 : 
            k = self.curkeyind()
            if k == -1 : 
                ind = 0
            else : 
                ind = (k + 1)
            if ind > (len(self.keylist) - 1) : 
                ind = 0
            self.set_key(self.curfunctind, self.strtokeycode(self.keylist[ind]))
        elif it == 2 : 
            k = self.curmodind()
            if k == -1 : 
                ind = 0
            else : 
                ind = (k + 1)
            if ind > (len(self.keylist) - 1) : 
                ind = 0
            self.set_mod(self.curfunctind, self.strtokeycode(self.keylist[ind]))
        elif it == 3 : 
            if self.gettimeout is None : 
                self.settimeout(100)
            else : 
                self.settimeout((self.gettimeout() + 50))
            pass




    def previtem(self):
        it = self.body.current()
        if it == 0 : 
            ind = (self.curfunctind - 1)
            if ind < 0 : 
                ind = (len(self.data) - 1)
            self.set_function(ind)
        elif it == 1 : 
            k = self.curkeyind()
            if k == -1 : 
                ind = (len(self.keylist) - 1)
            else : 
                ind = (k - 1)
            if ind < 0 : 
                ind = (len(self.keylist) - 1)
            self.set_key(self.curfunctind, self.strtokeycode(self.keylist[ind]))
        elif it == 2 : 
            k = self.curmodind()
            if k == -1 : 
                ind = (len(self.keylist) - 1)
            else : 
                ind = (k - 1)
            if ind < 0 : 
                ind = (len(self.keylist) - 1)
            self.set_mod(self.curfunctind, self.strtokeycode(self.keylist[ind]))
        elif it == 3 : 
            if self.gettimeout is None : 
                self.settimeout(10000)
            else : 
                self.settimeout((self.gettimeout() - 50))
            pass




    def set_function(self, ind):
        self.curfunctind = ind
        self.listbox_update()




    def settimeout(self, to):
        if to is None : 
            self.timeout = None
        elif to < 100 or to > 10000 : 
            self.timeout = None
        else : 
            self.timeout = (float(to) / 1000)
        self.listbox_update(3)




    def gettimeout(self):
        if self.timeout == None : 
            return None
        else : 
            return int((self.timeout * 1000))




    def curkeyind(self):
        try :
            return self.keylist.index(self.lst[1][1])
        except :
            return -1




    def curmodind(self):
        try :
            return self.keylist.index(self.lst[2][1])
        except :
            return -1




    def listbox_update(self, it = 0):
        self.lst[0] = (self.dtext['function'], self.data[self.curfunctind][0])
        key = self.keycodetostr(self.data[self.curfunctind][2])
        if key == u'' : 
            key = u'keycode:' + unicode(self.data[self.curfunctind][2])
        mod = self.keycodetostr(self.data[self.curfunctind][3])
        if mod == u'' : 
            mod = u'keycode:' + unicode(self.data[self.curfunctind][3])
        self.lst[1] = (self.dtext['key'], self.keycodetostr(self.data[self.curfunctind][2]))
        self.lst[2] = (self.dtext['modifier'], self.keycodetostr(self.data[self.curfunctind][3]))
        self.lst[3] = (self.dtext['modtimeout'], unicode(self.gettimeout()))
        self.body.set_list(self.lst, it)




    def enter_keycode(self, ind):
        if ind is None : 
            return None
        keycode = appuifw.query(self.dtext['enterkeycode'], 'number', 0)
        if ind == 0 : 
            self.set_key(self.curfunctind, keycode)
        else : 
            self.set_mod(self.curfunctind, keycode)




    def set_key(self, find, keycode):
        k = self.issamekey(find, keycode, self.data[find][3])
        if k is not None : 
            res = appuifw.query(self.dtext['alreadybound'] + ' ' + self.data[k[0]][0] + '.' + self.dtext['rebind'], 'query')
            if res is None : 
                return None
            elif res is True : 
                self.data[k[0]][2] = None
                self.data[k[0]][3] = None
            pass
        self.data[find][2] = keycode
        self.listbox_update(1)




    def set_mod(self, find, keycode):
        k = self.issamekey(find, self.data[find][2], keycode)
        if k is not None : 
            res = appuifw.query(self.dtext['alreadybound'] + ' ' + self.data[k[0]][0] + '.' + self.dtext['rebind'], 'query')
            if res is None : 
                return None
            elif res is True : 
                self.data[k[0]][2] = None
                self.data[k[0]][3] = None
            pass
        self.data[find][3] = keycode
        self.listbox_update(2)




    def issamekey(self, ind, key, mod):
        for t in xrange(len(self.data)):
            if ind != t : 
                if key == self.data[t][2] and key != None : 
                    if mod == self.data[t][3] : 
                        return (t, 2)
                    pass
                if key == self.data[t][3] and mod is None and key != None : 
                    return (t, 2)
                pass
        return None




    def keys_reset(self, itemlist, keys = None, mods = None):
        self.data = itemlist
        self.functname = list(zip(*self.data)[0])
        if keys is not None : 
            for t in xrange(len(self.data)):
                self.data[t][2] = keys[t]
            pass
        if mods is not None : 
            for t in xrange(len(self.data)):
                self.data[t][3] = mods[t]
            pass




    def reset_position(self):
        self.curfunctind = 0
        self.lst = [(self.dtext['function'], self.data[self.curfunctind][0]), (self.dtext['key'], self.keycodetostr(self.data[0][2])), (self.dtext['modifier'], self.keycodetostr(self.data[0][3])), (self.dtext['modtimeout'], unicode(self.gettimeout()))]
        self.body.set_list(self.lst, 0)




    def app_backup(self):
        self.oldapppar = (self.app.screen, self.app.body, self.app.menu, self.app.title, self.app.exit_key_handler)




    def app_restore(self):
        self.app.screen, self.app.body, self.app.menu, self.app.title, self.app.exit_key_handler = self.oldapppar




    def data_backup(self):
        self.olddata = [x[ : ] for x in self.data]




    def data_restore(self):
        self.data = self.olddata




    def exit(self, prmt = 0):
        if prmt == 0 : 
            self.hotkeys_unbind_old()
            self.hotkeys_set()
        elif prmt == 1 and self.data != self.olddata : 
            res = appuifw.query(self.dtext['savechange'], 'query')
            if res is None : 
                self.data_restore()
            else : 
                self.hotkeys_unbind_old()
                self.hotkeys_set()
            pass
        elif prmt == 2 : 
            self.data_restore()
        self.app_restore()




    def execute(self):
        self.app_backup()
        self.data_backup()
        self.reset_position()
        self.app.exit_key_handler = lambda  :  self.exit(1) 
        self.app.menu = [(self.dtext['ok'], lambda  :  self.exit(0) ), (self.dtext['cancel'], lambda  :  self.exit(2) )]
        self.app.title = self.dtext['keyconfig']
        self.app.screen = 'normal'
        self.app.body = self.body




    def strtokeycode(self, state):
        if state == u'#' : 
            return key_codes.EKeyHash
        elif state == u'*' : 
            return key_codes.EKeyStar
        elif state == u'Yes' : 
            return key_codes.EKeyYes
        elif state == u'No' : 
            return key_codes.EKeyNo
        elif state == u'C' : 
            return key_codes.EKeyBackspace
        elif state == u'Pen' : 
            return key_codes.EKeyEdit
        elif state == u'None' or state == self.dtext['none'] : 
            return None
        elif int(state) >= 0 and int(state) <= 9 : 
            return (48 + int(state))
        else : 
            return -1




    def keycodetostr(self, state):
        if state == key_codes.EKeyHash : 
            return u'#'
        elif state == key_codes.EKeyStar : 
            return u'*'
        elif state == key_codes.EKeyYes : 
            return u'Yes'
        elif state == key_codes.EKeyNo : 
            return u'No'
        elif state == key_codes.EKeyBackspace : 
            return u'C'
        elif state == key_codes.EKeyEdit : 
            return u'Pen'
        elif 48 <= state <= 57 : 
            return unicode((state - 48))
