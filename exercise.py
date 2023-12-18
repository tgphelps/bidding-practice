
import random
import sys
from collections import Counter
from typing import TextIO


SUIT_SYMS = "\u2660\u2665\u2666\u2663"
# BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


class Answer:
    bid: str
    expl: list[str]

    def __init__(self, bid: str, expl: list[str]):
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
    valid: bool
    keys: list[str]
    info: list[str]
    dealer: str
    vulnerable: str
    hand: Hand
    auction: list[str]
    answers: list[Answer]

    def __init__(self, f: TextIO):
        self.valid = True
        self.keys = []
        self.info = []
        self.auction = []
        self.answers = []
        while True:
            line = get_line(f, allow_eof=True)
            if line == ')EOF(':
                self.valid = False
                return
            if line.startswith('---'):
                break
        # Keys, Dealer, Vulnerable, Info, Hand, Auction, Answers
        while True:
            line = get_line(f)
            # if line.startswith('==='):
            #     break
            line = line.rstrip()
            print('line:', line)
            if line.startswith('Keys:'):
                fld = line.split()
                self.keys = fld[1:]
            elif line.startswith('Dealer'):
                fld = line.split()
                d = fld[1].upper()
                assert d in ('N', 'S', 'E', 'W')
                self.dealer = d
            elif line.startswith('Vulnerable:'):
                fld = line.split()
                v = fld[1].upper()
                assert v in ('N-S', 'E-W', 'BOTH', 'NONE')
                self.vulnerable = v
            elif line.startswith('Info:'):
                self.store_info(f)
            elif line.startswith('Hand:'):
                h = Hand(f)
                self.hand = h
                line = get_line(f)
                line = line.rstrip()
                assert line == ''
            elif line.startswith('Auction:'):
                self.store_auction(f)
            elif line.startswith('Answers:'):
                self.store_answers(f)
                break
            else:
                print('Invalid line:', line)
                sys.exit(1)

    def store_info(self, f: TextIO) -> None:
        # print('store info...')
        while True:
            line = get_line(f)
            line = line.rstrip()
            print(f'line: /{line}/')
            if line == '':
                break
            self.info.append(line)

    def store_auction(self, f: TextIO) -> None:
        line = get_line(f)
        assert 'N' in line
        line = get_line(f)
        assert line.startswith('---')
        while True:
            line = get_line(f)
            line = line.rstrip()
            if line == '':
                break
            fld = line.split()
            for bid in fld:
                self.auction.append(bid)

    def store_answers(self, f: TextIO) -> None:
        while True:
            line = get_line(f)
            if line.startswith('==='):
                break
            fld = line.split()
            bid = fld[1]
            expl = read_paragraph(f)
            self.answers.append(Answer(bid, expl))


def get_line(f: TextIO, allow_eof=False) -> str:
    while True:
        line = f.readline()
        if line == '':
            if allow_eof:
                return ')EOF('
            else:
                print('Unexpected EOF.')
                assert False
        if line.startswith('#'):
            continue
        line = line.rstrip()
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


def read_paragraph(f: TextIO) -> list[str]:
    para: list[str] = []
    while True:
        line = get_line(f)
        line = line.rstrip()
        if line == '':
            return para
        para.append(line)


# -------------------------

def run_test1():
    with open('test2.txt') as f:
        while True:
            print('READ...')
            e = Exercise(f)
            if not e.valid:
                break
            print('Dealer:', e.dealer)
            print('Vuln.:', e.vulnerable)
            print('Keys:', e.keys)
            print('Hand:')
            print(e.hand)
            print('Auction:', e.auction)
            print('Answers:')
            print(e.answers)
        print('DONE')


def run_test_hand() -> None:
    with open('test.txt') as f:
        while True:
            line = get_line(f)
            if line.startswith('Hand:'):
                h = Hand(f)
                print(h)
                break


if __name__ == '__main__':
    run_test1()
    # run_test_hand()
