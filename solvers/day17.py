from itertools import product
from collections import defaultdict

V3_COORDS = product([0, 1, -1], repeat=3)
V3_OFFSET_COORDS = [c for c in V3_COORDS if c != (0, 0, 0)]
V4_COORDS = product([0, 1, -1], repeat=4)
V4_OFFSET_COORDS = [c for c in V4_COORDS if c != (0, 0, 0, 0)]
VECTORS = {}


class Registry:
    def __init__(self, cube_cls, vector_cls):
        self.cubes = {}
        self.cube_cls = cube_cls
        self.vector_cls = vector_cls

    def register(self, cube):
        self.cubes[cube.position.as_tuple] = cube

    def get_cube_at(self, position):
        if isinstance(position, Vector):
            position = position.as_tuple

        if not position in self.cubes:
            cube = self.cube_cls(self.vector_cls(*position), self)

        return self.cubes[position]

    def step(self):
        needs_change = []
        for cube in list(self.cubes.values()):
            if cube.active and cube.position.z >= 0:
                # generate inactive cubes
                cube.neighbours

        for cube in list(self.cubes.values()):
            if cube.position.z >= 0 and cube.needs_change():
                needs_change.append(cube)

        for cube in needs_change:
            if cube.position.z > 0:
                mirror = self.get_cube_at(cube.position._invert('z'))
                mirror.active = not mirror.active
            cube.active = not cube.active

    def active_cubes(self):
        return sum(self.cubes.values())


class Vector:
    members = []

    def __new__(cls, *args):
        if args in VECTORS:
            return VECTORS[args]
        inst = super().__new__(cls)
        VECTORS[args] = inst
        return inst

    def __init__(self, *args):
        # for member, value in zip(self.members, args):
        #     setattr(self, member, value)
        self._vector = tuple(args)

    @property
    def as_tuple(self):
        return self._vector

    def __add__(self, other):
        args = []
        for a, b in zip(self._vector, other._vector):
            args.append(a + b)
        return self.__class__(*args)

    def __repr__(self):
        return ",".join([str(m for m in self._vector)])

    def _invert(self, plains):
        args = []
        for member in self.members:
            value = getattr(self, member)
            if member in plains:
                value *= -1
            args.append(value)
        return self.__class__(*args)


class Vector3(Vector):
    members = ['x', 'y', 'z']

    def __init__(self, *args):
        self.x, self.y, self.z = args
        super().__init__(*args)


class Vector4(Vector):
    members = ['x', 'y', 'z', 'w']

    def __init__(self, *args):
        self.x, self.y, self.z, self.w = args
        super().__init__(*args)


class Cube:
    def __init__(self, position, registry):
        self.position = position
        self.neighbour_coords = []
        self._neighbours = []
        self.active = False
        self.registry = registry
        self._generate_neighbour_coords()
        registry.register(self)

    def _generate_neighbour_coords(self):
        for neighbour in V3_OFFSET_COORDS:
            self.neighbour_coords.append(self.position + Vector3(*neighbour))

    @property
    def neighbours(self):
        if not self._neighbours:
            for coord in self.neighbour_coords:
                self._neighbours.append(self.registry.get_cube_at(coord))
        return self._neighbours

    def needs_change(self):
        active_neighbours = sum(self.neighbours)
        condition = set([3, 3 - self.active])
        if active_neighbours in condition:
            return self.active == False
        return self.active == True

    def __radd__(self, other):
        if self.active:
            return other + 1
        return other

    def __repr__(self):
        return "#" if self.active else "."


class HyperCube(Cube):
    def _generate_neighbour_coords(self):
        for neighbour in V4_OFFSET_COORDS:
            self.neighbour_coords.append(self.position + Vector4(*neighbour))


def solve1(puzzle_input):
    registry = Registry(Cube, Vector3)
    for y, line in enumerate(reversed(puzzle_input)):
        for x, char in enumerate(line):
            cube = Cube(Vector3(x, y, 0), registry)
            cube.active = char == "#"

    for _ in range(6):
        registry.step()

    return registry.active_cubes()


def solve2(puzzle_input):
    registry = Registry(HyperCube, Vector4)
    for y, line in enumerate(reversed(puzzle_input)):
        for x, char in enumerate(line):
            cube = HyperCube(Vector4(x, y, 0, 0), registry)
            cube.active = char == "#"

    for step in range(6):
        registry.step()

    return registry.active_cubes()
