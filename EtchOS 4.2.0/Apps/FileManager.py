def run(stdscr, file_path=None):
    import curses
    import os
    import subprocess
    import sys
    stdscr.clear()
    current_path = file_path if file_path and os.path.isdir(file_path) else os.getcwd()
    selected = 0
    start_index = 0
    curses.curs_set(0)
    stdscr.keypad(True)
    
    # Mapping extensions to apps
    EXT_MAP = {
        ".txt": "TextEditor",
        ".csv": "Spreadsheet",
        ".log": "TextEditor"
    }

    while True:
        stdscr.clear()
        try:
            items = os.listdir(current_path)
        except PermissionError:
            items = []
            stdscr.addstr(5, 2, "Permission denied")
        items.sort()
        term_h, term_w = stdscr.getmaxyx()
        desired_height = max(8, len(items) + 6)
        box_height = min(max(6, desired_height), max(6, term_h - 2))
        width = max(10, term_w - 4)
        content_x = 2
        inner_width = max(0, width - content_x)
        stdscr.addstr(1, content_x, "File Manager", curses.A_BOLD)
        stdscr.addstr(2, content_x, f"Path: {current_path}")
        stdscr.addstr(3, content_x, "↑ ↓ Navigate | Enter = open | Backspace = up | q = exit")
        max_items = max(0, box_height - 6)
        display_count = min(len(items) - start_index, max_items)
        if display_count <= 0:
            stdscr.addstr(4, 2, "(empty directory)")
            start_index = 0
            selected = 0
        else:
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
                if len(display) > inner_width:
                    if inner_width > 1:
                        display = display[:inner_width - 1] + "…"
                    else:
                        display = display[:inner_width]
                stdscr.addstr(4 + i, content_x, display)
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
                        # Open file with compatible app
                        ext = os.path.splitext(target)[1].lower()
                        app_name = EXT_MAP.get(ext)
                        if app_name:
                            # To open another app from within an app, we must exit the current one
                            # and let the OS handle it, or use subprocess.
                            # Since the OS runs apps as separate processes, we can't easily "switch".
                            # The cleanest way is to exit FileManager and let the main loop 
                            # know which app to launch. 
                            # But since we are a subprocess, we can just launch the target app 
                            # and then exit this one.
                            
                            # End curses to allow the new app to take over the terminal
                            curses.endwin()
                            app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{app_name}.py")
                            try:
                                subprocess.run([sys.executable, app_path, target], check=False)
                            except Exception as e:
                                print(f"Error opening {app_name}: {e}")
                            
                            # Now we exit the File Manager
                            return 
                        else:
                            # Unsupported file type
                            stdscr.addstr(box_height - 1, 2, "No compatible app found for this file.")
                            stdscr.refresh()
                            time.sleep(1)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            parent = os.path.dirname(current_path)
            if parent != current_path:
                current_path = parent
                selected = 0
        elif key == ord('q'):
            break
    stdscr.keypad(False)
    curses.curs_set(1)

if __name__ == "__main__":
    import curses
    import sys
    stdscr = curses.initscr()
    try:
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        # Check if a path was passed as an argument
        path_arg = sys.argv[1] if len(sys.argv) > 1 else None
        run(stdscr, path_arg)
    finally:
        curses.endwin()
