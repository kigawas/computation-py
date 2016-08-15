

import unittest


def detect(arr, func):
    for i in arr:
        if func(i):
            return i


class UtilTest(unittest.TestCase):
    def test_detect(self):
        self.assertEqual(detect([1, 2, 3], lambda x: x > 1 and x < 3), 2)
        self.assertEqual(detect([1, 2, 3], lambda x: False), None)
        self.assertEqual(detect([1, 2, 3], lambda x: True), 1)


if __name__ == '__main__':
    unittest.main()
