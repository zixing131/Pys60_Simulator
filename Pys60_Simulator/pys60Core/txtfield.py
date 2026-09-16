# -*- coding: utf-8 -*-
"""Desktop adapter for the bundled txtfield extension's editable overlays."""
import appuifw
import graphics
from pys60_examples import to_text

ECorner1 = 1
ECorner2 = 2
EReadOnly = 1
EDisableCursor = 1
EDisplayOnly = 1


class New(object):
    def __init__(self, pos, cornertype=0, txtlimit=0, strlimit=0, editorflag=0):
        self.pos = tuple(pos)
        self.limit = txtlimit or strlimit
        self._value = u''
        self._selection = (0, 0)
        self._visible = False
        self._focused = False
        self._font = ('dense', 14)
        self._foreground = 0
        self._background = 0xffffff
        self.textbox = None
        self.textwindow = None
        self._canvas = None

    def _sync(self):
        if self.textbox is not None:
            # Tk has one sentinel newline; it is never application content.
            value = self.textbox.get('1.0', 'end-1c')
            self._value = value[:self.limit] if self.limit else value
            if self._value != value:
                self.textbox.delete('1.0', 'end')
                self.textbox.insert('1.0', self._value)

    def _create(self):
        canvas = getattr(appuifw.app.body, '_widget', None)
        if canvas is None:
            return
        if self.textbox is None or self._canvas is not canvas:
            self._sync()
            if self.textbox is not None:
                self.textbox.destroy()
            self._canvas = canvas
            self.textbox = appuifw.tk.Text(canvas, borderwidth=0, highlightthickness=0,
                                         padx=1, pady=0, wrap='char', undo=True)
            self.textbox.insert('1.0', self._value)
            # Typing digits must not also activate the underlying game keys.
            self.textbox.bindtags((str(self.textbox), 'Text', 'all'))
            self.textbox.bind('<Return>', self._finish)
            self.textbox.bind('<Escape>', self._finish)
            self.textbox.bind('<KeyRelease>', lambda event: self._sync())
            self._style()

    def _finish(self, event):
        self._sync()
        body = appuifw.app.body
        for kind in (appuifw.EEventKeyDown, appuifw.EEventKey, appuifw.EEventKeyUp):
            body._dispatch({'type': kind,
                            'keycode': appuifw.EKeySelect if kind == appuifw.EEventKey else 0,
                            'scancode': appuifw.EScancodeSelect, 'modifiers': 0})
        return 'break'

    def _style(self):
        if self.textbox is not None:
            self.textbox.configure(font=('Helvetica', -self._font[1]),
                                   foreground=graphics.convertColor(self._foreground),
                                   background=graphics.convertColor(self._background))

    def textstyle(self, name, size, color, style='normal'):
        # txtfield sizes are twips, unlike graphics' pixel sizes.
        self._font = (name or 'dense', max(1, int(round(size / 15.0))))
        self._foreground = color
        self._style()

    def bgcolor(self, color):
        self._background = color
        self._style()

    def add(self, content):
        self._sync()
        self._value += to_text(content)
        if self.limit:
            self._value = self._value[:self.limit]
        if self.textbox is not None:
            self.textbox.delete('1.0', 'end')
            self.textbox.insert('1.0', self._value)

    def select(self, start, end):
        self._selection = (start, end)
        if self.textbox is not None:
            self.textbox.tag_remove('sel', '1.0', 'end')
            self.textbox.tag_add('sel', '1.0+%dc' % start, '1.0+%dc' % end)

    def focus(self, data):
        self._focused = bool(data)
        if data:
            self._create()
            if self.textbox is not None:
                self.textbox.focus_set()
        else:
            self._sync()
            if self._canvas is not None:
                self._canvas.focus_set()

    def visible(self, data):
        self._visible = bool(data)
        if data:
            self._create()
            if self.textbox is not None:
                x, y, right, bottom = self.pos
                self.textbox.place(x=x, y=y, width=right-x, height=bottom-y)
                self.textbox.lift()
                self.select(*self._selection)
                if self._focused:
                    self.textbox.focus_set()
        else:
            self._sync()
            if self.textbox is not None:
                self.textbox.place_forget()

    def get(self, fullget=1):
        # Keep the old keyword but never expose Tk's sentinel newline or
        # discard the last character (the former fullget=0 workaround).
        self._sync()
        return self._value
