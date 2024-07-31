from pathlib import Path

from testfixtures import compare, generator, ShouldRaise

from manipulate.actions import Parse, Render
from manipulate.elements import Text, Start, Element, End, File
from manipulate.sources import Files
from manipulate.tabular import Format, Table, Row


class DummyFormat(Format):

    def __init__(self, table: Table):
        self.table = table

    def parse(self, text: str) -> Table:
        compare(text, expected='x')
        return self.table

    def render(self, table: Table) -> str:
        compare(table, expected=self.table)
        return 'z'


class TestParse:

    def test_minimal(self) -> None:
        table = Table(columns=['x'], rows=[Row({'x': 1})])

        parse = Parse(DummyFormat(table))
        compare(
            parse([Text('x')]),
            expected=generator(
                Start(table),
                Element(Row({'x': 1})),
                End(table),
            ),
        )

    def test_pass_through_unhandled_elements(self, tmp_path: Path) -> None:
        path = tmp_path / 'test.txt'
        path.write_text('x')
        files = Files([path])
        table = Table(columns=['x'], rows=[Row({'x': 1})])

        parse = Parse(DummyFormat(table))
        compare(
            parse(files.elements()),
            expected=generator(
                Start(File(path)), Start(table), Element(Row({'x': 1})), End(table), End(File(path))
            ),
        )


class TestRender:

    def test_minimal(self) -> None:
        table = Table(columns=['x'], rows=[Row({'x': 1})])
        render = Render(DummyFormat(table))
        compare(
            render(
                [
                    Start(table),
                    Element(Row({'x': 1})),
                    End(table),
                ]
            ),
            expected=generator(
                Text('z'),
            ),
        )

    def test_with_columns(self) -> None:
        table = Table(columns=['x'], rows=[Row({'x': 1})])
        render = Render(DummyFormat(table))
        compare(
            render(
                [
                    Start(table),
                    Element(Row({'x': 1})),
                    End(table),
                ]
            ),
            expected=generator(
                Text('z'),
            ),
        )

    def test_rows_modified(self) -> None:
        render = Render(
            DummyFormat(Table(columns=['x', 'y', 'z'], rows=[Row({'y': 1}), Row({'z': 2})]))
        )
        table = Table(columns=['x', 'y', 'z'], rows=[Row({'x': 1})])
        compare(
            render(
                [
                    Start(table),
                    Element(Row({'y': 1})),
                    Element(Row({'z': 2})),
                    End(table),
                ]
            ),
            expected=generator(
                Text('z'),
            ),
        )

    def test_pass_through_unhandled_elements(self) -> None:
        row = Row({'x': 1})
        render = Render(DummyFormat(Table(columns=['x'], rows=[row])))
        table = Table(columns=['x'], rows=[row])
        compare(
            render(
                [
                    Start(File(Path('x'))),
                    Start(table),
                    Element(row),
                    End(table),
                    End(File(Path('x'))),
                ]
            ),
            expected=generator(
                Start(File(Path('x'))),
                Text('z'),
                End(File(Path('x'))),
            ),
        )

    def test_double_start(self) -> None:
        table1 = Table(columns=['x'], rows=[Row({'x': 1})])
        table2 = Table(columns=['x'], rows=[Row({'x': 2})])
        render = Render(DummyFormat(table1))
        with ShouldRaise(
            ValueError(
                "nested tables not supported, "
                "Start(value=Table(columns=['x'], rows=[{'x': 2}], types_location=None)) before "
                "End(Table(columns=['x'], rows=[], types_location=None)) ended"
            )
        ):
            next(iter(render([Start(table1), Start(table2)])))

    def test_end_without_start(self) -> None:
        table = Table(columns=['x'], rows=[Row({'x': 1})])
        render = Render(DummyFormat(table))
        with ShouldRaise(
            ValueError(
                "End(value=Table(columns=['x'], rows=[{'x': 1}], types_location=None)) "
                "before Start(Table(columns=['x'], rows=[{'x': 1}], types_location=None))"
            )
        ):
            next(iter(render([End(table)])))

    def test_end_wrong_table(self) -> None:
        table1 = Table(columns=['x'], rows=[Row({'x': 1})])
        table2 = Table(columns=['x'], rows=[Row({'x': 2})])
        render = Render(DummyFormat(table1))
        with ShouldRaise(
            ValueError(
                "End(value=Table(columns=['x'], rows=[{'x': 2}], types_location=None)), "
                "expected End(Table(columns=['x'], rows=[{'x': 1}], types_location=None))"
            )
        ):
            next(iter(render([Start(table1), End(table2)])))
