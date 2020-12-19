from collections import defaultdict
from itertools import product, chain


class Rule:
    def __init__(self, registry):
        self.registry = registry
        self.or_rules = []
        self._generated = None

    def __iter__(self):
        for r in self.value:
            yield r

    def parse_rule(self, rule):
        self.raw_rule = rule
        for or_def in rule.split(" | "):
            or_rule = []
            for dependency in or_def.split(" "):
                if dependency in '"a""b"':
                    or_rule.append([dependency[1]])
                    continue
                or_rule.append(self.registry[dependency])
            self.or_rules.append(or_rule)

    @property
    def value(self):
        if not self._generated:
            for idx, rules in enumerate(self.or_rules):
                for i, rule in enumerate(rules):
                    if isinstance(rule, Rule):
                        rules[i] = rule.value
                self.or_rules[idx] = ["".join(comb) for comb in product(*rules)]
            self._generated = list(chain(*self.or_rules))
        return self._generated


def parse_input(lines):
    messages = []
    rules = defaultdict(lambda: Rule(rules))

    for line in lines:
        if not line:
            continue
        if ':' in line:
            index, rule = line.split(': ')
            rules[index].parse_rule(rule)
        else:
            messages.append(line)
    return rules, messages


def solve1(puzzle_input):
    rules, messages = parse_input(puzzle_input)

    valid_counter = 0
    for message in messages:
        if message in rules["0"].value:
            valid_counter += 1
    return valid_counter


def solve2(puzzle_input):
    rules, messages = parse_input(puzzle_input)

    valid_messages = 0
    invalid_message = []
    for message in messages:
        if message in rules["0"].value:
            valid_messages += 1
        else:
            invalid_message.append(message)


    # I'm not smart enough for this (yet ;)) So imma just hack it.
    def find_start(message):
        for start in rules["8"].value:
            if message.startswith(start):
                return message[len(start):]

    def find_end(message):
        for start in rules["42"].value:
            for end in rules["31"].value:
                if message.startswith(start) and message.endswith(end):
                    return message[len(start): -len(end)]

    msgs = 0
    for message in invalid_message:
        candidates = []
        while message:
            message = find_start(message)
            if message:
                candidates.append(message)

        for message in candidates:
            while message:
                message = find_end(message)
            if message == '':
                msgs += 1
    return valid_messages + msgs
