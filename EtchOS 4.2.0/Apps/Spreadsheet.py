def run(stdscr, file_path=None):
    import curses
    import os
    import time
    import sys
    import csv
    
    stdscr.clear()
    if file_path:
        path = file_path
    else:
        stdscr.addstr(1, 2, "Spreadsheet Editor", curses.A_BOLD)
        stdscr.addstr(2, 2, "Enter filename (without extension):")
        stdscr.refresh()
        curses.echo()
        fname = stdscr.getstr(3, 2, 40).decode('utf-8').strip()
        curses.noecho()
        if not fname:
            return
        user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "UserFilesTextEditor")
        os.makedirs(user_dir, exist_ok=True)
        path = os.path.join(user_dir, fname + ".csv")

    data = []
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                data = list(reader)
        except Exception:
            data = [["Error reading file"]]
    else:
        data = [["Cell 1-1", "Cell 1-2", "Cell 1-3"]]

    if not data:
        data = [[""]]

    row, col = 0, 0
    while True:
        stdscr.clear()
        term_h, term_w = stdscr.getmaxyx()
        
        stdscr.addstr(0, 2, f"Spreadsheet: {os.path.basename(path)}", curses.A_DIM)
        
        # Draw Header (A, B, C...)
        stdscr.addstr(1, 2, "   " + "   ".join([chr(65+i) for i in range(min(10, term_w//5))]), curses.A_BOLD)
        
        # Draw Data
        for r_idx, row_data in enumerate(data):
            if r_idx + 2 >= term_h - 2: break
            
            # Row number
            stdscr.addstr(2 + r_idx, 2, f"{r_idx+1} ")
            
            # Cells
            for c_idx, cell in enumerate(row_data):
                if 3 + c_idx * 10 >= term_w - 1: break
                
                content = str(cell)[:9]
                if r_idx == row and c_idx == col:
                    stdscr.addstr(2 + r_idx, 3 + c_idx * 10, f"[{content}]", curses.A_REVERSE)
                else:
                    stdscr.addstr(2 + r_idx, 3 + c_idx * 10, f" {content} ")
        
        stdscr.addstr(term_h - 1, 2, "Ctrl-S: save  Ctrl-X: quit  Arrows: move  Enter: edit")
        stdscr.refresh()
        
        ch = stdscr.getch()
        if ch == 24: # Ctrl-X
            return
        if ch == 19: # Ctrl-S
            try:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
                stdscr.addstr(term_h - 2, 2, "Saved successfully!")
                stdscr.refresh()
                time.sleep(0.6)
            except Exception:
                stdscr.addstr(term_h - 2, 2, "Save failed!")
                stdscr.refresh()
                time.sleep(0.6)
            continue
        
        if ch == curses.KEY_UP:
            row = max(0, row - 1)
        elif ch == curses.KEY_DOWN:
            row = min(len(data) - 1, row + 1)
        elif ch == curses.KEY_LEFT:
            col = max(0, col - 1)
        elif ch == curses.KEY_RIGHT:
            col = min(len(data[row]) - 1 if data[row] else 0, col + 1)
        elif ch in (10, 13): # Enter to edit
            # Simple cell editing
            stdscr.addstr(term_h - 2, 2, f"Edit Cell {chr(65+col)}{row+1}: ")
            stdscr.refresh()
            curses.echo()
            new_val = stdscr.getstr().decode('utf-8').strip()
            curses.noecho()
            
            # Expand row if needed
            while len(data[row]) <= col:
                data[row].append("")
            data[row][col] = new_val
            
        # Ensure the current row has enough columns for the cursor
        if not data[row] or col >= len(data[row]):
             while len(data[row]) <= col:
                data[row].append("")

if __name__ == "__main__":
    import curses
    import sys
    stdscr = curses.initscr()
    try:
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        path_arg = sys.argv[1] if len(sys.argv) > 1 else None
        run(stdscr, path_arg)
    finally:
        curses.endwin()
