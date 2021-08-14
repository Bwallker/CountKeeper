from comparators import *


def test_less_than_limit_comparator():
    comparator = LessThanLimitComparator(5)
    assert comparator.comparison(4)
    assert not comparator.comparison(5)


def test_comparator_repr():
    assert GreaterThanLimitComparator(5).__repr__() == "> 5"


def test_reverse_comparator():
    assert GreaterThanLimitComparator(
        5).reverse() == LessThanLimitComparator(6)

    assert EqualToLimitComparator(5).reverse() == NotEqualToLimitComparator(5)


def test_simplify_comparator():
    assert GreaterThanOrEqualToLimitComparator(
        5).simplify() == GreaterThanLimitComparator(4)
    assert EqualToLimitComparator(5).simplify() == EqualToLimitComparator(5)
