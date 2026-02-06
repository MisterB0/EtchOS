# Curses for terminal UI, time for delays, math for calculations, os for file system operations
import curses
from curses import wrapper
import time
import math 
import os 

# EtchOS 3.4 - Terminal User Interface Operating System

def main(stdscr):
    
    def window(height):
        # original simple fixed-position box
        safe_addstr(0, 0, "==========================================================")
        for i in range(1, height - 1):
            safe_addstr(i, 0, "│                                                        │")
        safe_addstr(height - 1, 0, "==========================================================")
        
    
    
    # Safe addstr function to prevent crashes when text exceeds window size
    def safe_addstr(y, x, text):
        max_y, max_x = stdscr.getmaxyx()
        if y < 0:
            y = 0
        if x < 0:
            x = 0
        if y >= max_y:
            y = max_y - 1
        if x >= max_x:
            return
        s = str(text)
        avail = max_x - x
        if len(s) > avail:
            s = s[:avail]
        try:
            stdscr.addstr(y, x, s)
        except curses.error:
            try:
                stdscr.addnstr(y, x, s, avail)
            except Exception:
                pass
            
    # Startup Screen (Change ASCII art as needed)
    def StartupScreen():
        stdscr.clear()
        safe_addstr(0, 0," _______  _______  _______  __   __  _______  _______ ")
        safe_addstr(1, 0,"|       ||       ||       ||  | |  ||       ||       |")
        safe_addstr(2, 0,"|    ___||_     _||       ||  |_|  ||   _   ||  _____|")
        safe_addstr(3, 0,"|   |___   |   |  |       ||       ||  | |  || |_____ ")
        safe_addstr(4, 0,"|    ___|  |   |  |      _||       ||  |_|  ||_____  |")
        safe_addstr(5, 0,"|   |___   |   |  |     |_ |   _   ||       | _____| |")
        safe_addstr(6, 0,"|_______|  |___|  |_______||__| |__||_______||_______|")
        safe_addstr(7, 18,"EtchOS 3.4 ")
        stdscr.refresh()
        time.sleep(2)
        # Continue to Oboarding
        Onboarding()
    
    # Onboarding Process (Language Selection and User Setup)
    def Onboarding():
        while True:
            stdscr.clear()
            safe_addstr(1, 0, "Welcome to EtchOS 3.3!")
            safe_addstr(3, 0, "We will now start the onboarding process.")
            safe_addstr(5, 0, "Press any key to continue...")
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
            safe_addstr(1, 0, "In what language would you like to use EtchOS?")
            safe_addstr(3, 0, "1. English")
            safe_addstr(4, 0, "2. Deutsch")
            safe_addstr(6, 0, "Please enter the number of your choice: ")
            stdscr.refresh()
            choice = stdscr.getch()
            if choice == ord('1'):
                UserSetup_En()
                break
            elif choice == ord('2'):
                UserSetup_De()
                break
            else:
                safe_addstr(8, 0, "Invalid choice. Please try again.")
                stdscr.refresh()
                time.sleep(2)
                continue
        
    
    # User Setup Functions for English and German (-:
    def UserSetup_En():
        stdscr.clear()
        safe_addstr(0, 0, "======================= User Setup =======================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ Please choose your username:                           │")
        safe_addstr(3, 0, "│                                                        │")
        safe_addstr(4, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        username = stdscr.getstr(2, 35, 20).decode('utf-8')
        curses.noecho()
        safe_addstr(4, 0, f"│ Welcome,                                               │")
        safe_addstr(4, 10, username)
        safe_addstr(5, 0, "│                                                        │")
        safe_addstr(6, 0, "│ Please choose your password:                           │")
        safe_addstr(7, 0, "│                                                        │")
        safe_addstr(8, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        password = stdscr.getstr(6, 35, 20).decode('utf-8')
        curses.noecho()
        safe_addstr(11, 0, "User setup complete!")
        safe_addstr(13, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        Menu_En()
    
    def UserSetup_De():
        stdscr.clear()
        safe_addstr(1, 0, "Account-Einrichtung")
        safe_addstr(3, 0, "Bitte wähle einen Benutzernamen: ")
        stdscr.refresh()
        curses.echo()
        username = stdscr.getstr(4, 0, 20).decode('utf-8')
        curses.noecho()
        safe_addstr(6, 0, f"Willkommen, {username}!")
        safe_addstr(8, 0, "Bitte wähle ein Passwort: ")
        stdscr.refresh()
        curses.echo()
        password = stdscr.getstr(9, 0, 20).decode('utf-8')
        curses.noecho()
        safe_addstr(11, 0, "Account-Einrichtung abgeschlossen!")
        safe_addstr(13, 0, "Drücke eine Taste zum Fortfahren...")
        stdscr.refresh()
        stdscr.getch()
    
    # ===========================================================================================================
    # Firstly only English Menu and Features implemented, translation and features for German to be added later
    # Main Menu and Features in English
    # Programm Ideas:
    # - File Manager
    # - Settings
    # - Calculator
    # - Notes
    # - Text Editor
    # - Tetris Game (Evtl. try with os writnig in another pytohn file and importing it here)
    # - Terminal (change all variables in main.py)
    # - Assistant [Help Centre] (Simple Chatbot) (Evtl. try with os writnig in another pytohn file and importing it here)
    # - Exit
    # ===========================================================================================================
    
    
    
    def Menu_En():
        stdscr.clear()
        safe_addstr(0, 0, "==================== EtchOS Main Menu ====================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ 1. Open File Manager                                   │")
        safe_addstr(3, 0, "│ 2. Open Settings                                       │")
        safe_addstr(4, 0, "│ 3. Exit                                                │")
        safe_addstr(5, 0, "│ 4. Help Centre                                         │")
        safe_addstr(6, 0, "│ Please enter the number of your choice:                │")
        safe_addstr(7, 0, "│                                                        │")
        safe_addstr(8, 0, "==========================================================")
        safe_addstr(10, 0, " ")
        stdscr.refresh()
        choice = stdscr.getch()
        if choice == ord('1'):
            FileManager_En()
        elif choice == ord('2'):
            Settings_En()
        elif choice == ord('3'):
            Exit_En()
        elif choice == ord('4'):
            HelpCentre_En()
        else:
            safe_addstr(9, 0, "Invalid choice. Please try again.")
            stdscr.refresh()
            time.sleep(2)
            Menu_En()
    
    def HelpCentre_En():
        """Display help article list and view selected article with scrolling.
        Article content is shown one line lower (content_offset = 1).
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # draw help box and populate entries; keep content inside box
        stdscr.clear()
        height = 10
        window(height)
        base_y = 0
        content_x = 2
        safe_addstr(base_y + 1, content_x, "Help Centre")
        safe_addstr(base_y + 3, content_x, "Articles:")
        safe_addstr(base_y + 4, content_x + 2, "1. Getting Started")
        safe_addstr(base_y + 5, content_x + 2, "2. Troubleshooting")
        safe_addstr(base_y + 6, content_x + 2, "3. Update Instructions and Nodes")
        safe_addstr(8, 2, "Choose an article by number (or any other key to return).")
        stdscr.refresh()

        choice = stdscr.getch()
        if choice == ord('1'):
            file_path = os.path.join(current_dir, "Wiki", "Article 1.txt")
        elif choice == ord('2'):
            file_path = os.path.join(current_dir, "Wiki", "Article 2.txt")
        elif choice == ord('3'):
            file_path = os.path.join(current_dir, "Wiki", "Article 3.txt")
        else:
            # return to menu if no valid selection
            return

        # try to open and display the article if present
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            safe_addstr(9, 2, "Article not found. Press any key to return.")
            stdscr.refresh()
            stdscr.getch()
            return

        # prepare lines and scrolling parameters
        lines = content.splitlines()
        top = 0
        term_h, term_w = stdscr.getmaxyx()
        # reserve room for borders/instructions; ensure at least 1 row for content
        max_rows = max(1, term_h - 6)
        content_offset = 1  # move displayed article down by one line

        while True:
            stdscr.clear()
            # draw window tall enough for visible rows (+borders)
            box_h = min(max_rows + 3, term_h - 1)
            window(box_h)

            # draw visible lines inside the box, shifted down by content_offset
            for i in range(max_rows):
                idx = top + i
                if idx >= len(lines):
                    break
                safe_addstr(i + content_offset, 1, lines[idx])

            # instruction line
            safe_addstr(content_offset + max_rows, 0, "-- Press Up/Down or k/j to scroll, q or Esc to return --")
            stdscr.refresh()

            key = stdscr.getch()
            if key in (ord('q'), 27):
                # return to menu
                Menu_En()
                return
            elif key in (curses.KEY_DOWN, ord('j')):
                if top + max_rows < len(lines):
                    top += 1
            elif key in (curses.KEY_UP, ord('k')):
                if top > 0:
                    top -= 1
            elif key in (curses.KEY_NPAGE,):
                # page down
                top = min(len(lines) - max_rows, top + max_rows)
            elif key in (curses.KEY_PPAGE,):
                # page up
                top = max(0, top - max_rows)
    
    
    
    def FileManager_En():
        current_path = os.getcwd()
        selected = 0
        start_index = 0

        try:
            curses.curs_set(0)
        except Exception:
            pass
        stdscr.keypad(True)

        while True:
            stdscr.clear()

            try:
                items = os.listdir(current_path)
            except PermissionError:
                items = []
                safe_addstr(5, 2, "Permission denied")

            items.sort()

            term_h, term_w = stdscr.getmaxyx()
            # reserve header/footer rows; compute desired height from number of items
            desired_height = max(8, len(items) + 6)
            # compute box height and draw it at its fixed position
            box_height = min(max(6, desired_height), max(6, term_h - 2))
            window(box_height)

            # compute available width for file display based on window width
            width = max(10, term_w - 4)
            content_x = 2
            inner_width = max(0, width - content_x)

            safe_addstr(1, content_x, "File Manager")
            safe_addstr(2, content_x, f"Path: {current_path}")
            safe_addstr(3, content_x, "Navigate with ↑ ↓ | Enter = open | Backspace = up | q = exit")

            max_items = max(0, box_height - 6)
            display_count = min(len(items) - start_index, max_items)

            if display_count <= 0:
                safe_addstr(4, 2, "(empty directory)")
                start_index = 0
                selected = 0
            else:
                # keep selected within visible range
                if selected < 0:
                    selected = 0
                if selected >= display_count:
                    selected = display_count - 1

                for i, item in enumerate(items[start_index:start_index + display_count]):
                    prefix = "> " if i == selected else "  "
                    full_path = os.path.join(current_path, item)

                    if os.path.isdir(full_path):
                        display = f"{prefix}[DIR] {item}"
                    else:
                        display = f"{prefix}      {item}"

                    # truncate display to fit inner box width
                    if len(display) > inner_width:
                        if inner_width > 1:
                            display = display[:inner_width - 1] + "…"
                        else:
                            display = display[:inner_width]

                    safe_addstr(4 + i, content_x, display)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP:
                if items:
                    if selected > 0:
                        selected -= 1
                    elif start_index > 0:
                        start_index -= 1

            elif key == curses.KEY_DOWN:
                if items:
                    if selected < display_count - 1:
                        selected += 1
                    elif start_index + display_count < len(items):
                        start_index += 1

            elif key in (curses.KEY_ENTER, 10, 13):
                if items:
                    idx = start_index + selected
                    if idx < len(items):
                        target = os.path.join(current_path, items[idx])
                        if os.path.isdir(target):
                            current_path = target
                            selected = 0
                            start_index = 0

            elif key in (curses.KEY_BACKSPACE, 127, 8):
                parent = os.path.dirname(current_path)
                if parent != current_path:
                    current_path = parent
                    selected = 0

            elif key == ord('q'):
                break

        stdscr.keypad(False)
        try:
            curses.curs_set(1)
        except Exception:
            pass
        Menu_En()

    

        
    def Settings_En():
        stdscr.clear()
        safe_addstr(1, 0, "Settings - (Feature Coming Soon!)")
        safe_addstr(3, 0, "Press any key to return to the main menu...")
        stdscr.refresh()
        stdscr.getch()
        Menu_En()
    
    
    
    #TODO: In linux, "sudo visudo", add "username ALL=(ALL) NOPASSWD: /sbin/poweroff" at the bottom to allow poweroff without password
    def Exit_En():
        stdscr.clear()
        window(5)
        # position message inside the box (fixed offsets as original)
        safe_addstr(2, 15, "Exiting EtchOS. Goodbye!")
        stdscr.refresh()
        time.sleep(2)
        os.system("sudo poweroff")
        
    
    
    StartupScreen()
    stdscr.refresh()
    stdscr.getch()
    

wrapper(main)