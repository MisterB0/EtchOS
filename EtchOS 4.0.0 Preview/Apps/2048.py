def run(stdscr):
    import curses
    import random
    import time
    def get_logic_line(line):
        points = 0
        new_line = [x for x in line if x != 0]
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i+1]:
                new_line[i] *= 2
                points += new_line[i]
                new_line[i+1] = 0
        new_line = [x for x in new_line if x != 0]
        while len(new_line) < 4:
            new_line.append(0)
        return new_line, points
    def add_new_tile(board):
        empty_indices = [i for i, val in enumerate(board) if val == 0]
        if empty_indices:
            idx = random.choice(empty_indices)
            board[idx] = 4 if random.random() > 0.9 else 2
    def draw_board(board, score):
        stdscr.addstr(1, 1, "=========================")
        stdscr.addstr(2, 1, "│     │     │     │     │")
        stdscr.addstr(3, 1, "=========================")
        stdscr.addstr(4, 1, "│     │     │     │     │")
        stdscr.addstr(5, 1, "=========================")
        stdscr.addstr(6, 1, "│     │     │     │     │")
        stdscr.addstr(7, 1, "=========================")
        stdscr.addstr(8, 1, "│     │     │     │     │")
        stdscr.addstr(9, 1, "=========================")
        stdscr.addstr(10, 1, f"Score: {score}")
        stdscr.addstr(11, 1, "Arrow Keys: Move")
        stdscr.addstr(12, 1, "Q: Quit")
        coords = [
            (2, 2), (2, 8), (2, 14), (2, 20),
            (4, 2), (4, 8), (4, 14), (4, 20),
            (6, 2), (6, 8), (6, 14), (6, 20),
            (8, 2), (8, 8), (8, 14), (8, 20)
        ]
        for i, val in enumerate(board):
            y, x = coords[i]
            s_val = str(val) if val != 0 else "."
            stdscr.addstr(y, x, "     ")
            stdscr.addstr(y, x + (5 - len(s_val)) // 2, s_val)
    def check_game_over(board):
        if 0 in board: return False
        for r in range(4):
            for c in range(3):
                if board[r*4+c] == board[r*4+c+1]: return False
        for c in range(4):
            for r in range(3):
                if board[r*4+c] == board[(r+1)*4+c]: return False
        return True
    stdscr.clear()
    curses.curs_set(0)
    board = [0] * 16
    score = 0
    add_new_tile(board)
    add_new_tile(board)
    draw_board(board, score)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
            continue
        old_board = list(board)
        if key == curses.KEY_LEFT:
            for r in range(4):
                row = board[r*4 : r*4+4]
                new_row, pts = get_logic_line(row)
                score += pts
                board[r*4 : r*4+4] = new_row
        elif key == curses.KEY_RIGHT:
            for r in range(4):
                row = board[r*4 : r*4+4]
                row.reverse()
                new_row, pts = get_logic_line(row)
                score += pts
                new_row.reverse()
                board[r*4 : r*4+4] = new_row
        elif key == curses.KEY_UP:
            for c in range(4):
                col = [board[c], board[c+4], board[c+8], board[c+12]]
                new_col, pts = get_logic_line(col)
                score += pts
                board[c], board[c+4], board[c+8], board[c+12] = new_col
        elif key == curses.KEY_DOWN:
            for c in range(4):
                col = [board[c], board[c+4], board[c+8], board[c+12]]
                col.reverse()
                new_col, pts = get_logic_line(col)
                score += pts
                new_col.reverse()
                board[c], board[c+4], board[c+8], board[c+12] = new_col
        if board != old_board:
            add_new_tile(board)
            draw_board(board, score)
            if check_game_over(board):
                stdscr.addstr(14, 1, "GAME OVER!")
                stdscr.addstr(15, 1, f"Final Score: {score}")
                stdscr.addstr(16, 1, "Press Q to exit")
                while True:
                    if stdscr.getch() in [ord('q'), ord('Q')]:
                        return

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
