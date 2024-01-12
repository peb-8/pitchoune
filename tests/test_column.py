from pitchoune.column import Column
from pitchoune.type import Integer


def test_sort_indices():

    assert Column(name="A", value_type=Integer(), values=[4, 5, 2, 1, 8, 3, 2]).get_sort_indexes() == [3, 2, 6, 5, 0, 1, 4]


def test_columns_equality():

    assert Column(name="A", value_type=Integer(), values=[1, 2, 3]) == Column(name="A", value_type=Integer(), values=[1, 2, 3])


def test_column_filter():

    assert Column(name="A", value_type=Integer(), values=[1, 2, 3, 4, 5]).filter(mask=[True, True, True, False, True]) == Column(name="A", value_type=Integer(), values=[1, 2, 3, 5])
