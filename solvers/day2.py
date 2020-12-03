
def parse_password(line):
    constraints, letter, password = line.split(" ")
    lower, upper = constraints.split('-')
    letter = letter[0]
    return upper, lower, letter, password


def solve1(puzzle_input):
    valid_password = 0
    for line in puzzle_input:
        upper, lower, letter, password = parse_password(line)
        amount = password.count(letter)

        if int(lower) <= amount <= int(upper):
            valid_password += 1
    return valid_password


def solve2(puzzle_input):
    valid_password = 0
    for line in puzzle_input:
        upper, lower, letter, password = parse_password(line)
        lower_letter = password[int(lower) - 1]
        upper_letter = password[int(upper) - 1]

        has_letter = lower_letter == letter or upper_letter == letter
        is_not_both = not (lower_letter == letter and upper_letter == letter)

        if has_letter and is_not_both:
            valid_password += 1
    return valid_password


