from dataclasses import dataclass

from .expressions import Boolean
from .expressions.abstract import Expression, Statement


@dataclass
class DoNothing(Statement):
    def __str__(self):
        return "do-nothing"

    @property
    def reducible(self):
        return False

    def evaluate(self, environment):
        return environment

    @property
    def to_python(self):
        return "lambda e: e"


@dataclass
class Assign(Statement):
    name: str
    expression: Expression

    def __str__(self):
        return f"{self.name} = {self.expression}"

    def reduce(self, environment):
        if self.expression.reducible:
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            return DoNothing(), environment | {self.name: self.expression}

    def evaluate(self, environment):
        return environment | {self.name: self.expression.evaluate(environment)}

    @property
    def to_python(self):
        """
        Use dict comprehension or Python 3.9 new dict merge expression
        to eliminate outer function dependency

        This also works before Python 3.9:
        ```python
        lambda e: {{k: v for d in (e, {{"{self.name}": ({self.expression.to_python})(e)}}) for k, v in d.items()}}
        ```
        """

        return f'lambda e: e | {{"{self.name}": ({self.expression.to_python})(e)}}'


@dataclass
class If(Statement):
    condition: Expression
    consequence: Expression
    alternative: Expression

    def __str__(self):
        return f"if ({self.condition}) {{ {self.consequence} }} else {{ {self.alternative} }}"

    def reduce(self, environment):
        if self.condition.reducible:
            return (
                If(
                    self.condition.reduce(environment),
                    self.consequence,
                    self.alternative,
                ),
                environment,
            )
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            elif self.condition == Boolean(False):
                return self.alternative, environment

            raise ValueError("Invalid condition")

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.consequence.evaluate(environment)
        elif self.condition.evaluate(environment) == Boolean(False):
            return self.alternative.evaluate(environment)

        raise ValueError("Invalid condition")

    @property
    def to_python(self):
        return f"lambda e: ({self.consequence.to_python})(e) if ({self.condition.to_python})(e) else ({self.alternative.to_python})(e)"


@dataclass
class Sequence(Statement):
    first: Expression
    second: Expression

    def __str__(self):
        return f"{self.first}; {self.second}"

    def reduce(self, environment):
        if self.first == DoNothing():
            return self.second, environment
        else:
            reduced_first, reduced_env = self.first.reduce(environment)
            return Sequence(reduced_first, self.second), reduced_env

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))

    @property
    def to_python(self):
        return f"lambda e: ({self.second.to_python})(({self.first.to_python})(e))"


@dataclass
class While(Statement):
    condition: Expression
    body: Expression

    def __str__(self):
        return f"while ({self.condition}) {{ {self.body} }}"

    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self), DoNothing()), environment

    def evaluate(self, environment):
        """Optimize tail recursion"""
        while True:
            if self.condition.evaluate(environment) == Boolean(False):
                return environment
            elif self.condition.evaluate(environment) == Boolean(True):
                environment = self.body.evaluate(environment)

    def evaluate_with_recursion(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.evaluate_with_recursion(self.body.evaluate(environment))
        elif self.condition.evaluate(environment) == Boolean(False):
            return environment

    @property
    def to_python(self):
        """
        This is a workaround using Y-combinator because Python doesn't allow lambda expression including `while`,
        so we have to implement while using recursion.

        But notice that Python does no tail recursion optimization,
        so it may raise `RuntimeError` when looping too many times,
        check the limit by `import sys; sys.getrecursionlimit()`
        """
        return f"(lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args))))(lambda wh: lambda e: e if ({self.condition.to_python})(e) is False else wh(({self.body.to_python})(e)))"
