from __future__ import print_function, unicode_literals

import unittest


def merge_dict(dic1, dic2):
    '''Merge dic2 to dic1 without changing dic1'''
    dm = {}
    for k, v in dic1.iteritems():
        dm[k] = v
    for k, v in dic2.iteritems():
        dm[k] = v
    return dm


class UtilTest(unittest.TestCase):
    def test_merge_dict(self):
        d1 = {'a': 1, 'b': 2, 'c': 3}
        d2 = {'a': 2}
        self.assertEqual(merge_dict(d1, d2), {'a': 2, 'b': 2, 'c': 3})


if __name__ == '__main__':
    unittest.main()
