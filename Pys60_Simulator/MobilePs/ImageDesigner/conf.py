# -*- coding: utf-8 -*-
import appuifw
from sysinfo import display_pixels as display_pixels
import iniparser
import os
import sys
__version__ = 1.4
def he(state):
    if state is None : 
        return 'None'
    return ('%06x' % state)




class Cconf :


    __module__ = __name__
    def __init__(self):
        self.toolbar_slidespeed = 0
        self.cursor = 0
        self.cursorsize = 0
        self.cursormultiplier = 0
        self.undo_size = 0
        self.rectselecttype = 0
        self.statusbarupdatecicles = 0
        self.lastpath_img = 'c:\\'
        self.ui_menu_font = None
        self.ui_menu_font_bold = None
        self.ui_menu_font_fheight = None
        self.ui_menu_color = None
        self.ui_prog_color = None
        self.ui_grid_color = None
        self.ui_req_color = None
        self.recentfiles = None
        self.lang = None
        self.lang_list = None
        self.toolbar_slidespeed = None
        self.curs_del = None
        self.curs_step = None
        self.lastpath_img = None
        self.skin = 'default'
        self.screensize = None
        self.exitconfirm = 0
        self.curs_lastdelind = None
        self.keyconfig = None
        self.firststart = False




    def save(self, path):
        self.opt_list_keys = ['toolspanel', 'colorspanel', 'brushsize', 'winswitch', 'zoom', 'zoomin', 'zoomout', 'zoom_multiply', 'zoom_1_1', 'font', 'undo', 'redo', 'copy', 'cut', 'paste', 'clear', 'templet', 'preview', 'imtemplet', 'navigation', 'gradient']
        parser = iniparser.TIniParser()
        parser.create(path)
        parser.writegroup('MISC')
        parser.writeint('firststart', 0)
        parser.writeint('language', self.lang)
        parser.writeint('skin', self.skin)
        parser.writeint('toolslidespeed', (self.toolbar_slidespeed - 1))
        parser.writeint('cursortype', self.cursor)
        parser.writeint('cursorsize', (self.cursorsize - 1))
        parser.writeint('changecursor', self.cursormultiplier)
        parser.writeint('undosize', self.undo_size)
        parser.writeint('rectselecttype', self.rectselecttype)
        parser.writeint('cursordelay', self.curs_del, ',')
        parser.writeint('cursorstep', self.curs_step, ',')
        parser.writestr('imagefolder', self.lastpath_img)
        parser.writeint('confirmonexit', self.exitconfirm)
        parser.writecomment('')
        parser.writegroup('DISPLAY')
        if self.screen_size != display_pixels() : 
            size = str(self.screen_size[0]) + ',' + str(self.screen_size[1])
        else : 
            size = 'None'
        parser.writeint('force_display_size', size)
        parser.writecomment('example: force_display_size = 240,320')
        parser.writecomment('')
        parser.writegroup('UI_FONTS')
        parser.writestr('menu_font', self.ui_menu_font[0])
        parser.writestr('status_font', self.ui_status_font[0])
        parser.writeint('menu_font_forceheight', self.ui_menu_font_fheight)
        parser.writecomment('')
        parser.writegroup('UI_COLORS')
        parser.writestr('menu_form_out', he(self.ui_menu_color[0][0]))
        parser.writestr('menu_form_in', he(self.ui_menu_color[0][1]))
        parser.writestr('menu_form_shade', he(self.ui_menu_color[0][2]))
        parser.writestr('menu_selbox_out', he(self.ui_menu_color[1][0]))
        parser.writestr('menu_selbox_in', he(self.ui_menu_color[1][1]))
        parser.writestr('menu_item', he(self.ui_menu_color[1][2]))
        parser.writestr('menu_selitem', he(self.ui_menu_color[1][3]))
        parser.writestr('menu_blckitem', he(self.ui_menu_color[1][4]))
        parser.writestr('backgr_form', he(self.ui_form_color[2]))
        parser.writestr('status_form', he(self.ui_form_color[0]))
        parser.writestr('status_font', he(self.ui_form_color[1]))
        parser.writestr('editor_scroll_outline', he(self.ui_form_color[3][0]))
        parser.writestr('editor_scroll_slider', he(self.ui_form_color[3][1]))
        parser.writestr('editor_scroll_fill', he(self.ui_form_color[3][2]))
        parser.writestr('grid_selector_color', he(self.ui_grid_color))
        parser.writestr('fileman_background', he(self.ui_req_color[0]))
        parser.writestr('fileman_infobar', he(self.ui_req_color[1]))
        parser.writestr('fileman_selbox_out', he(self.ui_req_color[2][0]))
        parser.writestr('fileman_selbox_in', he(self.ui_req_color[2][1]))
        parser.writestr('fileman_item', he(self.ui_req_color[2][2]))
        parser.writestr('fileman_selitem', he(self.ui_req_color[2][3]))
        parser.writestr('fileman_markitem', he(self.ui_req_color[2][4]))
        parser.writestr('fileman_scroll_outline', he(self.ui_req_color[3][0]))
        parser.writestr('fileman_scroll_slider', he(self.ui_req_color[3][1]))
        parser.writestr('fileman_scroll_fill', he(self.ui_req_color[3][2]))
        parser.writestr('progressbar_out', he(self.ui_prog_color[0]))
        parser.writestr('progressbar_slider', he(self.ui_prog_color[1]))
        parser.writestr('progressbar_fill', he(self.ui_prog_color[2]))
        parser.writecomment('')
        parser.writegroup('HOTKEYS')
        keys = [x[2] for x in self.keyconfig.data]
        mods = [x[3] for x in self.keyconfig.data]
        parser.writeint('keys', keys)
        parser.writeint('mods', mods)
        parser.writeint('mods_timeout', self.keyconfig.gettimeout())
        parser.writecomment('')
        parser.writegroup('CUSTOM_PALETTES')
        for t in xrange(len(self.custompal)):
            parser.writestr(str(t), self.custompal[t])
        parser.writecomment('')
        parser.writegroup('RECENT_FILES')
        for t in self.recentfiles:
            parser.writestr(t, '')
        parser.close()




    def load(self, program_path):
        valuelist = []
        parser = iniparser.TIniParser()
        opt_list_def = ['language', 'toolslidespeed', 'cursortype', 'cursorsize', 'changecursor', 'undosize', 'rectselecttype']
        parser.open(program_path + 'config.ini')
        parser.readgroup('MISC')
        self.firststart = parser.readint('firststart', 10, 1)
        valuelist.append(self.lang_list.index(self.lang))
        for t in xrange(1, 7):
            valuelist.append(parser.readint(opt_list_def[t]))
        self.curs_del = parser.readint('cursordelay', 10, self.curs_del, ',')
        self.curs_step = parser.readint('cursorstep', 10, self.curs_step, ',')
        self.curs_lastdelind = (len(self.curs_del) - 1)
        if len(self.curs_del) != len(self.curs_step) : 
            raise NameError('curs_del<>curs_step')
        self.lastpath_img = parser.readstr('imagefolder')
        if  not (os.path.exists(self.lastpath_img)) or self.lastpath_img == '' : 
            self.lastpath_img = 'C:\\'
        valuelist.append(parser.readint('confirmonexit'))
        parser.readgroup('HOTKEYS')
        n = [None for x in self.keyconfig.data]
        keys = parser.readint('keys', 10, n, ',')
        mods = parser.readint('mods', 10, n, ',')
        self.keyconfig.settimeout(parser.readint('mods_timeout', 10, 1000))
        self.keyconfig.setkeycodedata((keys, mods))
        parser.readgroup('UI_FONTS')
        font = parser.readstr('menu_font')
        if font is not None : 
            self.ui_menu_font = (unicode(font), None)
        fnt = parser.readstr('status_font')
        if fnt is not None : 
            self.ui_status_font = (unicode(fnt), None)
        self.ui_menu_font_fheight = parser.readint('menu_font_forceheight')
        parser.readgroup('UI_COLORS')
        self.ui_menu_color = [[0, 0, 0], [0, 0, 0, 0, 0]]
        self.ui_form_color = [0, 0, 0, [0, 0, 0]]
        self.ui_prog_color = [0, 0, 0]
        self.ui_menu_color[0][0] = parser.readint('menu_form_out', 16)
        self.ui_menu_color[0][1] = parser.readint('menu_form_in', 16)
        self.ui_menu_color[0][2] = parser.readint('menu_form_shade', 16)
        self.ui_menu_color[1][0] = parser.readint('menu_selbox_out', 16)
        self.ui_menu_color[1][1] = parser.readint('menu_selbox_in', 16)
        self.ui_menu_color[1][2] = parser.readint('menu_item', 16)
        self.ui_menu_color[1][3] = parser.readint('menu_selitem', 16)
        self.ui_menu_color[1][4] = parser.readint('menu_blckitem', 16)
        self.ui_form_color[2] = parser.readint('backgr_form', 16)
        self.ui_form_color[0] = parser.readint('status_form', 16)
        self.ui_form_color[1] = parser.readint('status_font', 16)
        self.ui_form_color[3][0] = parser.readint('editor_scroll_outline', 16)
        self.ui_form_color[3][1] = parser.readint('editor_scroll_slider', 16)
        self.ui_form_color[3][2] = parser.readint('editor_scroll_fill', 16)
        self.ui_grid_color = parser.readint('grid_selector_color', 16)
        self.ui_req_color = [0, 0, [0, 0, 0, 0, 0, 0], [0, 0, 0]]
        self.ui_req_color[0] = parser.readint('fileman_background', 16)
        self.ui_req_color[1] = parser.readint('fileman_infobar', 16)
        self.ui_req_color[2][0] = parser.readint('fileman_selbox_out', 16)
        self.ui_req_color[2][1] = parser.readint('fileman_selbox_in', 16)
        self.ui_req_color[2][2] = parser.readint('fileman_item', 16)
        self.ui_req_color[2][3] = parser.readint('fileman_selitem', 16)
        self.ui_req_color[2][4] = parser.readint('fileman_markitem', 16)
        self.ui_req_color[3][0] = parser.readint('fileman_scroll_outline', 16)
        self.ui_req_color[3][1] = parser.readint('fileman_scroll_slider', 16)
        self.ui_req_color[3][2] = parser.readint('fileman_scroll_fill', 16)
        self.ui_prog_color[0] = parser.readint('progressbar_out', 16)
        self.ui_prog_color[1] = parser.readint('progressbar_slider', 16)
        self.ui_prog_color[2] = parser.readint('progressbar_fill', 16)
        parser.readgroup('CUSTOM_PALETTES')
        for t in xrange(len(self.custompal)):
            self.custompal[t] = parser.readstr(str(t), '')
        self.recentfiles = parser.getkeys('RECENT_FILES')
        parser.close()
        return valuelist



