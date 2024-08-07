import sys
from io import StringIO
from pathlib import Path
from subprocess import run

from testfixtures import compare, generator

from manipulate.elements import Start, File, Text, End
from manipulate.sources import Files, Stream


class TestFiles:

    def test_one(self, tmp_path: Path) -> None:
        path = tmp_path / 'test.txt'
        path.write_text('some text')
        files = Files([path])
        compare(
            files.elements(),
            expected=generator(
                Start(File(path)),
                Text('some text', parent=File(path), line=1, column=1),
                End(File(path)),
            ),
        )

    def test_str(self) -> None:
        compare(str(Files([Path('foo')])), expected="Files")

    def test_repr(self) -> None:
        compare(repr(Files([Path('foo')])), expected="Files(paths=[PosixPath('foo')])")


class TestStream:

    def test_string_io(self) -> None:
        stream = Stream(StringIO('some text'))
        compare(
            stream.elements(),
            expected=generator(Text('some text', line=1, column=1)),
        )

    def test_stdin(self) -> None:
        result = run(
            [
                sys.executable,
                '-c',
                'from manipulate.sources import Stream; import sys; '
                'print(tuple(Stream(sys.stdin).elements()))',
            ],
            check=True,
            input=b'some text',
            capture_output=True,
        )
        compare(
            result.stdout,
            expected=b"(Text(value='some text', parent=None, line=1, column=1, prefix=''),)\n",
        )

    def test_str_stringio(self) -> None:
        compare(str(Stream(StringIO('some text'))), expected='Stream')

    def test_str_stdin(self) -> None:
        compare(str(Stream(sys.stdin)), expected='Stream')

    def test_repr_stringio(self) -> None:
        io = StringIO('some text')
        compare(repr(Stream(io)), expected=f'Stream(stream={io!r})')

    def test_repr_stdin(self) -> None:
        compare(
            repr(Stream(sys.stdin)),
            expected="Stream(stream=<_io.TextIOWrapper name='<stdin>' mode='r' encoding='utf-8'>)",
        )
