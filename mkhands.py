
import sys
from typing import TextIO


class Hand:
    comment: str
    suits: list[list[str]]

    def __init__(self, suits: list[list[str]], comment: str):
        self.suits = suits
        self.comment = comment


def main() -> None:
    assert len(sys.argv) == 2
    fname = sys.argv[1]
    with open(fname, 'wt') as f:
        while True:
            cards, comment = get_hand()  # exits if no hand
            hand = parse(cards)
            print_hand(f, Hand(hand, comment))


def get_hand() -> tuple[str, str]:
    try:
        ans = input('Four suits > ')
    except EOFError:
        sys.exit()
    comment = input('Comment > ')
    return (ans, comment)


def print_hand(f: TextIO, hand: Hand) -> None:
    print(f'\nHand: # {hand.comment}', file=f)
    print('', file=f)
    for suit in hand.suits:
        print(' '.join(suit), file=f)
    print('\n', file=f)


def parse(hand: str) -> list[list[str]]:
    strs = hand.split()
    assert len(strs) == 4
    suits: list[list[str]] = []
    for i in range(4):
        suits.append([x.upper() for x in strs[i]])
    for i in range(4):
        if 'T' in suits[i]:
            new: list[str] = []
            for c in suits[i]:
                if c == 'T':
                    new.append('10')
                else:
                    new.append(c)
            suits[i] = new
    return suits


if __name__ == '__main__':
    main()
