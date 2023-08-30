# computation-py

[![License](https://img.shields.io/github/license/kigawas/computation-py.svg)](https://github.com/kigawas/computation-py)
[![CI](https://img.shields.io/github/actions/workflow/status/kigawas/computation-py/ci.yml?branch=master)](https://github.com/kigawas/computation-py/actions)
[![Codecov](https://img.shields.io/codecov/c/github/kigawas/computation-py.svg)](https://codecov.io/gh/kigawas/computation-py)

Python implementation for [Understanding Computation](http://computationbook.com/).

## Introduction

[Understanding Computation](http://computationbook.com/) is an awesome book about computation theory, which explains profound and complicated concepts by using short and concise Ruby code snippets.

I don't want to evangelize, but if you are curious about how a program functions, you must read this book. It's just like SICP's ruby version in a way, yet with much more fun.

## What does this repository cover

I just implemented equivalent codes from chapter to chapter, those contents are:

1. Two kinds of interpreters for a simple language with a parser based on [lark](https://github.com/lark-parser/lark)

2. Generating Python code for this language instead of Ruby (Because Python's anonymous functions are quite more limited than Ruby, there are some hacks like [Y-combinator](https://kigawas.me/posts/y-combinator-in-python/))

3. Simulating automata such as DFA, NFA, PDA

4. Using automata to build a simple regular expression engine

5. Simulating a Turing machine

6. Lambda calculus and Church numbers

7. Stay tuned..

## What is your Python's version

Python 3.9+
