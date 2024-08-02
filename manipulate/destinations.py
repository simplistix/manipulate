from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Iterable, Any, TextIO

from .actions import Container
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
        try:
            for element in Container(File)(elements):
                match element:
                    case Start(File(start_path)):
                        path = start_path
                        if path.is_absolute():
                            path_to_open = path
                        else:
                            if self.path is None:
                                raise ValueError(f'no directory for {path}')
                            path_to_open = self.path / path
                        stream = path_to_open.open('w')
                    case Text(text):
                        if stream is None:
                            raise ValueError(f'no path specified to write {element}')
                        stream.write(text)
                    case End(File(_)):
                        assert stream is not None
                        stream.close()
                        stream = None
                    case _:
                        raise TypeError(f"{type(self).__qualname__} can't handle {element}")
        finally:
            if stream is not None:
                stream.close()


class Memory:
    elements: list[Element[Any]]

    def handle(self, elements: Iterable[Element[Any]]) -> None:
        self.elements = list(elements)
