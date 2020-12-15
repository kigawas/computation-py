from typing import List
from lark import Lark, Transformer as _Transformer, Token


from .expressions import (
    Add,
    Variable,
    Number,
    Multiply,
    LessThan,
)
from .statements import DoNothing, Sequence, Assign, While
from .expressions.abstract import Expression

GRAMMAR = r"""
%import common.ESCAPED_STRING   -> STRING
%import common.INT    -> NUMBER
%import common.CNAME            -> NAME
%import common.WS
%ignore WS

OP: "+" | "*" | "<"
atom: NUMBER | NAME
expr: atom | atom OP expr
while_loop: "while" "(" expr ")" "{" stmt* "}"
assign: NAME "=" expr
stmt: assign | expr | while_loop
program: stmt*
"""

parser = Lark(GRAMMAR, start="program")


def token_to_atom(token: Token) -> Expression:
    if token.type == "NUMBER":
        return Number(int(token.value))
    elif token.type == "NAME":
        return Variable(token.value)
    raise ValueError("Invalid token")


class Transformer(_Transformer):
    def atom(self, items: List[Token]) -> List[Expression]:
        return [token_to_atom(t) for t in items]

    def assign(self, items):
        return Assign(items[0].value, items[1][0])

    def expr(self, items):
        if len(items) == 1:
            return items[0]

        left, op, right = items[0], items[1], items[2]
        if op.value == "+":
            return [Add(left[0], right[0])]
        elif op.value == "*":
            return [Multiply(left[0], right[0])]
        elif op.value == "<":
            return [LessThan(left[0], right[0])]
        else:
            raise ValueError

    def while_loop(self, items):
        return While(items[0][0], self.stmt(items[1:]))

    def program(self, items):
        if len(items) == 0:
            return DoNothing()
        elif len(items) == 1:
            return items[0]

        return Sequence(items[0], self.stmt(items[1:]))

    def stmt(self, items):
        if len(items) == 1:
            return items[0]

        return Sequence(items[0], self.stmt(items[1:]))


def parse(program: str):
    tree = parser.parse(program)
    return Transformer().transform(tree)
