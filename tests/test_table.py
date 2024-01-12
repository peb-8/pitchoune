from pitchoune.aggregation import Aggregation
from pitchoune.group import Group
from pitchoune.column import Column
from pitchoune.table import Table
from pitchoune.type import Float, Integer, String, StringArray


def test_equality():

    assert Table(
                Column(name="A", value_type=Integer(), values=[15, 25, 35]),
                Column(name="B", value_type=String(), values=["a", "aa", "aaa"])) == \
           Table(
                Column(name="A", value_type=Integer(), values=[15, 25, 35]),
                Column(name="B", value_type=String(), values=["a", "aa", "aaa"])
            )

    assert Table(
                Column(name="A", value_type=Integer(), values=[15, 25, 35]),
                Column(name="B", value_type=String(), values=["a", "aa", "aaa"])) == \
           Table(
                Column(name="A", value_type=Integer(), values=[15, 35, 25]),
                Column(name="B", value_type=String(), values=["a", "aaa", "aa"])
            )


def test_schema():

    assert Table(
                Column(name="A", value_type=Integer(), values=[15, 25, 35]),
                Column(name="B", value_type=String(), values=["a", "aa", "aaa"])
            ).schema == \
            Table(
                Column(name="A", value_type=Integer(), values=[15, 25, 35]),
                Column(name="B", value_type=String(), values=["a", "aa", "aaa"])
            ).schema


def test_distinct():

    assert Table(Column(name="A", value_type=Integer(), values=[15, 25, 25, 35]), Column(name="B", value_type=String(), values=["a", "aa", "aa", "aaa"])).distinct() == \
           Table(Column(name="A", value_type=Integer(), values=[15, 25, 35]),     Column(name="B", value_type=String(), values=["a", "aa", "aaa"]))


def test_union():

    table1 = Table(Column(name="A", value_type=Integer(), values=[15, 25, 35]), Column(name="B", value_type=String(), values=["a", "aa", "aaa"]))
    table2 = Table(Column(name="A", value_type=Integer(), values=[45, 25, 65]), Column(name="B", value_type=String(), values=["b", "aa", "bbb"]))

    assert table1.union(table2) == Table(Column(name="A", value_type=Integer(), values=[15, 25, 35, 45, 65]), Column(name="B", value_type=String(), values=["a", "aa", "aaa", "b", "bbb"]))


def test_clone_table():

    table = Table(Column(name="name", value_type=String(), values=["Kevin", "Kevin", "Kevina", "Kevin", "Kevina", "Kevina"]))
    cloned_table = table.clone()

    assert table == cloned_table
    assert id(table) != id(cloned_table)


def test_create_column():

    table = Table(Column(name="name", value_type=String(), values=["Kevin", "Kevin", "Kevina", "Kevin", "Kevina", "Kevina"]))

    assert table.width == 1
    assert table.height == 6

    table = table.create_column(name="sex", value_type=String(), values=lambda row: "M" if row["name"] == "Kevin" else "F")

    assert table.width == 2
    assert table.height == 6


def test_group_by():

    table = Table(Column(name="A", value_type=Integer(), values=[15, 25, 15, 45, 15]), Column(name="B", value_type=String(), values=["a", "aa", "aaa", "b", "bbb"]))
    table_group = table.group_by("A")
    assert type(table_group) is Group

    assert table_group.aggregate(
        Aggregation(op="collect_set", on="B")) == \
        Table(
            Column(name="A", value_type=Integer(), values=[25, 45, 15]),
            Column(name="B", value_type=StringArray(), values=[["aa"], ["b"], ["bbb", "a", "aaa"]])
        )


def test_count():

    assert Table(Column(name="A", value_type=Integer(), values=[15, 45, 45, 45, 45]), Column(name="B", value_type=String(), values=["M", "M", "F", "M", "F"])).group_by("A", "B").count() == \
           Table(
               Column(name="A", value_type=Integer(), values=[45, 45, 15, 15]),
               Column(name="B", value_type=String(), values=["F", "M", "F", "M"]),
               Column(name="count", value_type=Integer(), values=[2, 2, 0, 1])
            )


def test_unique_count():

    assert Table(
                Column(name="A", value_type=Integer(), values=[15, 45, 45, 45, 45]),
                Column(name="B", value_type=String(), values=["M", "M", "F", "M", "F"])).group_by("A", "B").unique_count() == \
           Table(
               Column(name="A", value_type=Integer(), values=[45, 45, 15, 15]),
               Column(name="B", value_type=String(), values=["F", "M", "F", "M"]),
               Column(name="unique_count", value_type=Integer(), values=[1, 1, 0, 1])
            )


def test_mean():

    assert Table(
        Column(name="age", value_type=Integer(), values=[19, 20, 23, 18, 33, 21, 48, 27, 45, 18]),
        Column(name="sex", value_type=String(), values=["M", "M", "F", "M", "F", "F", "F", "M", "F", "M"])
    ).group_by("sex").aggregate(
        Aggregation(op="mean", on="age")
    ) == \
        Table(
            Column(name="sex", value_type=String(), values=["F", "M"]),
            Column(name="age", value_type=Float(), values=[34.0, 20.4])
        )


def test_join():

    Table(
        Column(name="A", value_type=Integer(), values=[1, 2, 3, 4, 5]),
        Column(name="B", value_type=Integer(), values=[0, 1, 0, 0, 1])
    ).join(
        on=Table(
            Column(name="A", value_type=Integer(), values=[3, 3, 0, 6, 2]),
            Column(name="B", value_type=Integer(), values=[1, 1, 0, 1, 1]),
            Column(name="C", value_type=Integer(), values=[8, 8, 7, 7, 9])
        ),
        where=lambda left, right: left["A"] == right["A"],
        how="left"
    )
    assert 1 == 2
