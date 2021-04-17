import _solver

from typing import List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """Parse numbers."""
    return [int(number) for number in raw.strip().splitlines()]


def part_one(numbers: List[int]) -> int:
    """Find two numbers whose sum is equal to 2020 and multiply them."""
    return _solver.part_one(numbers)  # type: ignore


def part_two(numbers: List[int]) -> int:
    """Find three numbers whose sum is equal to 2020 and multiply them."""
    return _solver.part_two(numbers)  # type: ignore


if __name__ == "__main__":
    print("--- Day 1: Report Repair ---")
    puzzle = parse(get_data(day=1, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
