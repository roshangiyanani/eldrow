from argparse import ArgumentParser
from datetime import timedelta
import logging
from multiprocessing import Pool
from pathlib import Path
from time import perf_counter_ns
from typing import Set, List, Mapping, Dict, Optional, Tuple

from wordle.wordle import Wordle, CharResult
from wordle.lib import colored_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("wordlist", type=Path, help="wordlist file")
    parser.add_argument("-l", "--limit", type=int, help="limit wordlist to l possibilities (randomly selected)")
    parser.add_argument("-n", "--number", type=int, help="only solve n words")
    parser.add_argument("-s", "--seed", type=int, help="random number generator seed (useful when limiting)")
    parser.add_argument("-p", "--processes", type=int, help="run across p processes")
    return parser

def worst_solve(wordle: Wordle, possibilities: Set[str], filters: Optional[Mapping[str, Set[str]]] = None) -> List[str]:
    assert len(possibilities) != 0
    if len(possibilities) == 1:
        word = next(iter(possibilities))
        assert CharResult.all_correct(wordle.make_guess(word))
        return [word]

    modifieds: List[Tuple[str, Wordle, Set[str]]] = list()
    sub_filters: Dict[str, Set[str]] = dict()
    for possibility in possibilities:
        modified_wordle, result = wordle.copy_make_guess(possibility)
        if CharResult.all_correct(result):
            modified_possibilities = {}
        else:
            if filters is not None:
                filter = filters[possibility]
                modified_possibilities = {word for word in possibilities if word in filter and modified_wordle.is_legal(word)}
            else:
                modified_possibilities = {word for word in possibilities if modified_wordle.is_legal(word)}
            modifieds.append((possibility, modified_wordle, modified_possibilities))
        sub_filters[possibility] = modified_possibilities

    modifieds.sort(key=lambda m: len(m[2]), reverse=True)
    worst_guesses: List[str] = list()
    for word, m_wordle, m_possibilities in modifieds:
        if len(m_possibilities) + 1 <= len(worst_guesses):
            # this can only match the worst solve, since there's not enough words to try
            continue

        solve = worst_solve(m_wordle, m_possibilities, sub_filters)
        if len(worst_guesses) < len(solve) + 1:
            solve.append(word)
            worst_guesses = solve

    return worst_guesses


def run_worst_solve(words: Set[str], word: str) -> List[str]:
    wordle = Wordle(word, True)

    start = perf_counter_ns()
    ws = worst_solve(wordle, words)
    end = perf_counter_ns()
    elapsed = timedelta(microseconds=(end - start) / 1000)

    colored_ws = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(ws))
    logger.info("calculated worst solve for word %s (%d guesses) in %s: %s", word, len(ws), elapsed, colored_ws)
    return ws


if __name__ == "__main__":
    import random

    from wordle.lib import load_words

    parser = build_arg_parser()
    args = parser.parse_args()
    word_path: Path = args.wordlist
    limit: Optional[int] = args.limit
    number: Optional[int] = args.number
    seed: Optional[int] = args.seed
    processes: Optional[int] = args.processes

    words = load_words(word_path)
    logger.info(f"loaded {len(words)} words from {word_path}")

    if seed is not None:
        random.seed(seed)
        logger.info(f"set seed to %d", seed)

    if limit is not None:
        possibilities = random.sample(words, limit)
        logger.info("randomly sampled %d possibilities", limit)
    else:
        possibilities = words

    if number is not None:
        words_to_solve = random.sample(possibilities, number)
        logger.info("randomly sampled %d words to solve", number)
    else:
        words_to_solve = possibilities

    possibilities = set(possibilities)
    g_start = perf_counter_ns()

    if not processes or processes == 1:
        results = list()
        for word in words_to_solve:
            result = run_worst_solve(possibilities, word)
            results.append(result)
    else:
        logger.info("running across %d processes", processes)
        with Pool(processes=processes) as pool:
            results = pool.starmap(run_worst_solve, [(possibilities, word) for word in words_to_solve])

    g_end = perf_counter_ns()
    g_elapsed = timedelta(microseconds=(g_end-g_start) / 1000)

    worst_guesses = max(results, key=len)
    worst_word = worst_guesses[0]

    wordle = Wordle(worst_word, hard_mode=True)
    colored_worst_guesses = ", ".join(colored_text(w, wordle.make_guess(w)) for w in reversed(worst_guesses))
    logger.info(
        "calculated global (n=%d, l=%d) worst solve for word %s (%d guesses) in %s:\n%s",
        number,
        limit,
        worst_word,
        len(worst_guesses),
        g_elapsed,
        colored_worst_guesses
    )
