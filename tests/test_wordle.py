from eldrow.wordle import Wordle, CharacterResult


def test_correct():
    w = Wordle("ABATE")

    result = w.make_guess("abate")
    assert all(map(lambda r: r == CharacterResult.Green, result))

    result = w.make_guess("ABATE")
    assert all(map(lambda r: r == CharacterResult.Green, result))

    result = w.make_guess("AbAtE")
    assert all(map(lambda r: r == CharacterResult.Green, result))


def test_incorrect():
    w = Wordle("ABATE")

    result = w.make_guess("FLOWN")
    assert all(map(lambda r: r == CharacterResult.Gray, result))


def test_greens():
    w = Wordle("ABATE")

    result = w.make_guess("FLAKE")
    assert CharacterResult.to_string(result) == "XXGXG"

    result = w.make_guess("ABACK")
    assert CharacterResult.to_string(result) == "GGGXX"

    result = w.make_guess("ABASE")
    assert CharacterResult.to_string(result) == "GGGXG"

    result = w.make_guess("ELATE")
    assert CharacterResult.to_string(result) == "XXGGG"


def test_yellows():
    w = Wordle("ABATE")

    result = w.make_guess("LATER")
    assert CharacterResult.to_string(result) == "XYYYX"

    result = w.make_guess("METER")
    assert CharacterResult.to_string(result) == "XYYXX"


def test_greens_and_yellows():
    w = Wordle("ABATE")

    result = w.make_guess("ABBEY")
    assert CharacterResult.to_string(result) == "GGXYX"

    result = w.make_guess("AGORA")
    assert CharacterResult.to_string(result) == "GXXXY"
