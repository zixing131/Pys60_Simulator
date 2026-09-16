# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Desktop extension contracts derived from Nokia's wrappers and method tables."""

import os

os.environ["PYS60_HEADLESS"] = "1"
import sys
import tempfile
import shutil
import unittest
import threading
import time
import datetime

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pys60_Simulator", "pys60Core"))
)
from _compat import timestamp
import e32, graphics, simulator, contacts, calendar, inbox, messaging, telephone, logs, positioning, sensor, camera, location


class DeviceTest(unittest.TestCase):
    def setUp(self):
        self.old = os.environ.get("PYS60_DATA_DIR")
        self.path = tempfile.mkdtemp(prefix="pys60-devices-")
        os.environ["PYS60_DATA_DIR"] = self.path

    def tearDown(self):
        telephone.cancel()
        positioning.stop_position()
        camera.release()
        e32.ao_sleep(0.01)
        if self.old is None:
            os.environ.pop("PYS60_DATA_DIR", None)
        else:
            os.environ["PYS60_DATA_DIR"] = self.old
        shutil.rmtree(self.path)

    def test_contacts_transactions_groups_and_reopen(self):
        db = contacts.open()
        person = db.add_contact()
        person.add_field("first_name", "Ada")
        person.add_field("last_name", "Lovelace")
        person.add_field("mobile_number", "123", location="home")
        person.commit()
        key = person.id
        self.assertEqual(person.title, "Lovelace Ada")
        self.assertEqual(person.find("mobile_number", "home")[0].value, "123")
        person.begin()
        person[0].value = "Changed"
        self.assertEqual(contacts.open()[key][0].value, "Ada")
        person.rollback()
        self.assertEqual(person[0].value, "Ada")
        person[0].value = "Augusta"
        self.assertEqual(contacts.open()[key][0].value, "Augusta")
        group = db.groups.add_group("Friends")
        group.append(key)
        self.assertEqual(list(group), [key])
        self.assertEqual(contacts.open().groups[group.id].name, "Friends")
        self.assertEqual(db.find("augusta")[0].id, key)
        del db[key]
        self.assertEqual(list(group), [])

    def test_contacts_vcard_roundtrip(self):
        db = contacts.open()
        person = db.add_contact()
        person.add_field("first_name", "中文")
        person.add_field("date", 123456789.0)
        person.commit()
        copied = db.import_vcards(person.as_vcard())[0]
        self.assertEqual(copied.title, "中文")
        self.assertEqual(copied.find("date")[0].value, 123456789.0)
        imported = db.import_vcards(
            b"BEGIN:VCARD\r\nVERSION:3.0\r\nN:Test;Joe;;;\r\nTEL;TYPE=CELL,HOME:555\r\nEND:VCARD"
        )[0]
        self.assertEqual(imported.title, "Test Joe")
        self.assertEqual(imported.find("mobile_number", "home")[0].value, "555")

    def test_contacts_invalid_field_and_new_rollback(self):
        db = contacts.open()
        c = db.add_contact()
        with self.assertRaises(KeyError):
            c.add_field("made_up", "x")
        c.add_field("first_name", "draft")
        c.rollback()
        self.assertEqual(len(db), 0)
        self.assertEqual(len(c), 0)

    def test_calendar_transactions_and_repeat(self):
        db = calendar.open()
        event = db.add_appointment()
        start = timestamp(datetime.datetime(2026, 9, 1, 10))
        event.content = "Meeting"
        event.set_time(start, start + 3600)
        event.set_repeat(
            dict(
                type="weekly",
                start=start,
                end=None,
                days=[1],
                exceptions=[start + 7 * 86400],
            )
        )
        event.commit()
        event.begin()
        event.content = "draft"
        event.rollback()
        self.assertEqual(event.content, "Meeting")
        rows = db.monthly_instances(start)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], {"id": event.id, "datetime": start})
        copy_id = db.import_vcalendars(event.as_vcalendar())[0]
        self.assertEqual(db[copy_id].get_repeat(), event.get_repeat())
        with self.assertRaises(ValueError):
            event.alarm = start + 1
        event.alarm = start - 60
        self.assertEqual(calendar.open()[event.id].alarm, start - 60)
        self.assertEqual(calendar.monthrange(2026, 9), (1, 30))

    def test_calendar_todo_and_filters(self):
        db = calendar.open()
        todo = db.add_todo()
        todo.content = "todo"
        todo.commit()
        self.assertIsNone(todo.start_time)
        todo.crossed_out = True
        self.assertTrue(todo.crossed_out)
        with self.assertRaises(RuntimeError):
            db.add_todo_list("x")
        event = db.add_event()
        stamp = timestamp(datetime.datetime(2026, 9, 3, 15))
        event.set_time(stamp)
        event.commit()
        self.assertEqual(len(db.daily_instances(stamp, events=1)), 1)
        self.assertEqual(db.daily_instances(stamp, appointments=1), [])

    def test_message_notification_and_folders(self):
        box = inbox.Inbox()
        events = []
        box.bind(events.append)
        key = simulator.receive_sms("123", "hello")
        self.assertEqual(events, [])
        e32.ao_yield()
        self.assertEqual(events, [key])
        self.assertEqual(box.content(key), "hello")
        self.assertEqual(box.address(key), "123")
        self.assertEqual(box.unread(key), 1)
        box.set_unread(key, 0)
        self.assertEqual(box.unread(key), 0)
        self.assertEqual(logs.sms()[0]["number"], "123")
        box.delete(key)
        with self.assertRaises(e32.SymbianError):
            box.content(key)
        key = simulator.receive_sms("123", "cancel notification")
        box.bind(None)
        e32.ao_yield()
        self.assertEqual(events, [key - 1])

    def test_sms_async_first_event_then_terminal(self):
        events = []
        self.assertIsNone(messaging.sms_send("555", "text", "UCS2", events.append))
        self.assertEqual(events, [messaging.ECreated])
        with self.assertRaises(RuntimeError):
            messaging.sms_send("1", "busy")
        e32.ao_sleep(0.03)
        self.assertEqual(events, [0, 1, 2, 3, 4])
        self.assertEqual(inbox.Inbox(inbox.EOutbox).sms_messages(), [])
        self.assertEqual(len(inbox.Inbox(inbox.ESent).sms_messages()), 1)
        self.assertEqual(logs.sms(mode="out")[0]["subject"], "text")
        messaging.sms_send("556", "synchronous")
        self.assertFalse(messaging._sending)

    def test_telephone_outgoing_incoming_and_cancel(self):
        events = []
        telephone.call_state(events.append)
        telephone.dial("10086")
        e32.ao_sleep(0.04)
        self.assertEqual([x[0] for x in events], [2, 5, 6])
        self.assertTrue(all(x[1] == "" for x in events))
        telephone.hang_up()
        e32.ao_sleep(0.03)
        self.assertEqual(events[-1][0], telephone.EStatusIdle)
        telephone.incoming_call()
        simulator.receive_call("555")
        e32.ao_yield()
        self.assertEqual(events[-1], (telephone.EStatusRinging, "555"))
        telephone.answer()
        e32.ao_sleep(0.03)
        telephone.hang_up()
        e32.ao_sleep(0.03)
        self.assertEqual(len(logs.calls(mode="in")), 1)
        self.assertEqual(len(logs.calls(mode="out")), 1)
        telephone.dial("123")
        telephone.cancel()
        count = len(events)
        e32.ao_sleep(0.03)
        self.assertEqual(len(events), count)

    def test_gps_sync_async_deepcopy_and_cancel(self):
        simulator.set_position(31, 121, course={"speed": 2.5})
        positioning.set_requestors(
            [dict(type="service", format="application", data="tests")]
        )
        sample = positioning.position(course=1)
        self.assertEqual(sample["course"]["speed"], 2.5)
        self.assertIsNone(sample["satellites"])
        sample["position"]["latitude"] = 99
        self.assertEqual(positioning.last_position()["latitude"], 31)
        events = []

        def callback(event):
            events.append(event)
            positioning.stop_position()

        positioning.position(callback=callback, interval=1000)
        with self.assertRaises(RuntimeError):
            positioning.position()
        e32.ao_sleep(0.02)
        self.assertEqual(len(events), 1)
        simulator.set_gsm_location(460, 0, 12, 34)
        self.assertEqual(location.gsm_location(), (460, 0, 12, 34))

    def test_sensor_filters_and_disconnect(self):
        events = []
        device = sensor.Sensor(1, 1)
        device.set_event_filter(sensor.RotEventFilter())
        self.assertEqual(device.connect(events.append), 1)
        simulator.emit_sensor(1, 90)
        e32.ao_yield()
        self.assertEqual(events, [sensor.orientation.TOP])
        simulator.emit_sensor(1, 0)
        device.disconnect()
        e32.ao_yield()
        self.assertEqual(len(events), 1)

    def test_camera_images_finder_jpeg_and_recording(self):
        from PIL import Image

        simulator.set_camera_source(Image.new("RGB", (20, 20), (255, 0, 0)))
        self.assertEqual(camera.cameras_available(), 1)
        self.assertEqual(
            camera.take_photo(size=(160, 120)).getpixel((10, 10)), [(255, 0, 0)]
        )
        self.assertTrue(
            camera.take_photo("JPEG_Exif", size=(160, 120)).startswith(b"\xff\xd8")
        )
        frames = []
        camera.start_finder(frames.append, size=(32, 24))
        with self.assertRaises(RuntimeError):
            camera.start_finder(frames.append)
        events = []
        filename = os.path.join(self.path, "record.avi")
        camera.start_record(
            filename, lambda error, event: events.append((error, event))
        )
        e32.ao_sleep(0.18)
        camera.stop_record()
        camera.stop_finder()
        e32.ao_yield()
        self.assertGreaterEqual(len(frames), 2)
        self.assertEqual(frames[0].size, (32, 24))
        self.assertEqual(
            [v[1] for v in events],
            [camera.EOpenComplete, camera.EPrepareComplete, camera.ERecordComplete],
        )
        import cv2

        capture = cv2.VideoCapture(filename)
        ok, pixels = capture.read()
        capture.release()
        self.assertTrue(ok)
        self.assertEqual(pixels.shape, (480, 640, 3))


class GLTest(unittest.TestCase):
    def setUp(self):
        import gles, glcanvas

        self.g = gles
        self.c = glcanvas.GLCanvas(lambda frame: None)

    def tearDown(self):
        self.c._context.close()

    def test_triangle_framebuffer_and_fixed_point(self):
        g = self.g
        g.glClearColorx(0, 0, 0, 65536)
        g.glClear(g.GL_COLOR_BUFFER_BIT)
        g.glVertexPointerx(
            g.array(g.GL_FIXED, 2, [(-32768, -32768), (32768, -32768), (0, 32768)])
        )
        g.glEnableClientState(g.GL_VERTEX_ARRAY)
        g.glColor4x(65536, 0, 0, 65536)
        g.glPushMatrix()
        g.glDrawArrays(g.GL_TRIANGLES, 0, 3)
        g.glPopMatrix()
        w, h = self.c.size
        self.assertEqual(
            g.glReadPixels(w // 2, h // 2, 1, 1, g.GL_RGB, g.GL_UNSIGNED_BYTE),
            b"\xff\x00\x00",
        )
        self.c.drawNow()
        self.assertEqual(self.c.getpixel((w // 2, h // 2)), [(255, 0, 0)])
        self.assertEqual(g.glGetIntegerv(g.GL_VIEWPORT), (0, 0, w, h))
        with self.assertRaises(ValueError):
            g.glDrawArrays(g.GL_TRIANGLES, 0, 4)

    def test_buffers_texture_pixels_and_surface(self):
        g = self.g
        from _gles_manifest import METHODS, CONSTANTS

        self.assertTrue(all(hasattr(g, name) for name in METHODS + list(CONSTANTS)))
        texture = g.glGenTextures(1)
        g.glBindTexture(g.GL_TEXTURE_2D, texture)
        image = graphics.Image.new((3, 2), "RGB")
        image.clear(0x123456)
        self.assertEqual(
            g.Image2str(g.GL_RGB, g.GL_UNSIGNED_BYTE, image), b"\x12\x34\x56" * 6
        )
        g.glTexImage2DIO(g.GL_TEXTURE_2D, 0, g.GL_RGB, 0, g.GL_UNSIGNED_BYTE, image)
        buffer = g.glGenBuffers(1)
        g.glBindBuffer(g.GL_ARRAY_BUFFER, buffer)
        g.glBufferDataf(g.GL_ARRAY_BUFFER, [1, 2, 3], g.GL_STATIC_DRAW)
        self.assertEqual(
            g.glGetBufferParameteriv(g.GL_ARRAY_BUFFER, g.GL_BUFFER_SIZE), (12,)
        )
        g.glDeleteBuffers([buffer])
        g.glDeleteTextures([texture])
        self.assertFalse(g.CheckExtension("glCurrentPaletteMatrixOES"))
        with self.assertRaises(NotImplementedError):
            g.glCurrentPaletteMatrixOES(0)

    def test_context_isolation_and_callback_shapes(self):
        import glcanvas

        g = self.g
        g.glClearColor(1, 0, 0, 1)
        g.glClear(g.GL_COLOR_BUFFER_BIT)
        frames = []
        sizes = []
        c = glcanvas.GLCanvas(frames.append, resize_callback=sizes.append)
        try:
            g.glClearColor(0, 1, 0, 1)
            g.glClear(g.GL_COLOR_BUFFER_BIT)
            c.drawNow()
            self.assertEqual(frames, [0])
            self.assertEqual(c.getpixel((1, 1)), [(0, 255, 0)])
            self.c.makeCurrent()
            self.assertEqual(
                g.glReadPixels(1, 1, 1, 1, g.GL_RGB, g.GL_UNSIGNED_BYTE),
                b"\xff\x00\x00",
            )
            c._resize((32, 32))
            self.assertEqual(sizes, [None])
            self.assertEqual(frames, [0, 1])
        finally:
            c._context.close()


class DesktopDrawingTest(unittest.TestCase):
    def test_sdk_color_conversion_all_write_paths(self):
        expected = {
            "RGB12": (119, 34, 68),
            "RGB16": (123, 44, 66),
            "L": (67, 67, 67),
            "1": (0, 0, 0),
        }
        source = graphics.Image.new((2, 2), "RGB")
        source.clear((123, 45, 67))
        for mode, color in expected.items():
            image = graphics.Image.new((2, 2), mode)
            image.clear((123, 45, 67))
            self.assertEqual(image.getpixel((0, 0)), [color])
            image.clear()
            image.blit(source)
            self.assertEqual(image.getpixel((0, 0)), [color])

    def test_pattern_uses_fill_and_preserves_black_cells(self):
        pattern = graphics.Image.new((2, 1), "1")
        pattern.clear(0)
        pattern.point((0, 0), outline=0xFFFFFF)
        image = graphics.Image.new((4, 2), "RGB")
        image.clear(0x0000FF)
        image.rectangle((0, 0, 4, 2), fill=0xFF0000, pattern=pattern)
        self.assertEqual(
            image.getpixel(((0, 0), (1, 0), (2, 0), (3, 0))),
            [(255, 0, 0), (0, 0, 255)] * 2,
        )

    def test_font_flags_and_measurements(self):
        image = graphics.Image.new((100, 40), "RGB")
        plain = image.measure_text("Test", font=("normal", 20))
        bold = image.measure_text("Test", font=("normal", 20, graphics.FONT_BOLD))
        self.assertGreater(bold[0][2] - bold[0][0], plain[0][2] - plain[0][0])
        image.text(
            (3, 30),
            "Test",
            font=("normal", 20, graphics.FONT_ITALIC | graphics.FONT_ANTIALIAS),
        )
        self.assertEqual(graphics.GetFont(font=(None,)).size, 8)
        with self.assertRaises(ValueError):
            graphics.GetFont(font=("normal", 20, 64))

    def test_screenshot_chrome_text_list_and_canvas_alignment(self):
        import appuifw as ui

        old, screen, tabs = ui.app.body, ui.app.screen, ui.app._tabs
        try:
            ui.app.screen = "normal"
            ui.app.set_tabs(["A", "B"])
            ui.app.title = "Rendering"
            ui.app.body = ui.Text("visible text")
            shot = graphics.screenshot()
            self.assertEqual(shot.size, graphics.screen)
            self.assertNotEqual(shot.getpixel((1, 1)), [(255, 255, 255)])
            self.assertIsNotNone(
                shot.image.crop((0, 44, 200, 80))
                .convert("L")
                .point(lambda v: 255 - v)
                .getbbox()
            )
            ui.app.body = ui.Listbox(["one", "two"])
            shot = graphics.screenshot()
            self.assertEqual(shot.getpixel((1, 45)), [(49, 92, 135)])
            canvas = ui.Canvas()
            ui.app.body = canvas
            canvas.clear(0xFF0000)
            self.assertEqual(graphics.screenshot().getpixel((1, 45)), [(255, 0, 0)])
        finally:
            ui.app.set_tabs(tabs)
            ui.app.screen = screen
            ui.app.body = old


class BluetoothTest(unittest.TestCase):
    def setUp(self):
        getattr(DeviceTest.setUp, "__func__", DeviceTest.setUp)(self)
    def tearDown(self):
        getattr(DeviceTest.tearDown, "__func__", DeviceTest.tearDown)(self)

    # Separate only the transport test from the shared temporary device setup.
    def test_virtual_rfcomm_discovery_and_obex(self):
        import pys60Socket, socket

        server = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
        client = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
        peer = None
        try:
            channel = socket.bt_rfcomm_get_available_server_channel(server)
            server.bind(("", channel))
            server.listen(1)
            socket.bt_advertise_service("Example", server, True)
            address, services = socket.bt_discover()
            self.assertEqual(services["Example"], channel)
            accepted = []
            server.accept(accepted.append)
            client.connect((address, channel))
            e32.ao_yield()
            peer, remote = accepted[0]
            self.assertEqual(remote, address)
            client.sendall(b"payload")
            self.assertEqual(peer.recv(7), b"payload")
            socket.bt_advertise_service("Transfer", server, True, socket.OBEX)
            self.assertEqual(socket.bt_obex_discover()[1]["Transfer"], channel)
            source = os.path.join(self.path, "send.bin")
            target = os.path.join(self.path, "receive.bin")
            with open(source, "wb") as stream:
                stream.write(b"\x00\xffpayload")
            e32.ao_sleep(
                0.01, lambda: socket.bt_obex_send_file(address, channel, source)
            )
            socket.bt_obex_receive(server, target)
            with open(target, "rb") as a, open(source, "rb") as b:
                self.assertEqual(a.read(), b.read())
        finally:
            if peer is not None:
                peer.close()
            client.close()
            server.close()


if __name__ == "__main__":
    unittest.main()
