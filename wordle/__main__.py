from datetime import timedelta
import logging
from pathlib import Path
import random
from time import perf_counter_ns

from wordle.lib import load_words
from wordle.wordle import Wordle
from wordle.strategies import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

word_path = Path("./wordlist.csv")
words = load_words(word_path)
logging.info(f"loaded {len(words)} words from {word_path}")

random_word = random.choice(words)
logging.info(f'randomly chose: "{random_word}"')

strategies = {
    "exhaustive_guess": exhaustive_guess(words),
    "legal_hard_mode_guess": legal_hard_mode_guess(words),
}

for name, strat in strategies.items():
    wordle = Wordle(random_word)
    start = perf_counter_ns()
    count = execute_strategy(wordle, strat)
    end = perf_counter_ns()
    elapsed = timedelta(microseconds=(end - start) / 1000)
    logger.info("strategy '%s' took '%d' guesses and %s", name, count, elapsed)
