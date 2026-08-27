def run(stdscr):
    import os
    import sys
    stdscr.clear()
    stdscr.addstr(1, 2, "ReadMe - Instructions")
    stdscr.addstr(3, 2, "How to install new apps:")
    stdscr.addstr(4, 2, "1. Place the app file in the 'Apps' directory")
    stdscr.addstr(5, 2, "2. Restart the system")
    stdscr.addstr(6, 2, "3. The app should now appear in the main menu")
    stdscr.addstr(8, 2, "How to use the main menu:")
    stdscr.addstr(9, 2, "1. Use the w and s keys to navigate the menu")
    stdscr.addstr(10, 2, "2. Press Enter to select an app")
    stdscr.addstr(11, 2, "3. Press Q to exit a app")
    stdscr.addstr(13, 2, "4. Press X to shut down the system")
    
    stdscr.addstr(15, 2, "Press any key to return to the main menu.")
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
