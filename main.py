# main.py
import core
import commands
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

def show_assistant_avatar():
    gif_path = r"C:\Users\ANKIT\Downloads\LIGHT (2).gif"
    avatar_size = 250
    border_width = 4
    border_color = (255,255,255,255)
    chroma_hex = "#00ff00"
    frame_delay = 60
    auto_close_ms = 5000

    root = tk.Tk()
    root.title("Light")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg=chroma_hex)
    try:
        root.wm_attributes("-transparentcolor", chroma_hex)
    except tk.TclError:
        pass

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = int((screen_w - avatar_size) / 2)
    y = int((screen_h - avatar_size) / 2)
    root.geometry(f"{avatar_size}x{avatar_size}+{x}+{y}")

    from PIL import Image
    gif = Image.open(gif_path)
    frames = []
    gif_w, gif_h = gif.size
    side = min(gif_w, gif_h)
    left = (gif_w - side) // 2
    top = (gif_h - side) // 2
    crop_box = (left, top, left + side, top + side)
    inner_size = avatar_size - 2 * border_width

    for i in range(getattr(gif, "n_frames", 1)):
        gif.seek(i)
        frame = gif.convert("RGBA").crop(crop_box)
        frame = frame.resize((inner_size, inner_size), Image.LANCZOS)
        mask = Image.new("L", (inner_size, inner_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,inner_size,inner_size), fill=255)
        circular_img = Image.new("RGBA", (inner_size, inner_size), (0,0,0,0))
        circular_img.paste(frame, (0,0), mask=mask)
        final_img = Image.new("RGBA", (avatar_size, avatar_size), (0,0,0,0))
        final_draw = ImageDraw.Draw(final_img)
        final_draw.ellipse((0,0,avatar_size-1,avatar_size-1), outline=border_color, width=border_width)
        final_img.paste(circular_img, (border_width, border_width), circular_img)
        frames.append(ImageTk.PhotoImage(final_img))

    label = tk.Label(root, bg=chroma_hex, borderwidth=0, highlightthickness=0)
    label.pack(expand=True, fill="both")
    def animate(idx=0):
        label.config(image=frames[idx])
        root.after(frame_delay, animate, (idx+1) % len(frames))
    animate()
    root.after(auto_close_ms, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    core.say("Hello sir, I am Light, your virtual assistant. How can I help you?")
    # show avatar once
    try:
        show_assistant_avatar()
    except Exception as e:
        print("Avatar error:", e)

    print("Light is now always listening. Say something...")
    while True:
        query = core.takeCommand()
        if not query:
            continue
        status = commands.handle_query(query)
        if status == "exit":
            break
