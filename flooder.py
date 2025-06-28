import os
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
from pynput import keyboard
import sys

running = True

def get_usb_path():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def spawn_image_window(image_path):
    def show():
        try:
            root = tk.Tk()
            root.title("💥 Flooded 💥")
            img = Image.open(image_path).resize((600, 400))
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(root, image=tk_img)
            label.image = tk_img
            label.pack()
            root.attributes('-topmost', True)
            root.geometry(f"+{os.urandom(1)[0]*10}+{os.urandom(1)[0]*10}")  # scatter position
            root.mainloop()
        except:
            pass
    threading.Thread(target=show, daemon=True).start()

def flood_screen():
    image_folder = os.path.join(get_usb_path(), "images")
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    while running:
        for img_path in images:
            if not running:
                break
            spawn_image_window(img_path)
            time.sleep(0.01)  # Rapid spawn

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        print("[*] ESC pressed. Halting new spawns.")
        running = False
        return False

def main():
    print("[*] Spawning endless images. ESC to stop new spawns.")
    threading.Thread(target=flood_screen, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    main()
