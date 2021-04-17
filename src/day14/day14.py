import re

from itertools import combinations
from typing import Dict, List, Tuple, Union
from aocd import get_data


Instruction = Union[str, Tuple[int, int]]
Instructions = List[Instruction]


MEM_RE = re.compile(r"mem\[(\d+)\] = (\d+)")
MASK_RE = re.compile(r"mask = ([01X]*)")


def parse(raw: str) -> Instructions:
    """
    Parse instructions, exemple: `mask = 01X10001 \\n mem[7] = 33`
    -> `['01X10001', (7, 33)]`.
    """
    instructions: Instructions = []
    for line in raw.strip().split("\n"):
        if mem := MEM_RE.match(line):
            instructions.append((int(mem[1]), int(mem[2])))
        elif mask := MASK_RE.match(line):
            instructions.append(mask[1])
    return instructions


def part_one(instructions: Instructions) -> int:
    """
    Sum of values in memory.
    The numbers put in the memory come from the previous mask.
    """
    mem: Dict[int, int] = {}
    mask_0 = mask_1 = 0
    for instruction in instructions:
        if isinstance(instruction, str):
            mask_0 = mask_1 = 0
            for pos, bit in enumerate(instruction):
                if bit == "1":
                    mask_1 += 1 << (35 - pos)
                elif bit == "0":
                    mask_0 += 1 << (35 - pos)
            mask_0 = ~mask_0
        else:
            mem[instruction[0]] = (instruction[1] | mask_1) & mask_0
    return sum(mem.values())


def part_two(instructions: Instructions) -> int:
    """Sum of values in memory after part two."""
    mem: Dict[int, int] = {}
    mask_0, mask_1 = 0, 0
    for instruction in instructions:
        if isinstance(instruction, str):
            base_mask = []
            mask_1 = 0
            for pos, bit in enumerate(instruction):
                if bit == "X":
                    base_mask.append(1 << (35 - pos))
                elif bit == "1":
                    mask_1 += 1 << (35 - pos)
            mask_0 = ~sum(base_mask)
            # generates all possible masks for this instruction
            masks = {sum(mask) for lenght in range(1 << len(base_mask))
                     for mask in combinations(base_mask, r=lenght)}
        else:
            binary = (instruction[0] | mask_1) & mask_0
            # put value into all posibilities
            for mask in masks:
                mem[binary | mask] = instruction[1]
    return sum(mem.values())


if __name__ == "__main__":
    print("--- Day 14: Docking Data ---")
    puzzle = parse(get_data(day=14, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
