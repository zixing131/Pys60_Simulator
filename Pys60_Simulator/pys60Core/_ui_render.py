"""One software compositor for desktop presentation and graphics.screenshot()."""
from _compat import string_types

import graphics as g

_CACHE = {}


def chrome(app):
    width, height = g.screen
    image = g.Image.new((width, height), "RGB")
    if app.screen == "normal":
        image.rectangle((0, 0, width, 44), fill=0x234568)
        image.text((8, 21), app.title, fill=0xFFFFFF, font=("normal", 18))
        if app._tabs:
            tab_width = width // len(app._tabs)
            for i, label in enumerate(app._tabs):
                x = i * tab_width
                color = 0x426D98 if i == app._active_tab else 0x234568
                image.rectangle((x, 24, x + tab_width, 44), fill=color)
                image.text((x + 4, 40), label, fill=0xFFFFFF, font=("dense", 14))
    if app.screen != "full":
        image.rectangle((0, height - 20, width, height), fill=0x234568)
        image.text(
            (5, height - 4),
            "Options" if app.menu else "",
            fill=0xFFFFFF,
            font=("dense", 14),
        )
        image.text((width - 36, height - 4), "Exit", fill=0xFFFFFF, font=("dense", 14))
    return image.image


def control(body, size):
    import appuifw as ui

    if isinstance(body, ui.Canvas):
        return body.image
    image = g.Image.new(size, "RGB")
    width, height = size
    body._hit_positions = []
    if isinstance(body, ui.Text):
        body._sync()
        # Style/font is sampled at insertion and retained per character.
        styles = getattr(body, "_styles", [])
        default = (body.font, body.color, body.style, body.highlight_color)
        x, y = 4, 22
        positions = []
        for index, char in enumerate(body._value):
            spec, color, style, highlight = (
                styles[index] if index < len(styles) else default
            )
            font = (spec, 18) if isinstance(spec, string_types) else spec
            flags = (g.FONT_BOLD if style & ui.STYLE_BOLD else 0) | (
                g.FONT_ITALIC if style & ui.STYLE_ITALIC else 0
            )
            font = (font[0], font[1], flags)
            face = g.GetFont(font=font)
            advance = max(1, g._metrics(char, face)[1])
            line_height = max(22, face.size + 4)
            if char == "\n":
                positions.append((x, y))
                x, y = 4, y + line_height
                continue
            if x + advance > width - 4:
                x, y = 4, y + line_height
            positions.append((x, y))
            if style & (
                ui.HIGHLIGHT_STANDARD | ui.HIGHLIGHT_ROUNDED | ui.HIGHLIGHT_SHADOW
            ):
                image.rectangle((x, y - face.size, x + advance, y + 3), fill=highlight)
            image.text((x, y), char, fill=color, font=font)
            if style & ui.STYLE_UNDERLINE:
                image.line((x, y + 2, x + advance, y + 2), outline=color)
            if style & ui.STYLE_STRIKETHROUGH:
                image.line(
                    (x, y - face.size // 3, x + advance, y - face.size // 3),
                    outline=color,
                )
            x += advance
        positions.append((x, y))
        cursor = positions[min(body._pos, len(positions) - 1)]
        scroll = max(0, cursor[1] - height + 4)
        # Re-render into a tall backing buffer when text extends below the pane.
        if scroll and height == size[1] and not getattr(body, "_rendering_tall", False):
            body._rendering_tall = True
            try:
                tall = control(body, (width, max(y + 8, height)))
                image.image = tall.crop((0, scroll, width, scroll + height))
            finally:
                body._rendering_tall = False
        if body.focus:
            image.line(
                (cursor[0], cursor[1] - 17 - scroll, cursor[0], cursor[1] + 2 - scroll),
                outline=0,
            )
        body._hit_positions = [(px, py - scroll) for px, py in positions]
    elif isinstance(body, ui.Listbox):
        current = body.current()
        row_height = 44 if body._kind.startswith("double") else 28
        visible = max(1, height // row_height)
        first = max(0, current - visible + 1)
        body._first_visible = first
        for row, item in enumerate(body._items[first : first + visible + 1]):
            y = row * row_height
            selected = first + row == current
            if selected:
                image.rectangle((0, y, width, y + row_height), fill=0x315C87)
            color = 0xFFFFFF if selected else 0
            labels = (
                [item]
                if isinstance(item, string_types)
                else [v for v in item if isinstance(v, string_types)]
            )
            for line, label in enumerate(labels):
                image.text(
                    (6, y + 20 + line * 18),
                    label,
                    fill=color,
                    font=("normal", 17 if line == 0 else 14),
                )
    return image.image


def snapshot(app):
    import appuifw as ui

    pixels = chrome(app)
    if app.body is not None:
        size, position = app.layout(ui.EMainPane)
        pixels.paste(control(app.body, size), position)
    for overlay in app._overlays:
        if overlay.visible:
            pixels.paste(overlay._render().image, overlay.position)
    return pixels


def present(app):
    import appuifw as ui
    from PIL import ImageTk

    if ui.root is None:
        return
    if getattr(app, "_chrome_widget", None) is None:
        app._chrome_widget = ui.tk.Canvas(ui.root, highlightthickness=0)
        app._chrome_widget.place(x=0, y=0, width=g.screen[0], height=g.screen[1])
        app._chrome_widget.bind(
            "<Button-1>", lambda event: _chrome_click(app, event.x, event.y)
        )
        app._chrome_item = app._chrome_widget.create_image(0, 0, anchor="nw")
    app._chrome_widget.place_configure(width=g.screen[0], height=g.screen[1])
    key = (
        g.screen,
        app.screen,
        app.title,
        tuple(app._tabs),
        app._active_tab,
        bool(app.menu),
    )
    if getattr(app, "_chrome_key", None) != key:
        app._chrome_photo = ImageTk.PhotoImage(chrome(app), master=ui.root)
        app._chrome_widget.itemconfigure(app._chrome_item, image=app._chrome_photo)
        app._chrome_key = key
    body = app.body
    if body is None:
        return
    size, position = app.layout(ui.EMainPane)
    if body._widget is not None:
        body._widget.place(x=position[0], y=position[1], width=size[0], height=size[1])
        body._widget.tk.call("raise", body._widget._w)
    if isinstance(body, ui.Canvas):
        return
    if getattr(body, "_surface", None) is None:
        body._surface = ui.tk.Canvas(ui.root, highlightthickness=0)
        body._surface_item = body._surface.create_image(0, 0, anchor="nw")
        body._surface.bind(
            "<Button-1>", lambda event: _control_click(body, event.x, event.y)
        )
        body._surface.bind(
            "<Double-Button-1>",
            lambda event: body._activate() if isinstance(body, ui.Listbox) else None,
        )
    body._surface.place(x=position[0], y=position[1], width=size[0], height=size[1])
    body._surface.tk.call("raise", body._surface._w)
    if isinstance(body, ui.Text):
        body._sync()
        key = (size, body._value, body._pos, str(body._styles), body.focus)
    else:
        key = (size, str(body._items), body.current())
    if getattr(body, "_surface_key", None) != key:
        body._surface_photo = ImageTk.PhotoImage(control(body, size), master=ui.root)
        body._surface.itemconfigure(body._surface_item, image=body._surface_photo)
        body._surface_key = key


def _chrome_click(app, x, y):
    import appuifw as ui

    if app.screen == "normal" and 24 <= y < 44 and app._tabs:
        app._select_tab(min(len(app._tabs) - 1, x * len(app._tabs) // g.screen[0]))
    elif app.screen != "full" and y >= g.screen[1] - 20:
        app._show_menu() if x < g.screen[0] // 2 else ui._exit_key()


def _control_click(body, x, y):
    import appuifw as ui

    if isinstance(body, ui.Text):
        if body._hit_positions:
            index = min(
                range(len(body._hit_positions)),
                key=lambda i: abs(body._hit_positions[i][1] - y - 8) * 1000
                + abs(body._hit_positions[i][0] - x),
            )
            body.set_pos(index)
    else:
        row_height = 44 if body._kind.startswith("double") else 28
        body._current = min(len(body._items) - 1, body._first_visible + y // row_height)
        body._widget.selection_clear(0, "end")
        body._widget.selection_set(body._current)
        body._widget.activate(body._current)
    if body._widget is not None:
        body._widget.focus_set()
    present(ui.app)
