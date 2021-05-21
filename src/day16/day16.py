from typing import Dict, List, Tuple, TypedDict
from aocd import get_data


class RecursiveList(list):
    def __contains__(self, item):
        for range_ in self:
            if item in range_:
                return True
        return False


class Tickets(TypedDict):
    ticket: List[int]
    nearby: List[Tuple[int, ...]]
    fields: Dict[str, RecursiveList]


def parse(raw: str) -> Tickets:
    """
    Parse field, ticket and nearby tickets, example: `
    wagon: 3-6 or 8-9 \\n
    zone: 4-47 or 49-96 \\n\\n
    your ticket: \\n 4,9 \\n\\n
    nearby tickets: \\n 10,3`
    -> `{'ticket': [4, 9], 'nearby': [[10, 3]],
    'fields': {'wagon': RecursiveList([range(3, 9), range(8, 9)]),
    'zone': RecursiveList([range(4, 47), range(49, 96)])}}`.
    """
    data: Data = {}  # type: ignore
    raw_fields, raw_ticket, raw_nearby = raw.strip().split("\n\n")
    ticket = raw_ticket.split("\n")[1].split(",")
    data["ticket"] = [int(value) for value in ticket]
    data["nearby"] = [[int(value) for value in nearby.split(",")]
                      for nearby in raw_nearby.split("\n")[1:]]
    data["fields"] = {}
    for raw_field in raw_fields.split("\n"):
        name, raw_ranges = raw_field.split(": ")
        ranges = []
        for raw_range in raw_ranges.split(" or "):
            left, right = raw_range.split("-", 1)
            ranges.append(range(int(left), int(right) + 1))
        data["fields"][name] = RecursiveList(ranges)
    return data


def part_one(tickets: Tickets) -> int:
    """Return the sum of all values who are outside all ranges."""
    all_ranges = RecursiveList(tickets["fields"].values())
    return sum(value for ticket in tickets["nearby"]
               for value in ticket if value not in all_ranges)


def part_two(tickets: Tickets) -> int:
    """Return the sum of all values that are in no ranges."""
    # match my field with all the possible fields
    fields = tickets["fields"]
    ticket = tickets["ticket"]
    nearby = tickets["nearby"]
    all_possible_fields = [(value, {name for name, ranges in fields.items()
                                    if value in ranges})
                           for value in ticket]
    # look at all the fields and delete those which are not possible
    ranges_fields = [RecursiveList(fields[name] for name in possibilities[1])
                     for possibilities in all_possible_fields]
    for near in nearby:
        for pos, value in enumerate(near):
            ranges_field = ranges_fields[pos]
            possibilities = all_possible_fields[pos][1]
            if value in ranges_fields[pos]:
                for name, ranges in zip(tuple(possibilities), ranges_field):
                    if value not in ranges:
                        ranges_field.remove(ranges)
                        possibilities.remove(name)
    # sort the possibilities of the fields
    # by those with the fewest possibilities
    taken, total = set(), 1
    all_possible_fields.sort(key=lambda fc: len(fc[1]))
    for value, possible_fields in all_possible_fields:
        for field in possible_fields:
            if field not in taken:
                taken.add(field)
                if field.startswith("departure"):
                    total *= value
    return total


if __name__ == "__main__":
    print("--- Day 16: Ticket Translation ---")
    puzzle = parse(get_data(day=16, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
