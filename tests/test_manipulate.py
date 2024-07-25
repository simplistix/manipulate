from typing import Iterable

from testfixtures import compare

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
    def parse(texts: Iterable[Text]) -> Iterable[Element[int]]:
        for text in texts:
            yield Element(int(text.value))

    dest = Destination()
    manipulate(
        Source(Text('1'), Text('2'), Text('3')),
        (parse,),
        dest,
    )
    compare(dest.elements, expected=[Element[int](1), Element[int](2), Element[int](3)])
