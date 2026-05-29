import curses
import os
import json
import subprocess
import sys
import time
import hashlib
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.log")
BOOTSCREEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bootscreen.txt")

# Session tracking
session_start_time = None

# Multi-language support
LANGUAGES = {
    "en": {
        "welcome": "Welcome to EtchOS 4.0.0",
        "select_language": "Select Language",
        "select_username": "Enter Username",
        "select_password": "Enter Password",
        "confirm_password": "Confirm Password",
        "passwords_no_match": "Passwords don't match!",
        "password_too_short": "Password must be at least 4 characters!",
        "username_too_short": "Username must be at least 3 characters!",
        "main_menu": "Main Menu - Select an app (X to quit)",
        "select_app": "Select an app",
        "running_app": "Running app",
        "shutdown_confirm": "Do you want to shut down the system? (Y/N)",
        "shutdown": "System shutdown",
        "error_running": "Error running",
        "onboarding_title": "First Time Setup",
        "login_title": "System Login",
        "invalid_credentials": "Invalid credentials! Try again...",
        "keyboard_hints": "↑↓ Navigate | Enter Select | X Quit",
        "logged_in_as": "Logged in as",
        "apps_available": "apps available",
        "session_duration": "Session duration",
        "minutes": "minutes",
    },
    "de": {
        "welcome": "Willkommen bei EtchOS 4.0.0",
        "select_language": "Sprache auswählen",
        "select_username": "Benutzername eingeben",
        "select_password": "Passwort eingeben",
        "confirm_password": "Passwort bestätigen",
        "passwords_no_match": "Passwörter stimmen nicht überein!",
        "password_too_short": "Passwort muss mind. 4 Zeichen sein!",
        "username_too_short": "Benutzername muss mind. 3 Zeichen sein!",
        "main_menu": "Hauptmenü - App auswählen (X zum Beenden)",
        "select_app": "App auswählen",
        "running_app": "App wird ausgeführt",
        "shutdown_confirm": "System herunterfahren? (J/N)",
        "shutdown": "System wird heruntergefahren",
        "error_running": "Fehler beim Ausführen von",
        "onboarding_title": "Erstmalige Einrichtung",
        "login_title": "Systemanmeldung",
        "invalid_credentials": "Ungültige Anmeldedaten! Erneut versuchen...",
        "keyboard_hints": "↑↓ Navigieren | Eingabe Auswählen | X Beenden",
        "logged_in_as": "Angemeldet als",
        "apps_available": "Apps verfügbar",
        "session_duration": "Sitzungsdauer",
        "minutes": "Minuten",
    },
    "fr": {
        "welcome": "Bienvenue sur EtchOS 4.0.0",
        "select_language": "Sélectionner la langue",
        "select_username": "Entrer le nom d'utilisateur",
        "select_password": "Entrer le mot de passe",
        "confirm_password": "Confirmer le mot de passe",
        "passwords_no_match": "Les mots de passe ne correspondent pas!",
        "password_too_short": "Le mot de passe doit avoir au moins 4 caractères!",
        "username_too_short": "Le nom d'utilisateur doit avoir au moins 3 caractères!",
        "main_menu": "Menu principal - Sélectionner une app (X pour quitter)",
        "select_app": "Sélectionner une app",
        "running_app": "App en cours d'exécution",
        "shutdown_confirm": "Voulez-vous arrêter le système? (O/N)",
        "shutdown": "Arrêt du système",
        "error_running": "Erreur lors de l'exécution de",
        "onboarding_title": "Configuration initiale",
        "login_title": "Connexion système",
        "invalid_credentials": "Identifiants invalides! Réessayez...",
        "keyboard_hints": "↑↓ Naviguer | Entrée Sélectionner | X Quitter",
        "logged_in_as": "Connecté en tant que",
        "apps_available": "apps disponibles",
        "session_duration": "Durée de session",
        "minutes": "minutes",
    },
}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def log_action(action, details=None):
    """Log an action to the main.log file in JSON format"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    }
    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        pass

def load_config():
    """Load or initialize config/user data from log file"""
    config = {
        "onboarding_done": False,
        "username": None,
        "language": "en",
        "password_hash": None
    }
    
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("action") == "onboarding_complete":
                            config.update(entry.get("details", {}))
                            config["onboarding_done"] = True
                    except:
                        pass
        except:
            pass
    
    return config

def load_bootscreen():
    """Load ASCII art from bootscreen.txt"""
    if os.path.exists(BOOTSCREEN_PATH):
        try:
            with open(BOOTSCREEN_PATH, "r") as f:
                return f.read()
        except:
            return None
    return None

def safe_addstr(stdscr, y, x, text, attr=0):
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
        stdscr.addstr(y, x, s, attr)
    except Exception:
        pass

def get_center_x(max_x, text_len):
    """Get centered X position for text"""
    return max(1, (max_x - text_len) // 2)

def draw_box(stdscr, top, left, height, width):
    """Draw an ASCII box at the specified position"""
    # Top border
    safe_addstr(stdscr, top, left, "┌" + "─" * (width - 2) + "┐")
    # Side borders
    for i in range(1, height - 1):
        safe_addstr(stdscr, top + i, left, "│")
        safe_addstr(stdscr, top + i, left + width - 1, "│")
    # Bottom border
    safe_addstr(stdscr, top + height - 1, left, "└" + "─" * (width - 2) + "┘")

def get_text_input(stdscr, y, x, prompt, max_width=40, is_password=False, min_length=0):
    """Get text input from user with visual feedback and validation"""
    curses.curs_set(1)
    stdscr.nodelay(0)
    stdscr.timeout(-1)
    
    input_text = ""
    
    while True:
        stdscr.clear()
        safe_addstr(stdscr, y, x, prompt, curses.A_BOLD)
        
        if is_password:
            display = "*" * len(input_text)
        else:
            display = input_text
        
        safe_addstr(stdscr, y + 2, x, display[:max_width])
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == ord('\n'):
            if len(input_text) >= min_length:
                curses.curs_set(0)
                stdscr.nodelay(1)
                stdscr.timeout(100)
                return input_text
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            input_text = input_text[:-1]
        elif 32 <= key <= 126:
            if len(input_text) < max_width:
                input_text += chr(key)

def onboarding(stdscr):
    """First-time setup screen with language, username, and password"""
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    # Language selection
    stdscr.clear()
    languages_list = list(LANGUAGES.keys())
    selected_lang = 0
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Draw centered box
        box_width = 40
        box_height = len(languages_list) + 5
        box_left = get_center_x(max_x, box_width)
        box_top = (max_y - box_height) // 2
        
        draw_box(stdscr, box_top, box_left, box_height, box_width)
        safe_addstr(stdscr, box_top + 1, box_left + 2, "ONBOARDING", curses.A_BOLD)
        safe_addstr(stdscr, box_top + 2, box_left + 2, "Select Language")
        
        for idx, lang in enumerate(languages_list):
            y = box_top + 4 + idx
            if idx == selected_lang:
                safe_addstr(stdscr, y, box_left + 2, f"> {lang.upper()}", curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, box_left + 2, f"  {lang.upper()}")
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == -1:
            continue
        if (key == curses.KEY_UP or key == ord('w')) and selected_lang > 0:
            selected_lang -= 1
        elif (key == curses.KEY_DOWN or key == ord('s')) and selected_lang < len(languages_list) - 1:
            selected_lang += 1
        elif key in [ord('\n'), ord(' ')]:
            language = languages_list[selected_lang]
            break
    
    lang_dict = LANGUAGES[language]
    
    # Username input with validation
    while True:
        username = get_text_input(stdscr, 5, 5, lang_dict["select_username"])
        if len(username) >= 3:
            break
        else:
            stdscr.clear()
            safe_addstr(stdscr, 5, 5, lang_dict["username_too_short"], curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
    
    # Password input with validation
    passwords_match = False
    while not passwords_match:
        password = get_text_input(stdscr, 5, 5, lang_dict["select_password"], is_password=True, min_length=4)
        if len(password) < 4:
            stdscr.clear()
            safe_addstr(stdscr, 5, 5, lang_dict["password_too_short"], curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
            continue
            
        password_confirm = get_text_input(stdscr, 5, 5, lang_dict["confirm_password"], is_password=True)
        
        if password == password_confirm:
            passwords_match = True
        else:
            stdscr.clear()
            safe_addstr(stdscr, 5, 5, lang_dict["passwords_no_match"], curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
    
    # Save onboarding data
    password_hash = hash_password(password)
    config = {
        "username": username,
        "language": language,
        "password_hash": password_hash,
        "onboarding_done": True
    }
    
    log_action("onboarding_complete", config)
    
    return config

# Lists all python apps in the Apps directory for use in the main menu.
def ListApps():
    apps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Apps")
    apps = []
    if os.path.exists(apps_dir):
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            if os.path.isfile(item_path) and item.endswith(".py"):
                apps.append(item[:-3])  # Remove .py extension
    return apps

def MainMenu(stdscr, config):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    apps = ListApps()
    selected = 0
    language = config.get("language", "en")
    lang_dict = LANGUAGES.get(language, LANGUAGES["en"])

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Calculate dimensions
        box_width = min(max_x - 4, 60)
        box_height = len(apps) + 7
        box_top = 1
        box_left = get_center_x(max_x, box_width)
        
        # Draw main menu box
        draw_box(stdscr, box_top, box_left, box_height, box_width)
        
        # Title inside the box
        safe_addstr(stdscr, box_top + 1, box_left + 2, "MAIN MENU", curses.A_BOLD)
        safe_addstr(stdscr, box_top + 2, box_left + 2, f"{lang_dict['logged_in_as']}: {config.get('username')}")
        safe_addstr(stdscr, box_top + 3, box_left + 2, f"{len(apps)} {lang_dict['apps_available']}")
        
        # Menu items inside the box
        for idx, app in enumerate(apps):
            y = box_top + 4 + idx
            if idx == selected:
                safe_addstr(stdscr, y, box_left + 2, f"> {app}", curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, box_left + 2, f"  {app}")
        
        # Keyboard hints at bottom
        hints_y = max_y - 2
        safe_addstr(stdscr, hints_y, 1, lang_dict["keyboard_hints"], curses.A_DIM)
        
        # Session duration info
        if session_start_time:
            elapsed = int((time.time() - session_start_time) / 60)
            info_text = f"{lang_dict['session_duration']}: {elapsed} {lang_dict['minutes']}"
            safe_addstr(stdscr, max_y - 1, max_x - len(info_text) - 2, info_text, curses.A_DIM)

        stdscr.refresh()
        key = stdscr.getch()

        if key == -1:
            continue  # No key pressed
        
        if (key == curses.KEY_UP or key == ord('w') or key == ord('W')) and selected > 0:
            selected -= 1
        elif (key == curses.KEY_DOWN or key == ord('s') or key == ord('S')) and selected < len(apps) - 1:
            selected += 1
        elif key in [ord('\n'), ord(' ')]:  # Enter or Space
            app_name = apps[selected]
            log_action("app_launched", {"app": app_name, "user": config.get("username")})
            
            # End curses to let the app use the terminal
            curses.endwin()
            
            # Run the app directly in terminal (lets curses apps work properly)
            app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Apps", f"{app_name}.py")
            try:
                subprocess.run([sys.executable, app_path], check=False)
            except Exception as e:
                log_action("app_error", {"app": app_name, "error": str(e), "user": config.get("username")})
                print(f"{lang_dict['error_running']} {app_name}: {e}")
            
            # Reinitialize curses
            stdscr = curses.initscr()
            curses.cbreak()
            curses.noecho()
            stdscr.keypad(True)
            curses.curs_set(0)
            stdscr.nodelay(1)
            stdscr.timeout(100)
        elif key in [ord('x'), ord('X')]:
            log_action("shutdown_initiated", {"user": config.get("username")})
            
            # Shutdown confirmation box
            max_y, max_x = stdscr.getmaxyx()
            box_width = 40
            box_height = 5
            box_left = get_center_x(max_x, box_width)
            box_top = (max_y - box_height) // 2
            
            stdscr.clear()
            draw_box(stdscr, box_top, box_left, box_height, box_width)
            safe_addstr(stdscr, box_top + 1, box_left + 2, "SHUTDOWN", curses.A_BOLD)
            safe_addstr(stdscr, box_top + 2, box_left + 2, lang_dict["shutdown_confirm"])
            stdscr.refresh()
            
            time.sleep(0.5)
            key = stdscr.getch()
            if key in [ord('y'), ord('Y')] or (language == "de" and key in [ord('j'), ord('J')]) or (language == "fr" and key in [ord('o'), ord('O')]):
                log_action("shutdown_complete", {"user": config.get("username")})
                break
            else:
                log_action("shutdown_cancelled", {"user": config.get("username")})
        

def show_bootscreen(stdscr):
    """Display boot screen for 2 seconds"""
    boot_screen = load_bootscreen()
    if boot_screen:
        stdscr.clear()
        lines = boot_screen.split('\n')
        for i, line in enumerate(lines[:10]):  # Limit to first 10 lines
            safe_addstr(stdscr, i, 0, line)
        stdscr.refresh()
        time.sleep(2)

def show_welcome_screen(stdscr, username, language):
    """Show a welcome screen after successful login"""
    lang_dict = LANGUAGES.get(language, LANGUAGES["en"])
    
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    box_width = 50
    box_height = 7
    box_left = get_center_x(max_x, box_width)
    box_top = (max_y - box_height) // 2
    
    draw_box(stdscr, box_top, box_left, box_height, box_width)
    safe_addstr(stdscr, box_top + 1, box_left + 2, "WELCOME", curses.A_BOLD)
    safe_addstr(stdscr, box_top + 2, box_left + 2, f"{lang_dict['welcome']}")
    safe_addstr(stdscr, box_top + 3, box_left + 2, f"Hello, {username}!")
    safe_addstr(stdscr, box_top + 5, box_left + 2, "Press any key to continue...")
    
    stdscr.refresh()
    stdscr.getch()

def login(stdscr, config):
    """Login screen - verify username and password with framing"""
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    language = config.get("language", "en")
    lang_dict = LANGUAGES.get(language, LANGUAGES["en"])
    
    max_y, max_x = stdscr.getmaxyx()
    
    # Ask for username
    username = get_text_input(stdscr, 5, 5, lang_dict["select_username"])
    
    # Ask for password
    password = get_text_input(stdscr, 5, 5, lang_dict["select_password"], is_password=True)
    password_hash = hash_password(password)
    
    # Verify credentials
    if username == config.get("username") and password_hash == config.get("password_hash"):
        config["username"] = username
        log_action("login_success", {"user": username})
        show_welcome_screen(stdscr, username, language)
        return True
    else:
        stdscr.clear()
        
        box_width = 45
        box_height = 5
        box_left = get_center_x(max_x, box_width)
        box_top = (max_y - box_height) // 2
        
        draw_box(stdscr, box_top, box_left, box_height, box_width)
        safe_addstr(stdscr, box_top + 1, box_left + 2, "LOGIN FAILED", curses.A_BOLD)
        safe_addstr(stdscr, box_top + 2, box_left + 2, lang_dict["invalid_credentials"])
        
        stdscr.refresh()
        time.sleep(2)
        log_action("login_failed", {"attempted_user": username})
        return False

def main():
    global session_start_time
    
    try:
        stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        
        # Show boot screen
        show_bootscreen(stdscr)
        
        # Load config
        config = load_config()
        
        # If onboarding not done, run onboarding
        if not config.get("onboarding_done"):
            config = onboarding(stdscr)
        else:
            # If onboarding is done, show login screen
            login_success = False
            while not login_success:
                login_success = login(stdscr, config)
                if not login_success:
                    # Restart after failed login
                    curses.endwin()
                    return main()
        
        # Record session start time after successful login
        session_start_time = time.time()
        log_action("session_started", {"user": config.get("username")})
        
        MainMenu(stdscr, config)
        
        # Log session end
        if session_start_time:
            session_duration = int((time.time() - session_start_time) / 60)
            log_action("session_ended", {"user": config.get("username"), "duration_minutes": session_duration})
    finally:
        curses.endwin()

if __name__ == "__main__":
    main()