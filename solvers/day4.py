import re


def validate_height(field):
    rules = {
        'cm': (150, 193),
        'in': (59, 76),
    }
    match = re.match(r'(\d+)(cm|in)', field)
    if match:
        nb, unit = match.groups()
        hmin, hmax = rules[unit]
        return hmin <= int(nb) <= hmax
    return False


VALIDATORS = {
    "byr": lambda f: 1920 <= int(f) <= 2002,
    "iyr": lambda f: 2010 <= int(f) <= 2020,
    "eyr": lambda f: 2020 <= int(f) <= 2030,
    "hgt": validate_height,
    "hcl": lambda f: bool(re.match(r'#[0-9a-f]{6}', f)),
    "ecl": lambda f: f in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
    "pid": lambda f: bool(re.match(r'^\d{9}$', f)),
}

def parse_passports(passports, validator):
    parsed_passports = []
    fields = {}
    # making sure our last passport is validated
    passports.append(None)
    for line in passports:
        if not line:
            parsed_passports.append(validator(fields))
            fields = {}
        else:
            parsed = dict([f.split(':') for f in line.split(" ")])
            fields.update(parsed)
    return sum(parsed_passports)


def solve1(puzzle_input):
    validator = lambda f: all([f.get(field) for field in VALIDATORS.keys()])
    return parse_passports(puzzle_input, validator)


def solve2(puzzle_input):
    def validator(fields):
        for name, validate in VALIDATORS.items():
            try:
                if not validate(fields.get(name, None)):
                    return False
            except Exception as e:
                return False
        return True

    return parse_passports(puzzle_input, validator)
