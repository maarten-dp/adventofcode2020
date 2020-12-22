from collections import defaultdict
from itertools import chain


def get_allergen_candidates(puzzle_input):
    registry = defaultdict(set)
    all_ingredients = []

    for line in puzzle_input:
        ingredients, allergens = line.split(" (contains ")
        ingredients = ingredients.split(" ")
        all_ingredients.extend(ingredients)

        for allergen in allergens[:-1].split(", "):
            if not registry[allergen]:
                val = set(ingredients)
            else:
                val = registry[allergen].intersection(ingredients)
            registry[allergen] = val
    return registry, all_ingredients


def solve1(puzzle_input):
    registry, all_ingredients = get_allergen_candidates(puzzle_input)
    candidates = set()
    for value in registry.values():
        candidates.update(value)

    amount = 0
    for ingredient in set(all_ingredients).difference(candidates):
        amount += all_ingredients.count(ingredient)

    return amount


def solve2(puzzle_input):
    registry, all_ingredients = get_allergen_candidates(puzzle_input)
    
    while len(list(chain(*registry.values()))) != len(registry):
        for key, value in registry.items():
            if len(value) == 1:
                for k, v in registry.items():
                    if k == key:
                        continue
                    registry[k] = v.difference(value)

    ingredients = []
    for key in sorted(registry.keys()):
        ingredients.append(registry[key])

    return ",".join(chain(*ingredients))
