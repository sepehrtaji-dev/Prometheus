"""Regression tests for recursive glob patterns matching root-level files."""

from prometheus.coding.tools import _glob_matches


def test_double_star_slash_matches_root_level_file():
    assert _glob_matches("export.py", "**/*.py")
    assert _glob_matches("export.py", "**/export.py")
    assert _glob_matches("README.md", "**/*")


def test_double_star_slash_still_matches_nested_files():
    assert _glob_matches("tests/test_export.py", "**/*.py")
    assert _glob_matches("src/calc.py", "src/**/*.py")


def test_glob_without_double_star_keeps_fnmatch_semantics():
    assert _glob_matches("src/calc.py", "*.py")
    assert not _glob_matches("export.txt", "**/*.py")
