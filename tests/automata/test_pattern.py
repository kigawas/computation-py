from computation.automata.pattern import Choose, Concatenate, Empty, Literal, Repeat


def test_pattern():
    pattern = Repeat(Choose(Concatenate(Literal("a"), Literal("b")), Literal("a")))
    assert repr(pattern) == "/(ab|a)*/"
    assert str(pattern) == "(ab|a)*"

    assert not (Empty().matches("a"))
    assert Literal("a").matches("a")

    pattern = Repeat(Concatenate(Literal("a"), Choose(Empty(), Literal("b"))))
    assert repr(pattern) == "/(a(|b))*/"
    assert pattern.matches("")
    assert pattern.matches("a")
    assert pattern.matches("ab")
    assert pattern.matches("aba")
    assert pattern.matches("abab")
    assert pattern.matches("abaab")
    assert not (pattern.matches("bbba"))


def test_nfa_design():
    nfa_d = Empty().to_nfa_design
    assert nfa_d.accepts("")
    assert not (nfa_d.accepts("a"))

    nfa_d = Literal("a").to_nfa_design
    assert not (nfa_d.accepts(""))
    assert nfa_d.accepts("a")
    assert not (nfa_d.accepts("b"))

    pattern = Concatenate(Literal("a"), Literal("b"))
    assert pattern.matches("ab")
    assert not (pattern.matches("a"))
    assert not (pattern.matches("b"))
    assert not (pattern.matches("abc"))

    pattern = Concatenate(Literal("a"), Concatenate(Literal("b"), Literal("c")))
    assert pattern.matches("abc")
    assert not (pattern.matches("a"))
    assert not (pattern.matches("b"))
    assert not (pattern.matches("ab"))

    pattern = Choose(Literal("a"), Literal("b"))
    assert pattern.matches("a")
    assert pattern.matches("b")
    assert not (pattern.matches("c"))

    pattern = Repeat(Literal("a"))
    assert pattern.matches("")
    assert pattern.matches("a")
    assert pattern.matches("aa")
    assert pattern.matches("aaaaaaaaaa")
    assert not (pattern.matches("b"))
