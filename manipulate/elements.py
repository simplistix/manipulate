from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar, Generic, Any

T = TypeVar('T')


@dataclass()
class Element(Generic[T]):
    value: T
    parent: 'Element[Any] | None' = None

    def __str__(self) -> str:
        return f'{type(self).__qualname__}({self.value!r})'


class Start(Element[T]):
    pass


class End(Element[T]):
    pass


class Bytes(Element[bytes]):
    pass


class Text(Element[str]):
    pass


class File(Element[Path]):
    pass
