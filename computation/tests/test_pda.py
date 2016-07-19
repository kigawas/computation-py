import unittest

from computation.automata.pda import (Stack, PDAConfiguration, PDARule,
                                      DPDARulebook, DPDA, DPDADesign,
                                      NPDARulebook, NPDA, NPDADesign)


class PDATest(unittest.TestCase):
    def test_pda_rule(self):
        rule = PDARule(1, '(', 2, '$', ['b', '$'])
        configuration = PDAConfiguration(1, Stack(['$']))
        self.assertTrue(rule.applies_to(configuration, '('))

    def test_pda_config(self):
        config1 = PDAConfiguration(3, Stack(['$']))
        config2 = PDAConfiguration(3, Stack(['$']))
        self.assertEqual(config1, config2)
        self.assertEqual(set([config1, config2]), set([config1]))

    def test_pda_rulebook(self):
        configuration = PDAConfiguration(1, Stack(['$']))
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  # yapf: disable

        configuration = rulebook.next_configuration(configuration, '(')
        self.assertEqual(configuration.stack, Stack(['$', 'b']))

    def test_dpda(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  # yapf: disable
        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        self.assertTrue(dpda.accepting)
        self.assertFalse(dpda.read_string('(()').accepting)
        self.assertEqual(dpda.current_configuration.state, 2)

        with self.assertRaises(RuntimeError):
            DPDARulebook([PDARule(1, None, 1, '$', ['$'])]).follow_free_moves(
                PDAConfiguration(1, Stack(['$'])))

        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        self.assertFalse(dpda.read_string('(()(').accepting)
        self.assertTrue(dpda.read_string('))()').accepting)

    def test_dpda_design(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  # yapf: disable
        dpda_design = DPDADesign(1, '$', [1], rulebook)
        self.assertTrue(dpda_design.accepts('(((((((((())))))))))'))
        self.assertTrue(dpda_design.accepts('()(())((()))(()(()))'))
        self.assertFalse(dpda_design.accepts('(()(()(()()(()()))()'))
        self.assertFalse(dpda_design.accepts('())'))

        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        dpda.read_string('())')
        self.assertFalse(dpda.accepting)
        self.assertTrue(dpda.is_stuck)

    def test_npda_design(self):
        rulebook = NPDARulebook([
            PDARule(1, 'a', 1, '$', ['a', '$']),
            PDARule(1, 'a', 1, 'a', ['a', 'a']),
            PDARule(1, 'a', 1, 'b', ['a', 'b']),
            PDARule(1, 'b', 1, '$', ['b', '$']),
            PDARule(1, 'b', 1, 'a', ['b', 'a']),
            PDARule(1, 'b', 1, 'b', ['b', 'b']),
            PDARule(1, None, 2, '$', ['$']),
            PDARule(1, None, 2, 'a', ['a']),
            PDARule(1, None, 2, 'b', ['b']),
            PDARule(2, 'a', 2, 'a', []),
            PDARule(2, 'b', 2, 'b', []),
            PDARule(2, None, 3, '$', ['$'])
            ])  # yapf: disable
        configuration = PDAConfiguration(1, Stack(['$']))
        npda = NPDA([configuration], [3], rulebook)
        self.assertTrue(npda.accepting)
        self.assertFalse(npda.read_string('abb').accepting)
        self.assertTrue(PDAConfiguration(1, Stack([u'$', u'a', u'b', u'b']) in
                                         npda.current_configurations))
        self.assertTrue(npda.read_character('a').accepting)
        self.assertTrue(PDAConfiguration(1, Stack(
            [u'$', u'a', u'b', u'b', u'a']) in npda.current_configurations))
        npda_design = NPDADesign(1, '$', [3], rulebook)
        self.assertTrue(npda_design.accepts('abba'))
        self.assertTrue(npda_design.accepts('babbaabbab'))
        self.assertFalse(npda_design.accepts('abb'))


if __name__ == '__main__':
    unittest.main()
