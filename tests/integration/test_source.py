""" Verify that the library is usable as an external source tree.

"""
from pathlib import Path
from subprocess import run

import pytest


@pytest.mark.parametrize("key", [
    "LIBRARY_FETCH_DIR",  # FetchContent
    "LIBRARY_SOURCE_DIR",  # add_subdirectory()
])
def test_lib(build, build_dir, gtest, key):
    """ Test the library as part of an application.

    """
    defs = {
        key: Path.cwd(),
        "GTEST_VERSION": gtest[1],
    }
    source_dir = Path(__file__).parent / "src"
    build(source_dir, build_dir, defs)
    exe = build_dir / "test_lib"
    process = run([str(exe)], capture_output=True)
    stderr = process.stderr.decode().splitlines()  # for debugging
    assert process.returncode == 0
    return


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
