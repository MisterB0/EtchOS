import curses
import os
import json
import subprocess
import sys

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.log")

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

# Main menu, uses ListApps to display all python apps in the Apps directory. User can select an app to run it, or press Q to shut down the system. 
# The menu is navigated using the arrow keys and Enter to select an app. The selected app is run in the same terminal window. 
# The menu also displays a log of all actions taken by the user, including which apps were run and when the system was shut down. 
# The log is saved to a file called main.log in the same directory as the main.py script. 
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


def MainMenu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)  # Non-blocking mode
    stdscr.timeout(100)

    apps = ListApps()
    selected = 0
    log = []

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Draw box around menu
        box_width = min(max_x - 4, 50)
        box_height = len(apps) + 5
        box_top = 1
        box_left = (max_x - box_width) // 2
        
        draw_box(stdscr, box_top, box_left, box_height, box_width)
        
        # Title inside the box
        title = "Main Menu - Select an app (Q to quit)"
        safe_addstr(stdscr, box_top + 1, box_left + 2, title[:box_width - 4], curses.A_BOLD)
        
        # Menu items inside the box
        for idx, app in enumerate(apps):
            y = box_top + 2 + idx
            if idx == selected:
                safe_addstr(stdscr, y, box_left + 2, f"> {app}", curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, box_left + 2, f"  {app}")

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
            log.append(f"Running app: {app_name}")
            with open(LOG_PATH, "a") as log_file:
                log_file.write(f"Running app: {app_name}\n")
            
            # End curses to let the app use the terminal
            curses.endwin()
            
            # Run the app directly in terminal (lets curses apps work properly)
            app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Apps", f"{app_name}.py")
            try:
                subprocess.run([sys.executable, app_path], check=False)
            except Exception as e:
                print(f"Error running {app_name}: {e}")
            
            # Reinitialize curses
            stdscr = curses.initscr()
            curses.cbreak()
            curses.noecho()
            stdscr.keypad(True)
            curses.curs_set(0)
            stdscr.nodelay(1)
            stdscr.timeout(100)
        elif key in [ord('q'), ord('Q')]:
            log.append("System shutdown")
            with open(LOG_PATH, "a") as log_file:
                log_file.write("System shutdown\n")
            break
        

MainMenu(curses.initscr())
curses.endwin()