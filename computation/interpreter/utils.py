from __future__ import print_function, unicode_literals
from itertools import chain

import unittest


def merge_dict(dic1, dic2):
    '''Merge dic2 to dic1 without changing dic1'''
    return {k: v for d in (dic1, dic2) for k, v in d.items()}


class UtilTest(unittest.TestCase):
    def test_merge_dict(self):
        d1 = {'a': 1, 'b': 2, 'c': 3}
        d2 = {'a': 2}

        self.assertEqual(
            merge_dict(d1, d2), dict(chain(d1.items(), d2.items())))
        self.assertEqual(merge_dict(d1, d2), {'a': 2, 'b': 2, 'c': 3})


if __name__ == '__main__':
    unittest.main()
