
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
            ask_question(qu)


def read_question(f: TextIO) -> Optional[question.Question]:
    line = question.get_line(f)
    if line == 'Question':
        return question.Question(f)
    else:
        assert line == 'End'
        return None


def ask_question(qu: question.Question) -> None:
    print('question...')


if __name__ == '__main__':
    main()
