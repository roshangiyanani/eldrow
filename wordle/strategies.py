__all__ = [
    "execute_strategy",
    "exhaustive_guess",
    "legal_hard_mode_guess",
]

from collections import defaultdict, Counter
from logging import getLogger
import random
from typing import Sequence, Collection, Generator, Dict, Set

from wordle.lib import colored_text
from wordle.wordle import CharResult, Wordle, Constraint

logger = getLogger(__name__)


Strategy = Generator[str, Sequence[CharResult], None]


def execute_strategy(wordle: Wordle, strat: Strategy) -> int:
    count = 1
    guess = next(strat)
    result = wordle.make_guess(guess)
    while not CharResult.all_correct(result):
        logger.debug("guess %d: %s", count, colored_text(guess, result))

        count += 1
        guess = strat.send(result)
        result = wordle.make_guess(guess)

    return count


def exhaustive_guess(possibilities: Collection[str]) -> Strategy:
    possibilities = list(possibilities)
    random.shuffle(possibilities)
    for possibility in possibilities:
        result = yield possibility
        assert not CharResult.all_correct(result)


class _HardModeConstraintTracker:
    def __init__(self):
        self.constraints: Dict[str, Constraint] = dict()

    def update(self, guess: str, result: Sequence[CharResult]) -> None:
        char_indexes: Dict[str, Set[int]] = defaultdict(set)
        for index, char in enumerate(guess):
            char_indexes[char].add(index)

        for char, indexes in char_indexes.items():
            old_constraint = self.constraints.get(char)
            new_constraint = Constraint.from_result(indexes, result)

            if old_constraint:
                old_constraint.update(new_constraint)
            else:
                self.constraints[char] = new_constraint

    def is_legal(self, guess: str) -> bool:
        char_counts = Counter(guess)
        for char, constraint in self.constraints.items():
            count = char_counts[char]
            wrong_count = (
                count != constraint.min_count
                if constraint.min_is_exact
                else count < constraint.min_count
            )
            missing_known_positions = any(
                guess[index] != char for index in constraint.known_positions
            )
            if wrong_count or missing_known_positions:
                return False

        return True


def legal_hard_mode_guess(possibilities: Collection[str]) -> Strategy:
    possibilities = list(possibilities)
    constraint_tracker = _HardModeConstraintTracker()

    guess = random.choice(possibilities)
    result = yield guess
    while not CharResult.all_correct(result):
        constraint_tracker.update(guess, result)
        possibilities = [
            possibility
            for possibility in possibilities
            if constraint_tracker.is_legal(possibility)
        ]
        logger.debug("filtered to %d possibilities", len(possibilities))
        assert possibilities

        guess = random.choice(possibilities)
        result = yield guess
