import curses
import time 

language = "En"

def etch_txt(main):
    def wrapper(stdscr):
        curses.curs_set(0)
        stdscr.clear()

        buffer = []

        def etch(line, *args, sep=" "):
            text = sep.join(map(str, args))

            index = line - 1  # 1-basiert
            while len(buffer) <= index:
                buffer.append("")

            buffer[index] = text

            stdscr.clear()
            h, w = stdscr.getmaxyx()
            for i, l in enumerate(buffer):
                if i >= h:
                    break
                stdscr.addstr(i, 0, l[:w-1])
            stdscr.refresh()

        main(etch)
        stdscr.getch()

    curses.wrapper(wrapper)


def clear(etch, lines=20):
    for i in range(1, lines + 1):
        etch(i, "")


# ============ MAIN ============
def main(etch):
    clear(etch)


    def Start(language):
        etch(1, "░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░ ")
        etch(2, "░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        etch(3, "░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        etch(4, "░▒▓██████▓▒░    ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  ")
        etch(5, "░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ ")
        etch(6, "░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ ")
        etch(7, "░▒▓████████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░  ")

        etch(7, ".")
        time.sleep(0.5)
        etch(7, "..")
        time.sleep(0.5)
        etch(7, "...")
        time.sleep(0.5)
        clear(etch)
        etch(4, "Welcome to EtchOS!")
        time.sleep(2)
        etch(2, "In what language do you want to continue?")
        etch(3, "En - English")
        etch(4, "De - Deutsch")
        etch(5, "Input:")
        language = input()
        
    

    def Menu(language):





    Start(language)
    
    
    

etch_txt(main)
