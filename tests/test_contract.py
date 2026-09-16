# -*- coding: utf-8 -*-
"""Regression contracts derived from pys60-1.4.5_src (not simulator guesses)."""
import os
os.environ['PYS60_HEADLESS'] = '1'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import unittest
import tempfile
import shutil
import threading
import time
import wave
from contextlib import closing
import struct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pys60_Simulator', 'pys60Core')))
import graphics as g
import appuifw as ui
import e32
import e32db
import e32dbm
import sysinfo


class TemporaryFiles(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix='pys60-contract-')

    def tearDown(self):
        shutil.rmtree(self.directory)

    def path(self, name):
        return os.path.join(self.directory, name)


class GraphicsContract(TemporaryFiles):
    # ext/graphics/graphics.py and graphicsmodule.cpp:1135-1217
    def test_modes_and_readonly_attributes(self):
        image = g.Image.new((8, 6))
        self.assertEqual(image.mode, 'RGB16')
        self.assertEqual(image.size, (8, 6))
        with self.assertRaises(AttributeError):
            image.size = (4, 3)
        with self.assertRaises(ValueError):
            g.Image.new((2, 2), 'RGBA')
        for mode in ('1', 'L', 'RGB12', 'RGB16', 'RGB'):
            mask = g.Image.new((2, 2), mode)
            mask.clear(0)
            self.assertEqual(mask.getpixel((0, 0)), [(0, 0, 0)])
            mask.clear()
            self.assertEqual(mask.getpixel((0, 0)), [(255, 255, 255)])

    def test_resize_preserves_original(self):
        image = g.Image.new((12, 6))
        result = image.resize((6, 6), keepaspect=1)
        self.assertIsNot(result, image)
        self.assertEqual(image.size, (12, 6))
        self.assertEqual(result.size, (6, 3))

    def test_rotations_and_flips(self):
        image = g.Image.new((2, 3))
        image.point((0, 0), 0xff0000)
        rotated = image.transpose(g.ROTATE_90)
        self.assertEqual(rotated.size, (3, 2))
        self.assertEqual(rotated.getpixel((0, 1)), [(255, 0, 0)])
        flipped = image.transpose(g.FLIP_LEFT_RIGHT)
        self.assertEqual(flipped.getpixel((1, 0)), [(255, 0, 0)])
        with self.assertRaises(ValueError):
            image.transpose(270)

    def test_blit_source_target_and_positional_order(self):
        source = g.Image.new((8, 8))
        source.clear(0xff0000)
        source.rectangle((2, 3, 5, 6), fill=0x00ff00)
        target = g.Image.new((9, 9))
        target.clear(0)
        target.blit(source, ((2, 3), (5, 6)), (4, 1))
        self.assertEqual(target.getpixel(((4, 1), (6, 3), (3, 1), (7, 4))),
                         [(0, 255, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0)])

    def test_blit_scaled_source_crop(self):
        source = g.Image.new((8, 8))
        source.clear(0xff0000)
        source.rectangle((2, 2, 4, 4), fill=0x00ff00)
        target = g.Image.new((12, 10))
        target.blit(source, source=(2, 2, 4, 4), target=((2, 3), (10, 9)), scale=1)
        self.assertEqual(target.getpixel(((2, 3), (9, 8))), [(0, 255, 0)]*2)

    def test_blit_negative_source_does_not_paint_padding(self):
        source = g.Image.new((2, 2))
        source.clear(0xff0000)
        target = g.Image.new((4, 4))
        target.blit(source, source=(-1, -1, 2, 2))
        self.assertEqual(target.getpixel(((0, 0), (1, 1))), [(255, 255, 255), (255, 0, 0)])

    def test_grayscale_mask(self):
        source = g.Image.new((2, 1))
        source.clear(0xffffff)
        mask = g.Image.new((2, 1), 'L')
        mask.clear(0)
        mask.point((1, 0), 0x808080)
        target = g.Image.new((2, 1))
        target.clear(0)
        target.blit(source, mask=mask)
        self.assertEqual(target.getpixel(((0, 0), (1, 0))), [(0, 0, 0), (132, 130, 132)])
        with self.assertRaises(ValueError):
            target.blit(source, mask=mask, scale=1)
        with self.assertRaises(ValueError):
            target.blit(source, mask=source)

    def test_shape_coordinates_and_fill(self):
        image = g.Image.new((10, 10))
        image.rectangle(((1, 1), (3, 3), (5, 5), (7, 7)), fill=0)
        self.assertEqual(image.getpixel(((2, 2), (3, 3), (5, 5), (7, 7))),
                         [(0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255)])
        image.line(((0, 0), (9, 0), (9, 9)), outline=0xff0000)
        self.assertEqual(image.getpixel((9, 5)), [(255, 0, 0)])

    def test_arc_uses_radians_counterclockwise(self):
        import math
        image = g.Image.new((21, 21))
        image.arc((0, 0, 21, 21), 0, math.pi/2, outline=0)
        self.assertEqual(image.getpixel(((20, 10), (10, 0), (0, 10))),
                         [(0, 0, 0), (0, 0, 0), (255, 255, 255)])

    def test_polygon_fill_and_wide_outline_on_pillow6(self):
        image = g.Image.new((30, 30))
        image.polygon((5, 5, 24, 5, 24, 24, 5, 24),
                      outline=0, fill=0xff0000, width=3)
        self.assertEqual(image.getpixel(((15, 15), (5, 5), (15, 6), (0, 0))),
                         [(255, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255)])

    def test_text_baseline_and_small_cjk_strokes(self):
        # At baseline 35, every glyph must remain above the font descent.
        # Pillow 6 silently ignored anchor='ls', drawing below that baseline.
        text = u'密码gj'
        masks = {}
        for flags in (0, g.FONT_ANTIALIAS, g.FONT_BOLD):
            image = g.Image.new((100, 60), 'RGB')
            image.clear(0)
            font = ('dense', 15, flags)
            image.text((20, 35), text, 0xffffff, font)
            ink = image.image.getbbox()
            self.assertLess(ink[1], 30)
            self.assertLessEqual(ink[3], 40)
            self.assertGreater(ink[2] - ink[0], 30)
            self.assertGreater(sum(pixel != (0, 0, 0) for pixel in image.image.getdata()), 100)
            masks[flags] = set(i for i, pixel in enumerate(image.image.getdata()) if pixel != (0, 0, 0))
        self.assertTrue(masks[0].issubset(masks[g.FONT_BOLD]))
        self.assertEqual(image.measure_text(u'', font)[0], (0, 0, 0, 0))

    def test_measurement_returns_actual_width_and_limits(self):
        image = g.Image.new((30, 30))
        full = image.measure_text(u'hello', maxwidth=1000)
        self.assertLess(full[1], 1000)
        self.assertEqual(full[2], 5)
        short = image.measure_text(u'hello', maxadvance=full[1]-1)
        self.assertLess(short[2], 5)
        self.assertEqual(image.measure_text(u'', maxadvance=0)[2], 0)

    def test_save_inspect_load_and_nonmutation(self):
        image = g.Image.new((3, 2), 'L')
        image.clear(0x808080)
        image.save(self.path('x.png'), bpp=8)
        self.assertEqual(image.mode, 'L')
        self.assertEqual(g.Image.inspect(self.path('x.png')), {'size': (3, 2)})
        loaded = g.Image.open(self.path('x.png'))
        self.assertEqual(loaded.mode, 'RGB16')
        self.assertEqual(loaded.getpixel((0, 0)), [(132, 130, 132)])
        with self.assertRaises(RuntimeError):
            g.Image.new((1, 1)).load(self.path('x.png'))
        with self.assertRaises(ValueError):
            image.save(self.path('x.png'), bpp=16)

    def test_async_results_and_cancellation(self):
        image = g.Image.new((4, 4))
        results = []
        self.assertIsNone(image.resize((2, 2), results.append))
        self.assertEqual(results, [])
        e32.ao_yield()
        self.assertEqual(results[0].size, (2, 2))
        image.save(self.path('x.png'), results.append)
        e32.ao_yield()
        self.assertEqual(results[-1], 0)
        image.resize((1, 1), results.append)
        image.stop()
        e32.ao_yield()
        self.assertEqual(len(results), 2)

    def test_draw_shares_drawable(self):
        image = g.Image.new((2, 2))
        g.Draw(image).clear(0)
        self.assertEqual(image.getpixel((0, 0)), [(0, 0, 0)])


class ActiveObjectContract(TemporaryFiles):
    # core/Symbian/e32module.cpp:360-510,674-705,828-867,950-1090
    def test_file_copy_target_first(self):
        with open(self.path('source'), 'wb') as stream:
            stream.write(b'original')
        self.assertIsNone(e32.file_copy(self.path('target'), self.path('source')))
        with open(self.path('target'), 'rb') as stream:
            self.assertEqual(stream.read(), b'original')

    def test_signal_before_wait_is_consumed(self):
        lock = e32.Ao_lock()
        lock.signal()
        lock.wait()
        e32.ao_sleep(.01, lock.signal)
        lock.wait()

    def test_lock_thread_affinity(self):
        lock = e32.Ao_lock()
        errors = []
        def wrong_thread():
            try:
                lock.wait()
            except AssertionError as exc:
                errors.append(exc)
        thread = threading.Thread(target=wrong_thread)
        thread.start()
        thread.join(1)
        self.assertEqual(len(errors), 1)

    def test_timer_pending_cancel_and_synchronous_wait(self):
        calls = []
        timer = e32.Ao_timer()
        timer.after(.01, lambda: calls.append(1))
        with self.assertRaises(RuntimeError):
            timer.after(0, lambda: None)
        timer.cancel()
        e32.ao_sleep(.02)
        self.assertEqual(calls, [])
        timer.after(.001)
        with self.assertRaises(RuntimeError):
            timer.after(-1)
        with self.assertRaises(TypeError):
            timer.after(0, None)

    def test_sleep_callback_runs_on_owner_thread(self):
        calls = []
        owner = threading.current_thread().ident
        e32.ao_sleep(0, lambda: calls.append(threading.current_thread().ident))
        self.assertEqual(calls, [])
        e32.ao_yield()
        self.assertEqual(calls, [owner])

    def test_callgate_forwards_args_in_creator_thread(self):
        calls = []
        gate = e32.ao_callgate(lambda a, b=None: calls.append((a, b, threading.current_thread().ident)))
        thread = threading.Thread(target=lambda: gate(42, b='value'))
        thread.start()
        thread.join()
        self.assertEqual(calls, [])
        e32.ao_yield()
        self.assertEqual(calls, [(42, 'value', threading.current_thread().ident)])

    def test_nested_wait_keeps_scheduler_live(self):
        outer, inner = e32.Ao_lock(), e32.Ao_lock()
        calls = []
        def nested():
            e32.ao_sleep(0, inner.signal)
            inner.wait()
            calls.append(1)
            outer.signal()
        e32.ao_sleep(0, nested)
        outer.wait()
        self.assertEqual(calls, [1])

    def test_nested_wait_can_dispatch_already_ready_callback(self):
        inner = e32.Ao_lock()
        calls = []
        def nested():
            # Safety release makes a scheduler regression fail instead of hang.
            timer = e32.Ao_timer()
            timer.after(.1, lambda: (calls.append('fallback'), inner.signal()))
            inner.wait()
            timer.cancel()
            calls.append('returned')
        e32.ao_sleep(0, nested)
        e32.ao_sleep(0, lambda: (calls.append('ready'), inner.signal()))
        e32.ao_yield()
        self.assertEqual(calls, ['ready', 'returned'])

    def test_discarded_timer_cancels_pending_callback(self):
        import gc
        calls = []
        timer = e32.Ao_timer()
        timer.after(0, lambda: calls.append(1))
        del timer
        gc.collect()
        e32.ao_yield()
        self.assertEqual(calls, [])


class UIContract(unittest.TestCase):
    # appui/appuifw/appuifwmodule.cpp:1827-1910,3121-3245,3841-3845
    def setUp(self):
        ui.app.body = None
        ui.app.screen = 'normal'
        ui.app.orientation = 'portrait'
        ui._dialog_handler = None

    def tearDown(self):
        ui.app.body = None
        ui._dialog_handler = None

    def test_import_is_lazy_and_does_not_replace_os_abort(self):
        self.assertIsNone(ui.root)
        self.assertIsNot(os.abort, ui.abort)

    def test_text_cursor_and_editing(self):
        text = ui.Text(u'abc')
        text.set_pos(1)
        text.add(u'你好')
        self.assertEqual(text.get(), u'a你好bc')
        self.assertEqual(text.get_pos(), 3)
        self.assertEqual(text.get(1, 2), u'你好')
        self.assertEqual(text.get(1, 999), u'你好bc')
        text.delete(1, 2)
        self.assertEqual(text.get(), 'abc')
        text.set(u'new')
        self.assertEqual(text.get(), 'new')
        text.set_pos(999)
        self.assertEqual(text.get_pos(), 3)
        with self.assertRaises(e32.SymbianError):
            text.get(-1)
        text.clear()
        self.assertEqual(text.len(), 0)

    def test_listbox_selection_type_and_bind(self):
        box = ui.Listbox([u'a', u'b'])
        box.set_list([u'x', u'y'], current=999)
        self.assertEqual(box.current(), 1)
        with self.assertRaises(ValueError):
            box.set_list([])
        with self.assertRaises(ValueError):
            box.set_list([(u'a', u'b')])
        calls = []
        box.bind(ui.EKeySelect, lambda: calls.append(1))
        box._dispatch({'type': ui.EEventKey, 'keycode': ui.EKeySelect})
        box.bind(ui.EKeySelect, None)
        box._dispatch({'type': ui.EEventKey, 'keycode': ui.EKeySelect})
        self.assertEqual(calls, [1])

    def test_canvas_events_and_redraw_shape(self):
        events, draws, keys = [], [], []
        canvas = ui.Canvas(draws.append, events.append)
        canvas.bind(ui.EKeyUpArrow, lambda: keys.append(1))
        event = type('Event', (), {'keysym': 'Up'})()
        canvas.processKeyPressEvent(event)
        canvas.processKeyUpEvent(event)
        self.assertEqual([evt['type'] for evt in events], [2, 1, 3])
        self.assertTrue(all(set(evt) == set(('type', 'keycode', 'scancode', 'modifiers')) for evt in events))
        self.assertEqual(keys, [1])
        ui.app.body = canvas
        e32.ao_yield()
        self.assertEqual(draws[-1], (0, 0)+canvas.size)

    def test_canvas_resize_screenshot(self):
        sizes = []
        canvas = ui.Canvas(resize_callback=sizes.append)
        ui.app.body = canvas
        ui.app.screen = 'full'
        self.assertEqual(canvas.size, (240, 320))
        self.assertEqual(sizes[-1], canvas.size)
        canvas.clear(0xff0000)
        shot = g.screenshot()
        canvas.clear(0)
        self.assertEqual(shot.getpixel((1, 1)), [(255, 0, 0)])
        ui.app.orientation = 'landscape'
        self.assertEqual(canvas.size, (320, 240))
        self.assertEqual(sysinfo.display_pixels(), canvas.size)

    def test_form_sequence_and_save_hook(self):
        form = ui.Form([(u'name', 'text', u'old')])
        form.insert(1, (u'count', 'number', 1))
        self.assertEqual(form.pop(), (u'count', 'number', 1))
        ui._dialog_handler = lambda kind, **kwargs: [(u'name', 'text', u'new')]
        form.save_hook = lambda values: True
        form.execute()
        self.assertEqual(form[0][2], 'new')
        with self.assertRaises(ValueError):
            form.append((u'bad', 'number', -1))
        with self.assertRaises(ValueError):
            ui.Form([]).execute()
        self.assertEqual((ui.FFormEditModeOnly, ui.FFormDoubleSpaced), (1, 16))

    def test_dialog_accept_cancel_and_types(self):
        self.assertIsNone(ui.query(u'Name', 'text'))
        self.assertIsNone(ui.popup_menu([u'a']))
        self.assertEqual(ui.multi_selection_list([u'a']), ())
        ui._dialog_handler = lambda kind, **kwargs: '12'
        self.assertEqual(ui.query(u'Number', 'number'), 12)
        ui._dialog_handler = lambda kind, **kwargs: False
        self.assertIsNone(ui.query(u'Continue?', 'query'))
        with self.assertRaises(ValueError):
            ui.query(u'Invalid', 'info')
        with self.assertRaises(ValueError):
            ui.note(u'Invalid', 'invalid')

    def test_topwindow_images_and_alias(self):
        from topwindow import TopWindow
        import TopWindow as old
        self.assertIs(old.TopWindow, TopWindow)
        window = TopWindow()
        window.size = (5, 5)
        image = g.Image.new((2, 2))
        window.add_image(image, (1, 1))
        self.assertEqual(window.images, [(image, (1, 1, 3, 3))])
        window.show()
        self.assertEqual(window.visible, 1)
        window.remove_image(image)
        self.assertEqual(window.images, [])
        with self.assertRaises(ValueError):
            window.remove_image(image)
        window.hide()

    def test_original_emulator_sysinfo(self):
        self.assertEqual(sysinfo.imei(), '0'*15)
        self.assertEqual(sysinfo.battery(), 0)
        self.assertEqual(sysinfo.sw_version(), 'emulator')
        self.assertEqual(set(sysinfo.free_drivespace()), set(e32.drive_list()))

    def test_tabs_user_callback_and_sdk_constants(self):
        calls = []
        ui.app.set_tabs([u'first', u'second'], calls.append)
        ui.app.activate_tab(1)
        self.assertEqual(calls, [])
        ui.app._select_tab(0)
        self.assertEqual(calls, [0])
        self.assertEqual(ui.EHCenterVCenter, 0x11)
        self.assertEqual(ui.EControlPaneTop, ui.EControlPane)

    def test_keycapture_forwarding_and_stop(self):
        import keycapture
        calls, forwarded = [], []
        capture = keycapture.KeyCapturer(calls.append)
        capture.keys = [ui.EKeyUpArrow]
        capture.start()
        ui.app.body = ui.Canvas(event_callback=forwarded.append)
        event = type('Event', (), {'keysym': 'Up'})()
        self.assertEqual(ui._key_press(event), 'break')
        self.assertEqual(calls, [ui.EKeyUpArrow])
        self.assertEqual(capture.last_key(), ui.EKeyUpArrow)
        self.assertEqual(forwarded, [])
        capture.forwarding = 1
        ui._key_press(event)
        self.assertEqual(len(forwarded), 2)
        capture.stop()
        ui._key_press(event)
        self.assertEqual(len(calls), 2)

    def test_access_point_object_and_default_validation(self):
        import socket
        point = socket.access_point(1)
        self.assertIsNone(point.start())
        self.assertIsNone(socket.set_default_access_point(point))
        self.assertIsNone(point.stop())
        with self.assertRaises(ValueError):
            socket.set_default_access_point(1)
        with self.assertRaises(ValueError):
            socket.access_point(0)
        self.assertIsNone(socket.select_access_point())
        socket.set_default_access_point(None)

    def test_global_query_distinguishes_no_and_timeout(self):
        import globalui
        ui._dialog_handler = lambda kind, **kwargs: 0
        self.assertEqual(globalui.global_query(u'continue?'), 0)
        ui._dialog_handler = lambda kind, **kwargs: None
        self.assertIsNone(globalui.global_query(u'continue?', 1))
        with self.assertRaises(TypeError):
            globalui.global_query(u'continue?', 1.5)


class DatabaseContract(TemporaryFiles):
    # core/Lib/e32dbm.py; ext/e32db/e32dbmodule.cpp:390-605
    def test_dbm_persistence_keys_bytes_and_flags(self):
        filename = self.path('mapping')
        db = e32dbm.open(filename, 'n')
        db['abc'] = 'value'
        db[b'\x00\xff'] = b'\x00\xff'
        self.assertEqual(db.items(), [(b'abc', b'value'), (b'\x00\xff', b'\x00\xff')])
        db.close()
        db = e32dbm.open(filename, 'r')
        self.assertEqual(db['abc'], b'value')
        with self.assertRaises(IOError):
            db['bad'] = 'write'
        with self.assertRaises(IOError):
            db.clear()
        db.close()
        with self.assertRaises(RuntimeError):
            db.keys()
        with self.assertRaises(e32.SymbianError):
            e32dbm.open(self.path('missing'), 'w')

    def test_dbm_deferred_writes_and_deletions(self):
        filename = self.path('mapping')
        db = e32dbm.open(filename, 'nf')
        db['a'] = '1'
        other = e32dbm.open(filename, 'r')
        self.assertEqual(other.keys(), [])
        self.assertEqual(db['a'], b'1')
        db.sync()
        self.assertEqual(other['a'], b'1')
        del db['a']
        self.assertEqual(db.keys(), [])
        db.sync()
        self.assertEqual(other.keys(), [])
        other.close()
        db.close()

    def test_dbms_transactions_and_cursor(self):
        db = e32db.Dbms()
        filename = self.path('db')
        db.create(filename)
        db.open(filename)
        self.assertEqual(db.execute('CREATE TABLE sample (name LONG VARCHAR, amount INTEGER)'), 0)
        self.assertEqual(db.execute("INSERT INTO sample VALUES ('hello', 42)"), 1)
        db.begin()
        db.execute("INSERT INTO sample VALUES ('discard', 7)")
        db.rollback()
        view = e32db.Db_view()
        view.prepare(db, 'SELECT * FROM sample')
        self.assertEqual(view.count_line(), 1)
        self.assertEqual(view.col_count(), 2)
        with self.assertRaises(RuntimeError):
            view.col(1)
        view.first_line()
        view.get_line()
        self.assertEqual((view.col(1), view.col_type(1), view.col(2)), ('hello', 15, 42))
        self.assertEqual(view.col_raw(2), struct.pack('<i', 42))
        with self.assertRaises(TypeError):
            view.col_raw(1)
        view.next_line()
        with self.assertRaises(RuntimeError):
            view.get_line()
        db.close()

    def test_dates_nulls_and_literal_hashes(self):
        db = e32db.Dbms()
        db.create(self.path('db'))
        db.open(self.path('db'))
        db.execute('CREATE TABLE sample (stamp TIMESTAMP, number INTEGER, name VARCHAR(30))')
        db.execute("INSERT INTO sample VALUES (#%s#, NULL, 'literal #a#')" % e32db.format_time(12345678))
        view = e32db.Db_view()
        view.prepare(db, 'SELECT * FROM sample')
        view.get_line()
        self.assertEqual(view.col(1), 12345678.0)
        raw = view.col_rawtime(1)
        self.assertEqual(e32db.format_rawtime(raw), e32db.format_time(12345678))
        self.assertTrue(view.is_col_null(2))
        self.assertEqual(view.col(2), 0)
        self.assertEqual(view.col_length(2), 0)
        self.assertEqual(view.col(3), 'literal #a#')
        db.close()


class AudioContract(TemporaryFiles):
    def setUp(self):
        TemporaryFiles.setUp(self)
        try:
            import pygame
        except ImportError:
            self.skipTest('pygame not installed')
        import audio
        self.audio = audio
        self.filename = self.path('silence.wav')
        with closing(wave.open(self.filename, 'wb')) as stream:
            stream.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
            stream.writeframes(b'\x00\x00'*2205)
        self.sound = audio.Sound.open(self.filename)

    def tearDown(self):
        if hasattr(self, 'sound'):
            self.sound.close()
        TemporaryFiles.tearDown(self)

    def test_playback_state_callback_and_duration(self):
        sound, audio = self.sound, self.audio
        self.assertEqual(sound.state(), audio.EOpen)
        self.assertAlmostEqual(sound.duration(), 100000, delta=1000)
        calls = []
        sound.play(callback=lambda old, new, err: calls.append((old, new, err)))
        self.assertEqual(sound.state(), audio.EPlaying)
        with self.assertRaises(RuntimeError):
            sound.play()
        deadline = time.time()+2
        while sound.state() == audio.EPlaying and time.time() < deadline:
            e32.ao_sleep(.01)
        self.assertEqual(calls, [(audio.EOpen, audio.EPlaying, 0), (audio.EPlaying, audio.EOpen, 0)])

    def test_volume_position_and_close(self):
        self.sound.set_volume(999)
        self.assertEqual(self.sound.current_volume(), self.sound.max_volume())
        self.sound.set_volume(-1)
        self.assertEqual(self.sound.current_volume(), 0)
        self.sound.set_position(50000)
        self.assertEqual(self.sound.current_position(), 50000)
        self.sound.close()
        self.assertEqual(self.sound.state(), self.audio.ENotReady)


if __name__ == '__main__':
    unittest.main()
