from typing import Tuple
from aocd import get_data


def parse(raw: str) -> Tuple[int, int]:
    """Parse keys, exemple: `171 \\n 366` -> `(171, 366)`."""
    public_key_door, public_key_card = raw.strip().split("\n")
    return (int(public_key_door), int(public_key_card))


def part_one(public_keys: Tuple[int, int]) -> int:
    """Find loops size of public_key_door for get private key door."""
    public_key_door, public_key_card = public_keys
    value = 1
    loop_size = 0
    while public_key_door != value:
        value = value * 7 % 20201227
        loop_size += 1
    return pow(public_key_card, loop_size, 20201227)


def part_two(public_keys: Tuple[int, int]) -> int:
    """No part two this day, dummy function."""
    return 0


if __name__ == "__main__":
    print("--- Day 25: Combo Breaker ---")
    puzzle = parse(get_data(day=25, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
