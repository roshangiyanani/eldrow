from datetime import timedelta
import logging
from multiprocessing import Pool
from pathlib import Path
from time import perf_counter_ns
from typing import Set, List, Mapping, Dict

from wordle.wordle import Wordle, CharResult
from wordle.lib import colored_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def worst_solve(wordle: Wordle, possibilities: Set[str], filters: Mapping[str, Set[str]]) -> List[str]:
    assert len(possibilities) != 0
    if len(possibilities) == 1:
        word = next(iter(possibilities))
        assert CharResult.all_correct(wordle.make_guess(word))
        return [word]

    worst_guesses: List[str] = list()
    for possibility in possibilities:
        modified_wordle, result = wordle.copy_make_guess(possibility)
        if CharResult.all_correct(result):
            # this can't be the worst solve, since there's at least one other word to try first
            continue

        filter = filters[possibility]
        modified_possibilities = {word for word in possibilities if word in filter and modified_wordle.is_legal(word)}
        if len(modified_possibilities) + 1 <= len(worst_guesses):
            # this can only match the worst solve, since there's not enough words to try
            continue

        solve = worst_solve(modified_wordle, modified_possibilities, filters)
        if len(worst_guesses) < len(solve) + 1:
            solve.append(possibility)
            worst_guesses = solve

    return worst_guesses


def run_worst_solve(words: Set[str], word: str) -> List[str]:
    wordle = Wordle(word, True)

    start = perf_counter_ns()
    filters: Dict[str, Set[str]] = dict()
    for word in words:
        modified_wordle, _ = wordle.copy_make_guess(word)
        filters[word] = {w for w in words if modified_wordle.is_legal(w)}
    end = perf_counter_ns()
    elapsed = timedelta(microseconds=(end - start) / 1000)
    logger.debug("built filter for word %s in %s", word, elapsed)

    start = perf_counter_ns()
    ws = worst_solve(wordle, words, filters)
    end = perf_counter_ns()
    elapsed = timedelta(microseconds=(end - start) / 1000)

    colored_ws = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(ws))
    logger.info("calculated worst solve for word %s (%d guesses) in %s: %s", word, len(ws), elapsed, colored_ws)
    return ws


if __name__ == "__main__":
    import random

    from wordle.lib import load_words


    word_path = Path("./wordlist.csv")
    words = load_words(word_path)
    random.seed(9)
    words = set(random.sample(words, 200))
    logging.info(f"loaded {len(words)} words from {word_path}")

    g_start = perf_counter_ns()

    with Pool(processes=4) as pool:
        results = pool.starmap(run_worst_solve, [(words, w) for w in words])

    g_end = perf_counter_ns()
    g_elapsed = timedelta(microseconds=(g_end-g_start) / 1000)

    worst_guesses = max(results, key=len)
    worst_word = worst_guesses[0]

    wordle = Wordle(worst_word, hard_mode=True)
    colored_worst_guesses = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(worst_guesses))
    logger.info("calculated global worst solve for word %s (%d guesses) in %s: %s", worst_word, len(worst_guesses), g_elapsed, colored_worst_guesses)
