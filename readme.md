# Eldrow

## Wordle
The daily puzzle game Wordle has taken the world by storm! Wordlers try to track down the mystery five-letter word in as few guesses as possible each day, with each guess returning the information of whether its letters are:

- in the exact position they appear in the mystery word (these letters turn green),
- in the mystery word but NOT in the position guessed and NOT already accounted for by green or yellow letters, counting duplicity (these letters turn yellow), or
- not in the mystery word at all (these letters turn gray).

The marking happens in this specific order. First all correctly placed letters are marked green. Then of the remaining letters, from left to right, all letters that exist in the mystery word but haven’t been accounted for by greens or yellows so far are marked yellow. The remaining letters are marked gray. If the mystery word is ROVER, the guess of ERROR would be marked

ERROR

## Hard Mode

When operating in hard-mode, every subsequent guess has to satisfy all clues left by previous guesses, i.e., each guess has to have a possibility of being the mystery word conditional on the responses of all previous guesses1. For example, if TIGER is the mystery word, and a player’s first guess is TRACK, it would be colored

TRACK

and any future guess couldn’t be

- DIRTY, because the mystery word starts with T
- TROMP, because the mystery word’s second letter isn’t R
- TARDY, because the mystery word doesn’t contain an A
- TEPID, because the mystery word must contain an R.
- There are many other disqualified future guesses, but TOWER for example would be allowed.

## Eldrow Rules
We are playing Eldrow, the game of searching for the longest possible chain of hard-mode guesses (we ignore the limit of 6 guesses in Wordle). Choose the target word and sequence of hard-mode guesses from this [list](wordlist.csv) (SPOILER ALERT: this is an alphabetized copy of the list of Wordle mystery words, found from inspection of the website’s source code).

__What is the longest hard-mode guess sequence you can find?__ Submit your answer as a comma-separated list of words from the list linked above, in the order guessed, with the final word being the chosen target word. For example, “TRACK,TOWER,TIGER” would be a somewhat underwhelming submission (and “TRACK,TROMP,TIGER” would not qualify). We will keep a leaderboard of the longest qualifying submissions on this page!

1. In the actual Wordle game, this isn’t precisely true. The exact requirement is that, in every future guess, all green letters discovered so far appear in the position discovered and all yellow letters discovered so far continue to appear in future guesses. So in the example above with TIGER as the mystery word, the sequence:  
TRACK  
TROMP  
is allowed, even though the player knows that the R can’t be in the second position after the first guess because it would’ve been colored green in the first row. We will use our definition of hard-mode: every guess has to be a potential winner given all the information gathered so far (so by the above logic this sequence would NOT be allowed). ↩
1. If you’d prefer to solve by hand without testing each word against this list, your can still submit but your leaderboard entry may have an asterisk. ↩
1. Note there is a fairly straightforward proof that an (unachievable) upper bound on the length of an Eldrow sequence is 26 words. If your process is generating longer sequences, please recheck the rules. ↩