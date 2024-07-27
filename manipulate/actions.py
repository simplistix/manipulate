from typing import Iterable, Any, TypeAlias, Callable

from .elements import Element

Action: TypeAlias = Callable[[Iterable[Element[Any]]], Iterable[Element[Any]]]
