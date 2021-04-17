from typing import Dict, List, Set, Tuple
from aocd import get_data


Food = Tuple[List[str], List[str]]
Foods = List[Food]


def parse(raw: str) -> Foods:
    """
    Parse foods, exemple: `rzhb gsfqhcd (contains fish, shellfish)`
    -> `[(['rzhb', 'gsfqhcd'], ['fish', 'shellfish'])]`.
    """
    foods = []
    for line in raw.strip().split("\n"):
        ingredients, allergens = line.split(" (")
        foods.append((ingredients.split(" "),
                      allergens.strip()[9:-1].split(", ")))
    return foods


def part_one(foods: Foods) -> int:
    """Sum of ingredients who cannot possibly contain any of the allergens"""
    all_ingredients = foods_ingredients(foods)
    with_allergens = foods_allergens(allergens_possibilities(foods))
    without_allergens = all_ingredients - with_allergens
    return sum(ingredients.count(ingredient)
               for ingredients, _ in foods
               for ingredient in without_allergens)


def foods_ingredients(foods: Foods) -> Set[str]:
    """Set of ingreditents."""
    return set(ingredient
               for ingredients, _ in foods
               for ingredient in ingredients)


def allergens_possibilities(foods: Foods) -> Dict[str, Set[str]]:
    """
    Dict of allergent with the ingredients that may contain them as a key.
    """
    possibilities: Dict[str, Set[str]] = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            try:
                possibilities[allergen] &= set(ingredients)
            except KeyError:
                possibilities[allergen] = set(ingredients)
    return possibilities


def foods_allergens(possibilities: Dict[str, Set[str]]) -> Set[str]:
    """Set of allergens based on possibilities."""
    return set(allergen
               for allergens in possibilities.values()
               for allergen in allergens)


def part_two(foods: Foods) -> str:
    """Return Textual list of all ingredients containing allergens."""
    possibilities = allergens_possibilities(foods)
    matched: Set[str] = set()
    matchs = []
    while possibilities:
        allergen, ingredient = min(possibilities.items(),
                                   key=lambda ai: len(ai[1] - matched))
        available_ingredients = ingredient - matched
        ingredian = available_ingredients.pop()
        matched.add(ingredian)
        matchs.append((ingredian, allergen))
        del possibilities[allergen]
    matchs.sort(key=lambda k: k[1])
    return ",".join(ingredient for ingredient, _ in matchs)


if __name__ == "__main__":
    print("--- Day 21: Allergen Assessment ---")
    puzzle = parse(get_data(day=21, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
