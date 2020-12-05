def get_row_and_column(line):
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    column = int(line[7:].replace('L', '0').replace('R', '1'), 2)
    return row, column


def solve1(puzzle_input):
    max_seat = 0
    for line in puzzle_input:
        row, column = get_row_and_column(line)
        max_seat = max(max_seat, row * 8 + column)
    return max_seat


def solve2(puzzle_input):
    taken_seats = set()
    all_seats = set()
    for line in puzzle_input:
        row, column = get_row_and_column(line)
        taken_seats.add(row * 8 + column)
    for row in range(128):
        for column in range(8):
            all_seats.add(row * 8 + column)

    candidate = None
    for seat in all_seats.difference(taken_seats):
        if seat - 1 in taken_seats and seat + 1 in taken_seats:
            if candidate:
                raise Exception("Multiple seats found")
            candidate = seat
    return candidate
