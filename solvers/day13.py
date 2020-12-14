def solve1(puzzle_input):
    arrival_time, busses = puzzle_input
    arrival_time = int(arrival_time)
    closest_departures = {}
    for bus in busses.split(','):
        if bus == 'x':
            continue
        closest_departures[int(bus) - arrival_time % int(bus)] = int(bus)
    closest_departure = min(closest_departures.keys())
    return closest_departures[closest_departure] * closest_departure


def solve2(puzzle_input):
    raw_busses = puzzle_input[1].split(',')
    busses = {idx: int(bus) for idx, bus in enumerate(raw_busses) if bus != 'x'}

    rest = busses.pop(0)
    i = rest
    for offset, bus in busses.items():
        while (rest + i + offset) % bus != 0:
            rest += i
        rest += i
        i *= bus

    return rest
