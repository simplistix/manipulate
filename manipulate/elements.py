from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar, Generic, Any


T = TypeVar('T')


@dataclass
class Element(Generic[T]):
    value: T
    parent: 'Element[Any] | None' = None
    line: int | None = None
    column: int | None = None

    def _value_repr(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        text = f'{type(self).__qualname__}({self._value_repr()})'
        if self.line:
            text += f' at line {self.line}'
        if self.column:
            text += f', column {self.column}'
        return text


class Start(Element[T]):
    pass


class End(Element[T]):
    pass


class File(Element[Path]):
    pass


class Bytes(Element[bytes]):
    pass


MAX_TEXT_STR_SIZE = 50
TEXT_STR_ABBREVIATED_SIZE = int(MAX_TEXT_STR_SIZE / 2)


@dataclass
class Text(Element[str]):
    """
    A textual element. If it is embedded within another textual element or file,
    it may have a prefix specified, if that prefix occurs before every line making
    up this element.
    """

    prefix: str = ''

    def _value_repr(self) -> str:
        text = self.value
        if len(text) > MAX_TEXT_STR_SIZE:
            text = text[:TEXT_STR_ABBREVIATED_SIZE] + '...' + text[-TEXT_STR_ABBREVIATED_SIZE:]
        return repr(text)
