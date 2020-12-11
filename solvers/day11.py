from itertools import chain
from copy import deepcopy

DIRECTIONS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
]

class Seat:
    def __init__(self, is_floor=False, tolerance=4):
        self.is_floor = is_floor
        self.occupied = False
        self.tolerance = tolerance
        self.neighbours = set()

    def register_neighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)

    def needs_change(self):
        seat_sum = sum([1 for n in self.neighbours if n.occupied])
        if self.occupied:
            if seat_sum >= self.tolerance:
                return True
        else:
            if seat_sum == 0:
                return True
        return False 

    def __radd__(self, other):
        if self.occupied:
            return 1 + other
        return other

    def __repr__(self):
        return '.' if self.is_floor else '#' if self.occupied else 'L'


class SeatsMap:
    def __init__(self, puzzle_input, tolerance=4):
        self.rows = []
        for line in puzzle_input:
            line_max = len(line)
            row = []
            for idx, char in enumerate(line):
                seat = Seat(char is '.', tolerance)
                if self.rows:
                    for n in self.rows[-1][max(idx-1, 0):min(idx+2, line_max)]:
                        seat.register_neighbour(n)
                if row:
                    seat.register_neighbour(row[-1])
                row.append(seat)
            self.rows.append(row)
        self.seats = list([s for s in chain(*self.rows) if not s.is_floor])

    def step(self):
        seats = []
        for seat in self.seats:
            if seat.needs_change():
                seats.append(seat)
        for seat in seats:
            seat.occupied = not seat.occupied

    def sum(self):
        return sum([sum(r) for r in self.rows])

    def __repr__(self):
        return "\n".join([" ".join([str(s) for s in row]) for row in self.rows])


class SeatsMap2(SeatsMap):
    def __init__(self, puzzle_input, tolerance):
        self.rows = []
        for line in puzzle_input:
            row = []
            for char in line:
                x = len(row)
                y = len(self.rows)
                seat = Seat(char is '.', tolerance)
                if not seat.is_floor:
                    for direction in DIRECTIONS:
                        x1 = x + direction[0]
                        y1 = y + direction[1]
                        while x1 >= 0 and y1 >= 0 and x1 < len(line):
                            if y1 == y:
                                n = row[x1]
                            elif self.rows and self.rows[y1]:
                                n = self.rows[y1][x1]
                            if not n.is_floor:
                                seat.register_neighbour(n)
                                break

                            x1 += direction[0]
                            y1 += direction[1]

                row.append(seat)
            self.rows.append(row)
        self.seats = list([s for s in chain(*self.rows) if not s.is_floor])


def solve1(puzzle_input):
    seat_map = SeatsMap(puzzle_input)
    i = -1
    while seat_map.sum() != i:
        i = seat_map.sum()
        seat_map.step()
    return seat_map.sum()


def solve2(puzzle_input):
    seat_map = SeatsMap2(puzzle_input, 5)
    i = -1
    while seat_map.sum() != i:
        i = seat_map.sum()
        seat_map.step()
    return seat_map.sum()    
