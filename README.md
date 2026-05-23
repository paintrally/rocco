# Rocco USB Creator

A small Windows USB flashing tool inspired by Rufus, built with Python + Tkinter.

Rocco was originally started as a learning project to understand how bootable USB creators actually work behind the scenes - formatting drives, mounting ISOs, copying boot files, handling threads safely in Tkinter, and generally trying not to destroy somebody’s USB stick.

It’s lightweight, simple, slightly chaotic, and surprisingly functional.

# Features
Simple desktop GUI
Detects removable USB drives
ISO file picker
Formats USB drives automatically
Mounts ISOs using PowerShell
Copies installation media to USB
Live progress updates
Multithreaded (UI doesn't freeze)
Windows focused
Built entirely in Python

# Why I Made This

I wanted to build something that felt like a real desktop utility instead of another tiny terminal script.

Rufus has always been one of those tools that feels deceptively simple until you realise how much engineering is hiding underneath it. This project started as a UI experiment and slowly turned into a proper bootable USB creator.

It also became a good excuse to learn:

Tkinter threading
Windows disk utilities
PowerShell integration
subprocess handling
safe-ish drive formatting
GUI state management
why bootloaders are pain
Requirements
Windows 10 / 11
Python 3.10+
Administrator privileges
Installation

# Clone the repo:

git clone https://github.com/yourname/rocco-usb-creator.git
cd rocco-usb-creator

# Run it:

python rocco.py

# !Important Warning!

# This tool formats USB drives.

# Seriously.

# Double check the selected drive before pressing START.

# I am not responsible if you accidentally nuke:

your backup drive
your external SSD
your homework
your operating system
your entire will to live
How It Works

# Very simplified process:

Detect removable drives
Ask user for ISO
Format USB using diskpart
Mount ISO using PowerShell
Copy files using robocopy
Unmount ISO
Hope everything worked
Current Limitations

# This is still a work in progress.

# Things that are not fully solved yet:

Large Windows ISOs over FAT32 limits
Full BIOS/UEFI compatibility
Secure Boot edge cases
Hybrid Linux ISO handling
Proper boot sector installation
Real transfer speed calculation
Drive safety protections
Localization
Logging system
Planned Features
Better modern UI
Dark mode polish
Real flashing progress
SHA256 verification
Drag & drop ISO support
Persistent Linux storage
Ventoy-style multiboot
Portable .exe builds
Automatic update checker
Safer drive detection
Custom themes
Animated startup screen
Built With
Python
Tkinter
PowerShell
diskpart
robocopy
caffeine

# Credits

Inspired heavily by Rufus by Pete Batard.

Massive respect for the amount of engineering behind the real thing.
