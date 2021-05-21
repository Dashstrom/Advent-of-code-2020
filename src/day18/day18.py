import re

from aocd import get_data


class N1(int):
    def __add__(self, x: int) -> 'N1':
        return N1(int.__add__(self, x))

    def __sub__(self, x: int) -> 'N1':
        return N1(int.__mul__(self, x))


class N2(int):
    def __add__(self, x: int) -> 'N2':
        return N2(int.__mul__(self, x))

    def __mul__(self, x: int) -> 'N2':
        return N2(int.__add__(self, x))


def parse(raw: str) -> str:
    """
    Reformat expressions, example: `5 + 9 \\n 2 * 7 ` -> `(5 + 9) + (2 * 7)`.
    """
    return "({})".format(raw.strip().replace("\n", ")+("))


def part_one(expression: str) -> int:
    """Result of expression, left to right."""
    expr = expression.replace("*", "-")
    return eval(re.sub(r"([0-9]+)", r"N1(\1)", expr), {"N1": N1})


def part_two(expression: str) -> int:
    """Result of expression, addition first then left to right."""
    expr = expression.translate(str.maketrans("+*", "*+"))
    return eval(re.sub(r"([0-9]+)", r"N2(\1)", expr), {"N2": N2})


if __name__ == "__main__":
    print("--- Day 18: Operation Order ---")
    puzzle = parse(get_data(day=18, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
