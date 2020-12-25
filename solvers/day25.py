def encrypt(loop_size, subject_number):
    encryption_key = subject_number
    for _ in range(loop_size-1):
        encryption_key *= subject_number
        encryption_key %= 20201227
    return encryption_key


def find_loop_size(subject_number, public_key):
    loop_size = 1
    candidate_key = subject_number
    while not candidate_key == public_key:
        loop_size += 1
        candidate_key *= subject_number
        candidate_key %= 20201227
    return loop_size


def solve1(puzzle_input):
    card_key, door_key = [int(i) for i in puzzle_input]
    card_loop_size = find_loop_size(7, card_key)
    door_loop_size = find_loop_size(7, door_key)
    door_encryption_key = encrypt(card_loop_size, door_key)
    card_encryption_key = encrypt(door_loop_size, card_key)
    assert door_encryption_key, card_encryption_key
    return door_encryption_key

