import itertools

from .type import Float, Integer

from .aggregation import Aggregation
from .column import Column


class Group:

    def __init__(self, table, grouped_cols) -> None:
        self.table = table.clone()
        self.grouped_cols = [Column.reduce(col) for col in grouped_cols]
        rows = [col for col in itertools.product(*[col.values for col in self.grouped_cols])]
        cols_values = [*zip(*rows)]
        for k in range(len(self.grouped_cols)):
            self.grouped_cols[k] = Column(name=self.grouped_cols[k].name, value_type=self.grouped_cols[k].value_type, values=cols_values[k])

    def aggregate(self, *operations):
        """"""
        # create empty aggregated columns
        agg_cols = []
        for operation in operations:
            for col_name, col_value_type in self.table.schema:
                if col_name == operation.on:
                    agg_col = Column(name=operation.on, value_type=col_value_type)
                    if operation.op in ("collect_set", "collect"):
                        agg_col.value_type = agg_col.value_type.to_array()
                    elif operation.op == "mean":
                        agg_col.value_type = Float()
                    agg_cols.append(agg_col)
                    break
        # populate agg cols filtered with grouped cols using aggregation operations
        table = type(self.table)(*self.grouped_cols)
        for row in table.rows:
            sub_table = self.table.filter(lambda x: sum([x[k] == v for k, v in row.items()]) == len(row))
            for col in sub_table.cols:
                if col.name == operation.on:
                    agg_value = operation.process(col.values)
                    for agg_col in agg_cols:
                        if agg_col.name == operation.on:
                            agg_col.values.append(agg_value)
                            break
        for col in agg_cols:
            table.add_column(col)
        return table

    def count(self):
        """"""
        self.table = self.table.add_column(Column(name="count", value_type=Integer(), length=self.table.height))
        return self.aggregate(Aggregation(op="count", on="count"))

    def unique_count(self):
        """"""
        self.table = self.table.add_column(Column(name="unique_count", value_type=Integer(), length=self.table.height))
        return self.aggregate(Aggregation(op="unique_count", on="unique_count"))

    def __str__(self) -> str:
        return f"Aggregation(grouped_cols={self.grouped_cols})"

    def __repr__(self) -> str:
        return f"Aggregation(grouped_cols={self.grouped_cols})"
