import pkgutil
import os.path as osp
from collections import defaultdict
import copy

SOLVER_PKG = 'solvers'
TEST_LOCATION = 'test_input'
HEADER = "=" * 50

def print_title(title):
    print(HEADER)
    print(title)
    print(HEADER)


def get_test_case(file_name):
    test_case = defaultdict(list)
    with open(osp.join('test_input', file_name)) as fh:
        section = None
        for line in fh.readlines():
            line = line.strip('\n')
            if line.startswith('['):
                section = line[1:-1]
                continue
            if not section:
                raise Exception('Wrongly configured test case')
            if not line:
                continue
            test_case[section].append(line)
    return test_case


def run_test(puzzle_input, solve, expected):
    result = str(copy.deepcopy(solve(puzzle_input)))
    solver_name = solve.__name__
    if result != expected:
        print('TEST {} FAILED: {} != {}'.format(solver_name, result, expected))
    else:
        print('TEST {} OK'.format(solver_name))


for modelinfo in pkgutil.iter_modules([SOLVER_PKG]):
    day_module = modelinfo.name
    importer = modelinfo.module_finder
    solver = importer.find_module(day_module).load_module(day_module)

    puzzle_input = open(osp.join('input', modelinfo.name)).readlines()
    puzzle_input = [line.strip('\n') for line in puzzle_input]

    print_title(day_module)
    test_case = get_test_case(modelinfo.name)

    run_test(test_case['input'], solver.solve1, test_case['expected1'][0])
    print("RESULT 1:", solver.solve1(copy.deepcopy(puzzle_input)))

    if hasattr(solver, 'solve2'):
        run_test(test_case['input'], solver.solve2, test_case['expected2'][0])
        print("RESULT 2:", solver.solve2(copy.deepcopy(puzzle_input)))

