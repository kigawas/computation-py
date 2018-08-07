from functools import total_ordering


@total_ordering
class Number(object):
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("Not Number")
        self.value = value

    def __repr__(self):
        return "Number({})".format(self.value)

    def __str__(self):
        return "{}".format(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    @property
    def reducible(self):
        return False

    def evaluate(self, environment):
        return self

    @property
    def to_python(self):
        return "lambda e: {}".format(self.value)


class Boolean(object):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise TypeError("Not Boolean")
        self.value = value

    def __repr__(self):
        return "Boolean({})".format(self.value)

    def __str__(self):
        return "{}".format(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    @property
    def reducible(self):
        return False

    def evaluate(self, environment):
        return self

    @property
    def to_python(self):
        return "lambda e: {}".format(self.value)


class Variable(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(self.name)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def evaluate(self, environment):
        return environment[self.name]

    @property
    def to_python(self):
        return "lambda e: e['{}']".format(self.name)


class Add(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} + {})".format(self.left, self.right)

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
        return "lambda e:({})(e) + ({})(e)".format(
            self.left.to_python, self.right.to_python
        )


class Multiply(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} * {})".format(self.left, self.right)

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
        return "lambda e:({})(e) * ({})(e)".format(
            self.left.to_python, self.right.to_python
        )


class LessThan(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} < {})".format(self.left, self.right)

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
        return "lambda e:({})(e) < ({})(e)".format(
            self.left.to_python, self.right.to_python
        )
