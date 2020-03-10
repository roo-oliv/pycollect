.. currentmodule:: pycollect

=====
Usage
=====

Collect Python files
====================

Collecting Python files is really straight forward:

.. code-block:: python

    from pycollect import PythonFileCollector

    collector = PythonFileCollector()
    files = collector.collect()

.. note::
    By default, files are collected from the current execution's working directory.

At each :meth:`~PythonFileCollector.collect` call a custom search path can be specified:

.. code-block:: python

    from pycollect import PythonFileCollector

    collector = PythonFileCollector()
    files_foo = collector.collect("../foo")
    files_bar = collector.collect("../bar")

.. note::
    Search paths can be either, relative or absolute. Relative directories are **not**
    referring to the declaration file's location as root but to the current working
    directory.

Beyond default exclusion patterns for file and directory names the
:class:`PythonFileCollector` class accepts additional patterns:

.. code-block:: python

    from pycollect import PythonFileCollector

    collector = PythonFileCollector(
        additional_file_exclusion_patterns=["*_test.py", "foo*", "Bar_*qux.py"],
        additional_dir_exclusion_patterns=["*tests", "test*"],
    )
    files = collector.collect()

.. note::
    By default the simple pattern syntax is used to match file and directory names.
    The ``*`` character is considered a wildcard and can be used only once per pattern.
    The ``!`` character at the beginning of the pattern negates it.

.. note::
    Regex syntax can be enabled instead of the simple pattern syntax passing
    ``regex=True`` as parameter to the :class:`PythonFileCollector`. This may impact
    collection time performance though.


Find a file's Python module
===========================

Given a file one can easily find its referring Python module using the
:meth:`find_module_name` utility method:

.. code-block:: python

    from pycollect import find_module_name

    module_name = find_module_name("/path/to/file.py")

.. note::
    As a file can refer to multiple modules, by default, the outermost module found is
    returned. This behavior can be inverted by passing ``innermost=True`` as parameter
    to :meth:`find_module_name`.

More
====

For more refer to the `pycollect reference section <https://allrod5.github.io/pycollect/reference/pycollect.html>`_.
