# importing libraries
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import tempfile
import shutil
import os
import string
import ctypes
from queue import Queue

# check if the python program was ran as administrator

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showerror(
        "Please re-run",
        "This program uses Diskpart, which requires admin elevation."
    )
    raise SystemExit

# check for drives connected

def get_usb_drives():
    drives = []

    bitmask = ctypes.windll.kernel32.GetLogicalDrives()

    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive = f"{letter}:\\"

            drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)

            # DRIVE_REMOVABLE = 2
            if drive_type == 2:
                drives.append(drive)

        bitmask >>= 1

    return drives

# tkinter window

root = tk.Tk()
root.title("Rocco Version 1")
root.geometry("600x400")
root.configure(bg="#2a538c")

# variables

iso_path = tk.StringVar()
selected_drive = tk.StringVar()
status_var = tk.StringVar(value="Ready")

progress_value = tk.IntVar(value=0)

queue = Queue()

# user interface

title = tk.Label(
    root,
    text="Rocco USB disk writing tool",
    font=("Consolas", 18, "bold"),
    bg="#2a538c",
    fg="white"
)
title.pack(pady=15)

# drive

drive_frame = tk.Frame(root, bg="#2a538c")
drive_frame.pack(fill="x", padx=20, pady=10)

tk.Label(
    drive_frame,
    text="USB Device:",
    bg="#2a538c",
    fg="white"
).pack(anchor="w")

drive_combo = ttk.Combobox(
    drive_frame,
    textvariable=selected_drive,
    state="readonly",
    values=get_usb_drives()
)

drive_combo.pack(fill="x")

if drive_combo["values"]:
    drive_combo.current(0)

# iso selection

iso_frame = tk.Frame(root, bg="#2a538c")
iso_frame.pack(fill="x", padx=20, pady=10)

tk.Label(
    iso_frame,
    text="Select the ISO Image:",
    bg="#2a538c",
    fg="white"
).pack(anchor="w")

iso_entry = tk.Entry(
    iso_frame,
    textvariable=iso_path
)
iso_entry.pack(side="left", fill="x", expand=True)

def browse_iso():
    file = filedialog.askopenfilename(
        filetypes=[("ISO Files", "*.iso")]
    )

    if file:
        iso_path.set(file)

browse_btn = tk.Button(
    iso_frame,
    text="Browse",
    command=browse_iso
)
browse_btn.pack(side="left", padx=5)

# progress bar

status_label = tk.Label(
    root,
    textvariable=status_var,
    bg="#2a538c",
    fg="lightgreen"
)
status_label.pack(pady=10)

progress = ttk.Progressbar(
    root,
    maximum=100,
    variable=progress_value
)
progress.pack(fill="x", padx=20)

# actual part

def update_ui():
    while not queue.empty():
        action, value = queue.get()

        if action == "status":
            status_var.set(value)

        elif action == "progress":
            progress_value.set(value)

        elif action == "done":
            messagebox.showinfo("Success", value)
            start_btn.config(state="normal")

        elif action == "error":
            messagebox.showerror("Error", value)
            start_btn.config(state="normal")

    root.after(100, update_ui)

def flash_usb():
    try:
        drive = selected_drive.get()
        iso = iso_path.get()

        if not drive:
            queue.put(("error", "Select a USB drive"))
            return

        if not iso or not os.path.exists(iso):
            queue.put(("error", "Select a valid ISO"))
            return

        drive_letter = drive[0]

# diskpart
        queue.put(("status", "Formatting USB..."))
        queue.put(("progress", 10))

        diskpart_script = f"""
select volume {drive_letter}
clean
create partition primary
format fs=fat32 quick
active
assign
"""

        script_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        )

        script_file.write(diskpart_script.encode())
        script_file.close()

        subprocess.run(
            ["diskpart", "/s", script_file.name],
            check=True
        )

        os.unlink(script_file.name)

# iso mount

        queue.put(("status", "Mounting ISO..."))
        queue.put(("progress", 30))

        ps_mount = f'''
$img = Mount-DiskImage -ImagePath "{iso}" -PassThru
($img | Get-Volume).DriveLetter
'''

        result = subprocess.check_output(
            ["powershell", "-Command", ps_mount]
        ).decode().strip()

        iso_drive = result + ":\\"

# file copying

        queue.put(("status", "Copying files..."))
        queue.put(("progress", 50))

        subprocess.run([
            "robocopy",
            iso_drive,
            drive,
            "/E"
        ], check=True)

# unmount the iso

        queue.put(("status", "Unmounting ISO..."))
        queue.put(("progress", 90))

        subprocess.run([
            "powershell",
            "-Command",
            f'Dismount-DiskImage -ImagePath "{iso}"'
        ])

        queue.put(("progress", 100))
        queue.put(("status", "Complete"))

        queue.put((
            "done",
            f"Bootable USB created successfully on {drive}"
        ))

    except subprocess.CalledProcessError as e:
        queue.put(("error", str(e)))

    except Exception as e:
        queue.put(("error", str(e)))

# start

def start_process():
    start_btn.config(state="disabled")

    thread = threading.Thread(target=flash_usb)
    thread.daemon = True
    thread.start()

start_btn = tk.Button(
    root,
    text="START",
    height=2,
    bg="#4CAF50",
    fg="white",
    command=start_process
)

start_btn.pack(pady=20)

# loop

root.after(100, update_ui)

root.mainloop()
