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


def HelpCentre_En():
	
	current_dir = os.path.dirname(os.path.abspath(__file__))

	# draw help box and populate entries; keep content inside box
	stdscr.clear()
	height = 10
	window(height)
	base_y = 0
	content_x = 2
	safe_addstr(base_y + 1, content_x, "Help Centre")
	safe_addstr(base_y + 3, content_x, "Articles:")
	safe_addstr(base_y + 4, content_x + 2, "1. Getting Started")
	safe_addstr(base_y + 5, content_x + 2, "2. Troubleshooting")
	safe_addstr(base_y + 6, content_x + 2, "3. Update Instructions and Nodes")
	safe_addstr(8, 2, "Choose an article by number (or any other key to return).")
	stdscr.refresh()

	choice = stdscr.getch()
	if choice == ord('1'):
		file_path = os.path.join(current_dir, "Wiki", "Article 1.txt")
	elif choice == ord('2'):
		file_path = os.path.join(current_dir, "Wiki", "Article 2.txt")
	elif choice == ord('3'):
		file_path = os.path.join(current_dir, "Wiki", "Article 3.txt")
	else:
		# return to caller (test harness) silently
		return

	# try to open and display the article if present
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()
	except FileNotFoundError:
		safe_addstr(9, 2, "Article not found. Press any key to return.")
		stdscr.refresh()
		stdscr.getch()
		return

	# display article contents with simple scrolling and quit 
	lines = content.splitlines()
	top = 0
	max_rows = curses.LINES - 5
	content_offset = 1  # move displayed article down by one line
	while True:
		stdscr.clear()
		window(min(max_rows + 2, curses.LINES - 1))
		for i in range(max_rows):
			idx = top + i 
			if idx >= len(lines):
				break
			# display each line one row lower
			safe_addstr(i + content_offset, 1, lines[idx])
		# instruction line (moved down by same offset)
		safe_addstr(max_rows + content_offset, 0, "-- Press Up/Down or k/j to scroll, q or Esc to return --")
		stdscr.refresh()
		key = stdscr.getch()
		if key in (ord('q'), 27):
			break
		elif key in (curses.KEY_DOWN, ord('j')):
			if top + max_rows < len(lines):
				top += 1
		elif key in (curses.KEY_UP, ord('k')):
			if top > 0:
				top -= 1
		elif key in (curses.KEY_NPAGE,):
			# page down
			top = min(len(lines) - max_rows, top + max_rows)
		elif key in (curses.KEY_PPAGE,):
			# page up
			top = max(0, top - max_rows)
    
    


def run():
    """Default run for test harness: show help centre."""
    HelpCentre_En()


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



