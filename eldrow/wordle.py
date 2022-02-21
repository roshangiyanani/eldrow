from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Mapping, Optional, Sequence, Set


class CharResult(Enum):
    Gray = "X"
    Yellow = "Y"
    Green = "G"

    @staticmethod
    def to_string(results: Sequence["CharResult"]) -> str:
        return "".join((r.value for r in results))


@dataclass()
class Constraint:
    min_count: int
    min_is_exact: bool
    known_positions: Set[int]


class Wordle:
    def __init__(self, word: str, hard_mode: Optional[bool] = False):
        if not word:
            raise ValueError("cannot have empty word")

        self._hard_mode = hard_mode
        self._word = word.casefold()
        self._char_counts = Counter(self._word)
        self._constraints: Dict[str, Constraint] = dict()

    def make_guess(self, guess: str) -> List[CharResult]:
        if not guess:
            raise ValueError("cannot have an empty guess")

        guess = guess.casefold()
        if len(guess) != len(self._word):
            raise ValueError("guess does not match word length")

        guess_char_counts = Counter(guess)
        if self._hard_mode and not self._is_valid_hard_mode_guess(
            guess, guess_char_counts
        ):
            raise ValueError("invalid hard mode guess")

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

        self._update_constraints(guess, guess_char_counts, result)

        return result

    def _update_constraints(
        self,
        guess: str,
        guess_char_counts: Counter,
        result: Sequence[CharResult],
    ):
        char_indexes: Dict[str, Set[int]] = defaultdict(set)
        for index, char in enumerate(guess):
            char_indexes[char].add(index)

        for char, indexes in char_indexes.items():
            constraint = self._constraints.get(char)
            char_results = Counter(result[index] for index in indexes)

            min_count = char_results[CharResult.Green] + char_results[CharResult.Yellow]
            min_is_exact = bool(char_results[CharResult.Gray])
            known_positions = (
                index for index in indexes if result[index] == CharResult.Green
            )

            if constraint:
                if min_count > constraint.min_count:
                    assert not min_is_exact
                    constraint.min_count = min_count
                    constraint.min_is_exact = min_is_exact
                elif min_count == constraint.min_count:
                    constraint.min_is_exact = min_is_exact or constraint.min_is_exact
                else:
                    assert not min_is_exact

                for known_position in known_positions:
                    constraint.known_positions.add(known_position)
            else:
                constraint = Constraint(min_count, min_is_exact, set(known_positions))
                self._constraints[char] = constraint

    def is_valid_hard_mode_guess(self, guess: str) -> bool:
        if not guess:
            raise ValueError("cannot have an empty guess")

        guess = guess.casefold()
        if len(guess) != len(self._word):
            raise ValueError("guess does not match word length")

        character_counts = Counter(guess)
        return self._is_valid_hard_mode_guess(guess, character_counts)

    def _is_valid_hard_mode_guess(self, guess: str, char_counts: Counter) -> bool:
        for char, constraint in self._constraints.items():
            count = char_counts[char]
            wrong_count = (
                count != constraint.min_count
                if constraint.min_is_exact
                else count < constraint.min_count
            )
            missing_known_positions = any(
                self._word[index] != guess[index]
                for index in constraint.known_positions
            )
            if wrong_count or missing_known_positions:
                return False

        return True
