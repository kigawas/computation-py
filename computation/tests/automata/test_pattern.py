import unittest
from computation.automata.pattern import Choose, Repeat, Concatenate, Literal, Empty


class PatternTest(unittest.TestCase):
    def test_pattern(self):
        pattern = Repeat(Choose(
            Concatenate(
                Literal('a'), Literal('b')), Literal('a')))
        self.assertEqual(repr(pattern), '/(ab|a)*/')
        self.assertEqual(str(pattern), '(ab|a)*')

        self.assertFalse(Empty().matches('a'))
        self.assertTrue(Literal('a').matches('a'))

        pattern = Repeat(Concatenate(
            Literal('a'), Choose(Empty(), Literal('b'))))
        self.assertEqual(repr(pattern), '/(a(|b))*/')
        self.assertTrue(pattern.matches(''))
        self.assertTrue(pattern.matches('a'))
        self.assertTrue(pattern.matches('ab'))
        self.assertTrue(pattern.matches('aba'))
        self.assertTrue(pattern.matches('abab'))
        self.assertTrue(pattern.matches('abaab'))
        self.assertFalse(pattern.matches('bbba'))

    def test_nfa_design(self):
        nfa_d = Empty().to_nfa_design
        self.assertTrue(nfa_d.accepts(''))
        self.assertFalse(nfa_d.accepts('a'))

        nfa_d = Literal('a').to_nfa_design
        self.assertFalse(nfa_d.accepts(''))
        self.assertTrue(nfa_d.accepts('a'))
        self.assertFalse(nfa_d.accepts('b'))

        pattern = Concatenate(Literal('a'), Literal('b'))
        self.assertTrue(pattern.matches('ab'))
        self.assertFalse(pattern.matches('a'))
        self.assertFalse(pattern.matches('b'))
        self.assertFalse(pattern.matches('abc'))

        pattern = Concatenate(
            Literal('a'), Concatenate(
                Literal('b'), Literal('c')))
        self.assertTrue(pattern.matches('abc'))
        self.assertFalse(pattern.matches('a'))
        self.assertFalse(pattern.matches('b'))
        self.assertFalse(pattern.matches('ab'))

        pattern = Choose(Literal('a'), Literal('b'))
        self.assertTrue(pattern.matches('a'))
        self.assertTrue(pattern.matches('b'))
        self.assertFalse(pattern.matches('c'))

        pattern = Repeat(Literal('a'))
        self.assertTrue(pattern.matches(''))
        self.assertTrue(pattern.matches('a'))
        self.assertTrue(pattern.matches('aa'))
        self.assertTrue(pattern.matches('aaaaaaaaaa'))
        self.assertFalse(pattern.matches('b'))


if __name__ == '__main__':

    unittest.main()
