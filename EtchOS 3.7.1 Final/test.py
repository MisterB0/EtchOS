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


def TextEditor_En():
	# Minimal text editor using `window()` and `safe_addstr()`.
	# - Prompt for filename
	# - Basic multi-line editing (typing, Backspace, Enter)
	# - Arrow navigation
	# - Ctrl+S to save, Ctrl+Q to quit (without saving)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	user_dir = os.path.join(current_dir, "UserFilesTextEditor")
	try:
		os.makedirs(user_dir, exist_ok=True)
	except Exception:
		pass

	# prompt for filename
	stdscr.clear()
	window(6)
	safe_addstr(1, 2, "Text Editor")
	safe_addstr(2, 2, "Enter filename (without extension):")
	stdscr.refresh()
	curses.echo()
	try:
		fname = stdscr.getstr(3, 2, 40).decode('utf-8').strip()
	finally:
		try:
			curses.noecho()
		except Exception:
			pass

	if not fname:
		return

	path = os.path.join(user_dir, fname + ".txt")
	# load if exists
	if os.path.exists(path):
		with open(path, 'r', encoding='utf-8') as f:
			lines = [l.rstrip('\n') for l in f.readlines()]
		if not lines:
			lines = ['']
	else:
		lines = ['']

	# editor state
	top = 0
	cursor_r = 0
	cursor_c = 0

	while True:
		stdscr.clear()
		# compute box height based on terminal
		term_h, term_w = stdscr.getmaxyx()
		h = min( max(6, len(lines) + 4), term_h - 2)
		window(h)
		# draw visible lines inside box (offset by 1)
		max_rows = h - 3
		for i in range(max_rows):
			idx = top + i
			if idx >= len(lines):
				break
			safe_addstr(1 + i, 2, lines[idx])

		# status/instructions
		safe_addstr(h - 1, 2, "Ctrl-S: save  Ctrl-X: quit  Arrows to move")
		# place cursor
		vis_r = cursor_r - top
		if 0 <= vis_r < max_rows:
			try:
				stdscr.move(1 + vis_r, 2 + cursor_c)
			except Exception:
				pass

		stdscr.refresh()
		ch = stdscr.getch()
		# Ctrl-X quit without saving
		if ch == 24:
			return
		# Ctrl-S save
		if ch == 19:
			try:
				with open(path, 'w', encoding='utf-8') as f:
					f.write('\n'.join(lines))
				safe_addstr(h - 1, 2, "Saved.")
				stdscr.refresh()
				time.sleep(0.6)
			except Exception:
				safe_addstr(h - 1, 2, "Save failed.")
				stdscr.refresh()
				time.sleep(0.8)
			continue
		# navigation
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
				if cursor_r >= top + max_rows:
					top = cursor_r - max_rows + 1
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
			if cursor_r >= top + max_rows:
				top = cursor_r - max_rows + 1
			continue

		# Backspace
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

		# Enter -> new line
		if ch in (10, 13):
			rest = lines[cursor_r][cursor_c:]
			lines[cursor_r] = lines[cursor_r][:cursor_c]
			lines.insert(cursor_r + 1, rest)
			cursor_r += 1
			cursor_c = 0
			if cursor_r >= top + max_rows:
				top = cursor_r - max_rows + 1
			continue

		# printable
		if 32 <= ch <= 126:
			lines[cursor_r] = lines[cursor_r][:cursor_c] + chr(ch) + lines[cursor_r][cursor_c:]
			cursor_c += 1
			continue

		# ignore other keys
		continue

def run():
	"""Default run for test harness: show help centre."""
	TextEditor_En()


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



