from typing import Any, Dict, List

from prettytable import PrettyTable


def get_dict_list_from_list_dict(rows: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """"""
    cols = {k: [] for k in rows[0].keys()}
    for row in rows:
        for key, value in row.items():
            cols[key].append(value)
    return cols


def table_str(table):
    """"""
    x = PrettyTable()
    x.field_names = [x.name for x in table.cols]
    x.add_rows([row for row in zip(*[col.values for col in table.cols])])
    return x[0:10].get_string()


def is_iterable(x):
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True


def sort_if_iterable(x):
    if is_iterable(x):
        return sorted(x)
    return x


def sort_iterable_in_dict_values(d):
    """"""
    return {k: sort_if_iterable(v) for k, v in d.items()}
