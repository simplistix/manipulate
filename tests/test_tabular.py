from typing import Sequence, Any

from testfixtures import compare, ShouldRaise

from manipulate.tabular import Format, Table, Row, CSV, TypesLocation


def check_parse(format: Format, lines: Sequence[str], expected: Table) -> None:
    compare(expected, actual=format.parse(''.join(lines)))


class TestCSV:

    def test_parse_minimal(self) -> None:
        check_parse(
            CSV(),
            lines=(
                'x,y\n',
                '1,foo\n',
            ),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': '1', 'y': 'foo'})],
            ),
        )

    def test_parse_minimal_no_columns(self) -> None:
        check_parse(
            CSV(),
            lines=('1,foo\n',),
            expected=Table(
                columns=['1', 'foo'],
                rows=[],
            ),
        )

    def test_parse_with_specified_columns(self) -> None:
        check_parse(
            CSV(columns=['x', 'y']),
            lines=('1,foo\n',),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': '1', 'y': 'foo'})],
            ),
        )

    def test_parse_no_rows(self) -> None:
        check_parse(
            CSV(columns=['x', 'y']),
            lines=(),
            expected=Table(
                columns=['x', 'y'],
                rows=[],
            ),
        )

    def test_parse_empty(self) -> None:
        check_parse(
            CSV(columns=['x', 'y']),
            lines=('',),
            expected=Table(
                columns=['x', 'y'],
                rows=[],
            ),
        )

    def test_parse_no_rows_no_columns(self) -> None:
        with ShouldRaise(ValueError('No columns specified or found in source')):
            CSV().parse('')

    def test_types_in_header(self) -> None:
        check_parse(
            CSV(types_location=TypesLocation.HEADER),
            lines=(
                'x (float),y (str)\n',
                '1,foo\n',
            ),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': 1.0, 'y': 'foo'})],
                types_location=TypesLocation.HEADER
            ),
        )

    def test_types_in_row(self) -> None:
        check_parse(
            CSV(types_location=TypesLocation.ROW),
            lines=(
                'x,y\n',
                'float,str\n'
                '1,foo\n',
            ),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': 1.0, 'y': 'foo'})],
            ),
        )

    def test_guess_types_in_header(self) -> None:
        check_parse(
            CSV(types_location=TypesLocation.GUESS),
            lines=(
                'x (float),y (str)\n',
                '1,foo\n',
            ),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': 1.0, 'y': 'foo'})],
                types_location=TypesLocation.HEADER
            ),
        )

    def test_guess_types_in_row(self) -> None:
        # can't actually tell with csv
        check_parse(
            CSV(types_location=TypesLocation.GUESS),
            lines=(
                'x,y\n',
                'float,str\n'
                '1,foo\n',
            ),
            expected=Table(
                columns=['x', 'y'],
                rows=[Row({'x': 'float', 'y': 'str'}), Row({'x': 1.0, 'y': 'foo'})],
            ),
        )

    def test_types_in_header_but_no_guess(self) -> None:
        check_parse(
            CSV(types_location=None),
            lines=(
                'x (float),y (str)\n',
                '1,foo\n',
            ),
            expected=Table(
                columns=['x (float)', 'y (str)'],
                rows=[Row({'x (float)': '1', 'y (str)': 'foo'})],
            ),
        )
    #
    # def test_render_minimal(self) -> None:
    #     format_ = CSVFormat()
    #     actual = format_.render([
    #         {'x': 1, 'y': 'foo'},
    #     ])
    #     expected = "".join((
    #         'x,y\r\n',
    #         '1,foo\r\n'
    #     ))
    #     compare(expected=expected, actual=actual, show_whitespace=True)
    #
    # def test_render_empty(self) -> None:
    #     format_ = CSVFormat(types_location=ROW)
    #     actual = format_.render([])
    #     compare(
    #         actual,
    #         expected=dedent("")
    #     )
    #
    # def test_render_with_reference(self) -> None:
    #     format_ = CSVFormat()
    #     ref = [{'z': 0, 'y': 0, 'x': 0}]
    #     actual = format_.render([{'x': 1, 'y': 'foo'}], ref)
    #     expected = "".join((
    #         'z,y,x\r\n',
    #         'None,foo,1\r\n'
    #     ))
    #     compare(expected=expected, actual=actual, show_whitespace=True)
    #
    # def test_render_with_empty_reference(self) -> None:
    #     format_ = CSVFormat()
    #     actual = format_.render([{'x': 1, 'y': 'foo'}], ref=[])
    #     expected = "".join((
    #         'x,y\r\n',
    #         '1,foo\r\n'
    #     ))
    #     compare(expected=expected, actual=actual, show_whitespace=True)
    #
    # def test_roundtrip_minimal(self) -> None:
    #     source = "".join((
    #         'x,y\r\n',
    #         '1,foo\r\n'
    #     ))
    #     format_ = CSVFormat()
    #     parsed = format_.parse(source)
    #     compare(parsed, expected=[
    #         {'x': 1, 'y': 'foo'},
    #     ])
    #     compare(expected=source, actual=format_.render(parsed), show_whitespace=True)
    #
    # def test_roundtrip_whitespace_in_values(self) -> None:
    #     source = "".join((
    #         'x,y\r\n',
    #         '1,foo\r\n',
    #         "2,' bar'\r\n",
    #         "3,'baz '\r\n",
    #     ))
    #     format_ = CSVFormat()
    #     parsed = format_.parse(source)
    #     compare(parsed, expected=[
    #         {'x': 1, 'y': 'foo'},
    #         {'x': 2, 'y': ' bar'},
    #         {'x': 3, 'y': 'baz '},
    #     ])
    #     rendered = format_.render(parsed)
    #     compare(expected=source, actual=rendered, show_whitespace=True)
    #
    # def test_roundtrip_maximal_types_in_row(self) -> None:
    #     source = "".join((
    #         'start,time of day,end\r\n',
    #         'date,,date\r\n',
    #         '27 May 04,09:00,01 Jun 04\r\n'
    #         '02 Jun 04,11:02,02 Jul 04\r\n'
    #     ))
    #     format_ = CSVFormat(
    #         type_parse={'date': lambda text: datetime.strptime(text, '%d %b %y').date()},
    #         column_parse={'time of day': lambda text: datetime.strptime(text, '%H:%M').time()},
    #         type_render={date: lambda d: d.strftime('%d %b %y')},
    #         type_names={date: 'date', time: None},
    #         column_render={'time of day': lambda t: t.strftime('%H:%M')},
    #         types_location=ROW,
    #     )
    #     parsed = format_.parse(source)
    #     compare(parsed, expected=[
    #         {'start': date(2004, 5, 27), 'time of day': time(9, 0), 'end': date(2004, 6, 1)},
    #         {'start': date(2004, 6, 2), 'time of day': time(11, 2), 'end': date(2004, 7, 2)},
    #     ])
    #     rendered = format_.render(parsed)
    #     compare(expected=source, actual=rendered, show_whitespace=True)
    #
    # def test_roundtrip_maximal_types_in_header(self) -> None:
    #     source = "".join((
    #         'start (date),time of day,end (date)\r\n',
    #         '27 May 04,09:00,01 Jun 04\r\n'
    #         '02 Jun 04,11:02,02 Jul 04\r\n'
    #     ))
    #     format_ = CSVFormat(
    #         type_parse={'date': lambda text: datetime.strptime(text, '%d %b %y').date()},
    #         column_parse={'time of day': lambda text: datetime.strptime(text, '%H:%M').time()},
    #         type_render={date: lambda d: d.strftime('%d %b %y')},
    #         type_names={date: 'date', time: None},
    #         column_render={'time of day': lambda t: t.strftime('%H:%M')},
    #         types_location=HEADER,
    #     )
    #     parsed = format_.parse(source)
    #     compare(parsed, expected=[
    #         {'start': date(2004, 5, 27), 'time of day': time(9, 0), 'end': date(2004, 6, 1)},
    #         {'start': date(2004, 6, 2), 'time of day': time(11, 2), 'end': date(2004, 7, 2)},
    #     ])
    #     rendered = format_.render(parsed)
    #     compare(expected=source, actual=rendered, show_whitespace=True)
