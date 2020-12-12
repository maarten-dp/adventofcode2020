import math

DIRECTIONS = {
    'N': 0,
    'E': 1,
    'S': 2,
    'W': 3,
}

MODIFIERS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}


class Boat:
    def __init__(self):
        self.face = 1
        self.x = 0
        self.y = 0

    @property    
    def position(self):
        return self.x, self.y

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def rotate(self, direction, amount):
        amount /= 90
        if direction == 'L':
            amount *= -1
        self.face = (self.face + amount) % 4

    def move(self, direction, amount):
        x, y = MODIFIERS[direction]
        self.x += x * amount
        self.y += y * amount

    def follow_instruction(self, instruction):
        direction, amount = self._parse_instruction(instruction)
        if direction in DIRECTIONS:
            self._move(DIRECTIONS[direction], amount)
        elif direction == 'F':
            self.move(self.face, amount)
        else:
            self.rotate(direction, amount)

    def _move(self, direction, amount):
        self.move(direction, amount)

    def _parse_instruction(self, instruction):
        direction = instruction[0]
        amount = int(instruction[1:])
        return direction, amount


class WayPoint:
    def __init__(self):
        self.x = 10
        self.y = 1

    def move(self, direction, amount):
        x, y = MODIFIERS[direction]
        self.x += x * amount
        self.y += y * amount

    def rotate(self, origin, angle):
        angle = (angle + 360) % 360
        for _ in range(int(angle / 90)):
            x, y = self.x, self.y
            self.x = y
            self.y = x * -1


class WayPointBoat(Boat):
    def __init__(self):
        super().__init__()
        self.waypoint = WayPoint()

    def rotate(self, direction, amount):
        if direction == 'L':
            amount *= -1
        self.waypoint.rotate(self.position, amount)

    def move(self, direction, amount):
        self.x += self.waypoint.x * amount
        self.y += self.waypoint.y * amount

    def _move(self, direction, amount):
        self.waypoint.move(direction, amount)


def solve1(puzzle_input):
    boat = Boat()
    for instruction in puzzle_input:
        boat.follow_instruction(instruction)
    return boat.manhattan_distance()


def solve2(puzzle_input):
    boat = WayPointBoat()
    for instruction in puzzle_input:
        boat.follow_instruction(instruction)
    return boat.manhattan_distance()
