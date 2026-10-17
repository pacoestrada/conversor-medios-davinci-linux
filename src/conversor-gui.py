#!/usr/bin/env python3
"""Pantalla inicial; el motor Bash conserva la conversión y sus verificaciones."""
import os
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import messagebox

ROOT = Path(__file__).resolve().parent.parent
INSTALLED = Path('/usr/lib/conversor-medios/conversor-medios')
ENGINE = INSTALLED if INSTALLED.exists() else ROOT / 'src/conversor-medios'
LOGO = (Path('/usr/share/icons/hicolor/128x128/apps/com.pacoestrada.ConversorMp4Mov.png')
        if INSTALLED.exists() else ROOT / 'data/icons/128x128/com.pacoestrada.ConversorMp4Mov.png')


def main():
    window = tk.Tk()
    window.title('Conversor de medios · Compilando Podcast · 2.3.0')
    window.configure(bg='#f1f5f9')
    window.geometry('780x520')
    window.minsize(740, 520)
    header = tk.Frame(window, bg='#191d2d', padx=26, pady=20)
    header.pack(fill='x')
    logo = tk.PhotoImage(file=str(LOGO))
    window.iconphoto(True, logo)
    tk.Label(header, image=logo, bg='#191d2d').pack(side='left', padx=(0, 24))
    words = tk.Frame(header, bg='#191d2d')
    words.pack(side='left', fill='both', expand=True)
    tk.Label(words, text='Conversor de medios', font=('Sans', 24, 'bold'), fg='white', bg='#191d2d', anchor='w').pack(fill='x', pady=(12, 6))
    tk.Label(words, text='Compilando Podcast · Paco Estrada', font=('Sans', 12), fg='#bfc9e2', bg='#191d2d', anchor='w').pack(fill='x')
    tk.Label(window, text='¿Qué quieres preparar?', font=('Sans', 18, 'bold'), bg='#f1f5f9', fg='#172033').pack(pady=(18, 12))
    cards = tk.Frame(window, bg='#f1f5f9')
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

    for column, title, route, detail, color, mode in [
        (0, 'PARA EDITAR', 'MP4 → MOV', 'PCM · 24 bits · 48 kHz', '#2563eb', 'editar'),
        (1, 'PARA PUBLICAR', 'MOV → MP4', 'AAC · 256 kb/s · 48 kHz', '#7c3aed', 'publicar'),
    ]:
        card = tk.Frame(cards, bg='white', highlightbackground='#dce3ee', highlightthickness=1, padx=20, pady=16)
        card.grid(row=0, column=column, sticky='nsew', padx=(0, 8) if column == 0 else (8, 0))
        tk.Label(card, text=title, font=('Sans', 11, 'bold'), bg='white', fg=color).pack(anchor='w')
        tk.Label(card, text=route, font=('Sans', 25, 'bold'), bg='white', fg='#172033').pack(anchor='w', pady=(10, 8))
        tk.Label(card, text=detail, font=('Sans', 11), bg='white', fg='#475569').pack(anchor='w')
        tk.Button(card, text='Seleccionar vídeos', command=lambda m=mode: start(m), bg=color, fg='white', activebackground=color, activeforeground='white', font=('Sans', 12, 'bold'), relief='flat', padx=12, pady=10, cursor='hand2').pack(fill='x', pady=(18, 0))
    tk.Label(window, text='Vídeo sin recodificar · Comprobación de pistas y audio\nTus archivos originales se conservan', font=('Sans', 10), fg='#475569', bg='#f1f5f9').pack(pady=16)
    window.mainloop()


if __name__ == '__main__':
    main()
