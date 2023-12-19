#!/usr/bin/env python3

"""
quiz.py: Display questions and check answers

Usage:
    quiz.py [-k <key>] QUESTIONS
    quiz.py   --version
    quiz.py   --help

Options and commands:
    --version          Show version and exit.
    -h --help          Show this message and exit.
    -k <key>           Show only questions with this keyword.
"""


import docopt  # type: ignore
from exercise import Exercise


def main() -> None:
    keyword = ''
    args = docopt.docopt(__doc__, version='0.01')
    # print(args)
    fname = args['QUESTIONS']
    if args['-k']:
        keyword = args['-k']
    with open(fname) as f:
        print()
        while True:
            ex = Exercise(f)
            if not ex.valid:
                break
            if keyword != '':
                if keyword not in ex.keys:
                    continue
            want_more = ask_question(ex)
            if not want_more:
                break


def ask_question(ex: Exercise) -> bool:
    # clear screen
    # show info lines
    # show hand
    # for _ in range(len(answers)):
    #     show auction out to first '*', ending with '?'.
    #     remove the '*'
    #     get answer
    #     show yes/no
    #     show explanation if wrong
    # ask if we should continue
    # return True if yes, False if no
    print('asking...', ex)
    return True


# This tells how far to shift the auction so North's bids are on the left.
BID_PADDING = {'N': 0, 'E': 1, 'S': 2, 'W': 3}


# def normalize_auction(qu: question.Question) -> None:
#     # Normalize auction, so North's bids are on the left.
#     bids = qu.auction
#     # bids.append('?')
#     if qu.dealer != 'n':
#         count = BID_PADDING[qu.dealer]
#         for i in range(count):
#             bids.insert(0, '-')


# def update_auction(qu: question.Question, step: question.Step) -> None:
#     for bid in step.auction:
#         qu.auction.append(bid)
#     qu.auction.append('?')


# def show_auction(qu: question.Question) -> None:
#     for i in range(15):
#         print()
#     print('-----------------------------')
#     print('\nVulnerability:', qu.vulnerable)
#     print(f'Dealer: {qu.dealer}\n')
#     print('North   East  South   West')
#     print('------ ------ ------ ------')
#     auc = qu.auction
#     i = 0
#     while i < len(auc):
#         bids = [x.ljust(6) for x in auc[i:i+4]]
#         print(' '.join(bids))
#         i += 4
#     print('-----------------------------')


def get_user_bid() -> str:
    ans = input('Your bid? ')
    return ans


def print_explanation(expl: list[str]) -> None:
    for line in expl:
        print(line)


if __name__ == '__main__':
    main()
