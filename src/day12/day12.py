from typing import Callable, Dict, List, Tuple
from aocd import get_data
from dataclasses import dataclass


Instruction = Tuple[str, int]
Instructions = List[Instruction]


ORIENTATIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIRECTIONS = {"N": (1, 0), "E": (0, 1), "S": (-1, 0), "W": (0, -1)}
ROTATIONS: Dict[int, Callable[[int, int], Tuple[int, int]]] = {
    0: lambda n, e: (n, e),
    1: lambda n, e: (e, -n),
    2: lambda n, e: (-n, -e),
    3: lambda n, e: (-e, n)
}


@dataclass
class Position:
    n: int = 0
    e: int = 0

    def move(self, direction: Tuple[int, int], distance: int) -> None:
        self.n += direction[0] * distance
        self.e += direction[1] * distance

    def rotate(self, rotation: int) -> None:
        func_rotate = ROTATIONS[rotation // 90 % 4]
        self.n, self.e = func_rotate(self.n, self.e)

    @property
    def manhattan_distance(self) -> int:
        return abs(self.e) + abs(self.n)


def parse(raw: str) -> Instructions:
    """Parse Instructions, exemple: `F18` -> `[('F', 18)]`."""
    return [(action_with_value[0], int(action_with_value[1:]))
            for action_with_value in raw.strip().split("\n")]


def part_one(instructions: Instructions) -> int:
    """
    Return manhattan distance after execute inscrition
    with rules of part two.
    """
    boat = Position()
    oriented = 1
    for action, value in instructions:
        try:
            boat.move(DIRECTIONS[action], value)
        except KeyError:
            if action == "F":
                boat.move(ORIENTATIONS[oriented], value)
            else:
                rotation = value if action == "R" else -value
                oriented = (oriented + rotation // 90) % 4
    return boat.manhattan_distance


def part_two(instructions: Instructions) -> int:
    """
    Return manhattan distance after execute instructions
    with hrules of part two.
    """
    boat = Position()
    waypoint = Position(1, 10)
    for action, value in instructions:
        try:
            waypoint.move(DIRECTIONS[action], value)
        except KeyError:
            if action == "F":
                boat.move((waypoint.n, waypoint.e), value)
            else:
                waypoint.rotate(value if action == "L" else -value)
    return boat.manhattan_distance


if __name__ == "__main__":
    print("--- Day 12: Rain Risk ---")
    puzzle = parse(get_data(day=12, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
