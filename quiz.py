#!/usr/bin/env python3

"""
quiz.py: Display bidding exercises and check answers

Usage:
    quiz.py [-k <key>] [-s] EXERCISES...
    quiz.py   --version
    quiz.py   --help

Options and commands:
    --version          Show version and exit.
    -h --help          Show this message and exit.
    -k <key>           Show only exercises with this keyword.
    -s                 Sequential. Don't shuffle exercises before showing.
"""


import curses
import logging
import random
# import sys
import docopt  # type: ignore
from exercise import Exercise


VERSION = '0.01'
LOG_LEVEL = 'DEBUG'

SUIT_SYMS = "\u2660\u2665\u2666\u2663"  # spade, heart, diamond, club
C = SUIT_SYMS[3]
D = SUIT_SYMS[2]
H = SUIT_SYMS[1]
S = SUIT_SYMS[0]

ROW_TOP = 1
ROW_HAND = 18
ROW_BID_BOX = 16
COL_BID_BOX = 40
ROW_DIVIDER = 25
ROW_RESULT = 26
ROW_EXPL = 27
ROW_HINT = 29
ROW_DEBUG = 35
ROW_AUCTION = 11

BG_COLOR1 = curses.COLOR_RED
BG_COLOR2 = curses.COLOR_BLUE
FG_COLOR = curses.COLOR_WHITE


class MyError(Exception):
    pass


class Globals:
    click_count: int
    exercises: list[Exercise]
    total_answers: int
    total_right: int
    count: int


g = Globals()
g.click_count = 0
g.exercises = []
g.total_answers = 0
g.total_right = 0
g.count = 0


class Window:
    scr: curses.window
    rows: int
    cols: int

    def __init__(self, win: curses.window):
        self.scr = win
        curses.mousemask(1)
        self.rows, self.cols = self.scr.getmaxyx()


def main(scr) -> None:
    logging.basicConfig(level=LOG_LEVEL, filename='LOG.txt', filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.debug(f'quiz.py {VERSION}')

    win = Window(scr)
    logging.debug(f'screen rows: {win.rows} cols: {win.cols}')
    if win.rows < 40 or win.cols < 80:
        logging.fatal('Screen must be at least 40x80.')
        raise MyError('Screen must be at least 40x80')
    keyword = ''
    args = docopt.docopt(__doc__, version='0.01')
    logging.debug(args)
    if args['-k']:
        keyword = args['-k']
    g.exercises = read_exercises(args['EXERCISES'])
    if not args['-s']:
        random.shuffle(g.exercises)
    for ex in g.exercises:
        if keyword != '' and keyword not in ex.keys:
            continue
        want_more = show_exercise(ex, win)
        if not want_more:
            break
    curses.endwin()

    pct = float(g.total_right / g.total_answers)
    msg = f'Total: {g.total_answers}  Correct: {g.total_right}  Score: {100 * pct:2.0f}% '
    print(msg)


def read_exercises(files: list[str]) -> list[Exercise]:
    ex_list: list[Exercise] = []
    for fname in files:
        logging.debug(f'Reading file {fname}')
        with open(fname) as f:
            while True:
                ex = Exercise(f)
                logging.debug('Return from Exercise()')
                if not ex.valid:
                    break
                logging.debug('Read 1 exercise.')
                ex_list.append(ex)
    logging.debug(f'Total exercises read: {len(ex_list)}')
    return ex_list


def show_exercise(ex: Exercise, win: Window) -> bool:
    logging.debug('New exercise')
    if g.count % 2 == 0:
        curses.init_pair(1, FG_COLOR, BG_COLOR1)
    else:
        curses.init_pair(1, FG_COLOR, BG_COLOR2)
    g.count += 1
    win.scr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    win.scr.clear()

    show_screen_top(ex, win.scr, ROW_TOP)
    show_hand(ex, win.scr, ROW_HAND)
    show_bid_box(win.scr, ROW_BID_BOX, COL_BID_BOX)
    win.scr.addstr(ROW_DIVIDER, 0, '------------------------------')
    win.scr.addstr(ROW_HINT, 0, "Click to bid, ' ' to continue, 'q' to quit")
    win.scr.refresh()

    for i, answer in enumerate(ex.answers):
        g.total_answers += 1
        logging.debug('Next auction.')
        show_auction(win.scr, ROW_AUCTION, ex.auction)
        bid = get_bid(win.scr)
        win.scr.addstr(ROW_RESULT, 0, bid)
        if bid == ex.answers[i].bid:
            win.scr.addstr(ROW_RESULT, 6, 'Yes  ')
            g.total_right += 1
        else:
            win.scr.addstr(ROW_RESULT, 6, 'WRONG')
            show_explanation(win.scr, ROW_EXPL, ex.answers[i].expl)
        pct = float(g.total_right / g.total_answers)
        msg = f'Total: {g.total_answers}  Correct: {g.total_right}  Score: {100 * pct:2.0f} '
        win.scr.addstr(ROW_RESULT, 15, msg)
        logging.debug('wait for click')
        _, _, ch = get_mouse_click(win.scr)
        if ch == ord('q'):
            return False
    return True


def show_screen_top(ex: Exercise, scr: curses.window, row: int) -> None:
    for i, line in enumerate(ex.info):
        scr.addstr(row + i, 0, line)
    scr.addstr(row + 5, 0, '--------------------------------')
    s = f'Dealer: {ex.dealer}  Vulnerable: {ex.vulnerable}'
    scr.addstr(row + 6, 0, s)
    scr.addstr(row + 8, 0, 'North East  South West')
    scr.addstr(row + 9, 0, '----- ----- ----- -----')


def show_hand(ex: Exercise, scr: curses.window, row: int) -> None:
    scr.addstr(row, 0, '---------- Your hand ----------')
    row += 2
    for i, suit in enumerate(ex.hand.suits):
        scr.addstr(row + i, 0, f'{SUIT_SYMS[i]} {suit}')


def show_bid_box(scr: curses.window, row: int, col: int) -> None:
    scr.addstr(row, col, '    BID BOX')
    scr.addstr(row + 1, col, '--------------------')
    scr.addstr(row + 2, col, f'7{C}  7{D}  7{H}  7{S}  7NT')
    scr.addstr(row + 3, col, f'6{C}  6{D}  6{H}  6{S}  6NT')
    scr.addstr(row + 4, col, f'5{C}  5{D}  5{H}  5{S}  5NT')
    scr.addstr(row + 5, col, f'4{C}  4{D}  4{H}  4{S}  4NT')
    scr.addstr(row + 6, col, f'3{C}  3{D}  3{H}  3{S}  3NT')
    scr.addstr(row + 7, col, f'2{C}  2{D}  2{H}  2{S}  2NT')
    scr.addstr(row + 8, col, f'1{C}  1{D}  1{H}  1{S}  1NT')
    scr.addstr(row + 9, col, 'PASS  DBL   RDBL')


def show_auction(scr: curses.window, row: int, auction: list[str]) -> None:
    next = []
    # Append bids to 'next' until we find one that starts with '*'.
    for bid in auction:
        if bid.startswith('*'):
            break
        next.append(bid)
    n = len(next)
    auction[n] = auction[n][1:]  # remove the '*' from this bid
    next.append('?')
    # scr.addstr(row, 0, ' '.join(next))
    i = 0
    # Print the auction, 4 bids on each line.
    while i < len(next):
        this_line = next[i:i + 4]
        s = ''
        for bid in this_line:
            s += f'{bid:6}'
        scr.addstr(row + i // 4, 0, s)
        i += 4


def get_bid(scr: curses.window) -> str:
    "Translate a bidbox click to a bid."
    logging.debug('get_bid')
    top = ROW_BID_BOX
    left = COL_BID_BOX
    # Loop until he clicks somewhere in the bidbox.
    while True:
        x, y, ch = get_mouse_click(scr)
        logging.debug(f'click y: {y}  x: {x}')
        if x >= left and x < left + 20 and y >= top + 2 and y < top + 7 + 2:
            bid = level_and_suit(y, x)
            logging.debug(f'bid was: {bid}')
            return bid
        if y == top + 9 and x >= 39 and x <= 54:
            bid = pass_dbl_rdbl(x)
            logging.debug(f'bid was: {bid}')
            return bid


SUITS = ('C', 'D', 'H', 'S', 'NT')


def level_and_suit(y: int, x: int) -> str:
    "Translate click to <level><suit>."
    level = 7 - (y - ROW_BID_BOX - 2)
    suit = (x - COL_BID_BOX) // 4
    return str(level) + SUITS[suit]


CALLS = ('PASS', 'DBL', 'RDBL')


def pass_dbl_rdbl(x: int) -> str:
    "Translate click to PASS, DBL, or RDBL."
    offset = (x - COL_BID_BOX) // 6
    return CALLS[offset]


def show_explanation(scr: curses.window, row: int, expl: list[str]) -> None:
    for i in range(4):
        scr.addstr(row + i, 0, 80 * ' ')
    for i, line in enumerate(expl):
        scr.addstr(row + i, 0, line)


def get_mouse_click(scr: curses.window) -> tuple[int, int, int]:
    " return x, y, char"
    x = -1
    y = -1
    try:
        ch = scr.getch()
        if ch == ord('q'):  # XXX Probably not good code.
            return x, y, ch
        if ch == curses.KEY_MOUSE:
            g.click_count += 1
            _, x, y, _, _ = curses.getmouse()
            logging.debug(f'mouse: y: {y}  x: {x}')
            debug(scr, f'click {g.click_count}  y: {y}, x: {x}')
    except curses.error:
        logging.debug('curses error')
        raise MyError('curses error')
    return x, y, ch  # If he hit a key, (x,y) will be (-1,-1).


# def get_user_bid() -> str:
#     ans = input('Your bid? ')
#     return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


def debug(scr: curses.window, msg: str) -> None:
    "Write a message to the bottom line on screen."
    scr.move(ROW_DEBUG, 0)
    scr.clrtoeol()
    scr.addstr(ROW_DEBUG, 0, 'debug: ' + msg)


if __name__ == '__main__':
    curses.wrapper(main)
