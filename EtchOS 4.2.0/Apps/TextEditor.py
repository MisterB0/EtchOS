def run(stdscr, file_path=None):
    import curses
    import os
    import time
    import sys
    stdscr.clear()
    
    if file_path:
        path = file_path
    else:
        stdscr.addstr(1, 2, "Text Editor", curses.A_BOLD)
        stdscr.addstr(2, 2, "Enter filename (without extension):")
        stdscr.refresh()
        curses.echo()
        fname = stdscr.getstr(3, 2, 40).decode('utf-8').strip()
        curses.noecho()
        if not fname:
            return
        user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "UserFilesTextEditor")
        os.makedirs(user_dir, exist_ok=True)
        path = os.path.join(user_dir, fname + ".txt")

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = [l.rstrip('\n') for l in f.readlines()]
        if not lines:
            lines = ['']
    else:
        lines = ['']

    top = 0
    cursor_r = 0
    cursor_c = 0
    while True:
        stdscr.clear()
        term_h, term_w = stdscr.getmaxyx()
        h = min(max(6, len(lines) + 4), term_h - 2)
        
        stdscr.addstr(0, 2, f"Editing: {os.path.basename(path)}", curses.A_DIM)
        
        for i in range(h - 3):
            idx = top + i
            if idx >= len(lines):
                break
            stdscr.addstr(1 + i, 2, lines[idx])
            
        stdscr.addstr(h - 1, 2, "Ctrl-S: save  Ctrl-X: quit  Arrows to move")
        vis_r = cursor_r - top
        if 0 <= vis_r < h - 3:
            try:
                stdscr.move(1 + vis_r, 2 + cursor_c)
            except Exception:
                pass
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 24 or ch == ord('q') or ch == ord('Q'):
            return
        if ch == 19:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                stdscr.addstr(h - 1, 2, "Saved.")
                stdscr.refresh()
                time.sleep(0.6)
            except Exception:
                stdscr.addstr(h - 1, 2, "Save failed.")
                stdscr.refresh()
                time.sleep(0.8)
            continue
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
                if cursor_r >= top + (h - 3):
                    top = cursor_r - (h - 3) + 1
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
            if cursor_r >= top + (h - 3):
                top = cursor_r - (h - 3) + 1
            continue
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
        if ch in (10, 13):
            rest = lines[cursor_r][cursor_c:]
            lines[cursor_r] = lines[cursor_r][:cursor_c]
            lines.insert(cursor_r + 1, rest)
            cursor_r += 1
            cursor_c = 0
            if cursor_r >= top + (h - 3):
                top = cursor_r - (h - 3) + 1
            continue
        if 32 <= ch <= 126:
            lines[cursor_r] = lines[cursor_r][:cursor_c] + chr(ch) + lines[cursor_r][cursor_c:]
            cursor_c += 1
            continue

if __name__ == "__main__":
    import curses
    import sys
    stdscr = curses.initscr()
    try:
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        # Handle passed file path
        path_arg = sys.argv[1] if len(sys.argv) > 1 else None
        run(stdscr, path_arg)
    finally:
        curses.endwin()
