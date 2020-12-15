from computation.interpreter.interpreter import Machine
from computation.interpreter.statements import DoNothing
from computation.interpreter.parser import parse


def check_source(source: str, expected_env: dict, debug: bool = False):
    seq = parse(source)
    env = Machine(seq, debug=debug).run().environment
    for k, v in env.items():
        env[k] = v.value
    assert env == expected_env
    assert eval(seq.to_python)({}) == expected_env


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
    x = 1
    while (x < 50) {
        x = x + 3
    }
    """

    check_source(source, {"x": 52})

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
