from testfixtures import compare

from manipulate.elements import Element, Text


class TestElement:
    def test_repr(self) -> None:
        compare(
            repr(Element[int](13)),
            expected='Element(value=13, parent=None, line=None, column=None)',
        )

    def test_str(self) -> None:
        compare(
            str(Element[int](13)),
            expected='Element(13)',
        )

    def test_str_with_line(self) -> None:
        compare(
            str(Element[int](13, line=1)),
            expected='Element(13) at line 1',
        )

    def test_str_with_line_and_column(self) -> None:
        compare(
            str(Element[int](13, line=1, column=2)),
            expected='Element(13) at line 1, column 2',
        )


class TestText:

    def test_repr(self) -> None:
        compare(
            repr(Text('ABC', line=1, column=2)),
            expected="Text(value='ABC', parent=None, line=1, column=2, prefix='')",
        )

    def test_str_short(self) -> None:
        compare(
            str(Text('ABC')),
            expected="Text('ABC')",
        )

    def test_str_long(self) -> None:
        compare(
            str(Text('A' + 'Z' * 60 + 'C')),
            expected="Text('AZZZZZZZZZZZZZZZZZZZZZZZZ...ZZZZZZZZZZZZZZZZZZZZZZZZC')",
        )

    def test_str_maximal(self) -> None:
        compare(
            str(Text('A' + 'Z' * 60 + 'C', line=1, column=2)),
            expected=(
                "Text('AZZZZZZZZZZZZZZZZZZZZZZZZ...ZZZZZZZZZZZZZZZZZZZZZZZZC')"
                " at line 1, column 2"
            ),
        )
