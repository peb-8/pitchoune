from typing import List
from typeguard import typechecked

from .aggregation import Aggregation
from .type import Type


@typechecked
class Column:

    def __init__(self, name: str, value_type: Type, values=None, length: int = 0):
        self.name = name
        self.value_type = value_type
        self.values = [value_type.cast(value=value) for value in values] if values else [] if length == 0 else [None]*length

    def __next__(self):
        for value in self.values:
            yield value

    def __getitem__(self, index):
        return self.values[index]

    def __eq__(self, obj):
        if self.name != obj.name or \
            self.value_type != obj.value_type or \
                len(self) != len(obj):
            return False
        # return self.clone().sort() == obj.clone().sort()
        return self.values == obj.values

    def __hash__(self) -> int:
        return id(self.name)

    def filter(self, mask):
        return Column(name=self.name, value_type=self.value_type, values=[value for k, value in enumerate(self.values) if mask[k]])

    def empty(self):
        return Column(name=self.name, value_type=self.value_type)

    def clone(self):
        return Column(name=self.name, value_type=self.value_type, values=self.values)

    def __str__(self):
        return f"{self.name}<{self.value_type.__class__.__name__}>={self.values}"

    def __repr__(self):
        return f"{self.name}<{self.value_type.__class__.__name__}>={self.values}"

    @staticmethod
    def reduce(col):
        return Column(name=col.name, value_type=col.value_type, values=set(col.values))

    def __len__(self) -> int:
        return len(self.values)

    def count(self) -> int:
        return len(self.values)

    def unique_count(self) -> int:
        return len(set(self.values))

    def mean(self) -> Aggregation:
        return sum(float(value) for value in self.values)/len(self.values)

    def get_sort_indexes(self, asc: bool = True) -> List[int]:
        return [i[0] for i in sorted(enumerate(self.values), key=lambda x: x[1], reverse=not asc)]

    def sort_by_indexes(self, indexes, asc=False):
        return Column(name=self.name, value_type=self.value_type, values=[val for (_, val) in sorted(zip(indexes, self.values), key=lambda x: x[0], reverse=not asc)])

    def sort(self, asc: bool = True):
        self.values = sorted(self.values, reverse=not asc)
        return self
