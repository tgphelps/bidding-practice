#!/usr/bin/env python3

"""
quiz.py: Display questions and check answers

Usage:
    quiz.py [-k <key>] QUESTIONS
    quiz.py   --version
    quiz.py   --help

Options and commands:
    --version          Show version and exit.
    -h --help          Show this message and exit.
    -k <key>           Show only questions with this keyword.
"""


import curses
import logging
import sys
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
ROW_BID_BOX = 17
COL_BID_BOX = 40
ROW_DIVIDER = 25
ROW_RESULT = 26
ROW_EXPL = 27
ROW_BOTTOM = 32
ROW_AUCTION = 11


class MyError(Exception):
    pass


class Window:
    scr: curses.window
    rows: int
    cols: int

    def __init__(self, win: curses.window):
        self.scr = win
        curses.mousemask(1)
        self.rows, self.cols = self.scr.getmaxyx()


def main(scr) -> None:
    logging.basicConfig(level=LOG_LEVEL, filename='LOG.txt',
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.debug(f'quiz.py {VERSION}')

    win = Window(scr)
    logging.debug(f'screen rows: {win.rows} cols: {win.cols}')
    if win.rows < 35 or win.cols < 80:
        logging.fatal('Screen must be at least 40x80.')
        raise MyError('Screen must be at least 40x80')
    keyword = ''
    args = docopt.docopt(__doc__, version='0.01')
    # print(args)
    fname = args['QUESTIONS']
    if args['-k']:
        keyword = args['-k']
    with open(fname) as f:
        while True:
            ex = Exercise(f)
            if not ex.valid:
                break
            if keyword != '':
                if keyword not in ex.keys:
                    continue
            want_more = ask_question(ex, win)
            if not want_more:
                break


def ask_question(ex: Exercise, win: Window) -> bool:
    logging.debug('New question')
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    win.scr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    win.scr.clear()
    show_screen_top(ex, win.scr, ROW_TOP)
    show_hand(ex, win.scr, ROW_HAND)
    show_bid_box(win.scr, ROW_BID_BOX, COL_BID_BOX)
    win.scr.addstr(ROW_DIVIDER, 0, '------------------------------')
    # win.scr.addstr(ROW_BOTTOM, 0, '<Continue>  <Quit>')
    win.scr.refresh()

    for i, answer in enumerate(ex.answers):
        logging.debug('Next auction.')
        show_auction(win.scr, ROW_AUCTION, ex.auction)
        bid = get_bid(win.scr)
        win.scr.addstr(ROW_RESULT, 0, bid)
        if bid == ex.answers[i].bid:
            win.scr.addstr(ROW_RESULT, 6, 'Yes  ')
        else:
            win.scr.addstr(ROW_RESULT, 6, 'WRONG')
            show_explanation(win.scr, ROW_EXPL, ex.answers[i].expl)
        logging.debug('wait for click')
        _, _ = get_mouse_click(win.scr)
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
    for bid in auction:
        if bid.startswith('*'):
            break
        next.append(bid)
    n = len(next)
    auction[n] = auction[n][1:]
    next.append('?')
    # scr.addstr(row, 0, ' '.join(next))
    i = 0
    while i < len(next):
        this_line = next[i:i + 4]
        s = ''
        for bid in this_line:
            s += f'{bid:6}'
        scr.addstr(row + i // 4, 0, s)
        i += 4


def get_bid(scr: curses.window) -> str:
    logging.debug('get_bid')
    top = ROW_BID_BOX
    while True:
        x, y = get_mouse_click(scr)
        logging.debug(f'click y: {y}  x: {x}')
        if x >= 39 and x <= 57 and y >= top + 2 and y <= top + 8:
            bid = level_and_suit(y, x)
            logging.debug(f'bid was: {bid}')
            return bid
        if y == top + 9 and x >= 39 and x <= 54:
            bid = pass_dbl_rdbl(x)
            logging.debug(f'bid was: {bid}')
            return bid


SUITS = ('C', 'D', 'H', 'S', 'NT')


def level_and_suit(y: int, x: int) -> str:
    level = 7 - (y - ROW_BID_BOX - 2)
    suit = (x - COL_BID_BOX) // 4
    return str(level) + SUITS[suit]


CALLS = ('PASS', 'DBL', 'RDBL')


def pass_dbl_rdbl(x: int) -> str:
    offset = (x - COL_BID_BOX) // 6
    return CALLS[offset]


def show_explanation(scr: curses.window, row: int, expl: list[str]) -> None:
    for i in range(4):
        scr.addstr(row + i, 0, 80 * ' ')
    for i, line in enumerate(expl):
        scr.addstr(row + i, 0, line)


click_count = 0


def get_mouse_click(scr: curses.window) -> tuple[int, int]:
    global click_count
    x = 0
    y = 0
    try:
        c = scr.getch()
        if c == ord('q'):
            sys.exit(1)
        if c == curses.KEY_MOUSE:
            click_count += 1
            _, x, y, _, _ = curses.getmouse()
            logging.debug(f'mouse: y: {y}  x: {x}')
            debug(scr, f'click {click_count}  y: {y}, x: {x}')
    except curses.error:
        logging.debug('curses error')
        raise MyError('curses error')
    return x, y


def get_user_bid() -> str:
    ans = input('Your bid? ')
    return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


def debug(scr: curses.window, msg: str) -> None:
    scr.move(ROW_BOTTOM, 0)
    scr.clrtoeol()
    scr.addstr(ROW_BOTTOM, 0, msg)


if __name__ == '__main__':
    curses.wrapper(main)
