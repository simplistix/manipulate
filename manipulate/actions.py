from dataclasses import dataclass
from typing import Iterable, Any, TypeAlias, Callable, Type, TypeVar, Generic

from .elements import Element, Start, End
from .elements import Text
from .tabular import Format, Row, Table

Action: TypeAlias = Callable[[Iterable[Element[Any]]], Iterable[Element[Any]]]

T = TypeVar("T", bound=Element[Any])


@dataclass
class Container(Generic[T]):
    type: Type[T]

    def __call__(self, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        current: T | None = None
        value: Any
        for element in elements:
            match element:
                case Start(self.type(value)):
                    if current is not None:
                        raise ValueError(f'attempt to open {value} before {current} was closed')
                    current = value
                    yield element
                case End(self.type(value)):
                    if value is not current:
                        raise ValueError(f'attempt to close {value} when {current} was open')
                    current = None
                    yield element
                case _:
                    yield element

class Parse:

    def __init__(self, format: Format) -> None:
        self.format = format

    def __call__(self, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        for element in elements:
            if isinstance(element, Text):
                table = self.format.parse(element.value)
                yield Start(table)
                for row in table.rows:
                    yield Element[Row](row)
                yield End(table)
            else:
                yield element


class Render:

    def __init__(self, format: Format) -> None:
        self.format = format

    def __call__(self, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        table: Table | None = None
        start_table: Table | None = None
        rows: list[Row] = []
        for element in elements:
            if isinstance(element, Start) and isinstance(start_table := element.value, Table):
                if table is not None:
                    raise ValueError(
                        f'nested tables not supported, {element!r} before End({table!r}) ended'
                    )
                table = Table(columns=start_table.columns, rows=rows)
            elif isinstance(row := element.value, Row):
                rows.append(row)
            elif isinstance(element, End) and isinstance(end_table := element.value, Table):
                if table is None:
                    raise ValueError(f'{element!r} before Start({end_table!r})')
                elif end_table is not start_table:
                    raise ValueError(f'{element!r}, expected End({start_table!r})')
                yield Text(self.format.render(table))
            else:
                yield element
