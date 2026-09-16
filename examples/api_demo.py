# -*- coding: utf-8 -*-
"""Small Python 2/3 example exercising the source-aligned desktop API."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'Pys60_Simulator', 'pys60Core'))
import appuifw
import graphics
import e32

lock = e32.Ao_lock()
appuifw.app.title = u'PyS60 1.4.5 API demo'
appuifw.app.screen = 'full'
canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = lock.signal

image = graphics.Image.new((100, 70))
image.clear(0x2776bb)
image.rectangle((10, 10, 90, 60), outline=0xffffff, width=3)
image.text((18, 43), u'PyS60', fill=0xffffff, font=('normal', 19))


def draw(rect=None):
    canvas.clear(0xf2f4f8)
    canvas.blit(image, target=(15, 20))
    canvas.blit(image.transpose(graphics.ROTATE_90), target=(145, 20))
    canvas.text((15, 155), u'Resize returns a new image', font=('normal', 15))
    canvas.blit(image.resize((180, 80)), target=(20, 180))
    canvas.text((15, 290), u'Q / F1: menu   W / F2: exit', font=('normal', 13))


def show_text():
    editor = appuifw.Text(u'Text.set / add / get\n')
    editor.style = appuifw.STYLE_BOLD
    editor.add(u'Editable text, no blocking loop.')
    appuifw.app.body = editor


def show_canvas():
    appuifw.app.body = canvas
    draw()


canvas.redraw_callback = draw
appuifw.app.menu = [(u'Canvas', show_canvas), (u'Text', show_text), (u'Exit', lock.signal)]
draw()
lock.wait()
appuifw.app.set_exit()
