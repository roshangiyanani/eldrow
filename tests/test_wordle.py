from eldrow.wordle import Wordle, CharResult


def test_correct():
    w = Wordle("ABATE")

    result = w.make_guess("abate")
    assert all(map(lambda r: r == CharResult.Green, result))

    result = w.make_guess("ABATE")
    assert all(map(lambda r: r == CharResult.Green, result))

    result = w.make_guess("AbAtE")
    assert all(map(lambda r: r == CharResult.Green, result))


def test_incorrect():
    w = Wordle("ABATE")

    result = w.make_guess("FLOWN")
    assert all(map(lambda r: r == CharResult.Gray, result))


def test_greens():
    w = Wordle("ABATE")

    result = w.make_guess("FLAKE")
    assert CharResult.to_string(result) == "XXGXG"

    result = w.make_guess("ABACK")
    assert CharResult.to_string(result) == "GGGXX"

    result = w.make_guess("ABASE")
    assert CharResult.to_string(result) == "GGGXG"

    result = w.make_guess("ELATE")
    assert CharResult.to_string(result) == "XXGGG"


def test_yellows():
    w = Wordle("ABATE")

    result = w.make_guess("LATER")
    assert CharResult.to_string(result) == "XYYYX"

    result = w.make_guess("METER")
    assert CharResult.to_string(result) == "XYYXX"


def test_greens_and_yellows():
    w = Wordle("ABATE")

    result = w.make_guess("ABBEY")
    assert CharResult.to_string(result) == "GGXYX"

    result = w.make_guess("AGORA")
    assert CharResult.to_string(result) == "GXXXY"


def test_hard_mode():
    w = Wordle("ABATE", True)

    assert CharResult.to_string(w.make_guess("ABBEY")) == "GGXYX"
    assert not w.is_valid_hard_mode_guess("AGORA")
    assert not w.is_valid_hard_mode_guess("ABACK")
    assert all(r == CharResult.Green for r in w.make_guess("ABATE"))
