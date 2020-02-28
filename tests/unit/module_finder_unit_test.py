import sys

from pycollect import find_module_name


def test_find_outermost_module_name():
    """
    This test intents to ensure that the utility function `find_module_name` will
    find the correct outermost module name for a given filepath by default
    """
    # given
    package_path = "/system_path/some_package"
    inner_module_path = package_path + "/inner_module"
    filepath = inner_module_path + "/foo/bar.py"
    sys.path.append(package_path.rsplit("/", maxsplit=1)[0])
    sys.path.append(inner_module_path.rsplit("/", maxsplit=1)[0])
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
    package_path = "/system_path/some_package"
    inner_module_path = package_path + "/inner_module"
    filepath = inner_module_path + "/foo/bar.py"
    sys.path.append(package_path.rsplit("/", maxsplit=1)[0])
    sys.path.append(inner_module_path.rsplit("/", maxsplit=1)[0])
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
    filepath = "/not_in_python_path_module/bar.py"
    if filepath.rsplit("/", maxsplit=1)[0] in sys.path:
        sys.path.remove(filepath.rsplit("/", maxsplit=1)[0])

    # when
    module_name = find_module_name(filepath)

    # then
    assert module_name is None
