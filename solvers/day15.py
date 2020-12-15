from collections import defaultdict, deque


def play(puzzle_input, turns):
    memory = defaultdict(lambda: deque([0, 0], maxlen=2))
    last_spoken = None
    for turn, value in enumerate(puzzle_input[0].split(','), start=1):
        last_spoken = int(value)
        memory[last_spoken].append(turn)

    for turn in range(len(memory)+1, turns + 1):
        before, recent = memory[last_spoken]
        if before is 0:
            last_spoken = 0
        else:
            last_spoken = recent - before

        memory[last_spoken].append(turn)
    return last_spoken


def solve1(puzzle_input):
    return play(puzzle_input, 2020)


def solve2(puzzle_input):
    return play(puzzle_input, 30000000)
