from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Iterable, Any, IO

from .elements import Element, Start, File, Text, End


class Source(Protocol):
    def elements(self) -> Iterable[Element[Any]]: ...


@dataclass
class Files:
    paths: list[Path]

    def elements(self) -> Iterable[Start[File] | Text | End[File]]:
        for path in self.paths:
            file = File(path)
            yield Start(file)
            yield Text(path.read_text(), parents=[file])
            yield End(file)

    def __str__(self) -> str:
        return type(self).__qualname__


@dataclass
class Stream:
    stream: IO[str]

    def elements(self) -> Iterable[Text]:
        return [Text(self.stream.read())]

    def __str__(self) -> str:
        return type(self).__qualname__


class Memory:
    def __init__(self, *elements: Element[Any]) -> None:
        self._elements = elements

    def elements(self) -> Iterable[Element[Any]]:
        yield from self._elements
