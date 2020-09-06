from dataclasses import dataclass


class Expression:
    @property
    def reducible(self):
        raise NotImplementedError

    @property
    def to_python(self):
        """
        Python lambda generator
        """
        raise NotImplementedError

    def evaluate(self, environment):
        """
        Evaluate everything in "recursive descent"
        """
        raise NotImplementedError

    def reduce(self):
        """
        Reduce step by step
        """
        raise NotImplementedError


@dataclass(order=True)
class Number(Expression):
    value: int

    def __str__(self):
        return f"{self.value}"

    @property
    def reducible(self):
        return False

    def evaluate(self, environment):
        return self

    @property
    def to_python(self):
        return f"lambda e: {self.value}"


@dataclass
class Boolean(Expression):
    value: bool

    def __str__(self):
        return f"{self.value}"

    @property
    def reducible(self):
        return False

    def evaluate(self, environment):
        return self

    @property
    def to_python(self):
        return f"lambda e: {self.value}"


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
class Add(Expression):
    left: Number
    right: Number

    def __str__(self):
        return f"({self.left} + {self.right})"

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def evaluate(self, environment):
        return Number(
            self.left.evaluate(environment).value
            + self.right.evaluate(environment).value
        )

    @property
    def to_python(self):
        return f"lambda e:({self.left.to_python})(e) + ({self.right.to_python})(e)"


@dataclass
class Multiply(Expression):
    left: Number
    right: Number

    def __str__(self):
        return f"({self.left} * {self.right})"

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)

    def evaluate(self, environment):
        return Number(
            self.left.evaluate(environment).value
            * self.right.evaluate(environment).value
        )

    @property
    def to_python(self):
        return f"lambda e:({self.left.to_python})(e) * ({self.right.to_python})(e)"


@dataclass
class LessThan(Expression):
    left: Number
    right: Number

    def __str__(self):
        return f"{self.left} < {self.right}"

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def evaluate(self, environment):
        return Boolean(
            self.left.evaluate(environment).value
            < self.right.evaluate(environment).value
        )

    @property
    def to_python(self):
        return f"lambda e:({self.left.to_python})(e) < ({self.right.to_python})(e)"
