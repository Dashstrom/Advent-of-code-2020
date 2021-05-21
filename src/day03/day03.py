from typing import List
from aocd import get_data


Forest = List[List[bool]]


def parse(raw: str) -> Forest:
    """Parse forest, example: \n `#.` -> `[[True, False]]`."""
    return [[c != "." for c in line] for line in raw.strip().splitlines()]


def part_one(forest: Forest) -> int:
    """Numbers of trees hit in Toboggan Trajectory."""
    length = len(forest[0])
    return sum(1 for i, line in enumerate(forest)
               if line[(i * 3) % length])


def part_two(forest: Forest) -> int:
    """The product of the numbers of trees to hit at each trajectory."""
    answer = 1
    length = len(forest[0])
    for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        x, trees = 0, 0
        for y in range(0, len(forest), dy):
            if forest[y][x]:
                trees += 1
            x = (x + dx) % length
        answer *= trees
    return answer


if __name__ == "__main__":
    print("--- Day 3: Toboggan Trajectory ---")
    puzzle = parse(get_data(day=3, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
