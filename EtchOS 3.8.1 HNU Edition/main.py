
# TODO: Add more comments throughout the code for clarity
# TODO: Fix German translations for all features (Do in final relese for HNU Project)
# More see Notion doc for ideas and tasks


# Curses for terminal UI, time for delays, os for file system operations
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

import random
# Added for 2048 game
import time
import os
import json
import sys
import platform

current_version = "3.8.1"

# EtchOS 3.8.1 - Terminal User Interface Operating System

def main(stdscr):
    
    # Initialize colors
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # Logging/data helpers
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, "main.log")
    current_user = None

    def read_log():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if not data:
                    return {"users": [], "tasks": []}
                return json.loads(data)
        except Exception:
            return {"users": [], "tasks": []}

    def write_log(data):
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def ensure_log_initialized():
        d = read_log()
        changed = False
        if "users" not in d:
            d["users"] = []
            changed = True
        if "tasks" not in d:
            d["tasks"] = []
            changed = True
        if changed:
            write_log(d)
        return d

    def window(height):
        # original simple fixed-position box
        safe_addstr(0, 0, "==========================================================")
        for i in range(1, height - 1):
            safe_addstr(i, 0, "│                                                        │")
        safe_addstr(height - 1, 0, "==========================================================")
        
    
    
    # Safe addstr function to prevent crashes when text exceeds window size
    def safe_addstr(y, x, text, attr=0):
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
            # try with attribute
            stdscr.addstr(y, x, s, attr)
        except curses.error:
            try:
                # fallback to addnstr without attr
                stdscr.addnstr(y, x, s, avail)
            except Exception:
                pass
            
    # Startup Screen (Change ASCII art as needed)
    def StartupScreen():
        stdscr.clear()
        logo_path = os.path.join(base_dir, "Assets", "StartupScreenLogo.txt")
        try:
            with open(logo_path, "r", encoding="utf-8") as f:
                content = f.readlines()
        except FileNotFoundError:
            content = [f"EtchOS {current_version}", " Startup Logo not found."]
        for idx, line in enumerate(content):
            safe_addstr(idx, 0, line.rstrip('\n'))
        stdscr.refresh()
        time.sleep(2)
        # Continue to Onboarding or Login depending on stored data
        d = ensure_log_initialized()
        if not d.get("users"):
            Onboarding()
        else:
            Login_En()
    
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
        nonlocal current_user
        stdscr.clear()
        safe_addstr(0, 0, "======================= User Setup =======================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ Please choose your username:                           │")
        safe_addstr(3, 0, "│                                                        │")
        safe_addstr(4, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        username = stdscr.getstr(2, 35, 20).decode('utf-8').strip()
        curses.noecho()
        safe_addstr(4, 0, f"│ Welcome,                                               │")
        safe_addstr(5, 10, username)
        safe_addstr(5, 0, "│                                                        │")
        safe_addstr(6, 0, "│ Please choose your password:                           │")
        safe_addstr(7, 0, "│                                                        │")
        safe_addstr(8, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        password = stdscr.getstr(6, 35, 20).decode('utf-8')
        curses.noecho()

        # persist user
        d = read_log()
        users = d.get("users", [])
        for u in users:
            if u.get("username") == username:
                u["password"] = password
                break
        else:
            users.append({"username": username, "password": password})
        d["users"] = users
        write_log(d)
        current_user = username

        safe_addstr(11, 0, "User setup complete!")
        safe_addstr(13, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        Menu_En()
    
    def UserSetup_De():
        nonlocal current_user
        stdscr.clear()
        safe_addstr(0, 0, "===================== Benutzer-Setup =====================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ Bitte wähle deinen Benutzernamen:                      │")
        safe_addstr(3, 0, "│                                                        │")
        safe_addstr(4, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        username = stdscr.getstr(2, 36, 20).decode('utf-8').strip()
        curses.noecho()
        safe_addstr(4, 0, f"│ Willkommen,                                               │")
        safe_addstr(5, 10, username)
        safe_addstr(5, 0, "│                                                        │")
        safe_addstr(6, 0, "│ Bitte wähle dein Passwort:                             │")
        safe_addstr(7, 0, "│                                                        │")
        safe_addstr(8, 0, "==========================================================")
        stdscr.refresh()
        curses.echo()
        password = stdscr.getstr(6, 36, 20).decode('utf-8')
        curses.noecho()
        #save user and password in json log
        # persist user
        d = read_log()
        users = d.get("users", [])
        for u in users:
            if u.get("username") == username:
                u["password"] = password
                break
        else:
            users.append({"username": username, "password": password})
        d["users"] = users
        write_log(d)
        current_user = username

        safe_addstr(11, 0, "Benutzer-Setup vervollständigt!")
        safe_addstr(13, 0, "Drücke eine beliebige Taste um fortzufahren...")
        stdscr.refresh()
        stdscr.getch()
        Menu_De()       
    
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
    
    
    #TODO: Change all numbers to letters for easier navigation (-:
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
        safe_addstr(10, 0, "│ 9. 2048 Game                                           │")
        safe_addstr(11, 0, "│ T. Todo     L. System Log                              │")
        safe_addstr(12, 0, "│ Please enter the number/letter of your choice:         │")
        safe_addstr(13, 0, "│                                                        │")
        safe_addstr(14, 0, "==========================================================")
        safe_addstr(16, 0, " ")
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
        elif choice == ord('9'):
            G2048_En()
        elif choice in (ord('t'), ord('T')):
            TaskManager_En()
        elif choice in (ord('l'), ord('L')):
            Log_En()
        else:
            safe_addstr(14, 0, "Invalid choice. Please try again.")
            stdscr.refresh()
            time.sleep(2)
            Menu_En()
    
    def Menu_De():
        stdscr.clear()
        safe_addstr(0, 0, "==================== EtchOS Hauptmenü ====================")
        safe_addstr(1, 0, "│                                                        │")
        safe_addstr(2, 0, "│ 1. Datenmanager                                        │")
        safe_addstr(3, 0, "│ 2. Einstellungen                                       │")
        safe_addstr(4, 0, "│ 3. Exit                                                │")
        safe_addstr(5, 0, "│ 4. Hilfe Center                                        │")
        safe_addstr(6, 0, "│ 5. Taschenrechner                                      │")
        safe_addstr(7, 0, "│ 6. EtchEditor (Texteditor)                             │")
        safe_addstr(8, 0, "│ 7. System Info                                         │")
        safe_addstr(9, 0, "│ 8. EtchShell (Terminal)                                │") 
        safe_addstr(10, 0, "│ 9. 2048 Spiel                                          │")
        safe_addstr(11, 0, "│ T. Todo     L. System Log                              │")
        safe_addstr(12, 0, "│ Wähle die Nummer/Buchstabe deiner Wahl:                │")
        safe_addstr(13, 0, "│                                                        │")
        safe_addstr(14, 0, "==========================================================")
        safe_addstr(16, 0, " ")
        stdscr.refresh()
        choice = stdscr.getch()
        if choice == ord('1'):
            FileManager_De()
        elif choice == ord('2'):
            Settings_De()
        elif choice == ord('3'):
            Exit_En()
        elif choice == ord('4'):
            HelpCentre_De()
        elif choice == ord('5'):
            Calculator_De()
        elif choice == ord('6'):
            TextEditor_De()
        elif choice == ord('7'):
            SystemInfo_De()
        elif choice == ord('8'):
            EtchShell_De()
        elif choice == ord('9'):
            G2048_De()
        elif choice in (ord('t'), ord('T')):
            TaskManager_De()
        elif choice in (ord('l'), ord('L')):
            Log_De()
        else:
            safe_addstr(14, 0, "Ungültige Auswahl. Bitte versuche es erneut.")
            stdscr.refresh()
            time.sleep(2)
            Menu_De()
    
    
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
    
    
    def EtchShell_De():
        # Terminal with EtchShell Advanced functions; explanations to linux and windows cmd commands; auto complete feature
        height = 16
        output_buffer = ["EtchShell v1.0", "Gebe 'help' ein für Befehle."]
        current_input = ""

        # Command definitions
        commands = {
            "help": "Zeige diese Hilfe",
            "clear": "Bildschirm leeren",
            "exit": "Terminal verlassen",
            "ls": "Dateien anzeigen(Linux)",
            "dir": "Dateinen anzeigen (Windows)",
            "cd": "Verzeichnis wechseln",
            "pwd": "Arbeitsverzeichnis anzeigen",
            "whoami": "Zeige aktuellen Benutzer",
            "explain": "Einen Befehl erklären (e.g. 'explain ls')"
        }

        # Explanations for specific commands (cross-platform help)
        explanations = {
            "ls": "Inhalte des Arbeitsverzeichnisses anzeigen. Equivalent zu 'dir' in Windows.",
            "dir": "Inhalte des Arbeitsverzeichnisses anzeigen. Equivalent zu 'ls' in Linux.",
            "cd": "Ändert das Arbeitsverzeichnis.",
            "pwd": "Gibt den aktuellen Arbeitsverzeichnisweg aus.",
            "clear": "Leert den Terminal-Bildschirm. Equivalent zu 'cls' in Windows.",
            "whoami": "Gibt den Nutzernamen aus.",
            "mkdir": "Erstellt ein neues Verzeichnis.",
            "rm": "Entfernt ein Datei."
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
                        output_buffer.append("Befehle: " + ", ".join(commands.keys()))
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
                            output_buffer.append(f"Keine Erklärung für {args[0]}")
                        else:
                            output_buffer.append("Benutzung: explain <Befehl>")
                    else:
                        output_buffer.append(f"Unbekannter Befehl: {cmd}")
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
    
    
    def TaskManager_En():
        nonlocal current_user
        stdscr.clear()
        if not current_user:
            safe_addstr(1, 2, "Please login to manage tasks.")
            safe_addstr(3, 2, "Press any key to go to login.")
            stdscr.refresh()
            stdscr.getch()
            Login_En()
            return

        while True:
            d = read_log()
            tasks = [t for t in d.get("tasks", []) if t.get("user") == current_user]
            stdscr.clear()
            window(12)
            safe_addstr(1, 2, f"Todo - {current_user}")
            if not tasks:
                safe_addstr(3, 4, "No tasks. Press 'a' to add, 'q' to return.")
            else:
                for i, t in enumerate(tasks[:8], start=1):
                    mark = "x" if t.get("done") else " "
                    safe_addstr(2 + i, 4, f"{i}. [{mark}] {t.get('title')}")
                safe_addstr(11, 2, "a: add  m: mark done  d: delete  q: back")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')):
                Menu_En()
                return
            if ch in (ord('a'), ord('A')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "New task title:")
                stdscr.refresh()
                curses.echo()
                try:
                    title = stdscr.getstr(2, 2, 60).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if title:
                    new_task = {"user": current_user, "title": title, "done": False}
                    d = read_log()
                    d.setdefault("tasks", []).append(new_task)
                    write_log(d)
                continue
            if ch in (ord('m'), ord('M')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "Enter task number to toggle done:")
                stdscr.refresh()
                curses.echo()
                try:
                    s = stdscr.getstr(2, 2, 4).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(tasks):
                        real_idx = None
                        # find index in full tasks
                        for i, t in enumerate(d.get("tasks", [])):
                            if t is tasks[idx]:
                                real_idx = i
                                break
                        if real_idx is not None:
                            d["tasks"][real_idx]["done"] = not d["tasks"][real_idx].get("done", False)
                            write_log(d)
                continue
            if ch in (ord('d'), ord('D')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "Enter task number to delete:")
                stdscr.refresh()
                curses.echo()
                try:
                    s = stdscr.getstr(2, 2, 4).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(tasks):
                        # remove from full list
                        for i, t in enumerate(d.get("tasks", [])):
                            if t is tasks[idx]:
                                d["tasks"].pop(i)
                                write_log(d)
                                break
                continue
    
    def TaskManager_De():
        nonlocal current_user
        stdscr.clear()
        if not current_user:
            safe_addstr(1, 2, "Bitte Melde dich an um Aufgaben zu verwalten.")
            safe_addstr(3, 2, "Drücke eine beliebige Taste um zum Login zu kommen.")
            stdscr.refresh()
            stdscr.getch()
            Login_De()
            return

        while True:
            d = read_log()
            tasks = [t for t in d.get("tasks", []) if t.get("user") == current_user]
            stdscr.clear()
            window(12)
            safe_addstr(1, 2, f"Todo - {current_user}")
            if not tasks:
                safe_addstr(3, 4, "Keine Aufgaben. 'a' zum hinzufügen, 'q' zum zurückzukehren.")
            else:
                for i, t in enumerate(tasks[:8], start=1):
                    mark = "x" if t.get("done") else " "
                    safe_addstr(2 + i, 4, f"{i}. [{mark}] {t.get('title')}")
                safe_addstr(11, 2, "a: hinzufügen  m: als fertig markieren  d: löschen  q: zurück")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')):
                Menu_De()
                return
            if ch in (ord('a'), ord('A')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "Titel der neuen Aufgabe:")
                stdscr.refresh()
                curses.echo()
                try:
                    title = stdscr.getstr(2, 2, 60).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if title:
                    new_task = {"user": current_user, "title": title, "done": False}
                    d = read_log()
                    d.setdefault("tasks", []).append(new_task)
                    write_log(d)
                continue
            if ch in (ord('m'), ord('M')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "Nummer der Aufgabe zum Markieren als fertig:")
                stdscr.refresh()
                curses.echo()
                try:
                    s = stdscr.getstr(2, 2, 4).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(tasks):
                        real_idx = None
                        # find index in full tasks
                        for i, t in enumerate(d.get("tasks", [])):
                            if t is tasks[idx]:
                                real_idx = i
                                break
                        if real_idx is not None:
                            d["tasks"][real_idx]["done"] = not d["tasks"][real_idx].get("done", False)
                            write_log(d)
                continue
            if ch in (ord('d'), ord('D')):
                stdscr.clear()
                window(6)
                safe_addstr(1, 2, "Nummer der Aufgabe zu löschen:")
                stdscr.refresh()
                curses.echo()
                try:
                    s = stdscr.getstr(2, 2, 4).decode('utf-8').strip()
                finally:
                    try:
                        curses.noecho()
                    except Exception:
                        pass
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(tasks):
                        # remove from full list
                        for i, t in enumerate(d.get("tasks", [])):
                            if t is tasks[idx]:
                                d["tasks"].pop(i)
                                write_log(d)
                                break
                continue
    
    
    
    
    def Log_En():
        stdscr.clear()
        d = read_log()
        users = d.get("users", [])
        tasks = d.get("tasks", [])

        while True:
            stdscr.clear()
            window(10)
            safe_addstr(1, 2, "System Log")
            safe_addstr(2, 2, f"Users: {len(users)}")
            for i, u in enumerate(users[:5], start=1):
                safe_addstr(2 + i, 4, f"- {u.get('username')} (password: {'*'*len(u.get('password',''))})")
            safe_addstr(8, 2, f"Tasks: {len(tasks)}")
            safe_addstr(9, 2, "Options: (c) clear logs  (q) back")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')):
                Menu_En()
                return
            if ch in (ord('c'), ord('C')):
                write_log({"users": [], "tasks": []})
                users = []
                tasks = []
                safe_addstr(9, 2, "Logs cleared. Press any key to continue.")
                stdscr.refresh()
                stdscr.getch()
                Menu_En()
                return
    
    def Log_De():
        stdscr.clear()
        d = read_log()
        users = d.get("users", [])
        tasks = d.get("tasks", [])

        while True:
            stdscr.clear()
            window(10)
            safe_addstr(1, 2, "System Log")
            safe_addstr(2, 2, f"Benutzer: {len(users)}")
            for i, u in enumerate(users[:5], start=1):
                safe_addstr(2 + i, 4, f"- {u.get('username')} (Passwort: {'*'*len(u.get('password',''))})")
            safe_addstr(8, 2, f"Aufgaben: {len(tasks)}")
            safe_addstr(9, 2, "Optionen: (c) Logs leeren  (q) zurück")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')):
                Menu_De()
                return
            if ch in (ord('c'), ord('C')):
                write_log({"users": [], "tasks": []})
                users = []
                tasks = []
                safe_addstr(9, 2, "Logs geleert. Drücke eine beliebeige Taste um fortzufahren.")
                stdscr.refresh()
                stdscr.getch()
                Menu_De()
                return
    
    
    def Login_De():
        nonlocal current_user
        attempts = 0
        while True:
            stdscr.clear()
            window(6)
            safe_addstr(1, 2, "Login")
            safe_addstr(2, 2, "Nutzername: ")
            stdscr.refresh()
            curses.echo()
            try:
                username = stdscr.getstr(2, 12, 30).decode('utf-8').strip()
            finally:
                try:
                    curses.noecho()
                except Exception:
                    pass

            safe_addstr(3, 2, "Passwort: ")
            stdscr.refresh()
            try:
                curses.echo()
                password = stdscr.getstr(3, 12, 30).decode('utf-8')
            finally:
                try:
                    curses.noecho()
                except Exception:
                    pass

            d = read_log()
            users = d.get("users", [])
            match = None
            for u in users:
                if u.get("username") == username:
                    match = u
                    break
            if match and match.get("password") == password:
                current_user = username
                stdscr.clear()
                safe_addstr(2, 2, f"Login verfollständigt. Willkommen, {username}.")
                stdscr.refresh()
                time.sleep(1)
                Menu_De()
                return
            else:
                attempts += 1
                safe_addstr(6, 1, "Login fehlgeschlagen. Drücke 'r' zum Registrieren, alle anderen Tasten zum erneut versuchen, 'g' für Gast.")
                stdscr.refresh()
                ch = stdscr.getch()
                if ch in (ord('r'), ord('R')):
                    UserSetup_De()
                    return
                if ch in (ord('g'), ord('G')):
                    current_user = None
                    Menu_De()
                    return
                if attempts >= 3:
                    safe_addstr(6, 2, "Zu viele Versuche. Drücke eine beliebige Taste um fortzufahren als Gast.")
                    stdscr.refresh()
                    stdscr.getch()
                    current_user = None
                    Menu_De()
                    return
                continue
    
    
    def Login_En():
        nonlocal current_user
        attempts = 0
        while True:
            stdscr.clear()
            window(6)
            safe_addstr(1, 2, "Login")
            safe_addstr(2, 2, "Username: ")
            stdscr.refresh()
            curses.echo()
            try:
                username = stdscr.getstr(2, 12, 30).decode('utf-8').strip()
            finally:
                try:
                    curses.noecho()
                except Exception:
                    pass

            safe_addstr(3, 2, "Password: ")
            stdscr.refresh()
            try:
                curses.echo()
                password = stdscr.getstr(3, 12, 30).decode('utf-8')
            finally:
                try:
                    curses.noecho()
                except Exception:
                    pass

            d = read_log()
            users = d.get("users", [])
            match = None
            for u in users:
                if u.get("username") == username:
                    match = u
                    break
            if match and match.get("password") == password:
                current_user = username
                stdscr.clear()
                safe_addstr(2, 2, f"Login successful. Welcome, {username}.")
                stdscr.refresh()
                time.sleep(1)
                Menu_En()
                return
            else:
                attempts += 1
                safe_addstr(6, 1, "Login failed. Press 'r' to register, any other key to retry or 'g' for guest.")
                stdscr.refresh()
                ch = stdscr.getch()
                if ch in (ord('r'), ord('R')):
                    UserSetup_En()
                    return
                if ch in (ord('g'), ord('G')):
                    current_user = None
                    Menu_En()
                    return
                if attempts >= 3:
                    safe_addstr(6, 2, "Too many attempts. Press any key to continue as guest.")
                    stdscr.refresh()
                    stdscr.getch()
                    current_user = None
                    Menu_En()
                    return
                continue
    
    
    
    
    
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
    
    def SystemInfo_De():
        stdscr.clear()
        window(13)
        safe_addstr(1, 2, "System Information")
        safe_addstr(3, 2, f"Operating System: {os.name}")
        safe_addstr(4, 2, f"Gewähltes Verzeichnis: {os.getcwd()}")
        safe_addstr(5, 2, f"Nutzer: {os.getenv('USER') or os.getenv('USERNAME')}")
        safe_addstr(6, 2, f"Python Version: {os.sys.version.split()[0]}")
        safe_addstr(7, 2, f"EtchOS Version: {current_version}")
        safe_addstr(8, 2, "Drücke eine beliebige Taste um zum Hauptmenü zu kommen.")
        stdscr.refresh()
        stdscr.getch()
        Menu_De()
    
    
    
    
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

    
    def TextEditor_De(open_path=None):
        

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
            safe_addstr(1, 2, "Texteditor")
            safe_addstr(2, 2, "Bennene die Datei (ohne .txt):")
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
            safe_addstr(h - 1, 2, "Ctrl-S: Speichern  Ctrl-X: Exit  Pfeiltasten zum bewegen")
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
                Menu_De()
                return
            # Ctrl-S save
            if ch == 19:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    safe_addstr(h - 1, 2, "Gespeichert.")
                    stdscr.refresh()
                    time.sleep(0.6)
                except Exception:
                    safe_addstr(h - 1, 2, "Speichern fehlgeschlagen.")
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
    def G2048_En():


        def get_logic_line(line):
            points = 0
            new_line = [x for x in line if x != 0]
            for i in range(len(new_line) - 1):
                if new_line[i] == new_line[i+1]:
                    new_line[i] *= 2
                    points += new_line[i]
                    new_line[i+1] = 0
            new_line = [x for x in new_line if x != 0]
            while len(new_line) < 4:
                new_line.append(0)
            return new_line, points

        def add_new_tile(board):
            empty_indices = [i for i, val in enumerate(board) if val == 0]
            if empty_indices:
                idx = random.choice(empty_indices)
                board[idx] = 4 if random.random() > 0.9 else 2

        def draw_board(board, score):
            # frame
            safe_addstr(1, 1, "=========================")
            safe_addstr(2, 1, "│     │     │     │     │")
            safe_addstr(3, 1, "=========================")
            safe_addstr(4, 1, "│     │     │     │     │")
            safe_addstr(5, 1, "=========================")
            safe_addstr(6, 1, "│     │     │     │     │")
            safe_addstr(7, 1, "=========================")
            safe_addstr(8, 1, "│     │     │     │     │")
            safe_addstr(9, 1, "=========================")
            safe_addstr(10, 1, f"Score: {score}")
            safe_addstr(11, 1, "Arrow Keys: Move")
            safe_addstr(12, 1, "Q: Quit")

            coords = [
                (2, 2), (2, 8), (2, 14), (2, 20),
                (4, 2), (4, 8), (4, 14), (4, 20),
                (6, 2), (6, 8), (6, 14), (6, 20),
                (8, 2), (8, 8), (8, 14), (8, 20)
            ]

            for i, val in enumerate(board):
                y, x = coords[i]
                if val == 0:
                    s_val = "."
                    attr = 0
                else:
                    s_val = str(val)
                    attr = curses.A_BOLD
                offset = (5 - len(s_val)) // 2
                safe_addstr(y, x, "     ")
                safe_addstr(y, x + offset, s_val, attr)

        def check_game_over(board):
            if 0 in board: return False
            for r in range(4):
                for c in range(3):
                    if board[r*4+c] == board[r*4+c+1]: return False
            for c in range(4):
                for r in range(3):
                    if board[r*4+c] == board[(r+1)*4+c]: return False
            return True

        stdscr.clear()
        try:
            curses.curs_set(0)
        except Exception:
            pass

        board = [0] * 16
        score = 0
        add_new_tile(board)
        add_new_tile(board)

        draw_board(board, score)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break
            if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
                continue

            old_board = list(board)

            if key == curses.KEY_LEFT:
                for r in range(4):
                    row = board[r*4 : r*4+4]
                    new_row, pts = get_logic_line(row)
                    score += pts
                    board[r*4 : r*4+4] = new_row

            elif key == curses.KEY_RIGHT:
                for r in range(4):
                    row = board[r*4 : r*4+4]
                    row.reverse()
                    new_row, pts = get_logic_line(row)
                    score += pts
                    new_row.reverse()
                    board[r*4 : r*4+4] = new_row

            elif key == curses.KEY_UP:
                for c in range(4):
                    col = [board[c], board[c+4], board[c+8], board[c+12]]
                    new_col, pts = get_logic_line(col)
                    score += pts
                    board[c], board[c+4], board[c+8], board[c+12] = new_col

            elif key == curses.KEY_DOWN:
                for c in range(4):
                    col = [board[c], board[c+4], board[c+8], board[c+12]]
                    col.reverse()
                    new_col, pts = get_logic_line(col)
                    score += pts
                    new_col.reverse()
                    board[c], board[c+4], board[c+8], board[c+12] = new_col

            if board != old_board:
                add_new_tile(board)
                draw_board(board, score)
                if check_game_over(board):
                    safe_addstr(14, 1, "GAME OVER!", curses.A_BOLD)
                    safe_addstr(15, 1, f"Final Score: {score}")
                    safe_addstr(16, 1, "Press Q to exit")
                    while True:
                        if stdscr.getch() in [ord('q'), ord('Q')]:
                            Menu_En()
                            return
                stdscr.refresh()

        stdscr.clear()
        Menu_En()




    def G2048_De():


        def get_logic_line(line):
            points = 0
            new_line = [x for x in line if x != 0]
            for i in range(len(new_line) - 1):
                if new_line[i] == new_line[i+1]:
                    new_line[i] *= 2
                    points += new_line[i]
                    new_line[i+1] = 0
            new_line = [x for x in new_line if x != 0]
            while len(new_line) < 4:
                new_line.append(0)
            return new_line, points

        def add_new_tile(board):
            empty_indices = [i for i, val in enumerate(board) if val == 0]
            if empty_indices:
                idx = random.choice(empty_indices)
                board[idx] = 4 if random.random() > 0.9 else 2

        def draw_board(board, score):
            # frame
            safe_addstr(1, 1, "=========================")
            safe_addstr(2, 1, "│     │     │     │     │")
            safe_addstr(3, 1, "=========================")
            safe_addstr(4, 1, "│     │     │     │     │")
            safe_addstr(5, 1, "=========================")
            safe_addstr(6, 1, "│     │     │     │     │")
            safe_addstr(7, 1, "=========================")
            safe_addstr(8, 1, "│     │     │     │     │")
            safe_addstr(9, 1, "=========================")
            safe_addstr(10, 1, f"Punkte: {score}")
            safe_addstr(11, 1, "Pfeiltasten: Bewegen")
            safe_addstr(12, 1, "Q: Beenden")

            coords = [
                (2, 2), (2, 8), (2, 14), (2, 20),
                (4, 2), (4, 8), (4, 14), (4, 20),
                (6, 2), (6, 8), (6, 14), (6, 20),
                (8, 2), (8, 8), (8, 14), (8, 20)
            ]

            for i, val in enumerate(board):
                y, x = coords[i]
                if val == 0:
                    s_val = "."
                    attr = 0
                else:
                    s_val = str(val)
                    attr = curses.A_BOLD
                offset = (5 - len(s_val)) // 2
                safe_addstr(y, x, "     ")
                safe_addstr(y, x + offset, s_val, attr)

        def check_game_over(board):
            if 0 in board: return False
            for r in range(4):
                for c in range(3):
                    if board[r*4+c] == board[r*4+c+1]: return False
            for c in range(4):
                for r in range(3):
                    if board[r*4+c] == board[(r+1)*4+c]: return False
            return True

        stdscr.clear()
        try:
            curses.curs_set(0)
        except Exception:
            pass

        board = [0] * 16
        score = 0
        add_new_tile(board)
        add_new_tile(board)

        draw_board(board, score)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break
            if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
                continue

            old_board = list(board)

            if key == curses.KEY_LEFT:
                for r in range(4):
                    row = board[r*4 : r*4+4]
                    new_row, pts = get_logic_line(row)
                    score += pts
                    board[r*4 : r*4+4] = new_row

            elif key == curses.KEY_RIGHT:
                for r in range(4):
                    row = board[r*4 : r*4+4]
                    row.reverse()
                    new_row, pts = get_logic_line(row)
                    score += pts
                    new_row.reverse()
                    board[r*4 : r*4+4] = new_row

            elif key == curses.KEY_UP:
                for c in range(4):
                    col = [board[c], board[c+4], board[c+8], board[c+12]]
                    new_col, pts = get_logic_line(col)
                    score += pts
                    board[c], board[c+4], board[c+8], board[c+12] = new_col

            elif key == curses.KEY_DOWN:
                for c in range(4):
                    col = [board[c], board[c+4], board[c+8], board[c+12]]
                    col.reverse()
                    new_col, pts = get_logic_line(col)
                    score += pts
                    new_col.reverse()
                    board[c], board[c+4], board[c+8], board[c+12] = new_col

            if board != old_board:
                add_new_tile(board)
                draw_board(board, score)
                if check_game_over(board):
                    safe_addstr(14, 1, "GAME OVER!", curses.A_BOLD)
                    safe_addstr(15, 1, f"Endpunktestand: {score}")
                    safe_addstr(16, 1, "Drücke Q zum Beenden")
                    while True:
                        if stdscr.getch() in [ord('q'), ord('Q')]:
                            Menu_De()
                            return
                stdscr.refresh()

        stdscr.clear()
        Menu_De()





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
    
    
    
    def Calculator_De():
        stdscr.clear()
        window(8)
        safe_addstr(1, 2, "Taschenrechner")
        safe_addstr(3, 2, "Rechnung eingeben (z.B. 2 + 2):")
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
                raise ValueError("Format: NUMMER [SPACE] OPERATOR [SPACE] NUMMER")
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
                    raise ValueError("Kann nicht durch 0 geteilt werden.")
                result = num1 / num2
            else:
                raise ValueError("Inkorrekter Operator.")

            safe_addstr(5, 2, f"Ergebnis: {result}")
            safe_addstr(6, 2, "Drücke eine beliebige Taste um fortzufahren.")
            stdscr.refresh()
            stdscr.getch()
            Menu_De()

        except Exception as e:
            safe_addstr(5, 2, f"Fehler: {e}")
            stdscr.refresh()
            time.sleep(2)
            Calculator_De()
    
    
    
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
    
    
    def HelpCentre_De():
        
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # draw help box and populate entries; keep content inside box
        stdscr.clear()
        height = 10
        window(height)
        base_y = 0
        content_x = 2
        safe_addstr(base_y + 1, content_x, "Hilfe Center")
        safe_addstr(base_y + 3, content_x, "Artikel: [EN]")
        safe_addstr(base_y + 4, content_x + 2, "1. Getting Started")
        safe_addstr(base_y + 5, content_x + 2, "2. Troubleshooting")
        safe_addstr(base_y + 6, content_x + 2, "3. Update Instructions and Nodes")
        safe_addstr(8, 2, "Artikel wählen (oder andere Taste um zurückzukehren).")
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
            safe_addstr(9, 2, "Artikel nicht gefunden. Drücke eine beliebige Taste zum zurückzukehren.")
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
            safe_addstr(content_offset + max_rows, 0, "-- k/j oder Pfeiltasten zum scrollen, q oder Esc um zurückzukehren --")
            stdscr.refresh()

            key = stdscr.getch()
            if key in (ord('q'), 27):
                # return to menu
                Menu_De()
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

    
    
    def FileManager_De():
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
                safe_addstr(5, 2, "Zugriff verweigert")

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

            safe_addstr(1, content_x, "Dateien Manager")
            safe_addstr(2, content_x, f"Weg: {current_path}")
            safe_addstr(3, content_x, "Navigiere mit ↑ ↓ | Enter = offnen | Backspace = zurück | q = exit")

            max_items = max(0, box_height - 6)
            display_count = min(len(items) - start_index, max_items)

            if display_count <= 0:
                safe_addstr(4, 2, "(Leeres verzeichnis)")
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
                                TextEditor_De(target)
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
        Menu_De()
    
    
    
    

        
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
    
    
    def Settings_De():
        while True:
            stdscr.clear()
            window(10)
            safe_addstr(1, 2, "Einstellungen")
            safe_addstr(3, 2, "1. Ändere Nutzerdaten")
            safe_addstr(4, 2, "2. Ändere Bootscreen")
            safe_addstr(5, 2, "3. Verändere Systemfarbe")
            safe_addstr(6, 2, "4. Zurück zum Hauptmenü")
            safe_addstr(8, 2, "Bitte wähle deine Auswahl: ")
            stdscr.refresh()
            
            choice = stdscr.getch()
            
            if choice == ord('1'):
                UserSetup_De()
                break
            elif choice == ord('2'):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "Assets", "StartupScreenLogo.txt")
                TextEditor_De(file_path)
                break
            elif choice == ord('3'):
                while True:
                    stdscr.clear()
                    window(10)
                    safe_addstr(1, 2, "Sytemfarben Einstellungen")
                    safe_addstr(3, 2, "1. Matrix (Grün)")
                    safe_addstr(4, 2, "2. Classic (Weiß)")
                    safe_addstr(5, 2, "3. PowerShell (Blau)")
                    safe_addstr(6, 2, "4. Zurück")
                    safe_addstr(8, 2, "Farbe auswählen: ")
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
                Menu_De()
                break
            else:
                safe_addstr(8, 2, "Ungültige Auswahl.")
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
        try:
            if platform.system().lower().startswith("win"):
                os.system("shutdown /s /t 0")
            elif platform.system().lower() in ("linux", "darwin"):
                os.system("sudo poweroff")
        except Exception:
            pass
        finally:
            sys.exit(0)
        
    
    def Exit_De():
        stdscr.clear()
        window(5)
        # position message inside the box (fixed offsets as original)
        safe_addstr(2, 15, "Beende EtchOS. Bis zum nächsten Mal!")
        stdscr.refresh()
        time.sleep(2)
        try:
            if platform.system().lower().startswith("win"):
                os.system("shutdown /s /t 0")
            elif platform.system().lower() in ("linux", "darwin"):
                os.system("sudo poweroff")
        except Exception:
            pass
        finally:
            sys.exit(0)
    
    
    
    StartupScreen()
    stdscr.refresh()
    stdscr.getch()
    

wrapper(main)