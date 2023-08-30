from typing import Type

from lark import Lark, Token
from lark import Transformer as _Transformer

from ..exceptions import Unreachable
from .expressions import (
    Add,
    And,
    EqualTo,
    LessThan,
    Multiply,
    Number,
    Or,
    Sub,
    Variable,
)
from .expressions.abstract import BinaryExpression, Expression
from .statements import Assign, DoNothing, If, Sequence, While

# inspired by
# https://medium.com/@gvanrossum_83706/building-a-peg-parser-d4869b5958fb
# https://medium.com/@gvanrossum_83706/left-recursive-peg-grammars-65dab3c580e1
# note: lark is not exhaustive, so `expr: term ('+' term)*` won't work
GRAMMAR = r"""
%import common.ESCAPED_STRING   -> STRING
%import common.INT              -> NUMBER
%import common.CNAME            -> NAME
%import common.WS
%ignore WS

OP_AND: "&&"
OP_OR: "||"
OP_EQ: "<" | "=="
OP_ADD: "+" | "-"
OP_MUL: "*"
atom: NUMBER | NAME | "(" expr ")"

expr: expr OP_ADD mul_expr | mul_expr
mul_expr: mul_expr OP_MUL atom | atom

or_expr: or_expr OP_OR and_expr | and_expr
and_expr: and_expr OP_AND eq_expr | eq_expr
eq_expr: expr OP_EQ expr

if_stmt: "if" "(" or_expr ")" "{" stmts "}" [("else" "{" stmts "}")]
while_stmt: "while" "(" or_expr ")" "{" stmts "}"
assign_stmt: NAME "=" expr

stmt: expr | if_stmt | while_stmt | assign_stmt
stmts: stmt*
"""

parser = Lark(GRAMMAR, start="stmts", parser="lalr")


def token_to_atom(token: Token) -> Expression:
    if token.type == "NUMBER":
        return Number(int(token.value))
    elif token.type == "NAME":
        return Variable(token.value)
    else:
        raise Unreachable


def eval_binary_expr(
    left,
    op,
    right,
    expected_ops: list[str],
    expr_classes: list[Type[BinaryExpression]],
):
    for expected_op, expr_class in zip(expected_ops, expr_classes):
        if op.value == expected_op:
            return [expr_class(left[0], right[0])]
    raise Unreachable


class Transformer(_Transformer):
    def atom(self, items) -> list[Expression]:
        res = []
        for item in items:
            if isinstance(item, Token):
                res.append(token_to_atom(item))
            else:
                res.append(item[0])
        return res

    def _biexpr(self, items, expected_ops, expr_classes):
        if len(items) == 1:
            return items[0]
        left, op, right = items[0], items[1], items[2]
        return eval_binary_expr(left, op, right, expected_ops, expr_classes)

    def and_expr(self, items):
        return self._biexpr(items, ["&&"], [And])

    def or_expr(self, items):
        return self._biexpr(items, ["||"], [Or])

    def eq_expr(self, items):
        return self._biexpr(items, ["<", "=="], [LessThan, EqualTo])

    def expr(self, items):
        return self._biexpr(items, ["+", "-"], [Add, Sub])

    def mul_expr(self, items):
        return self._biexpr(items, ["*"], [Multiply])

    def if_stmt(self, items):
        cond, seq, alt = items[0][0], items[1], items[2]
        return If(cond, seq, alt or DoNothing())

    def while_stmt(self, items):
        return While(items[0][0], self.stmt(items[1:]))

    def assign_stmt(self, items):
        return Assign(items[0].value, items[1][0])

    def stmt(self, items):
        if len(items) == 1:
            return items[0]
        else:
            raise Unreachable

    def stmts(self, items):
        if len(items) == 0:
            return DoNothing()
        elif len(items) == 1:
            return items[0]

        return Sequence(items[0], self.stmts(items[1:]))


def parse(program: str):
    tree = parser.parse(program)
    return Transformer().transform(tree)
