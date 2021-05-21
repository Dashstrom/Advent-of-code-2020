import re

from typing import Dict, Set
from aocd import get_data

Bags = Dict[str, int]
Rules = Dict[str, Bags]
ITER_LINE_RE = re.compile(r"([0-9+]) ([^,]+) bag")


def parse(raw: str) -> Rules:
    """
    Parse bags rules, example: `dotted plum bags contain 3 wavy cyan bags`
    ->`{'dotted plum': {'wavy cyan': 3}}`.
    """
    bags: Rules = {}
    for line in raw.strip().split("\n"):
        name = line[:line.find(" bags")]
        bags[name] = {bag: int(number)
                      for number, bag in ITER_LINE_RE.findall(line)}
    return bags


def part_one(rules: Rules) -> int:
    """Bags counts containing shiny gold bag."""
    reverse_rules: Dict[str, Set[str]] = {}
    for bag, content in rules.items():
        for bag_contained in content:
            try:
                reverse_rules[bag_contained].add(bag)
            except KeyError:
                reverse_rules[bag_contained] = {bag}
    bags_with_shiny: Set[str] = set()
    stack = ["shiny gold", ]
    count = 0
    while stack:
        bag = stack.pop()
        count += 1
        news = reverse_rules.get(bag, set()) - bags_with_shiny
        stack.extend(news)
        bags_with_shiny.update(news)
    return count - 1


def sum_recursive(bags: Bags, rules: Rules) -> int:
    """Sum of bags contained in the bag of a bag."""
    return sum(number * sum_recursive(rules[name], rules)
               if name in rules else number
               for name, number in bags.items()) + 1


def part_two(rules: Rules) -> int:
    """Sum of all bags that can be contained in each bag."""
    return sum_recursive(rules["shiny gold"], rules) - 1


if __name__ == "__main__":
    print("--- Day 7: Handy Haversacks ---")
    puzzle = parse(get_data(day=7, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
