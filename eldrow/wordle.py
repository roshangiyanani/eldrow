from collections import Counter
from enum import Enum
from typing import List, Sequence


class CharResult(Enum):
    Gray = "X"
    Yellow = "Y"
    Green = "G"

    @staticmethod
    def to_string(results: Sequence["CharResult"]) -> str:
        return "".join((r.value for r in results))


class Wordle:
    def __init__(self, word: str):
        if not word:
            raise ValueError("cannot have empty word")

        self._word = word.casefold()
        self._character_counts = Counter(self._word)

    def make_guess(self, guess: str) -> List[CharResult]:
        if not guess:
            raise ValueError("cannot have an empty guess")

        guess = guess.casefold()

        if len(guess) != len(self._word):
            raise ValueError("guess does not match word length")

        result = [CharResult.Gray for _ in range(len(self._word))]

        guess_character_counts = Counter(guess)
        overlap = self._character_counts & guess_character_counts

        for index, (correct, guessed) in enumerate(zip(self._word, guess)):
            if correct == guessed:
                result[index] = CharResult.Green
                overlap[correct] -= 1

        for index, (correct, guessed) in enumerate(zip(self._word, guess)):
            if result[index] is not CharResult.Green and overlap.get(guessed):
                result[index] = CharResult.Yellow
                overlap[guessed] -= 1

        return result
