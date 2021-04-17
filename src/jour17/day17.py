from typing import Dict, Set, Tuple
from aocd import get_data


def parse(raw: str) -> Set[Tuple[int, int]]:
    """Parse cubes possitions, exemple: `#.#` -> `[(0, 0), (2, 0)]`."""
    return {(x, y) for y, line in enumerate(raw.strip().split("\n"))
            for x, c in enumerate(line) if c == "#"}


def run(cubes: Set[Tuple[int, int]], dim: int = 3, cycle: int = 6) -> int:
    """Number of cube after `cycle` repetition in `dim` dimension."""
    # expend cube dimention
    previous_cubes = {cube + (0,) * (dim - 2) for cube in cubes}
    for cycle in range(cycle):
        actual_cubes: Set[Tuple[int, ...]] = set()
        counter_new: Dict[Tuple[int, ...], int] = {}
        for cube in previous_cubes:
            # because the original cube is recount
            nb_active = -1
            # recursively find the neighbor
            nearby = [cube]
            for i, pos in enumerate(cube):
                nearby = [(*near[:i], dpos, *near[i + 1:])
                          for near in nearby
                          for dpos in (pos - 1, pos, pos + 1)]
            # count the neighbors and increments the neighbors counter
            for near in nearby:
                counter_new[near] = counter_new.get(near, 0) + 1
                if near in previous_cubes:
                    nb_active += 1
            # keep cube only if it have 2 or 3 neighbors
            if nb_active in (2, 3):
                actual_cubes.add(cube)
        # add active cube where there is an area surrounded by 3 cubes
        for cube, count in counter_new.items():
            if count == 3 and cube not in previous_cubes:
                actual_cubes.add(cube)
        previous_cubes = actual_cubes
    return len(actual_cubes)


def part_one(cubes: Set[Tuple[int, int]]) -> int:
    """Number of cube after 6 repetition in 3 dimension."""
    return run(cubes, dim=3)


def part_two(cubes: Set[Tuple[int, int]]) -> int:
    """Number of cube after 6 repetition in 4 dimension."""
    return run(cubes, dim=4)


if __name__ == "__main__":
    print("--- Day 17: Conway Cubes ---")
    puzzle = parse(get_data(day=17, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
