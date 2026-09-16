"""Camera, GPS, contacts/messages and native OpenGL in one desktop window.

python examples/extensions_demo.py
python examples/extensions_demo.py --camera 0  # explicitly use a host camera
python examples/extensions_demo.py --smoke     # short, isolated GUI verification
"""

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "Pys60_Simulator/pys60Core")
)
from pys60_runtime import activate

activate()
import appuifw as ui
import camera
import contacts
import e32
import glcanvas
import gles as gl
import graphics
import inbox
import positioning
import simulator
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", help="host camera index, image path, or video path")
    parser.add_argument("--smoke", action="store_true")
    options = parser.parse_args()
    temporary = tempfile.TemporaryDirectory() if options.smoke else None
    if temporary:
        os.environ["PYS60_DATA_DIR"] = temporary.name
    if options.camera is None:
        source = Image.new("RGB", (640, 480))
        draw = ImageDraw.Draw(source)
        colors = ["#dc5151", "#eebd4b", "#63b770", "#539ed3", "#9364c5"]
        for index, color in enumerate(colors):
            draw.rectangle((index * 128, 0, (index + 1) * 128, 480), fill=color)
        simulator.set_camera_source(source)
    else:
        simulator.set_camera_source(
            int(options.camera) if options.camera.isdigit() else options.camera
        )
    simulator.set_position(31.2304, 121.4737, altitude=12.5, horizontal_accuracy=3.0)
    positioning.set_requestors(
        [dict(type="service", format="application", data="PyS60 desktop demo")]
    )
    fix = positioning.position()["position"]
    database = contacts.open("simulator-demo.cdb", "c")
    if not database.find("Simulator"):
        person = database.add_contact()
        person.add_field("first_name", "Simulator")
        person.add_field("mobile_number", "5550100")
        person.commit()
    ui.app.title = "PyS60 1.4.5"
    ui.app.screen = "normal"
    canvas = ui.Canvas()
    active = [0]
    lock = e32.Ao_lock()
    timer = e32.Ao_timer()

    def finder(frame):
        canvas.blit(frame, scale=1, target=(0, 0, canvas.size[0], canvas.size[1]))
        canvas.rectangle(
            (0, canvas.size[1] - 52, canvas.size[0], canvas.size[1]), fill=0x17324D
        )
        canvas.text(
            (7, canvas.size[1] - 31),
            "Camera feed" if options.camera else "Simulated camera",
            fill=0xFFFFFF,
            font=("normal", 16),
        )
        canvas.text(
            (7, canvas.size[1] - 10),
            "GPS %.4f / %.4f" % (fix["latitude"], fix["longitude"]),
            fill=0xFFFFFF,
            font=("dense", 14),
        )

    def render(frame):
        gl.glClearColor(0.07, 0.12, 0.2, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glRotatef(frame * 2, 0, 0, 1)
        gl.glVertexPointerf([(-0.7, -0.6), (0.7, -0.6), (0, 0.7)])
        gl.glColorPointerf(
            [(1.0, 0.3, 0.3, 1.0), (0.3, 1.0, 0.5, 1.0), (0.3, 0.6, 1.0, 1.0)]
        )
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

    gl_body = glcanvas.GLCanvas(render)

    def select(index):
        camera.stop_finder()
        active[0] = index
        ui.app.activate_tab(index)
        if index == 0:
            ui.app.body = canvas
            camera.start_finder(finder, size=(240, 256))
        elif index == 1:
            ui.app.body = gl_body
            gl_body.drawNow()
        else:
            messages = inbox.Inbox().sms_messages()
            ui.app.body = ui.Listbox(
                [
                    ("Contacts", str(len(database))),
                    ("Inbox messages", str(len(messages))),
                    ("GPS source", "Injected desktop location"),
                    ("First contact", database[next(iter(database))].title),
                ]
            )

    def receive():
        simulator.receive_sms("5550100", "Hello from the desktop simulator")
        select(2)

    def tick():
        if active[0] == 1:
            gl_body.drawNow()
        timer.after(0.05, tick)

    def close():
        timer.cancel()
        camera.release()
        positioning.stop_position()
        ui.app.body = None
        gl_body._context.close()
        ui.app.set_exit()
        lock.signal()

    ui.app.menu = [
        ("Inject SMS", receive),
        ("Camera", lambda: select(0)),
        ("OpenGL", lambda: select(1)),
        ("Data", lambda: select(2)),
        ("Exit", close),
    ]
    ui.app.exit_key_handler = close
    ui.app.set_tabs(["Camera", "OpenGL", "Data"], select)
    select(0)
    tick()
    if options.smoke:
        e32.ao_sleep(0.12)
        select(1)
        e32.ao_sleep(0.12)
        assert gl_body.getpixel((120, 128)) != [(255, 255, 255)]
        receive()
        e32.ao_yield()
        assert len(inbox.Inbox().sms_messages()) == 1
        close()
        print(
            "Extensions demo: camera, GPS, contacts, SMS, OpenGL and tab switching passed"
        )
    else:
        lock.wait()
    if temporary:
        temporary.cleanup()


if __name__ == "__main__":
    main()
