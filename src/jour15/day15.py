from typing import List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """List of numbers."""
    return [int(number) for number in raw.strip().split(",")]


def number_spoken(numbers: List[int], at: int) -> int:
    """
    Return last number.

    If that was the first time the number has been spoken,
    the current player says 0.

    Otherwise, the number had been spoken before;
    the current player announces how many turns apart the number
    is from when it was previously spoken.
    """
    last = {n: t for t, n in enumerate(numbers[:-1], start=1)}
    last_number = numbers[-1]
    for turn in range(len(numbers), at):
        if (number := last.get(last_number)) is None:
            last[last_number], last_number = turn, 0
        else:
            last[last_number], last_number = turn, turn-number
    return last_number


def part_one(numbers: List[int]) -> int:
    """Game for 2020 turn."""
    return number_spoken(numbers, 2020)


def part_two(numbers: List[int]) -> int:
    """Game for 30 000 000 turn."""
    return number_spoken(numbers, 30_000_000)


if __name__ == "__main__":
    print("--- Day 15: Rambunctious Recitation ---")
    puzzle = parse(get_data(day=15, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
