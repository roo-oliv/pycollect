.. _pycollect:

pycollect
=========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - license
      - |license|
    * - docs
      - |docs|
    * - tests
      - |build| |requires| |coveralls|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |platforms|
.. |docs| image:: https://img.shields.io/badge/docs-GitHub%20Pages-black
    :target: https://allrod5.github.io/pycollect/
    :alt: Documentation Status

.. |build| image:: https://github.com/allrod5/pycollect/workflows/build/badge.svg
    :alt: Build Status
    :target: https://github.com/allrod5/pycollect/actions

.. |requires| image:: https://requires.io/github/allrod5/pycollect/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/allrod5/pycollect/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/allrod5/pycollect/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/allrod5/pycollect

.. |version| image:: https://img.shields.io/pypi/v/pycollect.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pycollect

.. |wheel| image:: https://img.shields.io/pypi/wheel/pycollect.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pycollect

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pycollect.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pycollect

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pycollect.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pycollect

.. |license| image:: https://img.shields.io/github/license/allrod5/pycollect
    :alt: GitHub license
    :target: https://github.com/allrod5/pycollect/blob/master/LICENSE

.. |platforms| image:: https://img.shields.io/badge/platforms-windows%20%7C%20macos%20%7C%20linux-lightgrey
    :alt: Supported Platforms
    :target: https://github.com/allrod5/pycollect/blob/master/.github/workflows/build.yml#L11


.. end-badges

Utility library dealing with Python files.

**Features**
 * Collect Python files recursively from a given directory
 * Find the Python module name respective to a Python file

Installation
============

.. code-block:: bash

    pip install pycollect


Basic Usage
===========

Collect Python files
--------------------

.. code-block:: python

    collector = PythonFileCollector()
    python_files = collector.collect()

When no explicit directory is given the parent folder of caller's file will be used.

It is possible to define custom exclusion patterns. `See the docs for more <https://allrod5.github.io/pycollect/reference/pycollect.html#pycollect.PythonFileCollector>`__.

Get the module name of a Python file
------------------------------------

.. code-block:: python

    module_name = find_module_name(filepath)

As there can be multiple valid module names for a given file, by default the outermost
module name is returned. The inverse behaviour can be enabled with the ``innermost``
parameter. `See the docs for more <https://allrod5.github.io/pycollect/reference/pycollect.html#pycollect.find_module_name>`__.

Documentation
=============

See the complete docs at `allrod5.github.io/pycollect <https://allrod5.github.io/pycollect/>`__.

`Integration tests <https://github.com/allrod5/pycollect/tree/master/tests/integration>`__
can be pretty helpful to understand pycollect usage more in-depth too.

See also
--------

* `CONTRIBUTING <https://allrod5.github.io/pycollect/contributing.html>`__: Bug reports, feature requests, documentation & pull requests.
* `CHANGELOG <https://allrod5.github.io/pycollect/changelog.html>`__: See what's changed in each version.
* `AUTHORS <https://allrod5.github.io/pycollect/authors.html>`__: Know who's behind the project.
