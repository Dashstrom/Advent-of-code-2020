from typing import List, Tuple
from aocd import get_data

Question = Tuple[str, int]
Questions = List[Question]


def parse(raw: str) -> Questions:
    """Parse survey, example: `f \\n nv \\n ki` -> `[('fvki', 3)]`."""
    return [(survey.replace("\n", ""), survey.count("\n") + 1)
            for survey in raw.strip().split("\n\n")]


def part_one(questions: Questions) -> int:
    """Sum of questions reply by all groups."""
    return sum(len(set(group[0])) for group in questions)


def part_two(questions: Questions) -> int:
    """Sum of questions where all reply yes for all groups."""
    return sum(sum(1 for question in set(group[0])
                   if group[0].count(question) == group[1])
               for group in questions)


if __name__ == "__main__":
    print("--- Day 6: Custom Customs ---")
    puzzle = parse(get_data(day=6, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
