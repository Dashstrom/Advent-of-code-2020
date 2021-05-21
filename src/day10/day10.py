from typing import List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """Parse numbers, example: `36 \\n 10` -> `[0, 10, 36, 39]`."""
    adapters = sorted([int(number) for number in raw.strip().splitlines()])
    return [0, *adapters, adapters[-1] + 3]


def part_one(adapters: List[int]) -> int:
    """Product of 1V connections and 3V connections among adapters."""
    counters = {1: 0, 3: 0}
    for previous, adapter in zip(adapters[:-1], adapters[1:]):
        counters[adapter - previous] += 1
    return counters[1] * counters[3]


def part_two(adapters: List[int]) -> int:
    """Numbers of possibilities of adapters connections."""
    possibilities, chain = 1, 0
    for i, adapter in enumerate(adapters[:-1]):
        if adapters[i + 1] - adapter == 1:
            chain += 1
        elif chain:
            if chain > 1:
                possibilities *= 2 + sum(range(2, chain))
            chain = 0
    return possibilities


if __name__ == "__main__":
    print("--- Day 10: Adapter Array ---")
    puzzle = parse(get_data(day=10, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
