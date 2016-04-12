from __future__ import print_function, unicode_literals

import unittest

from expressions import Variable, Add, Number, Boolean, LessThan, Multiply
from utils import merge_dict


class DoNothing(object):
    def __str__(self):
        return 'Do nothing'

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    @property
    def reducible(self):
        return False

    def evaluate(environment):
        return environment

    @property
    def to_python(self):
        return 'lambda e: e'


class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return '{} = {}'.format(self.name, self.expression)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.reducible:
            return Assign(self.name,
                          self.expression.reduce(environment)), environment
        else:
            return DoNothing(), merge_dict(environment, {self.name:
                                                         self.expression})

    def evaluate(self, environment):
        return merge_dict(environment, {self.name:
                                        self.expression.evaluate(environment)})

    @property
    def to_python(self):
        return 'lambda e: merge_dict(e, {{ \'{}\': ({})(e) }})'.format(
            self.name, self.expression.to_python)


class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return 'if ({0}) {{ {1} }} else {{ {2} }}'.format(
            self.condition, self.consequence, self.alternative)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible:
            return If(
                self.condition.reduce(environment), self.consequence,
                self.alternative), environment
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            elif self.condition == Boolean(False):
                return self.alternative, environment

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.consequence.evaluate(environment)
        elif self.condition.evaluate(environment) == Boolean(False):
            return self.alternative.evaluate(environment)

    @property
    def to_python(self):
        return 'lambda e: ({})(e) if ({})(e) else ({})(e)'.format(
            self.consequence.to_python, self.condition.to_python,
            self.alternative.to_python)


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '{}; {}'.format(self.first, self.second)

    @property
    def reducible(self):
        return True

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
        return 'lambda e: ({1})(({0})(e))'.format(self.first.to_python,
                                                  self.second.to_python)


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return 'while ({}) {{ {} }}'.format(self.condition, self.body)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self),
                  DoNothing()), environment

    def evaluate(self, environment):
        '''Optimize tail recursion'''
        while True:
            if self.condition.evaluate(environment) == Boolean(False):
                return environment
            elif self.condition.evaluate(environment) == Boolean(True):
                environment = self.body.evaluate(environment)

    def evaluate_with_recursion(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.evaluate_with_recursion(self.body.evaluate(
                environment))
        elif self.condition.evaluate(environment) == Boolean(False):
            return environment

    @property
    def to_python(self):
        # work around using Y-combinator because python don't allow lambda expression including `while`
        # so I implemented while using recursion
        # but notice that Python does no tail recursion optimization
        # it may raise RuntimeError when running too many whiles
        # check the limit by `import sys; sys.getrecursionlimit()`
        return '(lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args))))(lambda wh: lambda e: e if ({condition})(e) is False else wh(({body})(e)))'.format(
            condition=self.condition.to_python,
            body=self.body.to_python)
