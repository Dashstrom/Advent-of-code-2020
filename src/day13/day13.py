from typing import List, NamedTuple
from aocd import get_data


class Schedules(NamedTuple):
    timestamp: int
    ids: List[int]


def parse(raw: str) -> Schedules:
    """
    Parse timstamp and numbers, exemple: `1000390 \\n 13,x,41`
    -> Schedules(1000390, [13, 0, 41]).
    """
    timestamp, raw_ids = raw.strip().split("\n")
    ids = [int(id) for id in raw_ids.replace("x", "0").split(',')]
    return Schedules(int(timestamp), ids)


def part_one(schedules: Schedules) -> int:
    """Product of the id of the next bus by the time to wait for it."""
    next_in, id_ = min(((id - schedules.timestamp % id, id)
                        for id in schedules.ids if id), key=lambda di: di[0])
    return next_in * id_


def part_two(schedules: Schedules) -> int:
    """
    The earliest timestamp such that all of the listed bus IDs depart
    at offsets matching their positions in the list.
    """
    match_time: int = 0
    bus = [(lag, id) for lag, id in enumerate(schedules.ids) if id]
    _, step = bus.pop(0)
    while bus:
        for lag, id in reversed(bus):
            if (match_time + lag) % id == 0:
                step *= id
                bus.remove((lag, id))
        match_time += step
    return match_time - step


if __name__ == "__main__":
    print("--- Day 13: Shuttle Search ---")
    puzzle = parse(get_data(day=13, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
