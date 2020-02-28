import sys
from os import DirEntry
from os.path import basename, dirname, splitext
from pathlib import Path
from typing import Optional, Union


def find_module_name(
    filepath: Union[DirEntry, str], innermost: bool = False
) -> Optional[str]:
    """
    Utility function to find the Python module name of a python file.

    :param filepath:
        The absolute filepath as a DirEntry object or path string.
    :param innermost:
        (default: False) By default the outermost possible module name is returned.
        When this flag is set to True, the first found, innermost possible module name
        is then returned without further looking.
    :return:
        The module name string or None if no module was found for the specified
        filepath.
    """
    if isinstance(filepath, DirEntry):
        filepath = filepath.path

    valid_module_name = None
    module_name = splitext(basename(filepath))[0]
    full_path = Path(dirname(filepath))
    at_root = False
    while not at_root:
        if str(full_path) in sys.path:
            if innermost:
                return module_name
            else:
                valid_module_name = module_name
        module_name = f"{basename(full_path)}.{module_name}"
        at_root = full_path.parent == full_path.parent.parent
        full_path = Path(full_path.parent)
    return valid_module_name
