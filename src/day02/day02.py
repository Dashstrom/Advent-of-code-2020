import re

from typing import List, Tuple
from aocd import get_data


Password = Tuple[int, int, str, str]
Passwords = List[Password]

LINE_RE = re.compile(r"([0-9]*)-([0-9]*) (.): (.*)")


def parse(raw: str) -> Passwords:
    """Parse passwords, exemple: `1-3 b: cdefg` -> `(1, 3, 'b', 'cdefg')`."""
    parsed = []
    for line in raw.strip().split("\n"):
        if match := LINE_RE.fullmatch(line):
            n1, n2, c, password = match.groups()
        else:
            raise ValueError(f"{line} is not a valid field")
        parsed.append((int(n1), int(n2), c, password))
    return parsed


def part_one(passwords: Passwords) -> int:
    """Sum of passwords who have the right count of the character."""
    return sum(1 for min_c, max_c, c, password in passwords
               if min_c <= password.count(c) <= max_c)


def part_two(passwords: Passwords) -> int:
    """Sum of passwords who have the right char at one right place."""
    return sum(1 for first, second, c, password in passwords
               if (password[first - 1] == c) ^ (password[second - 1] == c))


if __name__ == "__main__":
    print("--- Day 2: Password Philosophy ---")
    puzzle = parse(get_data(day=2, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
