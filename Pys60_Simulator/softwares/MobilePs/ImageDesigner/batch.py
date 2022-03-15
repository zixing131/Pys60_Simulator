# -*- coding: utf-8 -*-

import appuifw
import graphics
from os import path as path
from e32 import Ao_lock as Ao_lock
import os
import mbm
__version__ = 1.4
def ru(s):
    return s.decode('utf-8')




def ur(s):
    return s.encode('utf-8')




class Cbatch_processor :


    __module__ = __name__
    def __init__(self, dtext, dialog):
        self.dialog = dialog
        self.filelist = []
        self.filename = None
        self.lastpath = None
        self.winparam = []
        self.body = None
        self.optbody = None
        self.dtext = dtext
        self.outpath = 'E:\\Images'
        self.quality = 75
        self.bpp = 24
        self.compression = 'default'
        self.comprname = {'no' : self.dtext['comp_no'], 'fast' : self.dtext['comp_fast'], 'default' : self.dtext['comp_def'], 'best' : self.dtext['comp_best']}
        self.conf = None
        self.format = 'PNG'
        self.lock = Ao_lock()




    def open(self, lastpath, append = False):
        if append is False : 
            self.ind_main = self.save_winparam()
        try :
            self.filename = self.dialog.open(path = ur(lastpath), ext = ['jpg', 'png', 'gif', 'bmp', 'mbm', 'jpeg'], kind = 'open')
        except :
            self.filename = self.dialog.open(path = lastpath, ext = ['jpg', 'png', 'gif', 'bmp', 'mbm', 'jpeg'], kind = 'open')
        if self.filename is None : 
            return None
        if type(self.filename) == type('') or type(self.filename) == type(u'') : 
            if os.path.isfile(self.filename) : 
                self.lastpath = path.split(self.filename)[0]
                if append : 
                    self.filelist.append(self.filename)
                else : 
                    self.filelist = [self.filename]
                pass
            pass
        else : 
            self.lastpath = path.split(self.filename[0])[0]
            for t in self.filename:
                if os.path.isfile(t) : 
                    self.filelist.append(t)
            pass
        if  not (self.filelist) : 
            self.filelist.append(u'')
        self.select()




    def save_winparam(self):
        self.winparam.append((appuifw.app.screen, appuifw.app.body, appuifw.app.menu, appuifw.app.title, appuifw.app.exit_key_handler))
        return (len(self.winparam) - 1)




    def restore_winparam(self, ind):
        appuifw.app.screen, appuifw.app.body, appuifw.app.menu, appuifw.app.title, appuifw.app.exit_key_handler = self.winparam[ind]




    def exit(self):
        self.restore_winparam(self.ind_main)
        self.filelist = []
        self.filename = None
        self.lastpath = None
        self.winparam = []
        self.body = None
        self.optbody = None
        self.conf = None




    def select(self):
        appuifw.app.title = self.dtext['batchproc']
        appuifw.app.screen = 'normal'
        if self.body is None : 
            appuifw.app.body = self.body = appuifw.Listbox([path.split(x)[1] for x in self.filelist], lambda  : None )
        else : 
            self.body.set_list([path.split(x)[1] for x in self.filelist])
        appuifw.app.exit_key_handler = self.exit
        appuifw.app.menu = [((u'%s%s' % (self.dtext['add'], '...')), lambda  :  self.open(self.lastpath, True) ), (self.dtext['delete'], lambda  :  self.delete_item(self.body.current()) ), (self.dtext['clear'], lambda  :  self.delete_item('all') ), (self.dtext['outputopt'], self.outopt), (self.dtext['operation'], ((self.dtext['resize'], lambda  :  self.resize_query(self.filelist) ), (self.dtext['packmbm'] + '...', lambda  :  self.pack_to_mbm('', self.filelist) ), (self.dtext['convert'], lambda  :  self.do(self.filelist) ))), (self.dtext['close'], self.exit)]




    def optbody_update(self):
        self.pngconf = [(self.dtext['savepath'], unicode(self.outpath)), (self.dtext['format'], u'PNG'), (self.dtext['bpp'], unicode(self.bpp)), (self.dtext['compression'], unicode(self.comprname[self.compression]))]
        self.jpgconf = [(self.dtext['savepath'], unicode(self.outpath)), (self.dtext['format'], u'JPEG'), (self.dtext['quality'], unicode(self.quality))]
        if self.conf is None : 
            self.conf = self.pngconf
        elif self.conf[1][1] == u'PNG' : 
            self.conf = self.pngconf
            self.format = 'PNG'
        elif self.conf[1][1] == u'JPEG' : 
            self.conf = self.jpgconf
            self.format = 'JPG'




    def outopt(self):
        self.ind_select = self.save_winparam()
        self.optbody_update()
        appuifw.app.title = self.dtext['outputopt']
        appuifw.app.screen = 'normal'
        appuifw.app.body = self.optbody = appuifw.Listbox(self.conf, self.outopt_edit)
        appuifw.app.exit_key_handler = lambda  :  self.restore_winparam(self.ind_select) 
        appuifw.app.menu = [(self.dtext['ok'], lambda  :  self.restore_winparam(self.ind_select) )]




    def outopt_edit(self):
        ind = self.optbody.current()
        if ind == 0 : 
            result = appuifw.query(self.dtext['savepath'], 'text', unicode(self.outpath))
            if result is None : 
                return None
            if path.exists(result) : 
                self.outpath = result
            else : 
                appuifw.note(self.dtext['pathnexist'], 'error')
            self.optbody_update()
            cur = self.optbody.current()
            self.optbody.set_list(self.conf, cur)
        elif ind == 1 : 
            if self.conf == self.pngconf : 
                self.conf = self.jpgconf
                self.format = 'JPG'
            else : 
                self.conf = self.pngconf
                self.format = 'PNG'
            cur = self.optbody.current()
            self.optbody.set_list(self.conf, cur)
        elif ind == 2 : 
            if self.conf == self.jpgconf : 
                result = appuifw.query(self.dtext['quality'], 'number', unicode(self.quality))
                if result is None : 
                    return None
                if 1 > self.quality > 100 : 
                    appuifw.note(self.dtext['e_wrongqual'], 'error')
                    return None
                self.quality = result
                self.optbody_update()
                cur = self.optbody.current()
                self.optbody.set_list(self.conf, cur)
            elif self.conf == self.pngconf : 
                bpp = [24, 8, 1]
                name = [self.dtext['bpp_24'], self.dtext['bpp_8'], self.dtext['bpp_1']]
                ind = appuifw.popup_menu(name, self.dtext['bpp'])
                if ind is None : 
                    return None
                self.bpp = bpp[ind]
                self.optbody_update()
                cur = self.optbody.current()
                self.optbody.set_list(self.conf, cur)
            pass
        elif ind == 3 : 
            if self.conf == self.jpgconf : 
                pass
            if self.conf == self.pngconf : 
                vals = ['no', 'fast', 'default', 'best']
                compr = [self.dtext['comp_no'], self.dtext['comp_fast'], self.dtext['comp_def'], self.dtext['comp_best']]
                ind = appuifw.popup_menu(compr, self.dtext['compression'])
                if ind is None : 
                    return None
                self.compression = vals[ind]
                self.optbody_update()
                cur = self.optbody.current()
                self.optbody.set_list(self.conf, cur)
            pass




    def delete_item(self, ind):
        if ind == 'all' : 
            self.filelist = []
        else : 
            self.filelist.pop(ind)
            if self.filelist : 
                self.body.set_list([path.split(x)[1] for x in self.filelist])
            pass
        if  not (self.filelist) : 
            self.body.set_list([u''])




    def resize_query(self, files):
        width = appuifw.query(self.dtext['width'], 'number', 240)
        if width is not None : 
            height = appuifw.query(self.dtext['height'], 'number', 320)
            if height is not None : 
                asp = appuifw.query(self.dtext['keepaspect'], 'query')
                if asp is None : 
                    asp = 0
                else : 
                    asp = 1
                pass
            pass


        def resize(im):
            return im.resize((width, height), keepaspect = asp)


        self.do(files, resize)




    def pack_to_mbm(self, outfile, files):
        try :
            outfile = self.dialog.open(path = ur(self.lastpath), ext = ['jpg', 'png', 'gif', 'bmp', 'mbm', 'jpeg'], kind = 'save')
        except :
            outfile = self.dialog.open(path = self.lastpath, ext = ['jpg', 'png', 'gif', 'bmp', 'mbm', 'jpeg'], kind = 'save')
        if outfile is None : 
            return None
        if path.isfile(ur(outfile)) : 
            defname = path.split(outfile)[1]
        else : 
            defname = u'noname'
        dirname = path.split(outfile)[0] + '\\'
        dirname = dirname.replace('\\\\', '\\')
        self.lastpath = dirname
        confirm = False
        while  not (confirm) : 
            name = appuifw.query(self.dtext['saveas'] + u':', 'text', defname)
            if name is None : 
                return None
            if path.splitext(name)[1].lower() != '.mbm' : 
                name += '.mbm'
            outfile = dirname + name
            if path.exists(ur(outfile)) : 
                confirm = appuifw.query(self.dtext['owconfirm'], 'query')
            else : 
                confirm = True
        arg = []
        for t in xrange(len(files)):
            arg.append(path.split(files[t])[1] + ':24,1,0,0')
        indir = path.split(files[0])[0] + '\\'
        self.delete_item('all')
        self.body.set_list([self.dtext['processing'] + ': 0%'])
        m = mbm.MbmPack(outfile, in_dir = indir, files = arg)
        m.PACK(self.progress)
        self.body.set_list([u''])
        appuifw.note(self.dtext['done'])




    def progress(self, percent):
        self.body.set_list([('%s: %s%%' % (self.dtext['processing'], unicode(percent)))])




    def do(self, files, function = None):
        self.delete_item('all')
        self.body.set_list([self.dtext['processing'] + ': 0%'])
        total = len(files)
        if self.format == 'JPEG' : 
            ext = '.jpg'
        elif self.format == 'PNG' : 
            ext = '.png'
        for t in xrange(total):
            try :
                im = graphics.Image.open(files[t])
            except SymbianError : 
                appuifw.note(u'Could not to open: ' + path.split(files[t])[1], 'error')
                continue
            if function is None : 
                newim = im
            else : 
                newim = function(im)
            self.progress(((t * 100) / total))
            outname = path.splitext(path.join(self.outpath, path.split(files[t])[1]))[0] + ext
            try :
                if self.format == 'PNG' : 
                    newim.save(outname, bpp = self.bpp, compression = self.compression, format = self.format)
                else : 
                    newim.save(outname, quality = self.quality, format = self.format)
            except :
                appuifw.note(self.dtext['cantsave'], 'error')
            im = None
            newim = None
        self.body.set_list([u''])
        appuifw.note(self.dtext['done'])



