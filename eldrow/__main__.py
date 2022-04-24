import logging
from pathlib import Path
import random

from eldrow.lib import colored_text, load_words
from eldrow.wordle import CharResult, Wordle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

word_path = Path("./wordlist.csv")
words = load_words(word_path)
logging.info(f"loaded {len(words)} words from {word_path}")

random_word = random.choice(words)
logging.info(f'randomly chose: "{random_word}"')
wordle = Wordle(random_word)
consideration_set = set(words)

count = 0
for word in consideration_set:
    count += 1
    result = wordle.make_guess(word)
    print(f"({count}) {colored_text(word, result)}")
    if all(cr == CharResult.Green for cr in result):
        break
