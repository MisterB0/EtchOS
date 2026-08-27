def run(stdscr):
    import curses
    import time
    stdscr.clear()
    stdscr.addstr(1, 2, "Calculator", curses.A_BOLD)
    stdscr.addstr(3, 2, "Enter calculation (e.g. 2 + 2):")
    stdscr.refresh()
    
    # Instead of using getstr which can be clunky, we use a simple loop for input
    # to maintain better control and visual feedback.
    input_text = ""
    curses.echo()
    stdscr.move(4, 2)
    while True:
        ch = stdscr.getch()
        if ch in (10, 13): # Enter
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if len(input_text) > 0:
                input_text = input_text[:-1]
                stdscr.delch()
        elif 32 <= ch <= 126:
            input_text += chr(ch)
    curses.noecho()
    
    s = input_text.strip()
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
        stdscr.addstr(5, 2, f"Result: {result}", curses.A_BOLD)
        stdscr.addstr(6, 2, "Press any key to continue.")
        stdscr.refresh()
        stdscr.getch()
    except Exception as e:
        stdscr.addstr(5, 2, f"Error: {e}", curses.A_REVERSE)
        stdscr.refresh()
        time.sleep(2)
        run(stdscr)

if __name__ == "__main__":
    import curses
    stdscr = curses.initscr()
    try:
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        run(stdscr)
    finally:
        curses.endwin()
