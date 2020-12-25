import time


class LinkedList(dict):
    def __init__(self, lst):
        next_ref = lst[1:] + [lst[0]]
        prev_ref = [lst[-1]] + lst[:-1]

        for idx, (prev, nxt) in enumerate(zip(prev_ref, next_ref)):
            self[lst[idx]] = [prev, nxt]

    def next(self, index, amount=1):
        values = []
        for _ in range(amount):
            values.append(self[index][1])
            index = values[-1]
        return values

    def move(self, start, destination, amount):
        values = self.next(start, amount)

        # wire the removal
        rewire_start = self[values[0]][0]
        rewire_end = self[values[-1]][1]
        self[rewire_start][1] = rewire_end
        self[rewire_end][0] = rewire_start


        # wire removal start to new parent
        old_ref = self[destination][1]
        self[destination][1] = values[0]
        self[values[0]][0] = destination

        # wire removal end to new child
        self[old_ref][0] = values[-1]
        self[values[-1]][1] = old_ref

    def as_list(self, init_key=None):
        if not init_key:
            init_key = list(self.keys())[0]
        key = self[init_key][1]
        lst = [init_key]
        while key is not init_key:
            lst.append(key)
            key = self[key][1]
        return lst


def play(cups, rounds):
    current_cup = cups[0]
    max_tag = max(cups)
    ll = LinkedList(cups)

    for i in range(rounds):
        if i % 1000000 == 0:
            print(i)

        taken_cups = ll.next(current_cup, 3)

        destination_cup = None
        candidate = current_cup
        while not destination_cup:
            candidate -= 1
            if candidate < 1:
                candidate = max_tag
            if candidate not in taken_cups:
                destination_cup = candidate

        ll.move(current_cup, destination_cup, 3)
        current_cup = ll.next(current_cup)[0]
    return ll


def solve1(puzzle_input):
    cups = [int(i) for i in puzzle_input[0]]
    result = play(cups, 100).as_list(1)
    return "".join([str(i) for i in result[1:]])


def solve2(puzzle_input):
    rng = list(range(1, 1000001))
    cups = [int(i) for i in puzzle_input[0]]
    cups = cups + rng[len(cups):]
    ll = play(cups, 10000000)
    res1, res2 = ll.next(1, 2)
    return res1 * res2
