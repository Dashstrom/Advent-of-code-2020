from typing import List, Tuple
from aocd import get_data

Decks = List[List[int]]


def parse(raw: str) -> Decks:
    """Parse decks, example: `Player 1: \\n 41` -> `[[41]]`."""
    return [[int(card) for card in deck.split('\n')[1:]]
            for deck in raw.strip().split('\n\n')]


def part_one(decks: Decks) -> int:
    """Play game with small crab and return the winner score."""
    p1, p2 = decks[0][:], decks[1][:]
    while p1 and p2:
        play = p1.pop(0), p2.pop(0)
        if play[0] > play[1]:
            p1.extend(play)
        else:
            p2.extend(play[::-1])
    return sum(card * i for i, card in enumerate(reversed(p2 or p1), start=1))


def part_two(decks: Decks) -> int:
    """Play recursive game with small crab and return the winner score."""
    final_decks, win_1 = recursive_combat([deck[:] for deck in decks[:]])
    winner_deck = reversed(final_decks[0] if win_1 else final_decks[1])
    return sum(card * i for i, card in enumerate(winner_deck, start=1))


def recursive_combat(decks: Decks) -> Tuple[Decks, bool]:
    """Recursive battle, if there is a tie then start a new fight."""
    memorised = set()
    p1, p2 = decks[0], decks[1]
    while p1 and p2:
        tuple_players = (tuple(p1), tuple(p2))
        if tuple_players in memorised:
            return decks, True
        else:
            memorised.add(tuple_players)
        play = p1.pop(0), p2.pop(0)
        if len(p1) >= play[0] and len(p2) >= play[1]:
            decks_combat = [p1[:play[0]], p2[:play[1]]]
            _, win_1 = recursive_combat(decks_combat)
            if win_1:
                p1.extend(play)
            else:
                p2.extend(play[::-1])
        elif play[0] > play[1]:
            p1.extend(play)
        else:
            p2.extend(play[::-1])
    return decks, bool(p1)


if __name__ == "__main__":
    print("--- Day 22: Crab Combat ---")
    puzzle = parse(get_data(day=22, year=2020))
    print("Part One:", part_one(puzzle))
    print("Part Two:", part_two(puzzle))
