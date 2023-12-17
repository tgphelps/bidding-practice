
import random
from collections import Counter
from typing import TextIO


SUIT_SYMS = "\u2660\u2665\u2666\u2663"
# BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


class Answer:
    bid: str
    expl: str

    def __init__(self, bid: str, expl: str):
        self.bid = bid
        self.expl = expl


class Hand:
    suits: list[str]

    def __init__(self, f: TextIO):
        "Read suits from f. There may be leading blank lines."
        self.suits = []
        while True:
            line = get_line(f)
            line = line.rstrip()
            if line == '':
                continue
            line = replace_xs(line)
            self.suits.append(line)
            if len(self.suits) == 4:
                break
        # print('end hand')

    def __str__(self) -> str:
        ss: list[str] = []
        for i, suit in enumerate(self.suits):
            cs = suit.split()
            a = [x.ljust(2) for x in cs]
            s = ' '.join(a)
            s = SUIT_SYMS[i] + ' ' + s
            ss.append(s)
        return '\n'.join(ss)


class Exercise:
    keys: list[str]
    info: list[str]
    dealer: str
    vulnerable: str
    hand: Hand
    auction: list[str]
    answers: list[Answer]


def get_line(f: TextIO) -> str:
    while True:
        line = f.readline()
        if line == '':
            print('Unexpected EOF.')
            assert False
        if line.startswith('#'):
            continue
        line = line.rstrip()
        if line != '':
            # print('debug:', line)
            return line


def decode_auction(raw: str, dealer: str) -> list[str]:
    bids: list[str] = []
    i = 0
    while i < len(raw):
        c = raw[i]
        i += 1
        if c == 'p':
            bids.append('Pass')
        elif c == 'x':
            bids.append('Dbl')
        elif c == 'r':
            bids.append('Rdbl')
        elif c in '1234567':
            c2 = raw[i]
            i += 1
            if c2 in 'shdc':
                bids.append(c + c2.upper())
            elif c2 == 'n':
                bids.append(c + 'NT')
            else:
                print('BAD auction:', raw)
                assert False
        else:
            print('BAD auction:', raw)
            assert False
    # Normalize auction, so North's bids are on the left.
    # bids.append('?')
    # if dealer != 'n':
    #     count = BID_PADDING[dealer]
    #     for i in range(count):
    #         bids.insert(0, '-')
    return bids


def replace_xs(suit: str) -> str:
    "Replace, e.g., 'A K x x x' with random low cards: 'A K 9 5 3'"
    cards = ['2', '3', '4', '5', '6', '7', '8', '9']
    random.shuffle(cards)
    d = dict(Counter(suit))
    if 'x' not in d:
        return suit
    n = d['x']
    cards = cards[0:n]
    cards.sort()
    new = ''
    for c in suit:
        if c != 'x':
            new += c.upper()
        else:
            new += cards.pop()
    return new


def run_test() -> None:
    with open('test.txt') as f:
        while True:
            line = get_line(f)
            if line.startswith('Hand:'):
                h = Hand(f)
                print(h)
                break


if __name__ == '__main__':
    run_test()
