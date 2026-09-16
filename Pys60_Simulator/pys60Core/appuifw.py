# -*- coding: utf-8 -*-
"""PyS60 controls backed by Tk, with an explicit headless mode for tests.

Importing the module does not create a window. Set PYS60_HEADLESS=1 before
assigning app.body to use controls without Tk. Headless dialogs cancel unless
an application/test supplies _dialog_handler(kind, **options).
"""
import os
import sys
import time
import numbers
import graphics
import e32
import pys60Socket
from key_codes import *
import key_codes

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)

screen = (240, 320)
FFormEditModeOnly, FFormViewModeOnly = 1, 2
FFormAutoLabelEdit, FFormAutoFormEdit, FFormDoubleSpaced = 4, 8, 16
STYLE_BOLD, STYLE_UNDERLINE, STYLE_ITALIC, STYLE_STRIKETHROUGH = 1, 2, 4, 8
HIGHLIGHT_ROUNDED, HIGHLIGHT_SHADOW, HIGHLIGHT_STANDARD = 16, 32, 64
EEventKey, EEventKeyDown, EEventKeyUp = 1, 2, 3
EEventRedraw = 5  # legacy simulator extension
(EScreen, EApplicationWindow, EStatusPane, EMainPane, EControlPane,
 ESignalPane, EContextPane, ETitlePane, EBatteryPane, EUniversalIndicatorPane,
 ENaviPane, EFindPane, EWallpaperPane, EIndicatorPane, EAColumn, EBColumn,
 ECColumn, EDColumn) = range(18)
EStatusPaneBottom, EControlPaneBottom, EStaconTop, EStaconBottom = 18, 19, 20, 21
EControlPaneTop, EStatusPaneTop = EControlPane, EStatusPane
# TGulAlignmentValue is a horizontal/vertical bit field, not a sequence.
EHLeftVTop, EHLeftVCenter, EHLeftVBottom = 0x00, 0x10, 0x20
EHCenterVTop, EHCenterVCenter, EHCenterVBottom = 0x01, 0x11, 0x21
EHRightVTop, EHRightVCenter, EHRightVBottom = 0x02, 0x12, 0x22
root = None
cv = None
tk = None
_dialog_handler = None


def _callable(value):
    if value is not None and not callable(value):
        raise TypeError('callable or None expected')
    return value


def _text(value):
    if not isinstance(value, string_types):
        raise TypeError('Unicode string expected')
    return value


def _ensure_root():
    global root, tk
    if os.environ.get('PYS60_HEADLESS') == '1':
        return None
    if root is None:
        if not e32.is_ui_thread():
            raise RuntimeError('UI must be used from the UI thread')
        try:
            import tkinter as tk_module
        except ImportError:
            import Tkinter as tk_module
        tk = tk_module
        root = tk.Tk()
        root.title(app.title)
        root.geometry('%dx%d' % screen)
        root.resizable(False, False)
        root.protocol('WM_DELETE_WINDOW', _exit_key)
        root.bind('<KeyPress>', _key_press)
        root.bind('<KeyRelease>', _key_release)
        root.bind('<F1>', lambda event: app._show_menu())
        root.bind('<F2>', lambda event: _exit_key())
        root.bind('<FocusIn>', lambda event: _focus_event(1))
        root.bind('<FocusOut>', lambda event: _focus_event(0))
        def tick():
            e32._pump()
            app._present()
            if root is not None:
                root.after(10, tick)
        root.after(10, tick)
        app._render_tabs()
    return root


def _focus_event(focused):
    if app.focus is not None:
        app.focus(focused)


def _exit_key():
    if app.exit_key_handler is not None:
        app.exit_key_handler()
    else:
        app.set_exit()


_KEYMAP = {
    'up': (EKeyUpArrow, EScancodeUpArrow), 'down': (EKeyDownArrow, EScancodeDownArrow),
    'left': (EKeyLeftArrow, EScancodeLeftArrow), 'right': (EKeyRightArrow, EScancodeRightArrow),
    'space': (EKeySelect, EScancodeSelect), 'return': (EKeySelect, EScancodeSelect),
    'backspace': (EKeyBackspace, EScancodeBackspace),
    'q': (EKeyLeftSoftkey, EScancodeLeftSoftkey), 'w': (EKeyRightSoftkey, EScancodeRightSoftkey)}


def _event(event, kind):
    name = event.keysym.lower()
    if name in _KEYMAP:
        code, scan = _KEYMAP[name]
    elif len(name) == 1:
        code, scan = ord(name), ord(name.upper())
    else:
        return None
    # Tk state bits are not Symbian modifier flags; do not leak them.
    return {'type': kind, 'keycode': code if kind == EEventKey else 0,
            'scancode': scan, 'modifiers': 0}


def _key_press(event):
    e32.reset_inactivity()
    capture = sys.modules.get('keycapture')
    key_event = _event(event, EEventKey)
    if capture is not None and key_event is not None and capture._dispatch(key_event['keycode']):
        return 'break'
    body = app.body
    if body is not None:
        for kind in (EEventKeyDown, EEventKey):
            data = _event(event, kind)
            if data is not None:
                body._dispatch(data)
    if event.keysym.lower() == 'q' and not isinstance(body, Text):
        app._show_menu()
        return 'break'
    if event.keysym.lower() == 'w' and not isinstance(body, Text):
        _exit_key()
        return 'break'


def _key_release(event):
    if app.body is not None:
        data = _event(event, EEventKeyUp)
        if data is not None:
            app.body._dispatch(data)


class _Control(object):
    def _init_control(self):
        self._bindings = {}
        self._widget = None
        self._surface = None

    def bind(self, event_code, callback):
        _callable(callback)
        if callback is None:
            self._bindings.pop(event_code, None)
        else:
            self._bindings[event_code] = callback

    def _dispatch(self, event):
        if event['type'] == EEventKey:
            callback = self._bindings.get(event['keycode'])
            if callback is not None:
                callback()

    @property
    def size(self):
        return app.layout(EMainPane)[0]

    @property
    def position(self):
        return app.layout(EMainPane)[1]

    def _detach(self):
        if self._surface is not None:
            self._surface.place_forget()
        if self._widget is not None:
            self._widget.place_forget()

    def _bind_before_widget(self):
        # Captures must run before Tk's default Text/Listbox key handling.
        tags = self._widget.bindtags()
        self._widget.bindtags((str(root),)+tuple(tag for tag in tags if tag != str(root)))


class Canvas(graphics.Image, _Control):
    def __init__(self, redraw_callback=None, event_callback=None, resize_callback=None):
        self.redraw_callback = _callable(redraw_callback)
        self.event_callback = _callable(event_callback)
        self.resize_callback = _callable(resize_callback)
        self._init_control()
        graphics.Image.__init__(self, app.layout(EMainPane)[0])
        self.lastimg = None
        self._image_item = None
        self._touch = {}

    def _attach(self):
        global cv
        if _ensure_root() is None:
            # Like a window expose event, drawing starts when the application
            # next yields, after its constructor has initialized the buffers.
            e32._schedule(0, lambda: self.redraw() if app.body is self else None)
            return
        if self._widget is None:
            self._widget = tk.Canvas(root, width=self.size[0], height=self.size[1], highlightthickness=0)
            self._widget.bind('<Button-1>', self.mouseLeftButtonEvent)
            self._widget.bind('<ButtonRelease-1>', self.mouseLeftButtonReleaseEvent)
            self._widget.bind('<Expose>', lambda event: self.redraw())
            self._bind_before_widget()
        cv = self._widget
        self.cv, self.root = cv, root
        self._widget.place(x=app.layout(EMainPane)[1][0], y=app.layout(EMainPane)[1][1], width=app.layout(EMainPane)[0][0], height=app.layout(EMainPane)[0][1])
        self._widget.focus_set()
        self.blitSelf()
        e32._schedule(0, lambda: self.redraw() if app.body is self else None)

    def _resize(self, size):
        if self.size != size:
            old = self.image
            self.image = graphics.PILImage.new(old.mode, size, 'white')
            self.image.paste(old, (0, 0))
            if self._widget is not None:
                self._widget.configure(width=size[0], height=size[1])
            self.blitSelf()
            if self.resize_callback is not None:
                self.resize_callback(size)
            self.redraw()

    def bind(self, event_code, callback, point=None):
        if 0x101 <= event_code <= 0x10a:
            _callable(callback)
            if callback is None:
                self._touch.pop(event_code, None)
            else:
                self._touch[event_code] = (callback, point)
        else:
            _Control.bind(self, event_code, callback)

    def _dispatch(self, event):
        if self.event_callback is not None:
            self.event_callback(event)
        _Control._dispatch(self, event)

    def _pointer(self, event, kind):
        binding = self._touch.get(kind)
        if binding is not None:
            callback, area = binding
            if area is None or (area[0][0] <= event.x <= area[1][0] and area[0][1] <= event.y <= area[1][1]):
                callback((event.x, event.y))

    def mouseLeftButtonEvent(self, event):
        self._pointer(event, key_codes.EButton1Down)

    def mouseLeftButtonReleaseEvent(self, event):
        self._pointer(event, key_codes.EButton1Up)

    def processKeyPressEvent(self, event):
        for kind in (EEventKeyDown, EEventKey):
            data = _event(event, kind)
            if data is not None:
                self._dispatch(data)

    def processKeyUpEvent(self, event):
        data = _event(event, EEventKeyUp)
        if data is not None:
            self._dispatch(data)

    def blitSelf(self):
        self._normalize()
        if self._widget is not None:
            from PIL import ImageTk
            self.lastimg = ImageTk.PhotoImage(self.image, master=self._widget)
            if self._image_item is None:
                self._image_item = self._widget.create_image(0, 0, anchor='nw', image=self.lastimg)
            else:
                self._widget.itemconfigure(self._image_item, image=self.lastimg)

    def redraw(self, rect=None):
        if self.redraw_callback is not None:
            self.redraw_callback((0, 0) + self.size if rect is None else rect)

    update = redraw

    def begin_redraw(self):
        return None

    def end_redraw(self):
        self.blitSelf()


class Text(_Control):
    def __init__(self, text=u''):
        self._init_control()
        self._value = _text(text)
        self._pos = len(text)
        self._styles = []
        self.color = 0
        self.highlight_color = 0xffffff
        self.font = 'normal'
        self.style = 0
        self.focus = True

    def _attach(self):
        if _ensure_root() is None:
            return
        if self._widget is None:
            self._widget = tk.Text(root, wrap='word', undo=True)
            self._widget.insert('1.0', self._value)
            self._bind_before_widget()
        self._widget.place(x=app.layout(EMainPane)[1][0], y=app.layout(EMainPane)[1][1], width=app.layout(EMainPane)[0][0], height=app.layout(EMainPane)[0][1])
        self.set_pos(self._pos)
        if self.focus:
            self._widget.focus_set()

    def _sync(self):
        if self._widget is not None:
            value = self._widget.get('1.0', 'end-1c')
            if value != self._value:
                import difflib
                previous = self._styles
                previous += [(self.font, self.color, self.style, self.highlight_color)] * (len(self._value) - len(previous))
                styles = []
                for tag, a, b, c, d in difflib.SequenceMatcher(a=self._value, b=value, autojunk=False).get_opcodes():
                    styles.extend(previous[a:b] if tag == 'equal' else [(self.font, self.color, self.style, self.highlight_color)] * (d-c))
                self._styles = styles
            self._value = value
            self._pos = len(self._widget.get('1.0', 'insert'))

    def _range(self, pos, length):
        self._sync()
        if not isinstance(pos, numbers.Integral) or not isinstance(length, numbers.Integral):
            raise TypeError('integer expected')
        if length == -1 or pos+length > len(self._value):
            length = len(self._value)-pos
        if pos < 0 or pos > len(self._value) or length < 0 or pos+length > len(self._value):
            raise e32.SymbianError(-6, 'invalid text range')
        return pos, pos+length

    def clear(self):
        self._value, self._pos = u'', 0
        self._styles = []
        if self._widget is not None:
            self._widget.delete('1.0', 'end')

    def get(self, pos=0, length=-1):
        start, end = self._range(pos, length)
        return self._value[start:end]

    def set(self, text):
        _text(text)
        self.clear()
        self.add(text)

    def add(self, text):
        _text(text)
        self._sync()
        pos = self._pos
        self._styles += [(self.font, self.color, self.style, self.highlight_color)] * (len(self._value)-len(self._styles))
        self._styles[pos:pos] = [(self.font, self.color, self.style, self.highlight_color)] * len(text)
        self._value = self._value[:pos]+text+self._value[pos:]
        self._pos += len(text)
        if self._widget is not None:
            tag = 'style_%d' % len(self._widget.tag_names())
            spec = self.font if isinstance(self.font, (tuple, list)) else (self.font, 18)
            size = spec[1] or 18
            styles = []
            for flag, name in ((STYLE_BOLD, 'bold'), (STYLE_ITALIC, 'italic'),
                               (STYLE_UNDERLINE, 'underline'), (STYLE_STRIKETHROUGH, 'overstrike')):
                if self.style & flag:
                    styles.append(name)
            options = {'foreground': graphics.convertColor(self.color),
                       'font': ('Helvetica', size, ' '.join(styles))}
            if self.style & (HIGHLIGHT_STANDARD | HIGHLIGHT_ROUNDED | HIGHLIGHT_SHADOW):
                options['background'] = graphics.convertColor(self.highlight_color)
            self._widget.tag_configure(tag, **options)
            self._widget.insert('1.0+%dc' % pos, text, (tag,))
            self._widget.mark_set('insert', '1.0+%dc' % self._pos)

    def delete(self, pos=0, length=-1):
        start, end = self._range(pos, length)
        del self._styles[start:end]
        self._value = self._value[:start]+self._value[end:]
        self._pos = max(0, min(len(self._value), self._pos-(end-start)))
        if self._widget is not None:
            self._widget.delete('1.0+%dc' % start, '1.0+%dc' % end)
            self._widget.mark_set('insert', '1.0+%dc' % self._pos)

    def len(self):
        self._sync()
        return len(self._value)

    __len__ = len

    def get_pos(self):
        self._sync()
        return self._pos

    def set_pos(self, cursor_pos):
        if not isinstance(cursor_pos, numbers.Integral):
            raise TypeError('integer expected')
        if cursor_pos < 0:
            raise e32.SymbianError(-6, 'negative cursor position')
        self._pos = min(cursor_pos, self.len())
        if self._widget is not None:
            self._widget.mark_set('insert', '1.0+%dc' % self._pos)


class Icon(object):
    def __init__(self, filename, bitmap, bitmapMask):
        self.filename = _text(filename)
        self.bitmap = int(bitmap)
        self.bitmapMask = int(bitmapMask)
        if not filename.lower().endswith(('.mbm', '.mif')):
            raise TypeError('expected valid icon file')
        if not 0 <= self.bitmap <= 32767 or not 0 <= self.bitmapMask <= 32767:
            raise TypeError('expected valid icon and icon mask indexes')


class Listbox(_Control):
    def __init__(self, list, callback=None):
        self._init_control()
        self._callback = _callable(callback)
        self._kind = None
        self.set_list(list)

    def set_list(self, list, current=0):
        if not isinstance(list, type([])):
            raise TypeError('list expected')
        if not list:
            raise ValueError('non-empty list expected')
        kinds = []
        for item in list:
            if isinstance(item, string_types):
                kind = 'single'
            elif isinstance(item, tuple) and len(item) in (2, 3):
                _text(item[0])
                if len(item) == 3:
                    _text(item[1])
                    if not isinstance(item[2], Icon):
                        raise TypeError('Icon expected')
                    kind = 'double_icon'
                elif isinstance(item[1], Icon):
                    kind = 'single_icon'
                else:
                    _text(item[1])
                    kind = 'double'
            else:
                raise TypeError('invalid list item')
            kinds.append(kind)
        if len(set(kinds)) != 1 or (self._kind is not None and self._kind != kinds[0]):
            raise ValueError('Listbox type mismatch')
        if not isinstance(current, numbers.Integral):
            raise TypeError('integer expected')
        self._kind, self._items = kinds[0], list[:]
        self._current = max(0, min(current, len(list)-1))
        self._refresh()

    def current(self):
        if self._widget is not None and self._widget.curselection():
            self._current = int(self._widget.curselection()[0])
        return self._current

    def _refresh(self):
        if self._widget is not None:
            self._widget.delete(0, 'end')
            for item in self._items:
                label = item if isinstance(item, string_types) else ' / '.join(v for v in item if isinstance(v, string_types))
                self._widget.insert('end', label)
            self._widget.selection_set(self._current)
            self._widget.activate(self._current)

    def _attach(self):
        if _ensure_root() is None:
            return
        if self._widget is None:
            self._widget = tk.Listbox(root, exportselection=False)
            self._widget.bind('<Double-Button-1>', lambda event: self._activate())
            self._bind_before_widget()
        self._refresh()
        self._widget.place(x=app.layout(EMainPane)[1][0], y=app.layout(EMainPane)[1][1], width=app.layout(EMainPane)[0][0], height=app.layout(EMainPane)[0][1])
        self._widget.focus_set()

    def _activate(self):
        self.current()
        if self._callback is not None:
            self._callback()

    def _dispatch(self, event):
        _Control._dispatch(self, event)
        if event['type'] == EEventKey and event['keycode'] == EKeySelect:
            self._activate()


class Form(list):
    def __init__(self, fields, flags=0):
        self.flags = int(flags)
        self.menu = []
        self.save_hook = None
        list.__init__(self, [self._field(field) for field in fields])

    @staticmethod
    def _field(field):
        if not isinstance(field, tuple) or len(field) not in (2, 3):
            raise TypeError('Form field must be a tuple of size 2 or 3')
        label, kind = field[:2]
        _text(label)
        if kind not in ('text', 'number', 'date', 'time', 'combo', 'float'):
            raise ValueError('Form field, unknown type')
        if len(field) == 2:
            if kind == 'combo':
                raise ValueError('Form combo field, no value')
            return field
        value = field[2]
        if kind == 'text':
            _text(value)
        elif kind == 'number':
            if not isinstance(value, numbers.Real):
                raise TypeError('number expected')
            value = int(value)
            if not 0 <= value <= 0x7fffffff:
                raise ValueError('number field must be between 0 and 2147483647')
        elif kind in ('date', 'time', 'float'):
            if not isinstance(value, float):
                raise TypeError('float expected')
        else:
            if not isinstance(value, tuple) or len(value) != 2 or not isinstance(value[0], list):
                raise TypeError('combo must be (list, index)')
            choices, index = value
            for choice in choices:
                _text(choice)
            if not isinstance(index, numbers.Integral) or not 0 <= index < len(choices):
                raise ValueError('invalid combo index')
        return label, kind, value

    def __setitem__(self, index, field):
        if isinstance(index, slice):
            list.__setitem__(self, index, [self._field(f) for f in field])
        else:
            list.__setitem__(self, index, self._field(field))

    def insert(self, index, field):
        list.insert(self, index, self._field(field))

    def append(self, field):
        self.insert(len(self), field)

    def extend(self, fields):
        values = [self._field(field) for field in fields]
        list.extend(self, values)

    def execute(self):
        if not self:
            raise ValueError('cannot execute an empty form')
        candidate = _dialog('form', fields=list(self), flags=self.flags, menu=self.menu)
        if candidate is not None and not self.flags & FFormViewModeOnly:
            if self.save_hook is None or self.save_hook(candidate):
                self[:] = candidate


class Application(object):
    def __init__(self):
        self._body = None
        self._screen = 'normal'
        self._orientation = 'automatic'
        self._title = u'Pys60 Simulator'
        self.menu = []
        self.focus = None
        self.exit_key_handler = None
        self.running = True
        self._tabs = []
        self._tab_callback = None
        self._active_tab = 0
        self._tabbar = None
        self._pumping = False
        self._overlays = []

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if value is not None and not isinstance(value, _Control):
            raise TypeError('body must be a Canvas, Text, Listbox or None')
        if self._body is not None:
            self._body._detach()
        self._body = value
        if value is not None:
            if isinstance(value, Canvas):
                value._resize(self.layout(EMainPane)[0])
            value._attach()
        self._present()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = _text(value)
        if root is not None:
            root.title(value)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        if value not in ('normal', 'large', 'full'):
            raise ValueError('invalid screen mode')
        self._screen = value
        self._layout_changed()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if value not in ('automatic', 'portrait', 'landscape'):
            raise ValueError('invalid orientation')
        self._orientation = value
        global screen
        screen = (320, 240) if value == 'landscape' else (240, 320)
        graphics.screen = screen
        if root is not None:
            root.geometry('%dx%d' % screen)
        self._layout_changed()

    def _layout_changed(self):
        if isinstance(self.body, Canvas):
            self.body._resize(self.layout(EMainPane)[0])
        self._present()

    def layout(self, layout_id):
        width, height = screen
        status = 44 if self.screen == 'normal' else 0
        control = 20 if self.screen != 'full' else 0
        if layout_id in (EScreen, EApplicationWindow, EWallpaperPane):
            return (width, height), (0, 0)
        if layout_id == EMainPane:
            return (width, height-status-control), (0, status)
        if layout_id in (EControlPane, EControlPaneBottom):
            return (width, control), (0, height-control)
        if layout_id in (EStatusPane, EStatusPaneTop, ETitlePane, ENaviPane):
            return (width, status), (0, 0)
        raise ValueError('unknown or unavailable layout')

    def full_name(self):
        return os.path.abspath(sys.argv[0])

    def uid(self):
        return u'2000b1a0'  # stable simulator application UID

    def set_exit(self):
        global root, cv
        self.running = False
        if root is not None:
            root.destroy()
            root, cv = None, None
            self._chrome_widget = None
            self._chrome_key = None

    def set_tabs(self, tab_texts, callback=None):
        _callable(callback)
        for label in tab_texts:
            _text(label)
        self._tabs, self._tab_callback = list(tab_texts), callback
        self._active_tab = 0
        self._render_tabs()

    def activate_tab(self, index):
        if not isinstance(index, numbers.Integral):
            raise TypeError('integer expected')
        if not 0 <= index < len(self._tabs):
            raise ValueError('invalid tab index')
        self._active_tab = index
        self._render_tabs()

    def _select_tab(self, index):
        if index != self._active_tab:
            self.activate_tab(index)
            if self._tab_callback is not None:
                self._tab_callback(index)

    def _render_tabs(self):
        if root is None:
            return
        if self._tabbar is not None:
            self._tabbar.destroy()
        # Keep commands addressable; the same software renderer draws tab pixels.
        self._tabbar = tk.Frame(root)
        for index, label in enumerate(self._tabs):
            tk.Button(self._tabbar, text=label,
                      command=lambda i=index: self._select_tab(i)).pack()
        self._present()

    def _present(self):
        if root is not None:
            import _ui_render
            _ui_render.present(self)

    def _show_menu(self):
        menu = self.menu
        while menu:
            selected = popup_menu([item[0] for item in menu])
            if selected is None:
                return
            action = menu[selected][1]
            if callable(action):
                action()
                return
            menu = action

    def _pump_ui(self):
        if root is not None:
            previous = self._pumping
            self._pumping = True
            try:
                if not previous:
                    self._present()
                # A key callback can enter a game loop or Ao_lock.wait().
                # Those nested schedulers must still receive Tk key events.
                root.update()
            finally:
                self._pumping = previous

    def Yield(self):
        e32.ao_yield()

    def redraw(self, rect=None):
        if isinstance(self.body, Canvas):
            self.body.redraw(rect)

    def getscreen(self):
        import _ui_render
        return _ui_render.snapshot(self)


app = Application()
graphics.app = app


def abort():
    app.set_exit()


def available_fonts():
    return [u'dense', u'normal', u'large', u'title', u'legend', u'annotation']


def _dialog(kind, **options):
    if _dialog_handler is not None:
        return _dialog_handler(kind, **options)
    if _ensure_root() is None:
        return None
    try:
        from tkinter import simpledialog, messagebox
    except ImportError:
        import tkSimpleDialog as simpledialog
        import tkMessageBox as messagebox
    if kind == 'note':
        fn = messagebox.showerror if options['type'] == 'error' else messagebox.showinfo
        fn(app.title, options['text'], parent=root)
        return None
    if kind == 'query':
        label, mode, value = options['label'], options['type'], options['initial']
        if mode == 'query':
            return True if messagebox.askyesno(app.title, label, parent=root) else None
        fn = {'number': simpledialog.askinteger, 'float': simpledialog.askfloat,
              'date': simpledialog.askfloat, 'time': simpledialog.askfloat}.get(mode, simpledialog.askstring)
        kwargs = {'parent': root, 'initialvalue': value}
        if mode == 'code':
            kwargs['show'] = '*'
        return fn(app.title, label, **kwargs)
    if kind == 'multi_query':
        first = query(options['labels'][0], 'text')
        if first is None:
            return None
        second = query(options['labels'][1], 'text')
        return None if second is None else (first, second)
    if kind == 'form':
        if options['flags'] & FFormViewModeOnly:
            note(u'\n'.join(u'%s: %s' % (f[0], f[2] if len(f) > 2 else '') for f in options['fields']))
            return None
        fields = []
        for field in options['fields']:
            label, mode = field[:2]
            value = field[2] if len(field) > 2 else (u'' if mode == 'text' else 0)
            if mode == 'combo':
                index = popup_menu(value[0], label)
                result = None if index is None else (value[0], index)
            else:
                result = query(label, mode, value)
            if result is None:
                return None
            fields.append((label, mode, result))
        return fields
    # Selection dialogs retain original indices when a search filter is used.
    window = tk.Toplevel(root)
    window.title(options.get('label', app.title))
    multiple = kind == 'multi_selection'
    box = tk.Listbox(window, selectmode='multiple' if multiple else 'browse', exportselection=False)
    choices = options['choices']
    visible = list(range(len(choices)))
    chosen = set()
    def label(item):
        return item if isinstance(item, string_types) else u' / '.join(item)
    def fill(indices):
        box.delete(0, 'end')
        for index in indices:
            box.insert('end', label(choices[index]))
            if index in chosen:
                box.selection_set('end')
    fill(visible)
    if options.get('search_field'):
        search = tk.StringVar()
        entry = tk.Entry(window, textvariable=search)
        entry.pack(fill='x')
        def filter_items(*args):
            if multiple:
                chosen.difference_update(visible)
                chosen.update(visible[int(i)] for i in box.curselection())
            visible[:] = [i for i, item in enumerate(choices) if search.get().lower() in label(item).lower()]
            fill(visible)
        search.trace('w', filter_items)
    box.pack(fill='both', expand=True)
    result = [None]
    def accept(event=None):
        indices = [visible[int(i)] for i in box.curselection()]
        if multiple:
            chosen.difference_update(visible)
            chosen.update(indices)
            result[0] = tuple(sorted(chosen))
        elif indices:
            result[0] = indices[0]
        window.destroy()
    tk.Button(window, text='OK', command=accept).pack(side='left')
    tk.Button(window, text='Cancel', command=window.destroy).pack(side='right')
    box.bind('<Return>', accept)
    if not multiple:
        box.bind('<Double-Button-1>', accept)
    window.transient(root)
    window.grab_set()
    root.wait_window(window)
    return result[0]


def query(label, type, initial_value=None):
    _text(label)
    if type not in ('text', 'code', 'number', 'date', 'time', 'query', 'float'):
        raise ValueError('unknown query type')
    result = _dialog('query', label=label, type=type, initial=initial_value)
    if result is None or (type == 'query' and not result):
        return None
    if type == 'query':
        return True
    if type in ('text', 'code'):
        return _text(result)
    return int(result) if type == 'number' else float(result)


def multi_query(label_1, label_2):
    return _dialog('multi_query', labels=(_text(label_1), _text(label_2)))


def note(text, type='info', global_note=0):
    _text(text)
    if type not in ('error', 'info', 'conf'):
        raise ValueError('unknown note type')
    _dialog('note', text=text, type=type, global_note=global_note)


def _choices(choices):
    if not isinstance(choices, list):
        raise TypeError('list expected')
    if not choices:
        raise ValueError('non-empty list expected')
    for item in choices:
        if isinstance(item, tuple) and len(item) == 2:
            for value in item:
                _text(value)
        else:
            _text(item)


def popup_menu(list, label=u''):
    _choices(list)
    return _dialog('selection', choices=list, label=_text(label))


def selection_list(choices, search_field=0):
    _choices(choices)
    if search_field not in (0, 1):
        raise ValueError('search_field must be 0 or 1')
    return _dialog('selection', choices=choices, search_field=search_field)


def multi_selection_list(choices, style='checkbox', search_field=0):
    _choices(choices)
    if style not in ('checkbox', 'checkmark'):
        raise ValueError('unknown selection style')
    if search_field not in (0, 1):
        raise ValueError('search_field must be 0 or 1')
    result = _dialog('multi_selection', choices=choices, style=style, search_field=search_field)
    return () if result is None else tuple(result)


class InfoPopup(object):
    def __init__(self):
        self._window = None
        self._show_timer = e32.Ao_timer()
        self._hide_timer = e32.Ao_timer()
        self._visible = False

    def show(self, text, position=(0, 0), time_shown=5000, time_before=0, alignment=EHLeftVTop):
        _text(text)
        if alignment not in (0, 1, 2, 16, 17, 18, 32, 33, 34):
            raise ValueError('invalid alignment')
        if time_shown < 0 or time_before < 0:
            raise ValueError('negative time is not allowed')
        self.hide()
        def display():
            self._visible = True
            if _ensure_root() is not None:
                self._window = tk.Toplevel(root)
                self._window.overrideredirect(True)
                tk.Label(self._window, text=text, background='#ffffcc').pack()
                self._window.update_idletasks()
                horizontal, vertical = alignment & 3, (alignment & 0x30) >> 4
                x = root.winfo_rootx()+position[0]-horizontal*self._window.winfo_reqwidth()//2
                y = root.winfo_rooty()+position[1]-vertical*self._window.winfo_reqheight()//2
                self._window.geometry('+%d+%d' % (x, y))
            self._hide_timer.after(time_shown / 1000.0, self.hide)
        self._show_timer.after(time_before / 1000.0, display)

    def hide(self):
        self._show_timer.cancel()
        self._hide_timer.cancel()
        self._visible = False
        if self._window is not None:
            self._window.destroy()
            self._window = None


class Content_handler(object):
    def __init__(self, callback=None):
        self.callback = _callable(callback)

    def open(self, filename):
        # There is no portable way to observe when a host document viewer closes.
        raise e32.SymbianError(-5, 'Embedded Symbian document handlers are not supported')

    def open_standalone(self, filename):
        import subprocess
        if not os.path.isfile(filename):
            raise e32.SymbianError(-1, 'file not found')
        if sys.platform == 'darwin':
            subprocess.Popen(['open', filename])
        elif os.name == 'nt':
            os.startfile(filename)
        else:
            subprocess.Popen(['xdg-open', filename])


Listbox2 = Listbox  # existing simulator alias

class Text_display(object):
    def __init__(self, text, skinned=False):
        self.text, self.skinned = text, skinned

class text(object):
    measure_text = staticmethod(graphics.getTextFontWidth)
