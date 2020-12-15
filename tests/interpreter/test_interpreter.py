from computation.interpreter.interpreter import Machine
from computation.interpreter.expressions import (
    Add,
    Variable,
    Number,
    Multiply,
    LessThan,
)
from computation.interpreter.statements import DoNothing, Sequence, Assign, While
from computation.interpreter.parser import parse


def test_interpreter():
    SEP = "=" * 50
    seq = Assign("x", Add(Variable("x"), Number(1)))
    Machine(seq, {"x": Number(5)}, True).run()

    print(SEP)

    seq = Sequence(
        Assign("x", Add(Number(1), Number(1))),
        Assign("y", Multiply(Variable("x"), Number(2))),
    )
    Machine(seq, {}, True).run()

    print(SEP)

    seq = Sequence(
        Assign("x", Add(Number(1), Number(1))),
        Assign("y", Add(Variable("x"), Number(1))),
    )
    Machine(seq, {}, True).run()

    print(SEP)

    seq = While(
        LessThan(Variable("x"), Number(50)),
        Assign("x", Add(Variable("x"), Number(3))),
    )
    Machine(seq, {"x": Number(1)}).run()

    assert eval(seq.to_python)({"x": 1}) == {"x": 52}

    source = """
        a = 0
        b = 0
        while (a < 5) {
            a = a + 1
            b = b + a + 1
        }
    """
    seq = parse(source)
    assert Machine(seq).run().environment, {"a": Number(5), "b": Number(20)}
    assert eval(seq.to_python)({}), {"a": 5, "b": 20}

    seq = parse(" ")
    assert seq == DoNothing()
