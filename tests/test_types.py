from datetime import date

from pitchoune.type import (
    Integer,
    Boolean,
    Float,
    String,
    Date,
    IntegerArray,
    BooleanArray,
    FloatArray,
    StringArray,
    DateArray
)


def test_integer():

    value_type = Integer()
    assert value_type.cast(5.5) == 5


def test_boolean():

    value_type = Boolean()
    assert value_type.cast(1) is True
    assert value_type.cast(0) is False


def test_float():

    value_type = Float()
    assert value_type.cast(5) == 5.0


def test_string():

    value_type = String()
    assert value_type.cast(5) == "5"


def test_date():

    value_type = Date()
    assert value_type.cast("2021-01-01") == date(day=1, month=1, year=2021)


def test_integer_array():

    value_type = IntegerArray()
    assert value_type.cast([1., 2., 3., 4.]) == [1, 2, 3, 4]


def test_float_array():

    value_type = FloatArray()
    assert value_type.cast([1, 2, 3, 4]) == [1., 2., 3., 4.]


def test_bool_array():

    value_type = BooleanArray()
    assert value_type.cast([0, 1, 0, 0]) == [False, True, False, False]


def test_string_array():

    value_type = StringArray()
    assert value_type.cast([1, 2, 3, 4]) == ["1", "2", "3", "4"]


def test_date_array():

    value_type = DateArray()
    assert value_type.cast(["2021-01-01", "2021-01-02", "2021-01-03"]) == [date(day=1, month=1, year=2021), date(day=2, month=1, year=2021), date(day=3, month=1, year=2021)]
