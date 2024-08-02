from dataclasses import dataclass
from typing import Iterable, Any, TypeAlias, Callable, Type, TypeVar, Generic, Mapping

from .elements import Element, Start, End, Text, File

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


@dataclass
class Classify:
    """
    Classify the text within files as a particular format
    """

    extensions: Mapping[str, Type[Text]]

    def __call__(self, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        type_: Type[Text] | None = None
        for element in Container(File)(elements):
            match element:
                case Start(File(path)):
                    type_ = self.extensions.get(path.suffix)
                    if type_ is None:
                        raise ValueError(f"Unable to classify extension: {path.suffix!r}")
                    yield element
                case Text(value, parent, line, column):
                    if type_ is None:
                        raise ValueError(f'{element} is not within a File()')
                    yield type_(value, parent, line, column)
                case End(File(_)):
                    type_ = None
                    yield element
                case _:
                    yield element
