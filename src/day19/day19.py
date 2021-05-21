import regex

from typing import Dict, List, TypedDict
from aocd import get_data

NUMBERS_RE = regex.compile(r" (\d+)")


class RulesWithEntries(TypedDict):
    rules: Dict[str, str]
    entries: List[str]


def parse(raw: str) -> RulesWithEntries:
    """
    Precompute regex, `47: 7 10 | 5 11 \\n aaaaaaaa`
    -> `{'rules': {'47': '(?:(?:7 10 )|(?: 5 11))'} , 'entries': 'aaaaaaaa'}`.
    """
    raw_rules, raw_entries = raw.strip().split("\n\n")
    rules = {}
    for rule in raw_rules.split("\n"):
        key, under_rules = rule.split(":", 1)
        if under_rules[2] in "ab":
            rules[key] = under_rules[2]
        elif rule.find("|") != -1:
            rules[key] = f"(?:(?:{under_rules.replace(' |', ')|(?:')}))"
        else:
            rules[key] = f"(?:{under_rules})"
    return {"rules": rules, "entries": raw_entries.split("\n")}


def run(rules: Dict[str, str], entries: List[str]):
    """Compute the regex and count how many entry match it."""
    rule_0 = rules["0"]
    match = NUMBERS_RE.search(rule_0)
    while match:
        rule_0 = NUMBERS_RE.sub(rules[match[1]], rule_0, count=1)
        match = NUMBERS_RE.search(rule_0)
    rule_0_re = regex.compile(rule_0)
    return sum(1 for line in entries if rule_0_re.fullmatch(line))


def part_one(rules_entries: RulesWithEntries):
    """Valid word number with regex."""
    return run(rules_entries["rules"], rules_entries["entries"])


def part_two(rules_entries: RulesWithEntries):
    """Valid word number with a recursive patched regex."""
    patched_rules = dict(rules_entries["rules"])
    patched_rules.update({"8": " 42+?",
                          "11": "(?P<rec>(?: 42 31)|(?: 42(?&rec) 31))"})
    return run(patched_rules, rules_entries["entries"])


if __name__ == "__main__":
    print("--- Day 19: Monster Messages ---")
    puzzle = parse(get_data(day=19, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
