from dataclasses import dataclass
from typing import Any, Protocol


class Row(dict[str, Any]):
    pass


@dataclass
class Table:
    columns: list[str] | None
    rows: list[Row]


class Format(Protocol):

    def parse(self, text: str) -> Table: ...

    def render(self, table: Table) -> str: ...
