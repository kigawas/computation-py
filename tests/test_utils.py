from computation.utils import detect


def test_detect():
    assert detect([1, 2, 3], lambda x: x > 1 and x < 3) == 2
    assert detect([1, 2, 3], lambda x: False) is None
    assert detect([1, 2, 3], lambda x: True) == 1
    assert detect([], lambda x: True) is None
