"""
This test covers a fix for a bug first reported in
https://github.com/allrod5/pycollect/issues/1

In version 0.2.2 the function `find_module_name` would sometimes fail to find the module
name of a file in Windows due to the implementation being case sensitive while Windows
paths are case insensitive.

This bug was fixed in version 0.2.3
"""
import os
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from pycollect import find_module_name


@pytest.mark.skipif(os.name != "nt", reason="Test exclusively meant for Windows")
def test_windows_case_insensitivity(mocker: MockFixture):
    # given
    mocked_pythonpath = [Path(r"d:\a\package")]
    mocker.patch("pycollect.module_finder.sys.path", mocked_pythonpath)
    filepath = Path(r"D:\a\package\module.py")
    expected_module_name = "module"

    # when
    module_name = find_module_name(filepath)

    # then
    assert module_name == expected_module_name
