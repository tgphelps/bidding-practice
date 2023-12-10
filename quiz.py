
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
        if line != 'End':
            print('line:', line)
            assert False
        return None


def ask_question(qu: question.Question) -> None:
    # pseudo code:
    # normalize the auction
    # for each step:
    #     append step auction to question auction
    #     show auction
    #     get user bid
    #     tell answer
    #     show explanation
    #     if he wants to stop:
    #         break
    normalize_auction(qu)
    for step in qu.steps:
        print('step...')
        update_auction(qu, step)
        show_auction(qu)
        show_hand(qu.hand)
        ans = get_user_bid()
        if ans == step.answer:
            print('Correct')
        else:
            print('No')
            print_explanation(step.expl)
        ans = input('Continue? ')
        if ans == 'n':
            print('Exiting.')
            sys.exit(0)
        # Going to next step
        qu.auction.remove('?')
        # qu.auction.append(step.answer)


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
