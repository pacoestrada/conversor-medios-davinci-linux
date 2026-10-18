"""Run with Xvfb at each target resolution; optional screenshots via Pillow."""
import importlib.util
import os
from pathlib import Path
import tkinter as tk

root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('gui', root / 'src/conversor-gui.py')
gui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gui)


def walk(widget):
    for child in widget.winfo_children():
        yield child
        yield from walk(child)


def check(window):
    window.update()
    sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
    assert window.winfo_width() <= sw
    assert window.winfo_height() <= sh
    assert abs(window.winfo_x() - (sw - window.winfo_width()) // 2) <= 24
    for size in [None, (620, 700), (360, 500)]:
        if size:
            window.geometry(f'{size[0]}x{size[1]}')
            window.update()
        widgets = list(walk(window))
        buttons = [w for w in widgets if isinstance(w, tk.Button)]
        assert len(buttons) == 2
        for widget in widgets:
            if isinstance(widget, (tk.Label, tk.Button)):
                assert widget.winfo_width() >= widget.winfo_reqwidth(), (widget.cget('text'), widget.winfo_width(), widget.winfo_reqwidth())
                assert widget.winfo_height() >= widget.winfo_reqheight(), widget.cget('text')
                assert widget.winfo_x() >= 0, widget.cget('text')
                assert widget.winfo_x() + widget.winfo_width() <= widget.master.winfo_width(), widget.cget('text')
        if size and size[0] == 360:
            assert buttons[1].winfo_rooty() > buttons[0].winfo_rooty()
        if os.environ.get('SCREENSHOT_DIR'):
            from PIL import ImageGrab
            target = Path(os.environ['SCREENSHOT_DIR'])
            target.mkdir(exist_ok=True, parents=True)
            ImageGrab.grab(xdisplay=os.environ['DISPLAY']).save(target / f'{sw}x{sh}-{window.winfo_width()}-scale{window.tk.call("tk", "scaling")}.png')
    canvas = next(w for w in walk(window) if isinstance(w, tk.Canvas))
    canvas.yview_moveto(1)
    window.update()
    assert canvas.yview()[1] == 1.0
    assert buttons[1].winfo_rooty() + buttons[1].winfo_height() <= window.winfo_rooty() + window.winfo_height()
    calls = []
    gui.subprocess.Popen = lambda args, env: calls.append(env['CONVERSOR_DIRECCION'])
    buttons[int(os.environ.get('TEST_BUTTON', '1'))].invoke()
    assert calls == ['editar' if os.environ.get('TEST_BUTTON') == '0' else 'publicar']
    print(f'GUI comprobada en {sw}x{sh}')


if os.environ.get('TEST_SCALE'):
    original = tk.Tk.__init__
    def init(self, *args, **kwargs):
        original(self, *args, **kwargs)
        self.tk.call('tk', 'scaling', float(os.environ['TEST_SCALE']))
    tk.Tk.__init__ = init
# Test desktop panels without needing a specific window manager.
if os.environ.get('TEST_WORKAREA'):
    gui.available_area = lambda window: (0, 32, window.winfo_screenwidth(), window.winfo_screenheight() - 80)
    def check_area(window):
        window.update()
        assert window.winfo_y() >= 32
        assert window.winfo_y() + window.winfo_height() <= window.winfo_screenheight() - 48
        window.destroy()
    gui.tk.Tk.mainloop = check_area
else:
    gui.tk.Tk.mainloop = check
gui.main()
