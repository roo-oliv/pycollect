import inspect
import os
import re
from typing import Iterable, Optional, Set


class PythonFileCollector:
    """
    PythonFileCollector provides method :meth:`collect` to collect files
    while applying exclusion patterns to files and directories.

    Exclusion patterns are in respect to file and directory names only, NOT taking
    into account the absolute nor the relative file or directory path.

    When not using regex patterns, a single wildcard, ``*``, can be used anywhere in
    a pattern to filter names "starting with" and/or "ending with". Also, a single
    exclamation mark, ``!``, can be used at the beginning of the pattern to negate it.
    These only applies when the parameter ``use_regex_patterns`` is ``False``.

    .. note::
        Using regex patterns may be slower as it consumes more CPU.

    :param use_regex_patterns:
        (default: ``False``) flag to indicate whether or not to use regex to match
        patterns. When this flag it set to ``False`` the ``*`` character is interpreted
        as wildcard and patterns starting with the ``!`` character are negated.
    :param additional_file_exclusion_patterns:
        (default: ``None``) additional patterns to filter out of collection files. In
        addition to the PythonFileCollector._DEFAULT_FILE_EXCLUSION_PATTERNS or
        PythonFileCollector._DEFAULT_FILE_EXCLUSION_REGEX_PATTERNS any file that
        matches these patterns will be excluded from collection.
    :param additional_dir_exclusion_patterns:
        (default: ``None``) additional patterns to filter out of collection directories.
        In addition to the PythonFileCollector._DEFAULT_DIR_EXCLUSION_PATTERNS or
        PythonFileCollector._DEFAULT_DIR_EXCLUSION_REGEX_PATTERNS any directory that
        matches these patterns will be excluded from collection.
    """

    _WILDCARD = "*"
    _NEGATION = "!"
    #: The default set of file exclusion patterns.
    #:
    #: Are excluded by default:
    #:
    #: 1. Files without the ``.py`` extension;
    #: 2. Files starting with a dot (``.``); and
    #: 3. Files starting with a tilde (``~``).
    DEFAULT_FILE_EXCLUSION_PATTERNS = {"!*.py", ".*", "~*"}
    #: The default set of directory exclusion patterns.
    #:
    #: Are excluded by default:
    #:
    #: 1. Directories starting with a dot (``.``);
    #: 2. Directories ending with a tilde (``~``).
    #: 3. Directories with common names indicating auto-generated content, binaries,
    #:    cache and temporary content (e.g., ``__pycache__``, ``tmp``, ``dist``)
    DEFAULT_DIR_EXCLUSION_PATTERNS = {
        "__pycache__",
        "tmp",
        "build",
        "dist",
        "sdist",
        "wheelhouse",
        "develop-eggs",
        "parts",
        "eggs",
        "var",
        "htmlcov",
        "bin",
        "venv*",
        "pyvenv*",
        ".*",
        "*~",
    }
    _DEFAULT_FILE_EXCLUSION_REGEX_PATTERNS = {r"(?!(.*\.py(?!.)))", r"^\..*", r"^\~.*"}
    _DEFAULT_DIR_EXCLUSION_REGEX_PATTERNS = {
        r"^__pycache__(?!.)",
        r"^tmp(?!.)",
        r"^build(?!.)",
        r"^dist(?!.)",
        r"^sdist(?!.)",
        r"^wheelhouse(?!.)",
        r"^develop-eggs(?!.)",
        r"^parts(?!.)",
        r"^eggs(?!.)",
        r"^var(?!.)",
        r"^htmlcov(?!.)",
        r"^bin(?!.)",
        r"^venv.*",
        r"^pyvenv.*",
        r"^\..*",
        r".*~(?!.)",
    }

    def __init__(
        self,
        use_regex_patterns: bool = False,
        additional_file_exclusion_patterns: Iterable[str] = None,
        additional_dir_exclusion_patterns: Iterable[str] = None,
    ):
        self.enable_regex_patterns = use_regex_patterns
        if self.enable_regex_patterns:
            self.file_exclusion_patterns = (
                self._DEFAULT_FILE_EXCLUSION_REGEX_PATTERNS.copy()
            )
            self.dir_exclusion_patterns = (
                self._DEFAULT_DIR_EXCLUSION_REGEX_PATTERNS.copy()
            )
        else:
            self.file_exclusion_patterns = self.DEFAULT_FILE_EXCLUSION_PATTERNS.copy()
            self.dir_exclusion_patterns = self.DEFAULT_DIR_EXCLUSION_PATTERNS.copy()

        if additional_file_exclusion_patterns:
            self.file_exclusion_patterns.update(additional_file_exclusion_patterns)

        if additional_dir_exclusion_patterns:
            self.dir_exclusion_patterns.update(additional_dir_exclusion_patterns)

    @staticmethod
    def _get_caller_path() -> str:
        caller_filename = inspect.stack(2)[1]
        caller_abs_path = os.path.abspath(caller_filename)
        return os.path.dirname(caller_abs_path)

    def collect(
        self,
        search_path: Optional[str] = None,
        recursion_limit: Optional[int] = None,
        follow_symlinks: bool = True,
    ) -> Set[os.DirEntry]:
        """
        Method to perform Python files collection in the specified search path,
        respecting exclusion patterns set to the class object.

        :param search_path:
            (default: uses the caller's path) absolute or relative path from which to
            search for when collecting Python files. This is expected to be a directory.
        :param recursion_limit:
            (default: None) directory recursion limit. The directory indicated by the
            :param search_path: is considered level 0 of recursion.
        :param follow_symlinks:
            (default: True) boolean indicating whether or not to follow symbolic links
            when collecting Python files.
        :return:
            A set of DirEntry instances referring to each collected file is returned.
        """
        if search_path is None:
            search_path = self._get_caller_path()

        collected_files = set()  # type: Set[os.DirEntry]
        excluded_files = set()  # type: Set[os.DirEntry]
        collected_dirs = set()  # type: Set[os.DirEntry]
        excluded_dirs = set()  # type: Set[os.DirEntry]

        for entry in os.scandir(search_path):
            if entry.is_file(follow_symlinks=follow_symlinks):
                if self._should_exclude_file(entry):
                    excluded_files.add(entry)
                    continue
                collected_files.add(entry)
                continue
            if entry.is_dir(follow_symlinks=follow_symlinks):
                if self._should_exclude_dir(entry):
                    excluded_dirs.add(entry)
                    continue
                collected_dirs.add(entry)
                continue

        if recursion_limit is None or recursion_limit > 0:
            if recursion_limit is not None:
                recursion_limit -= 1
            for subdir in collected_dirs:
                collected_files.update(
                    self.collect(
                        search_path=subdir.path,
                        recursion_limit=recursion_limit,
                        follow_symlinks=follow_symlinks,
                    )
                )

        return collected_files

    def _should_exclude_file(self, entry: os.DirEntry) -> bool:
        filename = entry.name  # type: str
        return any(
            self._matches_pattern(pattern, filename)
            for pattern in self.file_exclusion_patterns
        )

    def _should_exclude_dir(self, entry: os.DirEntry) -> bool:
        dirname = entry.name  # type: str
        return any(
            self._matches_pattern(pattern, dirname)
            for pattern in self.dir_exclusion_patterns
        )

    def _matches_pattern(self, pattern: str, name: str) -> bool:
        if self.enable_regex_patterns:
            return bool(re.match(pattern, name))
        negate = False
        if pattern.startswith(self._NEGATION):
            negate = True
            pattern = pattern[1:]
        splitted = pattern.split(self._WILDCARD)
        matches_pattern = name.startswith(splitted[0]) and name.endswith(splitted[-1])
        return matches_pattern if not negate else not matches_pattern
