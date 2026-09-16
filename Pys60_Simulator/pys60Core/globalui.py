# -*- coding: utf-8 -*-
"""Desktop equivalents of the global UI notifiers."""
import numbers
import appuifw


def global_note(note_text, type='info'):
    types = ('info', 'error', 'text', 'warn', 'charging', 'wait', 'perm',
             'not_charging', 'battery_full', 'battery_low', 'recharge_battery', 'confirm')
    if type not in types:
        raise ValueError('unknown note type')
    appuifw.note(note_text, 'error' if type == 'error' else 'conf' if type == 'confirm' else 'info', 1)


def _query(query_text, header_text, timeout, options=None):
    appuifw._text(query_text)
    appuifw._text(header_text)
    if not isinstance(timeout, numbers.Integral):
        raise TypeError('timeout must be an integer')
    if timeout < 0:
        raise ValueError('timeout must not be negative')
    if appuifw._dialog_handler is not None:
        return appuifw._dialog_handler('global_query', text=query_text, header=header_text,
                                       timeout=timeout, choices=options)
    root = appuifw._ensure_root()
    if root is None:
        return None
    tk = appuifw.tk
    window = tk.Toplevel(root)
    window.title(header_text)
    result = [None]
    def done(value):
        result[0] = value
        window.destroy()
    if options is None:
        tk.Label(window, text=query_text).pack()
        tk.Button(window, text='Yes / OK', command=lambda: done(1)).pack(side='left')
        tk.Button(window, text='No / Cancel', command=lambda: done(0)).pack(side='right')
        window.protocol('WM_DELETE_WINDOW', lambda: done(0))
    else:
        box = tk.Listbox(window, exportselection=False)
        for option in options:
            box.insert('end', option)
        box.pack()
        tk.Button(window, text='OK', command=lambda: done(int(box.curselection()[0]) if box.curselection() else None)).pack()
    timer = window.after(timeout*1000, lambda: done(None)) if timeout else None
    window.transient(root)
    window.grab_set()
    root.wait_window(window)
    return result[0]


def global_query(query_text, timeout=0):
    return _query(query_text, u'', timeout)


def global_msg_query(query_text, header_text, timeout=0):
    return _query(query_text, header_text, timeout)


def global_popup_menu(option_items, header_text=u'', timeout=0):
    appuifw._choices(option_items)
    return _query(u'', header_text, timeout, option_items)
