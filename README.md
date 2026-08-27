# EtchOS
Python Based Terminal Operating System with only Keyboard Support for slow hardware. Only needs python and curses to work

**History**

This is an little project i worked in my coding class for. It took multiple months and is my first big python project. I built it as an base for easy adding and removing features of your liking. Every release contains an test.py file to develop functions first and then add into main.py. The UI is made with the libary curses and is made using the safe_addstr() function and the window() functions i made. Hope u have fun!

**How to install**

1. Download Terminal-Based Linux Distro iso-Image (raspberry pi os lite, tiny core, ...)
2. Download and start Etcher (for raspi, raspberry pi for others balena etcher or rufus)
3. Select Storage device, for raspi, sd card else usb thumbdrive
4. Select Image (.iso file)
5. Flash and click through menu
6. Plug sd card into raspi for others do:
    1. Plug Drive in and start into BIOS
    2. Choose USB Drive as boot directory
    3. Restart
    4. Follow setup, for arch do ’archinstall’
    5. Restart and plug usb out
7. Download the latest EtchOS release and curses libary
8. Navigate to directory
9. Start EtchOS with python main.py
10. Have fun!

**Latest Version**

The Latest Fully Working and tested Version is 4.2.0.
It includes the Latest Features and Functions.

**What's new in 4.2.0**

- **Window Manager**: launch multiple apps at once and run them side by side
  - `Tab` — switch between running apps
  - `Q` — quit the focused app
  - `Enter`/`Space` — bring the focused app to the foreground
  - `Esc` — return to the main menu
- **Spreadsheet app**: edit CSV files directly in the terminal
- **File Manager cross-app opening**: opens files in the right editor based on file extension (e.g. `.txt` in the Text Editor, `.csv` in the Spreadsheet)
- Apps run as separate processes in the background, keeping the main menu responsive for true multitasking
- Full curses-based UI with multi-language support (English, Deutsch, Français)

**Version History**

- 4.2.0 — Window manager, Spreadsheet app, File Manager cross-app opening, background app multitasking
- 4.1.0 — Apps split into individual files (modular), Logs, Onboarding, Log In and Log Out, improved performance

Older versions (4.1.0 and below) are faster to start because each program now lives in its own file, built for modularity and easy installing of new apps.

**Naming Scheme**

First Number - Big Updates
Secound Number - Little Updates that get released individual
Third Number - State of Development:
.0 - Missing features and some bugs
.1 - Tested or in Testing
Final - Release Vesion
