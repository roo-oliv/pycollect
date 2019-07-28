import inspect
import os
import re
from typing import Iterable, Optional, List


class PythonFileCollector:
    """
    PythonFileCollector class provides general configurations
    and utility methods for collecting Python files
    """

    _WILDCARD = "*"
    _INIT_FILE = "__init__.py"
    _DEFAULT_FILE_INCLUSION_PATTERNS = ["*.py"]
    _DEFAULT_FILE_EXCLUSION_PATTERNS = [".*", "~*"]
    _DEFAULT_DIR_INCLUSION_PATTERNS = ["*"]
    _DEFAULT_DIR_EXCLUSION_PATTERNS = [
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
    ]
    _DEFAULT_FILE_INCLUSION_REGEX_PATTERNS = [r".*\.py(?!.)"]
    _DEFAULT_FILE_EXCLUSION_REGEX_PATTERNS = [r"^\..*", r"^\~.*"]
    _DEFAULT_DIR_INCLUSION_REGEX_PATTERNS = [r".*"]
    _DEFAULT_DIR_EXCLUSION_REGEX_PATTERNS = [
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
    ]

    def __init__(
        self,
        enable_regex_patterns: bool = False,
        file_inclusion_patterns: Iterable[str] = None,
        file_exclusion_patterns: Iterable[str] = None,
        dir_inclusion_patterns: Iterable[str] = None,
        dir_exclusion_patterns: Iterable[str] = None,
    ):
        self._enable_regex_patterns = enable_regex_patterns
        self._file_inclusion_patterns = (
            file_inclusion_patterns
            if file_inclusion_patterns is not None
            else self._DEFAULT_FILE_INCLUSION_PATTERNS
            if not self._enable_regex_patterns
            else self._DEFAULT_FILE_INCLUSION_REGEX_PATTERNS
        )
        self._file_exclusion_patterns = (
            file_exclusion_patterns
            if file_exclusion_patterns is not None
            else self._DEFAULT_FILE_EXCLUSION_PATTERNS
            if not self._enable_regex_patterns
            else self._DEFAULT_FILE_EXCLUSION_REGEX_PATTERNS
        )
        self._dir_inclusion_patterns = (
            dir_inclusion_patterns
            if dir_inclusion_patterns is not None
            else self._DEFAULT_DIR_INCLUSION_PATTERNS
            if not self._enable_regex_patterns
            else self._DEFAULT_DIR_INCLUSION_REGEX_PATTERNS
        )
        self._dir_exclusion_patterns = (
            dir_exclusion_patterns
            if dir_exclusion_patterns is not None
            else self._DEFAULT_DIR_EXCLUSION_PATTERNS
            if not self._enable_regex_patterns
            else self._DEFAULT_DIR_EXCLUSION_REGEX_PATTERNS
        )

    @staticmethod
    def _get_caller_path() -> str:
        caller_filename = inspect.stack(2)[1]
        caller_abs_path = os.path.abspath(caller_filename)
        return os.path.dirname(caller_abs_path)

    def collect_python_files(
        self,
        search_path: Optional[str] = None,
        recursion_limit: Optional[int] = None,
        follow_symlinks: bool = True,
    ) -> List[os.DirEntry]:
        if search_path is None:
            search_path = self._get_caller_path()

        collected_files = []  # type: List[os.DirEntry]
        excluded_files = []  # type: List[os.DirEntry]
        collected_dirs = []  # type: List[os.DirEntry]
        excluded_dirs = []  # type: List[os.DirEntry]

        for entry in os.scandir(search_path):
            if entry.is_file(follow_symlinks=follow_symlinks):
                if self._should_exclude_file(entry):
                    excluded_files.append(entry)
                    continue
                collected_files.append(entry)
                continue
            if entry.is_dir(follow_symlinks=follow_symlinks):
                if self._should_exclude_dir(entry):
                    excluded_dirs.append(entry)
                    continue
                collected_dirs.append(entry)
                continue

        if recursion_limit is None or recursion_limit > 0:
            if recursion_limit is not None:
                recursion_limit -= 1
            for subdir in collected_dirs:
                if not any(
                    entry.is_file(follow_symlinks=follow_symlinks)
                    and self._INIT_FILE == entry.name
                    for entry in os.scandir(subdir.path)
                ):
                    continue
                collected_files += self.collect_python_files(
                    search_path=subdir.path,
                    recursion_limit=recursion_limit,
                    follow_symlinks=follow_symlinks,
                )

        return collected_files

    def _should_exclude_file(self, entry: os.DirEntry) -> bool:
        filename = entry.name  # type: str
        return any(
            self._matches_pattern(pattern, filename)
            for pattern in self._file_exclusion_patterns
        ) or all(
            not self._matches_pattern(pattern, filename)
            for pattern in self._file_inclusion_patterns
        )

    def _should_exclude_dir(self, entry: os.DirEntry) -> bool:
        dirname = entry.name  # type: str
        return any(
            self._matches_pattern(pattern, dirname)
            for pattern in self._dir_exclusion_patterns
        ) or all(
            not self._matches_pattern(pattern, dirname)
            for pattern in self._dir_inclusion_patterns
        )

    def _matches_pattern(self, pattern: str, name: str) -> bool:
        if self._enable_regex_patterns:
            return bool(re.match(pattern, name))
        splitted = pattern.split(self._WILDCARD)
        return name.startswith(splitted[0]) and name.endswith(splitted[-1])
