
from typing import TextIO


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


class Question:
    f: TextIO
    dealer: str
    auction: str
    hands: list[Hand]

    def __init__(self, f: TextIO):
        self.f = f
        self.hands = []
        while True:
            line = get_line(f)
            print('LINE:', line)
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
        self.auction = fld[1]


def get_line(f: TextIO) -> str:
    while True:
        line = f.readline()
        if line == '':
            print('Unexpected EOF.')
            assert False
        line = line.rstrip()
        if line != '':
            return line
