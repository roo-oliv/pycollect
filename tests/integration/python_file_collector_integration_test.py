import os
import re
from typing import List

import pytest

from pycollect.python_file_collector import PythonFileCollector


@pytest.fixture
def search_path() -> str:
    return os.path.join(
        re.sub(
            "{0}\\{1}(?:.(?!{0}\\{1}))+$".format("integration", os.sep), "", __file__
        ),
        "resources",
        "example_module",
    )


@pytest.mark.parametrize("enable_regex_patterns", [False, True])
@pytest.mark.parametrize(
    "expected_files",
    [
        [
            ["__init__.py"],
            ["fun.py"],
            ["foo.py"],
            ["bar.py"],
            ["foo", "__init__.py"],
            ["foo", "foo.py"],
            ["bar", "__init__.py"],
            ["bar", "misc", "pkg", "pkg.py"],
            ["qux", "qux.py"],
        ]
    ],
)
def test_example_module_with_default_configurations(
    enable_regex_patterns: bool, expected_files: List[List[str]], search_path: str
):
    # given
    python_file_collector = PythonFileCollector(
        use_regex_patterns=enable_regex_patterns
    )
    expected_findings = {
        os.path.join(search_path, *expected_file) for expected_file in expected_files
    }

    # when
    collected_files = python_file_collector.collect(search_path=search_path)

    # then
    assert collected_files
    collected_filepaths = {file.path for file in collected_files}
    assert collected_filepaths == expected_findings


@pytest.mark.parametrize(
    "enable_regex_patterns, additional_file_exclusion_patterns, expected_files",
    [
        (
            False,
            ["f*.py"],
            [
                ["__init__.py"],
                ["bar.py"],
                ["foo", "__init__.py"],
                ["bar", "__init__.py"],
                ["bar", "misc", "pkg", "pkg.py"],
                ["qux", "qux.py"],
            ],
        ),
        (
            True,
            [r"f.*\.py(?!.)"],
            [
                ["__init__.py"],
                ["bar.py"],
                ["foo", "__init__.py"],
                ["bar", "__init__.py"],
                ["bar", "misc", "pkg", "pkg.py"],
                ["qux", "qux.py"],
            ],
        ),
        (False, ["!f*.py"], [["fun.py"], ["foo.py"], ["foo", "foo.py"]]),
    ],
)
def test_example_module_with_additional_file_exclusion_patterns(
    enable_regex_patterns: bool,
    additional_file_exclusion_patterns: List[str],
    expected_files: List[List[str]],
    search_path: str,
):
    # given
    python_file_collector = PythonFileCollector(
        use_regex_patterns=enable_regex_patterns,
        additional_file_exclusion_patterns=additional_file_exclusion_patterns,
    )
    expected_findings = {
        os.path.join(search_path, *expected_file) for expected_file in expected_files
    }

    # when
    collected_files = python_file_collector.collect(search_path=search_path)

    # then
    assert collected_files
    collected_filepaths = {file.path for file in collected_files}
    assert collected_filepaths == expected_findings


@pytest.mark.parametrize(
    "enable_regex_patterns, additional_dir_exclusion_patterns",
    [
        (False, ["fo*", "bar", "*ux"]),
        (True, [r"^fo.*", r"^bar(?!.)", r".*ux(?!.)"]),
        (False, ["!bar", "bar"]),
    ],
)
@pytest.mark.parametrize(
    "expected_files", [[["__init__.py"], ["fun.py"], ["foo.py"], ["bar.py"]]]
)
def test_example_module_with_additional_dir_exclusion_patterns(
    enable_regex_patterns: bool,
    additional_dir_exclusion_patterns: List[str],
    expected_files: List[List[str]],
    search_path: str,
):
    # given
    python_file_collector = PythonFileCollector(
        use_regex_patterns=enable_regex_patterns,
        additional_dir_exclusion_patterns=additional_dir_exclusion_patterns,
    )
    expected_findings = {
        os.path.join(search_path, *expected_file) for expected_file in expected_files
    }

    # when
    collected_files = python_file_collector.collect(search_path=search_path)

    # then
    assert collected_files
    collected_filepaths = {file.path for file in collected_files}
    assert collected_filepaths == expected_findings
