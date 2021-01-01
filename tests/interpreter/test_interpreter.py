from computation.interpreter.interpreter import Machine
from computation.interpreter.parser import parse
from computation.interpreter.statements import DoNothing


def check_source(source: str, expected_env: dict, debug: bool = False):
    seq = parse(source)
    env = Machine(seq, debug=debug).run().environment

    for k, v in env.items():
        env[k] = v.value
    assert env == expected_env
    assert eval(seq.to_python)({}) == expected_env

    return seq


def test_interpreter():
    seq = parse(" ")
    assert seq == DoNothing()
    check_source(" ", {})

    source = """
        x = 5
        x = x + 1
    """
    check_source(source, {"x": 6})

    source = """
        x = 1 + 1
        y = x * 2
    """
    check_source(source, {"x": 2, "y": 4})

    source = """
        x = 1 + 1
        y = x * 1
    """
    check_source(source, {"x": 2, "y": 2})

    source = """
        x = 5
        x = 1 + x * 2
    """
    check_source(source, {"x": 11})

    source = """
        x = 5
        x = (1 + x) * 2
    """
    check_source(source, {"x": 12})

    source = """
        x = 1
        while (x < 50) {
            x = x + 3
        }
    """
    check_source(source, {"x": 52})

    source = """
        a = 1
        b = 1
        c = 0
        d = 0
        if (a < 2 && b < 2) {
            a = a + 1
            c = a
        } else {
            d = b
        }
        if (a + 1 < 1 * 3) {
            b = b + 1
        } else {
            d = d + 1
        }
        if (b == 1 || a < 2) {
            b = b + 1
        }
    """
    check_source(source, {"a": 2, "b": 2, "c": 2, "d": 1})

    source = """
        a = 1
        b = 1
        if (a < 0 + 2 && b < 2) {
            a = a + 1
        } else {
            b = b + 1
        }
        if (a < 2 || b < 1) {
            b = b + 1
        }
    """
    check_source(source, {"a": 2, "b": 1})

    source = """
        a = 0
        b = 0
        while (a < 5) {
            a = a + 1
            b = b + a + 1
        }
    """
    check_source(source, {"a": 5, "b": 20})
