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


def main() -> None:
    args = docopt.docopt(__doc__, version='0.01')
    fname = args['<hands>']
    base, _ = os.path.splitext(fname)
    outfile = base + '.exr'
    template = read_template(TEMPLATE)
    with open(fname) as fh, open(outfile, 'wt') as fex:
        while True:
            line = fh.readline()
            if line == '':
                # print('eof looking for hand')
                return
            if line.startswith('Hand'):
                break
        hand = read_hand(fh)
        write_exercise(template, hand, fex)


def read_hand(fh: TextIO) -> list[str]:
    # print('read hand')
    hand: list[str] = []
    while True:
        line = fh.readline()
        if line == '':
            assert 'EOF while reading hand' == ''
        line = line.rstrip()
        # print('hand:', line)
        if line == '':
            break
        hand.append(line)
    return hand


def write_exercise(template: list[str], hand: list[str], fex: TextIO) -> None:
    #print('write exercise')
    for line in template:
        if line.startswith('HAND GOES HERE'):
            for hand_line in hand:
                print(hand_line, file=fex)
        else:
            print(line, file=fex)


def read_template(fname: str) -> list[str]:
    # print('read template')
    lines: list[str] = []
    with open(fname) as f:
        for line in f.readlines():
            lines.append(line.rstrip())
    return lines


if __name__ == '__main__':
    main()
