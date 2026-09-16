# -*- coding: utf-8 -*-
"""Run real bundled applications, with isolated saves, on Python 2.7 or 3.

python tests/app_regression.py [--gui] [--output /tmp/pys60-regression]
No external services are contacted. Each app runs through run_pys60.py from a
foreign working directory, exercises controls, and saves its actual framebuffer.
"""
from __future__ import print_function
import os
import sys
import tempfile
import shutil
import subprocess
import threading
import runpy
import traceback
import argparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APPS = [
    ('qq', 'softwares/qqui.py'),
    ('flappy', 'games/flappybird.PY'),
    ('2048', 'games/2048正式版v1.3.py'),
    ('sokoban', 'games/推箱子.py'),
    ('wsg', 'softwares/wsg/demo6.py'),
    ('zui', 'softwares/qq_for_symbian/main.py'),
]


def child(name, output):
    sys.path.insert(0, os.path.join(ROOT, 'Pys60_Simulator', 'pys60Core'))
    from pys60_runtime import activate
    activate()
    import e32, graphics, appuifw as ui
    import random
    random.seed(7)
    state = {}

    def press(key):
        event = type('Event', (), {'keysym': key})()
        ui.app.body.processKeyPressEvent(event)
        ui.app.body.processKeyUpEvent(event)

    def capture(suffix):
        image = graphics.screenshot()
        assert image.size == (240, 320), image.size
        assert len(image.image.getcolors(100000)) > 1, 'blank screen'
        image.save(os.path.join(output, name + '-' + suffix + '.png'))
        if ui.app.body._widget is not None:
            canvas = ui.app.body
            for x, y in ((10, 10), (100, 70), (100, 150), (200, 310)):
                actual = tuple(map(int, canvas._widget.tk.splitlist(
                    canvas._widget.tk.call(str(canvas.lastimg), 'get', x, y))))
                assert actual == image.image.getpixel((x, y)), (actual, x, y)

    def later(callback, delay=0.15):
        def guarded():
            try:
                callback()
            except SystemExit:
                raise
            except BaseException:
                traceback.print_exc()
                raise SystemExit(1)
        e32._schedule(delay, guarded)

    def finish():
        capture('after')
        print('PASS', name, sys.version.split()[0])
        raise SystemExit(0)

    def flappy_started():
        game = state['ns']['app'].classList[1]
        assert state['ns']['app'].index == 1
        assert game.game == 0
        press('5')
        assert game.game == 1
        state['y'] = game.y
        later(flappy_moving, .24)

    def flappy_moving():
        game = state['ns']['app'].classList[1]
        assert game.y != state['y'] or game.game == 2
        later(flappy_over, 3)

    def flappy_over():
        game = state['ns']['app'].classList[1]
        assert game.game == 2, 'bird must reach the ground'
        capture('gameover')
        press('5')
        assert game.game == 0
        ns = state['ns']
        path = os.path.join(ns['savepath'], 'regression.ini')
        ns['write'](path, 42)
        assert ns['read'](path, 'MA==') == 42
        later(finish)

    def sokoban_started():
        game = ui.app.body.event_callback.__self__
        assert game.level == 1
        before = len(game.key_history)
        for key in ('Up', 'Left', 'Down', 'Right'):
            press(key)
        assert len(game.key_history) > before, 'no legal movement'
        history = len(game.key_history)
        game.move_back()
        assert len(game.key_history) == history - 1
        capture('level')
        game.run = 0
        later(finish)

    def ready():
        ns = sys.modules['__main__'].__dict__
        state['ns'] = ns
        capture('before')
        if name == 'qq':
            form = ns['qqUi'].allForm
            assert form.RunningForm == form.login
            # Traverse actual focus/navigation then enter and leave the editor.
            for _ in range(10):
                if form.textboxUsername.focus:
                    break
                press('Down')
            assert form.textboxUsername.focus
            press('Return')
            assert form.textboxUsername.TextEditing == 1
            field = form.textboxUsername.field
            field.add(u'10001')
            if field.textbox is not None:
                field.textbox.insert('end', '2')
                field._finish(None)  # The native editor's Return binding.
            else:
                press('Return')
            assert form.textboxUsername.TextEditing == 0
            assert form.textboxUsername.text in (u'10001', u'100012')
            assert '\n' not in form.textboxUsername.text
            for _ in range(10):
                if form.ckb_rememberPassword.focus:
                    break
                press('Down')
            box = form.ckb_rememberPassword
            assert box.focus
            old = box.value
            press('Return')
            assert box.value != old
            ns['qqUi'].redraw()
            later(finish)
        elif name == 'flappy':
            later(ui._exit_key)  # Cancel the nested exit confirmation.
            ui._exit_key()      # The exact handler bound to F2.
            assert ns['app'].super == 0
            capture('exit-cancelled')
            later(flappy_started)
            press('5')  # Enters the game's nested active loop.
        elif name == '2048':
            game = ns['app'].classList[0]
            game.game = [[1 for _ in range(4)] for _ in range(4)]
            game.game[0][0] = game.game[1][0] = 2
            game.score = 0
            press('Left')
            assert game.score == 4 and game.game[0][0] == 4
            ns['write'](game.score)
            assert ns['read']() == 4
            later(finish)
        elif name == 'sokoban':
            later(sokoban_started)
            press('5')
        elif name == 'wsg':
            editor = ns['i']
            editor.SetText(editor._StaticEdit__text * 3)
            assert editor._StaticEdit__scroll
            editor.drawNext()
            assert editor._StaticEdit__beg > 0
            editor.drawPrev()
            assert editor._StaticEdit__beg == 0
            ns['OnClicked']()
            ns['OnSet']()
            assert ns['j'].GetValue() == 100.0
            for _ in range(3):
                ns['a'].redraw()
            assert editor._StaticEdit__end == len(editor._StaticEdit__text)
            later(finish)
        elif name == 'zui':
            app = ns['app']
            for _ in range(10):
                if app.txt_username._Textbox__enter:
                    break
                press('Down')
            assert app.txt_username._Textbox__enter
            press('Return')
            assert app.txt_username._Textbox__editing
            press('Return')
            assert not app.txt_username._Textbox__editing
            app.wnd.redraw()
            later(finish)

    def timeout():
        print('FAIL: scheduler deadline', name)
        raise SystemExit(1)

    later(ready, 4)
    later(timeout, 20)
    entry = dict(APPS)[name]
    sys.argv = [os.path.join(ROOT, 'run_pys60.py'),
                os.path.join(ROOT, 'Pys60_Simulator', entry)]
    runpy.run_path(sys.argv[0], run_name='__main__')
    raise AssertionError('application exited without completing regression')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--child')
    parser.add_argument('--gui', action='store_true')
    parser.add_argument('--output', default=os.path.join(tempfile.gettempdir(), 'pys60-app-regression'))
    args = parser.parse_args()
    if args.gui:
        os.environ.pop('PYS60_HEADLESS', None)
    else:
        os.environ['PYS60_HEADLESS'] = '1'
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    if args.child:
        child(args.child, os.path.abspath(args.output))
        return
    failures = []
    for name, entry in APPS:
        work = tempfile.mkdtemp(prefix='pys60-app-')
        env = os.environ.copy()
        env['PYS60_DATA_DIR'] = os.path.join(work, 'data')
        command = [sys.executable, os.path.abspath(__file__), '--child', name,
                   '--output', os.path.abspath(args.output)]
        if args.gui:
            command.append('--gui')
        process = subprocess.Popen(command, cwd=work, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        watchdog = threading.Timer(30, process.kill)
        watchdog.start()
        try:
            result = process.communicate()[0].decode('utf-8', 'replace')
        finally:
            watchdog.cancel()
            shutil.rmtree(work)
        sys.stdout.write(result.encode('utf-8') if sys.version_info[0] == 2 else result)
        sys.stdout.flush()
        if process.returncode or 'PASS ' + name not in result or 'Traceback' in result:
            failures.append(name)
    if failures:
        raise SystemExit('FAILED: ' + ', '.join(failures))
    print('6 actual applications passed; frames:', args.output)


if __name__ == '__main__':
    main()
