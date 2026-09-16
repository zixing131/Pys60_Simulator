# -*- coding: utf-8 -*-
"""Run explicitly on a desktop: python tests/gui_smoke.py."""
import os
os.environ.pop('PYS60_HEADLESS', None)
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pys60_Simulator', 'pys60Core')))
import appuifw as ui
import graphics
import e32

def pixel(widget, photo, x, y):
    return tuple(map(int, widget.tk.splitlist(widget.tk.call(str(photo), 'get', x, y))))

ui.app.screen = 'full'
redraws = []
canvas = ui.Canvas(redraws.append)
ui.app.body = canvas
e32.ao_yield()
canvas.clear(0xff0000)
e32.ao_yield()
assert canvas._widget.find_all() == (canvas._image_item,)
# Inspect the actual Tk photo, not just the Pillow backing buffer.
assert pixel(canvas._widget, canvas.lastimg, 1, 1) == (255, 0, 0)
for i in range(20):
    canvas.clear(i)
assert len(canvas._widget.find_all()) == 1
assert redraws and len(redraws[0]) == 4
ui.app.orientation = 'landscape'
e32.ao_yield()
assert int(canvas._widget.cget('width')) == 320
calls = []
ui.app.set_tabs([u'One', u'Two'], calls.append)
ui.app._tabbar.winfo_children()[1].invoke()
assert calls == [1]
ui.app.activate_tab(0)
assert calls == [1]
text = ui.Text(u'initial')
ui.app.body = text
text.set_pos(2)
text.add(u'中文')
assert text.get() == u'in中文itial'
text.set(u'replaced')
assert text._widget.get('1.0', 'end-1c') == 'replaced'
box = ui.Listbox([u'one', u'two'])
ui.app.body = box
box.set_list([u'first', u'second'], 1)
assert box.current() == 1
from topwindow import TopWindow
window = TopWindow()
window.size = (40, 30)
window.add_image(graphics.Image.new((20, 20)), (0, 0))
window.show()
e32.ao_yield()
assert window._window.winfo_exists()
window.hide()
# Check the software controls and chrome against the exact Tk photos shown.
window.hide()
ui.app.screen = 'normal'
ui.app.orientation = 'portrait'
ui.app.title = 'Pixel parity'
ui.app.body = text
text.set('Line one\nLine two')
text.set_pos(8)
e32.ao_yield()
assert text._widget.winfo_y() == 44
snapshot = graphics.screenshot().image
for x, y in ((5, 5), (15, 18), (30, 25), (8, 40)):
    displayed = pixel(text._surface, text._surface_photo, x, y)
    assert displayed == snapshot.getpixel((x, y + 44)), (x, y, displayed)
assert pixel(ui.app._chrome_widget, ui.app._chrome_photo, 1, 1) == snapshot.getpixel((1, 1))
ui.app.body = box
e32.ao_yield()
snapshot = graphics.screenshot().image
assert pixel(box._surface, box._surface_photo, 1, 30) == snapshot.getpixel((1, 74))
import glcanvas, gles
frames = []
def draw_gl(frame):
    frames.append(frame)
    gles.glClearColor(0, 1, 0, 1)
    gles.glClear(gles.GL_COLOR_BUFFER_BIT)
gl = glcanvas.GLCanvas(draw_gl)
ui.app.body = gl
e32.ao_yield()
assert frames
assert pixel(gl._widget, gl.lastimg, 1, 1) == (0, 255, 0)
assert graphics.screenshot().getpixel((1, 45)) == [(0, 255, 0)]
# The F2 handler in a Tk callback must be able to wait for another Tk event.
# Otherwise legacy games freeze when entering a nested loop or exit query.
import threading
nested = e32.Ao_lock()
order = []
old_exit = ui.app.exit_key_handler
def nested_exit():
    if not order:
        order.append('enter')
        root = ui.root
        root.after(20, ui._exit_key)
        nested.wait()
        order.append('return')
    else:
        order.append('signal')
        nested.signal()
ui.app.exit_key_handler = nested_exit
ui.root.after(0, ui._exit_key)
watchdog = threading.Timer(2, nested.signal)
watchdog.start()
try:
    e32.ao_yield()
    assert order == ['enter', 'signal', 'return'], order
finally:
    watchdog.cancel()
    ui.app.exit_key_handler = old_exit
gl._context.close()
ui.app.set_exit()
print('Tk GUI smoke: Canvas, chrome, Text, Listbox, OpenGL screenshot/display parity and TopWindow passed')
