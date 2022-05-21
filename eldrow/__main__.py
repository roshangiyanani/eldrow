import logging
import random
from pathlib import Path

from eldrow.lib import load_words
from eldrow.wordle import Wordle
from eldrow.strategies import execute_strategy, exhaustive_guess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

word_path = Path("./wordlist.csv")
words = load_words(word_path)
logging.info(f"loaded {len(words)} words from {word_path}")

random_word = random.choice(words)
logging.info(f'randomly chose: "{random_word}"')
wordle = Wordle(random_word)

strat = exhaustive_guess(words)
execute_strategy(wordle, strat)
