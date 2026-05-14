def run(stdscr):
    import os
    import sys
    stdscr.clear()
    stdscr.addstr(1, 2, "System Information")
    stdscr.addstr(3, 2, f"Operating System: {os.name}")
    stdscr.addstr(4, 2, f"Current Directory: {os.getcwd()}")
    stdscr.addstr(5, 2, f"User: {os.getenv('USER') or os.getenv('USERNAME')}")
    stdscr.addstr(6, 2, f"Python Version: {sys.version.split()[0]}")
    stdscr.addstr(7, 2, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

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
