def screen_size(default=(1440, 900)):
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        root.update_idletasks()
        size = (root.winfo_screenwidth(), root.winfo_screenheight())
        root.destroy()
        return size
    except Exception:
        return default


def centered(window, screen_w, screen_h):
    width = int(window['width'])
    height = int(window['height'])
    return width, height, (screen_w - width) // 2, (screen_h - height) // 2

