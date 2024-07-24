from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Iterable, Any, TextIO

from .elements import Element, Start, File, Text, End


class Destination(Protocol):
    def handle(self, elements: Iterable[Element[Any]]) -> None: ...


@dataclass
class Files:
    path: Path | None = None

    def __post_init__(self) -> None:
        if not (self.path is None or self.path.is_dir()):
            raise TypeError(f'not a directory: {self.path}')

    def handle(self, elements: Iterable[Element[Any]]) -> None:
        stream: TextIO | None = None
        path: Path | None = None
        try:
            for element in elements:
                if isinstance(element, Start) and isinstance(e := element.value, File):
                    if path is not None:
                        raise ValueError(f'attempt to open {e.value} before {path} was closed')
                    path = e.value
                    if path.is_absolute():
                        path_to_open = path
                    else:
                        if self.path is None:
                            raise ValueError(f'no directory for {path}')
                        path_to_open = self.path / path
                    stream = path_to_open.open('w')
                elif isinstance(element, Text):
                    if stream is None:
                        raise ValueError(f'no path specified to write {element}')
                    stream.write(element.value)
                elif isinstance(element, End) and isinstance(e := element.value, File):
                    close_path = e.value
                    if close_path != path or stream is None:
                        raise ValueError(f'attempt to close {close_path} when {path} was open')
                    stream.close()
                    stream = path = None
                else:
                    raise TypeError(f"{type(self).__qualname__} can't handle {element}")
        finally:
            if stream is not None:
                stream.close()


class Memory:
    elements: list[Element[Any]]

    def handle(self, elements: Iterable[Element[Any]]) -> None:
        self.elements = list(elements)
