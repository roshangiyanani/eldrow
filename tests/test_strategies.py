from random import choice

from wordle.wordle import Wordle
from wordle.strategies import *

vocabulary = ["ALPHA", "OMEGA", "TROPE", "MOVIE", "CROWD", "FROZE", "OZONE", "HEELS"]
word = choice(vocabulary)


def test_exhaustive_guess():
    strat = exhaustive_guess(vocabulary)
    wordle = Wordle(word)
    execute_strategy(wordle, strat)


def test_legal_hard_mode_guess():
    strat = legal_hard_mode_guess(vocabulary)
    wordle = Wordle(word)
    execute_strategy(wordle, strat)
