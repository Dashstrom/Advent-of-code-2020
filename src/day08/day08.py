from typing import List, Optional, Tuple
from aocd import get_data


Instruction = Tuple[str, int]
Instructions = List[Instruction]


def parse(raw: str) -> Instructions:
    """
    Parse instructions, exemple: `nop +38 \\n acc -9 \\n jmp +452`
    -> `[('nop', 38), ('acc', -9), ('jmp', 452)]`.
    """
    return [(t, int(v))
            for t, v in map(lambda i: i.split(" "), raw.strip().split("\n"))]


def execute(instructions: Instructions) -> Tuple[int, bool]:
    """
    Excecute instructions and return accumulator value
    and True if the program is a loop.
    """
    already_exe = [False for _ in instructions]
    acc, line = 0, 0
    while line < len(instructions) and not already_exe[line]:
        instruction = instructions[line]
        already_exe[line] = True
        if instruction[0] == "acc":
            acc += instruction[1]
        line += instruction[1] if instruction[0] == "jmp" else 1
    return acc, line < len(instructions)


def part_one(instructions: Instructions) -> int:
    """Accumulator value after execute inscriptions without loop."""
    return execute(instructions)[0]


def swap(instruction: Instruction) -> Instruction:
    """Swap `nop` into `jmp` and `jmp` into `nop`."""
    return "nop" if instruction[0] == "jmp" else "jmp", instruction[1]


def part_two(instructions: Instructions) -> Optional[int]:
    """
    Accumulator value after repair by swaping the instruction
    for remove loop and execute inscriptions.
    """
    is_loop, i, acc = True, -1, None
    while is_loop and i < len(instructions):
        while i < len(instructions):
            i += 1
            instruction = instructions[i]
            if instruction[0] in ("jmp", "nop"):
                instructions[i] = swap(instruction)
                acc, is_loop = execute(instructions)
                instructions[i] = instruction
                break
    return None if is_loop else acc


if __name__ == "__main__":
    print("--- Day 8: Handheld Halting ---")
    puzzle = parse(get_data(day=8, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
