from collections import defaultdict
from math import sqrt
import re
from pprint import pprint

RE = r"#....##....##....###"


def edge_to_bin(edge):
    return edge.replace("#", "0").replace(".", "1")


class Tile:
    def __init__(self, tid, tile):
        self.tid = tid
        self._tile = tile

        self._top = edge_to_bin(tile[0])
        self._bottom = edge_to_bin(tile[-1])
        left, right = list(zip(*tile))[::len(tile)-1]
        self._left = edge_to_bin("".join(left))
        self._right = edge_to_bin("".join(right))

        self.sides = []
        self._calc(self._top)
        self._calc(self._right)
        self._calc(self._bottom)
        self._calc(self._left)

    def _calc(self, side1):
        self.sides.extend([
            int(side1, 2),
            int(side1[::-1], 2),
        ])

    @property
    def top(self):
        return self.sides[0]

    @property
    def right(self):
        return self.sides[2]

    @property
    def bottom(self):
        return self.sides[4]

    @property
    def left(self):
        return self.sides[6]

    def re_orient(self, value, attr):
        i = 0
        while value != getattr(self, attr):
            self.rotate()
            i += 1
            if i == 5:
                self.flip()

    def rotate(self):
        image = []
        for row in zip(*[r[::-1] for r in self._tile]):
            image.append("".join(row))
        self._tile = image
        s = self.sides
        self.sides = s[2:4] + s[5:6] + s[4:5] + s[6:8] + s[1:2] + s[0:1]

    def flip(self):
        tile = []
        for row in self._tile:
            tile.append(row[::-1])
        self._tile = tile
        s = self.sides
        self.sides = s[1:2] + s[0:1] + s[6:8] + s[5:6] + s[4:5] + s[2:4]

    def trimmed(self):
        for row in self._tile[1:-1]:
            yield row[1:-1]
    
    def __repr__(self):
        return self.tid


class Image:
    def __init__(self, image):
        self.image = []
        self.waves = 0
        for row in image:
            for raw_row in zip(*[r.trimmed() for r in row]):
                self.image.append("".join(raw_row))
                self.waves += self.image[-1].count('#')

    def find_monsters(self):
        monsters = 0
        for idx, row in enumerate(self.image[1:-1], start=1):
            for hit in re.finditer(RE, row):
                start = hit.start()
                end = hit.end()
                has_head = self.image[idx-1][end - 2] == '#'
                has_belly = self.image[idx+1][start + 1:end - 3:3].count('#') == 6
                if has_head and has_belly:
                    monsters += 1
        return monsters

    def rotate(self):
        image = []
        for row in zip(*[r[::-1] for r in self.image]):
            image.append("".join(row))
        self.image = image

    def flip(self):
        tile = []
        for row in self.image:
            tile.append(row[::-1])
        self.image = tile

    def __repr__(self):
        for row in self.image:
            print(row)
        return ''


def is_corner(tile, tiles):
    anchor = tiles.pop(tile.tid)
    top = []
    bottom = []
    right = []
    left = []
    for tile in tiles.values():
        if anchor.top in tile.sides:
            top.append(tile)
        if anchor.bottom in tile.sides:
            bottom.append(tile)
        if anchor.left in tile.sides:
            left.append(tile)
        if anchor.right in tile.sides:
            right.append(tile)
    if top and not bottom and (left or right) and not (left and right):
        if left:
            return 'bl'
        else:
            return 'br'
    if bottom and not top and (left or right) and not (left and right):
        if left:
            return 'tr'
        else:
            return 'tl'
    return False


class Filter:
    def __init__(self):
        self.top = None
        self.left = None

    def matches(self, tile):
        matches = []
        if self.top:
            matches.append(self.top in tile.sides)
            if self.top in tile.sides:
                tile.re_orient(self.top, 'top')
        if self.left:
            matches.append(self.left in tile.sides)
            if self.left in tile.sides:
                tile.re_orient(self.left, 'left')
        return all(matches)


def parse(lines):
    tiles = defaultdict(list)
    tile_id = None

    for line in lines:
        if 'Tile' in line:
            tile_id = line.split(' ')[-1][:-1]
        elif not line:
            continue
        else:
            tiles[tile_id].append(line)

    for tid, raw_tile in tiles.items():
        tiles[tid] = Tile(tid, raw_tile)
    return tiles


def solve1(puzzle_input):
    tiles = parse(puzzle_input)

    corners = []
    for tile in tiles.values():
        if is_corner(tile, dict(tiles)):
            corners.append(tile)
    
    res = 1
    for t in corners:
        res *= int(t.tid)
    return res


def solve2(puzzle_input):
    tiles = parse(puzzle_input)

    image = []
    for tile in tiles.values():
        if is_corner(tile, dict(tiles)) == 'tl':
            break

    all_tiles = list(tiles.values())
    all_tiles.remove(tile)
    fltr = Filter()
    fltr.left = tile.right

    row = [tile]
    tiles_per_row = sqrt(len(tiles))
    while all_tiles:
        matched_tile = None
        for tile in all_tiles:
            if fltr.matches(tile):
                matched_tile = tile

        if len(row) == tiles_per_row:
            image.append(row)
            fltr.left = None
            fltr.top = row[0].bottom
            row = []
            continue

        row.append(matched_tile)
        all_tiles.remove(matched_tile)
        fltr.top = None
        fltr.left = matched_tile.right
    image.append(row)

    img = Image(image)
    monsters = 0
    i = 0
    while not monsters:
        monsters = img.find_monsters()
        img.rotate()
        i += 1
        if i == 4:
            img.flip()

    return img.waves - (monsters * 15)
