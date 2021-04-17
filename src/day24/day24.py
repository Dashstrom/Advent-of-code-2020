import re

from typing import Dict, List, Set, Tuple
from aocd import get_data

PATH_RE = re.compile("(e|se|sw|w|nw|and|ne)")
vectorizer = {"ne": (1, 1), "e": (2, 0), "se": (1, -1),
              "sw": (-1, -1), "w": (-2, 0), "nw": (-1, 1)}

Paths = List[List[Tuple[int, int]]]


def parse(raw: str) -> Paths:
    """Parse paths, exemple: `newsw` -> `[[(1, 1), (-2, 0), (-1, -1)]]`."""
    return [[vectorizer[direction] for direction in PATH_RE.findall(path)]
            for path in raw.strip().split('\n')]


def place_tiles(paths_tiles: Paths) -> Set[Tuple[int, int]]:
    """Place all tiles in space following `paths_tiles`."""
    black_tiles: Set[Tuple[int, int]] = set()
    for path in paths_tiles:
        x, y = 0, 0
        for move in path:
            x += move[0]
            y += move[1]
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))
    return black_tiles


def part_one(paths_tiles: Paths) -> int:
    """Sum of placed tiles."""
    return len(place_tiles(paths_tiles))


def part_two(paths_tiles: Paths) -> int:
    """Sum of placed tiles after 100 with with life game like."""
    black_tiles = place_tiles(paths_tiles)
    for day in range(100):
        possibles_blacks: Dict[Tuple[int, int], int] = {}
        to_delete = set()
        for tile in black_tiles:
            black_near = 0
            for dx, dy in vectorizer.values():
                near = tile[0] + dx, tile[1] + dy
                if near in black_tiles:
                    black_near += 1
                else:
                    possibles_blacks[near] = possibles_blacks.get(near, 0) + 1
            if black_near == 0 or black_near > 2:
                to_delete.add(tile)

        for tile in to_delete:
            black_tiles.remove(tile)

        for possible_black, nb_black_near in possibles_blacks.items():
            if nb_black_near == 2:
                black_tiles.add(possible_black)
    return len(black_tiles)


if __name__ == "__main__":
    print("--- Day 24: Lobby Layout ---")
    puzzle = parse(get_data(day=24, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
