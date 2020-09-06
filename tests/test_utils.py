import unittest
from itertools import chain

from computation.automata.utils import detect
from computation.interpreter.utils import merge_dict


class UtilTest(unittest.TestCase):
    def test_detect(self):
        self.assertEqual(detect([1, 2, 3], lambda x: x > 1 and x < 3), 2)
        self.assertEqual(detect([1, 2, 3], lambda x: False), None)
        self.assertEqual(detect([1, 2, 3], lambda x: True), 1)

    def test_merge_dict(self):
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"a": 2}

        self.assertEqual(merge_dict(d1, d2), dict(chain(d1.items(), d2.items())))
        self.assertEqual(merge_dict(d1, d2), {"a": 2, "b": 2, "c": 3})
