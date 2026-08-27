def run(stdscr):
    import os
    import sys
    import platform
    stdscr.clear()
    stdscr.addstr(1, 2, "System Information", curses.A_BOLD | curses.A_UNDERLINE)
    stdscr.addstr(3, 2, f"OS Name: {platform.system()} {platform.release()}")
    stdscr.addstr(4, 2, f"Architecture: {platform.machine()}")
    stdscr.addstr(5, 2, f"Host: {platform.node()}")
    stdscr.addstr(6, 2, f"Current Directory: {os.getcwd()}")
    stdscr.addstr(7, 2, f"User: {os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'}")
    stdscr.addstr(8, 2, f"Python Version: {sys.version.split()[0]}")
    stdscr.addstr(10, 2, "Press any key to return to the main menu.")
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
