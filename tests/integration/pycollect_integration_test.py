import os
import re

import pytest

from pycollect.pycollect import PythonFileCollector


@pytest.mark.parametrize("enable_regex_patterns", [False, True])
def test_example_module_with_default_configurations(enable_regex_patterns: bool):
    # given
    python_file_collector = PythonFileCollector(
        enable_regex_patterns=enable_regex_patterns
    )
    search_path = os.path.join(
        re.sub(
            "{0}\\{1}(?:.(?!{0}\\{1}))+$".format("integration", os.sep), "", __file__
        ),
        "resources",
        "example_module",
    )
    expected_findings = (
        os.path.join(search_path, "__init__.py"),
        os.path.join(search_path, "foo.py"),
        os.path.join(search_path, "bar.py"),
        os.path.join(search_path, "foo", "__init__.py"),
        os.path.join(search_path, "foo", "foo.py"),
        os.path.join(search_path, "bar", "__init__.py"),
    )

    # when
    collected_files = python_file_collector.collect_python_files(
        search_path=search_path
    )

    # then
    assert collected_files
    collected_filepaths = (file.path for file in collected_files)
    assert all(filepath in expected_findings for filepath in collected_filepaths)
