#!/usr/bin/env python3
"""
Lightweight test harness for EtchOS UI pieces.

Put any helper functions or UI pieces you want to develop here.
Define a `run()` function (no args) that will be executed inside the
curses `main(stdscr)` context. This file provides `safe_addstr`,
`window(height)` and a `main` harness so you can test code and then
copy functions to `main.py` as needed.

Usage: run this file directly. Edit `run()` below to call your code.
"""
import curses
from curses import wrapper
import time
import os
import traceback

# global stdscr used by helpers
stdscr = None

def safe_addstr(y, x, text):
	"""Write text safely inside the terminal bounds."""
	global stdscr
	if stdscr is None:
		return
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
		stdscr.addstr(y, x, s)
	except curses.error:
		try:
			stdscr.addnstr(y, x, s, avail)
		except Exception:
			pass

def window(height):
	"""Draw a simple fixed-position box like in `main.py`.

	Keeps the exact original feel so copying code to `main.py` works.
	"""
	safe_addstr(0, 0, "==========================================================")
	for i in range(1, height - 1):
		safe_addstr(i, 0, "│                                                        │")
	safe_addstr(height - 1, 0, "==========================================================")


def EtchShell_En():
    # Terminal with EtchShell Advanced functions; explanations to linux and windows cmd commands; auto complete feature
    height = 16
    output_buffer = ["EtchShell v1.0", "Type 'help' for commands."]
    current_input = ""

    # Command definitions
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

    # Explanations for specific commands (cross-platform help)
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
        window(height)

        # Display output buffer (scroll)
        max_lines = height - 3
        visible_lines = output_buffer[-(max_lines-1):]

        for i, line in enumerate(visible_lines):
            safe_addstr(1 + i, 2, line)

        # Prompt
        user = os.getenv('USER') or os.getenv('USERNAME') or 'user'
        cwd = os.getcwd()
        if len(cwd) > 15: cwd = "..." + cwd[-12:]
        prompt = f"{user}@{cwd} $ {current_input}"
        safe_addstr(height - 2, 2, prompt)

        stdscr.refresh()

        key = stdscr.getch()

        if key in (10, 13): # Enter
            output_buffer.append(f"$ {current_input}")
            parts = current_input.strip().split()
            if parts:
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == "exit":
                    break
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

        elif key == 9: # Tab
            parts = current_input.split()
            if parts and len(parts) == 1:
                matches = [c for c in commands if c.startswith(parts[0])]
                if len(matches) == 1:
                    current_input = matches[0] + " "

        elif 32 <= key <= 126:
            current_input += chr(key)
	
def run():
	"""Default run for test harness: show help centre."""
	EtchShell_En()


def main(stdscr_local):
	"""Curses entry point used by `wrapper(main)`.

	Sets global `stdscr` and runs `run()`.
	"""
	global stdscr
	stdscr = stdscr_local
	try:
		curses.curs_set(0)
	except Exception:
		pass
	stdscr.keypad(True)
	stdscr.clear()
	run()
	stdscr.refresh()
	stdscr.getch()
	stdscr.keypad(False)
	try:
		curses.curs_set(1)
	except Exception:
		pass

if __name__ == "__main__":
	# add logging to help debug silent failures in terminals
	try:
		with open('test.log', 'a', encoding='utf-8') as f:
			f.write('=== test.py start ===\n')
		wrapper(main)
		with open('test.log', 'a', encoding='utf-8') as f:
			f.write('=== test.py finished normally ===\n')
	except Exception:
		tb = traceback.format_exc()
		with open('test.log', 'a', encoding='utf-8') as f:
			f.write('=== test.py exception ===\n')
			f.write(tb + '\n')
		# also print to console so user sees it in PowerShell
		print('test.py crashed; details written to test.log')
		print(tb)
