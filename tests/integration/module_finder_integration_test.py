import os
import sys

from pycollect import find_module_name
from tests import resources
from tests.resources.example_module.foo import foo

sys.path.insert(0, os.path.dirname(resources.__file__))


def test_find_outermost_module_name():
    """
    This test intents to ensure that the utility function `find_module_name` will
    find the correct outermost module name for a given filepath by default
    """
    # given
    filepath = foo.__file__
    expected_module_name = "tests.resources.example_module.foo.foo"

    # when
    module_name = find_module_name(filepath)

    # then
    assert module_name == expected_module_name


def test_find_innermost_module_name():
    """
    This test intents to ensure that the utility function `find_module_name` will
    find the correct innermost module name for a given filepath when parameter
    `innermost=True`
    """
    # given
    filepath = foo.__file__
    expected_module_name = "example_module.foo.foo"

    # when
    module_name = find_module_name(filepath, innermost=True)

    # then
    assert module_name == expected_module_name


def test_find_nonexistent_module_name():
    """
    This test intents to ensure that the utility function `find_module_name` will
    return None for files it can not attribute a module name
    """
    # given
    root_dir = "usr" if os.name != "nt" else "C:"
    filepath = os.path.join(os.sep, root_dir + os.sep, "random", "path", "script.py")

    # when
    module_name = find_module_name(filepath)

    # then
    assert module_name is None
