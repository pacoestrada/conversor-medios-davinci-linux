#!/usr/bin/env python3
"""Pantalla inicial; el motor Bash conserva la conversión y sus verificaciones."""
import os
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import messagebox
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
    return area


def main():
    window = tk.Tk()
    window.title('Conversor de medios · 2.3.1')
    window.configure(bg='#f1f5f9')
    x, y, available_width, available_height = available_area(window)
    # Leave room for window decorations even when no work area is advertised.
    width = min(1100, max(1, available_width - 40))
    height = min(750, max(1, available_height - 64))
    window.geometry(f'{width}x{height}+{x + (available_width - width) // 2}+{y + (available_height - height) // 2}')
    window.minsize(min(360, width), min(300, height))
    window.maxsize(width=max(1, available_width - 16), height=max(1, available_height - 48))
    viewport = tk.Canvas(window, bg='#f1f5f9', highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient='vertical', command=viewport.yview)
    scrollbar.pack(side='right', fill='y')
    viewport.pack(side='left', fill='both', expand=True)
    viewport.configure(yscrollcommand=scrollbar.set)
    content = tk.Frame(viewport, bg='#f1f5f9')
    content_id = viewport.create_window(0, 0, window=content, anchor='nw')
    content.bind('<Configure>', lambda event: viewport.configure(scrollregion=viewport.bbox('all')))
    def scroll(event):
        viewport.yview_scroll(-1 if event.num == 4 or event.delta > 0 else 1, 'units')
    for event in ('<Button-4>', '<Button-5>', '<MouseWheel>'):
        window.bind(event, scroll)
    header = tk.Frame(content, bg='#191d2d', padx=26, pady=20)
    header.pack(fill='x')
    logo = tk.PhotoImage(file=str(LOGO))
    window.iconphoto(True, logo)
    logo_label = tk.Label(header, image=logo, bg='#191d2d')
    logo_label.pack(side='left', padx=(0, 24))
    words = tk.Frame(header, bg='#191d2d')
    words.pack(side='left', fill='both', expand=True)
    tk.Label(words, wraplength=1, justify='left', text='Conversor de medios', font=('Sans', 24, 'bold'), fg='white', bg='#191d2d', anchor='w').pack(fill='x', pady=(12, 6))
    tk.Label(words, wraplength=1, justify='left', text='Conversor de medios para Linux', font=('Sans', 12), fg='#bfc9e2', bg='#191d2d', anchor='w').pack(fill='x')
    tk.Label(content, wraplength=1, justify='center', text='¿Qué quieres preparar?', font=('Sans', 18, 'bold'), bg='#f1f5f9', fg='#172033').pack(pady=(18, 12))
    cards = tk.Frame(content, bg='#f1f5f9')
    cards.pack(fill='both', expand=True, padx=24)
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
        card = tk.Frame(cards, bg='white', highlightbackground='#dce3ee', highlightthickness=1, padx=20, pady=16)
        card_widgets.append(card)
        card.grid(row=0, column=column, sticky='nsew', padx=(0, 8) if column == 0 else (8, 0))
        tk.Label(card, wraplength=1, justify='left', text=title, font=('Sans', 11, 'bold'), bg='white', fg=color).pack(anchor='w')
        tk.Label(card, wraplength=1, justify='left', text=route, font=('Sans', 25, 'bold'), bg='white', fg='#172033').pack(anchor='w', pady=(10, 8))
        tk.Label(card, wraplength=1, justify='left', text=detail, font=('Sans', 11), bg='white', fg='#475569').pack(anchor='w')
        tk.Button(card, text='Seleccionar vídeos', command=lambda m=mode: start(m), bg=color, fg='white', activebackground=color, activeforeground='white', font=('Sans', 12, 'bold'), relief='flat', padx=12, pady=10, cursor='hand2').pack(fill='x', pady=(18, 0))
    tk.Label(content, wraplength=1, justify='center', text='Vídeo sin recodificar · Comprobación de pistas y audio\nTus archivos originales se conservan', font=('Sans', 10), fg='#475569', bg='#f1f5f9').pack(pady=16)
    def resize(event):
        if event.widget is not viewport:
            return
        usable = max(1, event.width)
        # Measure text at the actual Tk/font scaling, rather than assuming pixels.
        button_width = max(card.winfo_children()[-1].winfo_reqwidth() for card in card_widgets)
        side_by_side = usable >= 2 * (button_width + 42) + 64
        for i, card in enumerate(card_widgets):
            card.grid_configure(row=0 if side_by_side else i,
                                column=i if side_by_side else 0,
                                padx=((0, 8) if i == 0 else (8, 0)) if side_by_side else 0,
                                pady=0 if side_by_side else (0, 12))
            card_width = (usable - 64) // 2 if side_by_side else usable - 48
            for label in card.winfo_children():
                if isinstance(label, tk.Label):
                    label.configure(wraplength=max(1, card_width - 42))
        cards.columnconfigure(0, uniform='card' if side_by_side else '')
        cards.columnconfigure(1, weight=1 if side_by_side else 0, minsize=0, uniform='card' if side_by_side else '')
        compact_header = usable < 760
        logo_label.pack_configure(side='top' if compact_header else 'left', padx=0 if compact_header else (0, 24))
        words.pack_configure(side='top' if compact_header else 'left')
        for label in words.winfo_children():
            label.configure(wraplength=max(1, usable - 60 - (0 if compact_header else logo.width() + 24)))
        for label in content.winfo_children():
            if isinstance(label, tk.Label):
                label.configure(wraplength=max(1, usable - 48))
        viewport.itemconfigure(content_id, width=usable)
        content.update_idletasks()
        viewport.itemconfigure(content_id, height=max(event.height, content.winfo_reqheight()))
    viewport.bind('<Configure>', resize)
    window.mainloop()


if __name__ == '__main__':
    main()
