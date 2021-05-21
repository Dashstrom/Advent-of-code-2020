from typing import Dict, List
from aocd import get_data


def parse(raw: str) -> List[int]:
    """Parse digits."""
    return [int(number) for number in raw.strip()]


def part_one(cups: List[int]) -> int:
    """Concatenation labels on the cups after cup 1."""
    final_cups = play(cups, 100)
    previous = final_cups[1]
    result = ""
    while previous != 1:
        result += str(previous)
        previous = final_cups[previous]
    return int(result)


def play(
    cups: List[int], moves: int, numbers_of_cups: int = None
) -> Dict[int, int]:
    """Play the game of grab cups."""
    circle_cups = {previous: cup for previous, cup in zip(cups[:-1], cups[1:])}
    previous = cups[-1]
    if numbers_of_cups is not None:
        for cup in range(len(circle_cups) + 2, numbers_of_cups + 1):
            circle_cups[previous] = cup
            previous = cup
    circle_cups[previous] = cups[0]

    max_cup = max(circle_cups)
    current_cup = cups[0]
    for move in range(moves):
        first = circle_cups[current_cup]
        second = circle_cups[first]
        third = circle_cups[second]
        circle_cups[current_cup] = circle_cups[third]

        destination = current_cup - 1
        while (destination in (first, second, third, 0)
               or destination not in circle_cups):
            destination = max_cup if destination == 0 else destination - 1

        circle_cups[third] = circle_cups[destination]
        circle_cups[destination] = first
        current_cup = circle_cups[current_cup]
    return circle_cups


def part_two(cups: List[int]) -> int:
    """Product of the next two cups of cup 1."""
    final_cups = play(cups, 10_000_000, 1_000_000)
    return final_cups[1] * final_cups[final_cups[1]]


if __name__ == "__main__":
    print("--- Day 23: Crab Cups ---")
    puzzle = parse(get_data(day=23, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
