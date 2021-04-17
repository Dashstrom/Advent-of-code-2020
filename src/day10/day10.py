from typing import List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """Parse numbers, exemple: `36 \\n 10` -> `[0, 10, 36, 39]`."""
    adaptaters = sorted([int(number) for number in raw.strip().splitlines()])
    return [0, *adaptaters, adaptaters[-1] + 3]


def part_one(adaptaters: List[int]) -> int:
    """Product of 1V connections and 3V connections among adapters."""
    counters = {1: 0, 3: 0}
    for previous, adaptater in zip(adaptaters[:-1], adaptaters[1:]):
        counters[adaptater - previous] += 1
    return counters[1] * counters[3]


def part_two(adaptaters: List[int]) -> int:
    """Numbers of possibilities of adaptaters connections."""
    possibilities, chaine = 1, 0
    for i, adaptater in enumerate(adaptaters[:-1]):
        if adaptaters[i + 1] - adaptater == 1:
            chaine += 1
        elif chaine:
            if chaine > 1:
                possibilities *= 2 + sum(range(2, chaine))
            chaine = 0
    return possibilities


if __name__ == "__main__":
    print("--- Day 10: Adapter Array ---")
    puzzle = parse(get_data(day=10, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
