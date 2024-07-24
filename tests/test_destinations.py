from pathlib import Path

from testfixtures import generator, compare, TempDirectory, ShouldRaise

from manipulate.destinations import Memory, Files
from manipulate.elements import Start, File, Text, End, Element


class TestMemory:

    def test_it(self) -> None:
        memory = Memory()
        f = File(Path('foo.txt'))
        t = Text('some text')
        memory.handle(generator(Start(f), t, End(f)))
        compare(memory.elements, strict=True, expected=[Start(f), t, End(f)])


class TestFiles:

    def test_minimal(self, tempdir: TempDirectory) -> None:
        files = Files()
        source = File(tempdir / 'foo.txt')
        files.handle(generator(Start(source)))
        tempdir.compare(['foo.txt'])
        compare(tempdir.read('foo.txt'), expected='')

    def test_multiple_files(self, tempdir: TempDirectory) -> None:
        files = Files()
        file1 = File(tempdir / 'foo.txt')
        file2 = File(tempdir / 'bar.txt')
        files.handle(
            generator(
                Start(file1),
                Text('some text'),
                End(file1),
                Start(file2),
                Text('other'),
                Text(' text'),
                End(file2),
            )
        )
        tempdir.compare(['foo.txt', 'bar.txt'])
        compare(tempdir.read('foo.txt'), expected='some text')
        compare(tempdir.read('bar.txt'), expected='other text')

    def test_non_text_inside_file_element(self, tempdir: TempDirectory) -> None:
        files = Files()
        f = File(tempdir / 'foo.txt')
        with ShouldRaise(TypeError("Files can't handle Element(value=1, parents=[])")):
            files.handle(generator(Start(f), Element[int](1), End(f)))
        tempdir.compare(['foo.txt'])
        compare(tempdir.read('foo.txt'), expected='')

    def test_text_before_element(self) -> None:
        files = Files()
        with ShouldRaise(
            ValueError("no path specified to write Text(value='some text', parents=[])")
        ):
            files.handle(generator(Text('some text')))

    def test_close_wrong_path(self, tempdir: TempDirectory) -> None:
        files = Files()
        p1 = tempdir / '1.txt'
        p2 = tempdir / '2.txt'
        with ShouldRaise(ValueError(f'attempt to close {p2} when {p1} was open')):
            files.handle(generator(Start(File(p1)), End(File(p2))))
        tempdir.compare(['1.txt'])
        compare(tempdir.read('1.txt'), expected='')

    def test_double_open(self, tempdir: TempDirectory) -> None:
        files = Files()
        p1 = tempdir / '1.txt'
        p2 = tempdir / '2.txt'
        with ShouldRaise(ValueError(f'attempt to open {p2} before {p1} was closed')):
            files.handle(generator(Start(File(p1)), Start(File(p2))))
        tempdir.compare(['1.txt'])
        compare(tempdir.read('1.txt'), expected='')

    def test_close_before_open(self) -> None:
        files = Files()
        with ShouldRaise(ValueError('attempt to close foo.txt when None was open')):
            files.handle(generator(End(File(Path('foo.txt')))))

    def test_path_is_not_a_directory(self, tmp_path: Path) -> None:
        file_path = tmp_path / 'foo.txt'
        with ShouldRaise(TypeError(f'not a directory: {file_path}')):
            Files(file_path)

    def test_write_to_supplied_directory(self, tempdir: TempDirectory) -> None:
        directory = (tempdir / 'out')
        directory.mkdir()
        files = Files(directory)
        file = File(Path('foo.txt'))
        files.handle(generator(Start(file), Text('text'), End(file)))
        tempdir.compare(['out/', 'out/foo.txt'])
        compare(tempdir.read('out/foo.txt'), expected='text')

    def test_absolute_path_preferred_to_supplied_directory(self, tempdir: TempDirectory) -> None:
        directory = (tempdir / 'out')
        directory.mkdir()
        files = Files(directory)
        source = File(tempdir / 'foo.txt')
        files.handle(generator(Start(source)))
        tempdir.compare(['foo.txt', 'out/'])
        compare(tempdir.read('foo.txt'), expected='')

    def test_relative_but_no_directory_specified(self) -> None:
        files = Files()
        file = File(Path('foo.txt'))
        with ShouldRaise(ValueError(f'no directory for foo.txt')):
            files.handle(generator(Start(file), Text('text'), End(file)))
