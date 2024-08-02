from pathlib import Path
from typing import Iterable, Any

from testfixtures import compare, generator, ShouldRaise

from manipulate.actions import Classify
from manipulate.elements import Text, Start, Element, End, File


def should_raise_on_iter(elements: Iterable[Element[Any]], expected: Exception) -> None:
    with ShouldRaise(expected):
        next(iter(elements))


class TestClassify:

    def test_single(self) -> None:
        class MyText(Text):
            pass

        file = File(Path('foo.bar'))
        classify = Classify({'.bar': MyText})
        compare(
            classify([Start(file), Text('content', parent=file, line=1, column=2), End(file)]),
            expected=generator(
                Start(file),
                MyText('content', parent=file, line=1, column=2),
                End(file),
            ),
        )

    def test_multiple(self) -> None:
        class BarText(Text):
            pass

        class BazText(Text):
            pass

        bar_file = File(Path('foo.bar'))
        baz_file = File(Path('foo.baz'))
        classify = Classify({'.bar': BarText, '.baz': BazText})
        compare(
            classify(
                [
                    Start(bar_file),
                    Text('content', parent=bar_file, line=1, column=1),
                    End(bar_file),
                    Start(baz_file),
                    Text('line 1\n', parent=baz_file, line=1, column=1),
                    Text('line 2\n', parent=baz_file, line=2, column=1),
                    End(baz_file),
                ]
            ),
            expected=generator(
                Start(bar_file),
                BarText('content', parent=bar_file, line=1, column=1),
                End(bar_file),
                Start(baz_file),
                BazText('line 1\n', parent=baz_file, line=1, column=1),
                BazText('line 2\n', parent=baz_file, line=2, column=1),
                End(baz_file),
            ),
        )

    def test_unknown_file_type(self) -> None:
        classify = Classify({})
        should_raise_on_iter(
            classify([Start(File(Path('foo.bar')))]),
            ValueError("Unable to classify extension: '.bar'"),
        )

    def test_outside_file(self) -> None:
        classify = Classify({})
        should_raise_on_iter(
            classify([Text('x')]),
            ValueError("Text('x') is not within a File()"),
        )

    def test_pass_through_others(self) -> None:
        classify = Classify({})
        compare(classify([Element(1)]), expected=generator(Element(1)))
