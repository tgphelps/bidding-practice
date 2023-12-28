#!/usr/bin/env python3

"""
mkexercises.py: Merge hands into a template to make exercises.
Create a file of exercises, one exercise for each hand in the
<hands> file. User will have to manually complete the exercises.

Usage:
    mkexercises.py <hands>
    mkexercises.py   --version
    mkexercises.py   --help

Options and commands:
    --version          Show version and exit.
    -h --help          Show this message and exit.
"""


import os.path
from typing import TextIO
import docopt  # type: ignore


VERSION = '0.01'
TEMPLATE = 'template.txt'
DEBUG = True


class Hand:
    comment: str
    suits: list[str]

    def __init__(self, label: str, suits: list[str]):
        self.label = label
        self.suits = suits


def main() -> None:
    args = docopt.docopt(__doc__, version='0.01')
    fname = args['<hands>']
    base, _ = os.path.splitext(fname)
    outfile = base + '.exr'
    template = read_template(TEMPLATE)
    with open(fname) as fh, open(outfile, 'wt') as fex:
        while True:
            while True:
                line = fh.readline()
                if line == '':
                    debug('eof looking for hand')
                    return
                if line.startswith('Hand'):
                    break
            hand = read_hand(line, fh)
            debug('got complete hand')
            write_exercise(template, hand, fex)


def read_hand(label: str, fh: TextIO) -> Hand:
    debug('reading hand')
    _ = fh.readline()  # blank line after 'Hand:'
    suits: list[str] = []
    while True:
        line = fh.readline()
        if line == '':
            assert 'EOF while reading hand' == ''
        line = line.rstrip()
        debug('hand: ' + line)
        if line == '':
            break
        suits.append(line)
    assert len(suits) == 4
    return Hand(label, suits)


def write_exercise(template: list[str], hand: Hand, fex: TextIO) -> None:
    # print('write exercise')
    for line in template:
        if line.startswith('Hand:'):
            debug('hand goes here')
            if '#' in hand.label:
                i = hand.label.index('#')
                comment = hand.label[i:]
            else:
                comment = '#'
            print(f'Hand: {comment}', file=fex)
            for suit in hand.suits:
                print(suit, file=fex)
        else:
            print(line, file=fex)


def read_template(fname: str) -> list[str]:
    # print('read template')
    lines: list[str] = []
    with open(fname) as f:
        for line in f.readlines():
            lines.append(line.rstrip())
    return lines


def debug(msg: str) -> None:
    if DEBUG:
        print(msg)


if __name__ == '__main__':
    main()
