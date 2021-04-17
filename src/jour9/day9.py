from typing import Dict, List, TypeVar
from aocd import get_data

T = TypeVar("T")


def parse(raw: str) -> List[int]:
    """Parse numbers."""
    return [int(number) for number in raw.strip().splitlines()]


def part_one(numbers: List[int]) -> int:
    """
    Find the number that is not the sum of any of the preceding 25,
    return 0 if not found.
    """
    previous_numbers: Dict[int, int] = {}
    for n in numbers[:25]:
        previous_numbers[n] = previous_numbers.get(n, 0) + 1
    for first, number in zip(numbers, numbers[25:]):
        for previous in previous_numbers:
            if number - previous in previous_numbers:
                break
        else:
            return number
        previous_numbers[number] = previous_numbers.get(number, 0) + 1
        if previous_numbers[first] == 1:
            del previous_numbers[first]
        else:
            previous_numbers[first] -= 1
    return 0


def part_two(numbers: List[int]) -> int:
    """
    Return the sum of min and max of numbers set who is equal
    to number obtains in part one, return 0 if not found.
    """
    if not numbers:
        return 0
    target = part_one(numbers)
    sum_numbers = numbers[0]
    j = 1
    for i in range(len(numbers) - 1):
        while target >= sum_numbers and j < len(numbers):
            sum_numbers += numbers[j]
            j += 1
            if target == sum_numbers and j - i >= 1:
                return min(numbers[i:j]) + max(numbers[i:j])
        j -= 1
        sum_numbers -= numbers[j] + numbers[i]
    return 0


if __name__ == "__main__":
    print("--- Day 9: Encoding Error ---")
    puzzle = parse(get_data(day=9, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
