
from typing import TextIO


SUIT_SYMS = "\u2660\u2665\u2666\u2663"
BID_PADDING = {'N': 0, 'E': 1, 'S':2, 'W':3}


class Hand:
    suits: list[str]
    answer: str
    expl: list[str]

    def __init__(self, f: TextIO):
        self.suits = []
        self.expl = []
        for i in range(4):
            line = get_line(f)
            assert line[0] == ' '
            self.suits.append(line)
        line = get_line(f)
        assert line.startswith('Answer')
        fld = line.split()
        self.answer = fld[1]
        line = get_line(f)
        assert line.startswith('Explanation')
        self.store_explanation(f)

    def store_explanation(self, f: TextIO) -> None:
        while True:
            line = get_line(f)
            if line == 'Endh':
                break
            self.expl.append(line)

    def __str__(self) -> str:
        s = ''
        for suit in self.suits:
            s += suit
            s += '\n'
        s += 'Answer: ' + self.answer
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
    dealer: str
    auction: list[str]
    hands: list[Hand]

    def __init__(self, f: TextIO):
        self.f = f
        self.hands = []
        while True:
            line = get_line(f)
            # print('LINE:', line)
            if line == 'Endq':
                break
            if line.startswith('Dealer'):
                self.store_dealer(line)
            elif line.startswith('Auction'):
                self.store_auction(line)
            elif line.startswith('Hand'):
                self.hands.append(Hand(f))
            else:
                print('Unknown:', line)

    def store_dealer(self, line) -> None:
        fld = line.split()
        dealer = fld[1]
        assert dealer in ('n', 's', 'e', 'w')
        self.dealer = dealer.upper()

    def store_auction(self, line) -> None:
        fld = line.split()
        self.auction = decode_auction(fld[1], self.dealer)

    def __str__(self) -> str:
        s = f'dealer: {self.dealer}\nauction: {self.auction}\n'
        for hand in self.hands:
            s += hand.__str__()
            s += '\n'
        return s


def get_line(f: TextIO) -> str:
    while True:
        line = f.readline()
        if line == '':
            print('Unexpected EOF.')
            assert False
        line = line.rstrip()
        if line != '':
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
    bids.append('?')
    if dealer != 'n':
        count = BID_PADDING[dealer]
        for i in range(count):
            bids.insert(0, '-')
    return bids
