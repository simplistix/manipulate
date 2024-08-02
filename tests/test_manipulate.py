from dataclasses import dataclass
from typing import Iterable, Any

import pytest
from testfixtures import compare, ShouldRaise

from manipulate import manipulate
from manipulate.destinations import Memory as Destination
from manipulate.elements import Element, Text
from manipulate.sources import Memory as Source


def test_no_actions() -> None:
    dest = Destination()
    manipulate(
        Source(Text('one'), Text('one'), Text('one')),
        (),
        dest,
    )
    compare(dest.elements, expected=[Text('one'), Text('one'), Text('one')])


def test_single_action() -> None:
    def parse(texts: Iterable[Any]) -> Iterable[Element[int]]:
        for text in texts:
            yield Element(int(text.value))

    dest = Destination()
    manipulate(
        Source(Text('1'), Text('2'), Text('3')),
        (parse,),
        dest,
    )
    compare(dest.elements, expected=[Element[int](1), Element[int](2), Element[int](3)])


@pytest.mark.parametrize(
    'parse1_bad_value, parse2_bad_value, expected_note',
    [
        (1, 0, "Parse(name='first', bad_value=1) on Element(1)"),
        (2, 0, "Parse(name='first', bad_value=2) on Element(1) -> Element(2)"),
        (3, 0, "Parse(name='first', bad_value=3) on Element(1) -> Element(2) -> Element(3)"),
        (0, 1, "Parse(name='second', bad_value=1) on Element(1)"),
        (0, 2, "Parse(name='second', bad_value=2) on Element(1) -> Element(2)"),
        (0, 3, "Parse(name='second', bad_value=3) on Element(1) -> Element(2) -> Element(3)"),
    ],
)
def test_exception_in_action(
    parse1_bad_value: int, parse2_bad_value: int, expected_note: str
) -> None:

    @dataclass
    class Parse:
        name: str
        bad_value: int

        def __call__(self, elements: Iterable[Any]) -> Iterable[Element[Any]]:
            for element in elements:
                match element:
                    case Element(self.bad_value):
                        raise Exception('boom!')
                    case _:
                        yield element

    e1 = Element(1)
    e2 = Element(2, parent=e1)
    e3 = Element(3, parent=e2)

    expected_exception = Exception('boom!')
    expected_exception.add_note("Performing test_exception_in_action.<locals>." + expected_note)

    with ShouldRaise(expected_exception):
        manipulate(
            Source(e1, e2, e3),
            [Parse('first', parse1_bad_value), Parse('second', parse2_bad_value)],
            Destination(),
        )
