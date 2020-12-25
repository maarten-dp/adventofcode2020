from collections import defaultdict


class Vector3:
    def __init__(self, x=0, y=0 ,z=0):
        self.x = x
        self.y = y
        self.z = z

    def as_tuple(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __repr__(self):
        return "{},{},{}".format(*self.as_tuple())


COORDINATE_MAP = {
    "e": Vector3(1, 0, -1),
    "w": Vector3(-1, 0, 1),
    "se": Vector3(0, 1, -1),
    "nw": Vector3(0, -1, 1),
    "sw": Vector3(-1, 1, 0),
    "ne": Vector3(1, -1, 0),
}

class Tile:
    def __init__(self, coord, floor):
        self.coord = coord
        self.floor = floor
        self.flipped = False

    @property
    def neighbours(self):
        for coord in COORDINATE_MAP.values():
            yield self.floor.get_tile_at(self.coord + coord)

    def __bool__(self):
        return self.flipped

    def __radd__(self, other):
        if self.flipped:
            return other + 1
        return other

    def __repr__(self):
        return str(self.coord)


class Floor:
    def __init__(self):
        self.tiles = {}

    def get_tile_at(self, coord):
        if coord.as_tuple() not in self.tiles:
            self.tiles[coord.as_tuple()] = Tile(coord, self)
        return self.tiles[coord.as_tuple()]

    def get_coordinate(self, line):
        coordinate = Vector3()
        while line:
            slc = 1
            if line.startswith("s") or line.startswith("n"):
                slc = 2
            coord = line[:slc]
            line = line[slc:]
            coordinate += COORDINATE_MAP[coord]
        return coordinate

    def flip_tile(self, coordinate):
        tile = self.get_tile_at(coordinate)
        tile.flipped = not tile.flipped

    def __repr__(self):
        return "\n".join(["{} - {}".format(coord, t.flipped) for (coord, t) in self.tiles.items()])


def solve1(puzzle_input):
    floor = Floor()
    for line in puzzle_input:
        coord = floor.get_coordinate(line)
        floor.flip_tile(coord)
    return sum(floor.tiles.values())


def solve2(puzzle_input):
    floor = Floor()
    for line in puzzle_input:
        coord = floor.get_coordinate(line)
        floor.flip_tile(coord)

    for day in range(100):
        apply_change(floor)
    return sum(floor.tiles.values())


def apply_change(floor):
    black_tiles = set([t for t in floor.tiles.values() if t.flipped])
    white_tiles = set()

    for btile in black_tiles:
        for t in btile.neighbours:
            if not t.flipped:
                white_tiles.add(t)

    needs_change = set()
    for tile in black_tiles:
        black_neighbours = sum(tile.neighbours)
        if black_neighbours == 0 or black_neighbours > 2:
            needs_change.add(tile)

    for tile in white_tiles:
        if sum(tile.neighbours) == 2:
            needs_change.add(tile)

    for tile in needs_change:
        tile.flipped = not tile.flipped


