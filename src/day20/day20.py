import re

from copy import deepcopy
from typing import Dict, List, Optional, Tuple
from aocd import get_data

MONSTER_RE_MID = re.compile("#....##....##....###")
MONSTER_RE_BOT = re.compile(".#..#..#..#..#..#...")
NEAR = ((0, -1), (1, 0), (0, 1), (-1, 0))


def rotate(sides: List[str]) -> List[str]:
    """Rotate slides of tile."""
    return [sides[1], sides[2][::-1], sides[3], sides[0][::-1]]


def flip(sides: List[str]) -> List[str]:
    """Flip slides of tile."""
    return [sides[2], sides[1][::-1], sides[0], sides[3][::-1]]


class Tile:
    def __init__(self, id_: int, content: List[List[str]]) -> None:
        self.content = content
        self.original = deepcopy(self.content)
        self.id = id_
        self.state = 0
        list_sides = (self.content[0], [line[-1] for line in self.content],
                      self.content[-1], [line[0] for line in self.content])
        self.sides = ["".join(list_side) for list_side in list_sides]
        sides = deepcopy(self.sides)
        self.possibilities = []
        for s in range(4):
            self.possibilities.append(list(sides))
            self.possibilities.append(flip(sides))
            sides = rotate(sides)

    def rotate(self, power: int) -> None:
        """Rotate the tile."""
        content = self.content
        if power % 4 != 0:
            for y in range(len(content) // 2):
                div, mod = divmod(len(content[0]), 2)
                for x in range(div + mod):
                    temp = content[y][x]
                    content[y][x] = content[x][-y - 1]
                    content[x][-y - 1] = content[-y - 1][-x - 1]
                    content[-y - 1][-x - 1] = content[-x - 1][y]
                    content[-x - 1][y] = temp
            self.rotate(power - 1)

    def flip(self) -> None:
        """Flip the tile."""
        self.content = self.content[::-1]

    def place_with_code(self, code_position: int) -> None:
        """Place tile with int."""
        self.content = deepcopy(self.original)
        self.state = code_position % 8
        self.rotate(code_position // 2)
        if code_position % 2 == 1:
            self.flip()
        self.sides = self.possibilities[code_position]

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.content)

    def __repr__(self) -> str:
        return f'Tile({self.id}, {self.state})'


Placements = Dict[Tuple[int, int], Tile]
Tiles = List[Tile]


def parse(raw: str) -> Tiles:
    """
    Parse tiles, example: `Tile 16: \\n .. \\n #.`
    -> `[Tile(16, [['.', '.'], ['#', '.']])]`.
    """
    tiles = []
    for raw_input in raw.strip().split("\n\n"):
        title, *content = raw_input.split("\n")
        tiles.append(Tile(int(title[5:-1]), [list(line) for line in content]))
    return tiles


def find_constraints(x: int, y: int, placements: Placements):
    """Find the side needed to place a tile at x y."""
    constraints: List[Optional[str]] = []
    for code_side_neighbour, (dx, dy) in enumerate(NEAR):
        try:
            side_constraints = placements[(x + dx, y + dy)]
        except KeyError:
            constraints.append(None)
        else:
            index = (code_side_neighbour + 2) % 4
            constraints.append(side_constraints.sides[index])
    return constraints


def find_placements(
        x: int,
        y: int,
        constraints: List[Optional[str]],
        tiles: Tiles,
        placements: Placements,
        length: int
) -> Optional[Placements]:
    """Find tile who match with constraints and return None if there is no."""
    for tile in tiles:
        for code, positioning in enumerate(tile.possibilities):
            if all(constraints[code_pos] is None
                   or face == constraints[code_pos]
                   for code_pos, face in enumerate(positioning)):
                tile.place_with_code(code)
                placements[(x, y)] = tile
                if is_valid(placements, length):
                    tiles.remove(tile)
                    temp_placements = possibilities_places(
                        placements, tiles, length)
                    if temp_placements:
                        return temp_placements
                    else:
                        tiles.append(tile)
                        del placements[(x, y)]
                else:
                    del placements[(x, y)]
    return None


def possibilities_places(
        placements: Placements, tiles: Tiles, length: int
) -> Optional[Placements]:
    """Find placement recursively or return None."""
    if is_valid(placements, length) and not tiles:
        return placements
    placements = deepcopy(placements)
    tiles = deepcopy(tiles)
    last_length = -1
    while len(tiles) != last_length:
        last_length = len(tiles)
        for x, y in list(placements.keys()):
            for nx, ny in NEAR:
                neighbour = placements.get((x + nx, y + ny))
                if not neighbour:
                    constraints = find_constraints(x + nx, y + ny, placements)
                    possible_placements = find_placements(
                        x + nx, y + ny, constraints, tiles, placements, length)
                    if possible_placements is not None:
                        return possible_placements
    return None


def size(placements: Placements) -> Tuple[int, int, int, int]:
    """Get size of placements."""
    min_x, min_y = next(iter(placements.keys()))
    max_x, max_y = min_x, min_y
    for (x, y) in placements.keys():
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
    return min_x, min_y, max_x, max_y


def is_valid(placements: Placements, length: int) -> bool:
    """Returns false if the puzzle is too large."""
    min_x, min_y, max_x, max_y = size(placements)
    return 0 <= max_x - min_x <= length and 0 < max_y - min_y <= length


def resolve(tiles: Tiles) -> Placements:
    """Solves the placement."""
    copy_tiles = deepcopy(tiles)
    tile = copy_tiles.pop(0)
    placements = possibilities_places({(0, 0): tile}, copy_tiles,
                                      int(len(tiles) ** 0.5))
    if placements:
        return placements
    else:
        raise Exception("No placements valid")


def part_one(tiles: Tiles) -> int:
    """Product of corners."""
    placements = resolve(tiles)
    min_x, min_y, max_x, max_y = size(placements)
    mul = 1
    corners = ((min_x, min_y), (min_x, max_y),
               (max_x, min_y), (max_x, max_y))
    for corner in corners:
        mul *= int(placements[corner].id)
    return mul


def merge(placements: Placements) -> Tile:
    """Merge all tile to one tile."""
    min_x, min_y, max_x, max_y = size(placements)
    true_place: List[List[Tile]] = [  # type: ignore
        [None for _ in range(max_x - min_x + 1)]
        for _ in range(max_y - min_y + 1)]

    for (x, y), tile in placements.items():
        true_place[y - min_y][x - min_x] = tile

    meta_tile = []
    for frise_tiles in true_place:
        for lines in zip(*[tile.content[1:-1] for tile in frise_tiles]):
            meta_tile.append([c for line in lines for c in line[1:-1]])
    return Tile(-1, meta_tile)


def part_two(tiles: Tiles) -> int:
    """Sum of pieces belonging to a monster."""
    placements = resolve(tiles)
    meta_tile = merge(placements)
    for positioning in range(8):
        monsters_part = 0
        meta_tile.place_with_code(positioning)
        tile = str(meta_tile).split("\n")
        for top, mid, bot in zip(tile[:-2], tile[1:-1], tile[2:]):
            for progress in range(len(bot) - 20):
                slice_line = slice(progress, progress + 20)
                if MONSTER_RE_BOT.fullmatch(bot[slice_line]):
                    if (MONSTER_RE_MID.match(mid[slice_line])
                            and top[slice_line][18] == "#"):
                        monsters_part += 15
        if monsters_part != 0:
            return sum(line.count("#") for line in tile) - monsters_part
    return str(meta_tile).count("#")


if __name__ == "__main__":
    print("--- Day 20: Jurassic Jigsaw ---")
    puzzle = parse(get_data(day=20, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
