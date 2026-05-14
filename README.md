# EtchOS
Python Based Terminal Operating System

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
7. Download the latest EtchOS release.
8. Navigate to directory
9. Start EtchOS with python main.py
10. Have fun!

**Latest Version**
The Latest Fully Working and tested Version is 3.8.1 Final.
It includes the Latest Features and Functions.

**Latest Preview**
The Latest Preview is 4.0.0. 
It is still in Development and doesent contain:
- Logs
- Onboarding
This Version is faster then the 3. Version because all the programs are seperated into individual files. It aims to deliver a cleaner and faster experiance for the users as well as the devs. Its build for modularity
and easy installing of new apps. Still in work.

**Naming Scheme**
First Number - Big Updates
Secound Number - Little Updates that get released individual
Third Number - State of Development:
.0 - Missing features and some bugs
.1 - Tested or in Testing
Final - Release Vesion
