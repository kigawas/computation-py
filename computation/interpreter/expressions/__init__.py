from dataclasses import dataclass


from .abstract import Atom, Expression, BinaryExpression


@dataclass(order=True)
class Number(Atom):
    value: int


@dataclass
class Boolean(Atom):
    value: bool


@dataclass
class Variable(Expression):
    name: str

    def __str__(self):
        return f"{self.name}"

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def evaluate(self, environment):
        return environment[self.name]

    @property
    def to_python(self):
        return f"lambda e: e['{self.name}']"


@dataclass
class Add(BinaryExpression):
    left: Expression
    right: Expression

    @staticmethod
    def op_str() -> str:
        return "+"

    @staticmethod
    def build_atom(value):
        return Number(value)

    @property
    def to_python(self):
        return f"lambda e:({self.left.to_python})(e) + ({self.right.to_python})(e)"


@dataclass
class Multiply(BinaryExpression):
    left: Expression
    right: Expression

    @staticmethod
    def op_str() -> str:
        return "*"

    @staticmethod
    def build_atom(value):
        return Number(value)


@dataclass
class LessThan(BinaryExpression):
    left: Expression
    right: Expression

    def __str__(self):
        op = self.op_str()
        return f"{self.left} {op} {self.right}"

    @classmethod
    def op_str(cls) -> str:
        return "<"

    @staticmethod
    def build_atom(value):
        return Boolean(value)
