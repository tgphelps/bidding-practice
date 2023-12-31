
import random
from collections import Counter
from typing import TextIO


SUIT_SYMS = "\u2660\u2665\u2666\u2663"
BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


class Step:
    auction: list[str]
    answer: str
    expl: list[str]

    def __init__(self, f: TextIO, dealer: str):
        self.auction = []
        self.expl = []
        while True:
            line = get_line(f)
            if line.startswith('Auction'):
                fld = line.split()
                if len(fld) > 1:
                    self.auction += decode_auction(fld[1], dealer)
            elif line.startswith('Answer'):
                fld = line.split()
                self.answer = fld[1]
            elif line.startswith('Explanation'):
                last_line = self.store_explanation(f)
                assert last_line.startswith('Ends')
                # print('end step')
                break

    def store_explanation(self, f: TextIO) -> str:
        while True:
            line = get_line(f)
            if line.startswith(' '):
                self.expl.append(line)
            else:
                return line


class Hand:
    suits: list[str]

    def __init__(self, f: TextIO):
        self.suits = []
        for i in range(4):
            line = get_line(f)
            assert line[0] == ' '
            line = replace_xs(line)
            self.suits.append(line)
        line = get_line(f)
        assert line.startswith('Endh')
        # print('end hand')

    def __str__(self) -> str:
        s = ''
        for suit in self.suits:
            s += suit
            s += '\n'
        # s += 'Answer: ' + self.answer
        return s

    def print(self) -> None:
        print('\nYour hand:')
        for i, suit in enumerate(self.suits):
            cs = suit.split()
            a = [x.ljust(2) for x in cs]
            s = ' '.join(a)
            print(SUIT_SYMS[i], s)


class Question:
    f: TextIO
    keywords: str
    vulnerable: str
    dealer: str
    hand: Hand
    auction: list[str]
    steps: list[Step]

    def __init__(self, f: TextIO):
        self.f = f
        self.keywords = ''
        self.steps = []
        self.auction = []  # Will be built as steps are shown
        while True:
            line = get_line(f)
            # print('LINE:', line)
            if line == 'Endq':
                # print('end question')
                break
            if line.startswith('Dealer'):
                self.store_dealer(line)
            elif line.startswith('Hand'):
                self.hand = Hand(f)
            elif line.startswith('Step'):
                self.steps.append(Step(f, self.dealer))
            elif line.startswith('Vulnerable'):
                fld = line.split()
                self.vulnerable = fld[1].upper()
            elif line.startswith('Keywords'):
                fld = line.split()
                self.keywords = fld[1]
            else:
                print('Unknown:', line)
                assert False

    def store_dealer(self, line) -> None:
        fld = line.split()
        dealer = fld[1]
        assert dealer in ('n', 's', 'e', 'w')
        self.dealer = dealer.upper()

    # def store_auction(self, line) -> None:
    #     fld = line.split()
    #     self.auction = decode_auction(fld[1], self.dealer)

    # def __str__(self) -> str:
    #     s = f'dealer: {self.dealer}\nauction: {self.auction}\n'
    #     for hand in self.hands:
    #         s += hand.__str__()
    #         s += '\n'
    #     return s


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
