# TODO: Change all Version Numbers to 3.8.1 after testing and new features!
# TODO: Add more comments throughout the code for clarity
# TODO: Implement German translations for all features (Do in final relese for HNU Project)
# More see Notion doc for ideas and tasks



# Curses for terminal UI, time for delays, math for calculations, os for file system operations
# ImportError handling for Windows users without curses installed
try:
    import curses
    from curses import wrapper
except ModuleNotFoundError:
    import sys
    if sys.platform.startswith("win"):
        print("Missing curses (_curses). On Windows, install the compatibility package into your environment:")
        print("    python -m pip install windows-curses")
    else:
        print("Missing curses module. Please install the required curses support for your platform.")
    sys.exit(1)
import time
import math 
import os 

current_version = "3.8.0"

# EtchOS 3.8.0 - Terminal User Interface Operating System

def main(stdscr):
    
    # Initialize colors
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

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
        os.chdir("Assets")
        with open("StartupScreenLogo.txt", "r", encoding="utf-8") as f:
            content = f.readlines()
        for idx, line in enumerate(content):
            safe_addstr(idx, 0, line.rstrip('\n'))
        stdscr.refresh()
        time.sleep(2)
        # Continue to Oboarding
        Onboarding()
    
    # Onboarding Process (Language Selection and User Setup)
    def Onboarding():
        while True:
            stdscr.clear()
            safe_addstr(1, 0, f"Welcome to EtchOS {current_version}!")
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
    #               more see Notion doc
    # ===========================================================================================================
    
    
    
    def Menu_En():
        stdscr.clear()
        safe_addstr(0, 0, "==================== EtchOS Main Menu ====================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ 1. File Manager                                        │")
        safe_addstr(3, 0, "│ 2. Settings                                            │")
        safe_addstr(4, 0, "│ 3. Exit                                                │")
        safe_addstr(5, 0, "│ 4. Help Centre                                         │")
        safe_addstr(6, 0, "│ 5. Calculator                                          │")
        safe_addstr(7, 0, "│ 6. EtchEditor                                          │")
        safe_addstr(8, 0, "│ 7. System Info                                         │")
        safe_addstr(9, 0, "│ 8. EtchShell                                           │") 
        safe_addstr(10, 0, "│ Please enter the number of your choice:                │")
        safe_addstr(11, 0, "│                                                        │")
        safe_addstr(12, 0, "==========================================================")
        safe_addstr(14, 0, " ")
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
        elif choice == ord('5'):
            Calculator_En()
        elif choice == ord('6'):
            TextEditor_En()
        elif choice == ord('7'):
            SystemInfo_En()
        elif choice == ord('8'):
            EtchShell_En()
        else:
            safe_addstr(10, 0, "Invalid choice. Please try again.")
            stdscr.refresh()
            time.sleep(2)
            Menu_En()
    
    
    
    def EtchShell_En():
        # Terminal with EtchShell Advanced functions; explanations to linux and windows cmd commands; auto complete feature
        height = 16
        output_buffer = ["EtchShell v1.0", "Type 'help' for commands."]
        current_input = ""

        # Command definitions
        commands = {
            "help": "Show this help",
            "clear": "Clear screen",
            "exit": "Exit terminal",
            "ls": "List files (Linux)",
            "dir": "List files (Windows)",
            "cd": "Change directory",
            "pwd": "Print working directory",
            "whoami": "Show current user",
            "explain": "Explain a command (e.g. 'explain ls')"
        }

        # Explanations for specific commands (cross-platform help)
        explanations = {
            "ls": "Lists directory contents. Equivalent to 'dir' in Windows.",
            "dir": "Lists directory contents. Equivalent to 'ls' in Linux.",
            "cd": "Changes the current working directory.",
            "pwd": "Prints the current working directory path.",
            "clear": "Clears the terminal screen. Equivalent to 'cls' in Windows.",
            "whoami": "Displays the current username.",
            "mkdir": "Creates a new directory.",
            "rm": "Removes a file."
        }

        while True:
            stdscr.clear()
            window(height)

            # Display output buffer (scroll)
            max_lines = height - 3
            visible_lines = output_buffer[-(max_lines-1):]

            for i, line in enumerate(visible_lines):
                safe_addstr(1 + i, 2, line)

            # Prompt
            user = os.getenv('USER') or os.getenv('USERNAME') or 'user'
            cwd = os.getcwd()
            if len(cwd) > 15: cwd = "..." + cwd[-12:]
            prompt = f"{user}@{cwd} $ {current_input}"
            safe_addstr(height - 2, 2, prompt)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (10, 13): # Enter
                output_buffer.append(f"$ {current_input}")
                parts = current_input.strip().split()
                if parts:
                    cmd = parts[0].lower()
                    args = parts[1:]

                    if cmd == "exit":
                        Menu_En()
                        break
                    elif cmd == "clear":
                        output_buffer = []
                    elif cmd == "help":
                        output_buffer.append("Commands: " + ", ".join(commands.keys()))
                    elif cmd in ["ls", "dir"]:
                        try:
                            for f in os.listdir("."):
                                prefix = "[DIR] " if os.path.isdir(f) else "      "
                                output_buffer.append(prefix + f)
                        except Exception as e:
                            output_buffer.append(str(e))
                    elif cmd == "cd":
                        if args:
                            try:
                                os.chdir(args[0])
                            except Exception as e:
                                output_buffer.append(str(e))
                        else:
                            output_buffer.append(os.getcwd())
                    elif cmd == "pwd":
                        output_buffer.append(os.getcwd())
                    elif cmd == "whoami":
                        output_buffer.append(user)
                    elif cmd == "explain":
                        if args and args[0] in explanations:
                            output_buffer.append(f"{args[0]}: {explanations[args[0]]}")
                        elif args:
                            output_buffer.append(f"No explanation for {args[0]}")
                        else:
                            output_buffer.append("Usage: explain <command>")
                    else:
                        output_buffer.append(f"Unknown command: {cmd}")
                current_input = ""

            elif key in (curses.KEY_BACKSPACE, 127, 8):
                current_input = current_input[:-1]

            elif key == 9: # Tab
                parts = current_input.split()
                if parts and len(parts) == 1:
                    matches = [c for c in commands if c.startswith(parts[0])]
                    if len(matches) == 1:
                        current_input = matches[0] + " "

            elif 32 <= key <= 126:
                current_input += chr(key)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def SystemInfo_En():
        stdscr.clear()
        window(13)
        safe_addstr(1, 2, "System Information")
        safe_addstr(3, 2, f"Operating System: {os.name}")
        safe_addstr(4, 2, f"Current Directory: {os.getcwd()}")
        safe_addstr(5, 2, f"User: {os.getenv('USER') or os.getenv('USERNAME')}")
        safe_addstr(6, 2, f"Python Version: {os.sys.version.split()[0]}")
        safe_addstr(7, 2, f"EtchOS Version: {current_version}")
        safe_addstr(8, 2, "Press any key to return to the main menu.")
        stdscr.refresh()
        stdscr.getch()
        Menu_En()
    
    # Text Editor Functionality with connection to File Manager

    def TextEditor_En(open_path=None):
        # Minimal text editor using `window()` and `safe_addstr()`.
        # - Prompt for filename
        # - Basic multi-line editing (typing, Backspace, Enter)
        # - Arrow navigation
        # - Ctrl+S to save, Ctrl+X to quit (without saving)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_dir = os.path.join(current_dir, "UserFilesTextEditor")
        try:
            os.makedirs(user_dir, exist_ok=True)
        except Exception:
            pass

        # determine file path: use provided path or prompt for filename
        if open_path:
            path = open_path
            # ensure path is inside user_dir (if absolute path provided, accept it)
        else:
            stdscr.clear()
            window(6)
            safe_addstr(1, 2, "Text Editor")
            safe_addstr(2, 2, "Enter filename (without extension):")
            stdscr.refresh()
            curses.echo()
            try:
                fname = stdscr.getstr(3, 2, 40).decode('utf-8').strip()
            finally:
                try:
                    curses.noecho()
                except Exception:
                    pass

            if not fname:
                return

            path = os.path.join(user_dir, fname + ".txt")
        # load if exists
        # load if exists
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = [l.rstrip('\n') for l in f.readlines()]
            if not lines:
                lines = ['']
        else:
            lines = ['']

        # editor state
        top = 0
        cursor_r = 0
        cursor_c = 0

        while True:
            stdscr.clear()
            # compute box height based on terminal
            term_h, term_w = stdscr.getmaxyx()
            h = min(max(6, len(lines) + 4), term_h - 2)
            window(h)
            # draw visible lines inside box (offset by 1)
            max_rows = h - 3
            for i in range(max_rows):
                idx = top + i
                if idx >= len(lines):
                    break
                safe_addstr(1 + i, 2, lines[idx])

            # status/instructions
            safe_addstr(h - 1, 2, "Ctrl-S: save  Ctrl-X: quit  Arrows to move")
            # place cursor
            vis_r = cursor_r - top
            if 0 <= vis_r < max_rows:
                try:
                    stdscr.move(1 + vis_r, 2 + cursor_c)
                except Exception:
                    pass

            stdscr.refresh()
            ch = stdscr.getch()
            # Ctrl-X go to main menu
            if ch == 24:
                Menu_En()
                return
            # Ctrl-S save
            if ch == 19:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    safe_addstr(h - 1, 2, "Saved.")
                    stdscr.refresh()
                    time.sleep(0.6)
                except Exception:
                    safe_addstr(h - 1, 2, "Save failed.")
                    stdscr.refresh()
                    time.sleep(0.8)
                continue
            # navigation
            if ch in (curses.KEY_UP,):
                if cursor_r > 0:
                    cursor_r -= 1
                    cursor_c = min(cursor_c, len(lines[cursor_r]))
                    if cursor_r < top:
                        top = cursor_r
                continue
            if ch in (curses.KEY_DOWN,):
                if cursor_r + 1 < len(lines):
                    cursor_r += 1
                    cursor_c = min(cursor_c, len(lines[cursor_r]))
                    if cursor_r >= top + max_rows:
                        top = cursor_r - max_rows + 1
                continue
            if ch in (curses.KEY_LEFT,):
                if cursor_c > 0:
                    cursor_c -= 1
                elif cursor_r > 0:
                    cursor_r -= 1
                    cursor_c = len(lines[cursor_r])
                if cursor_r < top:
                    top = cursor_r
                continue
            if ch in (curses.KEY_RIGHT,):
                if cursor_c < len(lines[cursor_r]):
                    cursor_c += 1
                elif cursor_r + 1 < len(lines):
                    cursor_r += 1
                    cursor_c = 0
                if cursor_r >= top + max_rows:
                    top = cursor_r - max_rows + 1
                continue

            # Backspace
            if ch in (curses.KEY_BACKSPACE, 127, 8):
                if cursor_c > 0:
                    lines[cursor_r] = lines[cursor_r][:cursor_c-1] + lines[cursor_r][cursor_c:]
                    cursor_c -= 1
                else:
                    if cursor_r > 0:
                        prev = lines[cursor_r - 1]
                        lines[cursor_r - 1] = prev + lines[cursor_r]
                        del lines[cursor_r]
                        cursor_r -= 1
                        cursor_c = len(lines[cursor_r])
                        if cursor_r < top:
                            top = cursor_r
                continue

            # Enter -> new line
            if ch in (10, 13):
                rest = lines[cursor_r][cursor_c:]
                lines[cursor_r] = lines[cursor_r][:cursor_c]
                lines.insert(cursor_r + 1, rest)
                cursor_r += 1
                cursor_c = 0
                if cursor_r >= top + max_rows:
                    top = cursor_r - max_rows + 1
                continue

            # printable
            if 32 <= ch <= 126:
                lines[cursor_r] = lines[cursor_r][:cursor_c] + chr(ch) + lines[cursor_r][cursor_c:]
                cursor_c += 1
                continue

            # ignore other keys
            continue

    
    
    # Calculator Functionality
    def Calculator_En():
        stdscr.clear()
        window(8)
        safe_addstr(1, 2, "Calculator")
        safe_addstr(3, 2, "Enter calculation (e.g. 2 + 2):")
        stdscr.refresh()
        try:
            curses.echo()
            s = stdscr.getstr(4, 2, 40).decode('utf-8').strip()
        finally:
            try:
                curses.noecho()
            except Exception:
                pass

        if not s:
            return

        try:
            parts = s.split()
            if len(parts) != 3:
                raise ValueError("Expected format: NUMBER OPERATOR NUMBER")
            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    raise ValueError("Cannot divide by zero.")
                result = num1 / num2
            else:
                raise ValueError("Invalid operator.")

            safe_addstr(5, 2, f"Result: {result}")
            safe_addstr(6, 2, "Press any key to continue.")
            stdscr.refresh()
            stdscr.getch()
            Menu_En()

        except Exception as e:
            safe_addstr(5, 2, f"Error: {e}")
            stdscr.refresh()
            time.sleep(2)
            Calculator_En()
    
    # Help Centre Functionality (using os)
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
                        else:
                            # if selected file is a .txt, open in text editor
                            if target.lower().endswith('.txt'):
                                TextEditor_En(target)
                                # after editing, refresh listing
                                try:
                                    items = os.listdir(current_path)
                                except Exception:
                                    items = []

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
        while True:
            stdscr.clear()
            window(10)
            safe_addstr(1, 2, "Settings")
            safe_addstr(3, 2, "1. Change User Data")
            safe_addstr(4, 2, "2. Change Boot Animation")
            safe_addstr(5, 2, "3. Change System Color")
            safe_addstr(6, 2, "4. Back to Main Menu")
            safe_addstr(8, 2, "Please enter your choice: ")
            stdscr.refresh()
            
            choice = stdscr.getch()
            
            if choice == ord('1'):
                UserSetup_En()
                break
            elif choice == ord('2'):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "Assets", "StartupScreenLogo.txt")
                TextEditor_En(file_path)
                break
            elif choice == ord('3'):
                while True:
                    stdscr.clear()
                    window(10)
                    safe_addstr(1, 2, "System Color Settings")
                    safe_addstr(3, 2, "1. Matrix (Green)")
                    safe_addstr(4, 2, "2. Classic (White)")
                    safe_addstr(5, 2, "3. PowerShell (Blue)")
                    safe_addstr(6, 2, "4. Back")
                    safe_addstr(8, 2, "Select a color scheme: ")
                    stdscr.refresh()
                    
                    color_choice = stdscr.getch()
                    if color_choice == ord('4'):
                        break
                    
                    if color_choice == ord('1'):
                        if curses.has_colors(): stdscr.bkgd(' ', curses.color_pair(1))
                    elif color_choice == ord('2'):
                        if curses.has_colors(): stdscr.bkgd(' ', curses.color_pair(2))
                    elif color_choice == ord('3'):
                        if curses.has_colors(): stdscr.bkgd(' ', curses.color_pair(3))
            elif choice == ord('4'):
                Menu_En()
                break
            else:
                safe_addstr(8, 2, "Invalid choice.")
                stdscr.refresh()
                time.sleep(1)
    
    
    
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