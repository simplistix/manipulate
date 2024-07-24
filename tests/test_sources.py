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
                Start(File(path)), Text('some text', parents=[File(path)]), End(File(path))
            ),
        )


class TestStream:

    def test_string_io(self) -> None:
        stream = Stream(StringIO('some text'))
        compare(
            stream.elements(),
            expected=generator(Text('some text')),
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
        compare(result.stdout, expected=b"(Text(value='some text', parents=[]),)\n")
