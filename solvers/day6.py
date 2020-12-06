from itertools import chain
from operator import or_, and_


def get_groups(lines):
    group = []
    # make it register the last group
    lines.append('')
    for line in lines:
        if line:
            group.append(set(line))
        elif group:
            yield group
            group = []


def process_asnwers(lines, op):
    groups = list()

    for group in get_groups(lines):
        answers = group[0]
        for answer in group[1:]:
            answers = op(answers, answer)
        yield len(answers)


def solve1(puzzle_input):
    return sum(process_asnwers(puzzle_input, or_))


def solve2(puzzle_input):
    return sum(process_asnwers(puzzle_input,  and_))
