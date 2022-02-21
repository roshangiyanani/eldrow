from pathlib import Path
from eldrow.__lib__ import load_words

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

word_path = Path("./wordlist.csv")
words = load_words(word_path)
logging.info(f"loaded {len(words)} words from {word_path}")
