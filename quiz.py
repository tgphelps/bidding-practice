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


import sys
import docopt  # type: ignore
from typing import TextIO, Optional
import question


def main() -> None:
    keyword = ''
    args = docopt.docopt(__doc__, version='0.01')
    # print(args)
    fname = args['QUESTIONS']
    if args['-k']:
        keyword = args['-k']
    with open(fname) as f:
        print()
        while True:
            qu = read_question(f)
            if not qu:
                break
            if keyword != '':
                if keyword not in qu.keywords:
                    continue
            ask_question(qu)


def read_question(f: TextIO) -> Optional[question.Question]:
    line = question.get_line(f)
    # print('Reading question...')
    if line == 'Question':
        return question.Question(f)
    else:
        if line != 'End':
            print('line:', line)
            assert False
        return None


def ask_question(qu: question.Question) -> None:
    normalize_auction(qu)
    for step in qu.steps:
        print('step...')
        update_auction(qu, step)
        show_auction(qu)
        qu.hand.print()
        print()
        ans = get_user_bid()
        if ans == step.answer:
            print('Correct')
        else:
            print('No')
            print_explanation(step.expl)
        ans = input("Continue? ('n' to quit) ")
        if ans == 'n':
            print('Exiting.')
            sys.exit(0)
        # Going to next step
        qu.auction.remove('?')


# This tells how far to shift the auction so North's bids are on the left.
BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


def normalize_auction(qu: question.Question) -> None:
    # Normalize auction, so North's bids are on the left.
    bids = qu.auction
    # bids.append('?')
    if qu.dealer != 'n':
        count = BID_PADDING[qu.dealer]
        for i in range(count):
            bids.insert(0, '-')


def update_auction(qu: question.Question, step: question.Step) -> None:
    for bid in step.auction:
        qu.auction.append(bid)
    qu.auction.append('?')


def show_auction(qu: question.Question) -> None:
    for i in range(15):
        print()
    print('-----------------------------')
    print('\nVulnerability:', qu.vulnerable)
    print(f'Dealer: {qu.dealer}\n')
    print('North   East  South   West')
    print('------ ------ ------ ------')
    auc = qu.auction
    i = 0
    while i < len(auc):
        bids = [x.ljust(6) for x in auc[i:i+4]]
        print(' '.join(bids))
        i += 4
    print('-----------------------------')


def get_user_bid() -> str:
    ans = input('Your bid? ')
    return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


if __name__ == '__main__':
    main()
