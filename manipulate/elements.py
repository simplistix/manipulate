from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar, Generic, Any

T = TypeVar('T')


@dataclass
class Element(Generic[T]):
    value: T
    parent: 'Element[Any] | None' = None
    line: int | None = None
    column: int | None = None

    def __str__(self) -> str:
        return f'{type(self).__qualname__}({self.value!r})'


class Start(Element[T]):
    pass


class End(Element[T]):
    pass


class File(Element[Path]):
    pass


class Bytes(Element[bytes]):
    pass


@dataclass
class Text(Element[str]):
    """
    A textual element. If it is embedded within another textual element or file,
    it may have a prefix specified, if that prefix occurs before every line making
    up this element.
    """

    prefix: str = ''
