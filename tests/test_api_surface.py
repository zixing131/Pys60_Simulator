"""Ensure public entry points exported by the local 1.4.5 source exist.

This verifies API presence only. Semantic regressions live in test_contract.py.
No Symbian binary or the source's build system is executed.
"""
import os
import re
import sys
import unittest
os.environ['PYS60_HEADLESS'] = '1'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'Pys60_Simulator', 'pys60Core'))
REFERENCE = os.path.join(ROOT, 'pys60-1.4.5_src')


class ReferenceSurface(unittest.TestCase):
    def source(self, path):
        filename = os.path.join(REFERENCE, path)
        if not os.path.isfile(filename):
            self.skipTest('optional local pys60-1.4.5_src tree not present')
        with open(filename) as stream:
            return stream.read()

    def table(self, source, table_name):
        pattern = r'\b'+re.escape(table_name)+r'\[\]\s*=\s*\{(.*?)\{NULL'
        match = re.search(pattern, source, re.S)
        self.assertIsNotNone(match, 'reference table not found: '+table_name)
        body = re.sub(r'/\*.*?\*/', '', match.group(1), flags=re.S)
        return [name for name in re.findall(r'\{\s*"(\w+)"', body) if not name.startswith('_')]

    def assert_exports(self, target, names):
        missing = [name for name in names if not hasattr(target, name)]
        self.assertEqual(missing, [], 'missing public API on '+str(target))

    def test_e32_exports(self):
        import e32
        self.assert_exports(e32, self.table(self.source('core/Symbian/e32module.cpp'), 'e32_methods'))

    def test_ui_exports_and_controls(self):
        import appuifw
        source = self.source('appui/appuifw/appuifwmodule.cpp')
        self.assert_exports(appuifw, self.table(source, 'appuifw_methods'))
        for table, target in [('Text_methods', appuifw.Text), ('Listbox_methods', appuifw.Listbox),
                              ('Form_methods', appuifw.Form), ('Canvas_methods', appuifw.Canvas)]:
            self.assert_exports(target, self.table(source, table))
        constants = re.findall(r'PyDict_SetItemString\(d, "([A-Z]\w+)"', source)
        self.assert_exports(appuifw, constants)

    def test_graphics_exports(self):
        import graphics
        wrapper = self.source('ext/graphics/graphics.py')
        # Includes static methods and properties, but not private plumbing.
        methods = [name for name in re.findall(r'^    (?:    )?def (\w+)\(', wrapper, re.M) if not name.startswith('_')]
        self.assert_exports(graphics.Image, methods)
        self.assert_exports(graphics.Image, self.table(self.source('ext/graphics/graphicsmodule.cpp'), 'Draw_methods'))

    def test_database_exports(self):
        import e32db
        source = self.source('ext/e32db/e32dbmodule.cpp')
        self.assert_exports(e32db.Dbms, self.table(source, 'dbms_methods'))
        self.assert_exports(e32db.Db_view, self.table(source, 'dbview_methods'))

    def test_audio_and_system_exports(self):
        import audio
        import sysinfo
        methods = re.findall(r'^    def (\w+)\(', self.source('ext/recorder/audio.py'), re.M)
        self.assert_exports(audio.Sound, [name for name in methods if not name.startswith('_')])
        methods = re.findall(r'^def (\w+)\(', self.source('ext/sysinfo/sysinfo.py'), re.M)
        self.assert_exports(sysinfo, methods)

    def test_device_extension_exports(self):
        import importlib
        for name, path in [('camera','camera/camera.py'),('positioning','gps/positioning.py'),
                           ('messaging','messaging/messaging.py'),('telephone','telephone/telephone.py'),
                           ('logs','logs/logs.py'),('sensor','sensor/sensor.py')]:
            source = self.source('ext/'+path)
            names = [n for n in re.findall(r'^(?:    )?def (\w+)\(' if name == 'telephone' else r'^def (\w+)\(', source, re.M) if not n.startswith('_')]
            if name == 'sensor':
                names = ['sensors','Sensor','EventFilter','OrientationEventFilter','RotEventFilter']
            if name == 'positioning':
                names = [n for n in re.findall(r'^def (\w+)\(', source, re.M) if n != 'revdict']
            self.assert_exports(importlib.import_module(name), names)
        import inbox
        source = self.source('ext/inbox/inboxmodule.cpp')
        self.assert_exports(inbox.Inbox, self.table(source,'inb_methods'))

    def test_gles_and_glcanvas_exports(self):
        import gles, glcanvas
        source = self.source('ext/gles/glesmodule.cpp')
        self.assert_exports(gles, self.table(source,'gles_methods'))
        self.assert_exports(gles, re.findall(r'PyDict_SetItemString\(d, "(GL_\w+)"', source))
        source = self.source('ext/glcanvas/glcanvasmodule.cpp')
        self.assert_exports(glcanvas.GLCanvas, ['bind','drawNow','makeCurrent'])
        self.assert_exports(glcanvas, re.findall(r'^\s*PyDict_SetItemString\(d, "(EGL_\w+)"', source,re.M))


if __name__ == '__main__':
    unittest.main()
