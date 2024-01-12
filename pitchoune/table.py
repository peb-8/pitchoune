from typeguard import typechecked

from typing import List, Callable, Self, Tuple, Any

from .type import Type

from .group import Group
from .column import Column
from .utils import sort_iterable_in_dict_values, table_str


@typechecked
class Table:

    def __init__(self, *cols: Column) -> None:
        self._cols = list(cols) or []

    def __str__(self) -> str:
        return table_str(self)

    def __repr__(self) -> str:
        return f"Table({', '.join(str(col) for col in self.cols)}])"

    def clone(self) -> Self:
        return Table(*[col for col in self._cols])

    def create_column(self, name: str, value_type: Type, values: List | Callable = None) -> Self:
        values = values or []
        for col in self.cols:
            if col.name == self.cols:
                raise Exception(f"Column name '{name}' already in use")
        self._cols.append(Column(name=name, value_type=value_type, values=[values(row) for row in self.rows] if callable(values) else values))
        return self

    def add_column(self, col: Column) -> Self:
        self._cols.append(col)
        return self

    def __eq__(self, obj: Self) -> bool:
        found_indexes = []
        for row in self.rows:
            found = False
            row = sort_iterable_in_dict_values(row)
            for k, obj_row in enumerate(obj.rows):
                obj_row = sort_iterable_in_dict_values(obj_row)
                if row == obj_row and k not in found_indexes:
                    found_indexes.append(k)
                    found = True
                    break
            if not found:
                return False
        return True

    @property
    def schema(self) -> List[Tuple[str, Any]]:
        return [(col.name, col.value_type) for col in self.cols]

    @property
    def height(self) -> int:
        return len(max(self._cols, key=len))

    @property
    def width(self) -> int:
        return len(self._cols)

    @property
    def rows(self):
        def _():
            for r in range(self.height):
                yield {col.name: col[r] for col in self.cols}
        return _()

    @property
    def cols(self):
        def _():
            self._cols.sort(key=lambda x: x.name)
            for col in self._cols:
                yield col
        return _()

    def filter(self, condition: Callable) -> Self:
        return self.apply_mask([condition(row) for row in self.rows])

    def apply_mask(self, mask):
        cols = []
        for col in self.cols:
            filtered_col = col.filter(mask)
            cols.append(Column(name=filtered_col.name, value_type=filtered_col.value_type, values=filtered_col.values))
        return Table(*cols)

    def group_by(self, *column_names) -> Group:
        return Group(table=self, grouped_cols=[col for col in self.cols if col.name in column_names])

    def union(self, other_table: Self) -> Self:
        if self.schema != other_table.schema:
            raise Exception("Union can only be applied with two tables with the same schema")
        cols = []
        for c1 in self.cols:
            for c2 in other_table.cols:
                if c1.name == c2.name and c1.value_type == c2.value_type:
                    cols.append(Column(name=c1.name, value_type=c1.value_type, values=c1.values + c2.values))
                    break
        return Table(*cols).distinct()

    @staticmethod
    def load_from_csv(path: str, value_types: List[Type]):
        import csv
        cols = []
        data = []
        with open(path) as file:
            data = [row for row in csv.reader(file, delimiter=',')]
            cols = [Column(name=name, value_type=value_type, values=list(values)) for name, value_type, values in zip(data[0], value_types, zip(*data[1:]))]
            return Table(*cols)

    def select(self, *col_names) -> Self:
        return Table(*[col for col in self.cols if col.name in col_names])

    def distinct(self) -> Self:
        rows = []
        mask = []
        for row in self.rows:
            if row not in rows:
                rows.append(row)
                mask.append(True)
            else:
                mask.append(False)
        return self.apply_mask(mask)

    def drop(self, col_name: str) -> Self:
        return Table(col for col in self.cols if col.name != col_name)

    def join(self, on: Self, where: Callable, how: str = "left"):
        """
            Inner Join: Returns only the rows with matching keys in both DataFrames.
            Left Join: Returns all rows from the left DataFrame and matching rows from the right DataFrame.
            Right Join: Returns all rows from the right DataFrame and matching rows from the left DataFrame.
            Full Outer Join: Returns all rows from both DataFrames, including matching and non-matching rows.
            Left Semi Join: Returns all rows from the left DataFrame where there is a match in the right DataFrame.
            Left Anti Join: Returns all rows from the left DataFrame where there is no match in the right DataFrame.
        """
        cols = set(col.empty() for col in list(self.cols) + list(on.cols))
        print(cols)
        # join_table = Table(*cols)
        for left_index, left_row in enumerate(self.rows):
            matched = False
            for right_index, right_row in enumerate(on.rows):
                if where(left_row, right_row) is True:
                    matched = True
                    # paire de lignes trouvée
                    print('match:', left_index, right_index)
            if not matched:
                # paire de lignes non trouvée
                print('not match:', left_index)

        return Table()

    def sort(self, col_name: List[str], asc=True):
        indexes = []
        for col in self.cols:
            if col.name == col_name:
                indexes = col.get_sort_indexes(asc=asc)
                break
        return Table(col.sort_by_indexes(indexes=indexes, asc=asc) for col in self.cols)
