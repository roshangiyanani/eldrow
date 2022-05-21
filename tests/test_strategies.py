from random import choice

from eldrow.wordle import Wordle
from eldrow.strategies import execute_strategy, exhaustive_guess

vocabulary = ["ALPHA", "OMEGA", "TROPE", "MOVIE", "CROWD", "FROZE", "OZONE", "HEELS"]
word = choice(vocabulary)


def test_exhaustive_guess_strategy():
    strat = exhaustive_guess(vocabulary)
    wordle = Wordle(word)
    execute_strategy(wordle, strat)
