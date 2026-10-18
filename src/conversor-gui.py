#!/usr/bin/env python3
"""Pantalla inicial; el motor Bash conserva la conversión y sus verificaciones."""
import os
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import messagebox, font as tkfont
import re

ROOT = Path(__file__).resolve().parent.parent
INSTALLED = Path('/usr/lib/conversor-medios/conversor-medios')
ENGINE = INSTALLED if INSTALLED.exists() else ROOT / 'src/conversor-medios'
LOGO = (Path('/usr/share/icons/hicolor/128x128/apps/com.pacoestrada.ConversorMp4Mov.png')
        if INSTALLED.exists() else ROOT / 'data/icons/128x128/com.pacoestrada.ConversorMp4Mov.png')


def available_area(window):
    """Use the desktop work area on X11; fall back to Tk on other desktops."""
    area = (0, 0, window.winfo_screenwidth(), window.winfo_screenheight())
    try:
        desktop = subprocess.check_output(
            ['xprop', '-root', '_NET_CURRENT_DESKTOP'], timeout=1, text=True)
        index = int(desktop.split('=')[1].strip())
        output = subprocess.check_output(
            ['xprop', '-root', '_NET_WORKAREA'], timeout=1, text=True)
        values = [int(n) for n in re.findall(r'-?\d+', output.split('=')[1])]
        x, y, width, height = values[index * 4:index * 4 + 4]
        if width > 0 and height > 0:
            area = (x, y, width, height)
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        pass
    # EWMH describes the whole desktop, not an individual monitor.
    try:
        output = subprocess.check_output(
            ['xrandr', '--listactivemonitors'], timeout=1, text=True)
        monitors = []
        for line in output.splitlines():
            match = re.search(r'(\d+)/(?:\d+)x(\d+)/(?:\d+)([+-]\d+)([+-]\d+)', line)
            if match:
                width, height, x, y = map(int, match.groups())
                if width > 0 and height > 0:
                    monitors.append(((x, y, width, height), '*' in line.split()[1]))
        if monitors:
            pointer_x, pointer_y = window.winfo_pointerxy()
            monitor = next((rect for rect, _ in monitors
                            if rect[0] <= pointer_x < rect[0] + rect[2]
                            and rect[1] <= pointer_y < rect[1] + rect[3]),
                           next((rect for rect, primary in monitors if primary), monitors[0][0]))
            mx, my, mw, mh = monitor
            ax, ay, aw, ah = area
            left, top = max(mx, ax), max(my, ay)
            right, bottom = min(mx + mw, ax + aw), min(my + mh, ay + ah)
            area = ((left, top, right - left, bottom - top)
                    if right > left and bottom > top else monitor)
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        pass
    return area


def main():
    window = tk.Tk()
    window.title('Conversor de medios · 2.3.5')
    # Tk's coordinates and EWMH work area share the X11/XWayland coordinate
    # space. Convert design units to that space ONCE, using Tk's effective DPI.
    # Do not multiply by GDK_SCALE: XWayland may already apply compositor scaling.
    scale = float(window.tk.call('tk', 'scaling')) / (96 / 72)
    def px(value):
        return max(1, round(value * scale))
    def font(size, bold=False):
        base = tkfont.nametofont('TkDefaultFont')
        # Negative Tk font sizes are pixels: convert points once, with the
        # same scale as layout. Never reinterpret a resolved named font size
        # as points (desktop font aliases may already contain a pixel size).
        return (base.actual('family'), -px(size * 96 / 72 * 1.15),
                'bold' if bold else 'normal')
    window.configure(bg='#f1f5f9')
    x, y, available_width, available_height = available_area(window)
    # Leave room for window decorations even when no work area is advertised.
    width = min(px(1100), max(1, available_width - px(40)))
    height = min(px(750), max(1, available_height - px(64)))
    window.geometry(f'{width}x{height}+{x + (available_width - width) // 2}+{y + (available_height - height) // 2}')
    window.minsize(min(px(360), width), min(px(300), height))
    window.maxsize(width=max(1, available_width - px(16)), height=max(1, available_height - px(48)))
    viewport = tk.Canvas(window, bg='#f1f5f9', highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient='vertical', command=viewport.yview)
    scrollbar.pack(side='right', fill='y')
    viewport.pack(side='left', fill='both', expand=True)
    viewport.configure(yscrollcommand=scrollbar.set)
    content = tk.Frame(viewport, bg='#f1f5f9')
    content_id = viewport.create_window(0, 0, window=content, anchor='nw')
    def sync_content(event=None):
        viewport.itemconfigure(content_id, height=max(
            viewport.winfo_height(), content.winfo_reqheight()))
        viewport.configure(scrollregion=viewport.bbox('all'))
    content.bind('<Configure>', sync_content)
    def scroll(event):
        viewport.yview_scroll(-1 if event.num == 4 or event.delta > 0 else 1, 'units')
    for event in ('<Button-4>', '<Button-5>', '<MouseWheel>'):
        window.bind(event, scroll)
    header = tk.Frame(content, bg='#191d2d', padx=px(26), pady=px(20))
    header.pack(fill='x')
    logo = tk.PhotoImage(file=str(LOGO))
    window.iconphoto(True, logo)
    # Use the larger bundled raster at integral HiDPI scales.
    logo_display = logo.zoom(max(1, round(scale)))
    logo_label = tk.Label(header, image=logo_display, bg='#191d2d')
    logo_label.pack(side='left', padx=(0, px(24)))
    words = tk.Frame(header, bg='#191d2d')
    words.pack(side='left', fill='both', expand=True)
    tk.Label(words, wraplength=1, justify='left', text='Conversor de medios', font=font(24, True), fg='white', bg='#191d2d', anchor='w').pack(fill='x', pady=(px(12), px(6)))
    tk.Label(words, wraplength=1, justify='left', text='Conversor de medios para Linux', font=font(12), fg='#bfc9e2', bg='#191d2d', anchor='w').pack(fill='x')
    tk.Label(content, wraplength=1, justify='center', text='¿Qué quieres preparar?', font=font(18, True), bg='#f1f5f9', fg='#172033').pack(pady=(px(18), px(12)))
    cards = tk.Frame(content, bg='#f1f5f9')
    cards.pack(fill='both', expand=True, padx=px(24))
    cards.columnconfigure((0, 1), weight=1, uniform='card')
    cards.rowconfigure(0, weight=1)

    def start(mode):
        try:
            subprocess.Popen(['bash', str(ENGINE)], env={**os.environ, 'CONVERSOR_DIRECCION': mode})
        except OSError as error:
            messagebox.showerror('No se pudo abrir el conversor', str(error), parent=window)
            return
        window.destroy()

    card_widgets = []
    for column, title, route, detail, color, mode in [
        (0, 'PARA EDITAR', 'MP4 → MOV', 'PCM · 24 bits · 48 kHz', '#2563eb', 'editar'),
        (1, 'PARA PUBLICAR', 'MOV → MP4', 'AAC · 256 kb/s · 48 kHz', '#7c3aed', 'publicar'),
    ]:
        card = tk.Frame(cards, bg='white', highlightbackground='#dce3ee', highlightthickness=1, padx=px(20), pady=px(16))
        card_widgets.append(card)
        card.grid(row=0, column=column, sticky='nsew', padx=(0, px(8)) if column == 0 else (8, 0))
        tk.Label(card, wraplength=1, justify='left', text=title, font=font(11, True), bg='white', fg=color).pack(anchor='w')
        tk.Label(card, wraplength=1, justify='left', text=route, font=font(25, True), bg='white', fg='#172033').pack(anchor='w', pady=(px(10), px(8)))
        tk.Label(card, wraplength=1, justify='left', text=detail, font=font(11), bg='white', fg='#475569').pack(anchor='w')
        tk.Button(card, text='Seleccionar vídeos', command=lambda m=mode: start(m), bg=color, fg='white', activebackground=color, activeforeground='white', font=font(12, True), relief='flat', padx=px(12), pady=px(10), cursor='hand2').pack(fill='x', pady=(px(18), 0))
    tk.Label(content, wraplength=1, justify='center', text='Vídeo sin recodificar · Comprobación de pistas y audio\nTus archivos originales se conservan', font=font(10), fg='#475569', bg='#f1f5f9').pack(pady=px(16))
    def resize(event):
        if event.widget is not viewport:
            return
        usable = max(1, event.width)
        # Measure text at the actual Tk/font scaling, rather than assuming pixels.
        button_width = max(card.winfo_children()[-1].winfo_reqwidth() for card in card_widgets)
        side_by_side = usable >= 2 * (button_width + px(42)) + px(64)
        for i, card in enumerate(card_widgets):
            card.grid_configure(row=0 if side_by_side else i,
                                column=i if side_by_side else 0,
                                padx=((0, px(8)) if i == 0 else (px(8), 0)) if side_by_side else 0,
                                pady=px(0) if side_by_side else (0, 12))
            card_width = (usable - px(64)) // 2 if side_by_side else usable - px(48)
            for label in card.winfo_children():
                if isinstance(label, (tk.Label, tk.Button)):
                    label.configure(wraplength=max(1, card_width - px(42)))
        cards.columnconfigure(0, uniform='card' if side_by_side else '')
        cards.columnconfigure(1, weight=1 if side_by_side else 0, minsize=0, uniform='card' if side_by_side else '')
        compact_header = usable < px(760)
        logo_label.pack_configure(side='top' if compact_header else 'left', padx=px(0) if compact_header else (0, 24))
        words.pack_configure(side='top' if compact_header else 'left')
        for label in words.winfo_children():
            label.configure(wraplength=max(1, usable - px(60) - (0 if compact_header else logo_display.width() + px(24))))
        for label in content.winfo_children():
            if isinstance(label, tk.Label):
                label.configure(wraplength=max(1, usable - px(48)))
        viewport.itemconfigure(content_id, width=usable)
        # Let geometry settle without re-entering the Configure handler.
        viewport.after_idle(lambda: viewport.itemconfigure(
            content_id, height=max(viewport.winfo_height(), content.winfo_reqheight())))
    viewport.bind('<Configure>', resize)
    window.mainloop()


if __name__ == '__main__':
    main()
