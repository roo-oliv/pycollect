========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pycollect/badge/?style=flat
    :target: https://readthedocs.org/projects/pycollect
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/allrod5/pycollect.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/allrod5/pycollect

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/allrod5/pycollect?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/allrod5/pycollect

.. |requires| image:: https://requires.io/github/allrod5/pycollect/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/allrod5/pycollect/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/allrod5/pycollect/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/allrod5/pycollect

.. |version| image:: https://img.shields.io/pypi/v/pycollect.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pycollect

.. |commits-since| image:: https://img.shields.io/github/commits-since/allrod5/pycollect/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/allrod5/pycollect/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pycollect.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pycollect

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pycollect.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pycollect

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pycollect.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pycollect


.. end-badges

Utility library for collection valid Python files recursively

* Free software: MIT license

Installation
============

::

    pip install pycollect

Documentation
=============


https://pycollect.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
