from typing import List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """Parse paths to seats into codes, `FFFBFBFLRR` -> `[81]`."""
    translation = str.maketrans("FLBR", "0011")
    return sorted(int(way.translate(translation), 2)
                  for way in raw.strip().split("\n"))


def part_one(seats: List[int]) -> int:
    """Hightest seat id."""
    return seats[-1]


def part_two(seats: List[int]) -> int:
    """The id between two ids with a difference of 2."""
    for i, id_place in enumerate(seats[1:]):
        if seats[i] + 2 == id_place:
            return id_place - 1
    raise IndexError("Can't find id")


if __name__ == "__main__":
    print("--- Day 5: Binary Boarding ---")
    puzzle = parse(get_data(day=5, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
