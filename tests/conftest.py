from pathlib import Path

import pytest
from testfixtures import TempDirectory


@pytest.fixture()
def tempdir(tmp_path: Path) -> TempDirectory:
    return TempDirectory(tmp_path, encoding='utf-8')
