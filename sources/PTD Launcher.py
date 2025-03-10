import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import subprocess
import time
import pygetwindow as gw
import ctypes
import webbrowser

def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

def reproducir_sonido(archivo):
    pygame.mixer.music.load(get_resource_path(archivo))
    pygame.mixer.music.play()

def abrir_sitio(url):
    reproducir_sonido("Closetab.mp3")
    webbrowser.open(url)

def abrir_flash(swf, nombre):
    reproducir_sonido("Mewtab.mp3")
    subprocess.Popen([get_resource_path("flashplayer11_5r502_146_win_sa_debug.exe"), get_resource_path(swf)])
    time.sleep(1.5)
    hicon = ctypes.windll.user32.LoadImageW(None, get_resource_path("2.ico"), 1, 16, 16, 0x10)
    hicon2 = ctypes.windll.user32.LoadImageW(None, get_resource_path("2.ico"), 1, 48, 48, 0x10)
    for ventana in gw.getWindowsWithTitle("Adobe Flash Player 11"):
        hwnd = ventana._hWnd
        ctypes.windll.user32.SetWindowTextW(hwnd, nombre)
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, hicon2)
        hMenu = ctypes.windll.user32.GetMenu(hwnd)
        if hMenu:
            menu_item_count = ctypes.windll.user32.GetMenuItemCount(hMenu)
            for _ in range(menu_item_count):
                ctypes.windll.user32.DeleteMenu(hMenu, 0, 0x00000400)
            ctypes.windll.user32.DrawMenuBar(hwnd)

def abrir_github(event):
    webbrowser.open("https://github.com/tivp")

pygame.mixer.init()

root = tk.Tk()
root.title("PTD Launcher")
root.iconbitmap(get_resource_path("1.ico"))
root.configure(bg="#e5e5e5")
root.geometry("490x335")
root.resizable(False, False)
reproducir_sonido("on.mp3")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 490
window_height = 335
position_top = int((screen_height - window_height) / 2)
position_right = int((screen_width - window_width) / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

ttk.Style().configure("Main.TFrame", background="#e5e5e5")

banner_img = ImageTk.PhotoImage(Image.open(get_resource_path("Banner.png")).resize((500, 127), Image.Resampling.LANCZOS))
banner_label = tk.Label(root, image=banner_img, bg="#e5e5e5", bd=0, highlightthickness=0)
banner_label.pack()

def crear_boton(frame, etiqueta, accion, color, hover_color):
    btn = tk.Button(
        frame, text=etiqueta, bg=color, fg="white",
        font=("Arial", 10), relief="flat", borderwidth=0,
        padx=9, pady=3,
        command=accion,
        activebackground=color, activeforeground="white"
    )
    btn.pack(side=tk.LEFT, padx=10, pady=8)
    btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
    btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

botones_grupos = [
    (["PTD 1 PokéCenter", "PTD 2 PokéCenter", "PTD 3 PokéCenter"],
     [lambda: abrir_sitio("https://ptd.icu"), lambda: abrir_sitio("https://ptd.icu/ptd2/"), lambda: abrir_sitio("https://ptd.icu/ptd3/")],
     "#096c09", "#1a7f1d"),

    (["Play PTD 1", "Play PTD 2", "Play PTD 3"],
     [lambda: abrir_flash("PTD1-v2.9.4.swf", "PTD 1"), lambda: abrir_flash("PTD2-v3.5.4.swf", "PTD 2"), lambda: abrir_flash("PTD3-v1.2.1.swf", "PTD 3")],
     "#2a7ab7", "#2d73a9"),

    (["Play PTD 1 Regional Forms", "Play PTD 1 Hacked Version"],
     [lambda: abrir_flash("PTD1RF-v2.9.4.swf", "PTD 1 Regional Forms"), lambda: abrir_flash("PTD1_Hacked-v2.9.4.swf", "PTD 1 Hacked Version")],
     "#2a7ab7", "#2d73a9"),

    (["Play PTD 2 Hacked Version", "Play PTD 3 Hacked Version"],
     [lambda: abrir_flash("PTD2_Hacked-v3.5.4.swf", "PTD 2 Hacked Version"), lambda: abrir_flash("PTD3_Hacked-v1.2.1.swf", "PTD 3 Hacked Version")],
     "#2a7ab7", "#2d73a9")
]

grupo_principal = ttk.Frame(root, style="Main.TFrame")
grupo_principal.pack(pady=(14, 0))

for etiquetas, acciones, color, hover_color in botones_grupos:
    frame = ttk.Frame(grupo_principal, style="Main.TFrame")
    frame.pack()
    for i, etiqueta in enumerate(etiquetas):
        crear_boton(frame, etiqueta, acciones[i], color, hover_color)

signature = tk.Label(root, text="Fabricado por ", fg="#b0b0b0", bg="#e5e5e5")
signature.place(x=384, y=312)

signature_link = tk.Label(root, text="tivp", fg="#b0b0b0", cursor="hand2", bg="#e5e5e5")
signature_link.place(x=462, y=312)
signature_link.bind("<Enter>", lambda e: signature_link.config(fg="blue"))
signature_link.bind("<Leave>", lambda e: signature_link.config(fg="#b0b0b0"))
signature_link.bind("<Button-1>", abrir_github)

root.protocol("WM_DELETE_WINDOW", lambda: (reproducir_sonido("off.mp3"), root.after(500, root.destroy)))

root.mainloop()
