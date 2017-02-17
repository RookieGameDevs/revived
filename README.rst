=======
Revived
=======

.. image:: https://img.shields.io/pypi/v/revived.svg
    :target: https://badge.fury.io/py/revived
    :alt: pypi latest version

.. image:: https://img.shields.io/pypi/l/revived.svg
    :target: https://badge.fury.io/py/revived
    :alt: pypi packge license

.. image:: https://img.shields.io/requires/github/RookieGameDevs/revived.svg
    :target: https://requires.io/github/RookieGameDevs/revived/requirements/?branch=master
    :alt: dependencies status

.. image:: https://img.shields.io/travis/RookieGameDevs/revived.svg
    :target: https://travis-ci.org/RookieGameDevs/revived
    :alt: travis build status

.. image:: https://img.shields.io/codecov/c/github/RookieGameDevs/revived.svg
    :target: https://codecov.io/gh/RookieGameDevs/revived
    :alt: coverage status

.. image:: https://readthedocs.org/projects/revived/badge/?version=latest
    :target: http://revived.readthedocs.io/en/latest/?badge=latest
    :alt: documentation status

---------------------------------------------------------------------
A predictable state container for python *heavily* inspired by Redux_
---------------------------------------------------------------------

While not being a *strict 1:1 port* of `Redux API`_, **Revived** is supposed to
do pretty much the same job in the most pythonic way possible.

**NOTE**: I needed this piece of code to work with the **latest python available
at the moment** (3.6). While I am not really caring about other versions, the
Travis build is running the test suites on **all the 3.5+ versions**, including
the dev ones.

Contents
--------
* Documentation_
* Installation_
* Examples_
* Contribute_

Documentation
-------------

You can find the compiled documentation here:

* http://revived.readthedocs.io
* http://revived.rtfd.io

Installation
------------

**Revived** package is available on pypi: to install it use the following
command::

   pip install revived

Examples
--------

Usage examples are **coming soon**.

Contribute
----------

#. Clone the repository.
#. Create the virtualenv.

   * using virtualenv_::

      virtualenv ENV
      bin/activate

   * using virtualfish_::

      vf new ENV
      # optional: automatically load the virtualenv when entering the dir
      vf connect

#. Update pip and install pip-tools::

    pip install --upgrade pip  # pip-tools needs pip==6.1 or higher (!)
    pip install pip-tools

#. Install the dependencies::

    pip install -r requirements.txt

#. Build the documentation::

    cd docs
    make html  # or whatever format you prefer

#. Work on the revived module. This project uses pip-tools_ so you want to add
   your new direct dependencies in ``requirements.in`` and then compile the
   ``requirements.txt`` using::

       pip-compile requirements.in

#. Write tests.
#. Run tests::

    # to have coverage in command line
    pytest --cov revived --pep8 revived tests

    # to have html coverage file in the htmlcov directory
    pytest --cov revived --cov-report html --pep8 revived tests

#. Check type hints::

    mypy revived tests

#. Create a pull request.
#. Profit :)

.. _Redux: http://redux.js.org/
.. _`Redux API`: Redux_
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _virtualfish: http://virtualfish.readthedocs.io/en/latest/
.. _pip-tools: https://github.com/jazzband/pip-tools
