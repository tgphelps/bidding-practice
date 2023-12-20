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

ROW_TOP = 1
ROW_HAND = 18
ROW_BID_BOX = 18
COL_BID_BOX = 40
ROW_DIVIDER = 25
ROW_RESULT = 26
ROW_EXPL = 27
ROW_BOTTOM = 32
ROW_AUCTION = 11


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
        sys.exit(1)
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
    logging.debug('asking...')
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    win.scr.bkgd(' ', curses.color_pair(1))  # | curses.A_BOLD)
    win.scr.clear()
    show_screen_top(ex, win.scr, ROW_TOP)
    show_hand(ex, win.scr, ROW_HAND)
    show_bid_box(win.scr, ROW_BID_BOX, COL_BID_BOX)
    win.scr.addstr(ROW_DIVIDER, 0, '------------------------------')
    win.scr.addstr(ROW_BOTTOM, 0, '<Continue>  <Quit>')
    win.scr.refresh()

    for i, answer in enumerate(ex.answers):
        show_auction(win.scr, ROW_AUCTION)
        bid = get_bid(win.scr)
        if bid == ex.answers[i].bid:
            win.scr.addstr(ROW_RESULT, 0, 'Yes  ')
        else:
            win.scr.addstr(ROW_RESULT, 0, 'WRONG')
            show_explanation(win.scr, ROW_EXPL, ex.answers[i].expl)
        try:
            c = win.scr.getch()
            if c == ord('q'):
                sys.exit(1)
            if c == curses.KEY_MOUSE:
                pass
                # read_mouse()
        except curses.error:
            logging.debug('curses error')
            pass
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
        scr.addstr(row + i, 0, suit)


def show_bid_box(scr: curses.window, row: int, col: int) -> None:
    scr.addstr(row, col, '    BID BOX')
    scr.addstr(row + 1, col, '--------------------')
    scr.addstr(row + 2, col, '7C  7D  7H  7S  7NT')
    scr.addstr(row + 3, col, '6C  6D  6H  6S  6NT')
    scr.addstr(row + 4, col, '5C  5D  5H  5S  5NT')
    scr.addstr(row + 4, col, '4C  4D  4H  4S  4NT')
    scr.addstr(row + 5, col, '3C  3D  3H  3S  3NT')
    scr.addstr(row + 6, col, '2C  2D  2H  2S  2NT')
    scr.addstr(row + 7, col, '1C  1D  1H  1S  1NT')
    scr.addstr(row + 8, col, 'PASS  DBL   RDBL')


def show_auction(scr: curses.window, row: int) -> None:
    pass


def get_bid(scr: curses.window) -> str:
    return 'P'


def show_explanation(scr: curses.window, row: int, expl: list[str]) -> None:
    for i in range(4):
        scr.addstr(row + i, 0, 80 * ' ')
    for i, line in enumerate(expl):
        scr.addstr(row + i, 0, line)


# This tells how far to shift the auction so North's bids are on the left.
# BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


# def normalize_auction(qu: question.Question) -> None:
#     # Normalize auction, so North's bids are on the left.
#     bids = qu.auction
#     # bids.append('?')
#     if qu.dealer != 'n':
#         count = BID_PADDING[qu.dealer]
#         for i in range(count):
#             bids.insert(0, '-')


# def update_auction(qu: question.Question, step: question.Step) -> None:
#     for bid in step.auction:
#         qu.auction.append(bid)
#     qu.auction.append('?')


# def show_auction(qu: question.Question) -> None:
#     for i in range(15):
#         print()
#     print('-----------------------------')
#     print('\nVulnerability:', qu.vulnerable)
#     print(f'Dealer: {qu.dealer}\n')
#     print('North   East  South   West')
#     print('------ ------ ------ ------')
#     auc = qu.auction
#     i = 0
#     while i < len(auc):
#         bids = [x.ljust(6) for x in auc[i:i+4]]
#         print(' '.join(bids))
#         i += 4
#     print('-----------------------------')


def get_user_bid() -> str:
    ans = input('Your bid? ')
    return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


if __name__ == '__main__':
    curses.wrapper(main)
