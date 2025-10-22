# terminal: pip install pyautogui pillow

import pyautogui as pag
import tkinter as tk

# ----- Tk window -----
root = tk.Tk()
root.title("Pixel Color")
root.attributes("-topmost", True)   # keep on top
root.resizable(False, False)

color_swatch = tk.Canvas(root, width=80, height=80, highlightthickness=1, highlightbackground="#888")
color_swatch.grid(row=0, column=0, rowspan=3, padx=8, pady=8)

txt = tk.StringVar(value="Move the mouse…")
label = tk.Label(root, textvariable=txt, font=("Consolas", 11))
label.grid(row=0, column=1, sticky="w", padx=(0, 8), pady=(10, 0))

hint = tk.Label(root, text="Press Q to quit • Click swatch to copy HEX", fg="#666")
hint.grid(row=2, column=1, sticky="w", padx=(0, 8), pady=(0, 8))

def to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

def copy_hex(event=None):
    root.clipboard_clear()
    root.clipboard_append(current_hex[0])
    hint.config(text=f"Copied {current_hex[0]} to clipboard")

current_hex = ["#000000"]

def update():
    # current mouse position
    x, y = pag.position()

    # try fast per-pixel call; fall back to 1×1 screenshot if needed
    try:
        r, g, b = pag.pixel(x, y)
    except Exception:
        im = pag.screenshot(region=(x, y, 1, 1))
        r, g, b = im.getpixel((0, 0))

    hx = to_hex(r, g, b)
    current_hex[0] = hx

    # update UI
    color_swatch.delete("all")
    color_swatch.create_rectangle(0, 0, 80, 80, fill=hx, outline="")
    txt.set(f"Pos: ({x:4d}, {y:4d})  RGB: ({r:3d}, {g:3d}, {b:3d})  HEX: {hx}")

    root.after(50, update)  # ~20 FPS

def on_key(event):
    if event.char.lower() == "q":
        root.destroy()

color_swatch.bind("<Button-1>", copy_hex)
root.bind("<Key>", on_key)

update()
root.mainloop()
