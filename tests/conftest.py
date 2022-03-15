from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def testing_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("file.txt")
    Path(filename).touch()
    yield str(filename)
