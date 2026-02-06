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
import random 

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


# Test Here

def Test_En():
    safe_addstr(2, 0, "Hello World!")

def run():
	"""Default run for test harness: show help centre."""
	Test_En()

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
