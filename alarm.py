import time
import datetime
import pygame
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog

# Initialize mixer
pygame.mixer.init()

# Play alarm sound
def play_alarm(sound_file):
    if not os.path.exists(sound_file):
        messagebox.showwarning("Sound Not Found", "Using default sound: a.mp3")
        sound_file = "a.mp3"
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Alarm thread logic
def set_alarm_thread(alarm_time, sound_file):
    while True:
        now = datetime.datetime.now().strftime("%I:%M:%S %p")
        if now == alarm_time:
            show_alarm_popup()
            play_alarm(sound_file)
            break
        time.sleep(1)

# Alarm popup
def show_alarm_popup():
    popup = tk.Toplevel(root)
    popup.title("⏰ Wake Up!")
    popup.geometry("300x200")
    popup.configure(bg="#121212")
    popup.attributes("-topmost", True)
    tk.Label(popup, text="⏰", font=("Segoe UI", 48), fg="#BB86FC", bg="#121212").pack(pady=10)
    tk.Label(popup, text="Wake up, Nasa!", font=("Segoe UI", 16), fg="white", bg="#121212").pack()
    tk.Label(popup, text="It's time to start your day!", fg="#B3B3B3", bg="#121212").pack(pady=5)
    tk.Button(popup, text="DISMISS", command=popup.destroy, bg="#BB86FC", fg="white",
              font=("Segoe UI", 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=20)

# Validate time format
def is_valid_time(t):
    try:
        datetime.datetime.strptime(t, "%I:%M:%S %p")
        return True
    except ValueError:
        return False

# Set alarm button callback
def set_alarm():
    alarm_time = f"{time_entry.get().strip()} {ampm.get()}"
    sound_file = sound_path.get().strip()

    if not is_valid_time(alarm_time):
        messagebox.showerror("Invalid Time", "Enter time as HH:MM:SS AM/PM")
        return

    if sound_file == "" or sound_file == "Default":
        sound_file = "a.mp3"

    threading.Thread(target=set_alarm_thread, args=(alarm_time, sound_file), daemon=True).start()
    status_label.config(text=f"🔔 Alarm set for {alarm_time}", fg="#4CAF50")

# Browse sound
def browse_sound():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file:
        sound_path.set(file)
        sound_display.config(text=f"🎵 {os.path.basename(file)}", fg="#03DAC6")

# Focus placeholder behavior
def on_focus_in(event):
    if time_entry.get() == "HH:MM:SS AM/PM":
        time_entry.delete(0, tk.END)
        time_entry.config(fg="white")

def on_focus_out(event):
    if time_entry.get() == "":
        time_entry.insert(0, "HH:MM:SS AM/PM")
        time_entry.config(fg="#757575")

# Update current clock
def update_time():
    now = datetime.datetime.now()
    time_label.config(text=now.strftime("%I:%M:%S %p"))
    date_label.config(text=now.strftime("%A, %B %d"))
    root.after(1000, update_time)

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("Alarm Clock by Nasa")
root.geometry("400x600")
root.configure(bg="#121212")
root.resizable(False, False)

tk.Label(root, text="Clock ⏰", font=("Segoe UI", 20, "bold"), fg="white", bg="#121212").pack(pady=10)

# Time display
time_label = tk.Label(root, font=("Segoe UI", 44, "bold"), fg="white", bg="#121212")
time_label.pack()
date_label = tk.Label(root, font=("Segoe UI", 14), fg="#B3B3B3", bg="#121212")
date_label.pack(pady=(0, 20))
update_time()

# Alarm time input
tk.Label(root, text="Alarm Time (HH:MM:SS AM/PM)", font=("Segoe UI", 12), fg="#B3B3B3", bg="#121212").pack()
time_frame = tk.Frame(root, bg="#121212")
time_frame.pack(pady=10)

time_entry = tk.Entry(time_frame, font=("Segoe UI", 16), width=15, justify="center",
                      bg="#1E1E1E", fg="#757575", relief="flat")
time_entry.insert(0, " ")
time_entry.pack(side="left", ipady=10, ipadx=10)

ampm = ttk.Combobox(time_frame, values=["AM", "PM"], width=5, font=("Segoe UI", 12))
ampm.set("AM")
ampm.pack(side="left", padx=5)
time_entry.bind("<FocusIn>", on_focus_in)
time_entry.bind("<FocusOut>", on_focus_out)
time_entry.pack(pady=10, ipady=10, ipadx=10)

# Sound selector
sound_path = tk.StringVar()
tk.Button(root, text="🎵 Choose Alarm Sound", command=browse_sound,
          bg="#2C2C2C", fg="#03DAC6", font=("Segoe UI", 11), relief="flat",
          padx=10, pady=8).pack(pady=5)
sound_display = tk.Label(root, text="", fg="#757575", bg="#121212", font=("Segoe UI", 10))
sound_display.pack()

# SET ALARM button
tk.Button(root, text="SET ALARM", command=set_alarm, font=("Segoe UI", 14, "bold"),
          bg="#BB86FC", fg="white", relief="flat", padx=20, pady=10).pack(pady=30)

# Status
status_label = tk.Label(root, text="No alarm set", font=("Segoe UI", 12), fg="#757575", bg="#121212")
status_label.pack()

root.mainloop()
