from collections import defaultdict
from itertools import product
import re

IDX_RE = r"mem\[(\d+)\]"


class Mask:
    def __init__(self, mask):
        self.or_mask = int(mask.replace('X', '0'), 2)
        self.and_mask = int(mask.replace('X', '1'), 2)

    def apply(self, val):
        val |= self.or_mask
        val &= self.and_mask
        return val


class AddressDecoder:
    def __init__(self, mask):
        self.masks = []
        self.or_mask = int(mask.replace('X', '0'), 2)
        template = mask.replace('X', '{}').replace('0', 'X').replace('1', 'X')
        variations = mask.count('X')
        for perm in product('01', repeat=variations):
            self.masks.append(Mask(template.format(*perm)))

    def apply(self, val):
        to_write = []
        val |= self.or_mask
        for mask in self.masks:
            to_write.append(mask.apply(val))
        return to_write



def solve1(puzzle_input):
    memory = defaultdict(lambda: 0)
    mask = None
    for line in puzzle_input:
        instr, value = line.split(' = ')
        if instr == 'mask':
            mask = Mask(value)
        else:
            mem_idx = int(re.match(IDX_RE, instr).groups()[0])
            value = mask.apply(int(value))
            memory[mem_idx] = value
    return sum(memory.values())


def solve2(puzzle_input):
    memory = defaultdict(lambda: 0)
    decoder = None
    for line in puzzle_input:
        instr, value = line.split(' = ')
        if instr == 'mask':
            decoder = AddressDecoder(value)
        else:
            mem_idx = int(re.match(IDX_RE, instr).groups()[0])
            for idx in decoder.apply(int(mem_idx)):
                memory[idx] = int(value)
    return sum(memory.values())
