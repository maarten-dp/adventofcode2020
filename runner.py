import pkgutil
import os.path as osp
from collections import defaultdict
import copy
import time
import sys

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
            test_case[section].append(line)
    return test_case


def run_test(puzzle_input, solve, expected):
    result = str(solve(copy.deepcopy(puzzle_input)))
    solver_name = solve.__name__
    if result != expected:
        print('TEST {} FAILED: {} != {}'.format(solver_name, result, expected))
    else:
        print('TEST {} OK'.format(solver_name))


def run(puzzle_input, solve):
    t1 = time.time()
    result = solve(copy.deepcopy(puzzle_input))
    print("RESULT:", result, "({:.5f}s)".format(time.time() - t1))


def run_for_day(importer, day_module, moduleinfo):
    solver = importer.find_module(day_module).load_module(day_module)

    puzzle_input = open(osp.join('input', moduleinfo.name)).readlines()
    puzzle_input = [line.strip('\n') for line in puzzle_input]

    print_title(day_module)
    test_case = get_test_case(moduleinfo.name)

    run_test(test_case['input'], solver.solve1, test_case['expected1'][0])
    run(puzzle_input, solver.solve1)

    if hasattr(solver, 'solve2'):
        run_test(test_case['input'], solver.solve2, test_case['expected2'][0])
        run(puzzle_input, solver.solve2)


modules = {}
for moduleinfo in pkgutil.iter_modules([SOLVER_PKG]):
    day_module = moduleinfo.name
    importer = moduleinfo.module_finder
    modules[day_module.replace('day', '')] = (importer, day_module, moduleinfo)

if len(sys.argv) == 2:
    run_for_day(*modules[sys.argv[1]])
else:
    run_for_day(*modules[str(len(modules))])
