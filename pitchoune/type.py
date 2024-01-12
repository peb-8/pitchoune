from datetime import date
from typing import Any


class Type:

    def __init__(self, ref_type: Any, multiple: bool = False) -> None:
        self.multiple = multiple
        self.ref_type = ref_type

    def cast(self, value: Any):
        try:
            return self.ref_type(value) if not self.multiple else [self.ref_type(v) for v in value]
        except (ValueError, TypeError):
            return None

    def __eq__(self, other: object) -> bool:
        # print(self.multiple, "@", other.multiple)
        return self.multiple == other.multiple and  \
            self.ref_type == other.ref_type


class Boolean(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=bool, multiple=False)

    def to_array(self):
        return BooleanArray()


class Integer(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=int, multiple=False)

    def to_array(self):
        return IntegerArray()


class Float(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=float, multiple=False)

    def to_array(self):
        return FloatArray()


class String(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=str, multiple=False)

    def to_array(self):
        return StringArray()


class Date(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=date, multiple=False)

    def to_array(self):
        return DateArray()

    def cast(self, value):
        return date.fromisoformat(value)


class BooleanArray(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=bool, multiple=True)


class IntegerArray(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=int, multiple=True)


class FloatArray(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=float, multiple=True)


class StringArray(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=str, multiple=True)


class DateArray(Type):
    def __init__(self) -> None:
        super().__init__(ref_type=date, multiple=True)

    def cast(self, value):
        return [date.fromisoformat(v) for v in value]
