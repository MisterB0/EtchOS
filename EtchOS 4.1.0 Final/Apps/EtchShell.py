def run(stdscr):
    import curses
    import os
    stdscr.clear()
    height = 16
    output_buffer = ["EtchShell v1.0", "Type 'help' for commands."]
    current_input = ""
    commands = {
        "help": "Show this help",
        "clear": "Clear screen",
        "exit": "Exit terminal",
        "ls": "List files (Linux)",
        "dir": "List files (Windows)",
        "cd": "Change directory",
        "pwd": "Print working directory",
        "whoami": "Show current user",
        "explain": "Explain a command (e.g. 'explain ls')"
    }
    explanations = {
        "ls": "Lists directory contents. Equivalent to 'dir' in Windows.",
        "dir": "Lists directory contents. Equivalent to 'ls' in Linux.",
        "cd": "Changes the current working directory.",
        "pwd": "Prints the current working directory path.",
        "clear": "Clears the terminal screen. Equivalent to 'cls' in Windows.",
        "whoami": "Displays the current username.",
        "mkdir": "Creates a new directory.",
        "rm": "Removes a file."
    }
    while True:
        stdscr.clear()
        max_lines = height - 3
        visible_lines = output_buffer[-(max_lines-1):]
        for i, line in enumerate(visible_lines):
            stdscr.addstr(1 + i, 2, line)
        user = os.getenv('USER') or os.getenv('USERNAME') or 'user'
        cwd = os.getcwd()
        if len(cwd) > 15: cwd = "..." + cwd[-12:]
        prompt = f"{user}@{cwd} $ {current_input}"
        stdscr.addstr(height - 2, 2, prompt)
        stdscr.refresh()
        key = stdscr.getch()
        if key in (10, 13):
            output_buffer.append(f"$ {current_input}")
            parts = current_input.strip().split()
            if parts:
                cmd = parts[0].lower()
                args = parts[1:]
                if cmd == "exit":
                    return
                elif cmd == "clear":
                    output_buffer = []
                elif cmd == "help":
                    output_buffer.append("Commands: " + ", ".join(commands.keys()))
                elif cmd in ["ls", "dir"]:
                    try:
                        for f in os.listdir("."):
                            prefix = "[DIR] " if os.path.isdir(f) else "      "
                            output_buffer.append(prefix + f)
                    except Exception as e:
                        output_buffer.append(str(e))
                elif cmd == "cd":
                    if args:
                        try:
                            os.chdir(args[0])
                        except Exception as e:
                            output_buffer.append(str(e))
                    else:
                        output_buffer.append(os.getcwd())
                elif cmd == "pwd":
                    output_buffer.append(os.getcwd())
                elif cmd == "whoami":
                    output_buffer.append(user)
                elif cmd == "explain":
                    if args and args[0] in explanations:
                        output_buffer.append(f"{args[0]}: {explanations[args[0]]}")
                    elif args:
                        output_buffer.append(f"No explanation for {args[0]}")
                    else:
                        output_buffer.append("Usage: explain <command>")
                else:
                    output_buffer.append(f"Unknown command: {cmd}")
            current_input = ""
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            current_input = current_input[:-1]
        elif key == 9:
            parts = current_input.split()
            if parts and len(parts) == 1:
                matches = [c for c in commands if c.startswith(parts[0])]
                if len(matches) == 1:
                    current_input = matches[0] + " "
        elif 32 <= key <= 126:
            current_input += chr(key)

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
