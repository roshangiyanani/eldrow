from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
)


class CharResult(Enum):
    Gray = "X"
    Yellow = "Y"
    Green = "G"

    @staticmethod
    def to_string(results: Iterator[CharResult]) -> str:
        return "".join((r.value for r in results))

    @staticmethod
    def all_correct(results: Iterator[CharResult]) -> bool:
        return all(cr == CharResult.Green for cr in results)


@dataclass()
class Constraint:
    min_count: int
    min_is_exact: bool
    known_positions: Set[int]

    def update(self, u: Constraint):
        if u.min_count > self.min_count:
            assert not self.min_is_exact
            self.min_count = u.min_count
            self.min_is_exact = u.min_is_exact
        elif u.min_count == self.min_count:
            self.min_is_exact = self.min_is_exact or u.min_is_exact
        else:
            assert not u.min_is_exact

        self.known_positions.update(u.known_positions)

    @staticmethod
    def from_result(indexes: Iterable[int], result: Sequence[CharResult]) -> Constraint:
        char_results = Counter(result[index] for index in indexes)

        min_count = char_results[CharResult.Green] + char_results[CharResult.Yellow]
        min_is_exact = bool(char_results[CharResult.Gray])
        known_positions = {
            index for index in indexes if result[index] == CharResult.Green
        }

        return Constraint(
            min_count=min_count,
            min_is_exact=min_is_exact,
            known_positions=known_positions,
        )


@cache
def counter(word: str) -> Counter[str]:
    return Counter(word)


class Wordle:
    def __init__(self, word: str, hard_mode: Optional[bool] = False):
        if not word:
            raise ValueError("cannot have empty word")

        self._hard_mode = bool(hard_mode)
        self._word = word
        self._char_counts = counter(word)
        self._constraints: Dict[str, Constraint] = dict()

    def is_legal(self, guess: str) -> bool:
        char_counts = counter(guess)
        if len(guess) != len(self._word):
            return False

        if self._hard_mode:
            for char, constraint in self._constraints.items():
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

    def make_guess(self, guess: str) -> List[CharResult]:
        if not guess:
            raise ValueError("cannot guess empty word")

        guess_char_counts = counter(guess)
        self._verify_is_legal(guess, guess_char_counts)

        result = [CharResult.Gray for _ in range(len(self._word))]
        overlap = self._char_counts & guess_char_counts

        for index, (correct, guessed) in enumerate(zip(self._word, guess)):
            if correct == guessed:
                result[index] = CharResult.Green
                overlap[correct] -= 1

        for index, (correct, guessed) in enumerate(zip(self._word, guess)):
            if result[index] is not CharResult.Green and overlap[guessed]:
                result[index] = CharResult.Yellow
                overlap[guessed] -= 1

        self._update_constraints(guess, result)
        return result

    def _update_constraints(self, guess: str, result: Sequence[CharResult]) -> None:
        char_indexes: Dict[str, Set[int]] = defaultdict(set)
        for index, char in enumerate(guess):
            char_indexes[char].add(index)

        for char, indexes in char_indexes.items():
            old_constraint = self._constraints.get(char)
            new_constraint = Constraint.from_result(indexes, result)

            if old_constraint:
                old_constraint.update(new_constraint)
            else:
                self._constraints[char] = new_constraint

    def _verify_is_legal(self, guess: str, char_counts: Counter[str]) -> None:
        if not guess:
            raise ValueError("cannot have an empty guess")

        if len(guess) != len(self._word):
            raise ValueError(
                f"guess ({guess}) does not match word length ({len(self._word)})"
            )

        if self._hard_mode:
            for char, constraint in self._constraints.items():
                count = char_counts[char]
                if constraint.min_is_exact and count != constraint.min_count:
                    raise ValueError(f"count of '{char}' in '{guess}' ({count}) does not match known count ({constraint.min_count})")
                elif count < constraint.min_count:
                    raise ValueError(f"count of '{char}' in '{guess}' ({count}) does not meet minimum count ({constraint.min_count})")

                for index in constraint.known_positions:
                    if guess[index] != char:
                        raise ValueError(f"char {index} ('{guess[index]}') in '{guess}' does not match known char '{char}'")
