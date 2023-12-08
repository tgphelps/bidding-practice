
import sys
from typing import TextIO, Optional
import question


def main() -> None:
    assert len(sys.argv) == 2
    with open(sys.argv[1]) as f:
        print()
        while True:
            qu = read_question(f)
            if not qu:
                break
            # print('debug:')
            # print(qu)
            ask_question(qu)


def read_question(f: TextIO) -> Optional[question.Question]:
    line = question.get_line(f)
    # print('Reading question...')
    if line == 'Question':
        return question.Question(f)
    else:
        assert line == 'End'
        return None


def ask_question(qu: question.Question) -> None:
    show_auction(qu)
    for hand in qu.hands:
        show_hand(hand)
        ans = get_user_bid()
        if ans == hand.answer:
            print('Correct')
        else:
            print('No')
            print_explanation(hand.expl)
        ans = input('Continue? ')
        if ans == 'n':
            print('Exiting.')
            sys.exit(0)


def show_auction(qu: question.Question) -> None:
    print(f'\nDealer: {qu.dealer}\n')
    print('North   East  South   West')
    print('------ ------ ------ ------')
    auc = qu.auction
    i = 0
    while i < len(auc):
        bids = [x.ljust(6) for x in auc[i:i+4]]
        print(' '.join(bids))
        i += 4


def show_hand(hand: question.Hand) -> None:
    hand.print()


def get_user_bid() -> str:
    ans = input('Your bid? ')
    return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


if __name__ == '__main__':
    main()
