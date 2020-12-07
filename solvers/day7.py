import re

REGEX = r"([\w| ]+) contain ([\d \w+|, ]+)"
BAG_REGEX = r"(\d) ([\w+| ]+)|no other bags"
MVP_BAG = "shiny gold bag"


def make_or_create_bag(bag_name, registry):
    if bag_name.endswith('bags'):
        bag_name = bag_name[:-1]
    bag = registry.get(bag_name, None)
    if not bag:
        bag = Bag(bag_name, registry)
        registry[bag_name] = bag
    return bag


class Bag:
    def __init__(self, name, registry):
        self.name = name
        self.registry = registry
        self.contains = {}

    def add_bags(self, bags):
        amount, bag_name = re.match(BAG_REGEX, bags).groups()
        if bag_name is not None:
            bag = make_or_create_bag(bag_name, self.registry)
            self.contains[bag] = int(amount)

    def has_bag(self, bag_name):
        for bag in self.contains.keys():
            if bag.name == bag_name or bag.has_bag(bag_name):
                return True
        return False

    def nested_bag_amount(self):
        amount = 0
        for bag, amounts in self.contains.items():
            amount += amounts + (amounts * bag.nested_bag_amount())
        return amount


def create_bags(puzzle_input):
    registry = {}
    for line in puzzle_input:
        container, contents = re.match(REGEX, line).groups()
        bag = make_or_create_bag(container, registry)
        for bags in contents.split(', '):
            bag.add_bags(bags)
    return registry


def solve1(puzzle_input):
    registry = create_bags(puzzle_input)
    return sum([b.has_bag(MVP_BAG) for b in registry.values()])


def solve2(puzzle_input):
    registry = create_bags(puzzle_input)
    return registry[MVP_BAG].nested_bag_amount()
