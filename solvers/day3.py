TREE = '#'
GROUND = '.'


class InfiniteList(list):
    def __getitem__(self, index):
        index %= len(self)
        return list.__getitem__(self, index)


def trees_encountered(puzzle_input, horiz, vert):
    geology = []
    trees = 0
    for idx, line in enumerate(puzzle_input[vert::vert], start=1):
        location = InfiniteList(line)[idx * horiz]
        if location == TREE:
            trees += 1
    return trees


def solve1(puzzle_input):
    return trees_encountered(puzzle_input, 3, 1)


def solve2(puzzle_input):
    slopes = [    
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    multi = 1
    for horiz, vert in slopes:
        multi *= trees_encountered(puzzle_input, horiz, vert)
    return multi
