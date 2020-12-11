def clean(puzzle_input):
    puzzle_input.append('0')
    sorted_adapters = sorted([int(i) for i in puzzle_input])
    sorted_adapters.append(max(sorted_adapters) + 3)
    return sorted_adapters


def solve1(puzzle_input):
    jolts = {1: 0, 3: 0}
    sorted_adapters = clean(puzzle_input)
    for a, b in zip(sorted_adapters, sorted_adapters[1:]):
        jolts[b - a] += 1
    return jolts[1] * jolts[3]


def solve2(puzzle_input):
    sorted_adapters = clean(puzzle_input)

    # splitting up into sections is not needed but brings down 
    # execution time from 7h+ to 0.00024s
    section = []
    sections = [section]
    for a, b in zip(sorted_adapters, sorted_adapters[1:]):
        section.append(a)
        if b - a == 3:
            section = []
            sections.append(section)

    comb = 1
    for section in sections:
        if not section:
            continue
        cf = CombinationFinder(section)
        cf.traverse(0)
        comb *= cf.combinations
    return comb


class CombinationFinder:
    def __init__(self, lst):
        self.lst = lst
        self.combinations = 0
        self.size = len(self.lst)

    def traverse(self, depth):
        i = 1
        nb = self.lst[depth]

        if len(self.lst) == depth + 1:
            self.combinations += 1
            return

        while self.lst[depth + i] - nb <= 3:
            self.traverse(depth + i)
            i += 1
            if depth + i == self.size:
                break
