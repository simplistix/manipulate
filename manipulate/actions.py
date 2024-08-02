from dataclasses import dataclass
from typing import Iterable, Any, TypeAlias, Callable, Type, TypeVar, Generic

from .elements import Element, Start, End

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
