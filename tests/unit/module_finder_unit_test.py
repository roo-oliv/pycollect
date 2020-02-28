import os
import sys
from pathlib import Path

from pycollect import find_module_name


def build_path(*paths: str) -> str:
    root_dir = "usr" if os.name != "nt" else "C:"
    return os.path.join(os.sep, root_dir + os.sep, *paths)


def join_paths(*paths: str) -> str:
    return os.path.join(*paths)


def parent_path(path: str) -> str:
    return str(Path(path).parent)


def test_find_outermost_module_name():
    """
    This test intents to ensure that the utility function `find_module_name` will
    find the correct outermost module name for a given filepath by default
    """
    # given
    package_path = build_path("test_find_outermost_module_name", "some_package")
    inner_module_path = join_paths(package_path, "inner_module")
    filepath = join_paths(inner_module_path, "foo", "bar.py")
    sys.path.append(parent_path(package_path))
    sys.path.append(parent_path(inner_module_path))
    expected_module_name = "some_package.inner_module.foo.bar"

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
    package_path = build_path("test_find_outermost_module_name", "some_package")
    inner_module_path = join_paths(package_path, "inner_module")
    filepath = join_paths(inner_module_path, "foo", "bar.py")
    sys.path.append(parent_path(package_path))
    sys.path.append(parent_path(inner_module_path))
    expected_module_name = "inner_module.foo.bar"

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
    filepath = build_path("test_find_nonexistent_module_name", "bar.py")

    # when
    module_name = find_module_name(filepath)

    # then
    assert module_name is None
