import logging
from copy import deepcopy
from pathlib import Path
from typing import Set, List

from wordle.wordle import Wordle, CharResult


def worst_solve(wordle: Wordle, possibilities: Set[str]) -> List[str]:
    assert len(possibilities) != 0
    if len(possibilities) == 1:
        word = next(iter(possibilities))
        assert CharResult.all_correct(wordle.make_guess(word))
        return [word]

    worst_guesses: List[str] = list()
    for possibility in possibilities:
        modified_wordle = deepcopy(wordle)
        result = modified_wordle.make_guess(possibility)
        if CharResult.all_correct(result):
            # this can't be the worst solve, since there's at least one other word to try first
            continue

        modified_possibilities = {word for word in possibilities if modified_wordle.is_legal(word)}
        if len(modified_possibilities) + 1 <= len(worst_guesses):
            # this can only match the worst solve, since there's not enough words to try
            continue

        solve = worst_solve(modified_wordle, modified_possibilities)
        if len(worst_guesses) < len(solve) + 1:
            solve.append(possibility)
            worst_guesses = solve

    return worst_guesses


if __name__ == "__main__":
    from wordle.lib import load_words, colored_text
    from datetime import timedelta
    import random
    from time import perf_counter_ns

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    word_path = Path("./wordlist.csv")
    words = load_words(word_path)
    random.seed(9)
    words = random.sample(words, 100)
    logging.info(f"loaded {len(words)} words from {word_path}")

    g_start = perf_counter_ns()
    worst_word = None
    worst_guesses = []
    for word in words:
        wordle = Wordle(word, True)

        start = perf_counter_ns()
        ws = worst_solve(wordle, set(words))
        end = perf_counter_ns()
        elapsed = timedelta(microseconds=(end - start) / 1000)

        colored_ws = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(ws))
        logger.info("calculated worst solve for word %s (%d guesses) in %s: %s", word, len(ws), elapsed, colored_ws)

        if len(worst_guesses) < len(ws):
            worst_word = word
            worst_guesses = ws

    g_end = perf_counter_ns()
    g_elapsed = timedelta(microseconds=(g_end-g_start) / 1000)

    wordle = Wordle(worst_word, hard_mode=True)
    colored_worst_guesses = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(worst_guesses))
    logger.info("calculated global worst solve for word %s (%d guesses) in %s: %s", worst_word, len(worst_guesses), g_elapsed, colored_worst_guesses)
