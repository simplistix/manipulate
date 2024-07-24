from typing import Iterable, Any, TypeAlias, Callable

from .elements import Element

Action: TypeAlias = Callable[[Iterable[Any]], Iterable[Element[Any]]]
