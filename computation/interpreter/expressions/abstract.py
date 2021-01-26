import operator
from typing import Any

OP_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "<": operator.lt,
    "and": operator.and_,
    "or": operator.or_,
    "==": operator.eq,
}


class Expression:
    @property
    def reducible(self):
        raise NotImplementedError

    @property
    def to_python(self):
        """
        Python lambda code generator
        """
        raise NotImplementedError

    def evaluate(self, _environment: dict):
        """
        Evaluate everything in a "recursive descent" way
        """
        raise NotImplementedError

    def reduce(self, _environment: dict):
        """
        Reduce step by step
        """
        raise NotImplementedError


class Statement(Expression):
    @property
    def reducible(self):
        return True


class Atom(Expression):
    value: Any

    def __str__(self):
        return f"{self.value}"

    @property
    def reducible(self):
        return False

    @property
    def to_python(self):
        return f"lambda _: {self.value}"

    def evaluate(self, _environment):
        return self


class BinaryExpression(Expression):
    left: Expression
    right: Expression

    def __init__(self, _left, _right):
        raise NotImplementedError

    def __str__(self):
        op = self.op_str()
        return f"{self.left} {op} {self.right}"

    @staticmethod
    def op_str() -> str:
        raise NotImplementedError

    @staticmethod
    def build_atom(value: Any) -> Atom:
        raise NotImplementedError

    @classmethod
    def op(cls, a: Any, b: Any) -> Any:
        op = cls.op_str()
        return OP_MAP[op](a, b)

    @property
    def to_python(self):
        op = self.op_str()
        return f"lambda e:({self.left.to_python})(e) {op} ({self.right.to_python})(e)"

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return self.__class__(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return self.__class__(self.left, self.right.reduce(environment))
        else:
            assert isinstance(self.left, Atom)
            assert isinstance(self.right, Atom)
            return self.build_atom(self.op(self.left.value, self.right.value))

    def evaluate(self, environment):
        return self.build_atom(
            self.op(
                self.left.evaluate(environment).value,
                self.right.evaluate(environment).value,
            )
        )
