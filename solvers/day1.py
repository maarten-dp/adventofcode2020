from itertools import combinations
from operator import mul
from functools import reduce


def solve(puzzle_input, length):
    puzzle_input = [int(i) for i in puzzle_input]
    for numbers in combinations(puzzle_input, length):
        if sum(numbers) == 2020:
            return reduce(mul, numbers, 1)

def solve1(puzzle_input):
    return solve(puzzle_input, 2)

def solve2(puzzle_input):
    return solve(puzzle_input, 3)
