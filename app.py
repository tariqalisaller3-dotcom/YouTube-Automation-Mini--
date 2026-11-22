
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import imageio_ffmpeg

video_path = ""

def select_video():
    global video_path
    video_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.mov *.mkv *.avi")]
    )
    if video_path:
        selected.config(text=os.path.basename(video_path))

def edit_video():
    if not video_path:
        messagebox.showwarning("Select Video", "Please select a video first.")
        return

    output = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 Video", "*.mp4")],
        initialfile="edited_video.mp4"
    )
    if not output:
        return

    start_button.config(state="disabled")
    status.config(text="Editing video... Please wait.")

    def process():
        try:
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
            command = [
                ffmpeg, "-y", "-i", video_path,
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,fps=30",
                "-c:v", "libx264", "-preset", "ultrafast",
                "-crf", "23", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart", output
            ]
            subprocess.run(command, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            root.after(0, lambda: status.config(text="Editing complete!"))
            root.after(0, lambda: messagebox.showinfo(
                "Success", "Your edited video has been saved!"
            ))
        except Exception as e:
            root.after(0, lambda: status.config(text="Editing failed."))
            root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            root.after(0, lambda: start_button.config(state="normal"))

    threading.Thread(target=process, daemon=True).start()

root = tk.Tk()
root.title("YouTube Automation Mini")
root.geometry("430x300")
root.resizable(False, False)

tk.Label(root, text="YouTube Automation Mini",
         font=("Arial", 18, "bold")).pack(pady=20)

tk.Button(root, text="Select Video", command=select_video,
          width=22).pack(pady=8)

selected = tk.Label(root, text="No video selected")
selected.pack(pady=5)

start_button = tk.Button(root, text="AUTO EDIT VIDEO",
                         command=edit_video, width=22,
                         bg="#16834a", fg="white")
start_button.pack(pady=18)

status = tk.Label(root, text="Ready", fg="blue")
status.pack(pady=10)

tk.Label(root, text="Automatic vertical 1080p export",
         font=("Arial", 9)).pack(pady=5)

root.mainloop()
