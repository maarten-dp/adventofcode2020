from collections import defaultdict


class Rule:
    def __init__(self, line, registry):
        name, rules = line.split(': ')
        self.name = name
        self.rules = []
        for rule in rules.split(' or '):
            self.rules.append([int(r) for r in rule.split("-")])
        registry['rules'].append(self)

    def is_valid_number(self, number):
        applies = []
        for low, high in self.rules:
            applies.append(low <= number <= high)
        return any(applies)

    def is_valid_numbers(self, numbers):
        for number in numbers:
            if not self.is_valid_number(number):
                return False
        return True


class Rules:
    def __init__(self):
        self.rules = []

    def append(self, rule):
        self.rules.append(rule)

    def is_invalid(self, ticket):
        invalid_fields = list(self.invalid_fields(ticket))
        return bool(invalid_fields)

    def invalid_fields(self, ticket):
        for nb in ticket.numbers:
            applies = []
            for rule in self.rules:
                applies.append(rule.is_valid_number(nb))
            if not any(applies):
                yield nb


class Ticket:
    registry_name = 'tickets'
    def __init__(self, line, registry):
        self.numbers = [int(n) for n in line.split(',')]
        registry[self.registry_name].append(self)


class MyTicket(Ticket):
    registry_name = 'my_ticket'


def get_field_candidates(tickets, rules):
    candidates = defaultdict(list)
    for idx, column in enumerate(zip(*[t.numbers for t in tickets])):
        for rule in rules.rules:
            if rule.is_valid_numbers(column):
                candidates[idx].append(rule.name)
    return candidates



def parse_input(lines):
    registry = {
        'rules': Rules(),
        'my_ticket': [],
        'tickets': []
    }

    parser = Rule
    for line in lines:
        if 'your ticket' in line:
            parser = MyTicket
        elif 'nearby tickets' in line:
            parser = Ticket
        elif not line:
            continue
        else:
            parser(line, registry)
    return registry


def solve1(puzzle_input):
    invalid_numbers = []
    registry = parse_input(puzzle_input)
    rules = registry['rules']
    for ticket in registry['tickets']:
        invalid_numbers.extend(rules.invalid_fields(ticket))
    return sum(invalid_numbers)


def solve2(puzzle_input):
    invalid_numbers = []
    registry = parse_input(puzzle_input)
    rules = registry['rules']
    valid_tickets = []
    for ticket in registry['tickets']:
        if not rules.is_invalid(ticket):
            valid_tickets.append(ticket)
    candidates = get_field_candidates(valid_tickets, rules)
    
    named_fields = defaultdict(list)

    while candidates:
        for idx, fields in dict(candidates).items():
            if len(fields) == 1:
                field = fields[0]
                named_fields[idx] = field
                candidates.pop(idx)
                for fields in candidates.values():
                    fields.remove(field)
    
    result = 1
    for idx, field in named_fields.items():
        if 'departure' in field:
            result *= registry['my_ticket'][0].numbers[idx]
    return result
