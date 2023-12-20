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
    # clear screen
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    win.scr.bkgd(' ', curses.color_pair(1))  # | curses.A_BOLD)
    # show info lines
    # show hand
    win.scr.refresh()
    errors = 0
    try:
        c = win.scr.getch()
        if c == ord('q'):
            sys.exit(1)
        if c == curses.KEY_MOUSE:
            pass
            # read_mouse()
        if c == curses.KEY_RESIZE:
            pass
            # win.resize()
            # resized += 1
    except curses.error:
        errors += 1
        logging.debug('curses error')
        pass
    # for _ in range(len(answers)):
    #     show auction out to first '*', ending with '?'.
    #     remove the '*'
    #     get answer
    #     show yes/no
    #     show explanation if wrong
    # ask if we should continue
    # return True if yes, False if no
    return True


# This tells how far to shift the auction so North's bids are on the left.
BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


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
