import re

from typing import List, Tuple
from aocd import get_data


Passport = List[Tuple[str, str]]
Passports = List[Passport]

REQUIRED = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
FIELDS_RE = {
    'byr': re.compile(r"19[2-9][0-9]|200[0-2]"),
    'iyr': re.compile(r"20(?:20|1[0-9])"),
    'eyr': re.compile(r"20(?:30|2[0-9])"),
    'hcl': re.compile(r"#[0-9a-f]{6}"),
    'ecl': re.compile(r"amb|blu|brn|gry|grn|hzl|oth"),
    'pid': re.compile(r"[0-9]{9}"),
    'cid': re.compile(r".*"),
    'hgt': re.compile(r"(?:1[5-8][0-9]|19[0-3])cm|(?:59|6[0-9]|7[0-6])in")
}


def parse(raw: str) -> Passports:
    """
    Parse passports,
    example `hcl:#ae17e1 iyr:2013` -> `[('hcl', '#ae17e1'), ('iyr', '2013')]`.
    """
    passports = []
    for raw_passport in raw.strip().split("\n\n"):
        passport = []
        for line in raw_passport.replace("\n", " ").split(" "):
            field, value = line.split(":", maxsplit=1)
            passport.append((field, value))
        passports.append(passport)
    return passports


def part_one(passports: Passports) -> int:
    """Sum of passports who have required field."""
    valid = 0
    for passport in passports:
        passport_fields = {field[0] for field in passport}
        if all(field in passport_fields for field in REQUIRED):
            valid += 1
    return valid


def part_two(passports: Passports) -> int:
    """Sum of passports who have required field and valid value."""
    valid = 0
    for passport in passports:
        passport_fields = {field[0] for field in passport}
        if all(field in passport_fields for field in REQUIRED):
            for (field, value) in passport:
                try:
                    if not FIELDS_RE[field].fullmatch(value):
                        break
                except KeyError:
                    break
            else:
                valid += 1
    return valid


if __name__ == "__main__":
    print("--- Day 4: Passport Processing ---")
    puzzle = parse(get_data(day=4, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
