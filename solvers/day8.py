import copy


class InfiniteLoopError(Exception):
    pass


class UnrepairableError(Exception):
    pass


class Instruction:
    def __init__(self, memory, val):
        self.memory = memory
        self.val = int(val)
        self.visited = False

    def execute(self):
        if self.visited:
            raise InfiniteLoopError()
        self._execute()
        self.visited = True

    def _execute(self):
        self.memory.pc += 1


class Acc(Instruction):
    def _execute(self):
        self.memory.accumulator += self.val
        self.memory.pc += 1


class Jmp(Instruction):
    def _execute(self):
        self.memory.pc += self.val


OPERATIONS = {
    'acc': Acc,
    'jmp': Jmp,
    'nop': Instruction
}


class Loader:
    def __init__(self, instructions):
        self.instructions = instructions

    def load(self, memory):
        memory.instructions = []
        for instruction in self.instructions:
            op, val = instruction.split(" ")
            instruction = OPERATIONS[op](memory, val)
            memory.instructions.append(instruction)


class SelfRepairingLoader(Loader):
    def __init__(self, instructions):
        self.original_instructions = instructions
        self.instructions = instructions
        self.repaired_index = 0

    def attempt_repair(self):
        line = True
        self.instructions = copy.copy(self.original_instructions)
        while line:
            if self.repaired_index == len(self.original_instructions):
                raise UnrepairableError()
            line = self.original_instructions[self.repaired_index]
            if "nop" in line:
                line = line.replace("nop", "jmp")
            elif "jmp" in line:
                line = line.replace("jmp", "nop")
            else:
                self.repaired_index += 1
                continue
            self.instructions[self.repaired_index] = line
            self.repaired_index += 1
            line = None


class Memory:
    def __init__(self, loader):
        self.instructions = []
        self.accumulator = 0
        self.pc = 0
        loader.load(self)

    def run(self):
        try:
            self._run()
        except InfiniteLoopError:
            pass
        return self.accumulator

    def _run(self):
        while True:
            try:
                self.instructions[self.pc].execute()
            except IndexError:
                break


def solve1(puzzle_input):
    loader = Loader(puzzle_input)
    mem = Memory(loader)
    return mem.run()


def solve2(puzzle_input):
    loader = SelfRepairingLoader(puzzle_input)
    mem = Memory(loader)
    ended = False

    while not ended:
        try:
            mem._run()
        except InfiniteLoopError:
            loader.attempt_repair()
            mem = Memory(loader)
        else:
            ended = True
    return mem.accumulator
