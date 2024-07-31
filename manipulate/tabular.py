import csv
import re
from csv import DictReader
from dataclasses import dataclass
from enum import Enum, auto
from io import StringIO
from typing import Any, Protocol, Sequence, Callable, Iterable


class Row(dict[str, Any]):
    pass


class TypesLocation(Enum):
    #: The types are located in parentheses, after the column name, in the
    #: row containing the column names.
    HEADER = auto()
    #: The types are located in their own row.
    ROW = auto()
    #: Guess from the above two options when parsing. An exception should be raised
    #: if this is encountered when rendering.
    GUESS = auto()


@dataclass
class Table:
    columns: Sequence[str]
    rows: list[Row]
    types_location: TypesLocation | None = None


@dataclass
class Format:
    header_type_pattern = re.compile(r'([^ (]+) *\((.+)\) *')

    columns: Sequence[str] | None = None
    types_location: TypesLocation | None = None

    def lex(self, text: str) -> Iterable[Iterable[str]]: ...

    def parse(self, text: str) -> Table:
        rows = []
        columns: list[str] | None = self.columns
        types_row_handled = self.types_location is not TypesLocation.ROW
        types_row_next = False
        for parts in self.lex(text):

            if columns is not None and not types_row_handled:
                types_row_next = True

            if columns is None:
                columns = []
                type_names = {}
                for c in parts:
                    if (
                            self.types_location is TypesLocation.HEADER
                            and (match := self.header_type_pattern.match(c))
                    ):
                        column, t = match.groups()
                        type_names[column] = t
                    else:
                        column = c
                    columns.append(column)
                # self._resolve_type_names(type_names)
            elif types_row_next:
                # self._resolve_type_names(type_names={c: t for c, t in zip(columns, parts)})
                types_row_handled = True
                types_row_next = False
            else:
                row = Row()
                for column, value in zip(columns, parts):
                    # handler = self.column_parse.get(column)
                    # if handler is not None:
                    #     value = handler(value)
                    row[column] = value
                rows.append(row)
        if not columns:
            raise ValueError('No columns specified or found in source')
        return Table(columns, rows, self.types_location)

    def render(self, table: Table) -> str: ...


class CSV(Format):

    def lex(self, text: str) -> Iterable[Iterable[str]]:
        return csv.reader(StringIO(text))

    def render(self, table: Table) -> str:
        return ''
