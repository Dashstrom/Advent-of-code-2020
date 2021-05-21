import _solver

from typing import List, TypedDict, Tuple
from aocd import get_data


DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1),
              (0, 1), (1, 0), (-1, 0), (0, -1))


class Seats(TypedDict):
    # position of neighbors of each seat
    nears: List[List[List[Tuple[int, int]]]]
    state: List[List[int]]


def part_one(seats: Seats) -> int:
    """Sum of seats after executed with rules of parte one."""
    return _solver.part_one(seats)  # type: ignore


def part_two(seats: Seats) -> int:
    """Sum of seats after executed with rules of parte two."""
    return _solver.part_two(seats)  # type: ignore


def parse(raw: str) -> Seats:
    """"Composed of and (L.)* return Seats"""
    return _solver.parse(raw)  # type: ignore


if __name__ == "__main__":
    print("--- Day 11: Seating System ---")
    puzzle = parse(get_data(day=11, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
