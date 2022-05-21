from logging import getLogger
import random
from typing import Sequence, Collection, Generator

from eldrow.lib import colored_text
from eldrow.wordle import CharResult, Wordle

logger = getLogger(__name__)


Strategy = Generator[str, Sequence[CharResult], None]


def execute_strategy(wordle: Wordle, strat: Strategy) -> int:
    count = 1
    guess = next(strat)
    result = wordle.make_guess(guess)
    while not CharResult.all_correct(result):
        logger.debug("guess %d: %s", count, colored_text(guess, result))

        count += 1
        guess = strat.send(result)
        result = wordle.make_guess(guess)

    logger.info("%s found in %d guesses", guess, count)
    return count


def exhaustive_guess(
    possibilities: Collection[str],
) -> Generator[str, Sequence[CharResult], None]:
    possibilities = list(possibilities)
    random.shuffle(possibilities)
    for possibility in possibilities:
        result = yield possibility
        assert not CharResult.all_correct(result)
