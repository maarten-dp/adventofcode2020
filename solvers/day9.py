from itertools import combinations


class InvalidNumberError(Exception):
    pass


class PreambleChecker:
    def __init__(self, preable_length=25):
        self.values = []
        self.combinations = []
        self.preable_length = preable_length

    def check(self, number):
        if len(self.values) == self.preable_length:
            self.values.pop(0)
            if number not in self.combinations:
                raise InvalidNumberError()

        self.values.append(number)
        self._clean()

    def _clean(self):
        self.combinations = []
        for a, b in combinations(self.values, 2):
            self.combinations.append(a + b)


def get_inconsistent_number(puzzle_input):
    preamble = 25
    if len(puzzle_input) < 25:
        preamble = 5

    pc = PreambleChecker(preamble)
    for nb in puzzle_input:
        try:
            pc.check(int(nb))
        except InvalidNumberError:
            return nb

def solve1(puzzle_input):
    return get_inconsistent_number(puzzle_input)


def solve2(puzzle_input):
    inb = int(get_inconsistent_number(puzzle_input))
    nbs = [int(nb) for nb in puzzle_input]
    candidates = []

    for nb in nbs:
        candidates.append([0, []])
        for candidate in candidates:
            candidate[1].append(nb)
            candidate[0] += nb
            if candidate[0] == inb:
                return min(candidate[1]) + max(candidate[1])
